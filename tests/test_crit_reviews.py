"""Public launcher integration against the installed pinned Crit; HOME is unchanged."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time
import unittest
import sys

CLI = Path(__file__).resolve().parents[1] / 'scripts/crit-review.py'
BINARY = os.environ.get('CRIT_TEST_BINARY', '/home/rswift/.local/bin/crit')

@unittest.skipUnless(Path(BINARY).is_file(), 'installed pinned Crit required')
class Lifecycle(unittest.TestCase):
    def setUp(self):
        self.env = dict(os.environ, CRIT_SHARE_URL='http://127.0.0.1:1')
        self.tmp = tempfile.TemporaryDirectory(prefix='crit-launcher-test-')
        self.root = Path(self.tmp.name)
        self.repo = self.root / 'checkout'
        subprocess.run(['git','clone','--quiet','--shared',str(CLI.parents[1]),str(self.repo)],check=True)
        self.note=self.repo/'README.md'
        self.note.write_text(self.note.read_text()+'\nTemporary review fixture.\n')
        (self.repo/'.crit.config.json').write_text('{"disable_stats":true}')
    def cli(self,*args,ok=True):
        r = subprocess.run([sys.executable,str(CLI),'--registry',str(self.root/'registry'),'--binary',BINARY,*args],text=True,capture_output=True,timeout=30,env=self.env)
        if ok:
            self.assertEqual(r.returncode,0,r.stderr)
            return json.loads(r.stdout)
        self.assertNotEqual(r.returncode,0)
        return r.stderr
    def tearDown(self):
        if CLI.exists():
            try:
                for r in self.cli('list'):
                    self.cli('stop',r['id'])
            except Exception:
                self.tmp._finalizer.detach()
                raise
            else:
                self.tmp.cleanup()
        else:
            self.tmp.cleanup()
    def test_conversation_resumes_and_independent_conversations_do_not_alias(self):
        a=self.cli('start','--conversation','alpha','--cwd',str(self.repo))
        again=self.cli('start','--conversation','alpha','--cwd',str(self.repo))
        b=self.cli('start','--conversation','beta','--cwd',str(self.repo))
        self.assertEqual(a['id'],again['id'])
        self.assertNotEqual(a['id'],b['id'])
        self.assertNotEqual(a['generation']['port'],b['generation']['port'])

    def test_saved_id_rejects_changed_branch(self):
        a=self.cli('start','--conversation','branch','--cwd',str(self.repo))
        subprocess.run(['git','switch','-qc','changed-branch'],cwd=self.repo,check=True)
        self.assertIn('branch',self.cli('start','--review',a['id'],ok=False))

    def http(self,r,path,payload=None):
        import urllib.request
        opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
        req=urllib.request.Request(f"http://127.0.0.1:{r['generation']['port']}{path}",data=None if payload is None else json.dumps(payload).encode(),headers={'Content-Type':'application/json','Host':r['public_url'].split('://')[1]})
        with opener.open(req,timeout=5) as response:
            return json.load(response)

    def waiter(self,r):
        return subprocess.Popen([sys.executable,str(CLI),'--registry',str(self.root/'registry'),'--binary',BINARY,'wait',r['id'],'--timeout','12'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,env=self.env)

    def test_five_reviews_have_separate_comments_completion_restart_and_revision(self):
        reviews=[self.cli('start','--conversation',f'agent-{i}','--cwd',str(self.repo)) for i in range(5)]
        self.assertEqual(len({r['id'] for r in reviews}),5)
        for i,r in enumerate(reviews):
            self.cli('comment',r['id'],f'Feedback for agent {i}')
        for i,r in enumerate(reviews):
            self.assertEqual([c['body'] for c in self.http(r,'/api/comments')],[f'Feedback for agent {i}'])
        waits=[self.waiter(r) for r in reviews]
        try:
            time.sleep(.5)
            self.http(reviews[0],'/api/finish',{})
            out,err=waits[0].communicate(timeout=5)
            self.assertEqual(waits[0].returncode,0,err)
            self.assertIn('Feedback for agent 0',out)
            self.assertTrue(all(w.poll() is None for w in waits[1:]))
            for i in range(1,5):
                self.http(reviews[i],'/api/finish',{})
                out,err=waits[i].communicate(timeout=5)
                self.assertEqual(waits[i].returncode,0,err)
                self.assertIn(f'Feedback for agent {i}',out)
        finally:
            for w in waits:
                if w.poll() is None: w.terminate(); w.communicate(timeout=5)
        original=reviews[0]
        self.cli('stop',original['id'])
        self.assertFalse((Path.home()/'.crit/sessions'/f"{original['id']}.json").exists())
        restarted=self.cli('start','--review',original['id'])
        self.assertEqual(restarted['public_url'],original['public_url'])
        self.assertEqual(restarted['id'],original['id'])
        self.assertEqual([c['body'] for c in self.http(restarted,'/api/comments')],['Feedback for agent 0'])
        self.assertTrue(all(self.http(r,'/api/session')['session_key']==r['id'] for r in reviews[1:]))
        self.note.write_text(self.note.read_text()+'\nNext revision marker.\n')
        wait=self.waiter(reviews[1])
        try:
            time.sleep(.5)
            self.http(reviews[1],'/api/finish',{})
            out,err=wait.communicate(timeout=5)
            self.assertEqual(wait.returncode,0,err)
            self.assertIn('Feedback for agent 1',out)
            self.assertIn('Next revision marker.',json.dumps(self.http(reviews[1],'/api/file?path=README.md')))
            self.assertNotIn('Next revision marker.',json.dumps(self.http(reviews[2],'/api/file?path=README.md')))
        finally:
            if wait.poll() is None: wait.terminate(); wait.communicate(timeout=5)

    def test_concurrent_identity_creation_new_review_and_scope_guard(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
            reviews=list(pool.map(lambda _:self.cli('start','--conversation','same','--cwd',str(self.repo)),range(5)))
        self.assertEqual(len({r['id'] for r in reviews}),1)
        self.assertEqual(len({r['generation']['pid'] for r in reviews}),1)
        new=self.cli('start','--conversation','same','--cwd',str(self.repo),'--new')
        self.assertNotEqual(new['id'],reviews[0]['id'])
        self.assertEqual(len(self.cli('list')),2)
        self.assertIn('scope',self.cli('start','--conversation','same','--cwd',str(self.repo),'README.md',ok=False))
        self.assertIn('conversation',self.cli('start','--cwd',str(self.repo),ok=False))

    def test_document_review_and_git_range(self):
        doc=self.cli('start','--conversation','document','--cwd',str(self.repo),'README.md')
        self.assertEqual(doc['session']['mode'],'files')
        self.cli('comment',doc['id'],'Document feedback')
        self.cli('stop',doc['id'])
        resumed=self.cli('start','--review',doc['id'])
        self.assertEqual([c['body'] for c in self.http(resumed,'/api/comments')],['Document feedback'])
        ranged=self.cli('start','--conversation','range','--cwd',str(self.repo),'--range','HEAD~1..HEAD')
        self.assertEqual(ranged['session']['mode'],'git')

    def test_unverified_binary_is_rejected_before_launch(self):
        binary=self.root/'unverified-crit'
        binary.write_text('#!/bin/sh\necho "crit v0.23.2 (unknown)"\n')
        binary.chmod(0o700)
        r=subprocess.run([sys.executable,str(CLI),'--registry',str(self.root/'registry'),'--binary',str(binary),'start','--conversation','bad','--cwd',str(self.repo)],text=True,capture_output=True)
        self.assertNotEqual(r.returncode,0)
        self.assertIn('Unsupported Crit binary',r.stderr)
        self.assertEqual(self.cli('list'),[])

    def test_stale_generation_refuses_stop_and_resume_without_touching_daemon(self):
        r=self.cli('start','--conversation','stale','--cwd',str(self.repo))
        path=self.root/'registry/registry.json'
        original=path.read_text()
        try:
            data=json.loads(original)
            data['reviews'][r['id']]['generation']['start_time']='0'
            path.write_text(json.dumps(data))
            self.assertIn('generation conflict',self.cli('stop',r['id'],ok=False))
            self.assertIn('generation conflict',self.cli('start','--review',r['id'],ok=False))
            self.assertEqual(self.http(r,'/api/session')['session_key'],r['id'])
            data=json.loads(original)
            data['reviews'][r['id']]['generation']['socket_inode']='0'
            path.write_text(json.dumps(data))
            self.assertIn('socket generation conflict',self.cli('stop',r['id'],ok=False))
            self.assertEqual(self.http(r,'/api/session')['session_key'],r['id'])
        finally:
            path.write_text(original)

    def test_second_waiter_is_rejected_without_advancing_the_round(self):
        r=self.cli('start','--conversation','wait-lock','--cwd',str(self.repo))
        first=self.waiter(r)
        try:
            time.sleep(.4)
            self.assertIn('already waiting',self.cli('wait',r['id'],'--timeout','0.3',ok=False))
        finally:
            self.http(r,'/api/finish',{})
            first.communicate(timeout=5)

    def test_mutations_never_reconnect_to_replacement_listener(self):
        # Inject only at Python's HTTP transport boundary, in a real CLI process.
        # The first POST replaces this test's real Crit, before request() can send.
        wrapper=self.root/'network-race.py'
        wrapper.write_text('''import http.client, http.server, json, os, runpy, signal, sys, threading, time
from pathlib import Path
cli, pid, port, receipt = sys.argv[1:5]
sys.argv = [cli] + sys.argv[5:]
sys.path.insert(0, str(Path(cli).parent))
original = http.client.HTTPConnection.request
swapped = False
class Sink(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        Path(receipt).write_bytes(self.rfile.read(int(self.headers.get('Content-Length', '0'))))
        self.send_response(200); self.end_headers(); self.wfile.write(b'{"status":"finished"}')
    def log_message(self, *args): pass
def request(connection, method, url, *args, **kwargs):
    global swapped
    if method == 'POST' and not swapped:
        swapped = True
        os.kill(int(pid), signal.SIGTERM)
        for _ in range(100):
            try:
                server = http.server.HTTPServer(('127.0.0.1', int(port)), Sink)
                break
            except OSError: time.sleep(.02)
        else: raise RuntimeError('Fixture could not bind replacement listener')
        threading.Thread(target=server.serve_forever, daemon=True).start()
    return original(connection, method, url, *args, **kwargs)
http.client.HTTPConnection.request = request
runpy.run_path(cli, run_name='__main__')
''')
        for command in ('comment','wait','stop'):
            with self.subTest(command=command):
                r=self.cli('start','--conversation','race-'+command,'--cwd',str(self.repo))
                receipt=self.root/(command+'.received')
                args=[command,r['id']]
                if command=='comment': args+=['Private race feedback']
                if command=='wait': args+=['--timeout','1']
                proc=subprocess.run([sys.executable,str(wrapper),str(CLI),str(r['generation']['pid']),str(r['generation']['port']),str(receipt),'--registry',str(self.root/'registry'),'--binary',BINARY,*args],text=True,capture_output=True,env=self.env,timeout=15)
                self.assertFalse(receipt.exists(),f'{command} sent a mutation to an unrelated listener')
                self.assertNotEqual(proc.returncode,0,proc.stdout)

    def test_native_scope_mutation_blocks_saved_resume_and_wait(self):
        mutations=[('/api/base-branch',{'ref':'HEAD~1'}),
                   ('/api/focus',{'kind':'range','base_sha':'HEAD~1','head_sha':'HEAD'})]
        for i,(endpoint,payload) in enumerate(mutations):
            with self.subTest(endpoint=endpoint):
                r=self.cli('start','--conversation',f'scope-drift-{i}','--cwd',str(self.repo))
                self.http(r,endpoint,payload)
                self.assertIn('scope',self.cli('start','--review',r['id'],ok=False))
                self.assertIn('scope',self.cli('wait',r['id'],'--timeout','.2',ok=False))
                stopped=self.cli('stop',r['id'])
                self.assertIsNone(stopped['generation'])
                self.assertEqual(stopped['scope'],r['scope'])
                self.assertEqual(stopped['public_url'],r['public_url'])
