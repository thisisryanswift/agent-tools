# Explicit conversation reviews

`scripts/crit-review.py` owns independent local Crit reviews using the installed
**v0.23.1 (ad3e10f)** binary. It never changes HOME or edits existing Crit
configuration. Invoke it only for a requested review. It does not publish a
snapshot or configure DNS, HTTPS, or services.

```bash
# Git working-tree review. Use the runtime's stable conversation ID.
python3 scripts/crit-review.py start --conversation 'codex:conversation-id' --cwd "$PWD"

# A chosen diff range or base branch (use one).
python3 scripts/crit-review.py start --conversation 'codex:range-review' --cwd "$PWD" --range 'main..HEAD'
python3 scripts/crit-review.py start --conversation 'codex:base-review' --cwd "$PWD" --base main

# Documents; each path is relative to --cwd or absolute.
python3 scripts/crit-review.py start --conversation 'codex:documents' --cwd "$PWD" proposal.md notes.md

python3 scripts/crit-review.py list
python3 scripts/crit-review.py show 012345abcdef
python3 scripts/crit-review.py comment 012345abcdef 'Please clarify this paragraph.'
python3 scripts/crit-review.py wait 012345abcdef
python3 scripts/crit-review.py stop 012345abcdef
python3 scripts/crit-review.py start --review 012345abcdef
```

Every command returns JSON; errors go to stderr with a nonzero status. Start
returns `id`, `public_url`, `scope`, `output`, process `generation`, and the live
`session`. The public URL is the durable intended hostname; opening it remotely
requires the separately configured tailnet router. For local inspection, the
JSON's `generation.port` is a loopback HTTP listener.

Repeating the same conversation and scope resumes the same identity. A changed
checkout, branch, or scope is rejected. `start --conversation ... --cwd ... --new`
creates another saved identity and makes it the preferred identity for later
requests by that conversation; the previous review remains accessible by ID.
If a runtime has no stable conversation identifier, choose an explicit unique
name. The launcher never guesses from cwd or silently selects another session.
`start --review ID` resumes exactly the saved scope and URL. If the checkout has
changed branches, restore its saved branch or explicitly create a new review.

The launcher records the effective Crit base, focus/range and explicit document
selection at initial readiness. A later native Crit scope mutation is rejected
by saved resume, wait and routing; changing Git's file contents or changed-file
list between revisions is allowed. Use a new explicit review identity for a new
scope. `stop ID` can still stop the same verified owned daemon after scope or
branch drift, preserving its saved metadata and feedback.

`wait` starts the next review cycle and blocks for the browser's Finish action.
Only one launcher wait client can hold a given review at a time. Start and show
do not advance rounds. Wait timeouts, shutdown, and connection failures are
errors, never approval. A subsequent wait refreshes that review's content from
the checkout. Other reviews retain their prior content until advanced. Separate
reviews in one checkout isolate feedback and identity, not code authorship.

The default durable registry is `~/.local/share/crit-reviews`; a separate output
root is retained per review. Global options precede the command:

```bash
python3 scripts/crit-review.py --registry /tmp/my-review-registry --binary /absolute/path/to/crit --domain crit.wharfi.sh list
```

Keep a registry private and retain it with its output directories. It stores
conversation IDs and absolute checkout paths. `registry.json` is atomically
replaced under a mutation lock. Readers do not wait for slow daemon startup;
process ID, Linux process start time, executable, cwd, listening socket inode,
live session identity, pinned version, review path and Crit registry entry are
checked before routing or issuing requests. Stale identities fail closed.
Stop is targeted and preserves saved state. Logs are per review in the durable
root. No command deletes review data, changes existing share targets, or cleans
unrelated daemons. Existing global/project hooks remain effective; operators
must understand their existing hook behavior when pressing Finish.

The launcher uses Crit's internal `_serve --session-key` interface, so versions
other than the tested release/commit are refused before launching. Live app and
HTML preview review modes are unsupported. The runtime requires Linux `/proc`
and Python 3's standard library. The Crit daemon still writes its own transient
session entry beneath the existing HOME.

## Integration checks

```bash
/usr/bin/python3 -m unittest discover -s tests -p test_crit_reviews.py -v
```

Tests use the installed pinned binary (`CRIT_TEST_BINARY` can choose its path),
a disposable shared clone, and test-owned loopback daemons. They neither commit
nor change HOME. The test runner needs permission to bind loopback sockets and
to let Crit maintain its ordinary transient registry. Before running Finish tests,
check that existing global hooks do not cause unintended external actions.
Tests verify five independent review cycles, comment separation, targeted
restart after transient registry removal, revision refresh, document/range
scopes, concurrent creation, scope drift, version rejection, stale identity
refusal, and duplicate waiter rejection. Production remote review is a separate
validation gate.

## Python interface

Router callers can import `scripts/crit_reviews.py`. `Registry(root=None,
binary='crit', domain='crit.wharfi.sh')` provides `list()`, `get(id)`,
`verified(id)`, `start(...)`, `stop(id)`, `request(id,path,payload=None,timeout=5)`
and `wait(id,timeout=86400)`. `get` and `list` return durable metadata, including
inactive entries. `verified` returns live metadata with `session` and
`state='active'`, or raises `ReviewError`/an I/O exception. An upstream must always
be derived from verified metadata rather than caller-supplied headers or ports.

## Loopback hostname router

Run `python3 scripts/crit-review.py serve --port 17466` to listen only on
`127.0.0.1`. It accepts registered `<12-lowercase-hex>.crit.wharfi.sh` hosts and
preserves the incoming Host header for Crit. The exact root `crit.wharfi.sh`
always selects the index. `--index-host validation.crit.wharfi.sh` adds one exact
index alias for local/pre-cutover validation; it never changes saved review URLs.
Use an explicit Host header when exercising this locally; production DNS and
Caddy configuration are separate deployment work.

Each request verifies the owned daemon process generation, listening socket,
Crit session identity and saved scope. Unknown reviews return 404; stopped,
failed or conflicting generations return 503 without selecting another daemon.
Restart through `start --review ID` retains the same public hostname. Browser
SSE and non-advancing `/api/wait-for-event` responses stream promptly; idle
browser disconnects close their upstream socket. Inactive reviews and long-lived
streams each run independently of other reviews.

The browser route supports Crit's review UI, assets, files, comments and Finish.
Live app and HTML preview paths (`/live`, `/preview`, `/preview-content`, including
descendants) are unavailable. Shutdown, project prompt trust changes, agent spawning, `/api/share*`, round
advancement (`/api/review-cycle`, `/api/round-complete`) and scope mutations
(`/api/base-branch`, `/api/focus`, `/api/picker`) are rejected by the router.
Agent clients use the launcher `wait` command, which serializes completion waits;
create another explicit review identity to change scope. Read-only branch
listing and picker metadata remain available. Unsupported operations return an
explicit 403; no upload target or arbitrary upstream can be selected through
request headers, hostnames, paths or query parameters.

Requests require unambiguous Content-Length framing; chunked request uploads,
protocol upgrades and bodies over 16 MiB are rejected. The router terminates each
HTTP connection after its response and removes hop-by-hop headers, while
forwarding streamed response bodies without buffering the whole response.

Router integration tests use the real pinned Crit binary and synthetic fixture
checkouts, with `CRIT_SHARE_URL=http://127.0.0.1:1` in fixture subprocesses to keep
sharing unreachable without changing HOME or actual configuration:

```sh
/usr/bin/python3 -m unittest discover -s tests -p test_crit_router.py -v
```

## Saved review entry page

Open `https://crit.wharfi.sh/` after the tailnet proxy is configured. The root
index lists conversation labels, permanent review links, checkout, branch,
scope, round and live daemon activity. An empty registry has an explicit empty
state. Stopped reviews retain their last observed round/activity; failed or
stale processes are labeled **Failed**, independently of healthy reviews.
Reload to update the list. Active probes run concurrently, outside the registry
mutation lock. Observation persistence skips a busy mutation lock.

Reviews using the same checkout display a **Shared checkout** notice. Feedback
and identities are separate; content can include other agents' edits and follows
each review's own refresh/review-round lifecycle.

**Resume saved review** starts only an existing registered review using its
saved launcher metadata. It retains the review ID, hostname and stored feedback.
A changed branch or conflicting process fails safely and requires launcher
inspection. Browser forms cannot create identities, change a scope, select a
filesystem path, run a command, or choose an upstream. Resume requires the exact
HTTPS Origin/Host authority, `Sec-Fetch-Site: same-origin`, an unpredictable
action token and exactly the registered review ID. Reload after restarting the
router to obtain a fresh token. Index pages prohibit framing and external assets.

Local HTTP integration checks use Host headers and the intended HTTPS Origin;
they verify empty, five active, stopped, failed, escaped-label and safe-resume
states against the real pinned binary, including retained comments:

```sh
CRIT_SHARE_URL=http://127.0.0.1:1 /usr/bin/python3 -m unittest discover -s tests -p test_crit_index.py -v
```

These checks do not establish remote DNS/TLS availability or human review.
