---
name: browser-harness-cli
description: Use the Python Browser Harness CLI and isolated browser workers for interactive web tasks, screenshots, logged-in workflows, and reusable site knowledge when those commands are installed on the execution host.
---

# Browser Harness CLI

This skill covers `browser-harness`, `browser-harness-isolated`, and
`browser-harness-worker`: the Python/CDP tooling and Ryan's worker package.
Client-native browser tools have their own target IDs and APIs; use their own
instructions. This skill's distinct ID avoids replacing OpenCode's built-in
`browser-harness` skill.

Browser Harness uses the model running the current agent; it does not choose or
invoke a model itself. Prefer direct HTTP fetches for public static pages/APIs.
Use a browser when interaction, logged-in state, JavaScript, or screenshots matter.

## Execution host and profile

Determine where the commands and browser run. A Paseo client on a laptop does not
make that laptop's browser profile available to an agent on Reef. Check the
installed command versions and their help before relying on optional features.

Use a named isolated profile unless Ryan explicitly requests the main Chrome
profile or an approved cloud browser:

```bash
browser-harness-isolated research <<'PY'
new_tab("https://example.com")
wait_for_load()
print(page_info())
PY
```

- Profile names match `[A-Za-z0-9_-]{1,48}`. Choose a stable task-specific name.
- Concurrent agents use distinct names. Reusing a name deliberately reuses its
  cookies, tabs, Chrome process, and harness daemon.
- Use heredocs for multiline Python; the harness pre-imports its helpers.
- First navigation opens a task-owned tab. Subsequent commands reuse that tab;
  inspect `current_tab()` and `list_tabs()` and use `switch_tab()` as needed.
- Avoid duplicate tabs and close only tabs created for the task.
- Use plain `browser-harness` against the main Chrome profile only when requested.
- A failed isolated profile does not justify falling back to the main profile.

## Authenticated workers

For user-authorized parallel browser tasks, a controller can provision separate
workers using approved capabilities from the host's authentication registry:

```bash
browser-harness-worker create session42-worker1 --capability zoho-crm
browser-harness-worker run session42-worker1 <<'PY'
print(page_info())
PY
browser-harness-worker destroy session42-worker1
```

The controller owns provisioning and cleanup, including failed/cancelled tasks.
Give each worker agent one worker name and its `run` command; the worker agent
does not create, select, reassign, or destroy workers. Use `list` and `cleanup`
for ownership-checked stale cleanup. The current package permits four active local
workers; queue excess work rather than silently moving to cloud execution.

Workers receive only approved-domain cookies from the selected source profile,
not extensions, local storage, history, or the whole profile. Use only the user's
authorized authentication context; ask about ambiguous accounts or overlapping
domains. Never print cookies or put them in prompts, logs, or knowledge files.
The package isolates cooperative workers; ordinary Python/raw CDP is not a
sandbox against malicious code running as the same OS user.

## Workspace and shared learning

Use the workspace actually configured for this host. The packaged worker tooling
can use `BH_AGENT_WORKSPACE` and standard XDG paths; Ryan's older wrappers resolve
a chezmoi source workspace. Inspect the wrapper/configuration before choosing a
path. A wrapper's child-process environment is not automatically available to the
agent's next shell command.

For a confirmed chezmoi-managed workspace, resolve the source explicitly:

```bash
chezmoi source-path "$HOME/.config/browser-harness/agent-workspace"
```

Before site-specific work, read the matching site's files under `domain-skills/`.
When work reveals reusable knowledge:

- Add general primitives to the workspace's `agent_helpers.py`.
- Put durable selectors, APIs, waits, navigation patterns, and pitfalls under
  `domain-skills/<site>/`.
- Exclude credentials, cookies, personal data, narration, and pixel coordinates.
- Re-read shared files immediately before editing and preserve concurrent edits.
- Report changed knowledge files; commits and pushes require authorization.

Learning is instruction-driven. The harness does not independently infer and
persist knowledge in the background. Keep mutable workspace knowledge separate
from the installed skill's source.

## Page workflow

1. Prefer the accessibility tree for interactive elements:
   `cdp("Accessibility.getFullAXTree")["nodes"]`.
2. Resolve an AX node's `backendDOMNodeId` with `DOM.getBoxModel`, interact with
   its box, and verify the actual result. Use `js(...)` when DOM inspection is
   more suitable and screenshots when visible layout matters.
3. After navigation, call `wait_for_load()`. Use `ensure_real_tab()` to recover
   from a stale/internal attached tab.
4. Stop at passwords, MFA, consent, or ambiguous account selection. Existing
   unambiguous SSO in the chosen isolated profile may be used.
5. Raw CDP remains available through `cdp("Domain.method", ...)`.

## Cloud, recordings, and diagnostics

Cloud use may incur billing and transfer authentication state; obtain the user's
approval before using it. Follow the installed version's upstream instructions
and stop task-owned cloud browsers when finished. Record only when the user asks
to record, demonstrate, or make a video; do not reenact finished work just to record.

- `browser-harness --doctor` reports harness diagnostics.
- A named-profile launch failure reports its local Chrome log path.
- Upstream: https://github.com/browser-use/browser-harness
- Workers: https://github.com/thisisryanswift/browser-harness-workers
