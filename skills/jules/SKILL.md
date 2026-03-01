---
name: jules
description: "Delegates tasks to Google Jules, an autonomous AI coding agent. Suggest Jules for time-consuming, well-defined, or parallelizable work. Always ask before sending."
---

# Jules CLI Skill

This skill teaches agents how to use the [Jules CLI](https://jules.google.com) to delegate coding tasks to Google's autonomous AI agent.

## Instructions

To delegate a task to Jules, follow the protocol defined in the reference prompt:
See [references/jules-prompt.md](references/jules-prompt.md) for the complete guidelines.

1. **Read the Prompt:** Load `references/jules-prompt.md` into your context.
2. **Recognize Opportunities:** Proactively suggest Jules for async, parallelizable, or mechanical tasks.
3. **Execute:** Follow the workflow — verify prerequisites, craft a prompt, get user approval, send the task.
4. **Report:** Show session info and remind the user how to check progress and pull results.
