# A personal agent toolkit across runtimes

Status: OpenCode-first revision approved in Crit after round 3 on 2026-10-01
(session `0358398a35ac`), superseding the earlier baseline approved in session
`0b48471eca18`. Open questions remain where no explicit choice is recorded below.

Last reconciled: **2026-10-04**, using deployment checks from October 1–3 and fresh
four-store session metadata/transcript comparisons on October 4.

For the fresh Reef/Paseo session, use [the continuation handoff](paseo-handoff.md).
It records durable artifact locations, the accepted agent-wide CASS scope, and
the immediate task without requiring this entire design to be revisited.

Review covered: OpenCode's place in the daily workflow, the first milestone's
handoff requirements, and `rswift` ownership with background supervision.

Section 3 retains the pre-consolidation source inventory and dated deployment
checkpoints. Source work and deployment ownership are tracked in
[consolidation status](consolidation-status.md).

This is Ryan's internal toolset and operating plan. It records the current intent,
existing assets, proposed architecture, and questions that need experiments or
Ryan's judgment. The audience is Ryan and the agents helping maintain his setup.
Any future sharing should clearly label its personal assumptions and limited
support expectations. Recommendations remain proposals unless identified as
Ryan's direction. Deployment claims below are limited to the checks described.

### Current position

| Workstream | Recorded status |
| --- | --- |
| Reef backend and account migration | Upstream Paseo `0.11.0-beta.2` runs as `rswift` with Node `26.10.0` and canonical OpenCode `2.0.21`. The old `paseo` service is stopped/disabled; legacy OpenCode retirement is still pending. |
| OpenCode and client access | OpenAI OAuth with `openai/gpt-6.1-sol` passed a tool turn. Marlin and Android work. Desktop `0.11.0-beta.3` is installed on Marlin, Tortoise, and Reef; Reef/Tortoise GUI checks are deferred until physical access. |
| Native/Paseo continuity | Existing Paseo history and native continuation work with **Reload agent** on return. Ryan accepted manual reload; automatic live synchronization is deferred. Native-origin import and the remaining focused checks are still open. |
| Session history and legacy cleanup | Reef CASS `0.10.0` indexes all four preserved session-only snapshots; source-filtered CLI/MCP search and canonical viewing pass over SSH. Client wiring, older-store coverage, and scheduled refresh/backups remain open. Native history merges and legacy shutdown remain paused. |
| Toolkit source consolidation | Seven selected skills and installer/source checks are recorded as complete locally. Consumer deployment and runtime verification remain open in workstream B. |
| Broader integrations | Dedicated Codex/Claude/Gemini coverage, Hermes context sharing, browser verification, Entire, and additional execution hosts remain follow-on work. |

The actionable closeout checklist is in [section 6](#6-delivery-sequence). Resume
with Reef-owned CASS client wiring, older-store coverage, and possible
changed-ID copies. Snapshot inspection explains the changed assistant message and
confirms matching stored histories behind the two native API-read failures;
native readability still needs diagnosis.

## 1. Working thesis

Ryan wants a recognizable way of working with agents: engineering judgment,
writing style, browser workflows, and useful continuity between sessions.
Maintaining that behavior should become easier as clients and models change,
with development centered on Reef rather than repeated on each personal device.

The proposed foundation is one canonical repository for reusable instructions,
small integrations, compatibility records, and evaluations. It should work across
Ryan's existing model and agent subscriptions: OpenAI/Codex, Claude, Google AI Pro
(Gemini), OpenCode Go, GLM, Cursor, GitHub Copilot, and Devin.

OpenCode is Ryan's main coding tool today. The first delivery should improve that
daily workflow and preserve native OpenCode access. Paseo provides a complementary
way to observe and control coding work from Reef, Marlin, Tortoise, and the phone;
its clients should all connect to the Paseo backend on Reef.

Reef remains the default execution host. The approved first milestone is a working
OpenCode V2 route through Paseo, with demonstrated continuation between clients
and an explicitly tested handoff to and from native OpenCode. Dedicated Codex,
Claude, and Gemini/Antigravity routes follow. OpenCode's runtime priority is
separate from the choice of model or subscription used inside it.

Hermes is Ryan's general, technically capable assistant. Hermes and Paseo should
be aware of each other's relevant work, with useful project/session references,
context, and outcomes flowing between them. Starting, stopping, or steering coding
work from Hermes is an occasional workflow. Each environment should have its own
purpose-fit tools and skills, with shared material only where it is useful.

Browser tooling provides capabilities for those workflows. Entire is a candidate
for recording the work behind code changes. Other homelab computers and external
execution providers such as exe.dev and Daytona are candidates for running work
behind the Reef-centered coding experience.

The central hypothesis is that consolidating source ownership, choosing a clear
coding home, and connecting the right context can reduce maintenance and improve
results. The plan should test that with role-specific capabilities and real work.

## 2. Requirements and provisional decisions

### Direction established by Ryan

- Centralize reusable work from `agent-tools`, `skills`, chezmoi's personal skills
  and evaluations, and the browser repositories, wrappers, workspace, and saved
  customizations. Use the source map below to decide what to import or integrate.
- Make the resulting toolkit feel personal while keeping maintenance manageable.
- Treat OpenCode as Ryan's primary coding tool. The earlier Codex-first plan
  understated its importance and needs revision around actual daily use.
- Consolidate OpenCode onto one maintained V2 installation/version on Reef.
- Use `rswift` as the execution identity, with a lingering systemd user service
  for Paseo and OpenCode's native V2 background service. This target was approved
  and the new runtime is operating; the legacy account remains pending cleanup.
- Use Reef as the normal coding host and the backend for every Paseo client;
  retain useful native OpenCode access and minimize execution stacks on clients.
- Accept serialized native OpenCode ↔ Paseo handoff with **Reload agent** for the
  initial setup (Ryan, 2026-10-02). Automatic synchronization is deferred.
- Compare session drift across Marlin, Reef's two accounts, and Tortoise before
  importing or archiving legacy history and retiring services (Ryan, 2026-10-03).
- Keep Hermes as a separate general technical assistant. Give Hermes and the
  coding environment mutual awareness through selected context and handoffs,
  while maintaining purpose-fit tool and skill sets.
- Support OpenAI/Codex, Claude, Google AI Pro/Gemini, OpenCode Go, GLM, Cursor,
  GitHub Copilot, and Devin through their available model/agent access paths.
- Support clients on Reef, Marlin, Tortoise, and Ryan's Android phone (Play Store).
- The backend update selected upstream Paseo `0.11.0-beta.2` on Reef, with the old
  custom fork retained for recovery. Following design approval, the backend was
  migrated to `rswift`; the 2026-10-02 checkpoint below records validation.
- Drop Jules and ToolHive from the target setup, including their obsolete skills.
- Evaluate Entire as part of the overall workflow.
- Explore execution capacity on existing homelab computers and on exe.dev,
  Daytona, or similar providers.
- Keep this an internal personal-toolset plan as scope grows.

### Delivery direction and remaining recommendations

- Deliver OpenCode V2 through Paseo first, using Ryan's existing intended model
  access. Follow with dedicated Codex, Claude, and Gemini via Antigravity/`agy`;
  then expand OpenCode Go and GLM coverage. Cursor, Copilot, and Devin remain later
  targets. A working OpenCode route need not wait for every subscription.
- Complete the `rswift` cutover by preserving the selected history and replacing
  legacy remote-native launchers before retiring the old listener.
- Finish the serialized native OpenCode ↔ Paseo checks in section 4. Manual reload
  is accepted; shared live control is deferred.
- Keep `agent-tools` as the canonical repository initially; decide naming later.
- Organize skills by purpose and runtime; share instructions when the actual
  workflows overlap. A single repository can own several distinct skill sets.
- Keep standalone applications and libraries in their existing repositories;
  describe and test their integration from the toolkit.
- Reuse the existing evaluation assets after reviewing their assumptions.
- Keep client-side configuration small and deploy coding capabilities on Reef or
  the selected execution host. Use chezmoi for the relevant machine settings.

## 3. What already exists

Paths below are relative to Ryan's home unless shown as a repository URL. This
table records the source inventory before consolidation; the deployment checkpoint
below records subsequent backend work.

| Asset | Location and observed state | Implication |
| --- | --- | --- |
| Engineering toolkit | `dev/personal/agent-tools`, `thisisryanswift/agent-tools`, clean at `b403a63` before this draft | Four existing skills: code review, test coverage, brainstorming, Jules (selected for retirement). Canonical prompts plus copied skill references, OpenCode agents/commands, and a V1-era git-ai plugin. |
| Specialist skills | `dev/skills`, `thisisryanswift/skills`, HEAD `21fff3b` | Five tracked skills: session migration, Jules (excluded from import), blog style, ToolHive operator (excluded from import), Wayland icon repair. Two untracked Compound plugin directories also exist. |
| Installed/custom skill sources | `.local/share/chezmoi/dot_agents/skills/` | Includes `browser-harness`, `ryan-blog`, and `wayland-app-icon-fix`. These must be compared with repository versions; a two-repository merge alone misses active source material. |
| Existing evaluation harness | `.local/share/chezmoi/dot_agents/evaluations/` | Eight scenario definitions, fixture builders, frozen arms, launchers, grading records, and non-model checks. Pinned expectations target OpenCode 1.18.10; README reports no counted model runs. |
| Browser Harness upstream checkout | `dev/tools/browser-harness`, origin `browser-use/browser-harness`, clean at `f5f3ad9` | Python/CDP harness, CLI, MCP interface, and upstream skill. This is an upstream checkout, not a Ryan-owned toolkit implementation. |
| Saved browser customizations | `dev/tools/browser-harness`, `stash@{0}` at `f6c0fd0`, dated 2026-07-28, “pre-v0.1.8 local browser profile customization” | Actual Git stash affecting `SKILL.md` and `src/browser_harness/helpers.py`: earlier isolated-profile/CLI guidance, tab hygiene, and a `close_tab` helper. Inspected without applying it. Compare with current upstream, chezmoi, and the worker package before selecting reusable content. |
| Browser worker package | `dev/tools/browser-harness-workers`, `thisisryanswift/browser-harness-workers`, HEAD `50236e1` | Named persistent profiles and disposable authenticated workers. Local uncommitted dependency change from Browser Harness 0.1.8 to 0.1.10. |
| Browser wrapper/workspace sources | `.local/share/chezmoi/dot_local/bin/executable_browser-harness-{isolated,worker}` and `.local/share/chezmoi/dot_config/private_browser-harness/private_agent-workspace/` | Existing wrapper implementations plus reusable helpers and a domain-skills area. Establish the relationship to the packaged workers before replacing either. |
| Paseo integration work | `dev/tools/paseo`, branch `ryan/opencode-external-server`, HEAD `e0e50c9a8` | Substantial uncommitted external-OpenCode-server adapter work, tests, and design doc. Upstream and personal fork remotes are configured. |
| Reef deployment history | `dev/homelab/runbooks/reef-coding-services.md` | Partly stale runbook records a `/srv/dev/tools/paseo-next` deployment and a dirty original checkout. Its September observation supersedes parts of the older topology. Re-inventory the live backend and all clients before selecting the upgrade path. |
| Homelab resources | `dev/homelab/inventory.md`, last verified 2026-09-06 | Lists Reef, Marlin, Tortoise, Lobster, Barnacle, Beluga, and a Mac mini with different roles. Refresh availability and workload suitability; existing infrastructure and inference roles are inputs to placement. |
| Hermes candidate source | `dev/hermes-update-2026-09-27`, branch `deployment/v0.21.5`, clean at `6814f60907` | Fleet update snapshot with Hermes skills, plugins, CLI, gateway, TUI, desktop, and profile-aware configuration. Local origin points to `.hermes/hermes-agent`; this checkout does not prove deployed versions. |
| Hermes coding coordinator | `dev/homelab/coding_pm/` | Implemented MCP wrapper for a Hermes profile to drive OpenCode V2. Commits `b713389` and `31c7066` exist; its earlier design doc still says “not built.” Reassess as an occasional bridge under the new Paseo-centered direction; runtime status needs separate verification. |
| Entire | `entireio/cli` upstream; prior session research | Session capture and checkpoint candidate. Prior inspection found a V1 integration and open V2-support PR #2589; status needs refreshing before a trial. |

### Backend checkpoint observed on 2026-10-01

- Reef's `/srv/dev/tools/paseo-next` is clean on upstream `main`, commit
  `b5b43edd65cc1253493b13cca3941dd390df6ef3`, package version `0.11.0-beta.2`.
  The previous branch `ryan/opencode-reef-inbox` remains at `b348be7cb`.
- The deployment build and candidate server typecheck passed. Targeted lint and
  all 28 tests in the V2 adapter's `agent.test.ts` passed. These are not live
  provider or client acceptance tests.
- Paseo's Supervisor and Daemon run as `paseo`; `/api/health` returned 200 after
  startup. Its unit needed a drop-in selecting `/usr/bin/npm` because the old
  Homebrew npm path no longer existed. System Node is `22.22.2`; installation and
  build ran with `rswift`'s Node `26.10.0`, so native modules still need runtime
  validation under the selected service Node.
- Paseo's OpenCode provider is unavailable. Its configured command is `opencode`,
  but the `paseo` account cannot traverse the `0700` directories containing
  `rswift`'s Homebrew OpenCode `2.0.21`. No replacement binary was selected.
- The independent OpenCode listener remained owned by `opencode`. Initial
  inspection found `/usr/local/libexec/opencode/active` pointing to `1.18.30`.
  Direct process inspection on 2026-10-03 later confirmed that both live legacy
  servers actually ran `2.0.18`; the selector alone did not identify their running
  version. Those servers were not replaced during the Paseo update.
- The fork-only `agents.externalOpenCodeAdoption` and
  `agents.providers.opencode.serverUrl` fields were removed from Paseo's private
  config; upstream schema validation passed. Automatic native-session adoption
  and external-server attachment are no longer supplied by that fork.
- Ryan completed the standard Restic backup, a separate uploads backup, and a
  backup of the identified Paseo unit/environment files before cutover. The
  standard backup script omitted `/srv/paseo/uploads` despite the runbook's claim.
  Any later migration needs a fresh checkpoint including effective unit drop-ins.

At this checkpoint the backend upgrade had reached daemon health; account and
workflow validation continued after design approval as recorded below.

### Runtime and continuity checkpoint observed on 2026-10-02

- Reef's upstream Paseo `0.11.0-beta.2` now runs as `rswift` under the enabled
  systemd user unit `~/.config/systemd/user/paseo.service`, using Node `26.10.0`
  and `PASEO_HOME=/home/rswift/.paseo`. The last check found it active with no
  automatic restarts.
- The previous `paseo`-owned service is stopped and disabled. The stopped-state
  backup is `/var/backups/paseo-rswift-20261001-190854/state.tar.gz`; the previous
  personal home remains at `~/.paseo.before-rswift-20261001-191357`.
- Preserve the old service's network overrides when moving units:
  `PASEO_LISTEN=100.81.54.26:6767` and
  `PASEO_HOSTNAMES=reef,reef.tail1cda9f.ts.net,paseo.wharfi.sh,paseo.reef.wharfi.sh`.
  Without them, the copied config listened only on loopback and existing direct
  connections failed. Existing pairing works after restoring these settings.
- Paseo launches `/home/linuxbrew/.linuxbrew/bin/opencode` (`2.0.21`) under
  `rswift`. A real `pwd` tool turn succeeded through OpenCode using
  `openai/gpt-6.1-sol` and the account's OpenAI OAuth connection. The same display
  name under `openrouter/openai/gpt-6.1-sol` returned `User not found`; provider
  identity must be checked along with the model label.
- Android connectivity, workspace terminal/Git, and attachment checks succeeded.
  Those initial agent checks used Codex, so they do not establish OpenCode
  attachment coverage. Clearing Tailscale 1.102.3 storage and reauthenticating
  restored phone connectivity; the precise Tailscale failure cause is unconfirmed.
- Marlin now has the upstream Paseo `0.11.0-beta.3` RPM. Its local desktop launcher
  uses `/opt/Paseo/Paseo`, replacing the checkout-built `0.1.81` launch path.
  Ryan confirmed Marlin and Android both work against Reef.
- Tortoise and Reef also have the upstream `0.11.0-beta.3` RPM. Package versions,
  executable links, and desktop launchers were verified. Tortoise upgraded from
  `0.6.1`; Reef's local launcher now selects `/opt/Paseo/Paseo` instead of its
  `0.3.1` AppImage. Built-in daemon management is disabled on both desktops.
  Reef's systemd backend remained active with the same supervisor PID and a 200
  health response after installation. Ryan deferred GUI connection checks on
  these two hosts until the next time he has physical access, rather than setting
  up remote desktop access for this verification.
- Paseo-created native session `ses_f03397d7dffezLiAeQp2n3D8BE` in
  `/srv/dev/homelab` opened in native OpenCode with its full transcript. Ryan then
  continued it natively. The new turn appeared in Paseo only after right-clicking
  the agent and choosing **Reload agent**; reopening the tab was insufficient.
  This demonstrates persisted history and native continuation with manual reload,
  not shared live execution or automatic cross-server updates.
- Still unverified: a fresh native-origin session imported and continued in Paseo,
  a Paseo tool turn after the reverse handoff, permission/interruption behavior,
  OpenCode attachments, and GUI connection/continuation on Reef and Tortoise. Ryan
  accepted the manual-reload limitation on 2026-10-02 and deferred live
  synchronization.
- The legacy `opencode` account remained in place. Its private home required a
  subsequent sudo-assisted inventory, recorded below. The deployment runbook
  still needs reconciliation with the new runtime.

### Session drift audit started on 2026-10-03

Ryan paused history import and legacy retirement to compare four stores: Marlin's
`rswift`, Reef's `rswift`, Reef's legacy `opencode` account, and Tortoise's `rswift`.
Earlier imports from Marlin to Reef mean the stores may overlap and then diverge.
Compare session IDs and metadata first, then transcript fingerprints for overlaps;
timestamps alone do not establish which copy has the complete conversation.

The privileged Reef inventory found two legacy V2 `2.0.18` servers: the enabled
`opencode-serve.service` on `100.81.54.26:4096` and a separately registered native
background server. Both reported no active sessions and matching recent history
at inspection. `opencode-keyring.service` was also enabled/running. The old
account's current database was about 12 GiB, with several older backup files
retained. Recheck activity before any later shutdown.

| Store | Inventory progress |
| --- | --- |
| Marlin `rswift` | October 4 API inventory: 1,505 sessions (643 roots, 862 children), one active session. V2 `2.0.21`. |
| Reef `rswift` | Complete API inventory: 648 sessions (394 roots), no active sessions. V2 `2.0.21`. |
| Reef `opencode` | Sudo-assisted API inventory: 1,616 sessions (686 roots), no active sessions. V2 `2.0.18`. |
| Tortoise `rswift` | Complete API inventory: 288 sessions (188 roots), no active sessions. V2 `2.0.21`. |

No repeated IDs appeared during metadata pagination. The four stores contain
2,445 distinct IDs across 4,057 session records, including subagents. IDs present
in just one current store: Marlin 426, current Reef 116, legacy Reef 537, Tortoise
287. These are identity counts, not proof that every differently keyed transcript
has unique content.

The October 4 shared-ID comparison confirms the old copy operation:

- Marlin/legacy Reef share **1,079 IDs**: **1,075 exact projected-transcript
  matches**, one legacy-Reef continuation, one changed assistant message, and two
  HTTP-500 transcript traversal failures.
- Current Reef shares 532 IDs with each: 527 exact matches, three older copies
  whose fuller histories match on Marlin/legacy Reef, and the same two failures.
- Tortoise shares one ID with Marlin/legacy Reef and has an older copy of it; it
  shares no IDs with current Reef.

All 1,079 shared Marlin/legacy-Reef sessions have different workspace locations,
despite most transcripts matching exactly. No different-ID pair shares both title
hash and creation time, but same-title candidates remain to investigate. Snapshot
inspection subsequently established equal stored message arrays for both API
failures (146 and 12 messages) across Marlin and both Reef accounts. The changed
assistant message contains an embedded PDF on Marlin that legacy Reef replaces
with migration-related text and extra read records; retain both copies. Native
readability and remaining changed-ID questions are still open. Detailed IDs,
counts, method, and limitations are in the [consolidation status](consolidation-status.md).

CASS `0.10.0` adds OpenCode V2 indexing. Ryan selected Reef as the canonical CASS
archive host on October 4, with other computers accessing searches over SSH and
agent access through the stdio MCP interface. The archive should collect histories
with distinct host/account attribution and preserve newer work from every store.
Reef's `rswift` had no existing CASS database; its package is now upgraded to
`0.10.0`, and MCP startup/discovery/status passed over SSH. All four session-only
snapshots passed SQLite checks; Marlin/Tortoise mirrors passed SHA-256 verification.
Four-source indexing succeeded and source-filtered CLI/MCP searches plus a canonical
view passed over SSH. The named sources contain 3,840 searchable conversations;
the archive also retains 940 bootstrap rows, including 363 older JSON histories.
The older JSON inventory identifies 364 additional IDs outside all four earlier V2
inventories. Client configuration, older-store coverage, and refresh/backup deployment
remain open. The stock-SQLite inspection exposed CASS's known BusyRecovery bug; the
maintainer's sidecar workaround and copy-only inspection rule are documented in
the status log. Marlin and Tortoise remain on `0.8.0`; Marlin's existing archive
failed a read-only stats check and remains preserved for investigation.

Working artifacts (rerun the inventory if temporary files are unavailable):

- Current manifests, fingerprint reports, and comparisons:
  `/tmp/opencode/session-drift-20261004/` on Marlin. The October 3 Marlin manifest
  remains under `/tmp/opencode/session-drift-20261003/`.
- Reusable read-only API inventory: `/tmp/opencode/session-drift-inventory.py` on
  Marlin; it uses an existing server and does not start one.
- Transcript collector: `/tmp/opencode/session-drift-fingerprints.py` on Marlin.
  It uses paginated native APIs and saves message hashes without transcript text.
- Legacy full reports on Reef:
  `/home/rswift/.cache/paseo-upgrade/session-drift-20261004-legacy.json` and
  `/home/rswift/.cache/paseo-upgrade/session-drift-20261004-legacy-fingerprints.json`.

Ryan renewed Tailscale SSH approval and ran the legacy collectors with sudo on
October 4. Native `opencode-reef` launchers on Marlin and Reef still target
the old listener; their chezmoi source is
`dot_local/bin/executable_opencode-reef`. Updating the source and applying only the
selected target is part of the later cutover. History merges, archive selection,
and legacy OpenCode shutdown remain paused pending the audit.

### Source-consolidation findings and remaining drift

The following were identified during the pre-consolidation inventory. The source
workstream has since recorded seven selected skills, the combined blogging and
browser guidance, V2 session-migration guidance, and the Jules/ToolHive source
retirements. See [consolidation status](consolidation-status.md) for that completed
work; consumer migration and runtime verification remain pending.

- **Jules and ToolHive:** the source workstream removed Jules from the toolkit and
  excluded `toolhive-operator` from the selected catalog. Consumer migration and
  final source commits remain part of workstream B.
- **Blogging:** the selected source combines the earlier guidance as `ryan-blog`.
  Move consumers to that canonical copy during deployment.
- **Wayland repair:** the imported skill was verified byte-identical to both
  original copies; consumer cutover remains pending.
- **Session migration:** the selected skill now documents V2 session tools/API
  rather than direct V1 database recipes. Cross-server behavior still needs
  verification against the histories selected after the drift audit.
- **Installation:** a skill-link installer with preservation checks is prepared
  and locally tested. Inventory live consumers before applying selected links
  through the appropriate source manager.
- **Evaluation:** the V1 evaluation source/migration map is recorded. Port useful
  scenarios and align older Crit/Ticket assumptions with current preferences
  before running new behavioral comparisons.
- **Browser skill identity:** the selected personal source is
  `browser-harness-cli`. Upstream, the worker package, chezmoi wrappers, and native
  client browser tools still need host/runtime verification; source consolidation
  does not establish interchangeable implementations.

## 4. What support means

“Supported” should name a workflow and a tested configuration, not merely a valid
`SKILL.md`. Track runtime/client versions, installed toolkit revision, tool
availability, and the evidence for each claim.

| Surface | Intended role | First support checks |
| --- | --- | --- |
| OpenCode V2 | Primary coding runtime and first end-to-end delivery | Use the intended models/account, run tools, discover selected skills, and resume work through Paseo and native OpenCode under the reviewed continuity contract. |
| Paseo clients + Reef backend | Cross-device observation and control alongside native OpenCode | All clients select the same Reef backend, observe the same work, and reconnect without moving execution to a client machine. |
| Codex, Claude, Gemini/Antigravity | Additional coding-provider routes after the OpenCode milestone | Each chosen runtime authenticates through the intended subscription, completes a real tool-using task, and supports usable follow-up/review through the clients. |
| Hermes | Separate general technical assistant across its own surfaces and profiles | Use its own selected tools/skills; exchange relevant project/session context and outcomes with Paseo; preserve profile scope and cache-aware updates. |
| Browser Harness + workers | Browser execution and reusable site knowledge | Select the intended profile/worker, perform a real interaction, verify the result, and clean up owned workers across success and failure. |
| Entire + selected runtime | Recorded history and handoff evidence | Capture a fresh session and checkpoint; inspect actual recorded content; verify the documented resume path and configured storage behavior. |
| Homelab/cloud execution workers | Additional execution capacity behind the Reef-centered experience | Prove workspace placement, start/observe/stop behavior, artifact return, and client continuity for a chosen worker. |

### Provider and subscription coverage

First validate the OpenCode runtime with Ryan's intended current model routes.
Record the actual provider/model IDs and subscription or credential source during
inventory. OpenCode is not synonymous with OpenCode Go; putting the runtime first
does not select a different subscription or prove direct Codex/Claude integration.

Track the full route: **subscription/account → available model or agent interface
→ execution runtime → Paseo/client integration → task evidence**. The services
below offer different kinds of access; a subscription is not automatically a
general-purpose inference API credential. Prefer existing subscription access
where available and make any separately billed API route explicit.

| Priority | Ryan's subscription/service | Access path to establish | Paseo validation needed |
| --- | --- | --- | --- |
| First | Existing daily OpenCode model access | Verified OpenAI OAuth with `openai/gpt-6.1-sol` under `rswift`. The OpenRouter model of the same display name failed. | Tool use and manual-reload native continuation passed; finish native-origin import, permission/interruption, attachment, and selected client checks. |
| Next 1 | OpenAI/Codex | Use Ryan's Codex subscription through the dedicated Codex runtime on Reef. | Initial tool/attachment smoke checks passed through Codex; subscription-route and cross-client coverage still need explicit completion. |
| Next 2 | Claude | Verify Claude Code access for the current subscription; record any separate API route independently. | Test authentication, model choice, tool use, and session continuity through the Claude Code adapter. |
| Next 3 | Google AI Pro / Gemini | Establish Ryan's requested Antigravity/`agy` route and its actual subscription-backed capabilities. | Verify the required agent interface and adapter from Reef. Any alternate Gemini route needs an explicit choice rather than counting as proof of this one. |
| Expand | OpenCode Go | Verify subscription-backed model use in OpenCode, earlier if it is already one of the selected daily routes. | Exercise the actual subscription-backed models through Paseo. |
| Expand | GLM | Confirm the subscribed GLM service and eligible runtime/API integration. The local Paseo custom-provider doc describes a Z.AI coding-plan route to evaluate. | Test the selected runtime/custom-provider route with that subscription. |
| Later | Cursor | Identify the usable Cursor agent/CLI integration and subscription-backed capabilities. | Establish an adapter or handoff path; support has not been verified in this inventory. |
| Later | GitHub Copilot | Verify Copilot CLI access and the models available on the current subscription. | Paseo's local README lists Copilot; test the selected CLI/runtime configuration. |
| Later | Devin | Identify the supported Devin task/session interface and account access. | Establish how work is started, observed, and reviewed; direct Paseo support remains unverified. |

For each route, record model selection, available tools/skills, usage limits,
resume behavior, and whether work can remain on the intended host. Unsupported
paths remain explicit gaps in the coverage matrix. Compare providers within a
fixed runtime where possible, then test the complete client/runtime combinations;
otherwise model differences and integration differences become confounded.

### Execution identity and process supervision

Approved target: Reef's personal coding stack runs as `rswift`. Paseo and native
OpenCode V2 now operate under that account; retirement of the legacy OpenCode
processes is paused for the drift audit. The former split across `paseo` and
`opencode` required duplicate runtime setup, private-home configuration,
workspace/Git access rules, and upload ACLs. Consolidation brings execution closer
to Ryan's direct CLI workflow, using the files and credentials available to
`rswift` as the selected account boundary.

Keep lifecycle management explicit:

| Component | Selected owner and lifecycle |
| --- | --- |
| Paseo backend | `rswift` systemd user service; lingering provides operation across logout and boot. |
| Native OpenCode V2 | `rswift`'s normal background service, using the canonical OpenCode executable. Select and test its remote-client connection separately. |
| Paseo-managed OpenCode | Paseo launches its own helper from that same executable as `rswift`; the selected upstream adapter does not attach to the native background service. |
| Provider tools, selected skills, and configuration | Installed for the execution account on Reef; authenticate deliberately for that account and runtime. |
| Client applications | Connect to Reef; local UI shutdown does not own the server lifecycle. |

Use one installation and update path for the OpenCode executable. Configure
Paseo's provider command explicitly to the same stable executable path used by
the native CLI, and verify the running server versions after upgrades. Existing
processes retain their loaded version until restarted, so upgrades include
coordinated restarts after active work has finished. Historical binaries retained
for rollback are not separate maintained runtime installations.

With the selected upstream adapter, a single installation can run several server
processes. Paseo spawns `opencode serve --hostname 127.0.0.1 --port 0`, with its own
authentication and bridge plugin. Ordinary Paseo sessions can reuse that helper;
custom environment or MCP settings can require dedicated helpers. These helpers
use the configured executable rather than installing another OpenCode version.

One shared server for native clients and Paseo is a separate integration goal.
OpenCode V2 exposes service discovery/reuse through `@opencode/client/service`,
but the selected Paseo adapter does not use it. Sharing the native service would
require adapter work covering the bridge plugin, environment/MCP behavior, live
session control, and detach-only lifecycle ownership. Running both as `rswift`
does not itself enable that topology.

A systemd user service does not automatically inherit the interactive terminal's
shell initialization, PATH, or SSH/keyring environment. Select explicit runtime
paths and required environment, and verify provider behavior from the service.
Use one compatible Node version for dependency installation and service execution.
Manage unit sources and limited host settings in their existing source manager.

Migration should preserve Paseo's host identity and client pairing where supported,
agent/workspace records, uploads, and native history. Inventory the existing
`rswift` state first so no home or database is blindly overwritten. Transfer only
selected application state through a validated route; establish authentication as
`rswift` without copying another account's authentication state. Keep the existing
service accounts, units, and backups recoverable until the new setup passes real
workflow checks. Retire obsolete units/accounts only after that validation.

### OpenCode session continuity

Specify and test these separately:

1. **Environment continuity:** both entry points use the intended account, models,
   project configuration, skills, and workspace paths.
2. **Persisted-session continuity:** the same native session and transcript can be
   found and resumed from the other entry point after its active turn ends.
3. **Live-session continuity:** clients observe the same running execution and can
   deliver permissions, questions, interruption, or follow-ups to its owning server.

The upstream V2 adapter starts an authenticated helper on an ephemeral loopback
port. Its `opencode-home` path is the process working directory. The adapter does
not itself assign a separate `HOME` or XDG data directory, so normal same-account
defaults may share OpenCode storage. Provider environment overrides can change
that. A shared database does not establish shared live events or execution
ownership; verify concurrent-process support and the actual state paths.

Remaining first-milestone check: begin a fresh native OpenCode session on Reef,
finish a turn, find/import that session in Paseo, and continue it. Exercise the
reverse handoff as well and verify history, model/agent selection, tool results,
permissions/questions, and attachments. Use the same native session ID and avoid
simultaneous writers during this baseline test. Reconciliation of the four
existing session stores is a separate check before retiring the legacy services.

Ryan accepted serialized handoff with **Reload agent** on 2026-10-02 after testing
the upstream behavior. Simultaneous live control and automatic synchronization are
deferred. Revisit the integration approach if that requirement changes. Keep the
preserved fork as reference material; its V1 external-server code is not a V2
implementation. The remaining native-origin import/continuation check is distinct
from the accepted manual-refresh limitation.

### Hermes–coding awareness

The initial contract should be small and useful in both directions:

- Hermes can understand which coding projects/sessions exist, their purpose,
  status, blockers, and relevant outcomes, and point Ryan to work in Paseo.
- A coding session in Paseo can receive relevant requirements, research, and
  decisions from Hermes and return a concise outcome or follow-up reference.
- Define durable project/session identifiers and which context is explicitly
  shared. Evaluate whether an existing API, MCP bridge, or shared knowledge store
  supplies this contract before introducing another service.
- Give each side its own tools and skills. Shared guidance is selected for actual
  overlap; visibility into work and the authority to control it are separate
  integration choices. Occasional explicit control from Hermes can be added where
  Ryan finds it useful.

This reframes the older `coding_pm` design: OpenCode is the daily coding tool,
Paseo provides cross-device coding access, and Hermes retains its broader role.
Context links should identify the native runtime/session as well as any Paseo
record so work remains understandable from either coding entry point.

### Important integration facts

Paseo manages other agent runtimes. Installing a skill in a client UI is not proof
that a remote provider can discover its files or run its tools. The selected
upstream backend has separate V1 and V2 adapters, pins `@opencode/client` 2.0.10,
and requires an OpenCode V2 binary at least 2.0.10. Detection, OpenAI authentication,
and a tool turn passed under `rswift` with V2 `2.0.21`; remaining acceptance checks
are listed in section 6. The older fork's `@opencode-ai/sdk/v2/client` import
targets V1 and does not prove V2 compatibility.

Hermes skills support runtime-specific metadata for required tools/toolsets and
platforms. Its development guide emphasizes profile scope and a stable prompt
prefix within a conversation. Its selected skill set must account for those
behaviors; shared instructions need verification in every intended consumer.

Client, agent server, terminal execution target, and browser can be on different
machines. Capability documentation should identify where each resource lives.
File paths and authenticated browser state do not automatically follow a session.

## 5. Proposed repository organization

Evolve the existing repository incrementally toward:

```text
skills/                 # Catalog with shared, coding, and Hermes-specific selections
integrations/           # Small runtime/client adapters and tested setup contracts
evals/                  # Selected fixtures, rubrics, runners, sanitized results
docs/                   # Working design, inventory, compatibility, decisions
scripts/                # Only the installation/validation helpers actually needed
```

Existing `prompts/`, `agent/`, `command/`, and `plugin/` can remain during the
transition. Choose one editable source for each instruction and make any generated
copies explicit. Keep stable skill IDs where practical and document intentional
renames.

For each skill or integration, record its purpose, upstream provenance/license,
required tools, intended role/runtime, deployment target, and latest verification.
A small Markdown catalog is sufficient initially. Installation selects the
appropriate set for coding runtimes or Hermes rather than distributing every skill
to every agent.

The toolkit owns reusable content; the selected execution host receives the
relevant runtime and capabilities. Reef is the default coding host. Marlin,
Tortoise, and the phone need current Paseo clients and a connection to Reef;
retain native OpenCode clients where Ryan uses them and document how they connect
to the intended execution host. Chezmoi's role should stay small: relevant
client/connection preferences and host-specific configuration, with runtime/skill
deployment scoped to the hosts that execute work. Existing local tool
installations are migration inputs.
ToolHive has no role in the target distribution path. Independent packages such
as `browser-harness-workers` retain their own release lifecycle.

## 6. Delivery sequence

### A. First milestone: OpenCode-first coding from Reef and the four clients

**Status on 2026-10-04:** the core runtime works; history reconciliation and
operational closeout remain open. Client GUI checks explicitly deferred by Ryan
remain recorded below.

Completed:

- [x] Approve `rswift` ownership and the OpenCode-first sequence; accept manual
  **Reload agent** for native/Paseo handoff and defer live synchronization.
- [x] Take the stopped-state Paseo backup, preserve the previous personal home,
  migrate Paseo application state and upload access, and enable the new user
  service with Node `26.10.0`. Stop and disable the old `paseo` service.
- [x] Configure the canonical OpenCode `2.0.21` executable, restore listener and
  hostname overrides, and verify health and existing client pairing.
- [x] Verify an OpenCode tool turn with `openai/gpt-6.1-sol` through OpenAI OAuth.
  Verify workspace terminal/Git access; initial attachment evidence used Codex.
- [x] Install upstream desktop `0.11.0-beta.3` on Marlin, Tortoise, and Reef and
  correct the old desktop launch paths. Confirm Marlin and Android work against
  Reef. Verify built-in daemon management is disabled on Tortoise and Reef.
- [x] Open the Paseo-created session in native OpenCode with its full history,
  continue natively, and observe that turn in Paseo after **Reload agent**.

Closeout, in current working order:

1. [ ] **Audit session drift first.** Four-store inventories and shared-ID
   fingerprint comparisons are collected. Snapshot inspection explains the changed
   assistant message and matches stored rows for both API failures. Finish older
   JSON/Marlin CASS coverage, possible changed-ID copies, and native-readability
   diagnosis before selecting imports. All four snapshots are searchable on Reef;
   enable user-global OpenCode CASS access next, then automate refresh/backups.
2. [ ] Choose which histories to import or archive after reviewing that evidence.
   Take a fresh appropriate backup before changes, preserve the original stores,
   and validate any selected import without overwriting existing `rswift` history.
3. [ ] Select and test the replacement native remote-access path. Update the
   chezmoi-managed `opencode-reef` launchers, which still target the old listener.
4. [ ] After history and native access are ready, recheck legacy activity and
   complete the authorized stop/disable of obsolete OpenCode services and the
   separate background server. Reconcile executable paths and retained rollback
   artifacts. This step is paused while the drift audit is incomplete.
5. [ ] Finish the focused OpenCode checks: native-origin session import into
   Paseo, a Paseo tool turn after returning from native, permissions/questions,
   interruption, and an OpenCode attachment.
6. [ ] **Deferred until physical access:** open the installed desktop clients on
   Reef and Tortoise, connect to Reef, continue the same work, and confirm client
   shutdown leaves backend work available. Remote-desktop setup is deferred too.
7. [ ] Reconcile managed service/config sources and routine backup coverage for
   uploads and effective service configuration. The published October runbook and
   continuation handoff record current state; the dirty Reef homelab branch's
   historical edits remain preserved. Toolkit implementation changes remain
   uncommitted on Marlin and have a private recovery snapshot on Reef.

Completion: a version-recorded Reef backend, usable OpenCode V2 with Ryan's
intended model access, four working Paseo clients, and demonstrated continuity
at the level approved in this review. An unresolved required behavior is recorded
as a blocker. Dedicated Codex, Claude, and Gemini routes follow this milestone.

Independent source consolidation can proceed alongside this work; its completed
local checks remain recorded in the consolidation status. Broader provider/worker
coverage does not displace the daily OpenCode workflow on the critical path.

### B. Consolidate reusable sources and deploy selected capability sets

**Recorded progress:** source selection/import, seven skills, installer checks,
and source provenance are complete locally in the toolkit workstream. Consumer
inventory, live deployment, and runtime/behavioral verification remain open. The
following describes its full scope; use
[consolidation status](consolidation-status.md) for the completed source checks.

- Resolve canonical skill IDs and compare repository files with chezmoi sources.
- Identify current installation consumers, including remote Hermes profiles and
  Paseo's underlying providers, and map all eight subscription/service routes.
- Compare the saved browser stash with current upstream code, chezmoi's wrappers
  and workspace, and `browser-harness-workers`; record retained, superseded, and
  historical material before importing anything.
- Capture source revisions and license/provenance before importing content.

- Import the selected specialist skills into `agent-tools/skills/`, excluding
  Jules and `toolhive-operator`. Retire the existing Jules skill and related
  prompt/reference/install/sync entries, and remove stale ToolHive distribution
  guidance. The two repositories provide six remaining distinct skill names before
  considering chezmoi's additional/current variants or role-specific selection.
- Choose a history-preserving import or a file import with an exact source-revision
  record; retain the original repository during validation.
- Leave the untracked Compound plugin checkouts out of a bulk import.
- Bring selected reusable chezmoi skill/evaluation sources and browser workflow
  instructions/helpers into the same ownership model. Compare saved browser
  customizations before choosing canonical versions. Keep package implementation
  ownership explicit and review private-source material for its intended audience.
- Update installation references for Reef and the actual Hermes/worker hosts.
  Keep client configuration minimal and apply only the selected chezmoi targets.

Completion: every selected asset has an owner, source, intended consumer, and
deployment target; each selected skill has one authoritative copy and working
references. Archiving the old repository is a later authorized GitHub action after
its consumers have migrated.

### C. Extend coverage and connect the assistant/coding workflows

**Status:** follow-on work. The early Codex smoke tests are partial evidence;
complete provider/subscription coverage is still outstanding.

1. Add dedicated Codex, then Claude, then Gemini through Antigravity/`agy`. Each
   route must authenticate through the intended subscription, complete a real
   tool-using task, and support cross-client follow-up. Then expand OpenCode Go
   and GLM coverage where the initial daily-model checks did not already cover
   them. Keep Cursor, Copilot, and Devin in the later coverage backlog.
2. Exercise selected coding skills in the coding runtimes. Separately verify
   Hermes's own capabilities and the bidirectional project/session context contract
   with Paseo. Use a shared-skill comparison only for a genuinely shared workflow.
3. Exercise one browser workflow using a named isolated profile and record which
   execution path is used from each selected client/runtime.
4. Compare additional homelab execution and an exe.dev/Daytona-style worker using
   the placement criteria below, while retaining Reef as the normal coding entry
   point. Record the integration mechanism and any limitations before adopting it.

Completion: versioned compatibility evidence and explicit gaps, including client
reconnect, tool availability, and reference-path behavior.

### D. Establish outcome evidence and trial Entire

**Status:** follow-on work; no new evaluation or Entire trial is claimed by the
backend migration checks.

- Review and port the useful parts of the existing V1 evaluation harness. Preserve
  frozen baselines; establish new expectations for selected coding runtimes and
  separate Hermes workflows rather than requiring identical skill sets.
- Compare stock and skill-assisted review on genuine bugs, context-disproved
  apparent bugs, sound code, and pre-existing user changes.
- Measure correct findings, false positives, severity accuracy, preservation of
  user work, task completion, and time/token cost. Use deterministic checks where
  possible and independent grading where judgment is necessary.
- Test skill discovery/triggering separately from the quality of a loaded skill.
- Treat repeated runs as evidence with uncertainty, not a universal quality claim.
- Refresh Entire PR #2589, validate the relevant supported integration in a
  disposable repository, and inspect local-only capture before broader adoption.
- Compare Entire with `git-ai` and existing handoff tools against specific needs;
  do not assume transcript capture is equivalent to line attribution or exact
  cross-runtime continuation.

Completion: small reproducible comparisons, actual checkpoint evidence, and a
clear account of what improved and what still fails.

## 7. Execution placement: Reef, homelab, and external workers

The target separates the device Ryan uses, the coding backend, and the machine
that executes a task. Paseo clients connect to Reef; native OpenCode clients use
the selected native connection. Reef runs work by default, with `rswift` selected
as the execution identity. Additional homelab machines and external workers are
deliberate placement options. Reef remaining the coding host does not imply Paseo
already supports every remote execution topology.

| Candidate | Role to evaluate | Evidence needed |
| --- | --- | --- |
| Reef | Default coding backend, provider runtimes, and workspaces | First-milestone connectivity, provider tasks, persistent sessions, and recoverable updates. |
| Other homelab computers | Use existing capacity for suitable builds, tests, browser work, or isolated tasks | Fresh resource/role inventory, a chosen connection/dispatch mechanism, workspace lifecycle, and results visible from the Reef-centered workflow. |
| exe.dev | External VM execution candidate | Current service capabilities, agent connectivity, persistence, browser needs, cost, and a small end-to-end task returning usable artifacts. |
| Daytona | External execution candidate | Current environment/VM/sandbox capabilities and fit, plus the same lifecycle, connectivity, persistence, and cost checks. |
| Similar providers | Alternatives if they better fit a concrete task | Compare against the same task and criteria rather than adding integrations by default. |

Use the homelab inventory as a starting map, then verify availability and competing
workloads. Beluga's documented local-inference role, for example, is a different
resource from a general execution worker. Client machines can contribute selected
capacity without becoming required daily development environments.

For a candidate worker, trace repository checkout, dependencies, tool/skill
availability, browser location, session ownership, result return, and cleanup or
persistence. Choose the simplest demonstrated connection/dispatch mechanism that
preserves the desired client experience. A custom scheduler is only justified by
an observed gap. Entire's history role is evaluated separately from VM placement.

## 8. Browser workstream

The existing work includes several distinct contracts:

1. **Upstream harness and saved customization:** CDP connection and browser
   primitives, plus the July 28 Git stash containing earlier personal guidance and
   a tab-closing helper. Compare its behavior with the newer implementations.
2. **Worker package:** persistent isolated profiles, disposable workers, approved
   authentication contexts, leases, and cleanup.
3. **Personal browser skill:** selection policy, workflow, and instructions for
   improving shared helpers/site knowledge.
4. **Deployment:** existing chezmoi wrappers and shared workspace are migration
   sources; install browser capabilities on the selected execution/browser host.
5. **Client-native browser surfaces:** OpenCode's exposed browser tools and
   Paseo's Electron browser automation/capture paths need their own compatibility
   evidence. Paseo's capture harness is not the Python Browser Harness project.

Decide which path serves each coding or Hermes workflow before writing a universal
browser wrapper. Test remote-client behavior explicitly: a browser inside a client
app and a browser on Reef or a worker are different execution locations.
Test the behavior that matters: correct target, usable logged-in context, real
screenshots/results, and cleanup after cancellation. Preserve the existing
explicit-account/profile choices when moving instructions.

Shared site knowledge is a separate source-ownership question. The current
workspace instructs agents to propose durable helpers and domain knowledge, with
review before commits or pushes. Decide where reviewed knowledge belongs and how
it is distributed independently of cookies, profiles, and task artifacts.

## 9. Decisions and remaining questions

Established decisions:

- **Identity:** `rswift` is the approved execution account. The Paseo migration is
  operating; legacy OpenCode retirement awaits the history audit and native-access
  replacement.
- **Continuity:** manual **Reload agent** is accepted for the initial setup
  (2026-10-02); automatic synchronization and shared live control are deferred.
- **Sequence and first model route:** OpenCode first, then dedicated Codex, Claude,
  and Gemini/`agy`. OpenAI OAuth with `openai/gpt-6.1-sol` is the first verified
  OpenCode route; wider subscription coverage remains to be tested.
- **Client testing:** Reef/Tortoise desktop GUI checks and remote-desktop setup are
  deferred until physical access. Marlin and Android are user-confirmed working.
- **History/archive host:** Reef is the selected canonical CASS archive host
  (2026-10-04), owned by `rswift` and searched remotely over SSH/MCP. Reconcile
  histories from all sources there. Which native copies to import or retain
  remains subject to the drift audit; existing Reef copies do not automatically
   supersede newer histories elsewhere.
- **CASS consumers:** Ryan accepted shared, agent-wide access with a Reef-first
  rollout. Register it globally in each execution runtime, beginning with
  OpenCode and verifying native/Paseo use. Remote UI-only clients need no separate
  registration; agents running elsewhere can use SSH. Registration is pending.

Open decisions:

1. **History reconciliation:** after the drift report, which unique histories and
   divergent copies should be imported, retained separately, or archived?
2. **Native remote access:** how should `opencode-reef` connect to the `rswift`
   runtime after retiring the dedicated account's listener?
3. **Additional daily models:** which remaining model/subscription routes should
   be verified next after the first working OpenAI route?
4. **Gemini integration:** which Antigravity/`agy` interface works from Reef with
   Paseo and Ryan's subscription, and what adapter work does it require?
5. **Mutual awareness:** what project/session context should Hermes and the coding
   environment exchange, how is it referenced, and what existing integration can
   carry it?
6. **Execution placement:** which homelab resources and external VM/environment
   provider should be trialed first, for which concrete workloads?
7. **Learning:** which agent-proposed skills/site helpers should be promoted into
   reviewed reusable content, and how should changes be evaluated?
8. **Maintenance:** what ongoing update/testing effort is acceptable? Choose a
   support matrix that fits that budget rather than promising every combination.

## 10. Internal design-document structure

1. The personal problem: agent behavior, tools, and context scattered across apps.
2. OpenCode-first coding on Reef, cross-device Paseo access, and the separate
   Hermes assistant role.
3. Execution identity, process ownership, session continuity, and subscription
   access, with evidence for each architectural choice.
4. Role-specific capabilities, selected shared skills, and integration contracts.
5. Homelab/cloud placement, browser execution, context exchange, and continuity.
6. Evaluation method, baselines, observed results, and limitations.
7. Maintenance costs, unresolved tradeoffs, and the implementation roadmap.

Keep this document useful for operating Ryan's setup and distinguish observed
results from design intent. Dated checkpoints and the section 6 checklist record
implementation progress; the remaining roadmap identifies unverified work.

## Sources

Local source paths above are the primary inventory evidence. Key documents:

- `dev/personal/agent-tools/README.md` and `Makefile`.
- `dev/skills/README.md` and the tracked `SKILL.md` files.
- `.local/share/chezmoi/.chezmoiexternal.toml` and
  `dot_agents/evaluations/{README.md,coverage-matrix.md,arms/README.md}`.
- `.local/share/chezmoi/dot_agents/skills/browser-harness/private_SKILL.md`.
- `dev/tools/browser-harness/{README.md,AGENTS.md}`.
- `dev/tools/browser-harness` Git stash `f6c0fd0` (`stash@{0}` when inspected),
  including the saved `SKILL.md` and `src/browser_harness/helpers.py` changes.
- `dev/tools/browser-harness-workers/README.md` and
  `docs/superpowers/specs/2026-08-06-browser-harness-workers-public-project-design.md`.
- `dev/tools/paseo/docs/{architecture.md,custom-providers.md,external-opencode-server-design.md,browser-capture-harness.md}`.
- `dev/hermes-update-2026-09-27/AGENTS.md` and
  `website/docs/developer-guide/creating-skills.md`.
- `dev/homelab/coding_pm/README.md` and
  `docs/superpowers/specs/2026-09-27-coding-pm-bot-design.md`.
- `dev/homelab/inventory.md` and `runbooks/reef-coding-services.md` (historical
  deployment/resource evidence requiring a fresh live inventory).
- Backend review and upgrade: OpenCode session `ses_f07817f6fffeLyGlLfxz3Qtj69`;
  observed Reef source at `b5b43edd6`, including `docs/providers.md` and
  `packages/server/src/server/agent/providers/opencode/{runtime-client.ts,v2/runtime.ts,paths.ts}`.
- OpenCode V2 client and local service: https://opencode.ai/v2/docs/build/client
- OpenCode V2 skills: https://opencode.ai/v2/docs/skills
- OpenCode V2 migration: https://opencode.ai/v2/docs/migrate-v1
- Entire V2 integration proposal: https://github.com/entireio/cli/pull/2589
