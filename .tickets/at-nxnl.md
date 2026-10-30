---
id: at-nxnl
status: closed
deps: []
links: []
created: 2026-10-28T18:59:25Z
type: feature
priority: 2
assignee: Ryan Swift
parent: at-iv51
tags: [crit, toolkit, review]
---
# Add Crit review support alongside Matt Pocock skills

Ryan requested Crit (https://crit.md) support on 2026-10-28 alongside the global Matt Pocock skill rollout. Treat Crit as an optional human review surface for plans/docs and code, not a replacement engineering pack or an automatic approval gate. Start with OpenCode, then assess Claude Code, Codex and Antigravity CLI. Current Reef command /usr/local/bin/crit fails because its wrapper points at the retired /home/opencode/.local/bin/crit. Inspect ownership/source before repairing. Official upstream is tomasz-tomczyk/crit and documents OpenCode skills/commands. Scope and verify a local review round and remote-client access; do not upload/share documents or expose a service without authorization. Initial rollout only records this follow-up; no Crit installation or service change yet.

## Implementation update

Crit v0.23.1 is now installed in ~/.local/bin/crit with verified upstream release
SHA-256, shadowing the stale root-owned wrapper without editing it. A manual-only
Crit skill is linked for OpenCode, Claude Code, Codex, and Antigravity CLI; no
plugin hooks, implicit CLI skill, shared uploads, or network exposure were added.
A disposable local review served HTTP 200, wrote/read a synthetic comment, and
stopped its own daemon. No human approval was simulated.

Keep open for Ryan's real Marlin-to-Reef review via SSH forwarding, comments,
Finish Review, and a revision round. Current defaults keep the server on loopback;
phone/proxy exposure needs separate authorization. See docs/global-workflow.md and
implementation ticket at-inq5.

## Notes

**2026-10-30T00:25:37Z**

Ryan approved permanent self-hosted Crit Web at https://crit.wharfi.sh, tailnet-only. Read-only verification: Reef routes wharfi.sh through Tailscale split DNS; ns.wharfi.sh is 100.89.88.31 (Lobster), existing hub.reef.wharfi.sh resolves to Reef and returns HTTPS 200; git.wharfi.sh resolves to Barnacle. Reef managed Caddy binds 100.81.54.26 and uses Cloudflare DNS-challenge certificates. crit.wharfi.sh is unresolved; stale crit.reef.wharfi.sh proxies unused 127.0.0.1:17464 and returns 502. No service/routing changes applied. Access blockers: local sudo -n -u wharfi requires a password; rswift@barnacle requires a Tailscale SSH check; wharfi@lobster has no usable login shell. Do not bypass these via another account. Next: authorized admin access, inspect DNS maintenance and intended service placement, deploy persistent PostgreSQL 17+ and Crit Web with app authentication, scoped HTTPS/DNS route, then adapt manual skill and verify hosted comment synchronization rather than assuming local blocking completion.

**2026-10-30T00:35:26Z**

Hosted installation progressed under homelab ticket hom-swpf: rootless app/database healthy on Reef loopback with persistent volume, tested dump+restore and daily backup timer. Private crit.wharfi.sh and preview.crit.wharfi.sh DNS configured/verified after Ryan approved Lobster admin SSH. Managed Caddy route prepared with preview-origin isolation and tested bearer API gate; live reload still needs Reef sudo. Registration remains closed until HTTPS ready. CLI share target/manual skill hosted protocol not switched prematurely; account, real publish/fetch and human review remain pending. Existing local review preserved.

**2026-10-30T19:38:52Z**

Verified browser-created token over HTTPS without displaying credentials; ~/.crit.config.json mode0600 and sole default crit.wharfi.sh confirmed. Updated workflow overview from SSH forwarding to hosted tailnet review and published only that file, unlisted, to https://crit.wharfi.sh/r/UBZnxatk1rVnoAh7gGG2V using explicit target and isolated output ~/.crit/hosted/agent-tools-workflow. Authenticated hosted document readback verified expected content; crit fetch succeeded with No new comments and printed review JSON path. Original local review state preserved. Manual skill now routes Reef requests to hosted protocol with explicit local branch, state isolation, no public fallback, no automatic waiter/approval inference; eleven tests and skill checks pass. Keep open pending real human comments/fetch/revision and runtime usage validation.

**2026-10-30T19:46:24Z**

Real hosted human feedback verified: crit fetch with isolated hosted root retrieved one line1 comment on docs/workflow-overview.md: This is just a test comment : ). Ryan explicitly requested closing out this review if the agent could see it; comment read and acknowledged, no document revision needed. This completes the requested human publish/comment/fetch review check. No synthetic approval, automatic wakeup, reply mutation, server archive/status update, or code-diff revision was asserted. Remaining deployment backup checks belong to hom-swpf.
