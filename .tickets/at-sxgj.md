---
id: at-sxgj
status: in_progress
deps: []
links: []
created: 2026-11-01T15:06:47Z
type: epic
priority: 2
assignee: Ryan Swift
tags: [crit, spec]
---
# Remote Crit reviews with independent sessions

## Problem

Ryan develops remotely on Reef and has roughly five concurrent agent conversations, sometimes sharing a checkout. Crit Web's shared snapshots do not provide the CLI's full Git diff review UI. Per-session SSH forwarding is unwanted, and default Crit session identity can merge conversations in the same checkout.

## Intended outcome

An explicitly requested Crit review opens at a permanent tailnet HTTPS address without laptop localhost callbacks or SSH tunnels. Each conversation retains its own review identity, comments, completion signals, and revision rounds. The permanent entry page lists active and saved reviews. Reviews sharing a checkout are identified clearly; session isolation does not claim to isolate code authorship.

## Decisions

- Work with the existing pinned Crit v0.23.1 binary. No upstream modifications, accepted PRs, future releases, or upstream service are required.
- A local launcher supplies stable review IDs using the already-present internal daemon session-key interface and distinct review storage. Validate compatibility before adopting another binary version.
- Persist conversation mapping, review identity, working directory, branch/scope, output root, and public URL independently of the daemon registry. Reusing a conversation resumes the intended review; unrelated conversations remain separate.
- Use one review hostname per identity beneath crit.wharfi.sh. Keep the root hostname as an index; use a permanent Caddy wildcard route to a local registry-based router rather than privileged reloads for each review.
- Daemons and router listen on loopback. DNS, TLS, and the public-facing proxy are tailnet-only. Review IDs identify reviews and are not authentication credentials.
- Code and document reviews are the initial scope. Explicit user invocation remains mandatory; review completion is scoped feedback, not permission to implement, commit, or publish other work.
- Preserve existing hosted reviews, database, credentials, backups, and unrelated sessions through validation and cutover. Retire old services only after the replacement succeeds and rollback is documented.

## Investigation evidence

Five simultaneous Git-mode reviews of the same checkout passed tests for comment separation, explicitly targeted CLI comments, independent Finish waiters, streamed Finish events, saved state, targeted daemon restart, and a second revision round. Different output roots alone do not separate the running daemon identity. The internal session-key interface exists in the installed release and was exercised successfully.

Content refresh is per-review: only the session explicitly advanced in the revision experiment returned the subsequent shared file edit. Do not promise continuous synchronization across all reviews. HTTPS routing and browser end-to-end operation still require implementation testing. Live app mode assumes an additional HTTP iframe port and is outside this initial delivery.

## Delivery and validation

Deliver the five approved vertical slices as child tickets: isolated lifecycle; hostname routing; review index; tailnet HTTPS; agent workflow adoption and cutover. The lifecycle gates routing; routing independently gates the index and HTTPS; both index and HTTPS gate workflow adoption and replacement. Each slice must demonstrate its behavior and preserve pre-existing work.

## Out of scope

Live app review, HTML preview, upstream feature work, automatic agent-driven Crit activation, independent attribution of shared-checkout edits, public internet exposure, and destructive data deletion. Ticket creation does not authorize implementation, deployment, commits, pushes, or other external writes.

This epic is the authoritative specification for these child tickets. The prior Crit Web rollout remains a completed historical effort and is not reopened or modified.

## Acceptance Criteria

- [ ] Five concurrent conversations can review the same checkout without sharing comments, completion events, or saved review identities.
- [ ] A remote tailnet browser can open per-review HTTPS links, comment, finish, and review a revision without SSH forwarding or laptop callbacks.
- [ ] The index exposes review identity, checkout/branch, round, activity, and shared-checkout context.
- [ ] Restart and upgrade compatibility behavior is verified using the pinned installed binary, with no upstream changes required.
- [ ] All supported agent runtimes use the intended explicit review identity and preserve manual-only invocation.
- [ ] Existing hosted data is preserved, cutover and rollback are verified, and all five delivery tickets meet their acceptance criteria.


## Notes

**2026-11-01T15:49:13Z**

Local lifecycle/routing/index slices implemented, reviewed and closed on integration branch implement/at-sxgj, all changes uncommitted. Full repo33 tests pass plus final native-scope regression; final Crit suite21 pass in fix worktree. Synthetic headless browser Git/document/comment/Finish/revision checks pass; no human approval. Delivery report docs/crit-sessions-validation.md; deployment/rollback runbook docs/crit-sessions-operations.md. HTTPS/adoption tickets remain unfulfilled pending authorized live configuration, remote/human/runtime/recovery checks. Existing hosted services/data preserved. No commits/pushes/publication/deployment.

**2026-11-01T16:33:51Z**

Deployment phase complete: at-7193 closed after trusted private HTTPS, permanent root index, five isolated routes, real remote Git/document UI and two-round human feedback, saved resume/router restart, verified local+off-host recovery. Shared manual-only skill and allfour Reef global instructions now select independent sessions. Root backup script includes new state and unit. at-5ftr remains in_progress for fresh invocations in OpenCode/Claude Code/Antigravity and legacy-service/preview retirement; old services/data retained for rollback, no destructive cleanup or token change. No commits/pushes.
