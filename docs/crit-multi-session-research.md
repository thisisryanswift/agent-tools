# Crit multi-session remote routing investigation

Investigated 2026-11-01. This is a research note, not an implementation spec or deployment authorization. Source inspection and runtime testing use the installed Crit **v0.23.1**, upstream revision `ad3e10fbc864ca613eb084cf9a7b23c25f5317b3`. The exact release source was fetched into `/tmp/crit-investigation-v0231`; current main was inspected separately for comparison.

## Verified from upstream source

### Remote code/file review routing

`--public-url` advertises a browser URL without changing the listener address. Its hostname is permitted by the server's Host check, so a proxy can retain the external Host header while forwarding to a loopback listener. This avoids disabling the DNS rebinding check. Any configured public URL requires the explicit `--allow-unauthenticated-network` acknowledgment in this source version; Crit itself supplies no network authentication. [Host validation](https://github.com/tomasz-tomczyk/crit/blob/ad3e10fbc864ca613eb084cf9a7b23c25f5317b3/internal/server/server.go), [network exposure contract](https://github.com/tomasz-tomczyk/crit/blob/ad3e10fbc864ca613eb084cf9a7b23c25f5317b3/internal/config/network.go).

An optional path prefix is preserved when constructing advertised links, but this is not complete application subpath support: server handlers live at `/api/*`, `/live`, `/preview`, and `/preview-content`, and the browser fetches root-relative `/api/*` endpoints and opens SSE at `/api/events`. A prefix-stripping proxy alone cannot fix those browser requests. **Inference:** dedicate one hostname per review rather than route reviews under `/session-id/`; path routing would require application changes or fragile response rewriting. [Advertised URL construction](https://github.com/tomasz-tomczyk/crit/blob/ad3e10fbc864ca613eb084cf9a7b23c25f5317b3/internal/daemon/daemon.go), [server routes](https://github.com/tomasz-tomczyk/crit/blob/ad3e10fbc864ca613eb084cf9a7b23c25f5317b3/internal/server/server.go), [browser API calls](https://github.com/tomasz-tomczyk/crit/blob/ad3e10fbc864ca613eb084cf9a7b23c25f5317b3/web/app.js), [SSE](https://github.com/tomasz-tomczyk/crit/blob/ad3e10fbc864ca613eb084cf9a7b23c25f5317b3/web/app.js).

### Conversation isolation is not provided by `--output` alone

The Git-mode session key hashes resolved working directory and branch; file-mode keys hash working directory and sorted file arguments. `--output` does not enter that formula. The registry lives in `~/.crit/sessions/`, independently of the review output root. Startup reconnects to an existing daemon for the key before starting another. Therefore two conversations with the same checkout and review scope reconnect even if they request different output roots. [Identity and registry](https://github.com/tomasz-tomczyk/crit/blob/ad3e10fbc864ca613eb084cf9a7b23c25f5317b3/internal/daemon/daemon.go), [reconnection](https://github.com/tomasz-tomczyk/crit/blob/ad3e10fbc864ca613eb084cf9a7b23c25f5317b3/internal/session/review_cli.go).

Explicit output does isolate stored review data under `<root>/reviews/<key>/`, but it does not solve the registry collision. Headless commands can explicitly target a live session with `--session`; that flag cannot be combined with `--output`. [Review path resolution](https://github.com/tomasz-tomczyk/crit/blob/ad3e10fbc864ca613eb084cf9a7b23c25f5317b3/internal/review/review_file.go).

The internal `_serve` configuration has a hidden `--session-key` override, and the daemon honors it. This is an internal seam, not evidence of a supported public create-independent-session command. A wrapper relying on it must pin and test the CLI version, including how review identity, later commands, reconnect, and shutdown behave. [Internal flag](https://github.com/tomasz-tomczyk/crit/blob/ad3e10fbc864ca613eb084cf9a7b23c25f5317b3/internal/server/daemon_cli.go), [override use](https://github.com/tomasz-tomczyk/crit/blob/ad3e10fbc864ca613eb084cf9a7b23c25f5317b3/cmd/crit/cli_serve.go).

### Code/file reviews, preview, and live review differ

Static HTML preview is served from `/preview-content` on the same origin as the CLI API; injected scripts also use root-relative URLs. It does not inherit Crit Web's separate preview-host arrangement. [Preview handler](https://github.com/tomasz-tomczyk/crit/blob/ad3e10fbc864ca613eb084cf9a7b23c25f5317b3/internal/server/preview_handlers.go), [browser origin selection](https://github.com/tomasz-tomczyk/crit/blob/ad3e10fbc864ca613eb084cf9a7b23c25f5317b3/web/live-mode.js).

Live app review uses a separate proxy listener. The browser currently computes its iframe origin as `http://<window.location.hostname>:<session.proxy_port>`; it does not use `--public-url` to advertise a separate HTTPS iframe origin. **Inference:** proxying just the main CLI port over HTTPS will not make live app review remotely functional: it points at a raw HTTP port and risks mixed-content blocking. Treat live mode as a separate integration requiring verification and likely upstream changes for a configurable HTTPS proxy origin. The iframe has no sandbox attribute by design. [Iframe origin](https://github.com/tomasz-tomczyk/crit/blob/ad3e10fbc864ca613eb084cf9a7b23c25f5317b3/web/live-mode.js), [iframe construction](https://github.com/tomasz-tomczyk/crit/blob/ad3e10fbc864ca613eb084cf9a7b23c25f5317b3/web/live-mode.js), [two ports](https://github.com/tomasz-tomczyk/crit/blob/ad3e10fbc864ca613eb084cf9a7b23c25f5317b3/internal/live/live.go).

## Existing deployment evidence (local documentation only)

Read-only inspection of `/home/rswift/dev/homelab/reef/crit-web/README.md` records:

- Crit Web and PostgreSQL run under Reef's lingering user manager, with app port `127.0.0.1:17465`.
- Private `crit.wharfi.sh` and `preview.crit.wharfi.sh` names resolve to Reef's tailnet IP `100.81.54.26`.
- Caddy binds the tailnet address and already uses Cloudflare DNS challenges; authoritative Caddy source is chezmoi's `dot_config/homelab/reef/Caddyfile.wharfi`.
- Crit Web's preview hostname separates preview scripts from the application's login session.
- The private DNS zone on Lobster currently has explicit Crit names; wildcard review DNS would be a new change.
- Existing database, credentials, backups, and published reviews need preserving if the web app is retired.

These are documented installation claims, not fresh runtime checks. No remote configuration or services were changed during this research.

## Proposed minimal architecture

1. Keep `crit.wharfi.sh` as the entry page; use `<opaque-review-id>.crit.wharfi.sh` for each code/file review. Add private wildcard DNS to Reef and a wildcard certificate via the existing DNS challenge setup.
2. Use one permanent Caddy wildcard route to a small loopback routing service. That service validates the hostname against an explicit registry, forwards only to approved loopback daemon addresses, preserves the original Host header, and supports SSE streaming. Unknown/stopped review IDs return an explanatory page, never an arbitrary host/port proxy.
3. Let the launcher create a durable conversation-to-review mapping, display project/branch/checkout metadata, allocate/start the daemon, and register its loopback port and public URL only after health verification. The entry page lists active reviews; stale entries become inactive. Retain review state independently of daemon lifetime.
4. Use a launcher pinned to v0.23.1 that assigns a stable 12-character hex session key and starts `_serve --session-key <key>` with its own output root. This internal interface passed the isolation experiment below; it remains an integration dependency to check before upgrades. A public session-ID creation flag would be preferable long-term. Separate `--output` values alone are insufficient. Do not override `HOME`: it also changes Git/config/credentials behavior.
5. Keep all daemon and router listeners on loopback, with Caddy reachable only on the tailnet. Review IDs identify sessions; they are not authentication credentials.
6. Initially scope the integration to code/file diff reviews. Validate preview explicitly; live app review needs separate HTTPS proxy-origin work.

This design keeps session changes out of Caddy's privileged configuration and avoids reloading it for every new review. It is proposed integration work, not a feature already built into Crit.

## Runtime results on Reef

Ran the installed `/home/rswift/.local/bin/crit` v0.23.1 against a disposable local clone of the release. All five daemons used **the same checkout and branch in Git diff mode**, distinct internal session keys, distinct output roots, random loopback ports, and distinct `--public-url` hostnames. No `HOME` changes, new commits, live service changes, or uploads were made. Stats were disabled in the fixture. Synthetic comments and Finish events applied only to these temporary reviews.

The following checks passed:

- Five simultaneous daemons had distinct ports and Git-mode identities.
- Review comments and persisted review files stayed separate.
- `crit comment --session <key> <body>` wrote only to the chosen review; its live daemon reflected the change after the asynchronous watcher ran.
- Each daemon accepted its advertised hostname and rejected an unrelated non-loopback hostname with HTTP 403.
- The browser SSE endpoint flushed its initial event bytes and delivered the Finish event.
- Finishing review A released A's waiting `/api/review-cycle` request while B–E remained blocked. Their later feedback retained their own comments and `crit --session <key>` next-round command.
- Stopping and restarting A through the test launcher with the same key/output/public URL preserved comments; B–E remained running.
- Advancing B to a second round kept its identity and feedback and picked up a subsequent shared-checkout file edit.
- Every test-owned session registry entry was absent after cleanup; all temporary daemons were stopped.

One deliberately broader check **did not pass**: all five `/api/file` responses did not immediately converge to the latest shared file content, even after four seconds. In that experiment only B, explicitly advanced to its next review cycle, returned the new marker; the others still returned their previous content. Treat each review's content as governed by its own refresh/round lifecycle, rather than promise a continuously synchronized view. This does not isolate authorship: refreshing a review against a shared checkout can still include any agent's changes.

The final test harness and full results remain temporary investigation artifacts at `/tmp/crit-session-investigation.py` and `/tmp/crit-five-reviews-hy_mzeg_/results.json`. The latter exits nonzero for that all-sessions-content expectation while the isolation, targeting, restart, SSE, and second-round checks pass. The earlier isolation-only run at `/tmp/crit-five-reviews-stu5qpj6/results.json` passed all its assertions. These paths are disposable, not deployment dependencies.

## Remaining implementation checks

No production router, wildcard DNS, certificate, or browser end-to-end test has been created. Direct loopback requests with the external Host header verify Crit's side of proxy compatibility, not end-to-end Caddy behavior. Implementation should test SSE buffering/disconnection, concurrent registration, stale port/PID reuse, launcher restarts, unknown/inactive routes, and actual HTTPS access from a remote client.

The launcher must persist key, scope, cwd, output root, and public URL and own daemon restart. The registry entry is removed on clean stop; bare `crit --session <key>` cannot be relied on to rediscover a custom output root after that removal. Once the launcher recreates the daemon, explicit `--session` targeting can reconnect normally. [Reconnect path lookup](https://github.com/tomasz-tomczyk/crit/blob/ad3e10fbc864ca613eb084cf9a7b23c25f5317b3/internal/session/session_reconnect.go).

Keep code/file diff review as the initial scope. Preview and live mode need their own verification. Preserve the existing Crit Web reviews, database, credentials, and backups until a replacement has passed remote HTTPS testing; no migration or retirement was performed here.
