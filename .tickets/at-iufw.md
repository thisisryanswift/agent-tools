---
id: at-iufw
status: closed
deps: [at-zphe]
links: []
created: 2026-11-01T15:06:47Z
type: feature
priority: 2
assignee: Ryan Swift
parent: at-sxgj
tags: [crit, ready-for-agent]
---
# Route each Crit review through its own hostname

Connect registered review hostnames to the launcher-managed loopback daemons through one local routing service. Opening a hostname must load the correct full Crit UI and preserve API calls, assets, comments, and server-sent events across concurrent reviews. Demonstrate this on loopback before production DNS/Caddy changes.

Routes come only from the trusted local launcher registry. Preserve the external Host header to match Crit's configured public URL. Never accept a caller-supplied arbitrary upstream host/port. Validate daemon identity and generation so stale registration or reused ports cannot expose a different process. Unknown, stopped, and failed reviews must have explicit inactive/error behavior. Support changing daemon ports after restart without changing review URLs.

The service and all daemons remain on loopback. Use the installed pinned binary without upstream changes. Keep path-prefix routing, live app mode, and HTML preview outside scope.

## Acceptance Criteria

- [ ] Five review hostnames load their own UI, files, comments, and API state concurrently through the router.
- [ ] Streamed events are flushed promptly without buffering; finishing one review reaches only its waiting client.
- [ ] Browser/event-stream disconnects release upstream resources, and one inactive daemon does not block other reviews.
- [ ] Restarting a review updates its loopback target while its hostname remains stable.
- [ ] Unknown or malformed hostnames, inactive records, and stale/reused ports cannot proxy arbitrary or unrelated processes.
- [ ] Registration and lookup remain correct during concurrent launch/stop operations.
- [ ] Local integration tests exercise real Crit responses and completion streams without production DNS or proxy changes.


## Notes

**2026-11-01T15:28:04Z**

Implemented loopback routing on implement/at-sxgj (uncommitted). Merger ran 7 real pinned-Crit HTTP integration tests: five hostname UIs/files/comments; prompt SSE/non-advancing completion isolation; idle disconnect resource release; stopped/restart/stale reused-port routing; exact hostname/origin-form/framing boundaries; restricted scope/lifecycle/upload/agent/trust APIs. All pass in 7.280s; zero test-owned daemons left. Daemon Host retained, registry generation/socket checked before and after connection. No DNS/Caddy/deployment changes. See docs/crit-review-launcher.md. Test share incident and token exposure documented in docs/crit-sessions-operations.md; hosted read-only inventory found no fixture publication.
