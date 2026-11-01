# Independent Crit sessions: local validation

## Deployment follow-up — 2026-11-01

The router is now deployed behind private wildcard DNS and tailnet-only Caddy.
The permanent index is **https://crit.wharfi.sh**. Five HTTPS review identities
passed, including four synthetic remote checks from Marlin for comments, SSE,
independent Finish delivery and targeted restart. Ryan completed a real document
comment/Finish/revision/second-comment/Finish loop and confirmed the remote Git
diff UI with a screenshot. Saved index resume and router restart preserving
daemon identities also passed. These are scoped remote checks, distinct from
the initial local browser evidence below.

Deployment exposed incompatible user-unit mount sandboxing: ProtectSystem and
PrivateTmp each prevented peer `/proc` identity checks. A new real-systemd
regression reproduced the failure; removing these two settings passed. Ryan
explicitly approved that adjustment after reviewing the risk. NoNewPrivileges,
private state, loopback backends, tailnet HTTPS, and identity checks remain.
The full suite now passes 34 tests with the systemd regression enabled.

Fresh local database and isolated old-app recovery passed. Ryan's selective
off-host restore also matched all seven recovery inputs byte-for-byte. The root
backup script now includes independent review state and the router unit.
All four runtime instruction files and skill links select the new protocol;
fresh invocation in the other three agent runtimes and legacy-service retirement
remain pending. The old app/database/data are retained for rollback. See the
operations record for exact evidence and activation state. No commits or pushes.

## Initial local implementation record

Integration branch: `implement/at-sxgj`, based on `e64c9dc`. All implementation
changes are uncommitted. This record covers the local implementation, not a
completed deployment of epic `at-sxgj`.

Task-owned worktrees, synthetic Crit daemons, router and Browser Harness daemon
were cleaned up. The existing hosted app, database and backup timer were checked
after cleanup and remain active. Pre-existing and concurrent repository edits
were preserved.

## Local evidence

- Full repository suite: 33 tests passed. After the final narrow stop-after-scope-
  drift fix, the native scope regression passed again; the complete final Crit
  suite passed all 21 tests in its implementation worktree.
- Real installed Crit v0.23.1 (`ad3e10f`): five independent reviews, CLI comments,
  independent Finish waiters, restart, revision, document/range scopes, concurrent
  creation, stale process/socket rejection, transport replacement, scope drift,
  router streaming/disconnect, safe index resume and browser action validation.
- Skills structural check: 8 skills and 2 prompt copies pass. Tracked whitespace
  check passes. Prepared user unit verifies and selects the pinned user binary
  even with a service-like PATH. Synthetic private DNS zone passes syntax checks.
- Isolated headless Chromium: the index displayed five reviews with active,
  stopped and failed states at 1280px and 390px without horizontal overflow.
  Git and document UIs loaded over the local hostname router. A synthetic browser
  comment and Finish reached the matching launcher waiter with `approved:false`.
  A second browser round fetched the changed file content, retained prior
  feedback, added new synthetic feedback and completed the same waiter identity
  with `approved:false` again.
  Screenshot evidence is temporary under `/tmp/at-sxgj-index-desktop.png`,
  `/tmp/at-sxgj-index-mobile.png` and `/tmp/at-sxgj-document-ui.png`.

Browser checks used disposable `.localhost` hostnames and HTTP. They do not
establish tailnet DNS, TLS, cross-device connectivity, runtime invocation parity
or human approval. Displayed authorship from existing Crit settings does not
make automated test feedback human feedback. Tests pin share targets to an
unreachable loopback address.

## Standards

The standards review included the full uncommitted implementation and relevant
untracked files. It found no documented-standard violations. Its one low-severity
heuristic finding was duplicated branch/detached-HEAD resolution. The single
review-fix implementer replaced that block with the existing `_branch()` helper.
No unresolved standards finding remains.

## Spec

The initial spec review found three local issues: service PATH could select a
retired Crit wrapper; launcher mutations lacked connection-time identity checks;
and effective live scope was not compared with saved scope.

The targeted re-review confirmed all three are resolved. The prepared service
explicitly selects `%h/.local/bin/crit`. Comment, wait and stop establish a
connection before repeating ownership, generation and identity checks. Effective
scope is persisted and checked; native scope drift rejects resume/wait, while
targeted stop retains identity checks and permits cleanup. Documentation agrees.
No material unresolved local defect or additional scope creep was identified.

External acceptance remains pending: private DNS/TLS deployment, remote browser
validation, a human comment/Finish/revision loop, adoption in all four runtimes,
verified recovery and cutover. Local tests do not complete those gates.

Review totals: Standards 0 unresolved; Spec 0 unresolved local findings, with
external acceptance still pending.

## Deployment boundary

Follow [the operations and rollback runbook](crit-sessions-operations.md) and
review `deploy/crit-reviews/` before authorizing live changes. The session protocol
is not activated. Existing hosted services/data remain in place. The runbook
records the share-test incident, read-only evidence that no fixture publication
landed, and the required rotation of the exposed hosted API token.
