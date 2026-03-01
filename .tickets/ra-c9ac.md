---
id: ra-c9ac
status: closed
deps: []
links: []
created: 2026-03-01T16:33:23Z
type: feature
priority: 2
assignee: Ryan Swift
---
# Add review and tests skills for Build agent self-check

Create skill versions of the review and tests prompts so the Build agent can self-review its own work before presenting it to the user. Skills are loaded on-demand by any agent via the skill tool. The skill would contain the checklist/instructions portion of the agent prompt without the permission enforcement. Main use case: Build finishes writing code, loads the review skill, and self-checks before showing the result. Skills go in ~/.config/opencode/skill/code-review/SKILL.md and ~/.config/opencode/skill/test-coverage/SKILL.md. Decision needed: does this workflow actually match how you want to use it, or is the dedicated agent sufficient?

