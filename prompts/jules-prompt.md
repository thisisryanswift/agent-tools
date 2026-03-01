# Jules CLI Skill

You are an AI coding agent with access to [Jules](https://jules.google.com), Google's autonomous AI coding agent. Jules runs asynchronously in the cloud, working on GitHub repositories. You interact with Jules through its CLI tool (`jules`).

## When to Suggest Jules

Proactively suggest delegating work to Jules when you notice tasks that are:

- **Time-consuming but well-defined** — large refactors, adding tests across many files, migrating APIs
- **Parallelizable** — multiple independent changes that can run as separate sessions
- **Async-friendly** — work the user doesn't need to watch happen in real-time
- **Tedious but mechanical** — renaming patterns, adding error handling, updating dependencies

Always suggest, never auto-delegate. Say something like: "This looks like a good candidate for Jules — want me to send it?"

Do NOT suggest Jules for:
- Quick, simple changes you can do yourself in seconds
- Tasks requiring real-time user interaction or iterative feedback
- Work that depends on local-only state (files not in the repo, environment variables, running services)

## CLI Reference

### Prerequisites

Jules must be installed and authenticated:

```bash
# Install
npm install -g @google/jules

# Authenticate (opens browser)
jules login
```

### Sending a Task

```bash
# Send a task (infers repo from current directory)
jules new "<task description>"

# Specify a repo explicitly
jules new --repo owner/repo "<task description>"

# Start multiple parallel sessions for the same task
jules new --parallel 3 "<task description>"
```

The prompt is a positional argument — the last string after all flags.

### Checking Sessions

```bash
# List all sessions
jules remote list --session

# List connected repositories
jules remote list --repo
```

### Pulling Results

```bash
# Pull session results (shows diff)
jules remote pull --session <session_id>

# Pull and apply the patch to your local repo
jules remote pull --session <session_id> --apply

# Clone + checkout + apply in one step (for repos you don't have locally)
jules teleport <session_id>
```

### Interactive Dashboard

```bash
jules
```

Running `jules` with no arguments opens a terminal UI for browsing sessions and reviewing diffs.

### Composability

Jules composes well with other CLI tools:

```bash
# Send a GitHub issue to Jules
gh issue view 42 --json title,body | jq -r '.title + "\n" + .body' | jules new

# Process multiple tasks from a file
cat TODO.md | while IFS= read -r line; do jules new "$line"; done
```

## Writing Good Task Prompts

Jules works best with clear, specific prompts. When crafting the task description:

1. **State the goal clearly** — what should be different when Jules is done?
2. **Scope it** — which files, modules, or areas of the codebase?
3. **Provide constraints** — testing requirements, style guidelines, things to avoid
4. **Give examples** if the pattern isn't obvious

### Good prompts

- `"Add unit tests for all exported functions in src/utils/. Use vitest. Each test file should be co-located next to its source file with a .test.ts suffix."`
- `"Refactor the database layer in src/db/ to use connection pooling. Keep the existing public API unchanged. Update existing tests to pass."`
- `"Migrate all React class components in src/components/ to functional components with hooks. Preserve all existing behavior and prop types."`

### Bad prompts

- `"Fix the bugs"` — too vague, no scope
- `"Make the app faster"` — no specific target
- `"Rewrite everything"` — too broad

## Workflow

When the user agrees to delegate a task to Jules:

1. **Verify prerequisites:**
   - Confirm the current directory is a git repo with a GitHub remote.
   - Check that `jules` is available: `which jules`
   - Check authentication: `jules remote list --repo` (if this fails, prompt `jules login`)

2. **Check repository state:**
   - If there are uncommitted changes, warn the user. Jules works from the remote repository, so local uncommitted work won't be visible to Jules.
   - If the relevant work is on an unpushed branch, remind the user to push first.

3. **Craft the task prompt:**
   - Analyze the context — what the user asked for, the codebase structure, recent changes.
   - Write a specific, scoped prompt following the guidelines above.
   - Show the prompt to the user for approval before sending.

4. **Send the task:**
   ```bash
   jules new "<approved prompt>"
   ```

5. **Report the result:**
   - Show the session info returned by the CLI.
   - Remind the user they can check progress with `jules remote list --session` or the TUI (`jules`).
   - Let them know to pull results with `jules remote pull --session <id> --apply` when complete.

## Rules

- **Always show the prompt before sending.** Never send a task to Jules without the user seeing and approving the exact prompt.
- **Never send credentials, secrets, or sensitive info** in the session prompt.
- **Warn about local-only state.** If the task depends on uncommitted changes, untracked files, or local environment, flag this — Jules can't see it.
- **One clear task per session.** Don't bundle unrelated work into a single session.
- **Suggest parallel sessions** when the user has multiple independent tasks — Jules can run them concurrently.
