# October 2026 backend and session-history checkpoints

Dated evidence from the Paseo/OpenCode backend rollout and the session-drift/CASS
audit, moved verbatim out of [consolidation status](consolidation-status.md) on
2026-10-10. The current state and open work are in that document; this file is the
historical record behind it.

## Backend rollout checkpoint — 2026-10-01 to 10-03

The backend session reports upstream Paseo `0.11.0-beta.2` running under `rswift`
on Reef with OpenCode `2.0.21`, plus the upstream `0.11.0-beta.3` desktop package on
Marlin, Tortoise, and Reef. Package/launcher checks passed on Tortoise and Reef;
Ryan initially deferred their GUI connection checks until physical access. On
October 6, Ryan confirmed Tortoise works as expected while using Paseo there;
Reef's GUI check remains deferred. Marlin and Android are also user-confirmed
working against Reef. OpenCode tool use
passed with `openai/gpt-6.1-sol` through OpenAI OAuth. The same model's OpenRouter
route returned `User not found`.

Paseo-created session history opened correctly in native OpenCode, and native
continuation became visible in Paseo after **Reload agent**. Automatic updates
and reopening the tab did not refresh it. Ryan accepted manual reload for the
initial setup on 2026-10-02; live synchronization is deferred. Fresh native-origin
import/continuation, remaining client checks, and legacy OpenCode history/service
retirement remain pending. See the approved plan's 2026-10-02 checkpoint for the
full evidence and limitations.

On 2026-10-03 Ryan paused imports and legacy retirement for a session-drift audit
across Marlin, Reef's `rswift`, Reef's legacy `opencode` account, and Tortoise.
Some history was previously imported from Marlin to Reef; overlap and divergence
must be established before choosing import versus archival. The audit is in
progress; no history merge or legacy OpenCode shutdown has been performed. The old
`paseo` service was stopped/disabled during the completed account migration.

Initial audit evidence from 2026-10-03:

- Marlin: 1,504 sessions (642 roots, 862 children), with one active session at
  capture and no duplicate IDs during pagination. Manifest:
  `/tmp/opencode/session-drift-20261003/marlin.json` on Marlin.
- Legacy Reef: two V2 `2.0.18` servers, both idle at inspection, with matching
  recent history and a roughly 12 GiB database. The service and its keyring remain
  enabled. The stale `active` binary symlink points to V1 `1.18.30`, but neither
  observed running server used it.
- The three newest sampled legacy IDs are absent from Reef `rswift`; none of the
  eight recent legacy sample IDs appeared on Marlin. This is sample non-overlap,
   not a complete drift result. The subsequent fingerprint results follow below.
- Marlin/Reef `opencode-reef` launchers still target the legacy listener. Their
  chezmoi source is `dot_local/bin/executable_opencode-reef`; apply scoped source
  changes when the replacement native-access path has been selected.

## Session audit and CASS assessment — 2026-10-04

- Refreshed Marlin's native API metadata inventory: **1,505 sessions** (643 roots,
  862 children), one active session, no repeated IDs during pagination. Compared
  with October 3: one additional session, no missing IDs, and one existing session
  with changed metadata. New manifest:
  `/tmp/opencode/session-drift-20261004/marlin.json`; the older capture is retained.
- CASS is installed through Homebrew at `0.8.0`. Its existing
  `~/.config/cass/sources.toml` configures Tortoise over SSH, including OpenCode's
  data directory. The last saved sync attempt in the current data directory is
  March 22 and failed remote-home resolution, transferring zero files. The older
  `~/.local/share/cass` state also records an unsuccessful attempt.
- [CASS 0.10.0](https://github.com/Dicklesworthstone/coding_agent_session_search/releases/tag/v0.10.0),
  released October 2, adds OpenCode 2.x `session_v2`/`session_message` indexing and
  SQLite WAL-only change detection. The installed `0.8.0` connector predates V2
  transcript support. This makes the current release a candidate for searchable
  multi-machine history after upgrade and validation.
- CASS remote sources pull histories over SSH/rsync into a local search archive
  with source attribution. The V2 connector renders searchable text, reasoning,
  tool-result text, and completed compaction summaries, while omitting other
  fields/events. Use native API transcripts for exact equivalence, extension, and
  divergence decisions; CASS can help locate related or re-keyed conversations.
- `cass stats --json --by-source` failed to open the existing archive read-only
  at `~/.local/share/coding-agent-search/agent_search.db`. The cause is unconfirmed.
  Preserve the archive and investigate upgrade/recovery before indexing into it.
  No CASS upgrade, repair, source change, or sync was performed in this assessment.
- Ryan renewed Reef/Tortoise Tailscale access and ran the legacy metadata and
  transcript collectors with sudo. Those collections are now available below.

## Four-store comparison — 2026-10-04

All counts include child/subagent sessions. The union contains **2,445 distinct
session IDs** across 4,057 stored session records. A unique ID means absent from
the other current API inventories; it does not by itself prove unique content.

| Store | Sessions | Roots | IDs only in this store | Roots only in this store |
| --- | ---: | ---: | ---: | ---: |
| Marlin `rswift` | 1,505 | 643 | 426 | 66 |
| Reef `rswift` | 648 | 394 | 116 | 23 |
| Reef legacy `opencode` | 1,616 | 686 | 537 | 109 |
| Tortoise `rswift` | 288 | 188 | 287 | 187 |

Marlin, Reef `rswift`, and Tortoise report OpenCode `2.0.21`; legacy Reef reports
`2.0.18`. No repeated IDs appeared during metadata pagination. Only Marlin had an
active session at the inventory boundaries. Fingerprinted sessions had unchanged
metadata and were inactive at the observed boundaries; these are sequential API
observations, not an atomic database snapshot.

| Copies compared | Shared IDs | Transcript result |
| --- | ---: | --- |
| Marlin ↔ legacy Reef | 1,079 | 1,075 exact matches; one legacy continuation; one changed assistant message; two API failures. |
| Marlin ↔ current Reef | 532 | 527 exact matches; three older current-Reef copies; the same two API failures. |
| Current Reef ↔ legacy Reef | 532 | 527 exact matches; legacy has the fuller versions of the same three histories; the same two API failures. |
| Tortoise ↔ Marlin/legacy Reef | 1 | Tortoise has an older copy; Marlin and legacy Reef match each other. |
| Tortoise ↔ current Reef | 0 | No shared IDs. |

Exact matches mean the full projected message arrays have identical canonical
JSON hashes in API order. Session locations can still differ: all 1,079 shared
Marlin/legacy-Reef IDs have different workspace locations. Comparisons also
retain per-message IDs, types, strict hashes, and candidate hashes omitting outer
ID/time/metadata. System-message differences are recorded rather than treated as
proof of independent user conversation branches.

Exceptions and follow-up:

- `ses_03c38aa28ffeHCWLx7756IXZgX`: legacy Reef has 1,114 messages versus Marlin's
  451, including 103 additional user messages. The earlier non-system messages
  match; legacy Reef contains the continuation.
- `ses_0b64dd0cfffepjkJODhOpGFIRE`: both stores have 835 messages and the same 104
  user messages. Assistant message `msg_f57aebe70001j3GaZpqjZJJGne` differs;
   the later snapshot inspection below explains the binary/tool-result differences.
- `ses_1ed5bed06ffeVCeuVxX1n0T8yx` and
  `ses_2350b4f76ffeYUwX52hG2dKUHq`: full message traversal encounters HTTP 500 on
  Marlin and both Reef accounts. Small initial pages can be read on Marlin; the
  failures are not proof that the entire histories are missing. Diagnosis remains
  open. The collector records these errors separately from successful comparisons.
- Current Reef's older copies are `ses_1cf2baf75ffeND5lbUPbfZHB2L` (20 versus 47
  messages), `ses_1d7d6c056ffetemMChlpadze4A` (97 versus 105), and
  `ses_1ed18ee11ffeJsBVEZ7YSOwsE2` (45 versus 77). Marlin and legacy Reef match
  on the fuller copies. The first two also retain an incomplete assistant turn on
  current Reef; one tool has an error there but completed on Marlin. Their user
  sequences are prefixes of the fuller histories.
- Tortoise's `ses_08e6d638cffeOOWvWDd7bwCc2s` has 231 messages versus 661 on
  Marlin/legacy Reef. Its non-system message content is a prefix after excluding
  outer message ID/time/metadata; 215 assistant envelopes differ.
- No different-ID pairs share both title hash and creation time, within or across
  stores. Some different-ID titles match, including subagent titles; those remain
  candidates for investigation. This metadata check does not rule out copies
  whose IDs, titles, or creation times were changed during import.

Artifacts on Marlin: `/tmp/opencode/session-drift-20261004/` contains all four
manifests, `metadata-comparison.json`, `transcript-comparison.json`, and the
per-store fingerprint reports. Collectors are
`/tmp/opencode/session-drift-inventory.py` and
`/tmp/opencode/session-drift-fingerprints.py`. Reports store hashes rather than
transcript text or authentication state. Reef retains the legacy manifests and
collector copies under `/home/rswift/.cache/paseo-upgrade/`.

The duplication is established in native session stores. The contents of CASS's
existing archive remain unverified because its read-only stats call failed.
Preserve separate host/account provenance if these stores are indexed with CASS;
its index-row deduplication does not decide which native continuation to retain.

## Canonical CASS archive decision and first setup step — 2026-10-04

- Ryan selected Reef as the canonical history/archive host. The intended owner is
  `rswift`, consistent with the coding-runtime migration. The candidate main data
  directory is CASS's default:
  `/home/rswift/.local/share/coding-agent-search/` on Reef.
- Supported access pattern: Reef pulls source histories through CASS remote
  sources; other computers invoke CASS on Reef over SSH. Agent integrations can
  launch `cass serve --stdio --mcp` through SSH, with explicit archive/index paths.
  CASS's persistent search service uses stdio; its documented interface does not
  provide an HTTP listener. Database storage stays local to Reef.
- Reef initially had CASS `0.8.0`, no `rswift` CASS database, and no sources config.
  Its existing `cass`/`cass-sync` units and timers were disabled and referenced
  `%h/.local/bin/cass`; reconcile their managed sources before enabling them.
- Upgraded only the requested CASS package through Homebrew to **`0.10.0`**, with
  automatic package cleanup disabled. Marlin and Tortoise remain on `0.8.0`.
- Verified the Reef binary and MCP initialization, tool discovery, and status
  over SSH. The service advertised search and canonical-view tools with explicit
  paths; status confirmed zero archive/index opens. This validates transport and
  protocol startup, not an ingested or searchable archive.
- Ryan approved **Reef → Marlin** and **Reef → Tortoise** Tailscale SSH access;
  both reverse connections passed verification. Reef's missing Tortoise host-key entry was added after
  verifying the scanned public key against Marlin's existing trusted entry;
  Reef's `known_hosts` is not chezmoi-managed. Earlier approvals for Marlin → Reef
  and Marlin → Tortoise did not cover these reverse connections.
- Next setup work: preserve and prepare source histories, create the central
  archive, verify source-labelled searches, then connect clients and arrange
  refresh/backup coverage. Preserve original native histories and distinct
  continuations alongside the normalized search archive. The three native API
  exceptions remain tracked in the audit above.

## Preserved snapshots and CASS ingest — 2026-10-04

- Consistent SQLite backups were made through SQLite's backup API, retaining the
  complete native backup only inside each owning account. CASS receives a separate
  projection containing exactly `session_v2`, `session_message`, `session`,
  `message`, and `part`; credential/account tables are excluded. Every export passed
  `PRAGMA quick_check`. These projections are search inputs, not native restore files.
- Current exports live at `~/.local/share/cass-source-exports/opencode/opencode.db`
  on Marlin, Tortoise, and Reef. Ryan ran the legacy snapshot as `opencode`, retained
  its full backup under `/home/opencode/.local/share/cass-source-snapshots/20261004/`,
  and installed the session-only export as `rswift` at
  `/home/rswift/.local/share/cass-source-exports/reef-opencode/opencode.db` on Reef.
- V2 session counts in the snapshots: Marlin **1,507** (two more than the earlier
  API inventory), Reef `rswift` **648**, legacy Reef **1,616**, Tortoise **288**.
  Marlin's export is 3,748,016,128 bytes; Tortoise's is 342,675,456 bytes. CASS rsync
  fetched both to Reef; destination SHA-256 values match the source reports.
- The snapshot helper is `/tmp/opencode/cass-opencode-snapshot.py` on Marlin and
  `.cache/paseo-upgrade/cass-opencode-snapshot-20261004.py` on Reef. It refuses
  existing destinations. Reports are `*-cass-snapshot.json` in Marlin's October 4
  audit directory. Reef's sources config is `~/.config/cass/sources.toml`, currently
  unmanaged by chezmoi, with distinct `reef-rswift`, `reef-opencode`,
  `marlin-rswift`, and `tortoise-rswift` names. Only OpenCode is enabled initially.
- Initial indexing reported **1,517 conversations / 80,120 messages**, no scan
  errors, and no quarantined conversations. Coverage inspection found 577 named
  `reef-rswift` conversations plus an automatically detected `local` source with
  the same 577 database sessions and **363 older JSON sessions** absent from Reef's
  648-session V2 inventory. The other 71 V2 sessions have no stored messages.
  These bootstrap duplicates remain preserved; the count is not a unique-history
  count. Older JSON coverage across all machines/accounts still needs inventory.
- **CASS auto-detection gotcha:** explicit local sources do not replace default
  OpenCode discovery, and the attempted `CASS_EXCLUDE_PATHS` setting did not prevent
  those scans. Named legacy sources must not absorb current-Reef defaults. The
  successful four-source index ran with `HOME`, `XDG_DATA_HOME`, `XDG_CONFIG_HOME`,
  and `XDG_CACHE_HOME` scoped beneath `~/.local/share/cass-index-home`; its
  `.config/cass` links to the real CASS config, all source paths are absolute, and
  `--data-dir` explicitly names the canonical archive. SSH sync uses the real home.
- **CASS 0.10.0 / stock-SQLite gotcha:** a stock `sqlite3` read-only open of the
  live CASS archive can rewrite its empty WAL index into a form that prevents the
  next FrankenSQLite write. Our coverage inspection triggered this known
  [upstream #509](https://github.com/Dicklesworthstone/coding_agent_session_search/issues/509)
  / [engine #443](https://github.com/Dicklesworthstone/frankensqlite/issues/443)
  failure: remote re-ingest exited 7 with `BusyRecovery`, despite no writer.
  Following the maintainer's workaround, with no CASS process or open DB holder,
  preserved `agent_search.db*` under
  `~/.cache/paseo-upgrade/cass-before-shm-workaround-20261004/` and moved only the
  live `agent_search.db-shm` into that backup. WAL was header-only (32 bytes).
  **Use idle bundle copies for stock-SQLite checks, never the live CASS archive.**
  The upstream engine fix is not yet in a newer CASS release. No database rows or
  certificates were removed. Scheduled CASS services/timers remain disabled.
- After the sidecar workaround, the four-source index completed successfully in
  194 seconds with **3,840 source-attributed conversations / 181,368 messages**
  processed, no scan errors, and no quarantine. An idle database-family copy at
  `~/.cache/paseo-upgrade/cass-after-four-source-index-20261004/` was inspected:

  | Source | Indexed conversations | Coverage against session-only snapshot |
  | --- | ---: | --- |
  | `reef-rswift` | 577 | All 577 V2 sessions with stored messages; 71 empty sessions omitted. |
  | `reef-opencode` | 1,540 | 72 empty sessions and four sessions containing only an empty assistant message omitted. |
  | `marlin-rswift` | 1,435 | All 1,435 V2 sessions with stored messages; 72 empty sessions omitted. |
  | `tortoise-rswift` | 288 | All 288 V2 sessions. |
  | `local` (bootstrap scan) | 940 | 577 duplicate current-Reef DB histories plus 363 older JSON histories. |

  Total preserved archive rows: **4,780 conversations / 233,403 messages**, covering
  **2,734 distinct native IDs**. Counts include host/account copies and bootstrap
  duplicates; they are not independent-conversation counts. Each named source's
  indexed paths belong exclusively to its intended snapshot/mirror. Both previously
  failing API histories are present in CASS; the longer legacy continuation is
  retained independently from Marlin's shorter copy.
- Source-filtered CLI searches passed for all four named sources (about 0.8–0.9 s
  per invocation). A single MCP process over Marlin → Reef SSH returned a search
  hit from each source, then read a canonical message from Tortoise's source.
  Status confirmed one retained lexical reader, four completed queries, one
  canonical read, and no maintenance. Proof:
  `/tmp/opencode/session-drift-20261004/reef-cass-mcp-proof.json` on Marlin.
  MCP readers pin their index until `cass_reload` or process reconnection.
- Older JSON metadata inventory now finds **364 session IDs** on both Marlin and
  Reef `rswift`, all outside the four earlier V2 inventories. Tortoise has 35 JSON
  session IDs, all represented in those V2 inventories. There are 364 additional
  distinct IDs across the three JSON stores; filename overlap is not proof of
  transcript equivalence. Evidence: `older-json-inventories.json` in the October 4
  audit directory. Legacy-account JSON storage and Marlin's old CASS archive still
  need preservation/coverage investigation before declaring reconciliation complete.
- Client-scope decision: Ryan accepted CASS access for any agent, rather than an
  OpenCode-only integration, while consolidating execution behind Paseo. No client
  MCP registration had been changed at that checkpoint. Inspection of deployed
  Paseo commit `b5b43edd6` found per-agent `mcpServers` and injection of its own
  tools, but no daemon-global third-party MCP registry shared by every provider.
  Approved direction: keep the archive/interface on Reef, manage each
  execution runtime's user-level registration through existing source management,
  and verify native/Paseo access for each runtime. Desktop/phone clients that only
  control Reef do not need their own CASS registration; locally executing agents
  on other hosts can use the same archive over SSH. Changing models within one
  OpenCode runtime does not require a separate registration per model.

## User-global OpenCode/Paseo CASS access — 2026-10-04

- Added Reef-only `mcp.servers.cass` to the chezmoi source
  `~/.local/share/chezmoi/dot_config/opencode/opencode.json.tmpl`; scoped apply
  changed only `~/.config/opencode/opencode.json`. It launches CASS's local stdio
  MCP with explicit canonical archive and database paths. Existing settings and
  other hosts' rendering are unchanged. This does not configure dedicated Codex,
  Claude, or Gemini runtimes.
  Template checks confirmed byte-identical Marlin, Tortoise, Lobster, and Barnacle
  rendering; native CASS connections were also checked outside this repository.
- The running Paseo agent discovered all six CASS tools after the config change,
  searched `reef-rswift`, `reef-opencode`, `marlin-rswift`, and `tortoise-rswift`,
  and read a canonical message. Status confirmed five queries, one canonical
  read, one retained reader, and no maintenance. No per-agent CASS override was
  needed.
- Native `opencode mcp list` reports CASS connected. A separate native
  `opencode run --model openai/gpt-6.1-sol` completed real MCP search/view calls for
  the same **Paseo Desktop setup for rswift** message (`reef-rswift`, conversation
  `1508`, message `1`, 152 bytes). Native session: `ses_ef7909836ffeDK7s111SDkb8oB`.
- Both runtimes adopted the configuration without restart or explicit location
  reload. Main Paseo PID/start time remained unchanged; no legacy service,
  ingestion schedule, or archive repair was changed.
- Private evidence:
  `/home/rswift/.local/share/agent-migration/2026-10-04-cass-runtime-access/`, with
  selected Paseo tool records, native JSONL/metadata, and a SHA-256 manifest.
  Access is now useful; automatic snapshot refresh, collection/indexing, and
  routine backup deployment remain pending. Readers still pin their lexical
  index until CASS reload or reconnection.

## Native audit exceptions inspected from snapshots — 2026-10-04

- Both API-failure sessions have valid stored message JSON: **146** messages for
  `ses_1ed5bed06ffeVCeuVxX1n0T8yx` and **12** for
  `ses_2350b4f76ffeYUwX52hG2dKUHq`. Ordered `(id, type, seq, canonical data hash)`
  arrays are identical across Marlin and both Reef accounts. This resolves the
  stored-history comparison for these IDs, not their native HTTP-500 diagnosis.
- The changed assistant message in `ses_0b64dd0cfffepjkJODhOpGFIRE` contains tool
  results, not a different user-message sequence. Marlin retains a completed
  `read` result with an embedded PDF URI (24,926,356 characters), plus an interrupted
  read. Legacy Reef contains two additional completed read records, text mentioning
  migration in place of the PDF-bearing result, and the same interrupted read.
  Preserve both copies; legacy Reef's extra records do not make it a byte-complete
  substitute for Marlin's binary-bearing history. CASS's text rendering is not a
  substitute for preserving this native payload.
- Evidence: `*-snapshot-exceptions.json` in Marlin's October 4 audit directory;
  `/tmp/opencode/session-snapshot-exceptions.py` records hashes and field structure,
  without printing transcript text or embedded file data.
