---
id: at-zphe
status: closed
deps: []
links: []
created: 2026-11-01T15:06:47Z
type: feature
priority: 2
assignee: Ryan Swift
parent: at-sxgj
tags: [crit, ready-for-agent]
---
# Create and resume independent Crit reviews

Build a local launcher that creates a stable review for each explicitly selected agent conversation and reconnects subsequent rounds to it. Distinct conversations must remain independent even when cwd, branch, and file scope are identical. A completed slice can demonstrate five independent local Git diff reviews and targeted restart without routing changes.

Use the existing pinned Crit v0.23.1 binary and its internal daemon session-key capability; do not require upstream patches or new releases. Distinct output roots alone are insufficient. Persist review metadata independently of Crit's transient session registry, including scope and public URL, so clean shutdown does not lose custom storage discovery. Do not change HOME or select unrelated sessions by cwd alone. Existing configuration and other sessions must be preserved.

Support code and document review scopes. Require explicit identity when a caller cannot provide a stable conversation ID, and refuse ambiguous targeting. Define how a changed branch or scope is handled rather than silently attaching to another review. Keep this ticket verifiable on loopback.

## Acceptance Criteria

- [ ] Five concurrent Git reviews of one checkout/branch have separate IDs, comments, saved state, and waiting completion clients.
- [ ] Repeating the same conversation's request resumes its intended review; explicit creation can start a new review without replacing another.
- [ ] Targeted CLI comments and a Finish event affect only their intended review, including a subsequent revision round.
- [ ] Stop/restart retains review identity, scope, comments, and configured public URL even after the daemon registry entry disappears; unrelated daemons remain running.
- [ ] Concurrent creation for the same identity cannot start competing daemons or corrupt persistent state.
- [ ] Compatibility checks accept the tested pinned binary and fail clearly for an unverified interface/version; no upstream change is necessary.
- [ ] Tests and usage instructions demonstrate Git and document reviews without HOME changes, unintended uploads, or broad cleanup.


## Notes

**2026-11-01T15:20:03Z**

Implemented on integration branch implement/at-sxgj as uncommitted scripts/crit_reviews.py, scripts/crit-review.py, tests/test_crit_reviews.py and docs/crit-review-launcher.md. Verified by merger: 8 real Crit v0.23.1 integration tests pass (9.192s): five identities/comment/Finish separation, concurrent same-identity creation, saved restart/revision, files/range, scope/branch rejection, unknown binary, stale generation/socket rejection and duplicate waiter guard. No HOME changes, commits, uploads, service changes or leftover test-owned daemons. Final code review remains part of epic integration.
