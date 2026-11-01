#!/usr/bin/env python3
"""Explicit, durable per-conversation Crit review launcher. Emits JSON."""
import argparse
import json
import sys
from crit_reviews import Registry

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--registry',help='private durable state directory (default: ~/.local/share/crit-reviews)'); p.add_argument('--binary',default='crit',help='pinned Crit v0.23.1 executable'); p.add_argument('--domain',default='crit.wharfi.sh',help='public review hostname suffix')
    commands=p.add_subparsers(dest='command',required=True)
    start=commands.add_parser('start',help='create/resume by conversation and scope, or resume --review ID')
    start.add_argument('--conversation',help='explicit stable runtime conversation ID'); start.add_argument('--cwd',help='checkout/document directory'); start.add_argument('--review',dest='review_id',help='resume saved ID without other scope arguments'); start.add_argument('--new',action='store_true',help='create another identity and retain the previous one')
    start.add_argument('--base'); start.add_argument('--range',dest='revision_range'); start.add_argument('files',nargs='*')
    commands.add_parser('list',help='list saved active and inactive metadata')
    gateway=commands.add_parser('serve',help='Serve owned reviews through one loopback router')
    gateway.add_argument('--port',type=int,default=17466)
    gateway.add_argument('--index-host')
    for name in ('show','stop','comment','wait'):
        sub=commands.add_parser(name); sub.add_argument('id')
        if name=='comment': sub.add_argument('body')
        if name=='wait': sub.add_argument('--timeout',type=float,default=86400)
    a=p.parse_args()
    try:
        registry=Registry(a.registry,a.binary,a.domain)
        if a.command=='serve':
            from crit_router import serve
            serve(registry,a.port,a.index_host)
            return 0
        if a.command=='start': result=registry.start(a.conversation,a.cwd,a.files,a.base,a.revision_range,a.new,a.review_id)
        elif a.command=='list': result=registry.list()
        elif a.command=='show': result=registry.get(a.id)
        elif a.command=='stop': result=registry.stop(a.id)
        elif a.command=='comment': result=registry.request(a.id,'/api/comments',{'body':a.body,'author':'Agent'})
        else:
            result=registry.wait(a.id,a.timeout)
            if result.get('status')!='finished': raise RuntimeError('Review wait ended without Finish')
        print(json.dumps(result))
        return 0
    except Exception as e:
        print(f'crit-review: {e}',file=sys.stderr); return 1

if __name__=='__main__': sys.exit(main())
