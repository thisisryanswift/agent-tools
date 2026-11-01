# Independent Crit sessions

The independent-session router is deployed on Reef and verified over tailnet
HTTPS. Use this protocol for explicitly requested code and document reviews.
The deployment record in `docs/crit-sessions-operations.md` identifies the current
legacy-service retention and remaining runtime-adoption checks. The permanent
index is `https://crit.wharfi.sh`; per-review URLs are already active.

## Open and record a review

Only start after an explicit Crit request. Establish the exact Git diff/base/range
or selected document paths. Code and document review are supported; live app and
HTML preview are outside this deployment's scope. Report unsupported requests
without uploading to a different service.

Use the runtime's stable conversation ID if it is actually available, namespaced
by runtime and execution account. Otherwise require an explicitly selected
conversation identity. Cwd, branch and task titles alone cannot disambiguate
conversations. This rule applies to OpenCode, Claude Code, Codex and Antigravity.

The launcher lives at `~/dev/personal/agent-tools/scripts/crit-review.py` on Reef.
Inspect `--help` for flags. Example Git review:

```bash
/usr/bin/python3 ~/dev/personal/agent-tools/scripts/crit-review.py start \
  --conversation '<runtime>:<account>:<conversation-id>' --cwd "$PWD"
```

For documents, pass only the selected file paths after the start options.
Keep the same conversation and exact scope for later requests. If branch or scope
changes, resolve the change explicitly; `--new` creates a separate review while
retaining the previous identity and feedback.

Record the returned review ID, public URL, registry root, execution cwd, branch,
exact scope and conversation identity in the conversation's durable handoff.
Relay the actual `https://<review-id>.crit.wharfi.sh` URL promptly. The root
`https://crit.wharfi.sh` lists registered reviews. Tailnet access
is required; a review ID is a routing identity, not an authentication credential.

## Feedback, rounds and recovery

Use the saved review ID for every targeted action:

```bash
/usr/bin/python3 ~/dev/personal/agent-tools/scripts/crit-review.py show '<review-id>'
/usr/bin/python3 ~/dev/personal/agent-tools/scripts/crit-review.py wait '<review-id>'
```

Wait only when the requested round is ready for human review. The first wait
awaits Finish; subsequent waits advance that review's content before awaiting
Finish. Show/list/resume alone do not advance a round. Keep only one round waiter
for a review. Preserve the returned feedback and distinguish human feedback from
synthetic test comments/events. Empty comments, timeouts, disconnected clients and
successful connectivity checks are not approval.

Apply only changes already authorized in the conversation, then advance the same
review. Comments and replies remain scoped to its explicit ID. Leave comment
resolution to the reviewer unless asked. Review completion does not authorize
implementation, commits, pushes or publishing other content.

If the daemon has stopped, run `start --review '<review-id>'`. The
launcher restores the original key, scope, output path and URL; bare
`crit --session` cannot rediscover custom storage after Crit removes its transient
registry entry. A missing handoff requires inspection and explicit targeting,
not automatic attachment by cwd. Stop only a selected review when requested.

Concurrent reviews of one checkout have separate comments and completion signals,
but share the underlying files. Each review refreshes through its own round
lifecycle and can include edits from other agents. Separate review identities
do not establish independent code authorship or continuous synchronization.

## Compatibility and failures

The launcher depends on tested internal interfaces in Crit v0.23.1 (ad3e10f).
Run its real-binary compatibility tests before adopting another release. Keep
HOME and existing Crit configuration unchanged. Preserve unrelated daemons and
saved feedback. Stop on an identity conflict, unavailable router or HTTPS failure;
there is no automatic public sharing, SSH forwarding or localhost callback
fallback. Use the separate local protocol only after an explicit local request.
