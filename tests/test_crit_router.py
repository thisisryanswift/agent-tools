"""HTTP routing integration with the installed pinned Crit and owned launcher."""
import concurrent.futures
import http.client
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import time
import unittest

CLI=Path(__file__).resolve().parents[1]/'scripts/crit-review.py'
BINARY=os.environ.get('CRIT_TEST_BINARY','/home/rswift/.local/bin/crit')

@unittest.skipUnless(Path(BINARY).is_file(),'installed pinned Crit required')
class Router(unittest.TestCase):
    def setUp(self):
        self.env=dict(os.environ,CRIT_SHARE_URL='http://127.0.0.1:1')
        self.tmp=tempfile.TemporaryDirectory(prefix='crit-router-test-')
        self.root=Path(self.tmp.name)
        self.repo=self.root/'checkout'
        subprocess.run(['git','clone','--quiet','--shared',str(CLI.parents[1]),str(self.repo)],check=True)
        (self.repo/'README.md').write_text('Router review fixture.\n')
        (self.repo/'.crit.config.json').write_text('{"disable_stats":true}')
        with socket.socket() as s:
            s.bind(('127.0.0.1',0)); self.port=s.getsockname()[1]
        self.router=subprocess.Popen([sys.executable,str(CLI),'--registry',str(self.root/'registry'),'--binary',BINARY,'serve','--port',str(self.port),'--index-host','validation.crit.wharfi.sh'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,env=self.env)
        for _ in range(100):
            if self.router.poll() is not None:
                self.fail(self.router.communicate()[1])
            try:
                with socket.create_connection(('127.0.0.1',self.port),timeout=.1): break
            except OSError: time.sleep(.05)
        else: self.fail('Router did not listen')
    def cli(self,*args):
        r=subprocess.run([sys.executable,str(CLI),'--registry',str(self.root/'registry'),'--binary',BINARY,*args],text=True,capture_output=True,timeout=30,env=self.env)
        self.assertEqual(r.returncode,0,r.stderr)
        return json.loads(r.stdout)
    def tearDown(self):
        self.router.terminate(); self.router.communicate(timeout=5)
        for r in self.cli('list'): self.cli('stop',r['id'])
        self.tmp.cleanup()
    def request(self,host,path='/',body=None,method=None):
        c=http.client.HTTPConnection('127.0.0.1',self.port,timeout=5)
        headers={'Host':host}
        if body is not None: headers['Content-Type']='application/json'
        try:
            c.request(method or ('GET' if body is None else 'POST'),path,None if body is None else json.dumps(body),headers)
            r=c.getresponse()
            return r.status,r.read()
        finally:
            c.close()
    def start(self,name):
        r=self.cli('start','--conversation',name,'--cwd',str(self.repo))
        return r,r['public_url'].split('://')[1]
    def test_five_hostnames_load_their_own_ui_files_and_comments(self):
        reviews=[self.start(f'agent-{i}') for i in range(5)]
        def exercise(item):
            i,(r,host)=item
            self.assertEqual(self.request(host)[0],200)
            status,session=self.request(host,'/api/session')
            self.assertEqual(status,200)
            self.assertEqual(json.loads(session)['session_key'],r['id'])
            self.assertIn(b'Router review fixture',self.request(host,'/api/file?path=README.md')[1])
            self.assertEqual(self.request(host,'/api/comments',{'body':f'Router feedback {i}','author':'Reviewer'})[0],201)
            self.assertEqual([c['body'] for c in json.loads(self.request(host,'/api/comments')[1])],[f'Router feedback {i}'])
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
            list(pool.map(exercise,enumerate(reviews)))

    def event_stream(self,host):
        c=http.client.HTTPConnection('127.0.0.1',self.port,timeout=3)
        c.request('GET','/api/events',headers={'Host':host})
        r=c.getresponse()
        self.assertEqual(r.status,200)
        self.assertEqual(r.getheader('Content-Type'),'text/event-stream')
        self.assertEqual(r.readline(),b':\n')
        self.assertEqual(r.readline(),b'\n')
        return c,r

    def test_events_and_completion_stream_promptly_and_only_to_their_review(self):
        reviews=[self.start(f'stream-{i}') for i in range(2)]
        streams=[self.event_stream(host) for _,host in reviews]
        def finish_event(response):
            while True:
                line=response.readline()
                if not line: self.fail('Event stream ended before finish')
                if line.startswith(b'event: finish'): return line
        for i,(_,host) in enumerate(reviews):
            self.request(host,'/api/comments',{'body':f'Keep daemon alive {i}','author':'Reviewer'})
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            events=[pool.submit(finish_event,response) for _,response in streams]
            waits=[pool.submit(self.request,host,'/api/wait-for-event') for _,host in reviews]
            try:
                time.sleep(.3)
                self.request(reviews[0][1],'/api/finish',{})
                self.assertIn(b'finish',events[0].result(timeout=2))
                self.assertEqual(json.loads(waits[0].result(timeout=2)[1])['type'],'finish')
                self.assertFalse(events[1].done())
                self.assertFalse(waits[1].done())
            finally:
                self.request(reviews[1][1],'/api/finish',{})
                for future in events+waits: future.result(timeout=3)
                for c,r in streams: r.close(); c.close()

    def test_idle_browser_disconnect_releases_upstream_event_subscription(self):
        _,host=self.start('disconnect')
        c,r=self.event_stream(host)
        self.assertTrue(json.loads(self.request(host,'/api/health')[1])['browser_clients'])
        r.close(); c.close()
        for _ in range(30):
            if not json.loads(self.request(host,'/api/health')[1])['browser_clients']: break
            time.sleep(.05)
        else: self.fail('Idle disconnected browser still has an upstream subscription')

    def test_browser_cannot_mutate_scope_advance_rounds_shutdown_or_upload(self):
        r,host=self.start('restricted')
        for path in ('/live','/live/example','/preview','/preview-content/file',
                     '/api/shutdown','/api/%73hutdown', '/ignored/../api/shutdown',
                     '/api/base-branch','/api/focus','/api/review-cycle','/api/round-complete',
                     '/api/project-prompts/trust','/api/agent/request','/api/share','/api/share/reshare','/api/share-url','/api/share-policy'):
            with self.subTest(path=path):
                self.assertEqual(self.request(host,path,{} )[0],403)
        self.assertEqual(self.request(host,'/api/session')[0],200)
        self.assertEqual(self.request(host,'/api/branches')[0],200)

    def test_stopped_and_stale_routes_fail_while_other_reviews_continue_and_restart_keeps_host(self):
        a,host=self.start('restarting')
        b,other=self.start('other')
        self.cli('stop',a['id'])
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            responses=list(pool.map(lambda h:self.request(h,'/api/session'),[host,other,host,other]))
        self.assertEqual([status for status,_ in responses],[503,200,503,200])
        resumed=self.cli('start','--review',a['id'])
        self.assertEqual(resumed['public_url'],a['public_url'])
        self.assertNotEqual(resumed['generation']['pid'],a['generation']['pid'])
        self.assertEqual(json.loads(self.request(host,'/api/session')[1])['session_key'],a['id'])
        registry=self.root/'registry/registry.json'
        saved=registry.read_text()
        try:
            data=json.loads(saved)
            data['reviews'][a['id']]['generation']['port']=b['generation']['port']
            registry.write_text(json.dumps(data))
            self.assertEqual(self.request(host,'/api/session')[0],503)
            self.assertEqual(json.loads(self.request(other,'/api/session')[1])['session_key'],b['id'])
        finally:
            registry.write_text(saved)

    def test_only_exact_registered_review_hosts_and_origin_targets_are_routed(self):
        _,host=self.start('host-boundary')
        for unknown in ('unknown.crit.wharfi.sh','0123456789ab.crit.wharfi.sh',host+'.evil',host.upper(),'127.0.0.1',host+':99999'):
            with self.subTest(host=unknown):
                self.assertIn(self.request(unknown,'/api/session')[0],(400,404))
        for target in ('http://127.0.0.1:1/api/session','//127.0.0.1:1/api/session'):
            self.assertEqual(self.request(host,target)[0],400)
        self.assertEqual(self.request(host+':443','/api/session')[0],200)
        self.assertEqual(self.request('crit.wharfi.sh')[0],200)
        self.assertEqual(self.request('validation.crit.wharfi.sh')[0],200)

    def test_requests_are_framed_explicitly_and_cannot_smuggle_a_second_host(self):
        _,host=self.start('framing')
        for extra in (f'Host: {host}\r\n', 'Content-Length: 0\r\nContent-Length: 0\r\n',
                      'Transfer-Encoding: chunked\r\n','Content-Length: -1\r\n'):
            with self.subTest(header=extra.split(':',1)[0]):
                with socket.create_connection(('127.0.0.1',self.port),timeout=3) as c:
                    c.sendall(f'GET /api/session HTTP/1.1\r\nHost: {host}\r\n{extra}\r\n'.encode())
                    self.assertIn(b' 400 ',c.recv(1024).split(b'\r\n',1)[0])
