# review-agent

Code review and test coverage agents for [OpenCode](https://opencode.ai). Designed to critically review AI-generated code before you commit or merge it.

## What's included

### Review agent (`/review`)
- Reviews diffs for logic errors, security issues, performance problems, and AI slop
- Reads your project's `AGENTS.md` and surrounding code to understand conventions before reviewing
- Produces structured reports with severity levels and actionable suggestions
- Read-only: cannot modify your files

### Tests agent (`/tests`)
- Identifies missing or incomplete test coverage in changed code
- Discovers your project's test conventions automatically (any framework, any language)
- Locates related test files and assesses what's covered vs. what's missing
- Read-only: identifies gaps, does not write tests

Both agents are **model-agnostic** -- they use whatever model you have configured globally.

## Install

Create the directories if they don't exist, then copy the files:

```bash
mkdir -p ~/.config/opencode/agents ~/.config/opencode/command

# Agents
cp agent/review.md ~/.config/opencode/agents/review.md
cp agent/tests.md ~/.config/opencode/agents/tests.md

# Commands
cp command/review.md ~/.config/opencode/command/review.md
cp command/tests.md ~/.config/opencode/command/tests.md
```

Restart OpenCode for the agents to appear.

## Usage

### Review

```
# Tab to Review mode, then ask questions
<Tab>                              # cycle to Review agent
Review the auth middleware changes

# /review command (pre-loads git diff)
/review                            # unstaged changes (falls back to staged)
/review HEAD~3                     # last 3 commits
/review main...HEAD                # current branch vs main
/review -- src/api/                # changes in a specific directory

# @mention from Build mode
@review check the last commit for security issues
```

### Tests

```
# Tab to Tests mode, then ask questions
<Tab>                              # cycle to Tests agent
Check test coverage for the new auth module

# /tests command (pre-loads git diff)
/tests                             # unstaged changes (falls back to staged)
/tests HEAD~3                      # last 3 commits
/tests main...HEAD                 # current branch vs main

# @mention from Build mode
@tests what's untested in the last commit?
```

## Model agnostic

Neither agent has a model pinned. They use whatever model you have configured globally. Switch models before reviewing to get a different perspective:

```
/model google/gemini-2.5-pro
```

This works well for an "AI reviewing AI" workflow: have one model write the code, switch to a different model, then review.

## What gets reviewed

### Review agent

| Category | Examples |
| --- | --- |
| Logic & Correctness | Edge cases, off-by-one, race conditions, error handling |
| Security | Input validation, auth, secrets exposure, injection |
| Performance | N+1 queries, unnecessary allocations, blocking async |
| AI Slop | Comment noise, paranoid null checks, tautological names, single-use abstractions |
| Idiomatic Style | Project conventions, language idioms, naming consistency |

### Tests agent

| Focus | Examples |
| --- | --- |
| Missing coverage | New functions/methods with no tests |
| Partial coverage | Tests exist but miss error paths or edge cases |
| Branch coverage | Untested if/else, switch, guard clauses |
| Edge cases | Empty inputs, boundary values, null handling |
| Integration points | Unmocked external calls, missing integration tests |

## Output formats

### Review report

```
## Review Summary

| Severity | Count |
| -------- | ----- |
| Critical | 1     |
| Major    | 2     |
| Minor    | 0     |
| Nit      | 1     |

**Verdict:** ACCEPT WITH CHANGES

## Findings

### [Critical] src/auth.ts:42 - Missing authorization check

**Category:** Security
**Issue:** The endpoint allows unauthenticated access to user data.
**Rationale:** Any caller can read arbitrary user records without a token.
**Suggestion:**
...

## What Looks Good

The error handling in the payment flow correctly retries transient failures.
```

### Tests report

```
## Test Coverage Summary

| Status  | Count |
| ------- | ----- |
| Missing | 2     |
| Partial | 1     |
| Covered | 3     |

## Findings

### [Missing] src/auth.ts:42 - Login handler has no tests

**Changed Logic:** New login function with password validation and token generation.
**Related Tests:** None found.
**Expected Coverage:** Test valid login, invalid password, missing user, and token expiry.

### [Partial] src/api/users.ts:88 - Error path not tested

**Changed Logic:** Added error handling for database connection failures.
**Related Tests:** tests/api/users.test.ts:15 - tests success path only.
**Gap:** No test for connection failure branch.
**Expected Coverage:** Test database unavailable scenario.

## Already Well-Tested

The input validation in src/api/users.ts has thorough tests covering all edge cases.
```

## Customization

Edit the agent files in `~/.config/opencode/agents/` to:

- Adjust the review checklist for your domain
- Change severity thresholds or coverage criteria
- Add project-specific patterns to watch for
- Modify the output format

## License

MIT
