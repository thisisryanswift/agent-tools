# agent-tools

Agents, prompts, and plugins for AI coding tools. Designed to critically review AI-generated code before you commit or merge it.

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

### Brainstorming skill
- Turns rough ideas into validated designs through collaborative dialogue
- Asks one question at a time, proposes 2-3 approaches with trade-offs
- Presents design in digestible sections for incremental validation
- Adapted from [obra/superpowers](https://github.com/obra/superpowers) (MIT License)

### git-ai plugin (OpenCode)
- Tracks which code changes are human-authored vs AI-authored
- Creates checkpoints before and after every file edit
- Requires [git-ai](https://github.com/acunniffe/git-ai) installed in PATH
- Gracefully degrades if git-ai is not available

All agents are **model-agnostic** -- they use whatever model you have configured globally.

## Repository structure

```
prompts/              # Source of truth for all prompt logic
  review-prompt.md
  tests-prompt.md
  brainstorming-prompt.md

agent/                # OpenCode agent definitions (reference prompts/)
command/              # OpenCode slash commands (inject git context)
plugin/               # OpenCode plugins
  git-ai.ts

skills/               # Agent Skills spec (for Claude Code, Gemini CLI, etc.)
  code-review/
  test-coverage/
  brainstorming/

Makefile              # sync and check targets
```

## Install

### OpenCode

**Option A: Manual copy**

```bash
make install
```

Or copy files individually:

```bash
mkdir -p ~/.config/opencode/agents ~/.config/opencode/command ~/.config/opencode/prompts ~/.config/opencode/plugin

cp prompts/*.md ~/.config/opencode/prompts/
cp agent/*.md ~/.config/opencode/agents/
cp command/*.md ~/.config/opencode/command/
cp plugin/*.ts ~/.config/opencode/plugin/
```

**Option B: chezmoi externals (recommended for multi-machine setups)**

Add this to `~/.local/share/chezmoi/.chezmoiexternal.toml`:

```toml
[".config/opencode/prompts/review-prompt.md"]
    type = "file"
    url = "https://raw.githubusercontent.com/thisisryanswift/agent-tools/main/prompts/review-prompt.md"
    refreshPeriod = "168h"

[".config/opencode/prompts/tests-prompt.md"]
    type = "file"
    url = "https://raw.githubusercontent.com/thisisryanswift/agent-tools/main/prompts/tests-prompt.md"
    refreshPeriod = "168h"

[".config/opencode/prompts/brainstorming-prompt.md"]
    type = "file"
    url = "https://raw.githubusercontent.com/thisisryanswift/agent-tools/main/prompts/brainstorming-prompt.md"
    refreshPeriod = "168h"

[".config/opencode/agents/review.md"]
    type = "file"
    url = "https://raw.githubusercontent.com/thisisryanswift/agent-tools/main/agent/review.md"
    refreshPeriod = "168h"

[".config/opencode/agents/tests.md"]
    type = "file"
    url = "https://raw.githubusercontent.com/thisisryanswift/agent-tools/main/agent/tests.md"
    refreshPeriod = "168h"

[".config/opencode/command/review.md"]
    type = "file"
    url = "https://raw.githubusercontent.com/thisisryanswift/agent-tools/main/command/review.md"
    refreshPeriod = "168h"

[".config/opencode/command/tests.md"]
    type = "file"
    url = "https://raw.githubusercontent.com/thisisryanswift/agent-tools/main/command/tests.md"
    refreshPeriod = "168h"

[".config/opencode/plugin/git-ai.ts"]
    type = "file"
    url = "https://raw.githubusercontent.com/thisisryanswift/agent-tools/main/plugin/git-ai.ts"
    refreshPeriod = "168h"
```

Then run `chezmoi apply` (or `chezmoi -R apply` to force refresh).

Restart OpenCode for agents to appear.

### Claude Code & Gemini CLI (Agent Skills)

This repository supports the [Agent Skills](https://agentskills.io) specification. Link skills to your tool's configuration directory:

**Claude Code**
```bash
mkdir -p ~/.claude/skills
ln -s $(pwd)/skills/code-review ~/.claude/skills/code-review
ln -s $(pwd)/skills/test-coverage ~/.claude/skills/test-coverage
ln -s $(pwd)/skills/brainstorming ~/.claude/skills/brainstorming
```

**Gemini CLI**
```bash
mkdir -p .gemini/skills
ln -s $(pwd)/skills/code-review .gemini/skills/code-review
ln -s $(pwd)/skills/test-coverage .gemini/skills/test-coverage
ln -s $(pwd)/skills/brainstorming .gemini/skills/brainstorming
```

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

## Keeping skills in sync

The files in `skills/*/references/` are copies of the source-of-truth in `prompts/`. To check for drift:

```bash
make check
```

To sync copies from prompts:

```bash
make sync
```

## Model agnostic

No agent has a model pinned. They use whatever model you have configured globally. Switch models before reviewing to get a different perspective:

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

## Customization

Edit the prompt files in `prompts/` to:

- Adjust the review checklist for your domain
- Change severity thresholds or coverage criteria
- Add project-specific patterns to watch for
- Modify the output format

After editing, run `make sync` to propagate changes to the skills references.

## Credits

- Brainstorming skill adapted from [obra/superpowers](https://github.com/obra/superpowers) (MIT License)
- git-ai plugin integrates with [acunniffe/git-ai](https://github.com/acunniffe/git-ai)

## License

MIT
