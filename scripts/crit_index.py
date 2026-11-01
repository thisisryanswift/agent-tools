"""Saved review index. All actions use fixed launcher lifecycle metadata."""
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from html import escape
import re
import secrets
from urllib.parse import parse_qs, urlsplit

from crit_reviews import ReviewError

STYLE='''
:root{color-scheme:light dark;font:16px/1.55 system-ui,sans-serif;background:#101722;color:#e4eaf2}
*{box-sizing:border-box}body{margin:0}main{max-width:1100px;margin:auto;padding:3rem 1.5rem}
a{color:#9acbff;text-underline-offset:.2em}h1{font-size:2.25rem;line-height:1.15;margin:.3rem 0 1rem}
h2{font-size:1.18rem;margin:0;overflow-wrap:anywhere}.eyebrow{color:#98aec7;text-transform:uppercase;letter-spacing:.12em;font-size:.8rem}
.intro{max-width:74ch;color:#b7c6d8}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,390px),1fr));gap:1rem;margin-top:2rem}
article,.empty{border:1px solid #3a4c65;border-radius:12px;background:#192435;padding:1.4rem}
.badge{display:inline-block;border:1px solid #7d93b0;border-radius:99px;padding:.1rem .65rem;font-size:.83rem;margin:.7rem 0;color:#dce9fa}
.active{color:#a2ebc9;border-color:#559e81}.failed{color:#ffc5bc;border-color:#b26e62}
dl{margin:.5rem 0}dt{font-size:.8rem;color:#aabbd1;margin-top:.65rem}dd{margin:0;overflow-wrap:anywhere}
.notice{border-left:3px solid #dfb16a;padding:.2rem .8rem;color:#f0d6b0;font-size:.9rem}
.meta{color:#aabbd1;font-size:.85rem;overflow-wrap:anywhere}button{font:inherit;color:#122035;background:#a8d1ff;border:0;border-radius:6px;padding:.5rem .9rem;cursor:pointer}
a:focus-visible,button:focus-visible{outline:3px solid #f4cb83;outline-offset:4px}.actions{margin-top:1rem}footer{margin-top:2rem;color:#aabbd1;font-size:.9rem}
'''

def observation(registry, record):
    result=dict(record)
    result['state']='stopped' if not record.get('generation') else 'failed'
    result['activity']='Stopped' if result['state']=='stopped' else 'Daemon inactive or failed verification'
    try:
        live=registry.verified(record['id'])
        health=registry.request(record['id'],'/api/health',timeout=1)
        result['state']='active'
        result['activity']='Reviewer connected' if health.get('browser_clients') else 'Running · waiting for reviewer'
        result['last_known']={'round':live['session'].get('review_round')}
        registry.remember(record['id'],live['generation'],live['session'],result['activity'])
    except (OSError,ValueError,KeyError,ReviewError):
        pass
    return result

def render(registry, token):
    records=registry.list()
    with ThreadPoolExecutor(max_workers=8) as pool:
        reviews=list(pool.map(lambda r:observation(registry,r),records))
    shared=Counter(r['cwd'] for r in reviews)
    cards=[]
    for r in reviews:
        e=lambda value:escape(str(value),quote=True)
        state=r['state']; saved=r.get('last_known',{})
        scope=r['scope']; scope_text='Documents: '+', '.join(scope['files']) if scope['mode']=='files' else scope.get('range') or ('Base: '+scope['base'] if scope.get('base') else 'Working tree')
        round_text=str(saved.get('round') or 'Not yet observed')
        last=''
        if state!='active' and saved:
            when=datetime.fromtimestamp(saved.get('observed_at',0),timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
            last=f'<p class="meta">Last known: {e(saved.get("activity","Unknown"))} · {e(when)}. Round shown is saved.</p>'
        notice='<p class="notice"><strong>Shared checkout</strong> · Content can include other agents’ edits. Each review follows its own refresh and review-round lifecycle.</p>' if shared[r['cwd']]>1 else ''
        actions=f'<a href="{e(r["public_url"])}">Open review ↗</a>' if state=='active' else f'<form action="/resume" method="post"><input type="hidden" name="csrf" value="{token}"><input type="hidden" name="review" value="{e(r["id"])}"><button type="submit">Resume saved review</button></form>'
        cards.append(f'''<article><h2>{e(r['conversation'])}</h2><span class="badge {state}">{state.title()}</span>
<dl><dt>Checkout</dt><dd>{e(r['cwd'])}</dd><dt>Branch</dt><dd>{e(r.get('branch') or 'No branch')}</dd><dt>Scope</dt><dd>{e(scope_text)}</dd><dt>Round</dt><dd>{e(round_text)}</dd><dt>Activity</dt><dd>{e(r['activity'])}</dd></dl>{last}{notice}<p class="meta">Review {e(r['id'])} · <a href="{e(r['public_url'])}">Permanent link</a></p><div class="actions">{actions}</div></article>''')
    content='<section class="grid" aria-label="Saved reviews">'+''.join(cards)+'</section>' if cards else '<section class="empty"><h2>No saved reviews</h2><p>Explicitly request a review in your agent conversation to create one.</p></section>'
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Crit · Saved reviews</title><style>{STYLE}</style></head><body><main><div class="eyebrow">Crit · Private review workspace</div><h1>Saved reviews</h1><p class="intro">Find a conversation, open its active review, or resume its saved feedback at the same permanent address. Reload this page for current activity.</p>{content}<footer>Review identities separate feedback and completion. Finish is scoped review feedback; it does not authorize implementation or publishing.</footer></main></body></html>'''

def handle(handler):
    parsed=urlsplit(handler.path)
    if parsed.query or parsed.fragment:
        return handler.reply(400,'Index requests do not accept query arguments\n')
    if parsed.path not in ('/','/resume'):
        return handler.reply(404,'Unknown index path\n')
    if handler.command in ('GET','HEAD') and parsed.path=='/':
        page=render(handler.server.registry,handler.server.csrf).encode()
        handler.send_response(200)
        for key,value in {'Content-Type':'text/html; charset=utf-8','Content-Length':str(len(page)), 'Cache-Control':'no-store','Content-Security-Policy':"default-src 'none'; style-src 'unsafe-inline'; form-action 'self'; frame-ancestors 'none'; base-uri 'none'",'X-Content-Type-Options':'nosniff','Referrer-Policy':'no-referrer','Connection':'close'}.items():handler.send_header(key,value)
        handler.end_headers()
        if handler.command!='HEAD':handler.wfile.write(page)
        return
    if handler.command!='POST' or parsed.path!='/resume':
        return handler.reply(405,'Unsupported index method\n')
    host=handler.headers['Host']
    origins=handler.headers.get_all('Origin',[])
    # Require the exact HTTPS authority; sibling review hosts are other origins.
    if len(origins)!=1 or origins[0]!='https://'+host or handler.headers.get_all('Sec-Fetch-Site',[])!=['same-origin']:
        return handler.reply(403,'Same-origin browser action required\n')
    lengths=handler.headers.get_all('Content-Length',[])
    if handler.headers.get('Transfer-Encoding') or len(lengths)!=1 or not re.fullmatch(r'[0-9]+',lengths[0]) or int(lengths[0])>1024:
        return handler.reply(400,'Invalid action length\n')
    if handler.headers.get_all('Content-Type',[])!=['application/x-www-form-urlencoded']:
        return handler.reply(400,'Expected form action\n')
    try:
        form=parse_qs(handler.rfile.read(int(lengths[0])).decode('utf-8'),strict_parsing=True,keep_blank_values=True)
    except (ValueError,UnicodeError):return handler.reply(400,'Malformed action\n')
    if set(form)!={'review','csrf'} or any(len(v)!=1 for v in form.values()):
        return handler.reply(400,'Only a saved review and action token are accepted\n')
    if not re.fullmatch(r'[a-f0-9]{64}',form['csrf'][0]) or not secrets.compare_digest(form['csrf'][0],handler.server.csrf):
        return handler.reply(403,'Invalid action token; reload the index\n')
    try:
        handler.server.registry.get(form['review'][0])
    except (ValueError,ReviewError):
        return handler.reply(404,'Unknown saved review\n')
    try:
        review=handler.server.registry.start(review_id=form['review'][0])
    except (OSError,ValueError,ReviewError):
        return handler.reply(409,'Saved review could not resume. Inspect it with the launcher; no scope changes were accepted.\n')
    handler.send_response(303)
    handler.send_header('Location',review['public_url'])
    handler.send_header('Content-Length','0')
    handler.send_header('Cache-Control','no-store')
    handler.send_header('Connection','close')
    handler.end_headers()
