---
id: at-iv51
status: open
deps: []
links: []
created: 2026-10-20T23:40:40Z
type: task
priority: 1
assignee: Ryan Swift
tags: [toolkit]
---
# Toolkit: deploy skills and verify runtimes

Parent for the toolkit workstream. Context: docs/consolidation-status.md (Toolkit) and docs/personal-agent-toolkit-plan.md workstream B. Source is committed (3ad2946); make check/test pass.

## Current direction — 2026-10-28

Matt Pocock's promoted pack is the single engineering baseline, globally installed
for OpenCode on Reef first. See docs/matt-pocock-rollout.md. Preserve specialist
skills/prior work without layering the old engineering pack. at-duwo is superseded,
at-ohwo remains partial, and new child at-nxnl tracks Crit support. No cross-runtime
deployment or full workflow qualification yet.

## Notes

**2026-10-24T23:17:59Z**

Reconciliation leaves this parent and all five children open. Fresh `make check`
passes (7 skills, 3 prompt copies), and `make test` passes (4 installer tests).
These are structural/installer checks, not runtime discovery, deployment, browser,
or skill-quality evidence. The canonical brainstorming prompt still mandates
design/commit steps, and evals/README.md remains a migration map without counted
model runs. See docs/ticket-reconciliation-2026-10-24.md for the full disposition.
