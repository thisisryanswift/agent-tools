"""Loopback HTTP gateway for owned Crit review hostnames."""
import http.client
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import re
import secrets
import select
import socket
import threading
from urllib.parse import unquote, urlsplit

from crit_reviews import ReviewError

HOP_HEADERS={'connection','keep-alive','proxy-authenticate','proxy-authorization',
             'te','trailer','transfer-encoding','upgrade'}

class Router(ThreadingHTTPServer):
    daemon_threads=True
    block_on_close=False

    def __init__(self, registry, port=17466, index_host=None):
        if index_host and not re.fullmatch(r'[a-z0-9]+(?:[.-][a-z0-9]+)*',index_host):
            raise ReviewError('Invalid index hostname')
        self.registry=registry
        self.csrf=secrets.token_hex(32)
        self.index_hosts={registry.domain,index_host}-{None}
        super().__init__(('127.0.0.1',port),Handler)

class Handler(BaseHTTPRequestHandler):
    protocol_version='HTTP/1.1'

    def log_message(self,*args):
        pass  # Never log review paths, comments or request bodies.

    def reply(self,status,message):
        body=message.encode()
        self.send_response(status)
        self.send_header('Content-Type','text/plain; charset=utf-8')
        self.send_header('Content-Length',str(len(body)))
        self.send_header('Cache-Control','no-store')
        self.send_header('Connection','close')
        self.end_headers()
        self.close_connection=True
        if self.command!='HEAD': self.wfile.write(body)

    def index(self):
        from crit_index import handle
        handle(self)

    def route(self):
        self.close_connection=True
        hosts=self.headers.get_all('Host',[])
        if len(hosts)!=1:
            return self.reply(400,'One explicit Host header is required\n')
        incoming=hosts[0]
        match=re.fullmatch(r'([a-z0-9.-]+)(?::([0-9]{1,5}))?',incoming)
        if not match or (match[2] and not 0<int(match[2])<65536):
            return self.reply(400,'Malformed review hostname\n')
        hostname=match[1]
        raw_target=self.requestline.split()[1]
        parsed=urlsplit(raw_target)
        if not raw_target.startswith('/') or raw_target.startswith('//') or parsed.scheme or parsed.netloc:
            return self.reply(400,'Only origin-form request targets are accepted\n')
        if hostname in self.server.index_hosts:
            return self.index()
        match=re.fullmatch(r'([0-9a-f]{12})\.'+re.escape(self.server.registry.domain),hostname)
        if not match:
            return self.reply(404,'Unknown review hostname\n')
        path=unquote(parsed.path)
        # Crit uses Go ServeMux, which cleans dot segments before routing.
        parts=[]
        for part in path.split('/'):
            if part=='..':
                if parts: parts.pop()
            elif part and part!='.': parts.append(part)
        path='/'+ '/'.join(parts)
        if (any(path==prefix or path.startswith(prefix+'/') for prefix in
                ('/live','/preview','/preview-content','/api/shutdown','/api/project-prompts/trust','/api/agent/request','/api/review-cycle','/api/round-complete'))
                or path.startswith('/api/share')
                or (self.command not in ('GET','HEAD') and path in ('/api/base-branch','/api/focus','/api/picker'))):
            return self.reply(403,'This operation is unavailable through the browser router\n')
        if self.headers.get('Transfer-Encoding') or self.headers.get('Upgrade'):
            return self.reply(400,'Unsupported request transfer encoding or upgrade\n')
        lengths=self.headers.get_all('Content-Length',[])
        if len(lengths)>1 or (lengths and not re.fullmatch(r'[0-9]+',lengths[0])):
            return self.reply(400,'Invalid request length\n')
        length=int(lengths[0]) if lengths else 0
        if length>16*1024*1024:
            return self.reply(413,'Request body too large\n')
        try:
            review=self.server.registry.verified(match[1])
        except ReviewError as exc:
            status=404 if 'Unknown review' in str(exc) else 503
            return self.reply(status,str(exc)+'\n')
        except (OSError,ValueError,KeyError):
            return self.reply(503,'Review daemon is inactive or failed verification\n')
        body=self.rfile.read(length) if length else None
        connection_tokens={v.strip().lower() for v in self.headers.get('Connection','').split(',')}
        headers={key:value for key,value in self.headers.items() if key.lower() not in HOP_HEADERS|connection_tokens}
        headers['Host']=incoming
        headers['Connection']='close'
        upstream=http.client.HTTPConnection('127.0.0.1',review['generation']['port'],timeout=5)
        sent=False
        finished=threading.Event()
        watcher=None
        response=None
        try:
            upstream.connect()
            # Verify again after connecting, before exposing any response. A stop or
            # restart during connection establishment must not change its identity.
            current=self.server.registry.verified(match[1])
            if current['generation']!=review['generation']:
                raise ReviewError('Review generation changed; retry')
            upstream.request(self.command,self.path,body=body,headers=headers)
            # Completion and SSE can wait indefinitely. select below still notices
            # an idle browser disconnect and closes the associated daemon socket.
            upstream.sock.settimeout(None)
            upstream_socket=upstream.sock
            def disconnect_watch():
                while not finished.is_set():
                    try:
                        ready,_,_=select.select([self.connection],[],[],.25)
                        if ready:
                            if not self.connection.recv(1,socket.MSG_PEEK):
                                upstream_socket.shutdown(socket.SHUT_RDWR)
                                return
                            finished.wait(.25)
                    except OSError:
                        return
            watcher=threading.Thread(target=disconnect_watch,daemon=True)
            watcher.start()
            response=upstream.getresponse()
            self.send_response(response.status,response.reason)
            response_tokens={v.strip().lower() for v in response.getheader('Connection','').split(',')}
            for key,value in response.getheaders():
                if key.lower() not in HOP_HEADERS|response_tokens:
                    self.send_header(key,value)
            self.send_header('Connection','close')
            self.send_header('X-Accel-Buffering','no')
            self.end_headers(); self.wfile.flush(); sent=True
            if self.command=='HEAD': return
            while True:
                chunk=response.read1(65536)
                if not chunk: break
                self.wfile.write(chunk); self.wfile.flush()
        except (OSError,ValueError,http.client.HTTPException,ReviewError):
            if not sent: self.reply(503,'Review daemon disconnected or failed verification\n')
        finally:
            finished.set()
            if response: response.close()
            upstream.close()
            if watcher: watcher.join(timeout=.5)

    do_GET=route
    do_HEAD=route
    do_POST=route
    do_PUT=route
    do_PATCH=route
    do_DELETE=route
    do_OPTIONS=route

def serve(registry,port=17466,index_host=None):
    with Router(registry,port,index_host) as server:
        server.serve_forever()
