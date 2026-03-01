---
description: Review code changes (staged, unstaged, commits, or branch diffs)
agent: review
---

Review the following code changes.

## Repository State

!`git status --short`

## Recent Commits

!`git log --oneline -10`

## Diff Stats

!`git diff --stat $ARGUMENTS 2>/dev/null; git diff --cached --stat 2>/dev/null`

## Changes to Review

!`if [ -n "$ARGUMENTS" ]; then git diff $ARGUMENTS; else git diff; if [ -z "$(git diff)" ]; then git diff --cached; fi; fi`

## Instructions

Review all the changes shown above. Follow your full review protocol:

1. Gather project context (read AGENTS.md, understand conventions).
2. Understand the intent behind these changes from the commit messages and diff.
3. Audit systematically against your checklist.
4. Produce your structured report.

If `$ARGUMENTS` was provided, it may be a commit range (e.g., `HEAD~3`), a branch comparison (e.g., `main...HEAD`), or a path filter (e.g., `src/api/`). The diff above was produced by passing it directly to `git diff`.

If no `$ARGUMENTS` was provided, unstaged changes are shown. If there were no unstaged changes, staged changes are shown instead.

If the diff above is empty, tell the user there are no changes to review and suggest how to target specific changes (e.g., `/review HEAD~3`, `/review main...HEAD`).

If the diff stats above show a very large changeset (more than ~1000 lines changed across many files), recommend the user narrow the scope by reviewing per-directory or per-commit range rather than attempting a full review of a massive diff.
