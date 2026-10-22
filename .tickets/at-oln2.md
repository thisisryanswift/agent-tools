---
id: at-oln2
status: open
deps: []
links: [at-lek9]
created: 2026-10-22T16:15:14Z
type: feature
priority: 2
assignee: Ryan Swift
tags: [cass, mcp, syncthing, tailscale]
---
# Cross-machine CASS: one Reef archive searchable from every host

Goal (Ryan, 2026-10-22): use the cass MCP on Marlin, Tortoise and Reef, all searching one central Reef archive that includes every host's sessions. Blockers for the plain SSH approach: (1) the Tailscale SSH model (homelab runbooks/acl-changes.md) puts rswift on autogroup:self in 12h check mode, per source device, so Lobster never gets unattended rswift. Reef's cass sources sync (Reef to Marlin/Tortoise) and an agent's 'ssh reef cass serve --stdio --mcp' (Marlin/Tortoise to Reef) would both stall whenever the check lapses. (2) cass 0.10's native SSH sync copies the live OpenCode SQLite DB without a consistent snapshot (noted 2026-10-04). (3) cass serve is stdio-only; there is no HTTP transport. Reef's sources.toml still lists marlin-rswift and tortoise-rswift as ssh sources pointing at frozen exports.

## Design

Options considered on 2026-10-22: (A, recommended) Syncthing collection: send-only folders on Marlin/Tortoise for ~/.claude/projects and ~/.codex/sessions (append-only JSONL), receive-only on Reef, indexed as local sources named <host>-claude/<host>-codex by the existing cass-incremental/cass-nightly timers. Skip remote OpenCode (live SQLite). Serve MCP from Reef through a small stdio-to-HTTP bridge user service behind Wharfi Caddy (e.g. cass.reef.wharfi.sh/mcp), tailnet-only, plus a bearer token because Lobster has network reach. Point the Marlin/Tortoise agent configs at it. (B) Same collection, but MCP over 'ssh reef'. No bridge, but it hangs when the 12h check lapses. (C) Relax the SSH policy to allow unattended rswift and use native cass sync. Not recommended: it removes the Lobster protection. Before building A, verify that cass indexes Claude/Codex trees from a non-default root with correct source attribution (sources add --path / mappings).

## Acceptance Criteria

From Marlin and Tortoise, an agent's cass MCP search returns sessions created on all three hosts within about 30 min of creation, with no Tailscale check prompts and no SSH policy change (unless option C is chosen explicitly). The endpoint is not reachable without credentials. Old frozen ssh sources are removed or archived from sources.toml. Decisions are recorded in docs/consolidation-status.md.

