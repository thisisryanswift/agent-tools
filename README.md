# agent-tools

Ryan's personal agent toolkit: selected coding, writing, browser, and maintenance
skills, with explicit runtime and execution-host choices. This repository is
tailored to Ryan's setup; it is not a generally supported agent distribution.

## Working plan

The [approved plan](docs/personal-agent-toolkit-plan.md) describes the Reef-centered
Paseo coding environment, Hermes's separate assistant role, and the broader roadmap.
See the [skill catalog](docs/skill-catalog.md) for selections and compatibility,
[source provenance](docs/source-provenance.md) for imported material, and
[consolidation status](docs/consolidation-status.md) for implementation progress.

## What's included

### Code review
- Reviews diffs for logic errors, security issues, performance problems, and AI slop
- Reads your project's `AGENTS.md` and surrounding code to understand conventions before reviewing
- Produces structured reports with severity levels and actionable suggestions
- Requests read-only review; runtime permissions must enforce access restrictions

### Test coverage
- Identifies missing or incomplete test coverage in changed code
- Discovers your project's test conventions automatically (any framework, any language)
- Locates related test files and assesses what's covered vs. what's missing
- Read-only: identifies gaps, does not write tests

### Brainstorming skill
- Turns rough ideas into validated designs through collaborative dialogue
- Asks one question at a time, proposes 2-3 approaches with trade-offs
- Presents design in digestible sections for incremental validation
- Adapted from [obra/superpowers](https://github.com/obra/superpowers) (MIT License)

### Specialist skills
- `agent-session-migration`: OpenCode V2 session location and transfer workflow
- `ryan-blog`: current blogging guidance consolidated with the older style skill
- `browser-harness-cli`: isolated profiles and workers through the Python/CDP CLI
- `wayland-app-icon-fix`: runtime/desktop identity diagnosis on a Linux desktop

Jules and ToolHive are retired from the target toolkit.

### Retained OpenCode adapters

`agent/` and `command/` contain the older review/tests adapters. V2 documents
compatibility for these file formats; this repository's permissions and command
behavior still need runtime verification. `plugin/git-ai.ts` uses the V1 plugin
API and requires a port before OpenCode V2 use. The skill installer installs none
of these adapters.

The skills do not pin a model. A portable file format does not establish equivalent
behavior across models, runtimes, or clients; record those results separately.

## Repository structure

```
prompts/              # Canonical prompts for the original engineering skills
  review-prompt.md
  tests-prompt.md
  brainstorming-prompt.md

agent/                # OpenCode agent definitions (reference prompts/)
command/              # OpenCode slash commands (inject git context)
plugin/               # Retained V1 integration source
  git-ai.ts

skills/               # Canonical portable units, selected individually
  code-review/
  test-coverage/
  brainstorming/
  agent-session-migration/
  ryan-blog/
  browser-harness-cli/
  wayland-app-icon-fix/

docs/                 # Plan, catalog, provenance, and progress
evals/                # Evaluation migration notes
scripts/              # Structural checker and explicit skill-link installer
tests/                # Installer preservation tests
Makefile              # check, sync, test, and install targets
```

## Install

Install on the host/account where the agent executes, from a persistent checkout
it can read. Paseo clients do not each need a copy of every runtime's skills.
Choose individual IDs from the catalog and confirm that runtime's discovery path.
Hermes gets its own selected set and profile-scoped deployment.

With Python 3.9+:

```bash
# Example: preview selected skills for an OpenCode execution account.
python3 scripts/install-skills.py \
  --destination "$HOME/.config/opencode/skills" --dry-run \
  code-review test-coverage

# Apply to the chosen discovery directory.
make install ARGS='--destination /absolute/discovery/directory code-review test-coverage'
```

The installer links whole skill directories, preserving relative references.
It preflights the selection, preserves existing files/foreign links, and is
idempotent for matching links. It requires an explicit destination and skill list.
Keep the source checkout at its chosen path while links use it.

Compare any existing installed copies before a cutover, especially chezmoi-managed
files. Update managed sources and apply only scoped targets. Check discovery in
the actual runtime after installation; host paths, tools, and session reload rules
remain runtime-specific. The legacy automatic chezmoi downloads are retired.

## Retained adapter usage

These commands apply after explicitly enabling compatible OpenCode agent/command
adapters. For portable skills, ask the runtime to load the selected catalog ID.

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

The three engineering skills keep copied prompt references. Specialist skills are
edited directly in their own directories. To check frontmatter basics, portable
Markdown references, prompt-copy drift, and installer behavior:

```bash
make check
make test
```

To sync copies from prompts:

```bash
make sync
```

## Model agnostic

Select models through the runtime's normal controls. Independent reviews can use
a different model, but this is a workflow choice rather than evidence of better
results. See [evaluation notes](evals/README.md) for the current evidence status.

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
