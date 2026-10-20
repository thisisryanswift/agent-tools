# Continue the Reef agent consolidation from Paseo

Handoff started **2026-10-04**, from the Marlin OpenCode session to agents running
as `rswift` on Reef through Paseo; last updated **2026-10-20**. This is a working
checkpoint, not a new design exercise. Ryan is using the setup while completing it.
The current snapshot and open work are in [consolidation status](consolidation-status.md);
dated evidence is in [October 2026 checkpoints](checkpoints-2026-10.md).

## Start here

Use `/home/rswift/dev/personal/agent-tools` on Reef as the Paseo workspace. Read
this document and [consolidation status](consolidation-status.md); consult the
[approved plan](personal-agent-toolkit-plan.md) for wider context as needed.

**Next useful work: the toolkit workstream** (skill discovery inventory, the
`brainstorming` trigger, deployment, Browser Harness verification), then the
remaining OpenCode-in-Paseo checks. CASS scheduling and Reef backups were done on
2026-10-18. The legacy `opencode`/`paseo` accounts and `opencode-reef` were
retired on 2026-10-10; Paseo is the coding interface. The upstream follow-up about safe
live remote OpenCode collection is **deferred by Ryan (2026-10-04)**. Ryan wants
no maintained custom integrations; do not schedule the migration export helper.
CASS is now available globally to Reef's OpenCode runtime, with real searches and
canonical message reads verified from native OpenCode and this running Paseo agent.
Ryan accepted agent-wide access: the same Reef archive should serve OpenCode,
dedicated Codex, Claude, and later Gemini/other runtimes. Start with OpenCode;
configure the others as their runtime rollout proceeds. A model switch inside
OpenCode does not require another MCP registration. Desktop/phone clients that
only control Reef need no separate CASS configuration. Agents actually executing
elsewhere can reach the same archive over SSH.

Take the work one useful step at a time. Explain meaningful findings briefly and
ask for the next human decision or privileged command when needed. Avoid a new
orchestration framework, a maintained Paseo fork, or another full migration plan.

## What already works

- Reef's lingering `rswift` user service runs upstream Paseo **0.11.0** from the
  published npm package `@getpaseo/cli`, installed under `~/.local/share/paseo`
  and started as `paseo daemon run --home ~/.paseo` with Node **26.10.0**.
  Switched from the beta.2 source build in `/srv/dev/tools/paseo-next` on
  2026-10-07. Claude, Codex, and OpenCode were available afterwards.
  `~/dev/tools/paseo` is Ryan's development clone; the service never runs from it.
- Upgrades follow the npm `beta` tag, which also receives stable releases. Ryan's
  `~/.npmrc` sets `min-release-age=7`; override it per deliberate upgrade only:
  `npm install -g --prefix ~/.local/share/paseo --min-release-age=0 @getpaseo/cli@beta`,
  then `systemctl --user restart paseo` from a shell outside Paseo. npm's blocked
  install scripts (esbuild, node-pty, msgpackr-extract) are not needed on Reef;
  bundled binaries work. Ops scripts and unit copies: `~/.local/share/paseo/ops/`.
- Active Paseo state/config/logs: `/home/rswift/.paseo`. Listener:
  `100.81.54.26:6767`. The old `paseo` account's service is stopped/disabled.
- Canonical OpenCode executable: `/home/linuxbrew/.linuxbrew/bin/opencode`,
  verified **2.0.21**. An OpenAI OAuth tool turn passed with
  `openai/gpt-6.1-sol`. The same model through OpenRouter failed with `User not found`.
- Desktop **0.11.0-beta.3** is installed on Marlin, Tortoise, and Reef. Ryan confirmed
  Marlin and Android work, and confirmed Tortoise during normal Paseo use on
  October 6. Reef's GUI check awaits physical access.
- Paseo history opens in native OpenCode, and native continuation appears in
  Paseo after **Reload agent**. Ryan accepted this serialized handoff. Separate
  helper/background processes share persistent storage; live synchronization is
  not established or required for this milestone.
- Direct Codex and Claude connections: Ryan confirmed both working on October 6.
  Antigravity/`agy`: signed in and smoke-tested through Paseo on October 10. After
  signing in, Paseo kept its cached "unavailable" status until
  `paseo provider diagnostic antigravity` forced a re-check. Antigravity runs in
  Full access only (`--dangerously-skip-permissions`).
- Cursor: `cursor-agent` installed and signed in; added to `~/.paseo/config.json` as
  an ACP provider and applied with `paseo reload`. Smoke-tested on October 10.
- Reef CASS **0.10.0** has indexed preserved session-only snapshots from Marlin
  `rswift`, Reef `rswift`, Reef legacy `opencode`, and Tortoise `rswift`. Source-
  filtered CLI and MCP searches passed, as did an MCP canonical-message view over
  SSH. Reef's OpenCode global registration now works natively and through Paseo;
  other runtime registrations and refresh/backup scheduling are still pending.

## CASS access and operating facts

Archive: `/home/rswift/.local/share/coding-agent-search/` on Reef. The verified
local MCP launch is:

```sh
/home/linuxbrew/.linuxbrew/bin/cass serve --stdio --mcp \
  --data-dir /home/rswift/.local/share/coding-agent-search \
  --db /home/rswift/.local/share/coding-agent-search/agent_search.db
```

It exposes search, bounded canonical view, status, reload, and unload tools. Reads
do not ingest or repair the archive. A reader pins its lexical index until
`cass_reload` or reconnection. CASS's documented persistent transport is stdio,
not an HTTP endpoint; remote consumers launch this command through SSH.

Deployed Paseo offers per-agent `mcpServers` and its own tool injection, not a
daemon-global third-party MCP registry for every provider. Configure the native
runtime's user-level registration through its existing source manager and verify
Paseo inheritance. OpenCode's global config is chezmoi-managed; use its source
template and a scoped apply. Read the V2 MCP/config docs before editing; do not
guess V2 syntax or use the published V1 schema to infer it.

### Runtime access checkpoint — 2026-10-04

- Added `mcp.servers.cass` to the Reef-only branch of
  `~/.local/share/chezmoi/dot_config/opencode/opencode.json.tmpl`, using the exact
  local command above. Applied only `~/.config/opencode/opencode.json`; unrelated
  model/provider/Gbrain settings and other hosts' rendering are unchanged.
- The running Paseo agent picked up the six CASS tools at a tool boundary. It
  searched all four named sources and read the canonical first user message from
  **Paseo Desktop setup for rswift** (`reef-rswift`, conversation `1508`, message
  `1`, native ID `ses_00cd5f527ffeteXXabrqVaQE4w`). Status confirmed five completed
  queries, one canonical read, one retained lexical reader, and no maintenance.
- A separate native `opencode run` using `openai/gpt-6.1-sol` independently called
  CASS MCP search/view for the same 152-byte user message. Native `opencode mcp
  list` reports CASS connected. Neither OpenCode nor Paseo needed a restart or
  explicit location reload; legacy services were untouched.
- Private proof is under
  `/home/rswift/.local/share/agent-migration/2026-10-04-cass-runtime-access/`:
  `paseo-tool-proof.json`, `native-run.jsonl`, `native-run-metadata.json`, and
  `manifest.json`. Paseo session: `ses_ef79730e0ffeDU1RsTLw0q4vNn`; native smoke
  session: `ses_ef7909836ffeDK7s111SDkb8oB`. These are access checks against the
  existing frozen exports, not new ingestion or proof of archive freshness.

### Native-only collection direction — 2026-10-04

Ryan clarified that ongoing collection should use CASS natively, without a
custom export-refresh integration. He expects to continue local development on
other machines, so automatic multi-host collection is a requirement, not merely
an optional legacy-import feature; a Reef-only solution is insufficient.
CASS 0.10's OpenCode connector directly opens
the native store read-only and supports V2 `session_v2`/`session_message` tables;
the earlier bootstrap ingest already found Reef's live local histories. Its
`schedule` commands provide incremental/nightly OS timers. Validate current live
ingestion in an isolated archive before changing canonical sources or timers.
Preserved session-only exports remain migration evidence, not a proposed ongoing
export pipeline; do not remove or replace them.

Native SSH sync copies configured files via rsync/scp/SFTP; inspected 0.10 source
does not make coherent session-only snapshots before transfer. Therefore safe
automatic collection of active remote OpenCode databases is not established.
Do not silently copy credential-bearing databases or introduce a custom wrapper
to bridge that gap. Keep remote/legacy history preserved while deciding whether
native upstream support or an explicitly accepted operating constraint is needed.
An October 4 upstream check still finds `v0.10.0` as the latest stable release;
no newer released native snapshot transport was identified. An upstream support
question/feature request is preferable to maintaining local glue, but Ryan asked
to **defer that upstream follow-up on October 4**. Do not publish an issue or
install a custom workaround. Multi-host collection remains a requirement, not
a completed capability; existing remote snapshots remain searchable and automatic
live remote refresh is still undeployed. Local validation and other consolidation
work can proceed independently.
Routine off-Reef backup coverage is still separate; CASS also has native logical
`archive export`/`verify` commands, but its refresh timers are not off-host backups.

Sources config: `~/.config/cass/sources.toml` on Reef, presently unmanaged by
chezmoi. Names: `reef-rswift`, `reef-opencode`, `marlin-rswift`, `tortoise-rswift`.
Only OpenCode is enabled for ingestion so far. Other providers need collection
work as well as MCP access.

Important implementation findings:

1. **Do not open the live CASS archive with stock SQLite, even read-only.** CASS
   0.10.0 has upstream [#509](https://github.com/Dicklesworthstone/coding_agent_session_search/issues/509):
   a stock read can rewrite an empty WAL index and block subsequent writes with
   `BusyRecovery`. We encountered it and used the maintainer's idle, backed-up
   `-shm` move-aside workaround. Use copies of the complete idle database family
   for stock-SQLite inspection. The snapshots used as OpenCode ingest inputs are
   separate files, not the live CASS archive.
2. Explicit local source paths do not suppress OpenCode default discovery. The
   verified index command scopes `HOME` and all three XDG directories under
   `~/.local/share/cass-index-home`, with `.config/cass` linked to the real config,
   and supplies the real archive through `--data-dir`. SSH sync uses the real home.
   Preserve this separation when implementing scheduled jobs.
3. Existing CASS units/timers are disabled and still reference `%h/.local/bin/cass`.
   The actual executable is `/home/linuxbrew/.linuxbrew/bin/cass`. Their sources
   are chezmoi-managed. Refresh the coherent source exports before syncing/indexing;
   running `sources sync` alone just recopies the current frozen exports.

## History and remaining migration work

The earlier four-store API audit found 2,445 distinct IDs. It is a dated inventory,
not a live total. Marlin added two sessions before its SQLite snapshot.

The four named CASS sources contain **3,840 searchable source-attributed
conversations**. The archive also retains **940 bootstrap rows**: 577 duplicate
current-Reef DB copies and 363 older JSON histories. Totals are 4,780 conversation
rows, 233,403 messages, and 2,734 distinct native IDs. Empty sessions/empty
assistant messages explain the verified gaps against the four snapshot counts.

Remaining closeout, after making CASS useful in the daily workflow:

- **Resolved 2026-10-10:** the legacy history is archived in CASS (no native import).
  The 364 older JSON session IDs match Reef `rswift`'s; the live legacy store had
  no changes since the Oct 4 snapshot. The HTTP-500 histories, changed-ID copies,
  and Marlin's old CASS archive were closed as not needed. The legacy accounts and
  `opencode-reef` are retired. See [consolidation status](consolidation-status.md).
- Arrange source refresh, collection, indexing, and routine backup coverage.
- Finish Paseo permissions/interruption and OpenCode attachment checks.
- Reconcile managed service/config sources and backups. Then continue with
  toolkit deployment (Codex, Claude, Antigravity, and Cursor all work), and the wider approved roadmap.

## Durable evidence and unfinished source work

The private handoff bundle is available on **both Marlin and Reef** at:

```text
/home/rswift/.local/share/agent-migration/2026-10-04-paseo-handoff/
  manifest.json
  audit/                   # inventories, fingerprints, comparisons, MCP proof
  helpers/                 # collectors and the tested snapshot helper
  working-tree-recovery/   # original commit IDs, tracked patches, untracked archives
```

The manifest records SHA-256 and size per file. These artifacts are private,
outside Git. The original `/tmp/opencode/session-drift-20261004/` paths are
historical convenience copies, not the only handoff evidence.

Full native backups remain inside their owning account's
`~/.local/share/cass-source-snapshots/`; the legacy backup is under
`/home/opencode/.local/share/cass-source-snapshots/20261004/`. Session-only exports
are under `~/.local/share/cass-source-exports/`. They contain exactly the five
history tables, not credential/account tables, and are **not native restore DBs**.
Marlin/Tortoise exports were mirrored to Reef with verified matching SHA-256.

Additional Reef evidence and CASS database-family copies are retained under
`/home/rswift/.cache/paseo-upgrade/`. Paseo recovery locations include
`/home/paseo/.paseo`, `/home/rswift/.paseo.before-rswift-20261001-191357`,
`/var/backups/paseo-rswift-20261001-190854/state.tar.gz`, and `/srv/paseo/uploads`.
These are migration recovery assets; routine backup coverage still needs review.

Repository/worktree cautions:

- `agent-tools`: the published handoff commit contains only migration documents.
  On October 6, Marlin's live uncommitted toolkit work was reconciled into this
  Reef checkout, preserving the newer Reef docs. The seven-skill implementation
  was committed and pushed as `3ad2946` on 2026-10-15; Marlin picks it up with a
  pull. Reef's structural/installer checks pass; deployment and behavioral
  verification remain open. The original private recovery bundle remains available, and the status
  document records the fresh source snapshot and pre-sync Reef recovery files.
- Marlin `~/dev/tools/paseo`: dirty, diverged `ryan/opencode-external-server`
  experiment. Preserved privately; it is not the deployed upstream backend and
  should not be revived just to achieve live synchronization.
- Reef has one `homelab` checkout, `~/dev/homelab`, on `main` (HTTPS). Its
  `runbooks/reef-coding-services-2026-10.md` is the operational checkpoint. On
  2026-10-18 it replaced the old dirty `ryan/reef-coding-client` checkout, after
  that checkout's Beluga and Hermes media work was moved onto `main`.
- `/srv/dev` was retired on 2026-10-10; all development lives under `/home/rswift/dev`.
  Use the `/home/rswift/dev/personal/agent-tools` checkout for this continuation.
- As of 2026-10-20, `agent-tools`, chezmoi, and `homelab` on Reef are clean and in
  sync with `origin/main`.

## Operating boundaries

- **Never restart the main Paseo daemon on port 6767 without Ryan's permission.**
  It owns the running agents, including potentially this one. Timeouts alone do
  not justify a restart. Native imports and legacy shutdown remain unperformed;
  only the CASS global registration described above has since been applied.
- Use existing credentials and HTTPS Git remotes; never print secrets or copy
  another account's authentication state. Keep databases/transcripts out of Git.
- Preserve other work. Avoid broad stashes, resets, cleans, or indiscriminate
  commits. Make scoped chezmoi source edits and apply only reviewed targets.
- Ryan performs privileged commands interactively. For a sudo session use
  `/usr/bin/ssh -t rswift@reef ...`; his `ssh` alias resolves to `tailscale ssh`,
  which rejects `-t`. If Tailscale needs approval, provide its raw approval URL.
- Inspect current host, runtime, worktree, and repository instructions. Verify
  proportionately; the Paseo repository forbids running its full local test suite.
