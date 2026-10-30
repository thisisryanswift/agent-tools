---
id: at-th8j
status: open
deps: []
links: []
created: 2026-10-20T23:40:40Z
type: task
priority: 2
assignee: Ryan Swift
parent: at-iv51
tags: [toolkit, browser]
---
# Verify Browser Harness on the browser host

Verify the package/wrapper, profile reuse, worker cleanup, workspace access, and
OpenCode V2 setup on the actual browser host. Distinguish local candidate tests
from a deployed runtime; preserve existing work in browser-harness-workers.

## Notes

**2026-10-24T23:17:59Z**

The old "likely 0.1.8 -> 0.1.10" description understated the existing work.
Read-only inspection of ~/dev/tools/browser-harness-workers finds HEAD 50236e1
with extensive tracked/untracked changes. Its docs/restart-checkpoint.md records
an unpublished Harness 0.1.13 candidate and local test evidence, not live rollout.
Its final review ticket bhw-revw is in_progress and depends on unresolved
bhw-wyd4; rollout ticket bhw-roll remains open. Those are external gates, not
authorization to resume that project's implementation, commit, or install.
Keep this ticket open until target-host verification is recorded. No browser
tests, release review, or deployment were performed during this reconciliation.

**2026-10-28, Reef-first direction** — Ryan now codes almost entirely through
agents executing on Reef while using Marlin/other devices as clients. Review
browser routing around that split: a local Reef task browser versus explicitly
requested control of a client browser; where authentication lives; human-visible
login/MFA; and ownership/cleanup. Compare Python/CDP tooling, client-native browser
tools, and Codex's isolated desktop rather than activating overlapping defaults.
This is a review request, not authorization to resume the separate worker release,
copy client profiles, change browser services, or expose remote-control endpoints.
