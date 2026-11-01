---
id: at-5ftr
status: in_progress
deps: [at-g9co, at-7193]
links: []
created: 2026-11-01T15:06:47Z
type: feature
priority: 2
assignee: Ryan Swift
parent: at-sxgj
tags: [crit, ready-for-agent]
---
# Adopt the Crit launcher across agent workflows and replace Crit Web

Make explicitly invoked Crit reviews use the launcher across OpenCode, Claude Code, Codex, and Antigravity CLI. Retain the correct conversation/review identity for opening, targeted comments, waiting, and later rounds, including separate conversations sharing a checkout. Update the manually invoked skill, instructions, and operational documentation to the validated CLI routing workflow.

Switch crit.wharfi.sh to the review index after the remote replacement passes validation. Inventory and preserve existing hosted review content and comments, database, credentials, and backups; provide a verified recovery route before stopping old Crit Web services. Stop only the identified old services and retain recoverable data. Do not delete volumes, credentials, backups, or historical reviews. Keep rollback available until explicitly released.

Crit stays manually invoked, with no automatic review gate or inferred implementation/commit approval. Unsupported live/preview modes must be reported clearly rather than routed into a broken experience or silently uploaded elsewhere. Use the pinned installed binary without upstream modifications. Ticket creation is not authorization to deploy or edit global instructions; prepare the result and follow the session's applicable authorization boundaries.

## Acceptance Criteria

- [ ] Each supported runtime demonstrably opens an explicitly requested review through the launcher and records a stable identity for later rounds.
- [ ] Concurrent conversations in one checkout do not merge comments or completion events; ambiguous targeting is rejected.
- [ ] A real remote human comment/Finish/revision loop reaches the correct agent, with synthetic testing kept distinct from human approval.
- [ ] The permanent root hostname serves the review index and per-review links continue working after cutover.
- [ ] Existing hosted content/comments and recovery material are inventoried, preserved, and verifiably recoverable before old services are stopped.
- [ ] Only the intended old services are retired; unrelated daemons and stored data are preserved, and rollback is documented and validated.
- [ ] Current skill/instruction/docs agree on manual-only invocation, explicit identity, shared-checkout limitations, supported modes, and pinned-version compatibility.
- [ ] No upstream change, new release, public fallback upload, commit, push, or destructive deletion is required to complete this delivery.


## Notes

**2026-11-01T15:49:13Z**

Prepared gated sessions protocol skills/crit/references/sessions.md and manual skill/global workflow source pointers; existing hosted protocol remains active until approved remote cutover. Deploy artifacts and preservation/restore/rollback runbook are in deploy/crit-reviews and docs/crit-sessions-operations.md. Source implementation is ready, but remote HTTPS, real human loop, four-runtime invocation evidence, verified recovery and cutover/retirement remain pending. No global instructions, credentials, services, DNS, Caddy, commits or pushes changed. The runbook records a test-side credential exposure requiring human token rotation; no fixture publication was observed in read-only hosted inventory.

**2026-11-01T16:09:54Z**

Ryan explicitly accepted the low risk of the previously exposed hosted Crit API token and directed leaving it unchanged. Token rotation is not a deployment gate; preserve existing credentials. Fresh existing backup service succeeded at2026-11-01T16:08:17Z with readable mode0600 custom archive; restore and off-host checks still pending.

**2026-11-01T16:24:59Z**

Fresh local archive restored into owned disposable database crit_recovery_20261101161406, matching live7 reviews/20 comments/44 snapshots byte-content hashes. Temporary pinned old-app container with jobs disabled passed health, token identity, historical document/comments readback, login page and closed registration; only fixture app/env removed. Live DB unchanged. Off-host fresh backup+selective restore helper prepared for Ryan sudo; pending result. Root cutover candidate remains unapplied.

**2026-11-01T16:32:35Z**

Root cutover and independent-session protocol activated. Four Reef instruction files updated through chezmoi with unrelated bytes/Gemini memories preserved; four skill roots verified shared manual-only skill. Codex real human two-round launcher loop and remote Git UI passed. Off-host snapshot deebaa684fc56b069dd67d1622580ce66a3f592689543182bfd9ae66a15383c8 selective restore matched7 files, and isolated old-app restore/readback passed. Ryan installed expanded root backup paths for independent review state/router unit; source/live hashes match. Remaining: fresh actual invocation in OpenCode/Claude Code/Antigravity and legacy service/preview retirement. Keep this ticket and epic open; old services/data retained for rollback, token unchanged by explicit preference.
