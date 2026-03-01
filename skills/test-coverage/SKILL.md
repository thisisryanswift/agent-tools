---
name: test-coverage
description: Identifies missing test coverage in changed code. Use this when asked to check what tests need to be written for recent changes.
---

# Test Coverage Skill

This skill provides a structured protocol for identifying gaps in test coverage.

## Instructions

To analyze test coverage, you must follow the protocol defined in the reference prompt:
See [references/tests-prompt.md](references/tests-prompt.md) for the complete guidelines.

1. **Read the Prompt:** Load `references/tests-prompt.md` into your context.
2. **Execute:** Follow its phases precisely to assess covered, partial, and missing paths for the provided diff or files.
3. **Format:** Output your findings using the exact Markdown format specified in the prompt.