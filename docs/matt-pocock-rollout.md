# Matt Pocock baseline rollout

## Decision and deployment — 2026-10-28

Ryan selected **one engineering pack: Matt Pocock's promoted skills**, not a merge
of Superpowers, Compound Engineering, and pstack. Install globally on execution
accounts. OpenCode, Claude Code, Codex, and Antigravity CLI are now installed on
Reef, with discovery/basic loading checks below. Full workflows and other hosts
are not certified.

- Upstream: <https://github.com/mattpocock/skills>
- Pin: `59db609eb1e18aaf59b63284d0e52255aff0c63c` (October 27; version 1.3.1).
- License: MIT, Matt Pocock; retained in the complete source checkout.
- Source: `~/.local/share/agent-tools/upstreams/mattpocock-skills/<pin>`.
- Global links:

  | Runtime | Discovery directory |
  | --- | --- |
  | OpenCode | `~/.config/opencode/skills/` |
  | Claude Code | `~/.claude/skills/` |
  | Codex | `~/.agents/skills/` (shared user skills, not another copy in `.codex/skills`) |
  | Antigravity CLI | `~/.gemini/antigravity-cli/skills/` |
- Selection: exactly 27 entries from `.claude-plugin/plugin.json`, not experimental
  or misc skills. Whole directories preserve sibling references.

Upstream files are unchanged. No automatic updates or parallel marketplace install.
The existing personal specialists were preserved. No existing files in Reef's
global OpenCode skills directory needed replacement. The old engineering sources
in this repository remain reference material, not a second installed baseline.
The old brainstorming-fix proposal (`at-duwo`) is superseded, not implemented.

## Reproduction and maintenance

On an authorized execution host, obtain the pinned checkout, then run the installer
from this repository:

```bash
git clone --no-checkout https://github.com/mattpocock/skills.git \
  ~/.local/share/agent-tools/upstreams/mattpocock-skills/59db609eb1e18aaf59b63284d0e52255aff0c63c
git -C ~/.local/share/agent-tools/upstreams/mattpocock-skills/59db609eb1e18aaf59b63284d0e52255aff0c63c \
  -c core.hooksPath=/dev/null checkout --detach 59db609eb1e18aaf59b63284d0e52255aff0c63c
python3 scripts/install-matt-skills.py --dry-run
python3 scripts/install-matt-skills.py
# The other global consumers use the same pin and installer:
python3 scripts/install-matt-skills.py --destination ~/.claude/skills
python3 scripts/install-matt-skills.py --destination ~/.agents/skills
python3 scripts/install-matt-skills.py --destination ~/.gemini/antigravity-cli/skills
```

The installer honors XDG data/config roots; adjust the clone destination or pass
`--source` for a non-default data root. It requires the exact pin and unchanged
promoted sources, preflights the entire pack, refuses foreign/dangling links or
files, and preserves matching links. It does not download or run upstream code.
The clone command refuses an existing source directory rather than overwriting it.

Links are installer-owned state, not automatically provisioned by chezmoi. Policy
is managed separately below. Copying links alone does not deploy the policy.
Updates require reviewing the next revision, changing the installer pin, and
explicitly migrating owned links; the installer does not silently repoint them.
For rollback, remove only links still resolving to this pin's promoted directories,
preserve replaced entries/source, and reconcile the policy in chezmoi's source
without resetting unrelated dotfiles work.

## Local policy without a fork

OpenCode policy is sourced from
`~/.local/share/chezmoi/dot_config/opencode/AGENTS.md.tmpl`. Equivalent policy for
the other consumers was added to the existing shared
`~/.local/share/chezmoi/.chezmoitemplates/agents.md`. Only these rendered targets
were applied on Reef:

- `~/.config/opencode/AGENTS.md`
- `~/.claude/CLAUDE.md`
- `~/.codex/AGENTS.md`
- `~/.gemini/GEMINI.md` (Antigravity CLI global rules; its added memories preserved)

Policy boundaries:

- Selected Matt workflows may delegate through stock OpenCode tools.
- Existing authorization/preservation boundaries win over skill commit, publish,
  reset, and cleanup instructions.
- Existing trackers win; `.tickets/` uses `tk`, not a parallel `.scratch` or GitHub
  tracker. Missing project setup is not silently scaffolded.
- WIP review explicitly covers agreed staged/unstaged/relevant untracked work.
  Upstream's `<fixed-point>...HEAD` diff alone excludes uncommitted implementation.

These are prompt-level boundaries, not a new enforcement mechanism. No project
setup, global JSON configuration, permission settings, or other hosts were changed.

## Verification

OpenCode **2.1.4** on Reef sees all 27 promoted skills via
`opencode api get /api/skill` at location `/home/rswift`, outside this project.
Every source path resolves to the pin. All 16 user-invoked skills have
`autoinvoke: false`; 11 remain model-invoked. Hiding a skill from the catalog is
not a security boundary: known IDs can still be explicitly loaded.

The active session received the new skill catalog and loaded `writing-for-agents`
through the native tool. No restart was needed. Repeat installer dry-run recognizes
all links; scoped `chezmoi verify` passes. `make check` passes (8 personal skills,
3 prompt copies), and `make test` passes (8 installer tests). Personal-skill counts
are separate from the external Matt pack.

This proves discovery, metadata, directory/reference preservation, and basic
loading, **not** a full implementation/review workflow or cross-runtime parity.
Use `@ask-matt` or `@setup-matt-pocock-skills` to explicitly load a skill in
OpenCode. Setup remains per-project and user-selected. Skill installation does not
create dedicated slash commands.

### Additional consumers and overlap audit

The same unchanged 27-skill pin was linked into the three other discovery roots.
All destinations were preflighted before installation, and 56 existing specialist
skill files were checked unchanged byte-for-byte. No new marketplace plugin was
installed, and no existing skill or bundled plugin was disabled.

- **Claude Code 2.1.286:** a bounded no-tools print-mode smoke run completed
  successfully. Its initialization command catalog advertised all 27 Matt skills.
  Use `/ask-matt`; these are personal standalone skills, not a separately installed
  marketplace plugin. Matt's personal `code-review` intentionally takes the same
  command name as Claude's bundled `/code-review`; other built-in aliases are not
  globally disabled.
- **Codex CLI 0.159.3:** initialized an app-server stdio connection and queried
  `skills/list` at `/home/rswift` without creating a thread or starting a model
  turn. All 27 pinned skills appeared exactly once, with no discovery errors.
  The runtime exposed them as `mattpocock-skills:<id>` with canonical paths in the
  upstream checkout. Use the skill picker or `$mattpocock-skills:ask-matt`.
- **Antigravity CLI:** official CLI skill location is the CLI-specific directory
  above, not the app/IDE's `~/.gemini/config/skills`. A plan/sandbox print-mode
  `/ask-matt` smoke run completed with `expanded_commands` identifying it as a
  skill, and only `user_input`/`agent_response` steps (no tools). Global folder
  contents/path resolution for all 27 were checked; the CLI's init event does
  not list every discovered skill. No full workflow or all-skill activation test.

The upstream user-invocation frontmatter and Codex `agents/openai.yaml` files are
preserved. Antigravity's documentation does not establish identical enforcement
of those fields; shared rules also require explicit selection for user-invoked
workflows. Do not infer identical behavior from installation alone.

There are **no active user copies of the old engineering pack to clean out** in
the inspected Reef discovery roots. Retain `browser-harness`, `ryan-blog`,
`wayland-app-icon-fix`, and Codex's `agent-workspace-linux` plus its system skills.
The old `code-review`, `brainstorming`, and their review adapters remain reference
material. Ryan subsequently requested deletion of `test-coverage`: its skill,
canonical/copied prompt, dedicated agent/command, and sync/check entries were
removed. Installer tests remain and reject attempts to install the retired ID.
After retirement, `make check` covers 7 personal skills and 2 prompt copies;
the earlier 8/3 counts above describe the pre-retirement snapshot. Project-local
overrides and other machines were not exhaustively searched.

Discovery references: [Claude skills](https://code.claude.com/docs/en/skills),
[Codex local skills](https://developers.openai.com/codex/build-skills),
[Codex skills/list](https://developers.openai.com/codex/app-server),
[Antigravity skills](https://antigravity.google/docs/skills/), and
[Antigravity rules](https://antigravity.google/docs/rules/) (CLI tabs).

## Crit follow-up

Global `tk` defaults and manual Crit support are now implemented; see
[the deployment record](global-workflow.md). Crit v0.23.1 in `~/.local/bin` takes
precedence over the stale root-owned launcher, which was not modified. The manual
skill is linked for all four runtimes. Requested reviews use the approved
tailnet-hosted **https://crit.wharfi.sh** target; local mode is only for explicit
local requests. No hooks or automatic review gates were added. Hosted publication,
a real human comment, and authenticated feedback fetch passed, and Ryan closed
the test review without requiring a revision (`at-nxnl` closed). The managed global
instructions now agree with the hosted skill; see the deployment record for
authentication, review-state isolation, and remaining operational checks.
