---
id: at-ohwo
status: open
deps: [at-zvo9, at-duwo]
links: []
created: 2026-10-20T23:40:40Z
type: task
priority: 2
assignee: Ryan Swift
parent: at-iv51
tags: [toolkit]
---
# Install skills for chosen runtimes

Use the explicit installer after the inventory and brainstorming fix.

## Notes

**2026-10-28** — Direction changed to Matt Pocock's promoted pack. Global
OpenCode-on-Reef slice deployed: 27 pinned unchanged upstream skills, live registry
paths/invocation metadata verified, scoped managed policy applied. See
docs/matt-pocock-rollout.md. Old brainstorming fix superseded. Keep open for Claude
Code, Codex, Antigravity CLI, broader discovery/overlap checks and real workflow
qualification; inventory dependency at-zvo9 is not complete.

**2026-10-28, additional consumers** — Same 27-skill pin installed for Claude
Code (~/.claude/skills), Codex (~/.agents/skills), and Antigravity CLI
(~/.gemini/antigravity-cli/skills) on Reef. Claude's command catalog and Codex
skills/list see all 27; Antigravity's /ask-matt expands successfully in a no-tools
smoke test. Scoped shared policy applied; existing skills preserved. No old
engineering skills were active in these user roots, so nothing was deleted.
Keep open for full workflow qualification and the broader at-zvo9 inventory;
see docs/matt-pocock-rollout.md for exact evidence/limitations.
