# Global tracker defaults and manual Crit

## Hosted Crit — current state

Ryan subsequently approved Crit Web on Reef at `https://crit.wharfi.sh`,
tailnet-only, replacing the need for SSH forwarding for hosted reviews.
The rootless app and PostgreSQL are healthy on loopback behind tailnet-bound
Caddy, private DNS, and HTTPS. Ryan created a local account; registration is now
closed. The browser-created API token was verified and saved in Reef's mode-0600
CLI config with `crit.wharfi.sh` as the sole default. Device-code login is
OAuth-only in the pinned web release, so local accounts use API Tokens from
Settings and the hidden-input importer in `~/dev/homelab/reef/crit-web/`.

The workflow overview is published at
<https://crit.wharfi.sh/r/UBZnxatk1rVnoAh7gGG2V>. Authenticated document readback
and `crit fetch` succeeded. Ryan's real test comment was fetched and acknowledged;
he explicitly closed the review with no document revision needed (`at-nxnl` closed).
This verifies publication/comment/fetch, not an unperformed revision or automatic
notification loop. Hosted state is isolated under `~/.crit/hosted/agent-tools-workflow`,
with the original loopback session preserved.
The manual skill now routes to [the hosted protocol](../skills/crit/references/hosted.md)
by default on Reef; explicit local reviews retain their separate protocol.

Deployment and remaining checks are tracked as `hom-swpf` in `~/dev/homelab`,
with details in `reef/crit-web/README.md`. Its daily dumps have been restore-tested;
the updated root restic script is installed, but actual off-host coverage still
needs verification. The initial local rollout record below is historical where
it differs from this hosted state.

The global instruction templates and current docs now name the hosted target
explicitly, with local mode only for explicit local requests. Only the four live
instruction targets on Reef were reapplied; credentials and services were untouched.

Implemented on Reef for Ryan's OpenCode, Claude Code, Codex, and Antigravity CLI
execution account. This is shared global policy, not a project-local pilot.
Existing repositories were not bulk-migrated or given duplicate setup files.

## Tracker source of truth

The canonical [workflow guide](../workflows/matt-workflow.md) is linked by chezmoi
to `~/.config/agent-tools/matt-workflow.md`. Both OpenCode's managed instructions
and the shared Claude/Codex/Gemini instruction template direct agents to read it
for tracker/spec/triage/wayfinding work.

The guide supplies Matt's missing tracker context globally: honor an established
project tracker, otherwise use `tk`. GitHub remotes do not opt projects into GitHub
Issues. Specs live in tracker tickets; `.scratch/` and `docs/specs/` are not
mandatory. Child tickets use real parent IDs and `tk dep` relationships. Triage
roles can be tags without replacing `tk`'s lifecycle states. Do not add tags or
initialize tickets on every exploratory turn. Ordinary authorization boundaries
remain in force.

This is a prompt adapter over native `tk`, not an enforcement service or an atomic
multi-agent claim system. A project's explicit tracker/config overrides the
default. Its own glossary/ADR conventions are unchanged. Project-specific setup
is available when requested, not a prerequisite for using these defaults.

Managed sources changed:

- `~/.local/share/chezmoi/.chezmoitemplates/agents.md`
- `~/.local/share/chezmoi/dot_config/opencode/AGENTS.md.tmpl`
- `~/.local/share/chezmoi/dot_config/agent-tools/symlink_matt-workflow.md.tmpl`

Only the global guide directory and four relevant instruction files were applied.
Gemini's existing added-memory section was preserved. The symlink requires this
canonical checkout at `~/dev/personal/agent-tools`; a different host layout needs
an explicit deployment adjustment. No other host was modified.

## Crit deployment

Installed the upstream Linux amd64 release **v0.23.1** into
`~/.local/bin/crit`, which precedes `/usr/local/bin` on Reef. The root-owned
`/usr/local/bin/crit` wrapper still references the retired account; it was neither
edited nor deleted. There was no existing user binary to overwrite.

Release: <https://github.com/tomasz-tomczyk/crit/releases/tag/v0.23.1>

Asset: `crit-linux-amd64`, verified against the GitHub release asset digest:

```text
309e086e488a2c37a11760aefb78d2d6089ebcf21a6447adba4360ae850e5c0d
```

The MIT-licensed upstream protocol is adapted in [our manual Crit skill](../skills/crit/SKILL.md),
with the notice retained. Whole skill directories are linked to the existing four
discovery roots through `scripts/install-skills.py`. Claude's `~/.claude/skills`
is already an alias of `~/.agents/skills`, so those two paths share one link set.
No marketplace install, lifecycle hook, runtime permission change, or automatic
`crit-cli` skill was added. The hosted CLI configuration stores credentials outside
the repository as described above. Matt's pinned source checkout is unchanged.

Invocation:

- OpenCode: `@crit .tickets/<id>.md`
- Claude Code / Antigravity CLI: `/crit .tickets/<id>.md`
- Codex: `$crit .tickets/<id>.md` (or select Crit from the skill picker)

A generic review request does not activate Crit. OpenCode/Claude manual frontmatter
and Codex's `allow_implicit_invocation: false` are supplied; the explicit-request
rule also applies on runtimes that do not enforce those fields identically.

The original local-only skill ran on `127.0.0.1` with SSH forwarding from Marlin.
That protocol remains available for explicit local requests; the current default
is the approved self-hosted target described above. Approval still does not grant
permission to implement, commit, or publish beyond the requested review.

## Verification and remaining human check

- The unit suite exercises native `tk` create/spec/parent/dependency/ready/blocked/
  start/note/close/reopen behavior in an isolated `TICKETS_DIR`. It confirms no
  `.scratch`/spec directory appears and children do not auto-close their parent.
- Contract tests check Crit's explicit-invocation metadata, hosted protocol,
  explicit-local flags, and current documentation's hosted-target agreement.
- OpenCode's live registry sees canonical `crit` with `autoinvoke: false` after a
  location reload; no service restart was used. Codex's live `skills/list` sees it
  exactly once as `crit`. All four installed links resolve to the same canonical
  source. Claude/Antigravity invocation still needs a real user review rather
  than invoking the review skill just to test installation.
- A disposable Crit fixture served HTTP 200 on loopback, wrote/read a synthetic
  session-scoped comment, and stopped only its own daemon. No browser was opened,
  human completion simulated, or approval asserted. Evidence remains under
  `/tmp/opencode/crit-smoke-p7ve0sxs` until temporary-file maintenance.
- Crit v0.23.1 requires relative paths for file comments and subcommand-first
  argument ordering; those findings are captured in the skill protocol.

The real human publication/comment/fetch check is complete by Ryan's explicit
decision. A content revision was unnecessary for his test-only comment and was
not exercised. Agent replies/re-sharing revisions, automatic notifications, and
full cross-runtime parity are not established by that test.

`make check` passes (8 personal skills, 2 prompt copies), `make test` passes
(12 tests, including native tk and manual/hosted-Crit contracts), and scoped chezmoi
verification covers the guide link plus all four instruction targets.
