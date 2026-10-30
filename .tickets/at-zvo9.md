---
id: at-zvo9
status: open
deps: []
links: []
created: 2026-10-20T23:40:40Z
type: task
priority: 1
assignee: Ryan Swift
parent: at-iv51
tags: [toolkit]
---
# Inventory skill discovery per runtime

Where Claude, Codex, OpenCode, Cursor, agy on Reef and the Hermes profiles on Lobster currently load skills from. Then choose which consumers migrate to this checkout's canonical sources.

## Current direction — 2026-10-28

Matt's pack is installed for OpenCode, Claude Code, Codex, and Antigravity CLI on
Reef; see docs/matt-pocock-rollout.md. Remaining specialist review should reflect
Ryan's Reef-first execution with Marlin as the current client:

- Browser: first priority; host/authentication/visibility boundaries under at-th8j.
- Wayland: workstation maintenance only, targeting the affected graphical session,
  not whichever host executes the coding agent.
- Blogging: keep personal voice and actual blog repository checks; recheck deployed
  source copies and host paths before changing its content.
- agent-workspace-linux: distinguish its hidden app-QA desktop from Git worktrees
  and the user's actual desktop; assess overlap with browser tooling.

Ryan requested removal of the old test-coverage skill/prompt/adapters; done in the
current working tree, not committed. No other specialist was removed or upgraded.
