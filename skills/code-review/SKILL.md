---
name: code-review
description: Reviews AI-generated code for correctness, security, performance, and slop. Use this when you are asked to review a diff or recent changes.
---

# Code Review Skill

This skill provides a structured protocol and checklist for reviewing code changes.

## Instructions

To execute a code review, you must follow the protocol and checklist defined in the reference prompt:
See [references/review-prompt.md](references/review-prompt.md) for the complete guidelines.

1. **Read the Prompt:** Load `references/review-prompt.md` into your context.
2. **Execute:** Follow its phases precisely, conducting a systematic audit of the provided diff or files.
3. **Format:** Output your review using the exact Markdown format specified in the prompt.