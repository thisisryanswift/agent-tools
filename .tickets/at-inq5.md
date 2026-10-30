---
id: at-inq5
status: closed
deps: []
links: []
created: 2026-10-28T19:57:30Z
type: task
priority: 1
assignee: Ryan Swift
parent: at-iv51
tags: [toolkit, tk, crit]
---
# Configure global Matt tracker defaults and manual Crit review

Implement Ryan-approved global default: tk for projects without an established tracker, explicit existing project trackers win, specs live in tracker tickets, no mandatory docs/specs. Add optional manually invoked local Crit support across the four installed runtimes. Preserve upstream Matt files, do not mass-migrate projects, add automatic review gates, upload reviews, or expose network services. Verify scoped instruction rendering, tk operations in disposable fixtures, Crit executable/manual discovery and local CLI smoke checks. Remote human browser approval remains an explicit user test.


## Notes

**2026-10-28T20:09:01Z**

Implemented shared global workflow guide with established-tracker precedence, tk default, tracker-backed specs, native tk operation/triage/wayfinding mapping, and optional manual Crit. Applied only the guide link and four managed instruction targets on Reef. Installed checksum-verified Crit v0.23.1 in ~/.local/bin without changing the stale root-owned launcher. Manual Crit skill installed for all four runtimes; OpenCode autoinvoke=false and Codex single registration verified. Local disposable HTTP/comment/stop fixture passed; no human approval simulated and no fixture sessions left active. make check, 10 tests, scoped chezmoi verify and diff checks pass; upstream Matt tree unchanged. No commits, pushes, hosted sharing or external service exposure. Real Marlin human review remains open under at-nxnl. See docs/global-workflow.md.
