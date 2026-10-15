# Skill catalog

Source selection as of 2026-10-01. Owner: Ryan, in `agent-tools`. These are local
source candidates for deployment; structural checks are not runtime qualification.
See [provenance](source-provenance.md) and [rollout status](consolidation-status.md).

## Selected skills

| ID | Purpose and intended consumer | Execution host / required capabilities | Evidence and remaining check |
| --- | --- | --- | --- |
| `code-review` | Requested diff review in coding runtimes | Reef or the selected repository host; repository reads, Git, search | Existing prompt retained; reference copy checked. Test findings and read-only permissions in each runtime. |
| `test-coverage` | Requested coverage-gap analysis in coding runtimes | Repository and tests on execution host; Git and search | Existing prompt retained; reference copy checked. Test usefulness and false-positive rate. |
| `brainstorming` | Deliberate design dialogue when selected | Host with project context and a place to write the design | Existing Superpowers-derived protocol retained. Its broad automatic trigger and approval/commit rules need preference alignment before deployment. |
| `agent-session-migration` | OpenCode V2 session administration; optional Hermes use only with that capability | The owning OpenCode server and authenticated CLI/API, or the native session-move tool | Rewritten for V2. This session exercised native same-server movement and API lookup; cross-server transfer remains untested. |
| `ryan-blog` | Personal writing in coding or Hermes workflows | Host that can read the current blog checkout and relevant source notes; the blog's checker when available | Merged from two personal sources. Needs a real draft/edit comparison against Ryan's edits. |
| `browser-harness-cli` | Interactive Python/CDP browser work from coding or Hermes agents | Chosen browser host; Browser Harness, workers/wrappers, Chrome, and selected profile access | Source contracts compared. No browser execution test in this pass. |
| `wayland-app-icon-fix` | Desktop maintenance when a Linux app's runtime ID mismatches its launcher | The affected desktop user/session; desktop files, optional `kdotool`, KWin D-Bus tools | Byte-identical import from matching repository/chezmoi sources. Verify on an affected desktop. |

## Selection by role

- **Coding on Reef:** start with review and test coverage. Select design guidance
  deliberately, after aligning the retained brainstorming protocol with Ryan's
  preference for proportionate process.
- **Hermes:** select writing or browser guidance only where its profile has the
  relevant tools and project access. Hermes's own assistant skills stay distinct.
- **Desktop maintenance:** install Wayland guidance only for workflows that can
  reach the affected desktop session. Running a command on Reef does not inspect
  Marlin's compositor.
- **Session administration:** the migration skill is OpenCode-specific; ordinary
  Paseo client switching does not require a session migration.

These are selections, not a bundle installed everywhere. Codex, Claude, and
Gemini/Antigravity discovery and tool behavior remain separate verification tasks.

## IDs and compatibility

- `ryan-blog-style` is folded into `ryan-blog`; do not install both.
- Ryan's Python `browser-harness` instructions become `browser-harness-cli` here.
  OpenCode's built-in `browser-harness` remains a different implementation. When
  migrating existing custom copies, remove their old-ID override through their
  actual source manager after comparison. Installing the new ID alone does not
  remove that override.
- Jules and `toolhive-operator` are excluded. Historical mentions in provenance,
  the plan, and blog examples do not make them active capabilities.
- `agent/` and `command/` are retained adapters. V2 supports their legacy file
  formats; permission enforcement and command behavior need verification.
- `plugin/git-ai.ts` is V1-only implementation source. Do not infer V2 support
  from its presence or install it through the skill installer.

## Editing and installation

Edit the original engineering prompts in `prompts/`, then run `make sync` and
`make check`. Edit the four specialist skills directly in `skills/<id>/SKILL.md`.
Source ancestry and intentional adaptations belong in the provenance record.

Use the [explicit installer](../README.md#install) from a persistent checkout on
the execution host. Preserve full skill directories and supporting references.
For OpenCode, `~/.config/opencode/skills` and project `.opencode/skills` are
documented discovery paths. Confirm paths for the actual Codex, Claude,
Antigravity, or Hermes version/profile before choosing a destination.

Record runtime/client versions, toolkit revision, execution account/host, selected
IDs, discovery evidence, and a task result for each deployed selection. Symlink
creation alone is not proof of runtime discovery or useful behavior.
