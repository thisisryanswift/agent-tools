# Consolidation status

Updated **2026-10-10**. This is the current snapshot of the Reef agent setup and
toolkit consolidation, tracked against the [approved plan](personal-agent-toolkit-plan.md).
Dated evidence from the October 1–4 backend rollout and session-history audit is in
[October 2026 checkpoints](checkpoints-2026-10.md). Resuming through Paseo on Reef?
Start with [the handoff](paseo-handoff.md).

## Where things stand

| Area | State |
| --- | --- |
| Paseo backend (Reef) | Upstream **0.11.0** from the npm package in `~/.local/share/paseo`, run as `rswift` (`paseo daemon run`), Node 26.10.0. Switched from the beta.2 source build on 2026-10-07; `~/dev/tools/paseo` is a development clone only. Upgrade steps are in the handoff. |
| Coding providers in Paseo | OpenCode 2.0.21 (`openai/gpt-6.1-sol` via OpenAI OAuth), Claude, and Codex (user-confirmed 2026-10-06), Antigravity/`agy` and Cursor (smoke-tested 2026-10-10). OpenCode Go, GLM, Copilot, and Devin are not yet covered. |
| Clients | Marlin, Tortoise, and Android user-confirmed against Reef. Desktop `0.11.0-beta.3` is installed on Marlin, Tortoise, and Reef; Reef's GUI check awaits physical access. |
| Native ↔ Paseo continuity | Works with manual **Reload agent** (accepted); live sync deferred. Native-origin import, permissions/interruption, and attachment checks are still open. |
| Session history (CASS) | Reef is the canonical archive (CASS 0.10.0). All four preserved snapshots are indexed and searchable over SSH and from native/Paseo OpenCode. Scheduled refresh, backups, and older-store coverage are open. Safe live remote-DB collection is **deferred by Ryan** (2026-10-04); no custom export pipeline. |
| Legacy accounts | **Retired 2026-10-10.** The `opencode` and `paseo` accounts, their services, the `:4096` server, and the `opencode-reef` launcher are gone. The history is archived in CASS. Ryan uses Paseo for coding; plain `opencode` on Reef shares Paseo's store. |
| Toolkit source | Seven skills, installer, checker/tests, catalog, and provenance in this checkout; `make check` and `make test` pass. **Uncommitted.** Consumer deployment and runtime verification are open. |
| Dev layout | `/srv/dev` retired 2026-10-10; all development lives under `/home/rswift/dev`. |
| Hermes | General assistant on **Lobster**. Reef keeps only the install for the `hermes desktop` client; no local runtime or sessions. |
| MLH Core Services | On-demand test environment in `~/dev/mlh/core-services`: `mlh-up` and `mlh-down` (Reef-only via chezmoi). See its `STACK.md`. |

## Next work

### Backend closeout

1. **CASS operations.** Validate direct native Reef collection and CASS's built-in
   scheduler, then arrange routine backups. Ryan wants no custom export-refresh
   integration, and no upstream issue will be published while that follow-up is
   deferred.
2. **OpenCode checks in Paseo.** Permissions/interruption and an OpenCode
   attachment. Native-origin import matters only for sessions started with plain
   `opencode` on Reef.
3. **Reef GUI check** when physically at Reef. Automatic native ↔ Paseo sync and
   remote-desktop setup are deferred by Ryan.
4. **Mastra Factory** (`factory` account, `~/dev/tools/reef-factory` (private repo `thisisryanswift/reef-factory`)). It stays
   isolated under its own account because it runs autonomous agents with GitHub
   access and the Podman socket. On 2026-10-10 its Caddy routes, which a Caddy
   deploy had dropped (they had been appended outside chezmoi), moved into the chezmoi
   Caddyfile; its docs, scripts, and tests now use `~/dev`. **Deferred by Ryan
   (2026-10-15):** how `factory` builds and upgrades now that it can't read
   `/home/rswift`. Recommendation: have `factory` build from its own clone of the
   new `reef-factory` repository (extracted from homelab on 2026-10-15).
   Also open: backup health, newer Factory releases, and choosing a first real
   project (`agent-tools` suggested). Other lingering accounts: `toolhive`, `wharfi` (Caddy).
5. **Service configuration and backups.** Reconcile managed service/config sources
   and routine backup coverage for Paseo uploads and service configuration. The
   October runbook in `~/dev/homelab` records current state. Reef's nightly restic
   backup was repointed at the rswift layout on 2026-10-18, after failing
   2026-10-11 to 10-17; it now covers `~/dev`, `~/.paseo`, OpenCode data, and the
   CASS source exports.

### Toolkit

1. Inventory skill discovery for the Reef execution account and the runtimes in
   use (OpenCode, Claude, Codex, Antigravity, Cursor), plus the Hermes profiles on
   Lobster. Migrate only chosen consumers to this checkout's canonical sources.
2. Make the retained `brainstorming` skill optional and proportionate before
   installing it. It still has an automatic trigger and unconditional
   design/commit steps from the old toolkit.
3. Verify the browser package/wrapper, profile reuse, worker cleanup, workspace
   access, and OpenCode V2 setup on the actual browser host.
4. Port the selected evaluation cases and exercise real skills.
5. Commit this checkout's source and documentation changes (pending Ryan).

## Completed

### Toolkit source (2026-10-06)

- Seven skills: `agent-session-migration`, `brainstorming`, `browser-harness-cli`,
  `code-review`, `ryan-blog`, `test-coverage`, `wayland-app-icon-fix`; catalog in
  [skill-catalog.md](skill-catalog.md), provenance in
  [source-provenance.md](source-provenance.md).
- `ryan-blog` combines the blogging sources; the Wayland skill is a byte-identical
  import; the V1 session-database recipe is replaced with V2 session tools/API
  guidance; `browser-harness-cli` consolidates the personal browser instructions.
- Jules retired; ToolHive excluded. Blanket adapter/plugin installation replaced
  with an explicit skill-link installer that preflights selections and preserves
  existing content.
- Reconciled Marlin's uncommitted implementation into this checkout on 10-06; the
  pre-sync files are kept privately in `~/.cache/agent-tools-marlin-sync-c1xy_1hp/`.
- Checks: `make check` (7 skills, 3 prompt copies), `make test` (4 installer tests:
  preserved user content, dangling links, dry-run/invalid selections, complete
  references, idempotence), `make install` dry-run, `git diff --check`. Provider
  skill discovery, browser behavior, and cross-server export/import were not
  exercised.
- 2026-10-10: dropped the old clone (`~/dev/tools/agent-tools`) and its unpushed
  September "review assets" commit `5c95316`; this checkout is canonical.

### Backend and clients (2026-10-01 to 10-10)

- Paseo migrated to `rswift`, then upgraded to npm 0.11.0. Details and the upgrade
  procedure are in the [handoff](paseo-handoff.md#what-already-works).
- User-global CASS MCP for Reef's OpenCode, verified natively and through Paseo
  (2026-10-04).
- Antigravity: `agy` 1.3.0 signed in. After sign-in, Paseo needed
  `paseo provider diagnostic antigravity` to refresh its cached status. Full access
  only.
- Cursor: `cursor-agent` installed with the official Linux installer and signed in
  (Ryan's work account); added as an ACP provider in `~/.paseo/config.json` and
  applied with `paseo reload`.

### Retire `/srv/dev` (2026-10-09 to 10-10)

- Audited 127 checkouts (41 GB) against `~/dev`, deleted 51 verified duplicates,
  moved 35 projects, and replaced 11 stale `~/dev` copies with newer ones, keeping
  the newest copy throughout. Legacy-account and Hermes experiments were dropped.
  Ryan then removed `/srv/dev`. Audit, merge script, and config originals:
  `~/.local/share/srv-dev-retirement/`.
- Repointed Hermes and Codex configs; restored SELinux labels on moved files; and
  removed a stray global lefthook `pre-commit` hook created by the old `paseo-next`
  install. A final search found no `/srv/dev` references except the
  `opencode-reef` launcher hint.

### Legacy session history (2026-10-10)

- **Decision: archive, don't import.** CASS (the `reef-opencode` source from the
  Oct 4 snapshot) is the record of the legacy account's history. About 1,075 of
  its 1,616 sessions are exact duplicates of Marlin's, and the rest are searchable
  and readable through CASS. A full native backup remains in
  `/home/opencode/.local/share/cass-source-snapshots/20261004/` until the account
  is retired. (Removed with the account on 2026-10-10.)
- **Verified complete.** A read-only check of the live legacy store as `opencode`
  found the same 1,616 sessions and none updated after the snapshot. Its 364 V1
  JSON session IDs are identical to Reef `rswift`'s, which CASS indexes.
- **Closed as not needed:** the two HTTP-500 API histories (present in CASS),
  possible changed-ID copies, and verifying Marlin's old CASS archive.

### Legacy account retirement (2026-10-10)

- Ryan's direction: stop using `opencode-reef` and use Paseo for coding.
- Removed `opencode-reef` from chezmoi (source, test, and docs) and added it to
  `.chezmoiremove`, so `chezmoi apply` deletes it on every host. Ryan ran `chezmoi update`
  on Tortoise and Marlin on 2026-10-15; checks over SSH from Reef confirmed both
  are at `2bf5654` with `opencode-reef` gone and no pending changes. Removed the
  `opencode.reef.wharfi.sh` Caddy site and deployed it with `apply-reef-caddy`.
- Removed `machine`'s Reef section, which deployed legacy OpenCode builds and
  restarted the old `paseo` service; Homebrew keeps updating `rswift`'s OpenCode.
  Updated the chezmoi tests, including expecting the Oct 4 `cass` MCP server on
  Reef. The full suite passes.
- A read-only inventory found nothing to rescue: `~/homelab` was clean and pushed;
  the rest was OpenCode data, backups, caches, and credentials for the retired
  services. A disabled `admiral-reef-executor.service` (Lobster's Admiral bot)
  existed under `opencode`; if Admiral needs to run on Reef, set it up under
  `rswift`.
- Ryan disabled lingering for both accounts, stopped the remaining process,
  removed `/etc/sudoers.d/opencode-reef-credential`, the `opencode-reef-credential`
  and `opencode-reef-host-attach` helpers, and `/usr/local/libexec/opencode`, and
  deleted both accounts with their homes. He also removed `/srv/paseo` and the
  three Jul/Aug `/srv/dev` snapshots. Disk use went from 663 GB to 517 GB. Paseo
  stayed healthy throughout.
- Ryan then removed `/srv/migration`, the finished July–August Marlin→Reef cutover
  workspace (`du` reported 545 GB of reflinked validation runs). Disk use dropped
  from 517 GB to **220 GB**. `/srv` now holds only `factory`.

### Reef Hermes and service cleanup (2026-10-09 to 10-10)

- Removed `hermes-serve` and `hermes-gateway` (no platforms or cron jobs) and the
  15 local Hermes sessions; kept the install for `hermes desktop`.
- Removed the finished Zoho export pilot: container, image, volume, Quadlet, hook,
  `~/.hermes/migration/`, and its dashboard credentials.
- Cleared stale transient `reef-*-trial` demo units.

### MLH Core Services (2026-10-10)

- Rebuilt as `rswift` systemd user units on default branches (DEV-3974 had landed
  upstream), with fresh PostgreSQL 17 and Redis. It runs on demand via
  `mlh-up`/`mlh-down`, becomes healthy in about 20 seconds, and uses about 6 GB of
  RAM. The hardened system-user design in `~/.config/homelab/reef/core-services`
  was not deployed.
- Remaining manual steps for Ryan: create the Strapi administrator and publish a
  Home Page.
