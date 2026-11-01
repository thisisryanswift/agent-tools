# Crit sessions deployed — runtime adoption and legacy retirement pending

## Deployment progress — 2026-11-01

Ryan authorized deployment and completed the scoped sudo handoffs for Lobster's
private DNS additions and Reef's existing Caddy helper. The new router user unit
is installed through chezmoi and enabled at `127.0.0.1:17466`; the old app and
database remain active at `127.0.0.1:17465` for rollback. The permanent index
is **https://crit.wharfi.sh**, with independent per-review HTTPS hostnames.
The validation index also remains available. Root cutover was applied by Ryan
using the existing Caddy helper and verified from Reef and Marlin. The old
preview route remains available; no old service has been retired.

The initial service configuration failed cross-process identity verification:
either `ProtectSystem=full` or `PrivateTmp=true` prevents this unprivileged
service from reading separately launched daemons' `/proc/<pid>/exe`, yielding
503 review routes. Isolated systemd probes and a regression test reproduce it.
The deployed unit removes these two mount-sandbox settings while retaining
`NoNewPrivileges=true`, private state permissions, loopback backend listeners,
and all daemon identity checks. Automatic approval review rejected applying
this candidate without explicit authorization for the broadened access. The
running unit was initially unchanged. Ryan then explicitly approved this exact
two-setting change after reviewing the risk explanation. It was applied through
chezmoi, and only the router was restarted. All five review HTTPS routes now
verify correctly; the real systemd regression passes. The full suite passes
34 tests, including this new boundary test.

From Marlin, trusted HTTPS checks passed for four synthetic reviews: Git and
document identities and comments, promptly streamed Finish events, independent
local waiter delivery, and targeted daemon restart retaining URLs/comments.
Ryan supplied real feedback in the separate fifth document review; it reached
the intended waiter with unresolved feedback. That same review has advanced to
round two, with its prior comment retained and a visible revision marker;
Ryan's second comment and Finish arrived at the same review ID. He also confirmed
the remote Git diff UI and supplied a screenshot. Saved review resume through
the permanent HTTPS index, unknown-host rejection, and router restart preserving
all five daemon identities also passed. These observations are
remote HTTP and real human-browser evidence, not a claim of automated browser
coverage: Reef's browser-harness wrapper cannot start without Chrome installed.

Rollback copies of the prior Caddy source/rendered configuration and ignore
template are under the private deployment state directory. A fresh existing
backup job succeeded at 16:08:17 UTC; its mode-0600 custom archive passes
`pg_restore --list`. A disposable restore exactly matched all 7 reviews,
20 comments, and 44 round snapshots. A temporary instance of the pinned old
app, with background jobs disabled, passed health, existing-token identity,
historical review/comment readback, login-page, and closed-registration checks.
Only that temporary app container and its private temporary environment file
were removed. The named fixture database remains for recovery evidence.
Ryan ran the existing off-host backup and selective restore verifier. Snapshot
`deebaa684fc56b069dd67d1622580ce66a3f592689543182bfd9ae66a15383c8`
at `2026-11-01T11:25:10.12085755-05:00` restored seven recovery files to a new
root-private scratch location; every byte matched, including dump SHA-256
`e74323ae51062cef2835a6b301296d4207063c12b644e0ea8d3b8fc991057b80`.
The installed root backup script now also includes independent review state
and the router user unit. It matches the updated source exactly; that addition
extends future backup coverage and does not claim a newer restore verification.

The independent-session protocol is **activated**. All four Reef instruction
files were reapplied through chezmoi with unrelated bytes and Gemini memories
preserved; all four skill discovery paths resolve to the shared updated manual
skill. This Codex conversation exercised the real launcher/comment/round loop.
Fresh end-to-end invocation in OpenCode, Claude Code, and Antigravity CLI remains
pending; link/render verification is not equivalent to running those workflows.
Keep legacy services and data intact until these remaining adoption checks and
the separately recorded retirement step complete. The epic remains open.

Ryan explicitly accepted the risk recorded in the earlier token incident and
instructed leaving the hosted Crit API token unchanged. Rotation is not a gate
for this deployment; preserve the credential.

## Initial preparation record

Prepared from at-sxgj, at-7193, at-5ftr, `docs/crit-multi-session-research.md`,
`~/dev/homelab/reef/crit-web/README.md`, and the inspected chezmoi Caddy source.
The snippets in `deploy/crit-reviews/` contain proposals only.
At the initial preparation stage, no live DNS, Caddy, user services, global
instructions, database, secrets, or historical reviews were modified. Neither
remote HTTPS nor human review has been verified by this preparation.

## Ownership and gates

Local preparation evidence (2026-11-01): the synthetic DNS zone passes
`named-checkzone`; the prepared unit passes `systemd-analyze --user verify` when
run with access to the user manager. Caddy is absent from this account's PATH,
so full candidate adaptation and certificate checks were then pending. The existing
Crit Web app, database and backup timer are active; the app still publishes only
127.0.0.1:17465. Four mode-0600 dumps were found and their table-of-contents
checks pass. The latest is `crit-20261101T073003Z.dump` (99,324 bytes), SHA-256
`df328b48b16664388251be4c4e88ec34e33b38a897da78c15eeedc158db73920`.
These checks do not establish a fresh restore or off-host recovery. No old
service has been stopped. Remote HTTPS, real human review, runtime adoption,
cutover and recovery gates below were all pending in the preparation record.
Current activation and remaining checks are recorded in the deployment section
above; this historical preparation state does not override that evidence.

The local implementation and review results are recorded in
[the validation report](crit-sessions-validation.md). Synthetic browser tests
completed a comment/Finish/revision loop on disposable local reviews. They are
separate from the required real remote human loop below.

Full validation and cutover Caddy candidates were prepared outside the repo from
the existing source (SHA-256
`26945d2f038cae8b3d82f3aa7ed59aa4d6237361ba3e307ffb8593dc1de6be8f`).
Read-only adaptation through the existing admin socket was attempted, but
`sudo -n -u wharfi` requires a password. No request reached the Caddy admin API;
adaptation must be completed in the operator's authenticated terminal. No load
endpoint was called.

A router test accidentally reached the share endpoint before its deny rule was
implemented; its response was 502. A subsequent read-only transaction found
7 hosted reviews and 20 comments, with latest review creation at 13:34:43 UTC and
latest review/comment update at 14:28:07 UTC, before the estimated 15:22–15:23
UTC test window. No test-period hosted write was observed. Tests now pin sharing
to a loopback sink, and the router denies sharing endpoints. The same subagent
exposed a saved hosted API credential in tool output. **Rotate the affected Reef
CLI token before relying on it again** was the original recommendation; Ryan
subsequently directed leaving it unchanged, as recorded above. No credential
was changed automatically.
Do not copy credentials or the private transcript into this repository.

Review the final launcher command and registry layout against the implemented CLI
before installation. Expected router command is
`python3 ~/dev/personal/agent-tools/scripts/crit-review.py --binary ~/.local/bin/crit serve --port 17466 --index-host validation.crit.wharfi.sh`,
listening only at `127.0.0.1:17466`, using durable registry
`~/.local/share/crit-reviews`. Daemons must also listen only on loopback.
Crit stays pinned to installed v0.23.1. Internal daemon compatibility tests must
pass before deployment. Do not change HOME or replace the installed binary.

Live deployment, DNS administration, global workflow edits, and cutover require
session authorization. Test-seam approval covers prepared configuration checks;
it does not assert approval for those external changes. Resolve at-7193 only when
its real remote acceptance checks pass, and at-5ftr only when workflow adoption,
human loop, preservation, recovery, and cutover checks pass.

## Preserve and prove recovery before cutover

1. Read-only inventory the exact `crit-web.service`, `crit-web-db.service`,
   `crit-web-backup.service`, `crit-web-backup.timer`, their Quadlet sources,
   image digests, database named volume/network, configured dump retention,
   current signing/app/database secrets locations and modes. Do not print secret
   values, environment files, full container inspection, or credentials.
2. Record hosted review IDs, owners/visibility, titles, comment counts, and
   recoverable content privately; include the known historical
   `/r/UBZnxatk1rVnoAh7gGG2V` and independent pre-existing reviews. Authorized
   authenticated export or DB queries must be read-only. Do not place real
   review content or secrets in this repo or public artifacts.
3. Run the existing backup service only after operational authorization. Require
   a fresh successful PostgreSQL custom-format dump and `pg_restore --list`.
   Record dump checksum, timestamp and size without revealing data. Verify
   signing secret, app/database credentials, Quadlets and required pinned images
   are recoverable. Preserve all pre-existing dumps and volumes.
4. Verify a real off-host restic backup includes dump, private secrets and unit
   definitions, with a successful snapshot and a restore into a private scratch
   location. Existing README evidence does not prove current off-host coverage.
5. Restore the fresh dump with PostgreSQL 17 `pg_restore --exit-on-error` into a
   newly named disposable database, never over the live DB and never `--clean`.
   Run an isolated old-app instance bound to a separately selected free loopback
   port, using preserved configuration without exposing secrets. Check login,
   historical content and comments against the inventory, and registration stays
   closed. Preserve signing-key behavior. Record exact evidence privately.
   Stop only this recovery fixture afterwards; removing fixture resources needs
   their ownership confirmed. A table-of-contents check alone fails this gate.
6. Record an executable restore/rollback procedure with paths and backup IDs in
   private operator notes. Do not stop old services until this gate and remote
   replacement validation both pass. Keep historical review data recoverable;
   the new CLI index does not migrate old Crit Web URLs/content.

## Prepare and validate the router service

Inspect the repository script and CLI help, then create the registry directory
mode 0700 before applying the unit. Install the prepared unit through the chosen
existing user-unit ownership convention, preserving any pre-existing conflicting
unit and refusing to replace it blindly. On Reef validate with
`systemd-analyze --user verify <prepared-unit-path>` before install; then, only
after authorization, `systemctl --user daemon-reload` and enable/start this one
unit. Confirm rswift's existing lingering manager; do not change unrelated units.
The initial proposed mount sandbox proved incompatible with peer-process
verification on Reef; follow the deployment progress section for the explicit
authorization and tested unit settings. The unit is not intended to isolate
repository read/write access from the user.

The unit uses `KillMode=process`: stopping/restarting the router leaves review
daemons alive, including those resumed through its index. Review shutdown remains
an explicit, targeted launcher operation. Retain the registry and output paths.

Check `ss -ltn` for 127.0.0.1:17466 and every Crit daemon port, with no 0.0.0.0,
::, LAN, or tailnet-bound backend. Loopback `curl` with Host `crit.wharfi.sh`
should show the index; known review Host should show only that review; unknown
Host, stale PID/port, stopped reviews and malformed IDs must fail safely.

## Private DNS addition on Lobster

The live private CoreDNS file-plugin zone is
`/home/wharfi/.config/coredns/db.wharfi.sh`; it has no known chezmoi source. Use
its existing administration owner/convention. Existing `add-private-dns.py` is
reference only: it adds old explicit records and must not be rerun as though it
adds wildcard routing. Merge `private-zone-additions.txt`, preserving existing
`crit`, `preview.crit`, shared wildcards and all other records.

Under a serialized DNS maintenance window (or a shared lock respected by every
writer), snapshot the live bytes, owner/mode and SOA serial and make a private
rollback copy. Reject symlinks, unexpected origin/SOA format, and conflicting
existing wildcard/validation records or CNAMEs. A matching record is a no-op.
Stage in the same directory. Advance the SOA to a valid 32-bit serial greater
than the current serial under RFC 1982 ordering (normally current+1 or today's
YYYYMMDD01, whichever is larger; abort near wraparound for operator review).
Run `named-checkzone wharfi.sh <staged-file>`. Immediately before atomic rename,
compare live bytes with the original snapshot; abort on any concurrent edit and
rebase from fresh bytes. Preserve ownership/mode and fsync the stage and backup,
then atomically rename and fsync the directory. Do not restart shared CoreDNS;
wait its configured file-plugin reload interval and account for resolver caches.

From a separate tailnet device, query the configured private resolver for a
fresh opaque-ID hostname and validation.crit.wharfi.sh; both must return only
100.81.54.26. Check existing Crit, preview and unrelated records still resolve.
Public DNS must not gain A/AAAA review records; DNS challenge TXT is expected.
For rollback, use the same concurrency and validation procedure to remove only
the additions and increment the live serial again. Never overwrite a newer zone
with the old rollback bytes/serial; merge intervening legitimate edits.

## Caddy validation phase — old root remains live

Source of truth is chezmoi
`~/.local/share/chezmoi/dot_config/homelab/reef/Caddyfile.wharfi`; verify with
`chezmoi source-path ~/.config/homelab/reef/Caddyfile.wharfi`. Prepare a source
diff that appends `validation.Caddyfile` while preserving the complete existing
source. The explicit old preview host continues to take precedence over the
wildcard. The router explicitly permits the validation index hostname in addition
to the root hostname. Preserve Host on both routes so same-origin browser actions
and Crit's rebinding check see the actual requested hostname.

Validate the full candidate with Reef's actual Caddy binary including its
Cloudflare module. `caddy adapt --config <candidate> --adapter caddyfile --validate`
or `caddy validate` must run in the established service credential context;
never echo/copy the Cloudflare API token or service environment into logs.
Use `caddy list-modules` to confirm `dns.providers.cloudflare`. Formatting and
adaptation alone are not live certificate or reachability evidence. No rewrite,
compression or buffering should interfere with SSE; `flush_interval -1` is set.

Only after validation and authorization apply the scoped chezmoi target and use
existing `apply-reef-caddy` (managed wharfi service/admin socket) to reload.
Preserve the previous complete source and rendered file in private operator
backup. Do not start another Caddy service or replace unrelated configuration.
Verify valid trusted TLS for validation and multiple fresh review hosts from a
remote tailnet browser; wildcard *.crit.wharfi.sh covers one label only. Verify
old root login/health and preview remain available and unrelated routes work.
No Funnel, public listener, public record, SSH tunnel or laptop callback is used.

## Remote replacement validation matrix

Create disposable synthetic fixtures through the launcher: five identities on
one checkout/branch (include Git and document scopes), each with its own URL,
output root and stable conversation mapping. Record IDs and timestamps privately.
From a second tailnet-connected device with no forwarding, open all five HTTPS
URLs and the validation index. Check correct labels, branches, rounds, activity,
shared-checkout notice, and direct deep links. An ID is not an auth secret; the
tailnet is the boundary.

For each URL, add a uniquely labeled SYNTHETIC comment in the real browser UI
and verify targeted launcher feedback only contains its own marker. Observe
SSE updates promptly. Keep four Finish waiters pending while finishing the fifth;
only the matching conversation must release. Advance a revision through the
launcher and verify changed content in that round, stable identity, prior
comments and a second comment/Finish cycle. Other reviews need not refresh
shared-checkout content until their own round transition; isolation does not
claim independent authorship.

Restart one selected daemon via the launcher, reconnect its browser, and verify
comments/state survive while the other four remain routed and waiting. Restart
the router and verify durable saved/inactive state and safe resume. Probe
unknown IDs, wrong Host, inactive reviews, unavailable ports and stale/reused
PID/port; never route to another daemon. Add/remove another fixture and verify
reachability without DNS edits or Caddy reload. Record evidence for valid TLS,
streamed responses, reconnect and failure states; local HTTP tests do not satisfy
this matrix.

Run a separate real human review: Ryan opens a targeted URL, supplies an actual
comment, selects Finish, the intended agent receives it, a revision is prepared,
and Ryan reviews the subsequent round. Record human versus synthetic provenance
explicitly. Empty comments, connectivity, HTTP success and synthetic Finish are
not human approval or permission to implement/commit/publish other work.

Before resolving workflow adoption, explicitly invoke the updated Crit workflow
in OpenCode, Claude Code, Codex and Antigravity CLI; record each stable runtime /
conversation mapping and later-round targeted feedback. Generic review requests
must not activate Crit. Ambiguous targeting must fail, and unsupported live/HTML
preview modes must explain the limit without fallback uploads.

## Separate root cutover and retirement

Require remote matrix, real human loop, runtime adoption and recovery gates,
then prepare a fresh full Caddy diff using `cutover.Caddyfile`. Replace only the
old combined root/preview block, retain wildcard and unrelated routes. Validate
and authorize using the same source/apply convention. Root now serves index;
verify old per-review replacement URLs still work and unrelated services remain
healthy. The legacy preview route can remain while the old app runs.

Before old-app retirement, switch preview's handlers to the prepared explicit
410 response so it never silently falls through to the review wildcard. Record
how historical content is recovered from the verified archive; old /r/* hosted
links are not equivalent to new per-review CLI URLs. Only then stop the identified
`crit-web.service` and `crit-web-db.service`. Inspect the backup timer: stopping
those services may cause scheduled dump failures. Either keep a working archive
backup plan or, with separate authorization, disable only the identified backup
timer after final successful backup and verified off-host retention. Do not delete
its unit, DB volume, credentials, exports, dumps, images, historical reviews or
unrelated local Crit daemons. Retain rollback until explicitly released.

## Rollback and evidence

If validation fails, restore only the appended Caddy routing changes using a fresh
source merge, validate and apply; retain root/preview untouched. Stop only the
new router if needed; do not stop independent review daemons. DNS wildcard can
remain harmlessly during diagnosis, or remove only additions with a newer SOA.
For failed cutover, start the exact old DB then app units if previously stopped,
verify old loopback health, restore the old combined Crit Caddy block (including
bearer forward_auth), validate/apply and verify root login, historical reviews
and preview from a remote tailnet device. Preserve wildcard review routes if
still used. Re-enable the backup timer only if it was intentionally disabled.
Do not restore over the original DB if it is intact. A full disaster recovery
restore follows the tested empty-database procedure and needs separate operator
authorization. Merge any intervening unrelated source/DNS edits during rollback.

Keep an evidence table with check, expected outcome, actual observation,
fixture/human provenance, timestamp and reviewer. Mark not-run checks pending;
no local artifact validation is remote deployment or human evidence.
