"""Index HTTP behavior backed by the real pinned Crit daemon."""
import html
import http.client
import json
import os
from pathlib import Path
import re
import signal
import socket
import subprocess
import sys
import tempfile
import time
import unittest
from urllib.parse import urlencode

CLI=Path(__file__).resolve().parents[1]/'scripts/crit-review.py'
BINARY=os.environ.get('CRIT_TEST_BINARY','/home/rswift/.local/bin/crit')

@unittest.skipUnless(Path(BINARY).is_file(),'installed pinned Crit required')
class Index(unittest.TestCase):
    def setUp(self):
        self.env=dict(os.environ,CRIT_SHARE_URL='http://127.0.0.1:1')
        self.tmp=tempfile.TemporaryDirectory(prefix='crit-index-test-')
        self.root=Path(self.tmp.name)
        self.repo=self.root/'checkout'
        subprocess.run(['git','clone','--quiet','--shared',str(CLI.parents[1]),str(self.repo)],check=True,env=self.env)
        (self.repo/'README.md').write_text('Index review fixture.\n')
        (self.repo/'.crit.config.json').write_text('{"disable_stats":true}')
        with socket.socket() as s:
            s.bind(('127.0.0.1',0)); self.port=s.getsockname()[1]
        self.router=subprocess.Popen([sys.executable,str(CLI),'--registry',str(self.root/'registry'),'--binary',BINARY,'serve','--port',str(self.port)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,env=self.env)
        for _ in range(100):
            if self.router.poll() is not None: self.fail(self.router.communicate()[1])
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
    def request(self,path='/',method='GET',body=None,headers=None,host='crit.wharfi.sh'):
        c=http.client.HTTPConnection('127.0.0.1',self.port,timeout=10)
        try:
            c.request(method,path,body,{'Host':host,**(headers or {})})
            r=c.getresponse()
            return r.status,dict(r.getheaders()),r.read().decode()
        finally: c.close()
    def start(self,name):
        return self.cli('start','--conversation',name,'--cwd',str(self.repo))
    def token(self):
        return re.search(r'name="csrf" value="([a-f0-9]+)"',self.request()[2])[1]
    def resume(self,r,**extra):
        return self.request('/resume','POST',urlencode({'review':r['id'],'csrf':self.token(),**extra}),{'Content-Type':'application/x-www-form-urlencoded','Origin':'https://crit.wharfi.sh','Sec-Fetch-Site':'same-origin'})

    def test_empty_then_five_reviews_show_distinct_context_and_shared_checkout(self):
        self.assertIn('No saved reviews',self.request()[2])
        reviews=[self.start(f'Conversation {i}') for i in range(5)]
        status,headers,page=self.request()
        self.assertEqual(status,200)
        self.assertIn('text/html',headers['Content-Type'])
        for r in reviews:
            self.assertIn(f'href="{r["public_url"]}"',page)
            self.assertIn(r['conversation'],page)
        self.assertIn(str(self.repo),page)
        self.assertIn(reviews[0]['branch'],page)
        self.assertIn('Round',page)
        self.assertIn('Active',page)
        self.assertIn('Shared checkout',page)
        self.assertIn('other agents',page)
        self.assertIn('refresh',page)

    def test_resume_retains_hostname_comments_and_stopped_round_context(self):
        r=self.start('Saved <script>alert("label")</script>')
        host=r['public_url'].split('://')[1]
        self.cli('comment',r['id'],'Retain this saved feedback')
        page=self.request()[2]
        self.assertIn('Saved &lt;script&gt;',page)
        self.assertNotIn('<script>',page)
        self.cli('stop',r['id'])
        page=self.request()[2]
        self.assertIn('Stopped',page)
        self.assertIn('Round</dt><dd>1</dd>',page)
        self.assertIn('Last known:',page)
        status,headers,_=self.resume(r)
        self.assertEqual(status,303)
        self.assertEqual(headers['Location'],r['public_url'])
        self.assertEqual([c['body'] for c in json.loads(self.request('/api/comments',host=host)[2])],['Retain this saved feedback'])
        self.assertEqual(json.loads(self.request('/api/session',host=host)[2])['session_key'],r['id'])
        self.assertIn('Active',self.request()[2])

    def test_actions_reject_unknown_fields_origins_and_unregistered_targets(self):
        r=self.start('Guarded')
        self.cli('stop',r['id'])
        # Even blank unknown fields must not disappear during form parsing.
        self.assertEqual(self.resume(r,cwd='')[0],400)
        valid={'review':r['id'],'csrf':self.token()}
        headers={'Content-Type':'application/x-www-form-urlencoded','Origin':'https://crit.wharfi.sh','Sec-Fetch-Site':'same-origin'}
        for body in (urlencode({**valid,'command':'touch /tmp/not-allowed'}),urlencode({**valid,'upstream':'127.0.0.1:1'}),urlencode(valid)+'&review='+r['id']):
            self.assertEqual(self.request('/resume','POST',body,headers)[0],400)
        for change in ({'Origin':'https://evil.example'},{'Origin':'https://0123456789ab.crit.wharfi.sh'},{'Origin':'http://crit.wharfi.sh'},{'Sec-Fetch-Site':'cross-site'},{'Sec-Fetch-Site':''},{'Origin':''}):
            self.assertEqual(self.request('/resume','POST',urlencode(valid),{**headers,**change})[0],403)
        for token in ('wrong','☃'):
            self.assertEqual(self.request('/resume','POST',urlencode({**valid,'csrf':token}),headers)[0],403)
        self.assertEqual(self.resume({'id':'0123456789ab'})[0],404)
        for method,path in (('GET','/resume'),('POST','/'),('DELETE','/'),('PUT','/resume'),('GET','/unknown'),('GET','/?cwd=/tmp')):
            self.assertIn(self.request(path,method)[0],(400,404,405))
        self.assertIsNone(self.cli('show',r['id'])['generation'])
        self.assertEqual(len(self.cli('list')),1)

    def test_dead_review_is_failed_without_blocking_healthy_review(self):
        dead=self.start('Interrupted daemon')
        healthy=self.start('Healthy daemon')
        os.kill(dead['generation']['pid'],signal.SIGTERM)
        for _ in range(50):
            status,_,page=self.request()
            if 'Failed' in page:break
            time.sleep(.05)
        self.assertEqual(status,200)
        self.assertIn('Failed',page)
        self.assertIn('Daemon inactive or failed verification',page)
        self.assertIn('Active',page)
        self.assertEqual(self.request('/api/session',host=healthy['public_url'].split('://')[1])[0],200)
