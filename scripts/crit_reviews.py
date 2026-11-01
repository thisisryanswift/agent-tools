"""Owned Crit v0.23.1 reviews. Linux process generations and sockets are verified.

The durable registry is independent from ~/.crit/sessions. All mutations serialize
under flock; a browser router should call verified() before opening an upstream.
"""
import contextlib
import fcntl
import http.client
import json
import os
from pathlib import Path
import re
import secrets
import shutil
import socket
import subprocess
import time
import urllib.request

VERSION = '0.23.1'
ID = re.compile(r'^[0-9a-f]{12}$')

class ReviewError(RuntimeError):
    pass

def process_generation(pid):
    p = Path('/proc') / str(pid)
    stat = (p/'stat').read_text().rsplit(')', 1)[1].split()
    if stat[0] == 'Z':
        raise ProcessLookupError(pid)
    return {'pid':pid, 'start_time':stat[19], 'exe':str((p/'exe').resolve(strict=True))}

def socket_inode(pid, port):
    inodes = set()
    for line in Path('/proc/net/tcp').read_text().splitlines()[1:]:
        fields = line.split()
        if fields[1] == f'0100007F:{port:04X}' and fields[3] == '0A':
            inodes.add(fields[9])
    for fd in (Path('/proc')/str(pid)/'fd').iterdir():
        try:
            target = os.readlink(fd)
        except FileNotFoundError:
            continue
        for inode in inodes:
            if target == f'socket:[{inode}]':
                return inode
    raise ReviewError('Daemon does not own the expected loopback listening socket')

class Registry:
    def __init__(self, root=None, binary='crit', domain='crit.wharfi.sh'):
        self.root = Path(root or Path.home()/'.local/share/crit-reviews').expanduser().resolve()
        self.root.mkdir(parents=True, exist_ok=True, mode=0o700)
        self.binary = str(Path(shutil.which(binary) or binary).resolve())
        if not re.fullmatch(r'[a-z0-9]+(?:[.-][a-z0-9]+)*', domain):
            raise ReviewError('Invalid public hostname domain')
        self.domain = domain
        self.opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    @contextlib.contextmanager
    def locked(self, blocking=True):
        with (self.root/'registry.lock').open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | (0 if blocking else fcntl.LOCK_NB))
            yield
    def _read(self):
        path = self.root/'registry.json'
        return json.loads(path.read_text()) if path.exists() else {'reviews':{},'conversations':{}}
    def _save(self, data):
        path = self.root/'registry.json'
        temp = self.root/('registry.'+secrets.token_hex(8)+'.tmp')
        with temp.open('x') as f:
            json.dump(data,f,indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp,path)
        fd=os.open(self.root,os.O_DIRECTORY)
        try: os.fsync(fd)
        finally: os.close(fd)
    def list(self):
        return list(self._read()['reviews'].values())
    def get(self, review_id):
        if not ID.fullmatch(review_id): raise ReviewError('Expected an explicit 12-hex review ID')
        r=self._read()['reviews'].get(review_id)
        if r is None: raise ReviewError('Unknown review ID')
        return r
    def _http(self,r,path,payload=None,timeout=5):
        port=r['generation']['port']
        if type(port) is not int or not 0 < port < 65536: raise ReviewError('Invalid daemon port')
        body=None if payload is None else json.dumps(payload).encode()
        req=urllib.request.Request(f'http://127.0.0.1:{port}{path}',data=body,headers={'Host':r['public_url'].split('://',1)[1], 'Content-Type':'application/json'})
        with self.opener.open(req,timeout=timeout) as response: return json.load(response)
    def _owned(self,r):
        g=r.get('generation')
        if not g: raise ReviewError('Review is stopped; start the saved review explicitly')
        try: current=process_generation(g['pid'])
        except (FileNotFoundError,ProcessLookupError): raise ReviewError('Review is inactive; start it to resume')
        if any(current[k]!=g[k] for k in current): raise ReviewError('Process generation conflict; refusing stale review target')
        p=Path('/proc')/str(g['pid'])
        argv=(p/'cmdline').read_bytes().split(b'\0')
        if b'_serve' not in argv or r['id'].encode() not in argv or str((p/'cwd').resolve())!=r['cwd']:
            raise ReviewError('Daemon process identity conflict')
        if socket_inode(g['pid'],g['port']) != g['socket_inode']: raise ReviewError('Daemon socket generation conflict')
    @staticmethod
    def _effective_scope(session):
        scope={key:session.get(key) for key in ('mode','base_ref','base_branch_name','focus')}
        # Git's changed-file list legitimately evolves between revisions. Explicit
        # document selection does not: preserve its paths, not volatile metadata.
        if session.get('mode')=='files':
            scope['files']=sorted(file['path'] for file in session['files'])
        return scope
    def _verified(self,r,check_branch=True,capture_scope=False,check_scope=True):
        self._owned(r)
        if check_branch and self._branch(r['cwd']) != r['branch']:
            raise ReviewError('Saved review branch changed; create a new explicit review')
        session=self._http(r,'/api/session')
        config=self._http(r,'/api/config')
        if session.get('session_key')!=r['id'] or session.get('cwd')!=r['cwd'] or session.get('mode')!=r['scope']['mode'] or config.get('version')!='v'+VERSION or config.get('review_path')!=str(Path(r['output'])/'reviews'/r['id']):
            raise ReviewError('Crit identity or compatibility conflict')
        effective_scope=self._effective_scope(session)
        if capture_scope and 'effective_scope' not in r:
            r['effective_scope']=effective_scope
        elif check_scope and r.get('effective_scope')!=effective_scope:
            raise ReviewError('Saved review scope changed; create a new explicit review')
        transient=Path.home()/'.crit/sessions'/f"{r['id']}.json"
        entry=json.loads(transient.read_text())
        if entry.get('pid')!=r['generation']['pid'] or entry.get('port')!=r['generation']['port'] or entry.get('host')!='127.0.0.1' or entry.get('public_url')!=r['public_url']:
            raise ReviewError('Crit session registry identity conflict')
        result=dict(r)
        result['session']=session
        result['state']='active'
        return result
    def verified(self,review_id):
        r=self.get(review_id)
        result=self._verified(r)
        if self.get(review_id).get('generation') != r.get('generation'):
            raise ReviewError('Daemon generation changed during verification; retry')
        return result
    def remember(self, review_id, generation, session, activity):
        """Persist a live observation only while its verified generation still matches."""
        try:
            with self.locked(blocking=False):
                data=self._read()
                r=data['reviews'].get(review_id)
                if r is not None and r.get('generation')==generation:
                    r['last_known']={'round':session.get('review_round'),
                                     'activity':activity, 'observed_at':time.time()}
                    self._save(data)
        except BlockingIOError:
            pass  # A slow launcher operation must never delay the index.

    def request(self,review_id,path,payload=None,timeout=5):
        r=self.verified(review_id)
        return self._request_owned(r,path,payload,timeout)
    def _request_owned(self,r,path,payload=None,timeout=5,check_branch=True,check_scope=True):
        connection=http.client.HTTPConnection('127.0.0.1',r['generation']['port'],timeout=timeout)
        try:
            connection.connect()
            # Validate the established target before sending a mutation. Never
            # reconnect after validation: a recycled port is a different daemon.
            self._verified(r,check_branch=check_branch,check_scope=check_scope)
            if self.get(r['id']).get('generation') != r['generation']:
                raise ReviewError('Daemon generation changed during connection; retry')
            self._owned(r)
            body=None if payload is None else json.dumps(payload).encode()
            connection.request('GET' if payload is None else 'POST',path,body=body,
                               headers={'Host':r['public_url'].split('://',1)[1],
                                        'Content-Type':'application/json'})
            with connection.getresponse() as response:
                if response.status >= 400:
                    raise ReviewError(f'Crit request failed: HTTP {response.status}')
                return json.load(response)
        finally:
            connection.close()
    def wait(self,review_id,timeout=86400):
        self.get(review_id)  # validates the ID before using it as a filename
        with (self.root/f'{review_id}.wait.lock').open('a') as lock:
            try:
                fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
            except BlockingIOError:
                raise ReviewError('A completion client is already waiting for this review')
            result=self.request(review_id,'/api/review-cycle',{},timeout)
            if result.get('status') != 'finished':
                raise ReviewError('Review wait ended without Finish')
            return result
    @staticmethod
    def _branch(cwd):
        branch=subprocess.run(['git','symbolic-ref','--quiet','--short','HEAD'],cwd=cwd,text=True,capture_output=True).stdout.strip()
        if not branch:
            branch=subprocess.run(['git','rev-parse','HEAD'],cwd=cwd,text=True,capture_output=True).stdout.strip() or None
        return branch
    def start(self,conversation=None,cwd=None,files=(),base=None,revision_range=None,new=False,review_id=None):
        version=subprocess.check_output([self.binary,'--version'],text=True,timeout=5).splitlines()[0]
        if not re.match(r'^crit v0\.23\.1 \([^\n]*, ad3e10f\)$',version):
            raise ReviewError('Unsupported Crit binary; requires verified v0.23.1 (ad3e10f)')
        with self.locked():
            data=self._read()
            if review_id:
                if new or conversation or cwd or files or base or revision_range: raise ReviewError('Resume by ID without changing saved scope')
                r=data['reviews'].get(review_id)
                if r is None: raise ReviewError('Unknown review ID')
            else:
                if not conversation or not cwd: raise ReviewError('start requires explicit conversation and cwd (or saved review ID)')
                cwd=str(Path(cwd).resolve(strict=True))
                branch=self._branch(cwd)
                scope={'mode':'files' if files else 'git','files':[str((Path(cwd)/f).resolve(strict=True)) for f in files], 'base':base,'range':revision_range}
                key=None if new else data['conversations'].get(conversation)
                if key:
                    r=data['reviews'][key]
                    if any(r[k]!=v for k,v in [('cwd',cwd),('branch',branch),('scope',scope)]): raise ReviewError('Conversation branch or scope changed; use --new for a separate review')
                else:
                    key=secrets.token_hex(6)
                    r={'id':key,'conversation':conversation,'cwd':cwd,'branch':branch,'scope':scope,'output':str(self.root/'reviews'/key),'public_url':f'https://{key}.{self.domain}','created_at':time.time(),'generation':None}
                    data['reviews'][key]=r
                    data['conversations'][conversation]=key
                    self._save(data)
            if self._branch(r['cwd']) != r['branch']:
                raise ReviewError('Saved review branch changed; create a new explicit review')
            g=r.get('generation')
            if g:
                try: current=process_generation(g['pid'])
                except (FileNotFoundError,ProcessLookupError): current=None
                if current is not None: return self._verified(r)
            transient=Path.home()/'.crit/sessions'/f"{r['id']}.json"
            if transient.exists():
                entry=json.loads(transient.read_text())
                try: process_generation(entry['pid'])
                except (FileNotFoundError,ProcessLookupError): pass
                else: raise ReviewError('Existing Crit session process conflicts with saved review')
            with socket.socket() as sock:
                sock.bind(('127.0.0.1',0)); port=sock.getsockname()[1]
            args=[self.binary,'_serve','--session-key',r['id'],'--output',r['output'],'--host','127.0.0.1','--port',str(port),'--no-open','--public-url',r['public_url'],'--allow-unauthenticated-network']
            if r['scope']['base']: args+=['--base-branch',r['scope']['base']]
            if r['scope']['range']: args+=['--range',r['scope']['range']]
            args+=r['scope']['files']
            env=dict(os.environ,CRIT_NO_UPDATE_CHECK='1',CRIT_NO_INTEGRATION_CHECK='1'); env.pop('CRIT_PORT',None)
            with (self.root/f"{r['id']}.log").open('ab') as log:
                proc=subprocess.Popen(args,cwd=r['cwd'],env=env,stdout=log,stderr=log,start_new_session=True)
            # Persist the process generation before probing readiness, so interrupted
            # launches remain recognizable and can never start a competing daemon.
            r['generation']={**process_generation(proc.pid),'port':port,'socket_inode':None}
            self._save(data)
            for _ in range(150):
                if proc.poll() is not None: raise ReviewError(f"Crit exited during startup; see {self.root/r['id']}.log")
                try:
                    r['generation']['socket_inode']=socket_inode(proc.pid,port)
                    self._save(data)
                    result=self._verified(r,capture_scope=True)
                    self._save(data)
                    return result
                except (OSError,ValueError,ReviewError): time.sleep(.1)
            raise ReviewError('Crit readiness timeout; saved process retained for safe inspection')
    def stop(self,review_id):
        with self.locked():
            data=self._read(); r=data['reviews'].get(review_id)
            if r is None: raise ReviewError('Unknown review ID')
            if not r.get('generation'): return r
            try: process_generation(r['generation']['pid'])
            except (FileNotFoundError,ProcessLookupError):
                r['generation']=None; self._save(data); return r
            live=self._verified(r,check_branch=False,check_scope=False)
            r['last_known']={'round':live['session'].get('review_round'), 'activity':'Running', 'observed_at':time.time()}
            self._owned(r)
            self._request_owned(r,f"/api/shutdown?pid={r['generation']['pid']}",{},check_branch=False,check_scope=False)
            for _ in range(100):
                try: process_generation(r['generation']['pid'])
                except (FileNotFoundError,ProcessLookupError): break
                time.sleep(.05)
            else: raise ReviewError('Daemon shutdown timed out; process metadata retained')
            r['generation']=None; self._save(data); return r
