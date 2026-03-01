---
description: Identify missing test coverage in recent code changes
agent: tests
---

Analyze the following code changes for missing test coverage.

## Repository State

!`git status --short`

## Recent Commits

!`git log --oneline -10`

## Diff Stats

!`git diff --stat $ARGUMENTS 2>/dev/null; git diff --cached --stat 2>/dev/null`

## Changes to Analyze

!`if [ -n "$ARGUMENTS" ]; then git diff $ARGUMENTS; else git diff; if [ -z "$(git diff)" ]; then git diff --cached; fi; fi`

## Instructions

Analyze all the changes shown above for missing test coverage. Follow your full review protocol:

1. Gather project context (read AGENTS.md, discover test conventions).
2. Understand what logic was added or changed.
3. Locate related test files.
4. Assess coverage: missing, partial, or covered.
5. Produce your structured report.

If `$ARGUMENTS` was provided, it may be a commit range (e.g., `HEAD~3`), a branch comparison (e.g., `main...HEAD`), or a path filter (e.g., `src/api/`). The diff above was produced by passing it directly to `git diff`.

If no `$ARGUMENTS` was provided, unstaged changes are shown. If there were no unstaged changes, staged changes are shown instead.

If the diff above is empty, tell the user there are no changes to analyze and suggest how to target specific changes (e.g., `/tests HEAD~3`, `/tests main...HEAD`).

If the diff stats above show a very large changeset (more than ~1000 lines changed across many files), recommend the user narrow the scope by analyzing per-directory or per-commit range.
