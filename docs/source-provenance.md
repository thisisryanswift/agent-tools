# Source provenance and consolidation decisions

Inspected 2026-10-01. This is a file import/adaptation with exact source revisions;
Git histories have not been merged. Original repositories and the browser stash
remain available during consumer migration.

## Source snapshots

| Source | Revision | Ownership / license evidence |
| --- | --- | --- |
| `thisisryanswift/agent-tools` | `b403a63ed35d6cb3ed96116be330e1ab1775e3a7` | Existing Ryan toolkit; README says MIT. No tracked root license file in this snapshot. Brainstorming already credits `obra/superpowers` (MIT). |
| `thisisryanswift/skills` (`~/dev/skills`) | `21fff3b48f44a663712f7c9c3a23213dc0aed9a9` | Ryan's personal skills; no tracked license file or README license declaration observed. Imported for this authorized personal consolidation. |
| Chezmoi source (`~/.local/share/chezmoi`) | `7552c3fc03a1bb4c2a7dd5501048b5e0abf1115a` | Ryan's personal source; clean when inspected, no tracked license file observed. Selected instruction prose, not configuration or authentication state. |
| `browser-use/browser-harness` (`~/dev/tools/browser-harness`) | `f5f3ad98878910b1558c09c49d6bd74aa003df29` | MIT, copyright 2026 Browser Use; implementation remains upstream. |
| Browser Harness stash | `f6c0fd012c6e5848939cdd365e2fc1a4d0aabc0d` | Ryan's July 28 local customization, `pre-v0.1.8 local browser profile customization`; inspected without applying it. |
| `thisisryanswift/browser-harness-workers` | `50236e17982ef787049e8ee2008ffe9216e765db` | MIT, copyright 2026 Ryan Swift; independently maintained package. Existing uncommitted dependency bump in `pyproject.toml` is separate work. |

No upstream package implementation is vendored here. Existing attribution stays
with the engineering prompts; the browser skill describes integration behavior.

## Imported skill sources

Hashes identify the input bytes before adaptation, not the resulting files.

| Source path (relative to the repository above) | SHA-256 | Decision |
| --- | --- | --- |
| `skills`: `agent-session-migration/SKILL.md` | `d4d917886ba084bd5aa7315ce6af2ce9d88abb876bb4102c21ce6cbd11bd0339` | Rewrite for V2 session tools/API. Drop the direct SQLite editing recipe; retain separate same-server move and cross-server transfer concepts. |
| `skills`: `ryan-blog-style/SKILL.md` | `a7ff3c6849c1078b9b1149097ec8c09ce75420d4889ff3a50964319daec179a5` | Merge its voice, editing, and session-to-story guidance into `ryan-blog`. |
| `chezmoi`: `dot_agents/skills/ryan-blog/SKILL.md` | `9b93c416fae39b22fe9a3662931db79ce630ce027ff75c4548073850ef9c9699` | Main blogging source: preserve current edited posts as authority and remove the dependency on a separately installed older skill. Adapt paths for the execution host. |
| `skills`: `wayland-app-icon-fix/SKILL.md` | `202e127d495bfc252150592cf0785dadd4530a704fa57d084a2ee24210762047` | Import byte-for-byte. Chezmoi's `dot_agents/skills/wayland-app-icon-fix/SKILL.md` has the same hash. |
| `chezmoi`: `dot_agents/skills/browser-harness/private_SKILL.md` | `b786ae56f778e302dbf29b500356f42cb6643ab471f544d2a63a0f1a3efcf68d` | Adapt as `browser-harness-cli`, preserving isolated profiles, worker ownership, tab hygiene, and shared learning; distinguish package and older wrapper workspace paths. |

The V2 migration rewrite uses the documented API contract and observed CLI help:

- https://opencode.ai/v2/docs/api
- https://opencode.ai/v2/docs/cli
- https://opencode.ai/v2/docs/migrate-v1
- https://opencode.ai/v2/docs/skills

## Browser reconciliation

| Material | Disposition |
| --- | --- |
| Stash's `browser-use-isolated`, fixed port 9333, single shared profile, and renamed CLI advice | Historical. Current named-profile/worker guidance supersedes those machine-specific instructions. |
| Stash's heredoc usage, main-profile opt-in, and avoiding abandoned tabs | Retained through the newer personal skill. Use one task-owned tab and reuse it across commands. |
| Stash's `close_tab` implementation | Superseded by current upstream `src/browser_harness/helpers.py`, which already provides `close_tab(target=None)` through `_target_id`. No duplicate helper imported. |
| Chezmoi `executable_browser-harness-{isolated,worker}` | Existing implementations remain migration sources. The package README describes compatible profile paths and a self-test/reuse procedure; runtime cutover is still pending. |
| Package workspace configuration | `BH_AGENT_WORKSPACE`/XDG paths and optional chezmoi source path are documented in the consolidated skill. Package setup instructions referencing OpenCode 1.18.11 need V2 verification before use. |
| Chezmoi workspace `agent_helpers.py` | Only a five-line placeholder docstring at inspection; no reusable helper implementation to import. |
| Chezmoi workspace `domain-skills/` | Only its seven-line README at inspection. Its learning policy is retained in the skill; no site knowledge files were present to import. |

Browser runtime code stays in its package repositories. Mutable site knowledge
stays in the configured browser workspace until useful reviewed content exists to
promote; it is separate from cookies, profiles, and installed skill instructions.

## Retired and retained material

- Removed `agent-tools`' Jules prompt, skill, copied reference, sync entry, and
  installation guidance. Excluded the older repository's Jules skill.
- Excluded `toolhive-operator` and replaced distribution guidance with explicit
  execution-host skill selection. The old `skills` README is historical source,
  not the current installation procedure.
- Kept the untracked Compound plugin directories out of the import.
- Kept the V1 git-ai plugin as source for later comparison with Entire, without
  installing it. Retained agent/command adapters for explicit runtime validation.
- Recorded the existing V1 evaluations in [the migration map](../evals/README.md)
  rather than copying a pinned launcher and calling it a V2 suite.

The source copies in chezmoi and the older skill repository are preserved migration
inputs. Active consumers still need a scoped cutover before those copies can be
retired or their repositories archived.
