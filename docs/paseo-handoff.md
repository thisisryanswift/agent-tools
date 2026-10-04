# Continue the Reef agent consolidation from Paseo

Handoff: **2026-10-04**, from the Marlin OpenCode session to a fresh OpenCode agent
running as `rswift` on Reef through Paseo. This is a working checkpoint, not a new
design exercise. Ryan wants to start using the setup while completing it.

## Start here

Use `/home/rswift/dev/personal/agent-tools` on Reef as the Paseo workspace. Read
this document and [consolidation status](consolidation-status.md); consult the
[approved plan](personal-agent-toolkit-plan.md) for wider context as needed.

**The next useful task is enabling CASS globally for Reef's OpenCode runtime and
verifying a real history search from both native OpenCode and a Paseo agent.**
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

- Reef's lingering `rswift` user service runs upstream Paseo **0.11.0-beta.2**,
  commit `b5b43edd65cc1253493b13cca3941dd390df6ef3`, from
  `/srv/dev/tools/paseo-next`, using Node **26.10.0**. The checkout is clean and
  intentionally pinned; a newer remote branch is not an instruction to upgrade.
- Active Paseo state/config/logs: `/home/rswift/.paseo`. Listener:
  `100.81.54.26:6767`. The old `paseo` account's service is stopped/disabled.
- Canonical OpenCode executable: `/home/linuxbrew/.linuxbrew/bin/opencode`,
  verified **2.0.21**. An OpenAI OAuth tool turn passed with
  `openai/gpt-6.1-sol`. The same model through OpenRouter failed with `User not found`.
- Desktop **0.11.0-beta.3** is installed on Marlin, Tortoise, and Reef. Ryan confirmed
  Marlin and Android work; Reef/Tortoise GUI checks await physical access.
- Paseo history opens in native OpenCode, and native continuation appears in
  Paseo after **Reload agent**. Ryan accepted this serialized handoff. Separate
  helper/background processes share persistent storage; live synchronization is
  not established or required for this milestone.
- Reef CASS **0.10.0** has indexed preserved session-only snapshots from Marlin
  `rswift`, Reef `rswift`, Reef legacy `opencode`, and Tortoise `rswift`. Source-
  filtered CLI and MCP searches passed, as did an MCP canonical-message view over
  SSH. Runtime MCP registrations and refresh/backup scheduling are still pending.

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

- Preserve/compare the **364 older JSON session IDs** outside all four V2 API
  inventories, investigate legacy-account JSON storage, and inspect Marlin's
  existing CASS archive without indexing over it. Check possible changed-ID copies.
- Arrange source refresh, collection, indexing, and routine backup coverage.
- Ask Ryan which histories need native import versus searchable archival. Do not
  merge or discard native stores automatically. A longer legacy session contains
  a real continuation; another legacy transcript replaces Marlin's embedded PDF
  with migration text, so neither store uniformly supersedes the other.
- Two HTTP-500 API histories have identical stored message arrays across Marlin
  and both Reef accounts (146 and 12 messages). Stored comparison is resolved;
  native API readability is not. Both are searchable in CASS.
- Finish native-origin import into Paseo, a Paseo tool turn after reverse handoff,
  permissions/interruption, and OpenCode attachment checks.
- Choose the replacement native remote-access path, update the chezmoi-managed
  `opencode-reef` launchers, then obtain authorization to retire legacy OpenCode.
  They still target the `opencode` account's listener on port 4096.
- Reconcile managed service/config sources and backups. Then continue dedicated
  Codex → Claude → Gemini/`agy`, toolkit deployment, and the wider approved roadmap.

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

- `agent-tools`: the published handoff documents describe the parallel toolkit
  workstream, but its implementation remains uncommitted on **Marlin**. Its tracked
  patch/untracked archive are in the private bundle. Source checks were previously
  green; deployment and behavioral verification remain open. Do not assume a clean
  Reef clone already contains the consolidated seven-skill toolkit.
- Marlin `~/dev/tools/paseo`: dirty, diverged `ryan/opencode-external-server`
  experiment. Preserved privately; it is not the deployed upstream backend and
  should not be revived just to achieve live synchronization.
- Reef `/srv/dev/homelab`: dirty branch with unrelated staged and unstaged work,
  including another version of the old runbook. Preserved in place. The clean
  handoff checkout is `/home/rswift/dev/homelab-coding-handoff`; its
  `runbooks/reef-coding-services-2026-10.md` is the current operational checkpoint.
- Reef has another `agent-tools` clone at `/srv/dev/personal/agent-tools`. Use the
  `/home/rswift/dev/personal/agent-tools` checkout above for this continuation.

## Operating boundaries

- **Never restart the main Paseo daemon on port 6767 without Ryan's permission.**
  It owns the running agents, including potentially this one. Timeouts alone do
  not justify a restart. Native imports, legacy shutdown, and global MCP changes
  were not performed before this handoff.
- Use existing credentials and HTTPS Git remotes; never print secrets or copy
  another account's authentication state. Keep databases/transcripts out of Git.
- Preserve other work. Avoid broad stashes, resets, cleans, or indiscriminate
  commits. Make scoped chezmoi source edits and apply only reviewed targets.
- Ryan performs privileged commands interactively. For a sudo session use
  `/usr/bin/ssh -t rswift@reef ...`; his `ssh` alias resolves to `tailscale ssh`,
  which rejects `-t`. If Tailscale needs approval, provide its raw approval URL.
- Inspect current host, runtime, worktree, and repository instructions. Verify
  proportionately; the Paseo repository forbids running its full local test suite.
