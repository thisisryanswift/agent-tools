---
id: at-g9co
status: closed
deps: [at-iufw]
links: []
created: 2026-11-01T15:06:47Z
type: feature
priority: 2
assignee: Ryan Swift
parent: at-sxgj
tags: [crit, ready-for-agent]
---
# Browse active and saved Crit reviews

Provide an entry page that lets Ryan find and open active and saved launcher-managed reviews. Show enough context to select among five concurrent workstreams: review/conversation label, checkout, branch or scope, round, and current activity. Identify reviews using the same checkout and explain that their file content follows their own refresh/review-round lifecycle and can include other agents' edits.

The page is backed by the same durable review registry used by the launcher/router. Opening an active review reaches its hostname. Resuming a stopped review uses the launcher-controlled lifecycle and returns the same review identity and saved feedback. Browser actions may target existing registered reviews only; they must not accept arbitrary commands or filesystem paths. Stale records must remain distinguishable from running reviews.

This slice is locally demonstrable independently of tailnet DNS/TLS deployment and requires no upstream modifications.

## Acceptance Criteria

- [ ] The index lists five concurrent reviews with distinct links, useful labels, checkout/branch context, round, and activity.
- [ ] Shared-checkout reviews are clearly identified without claiming isolated authorship or synchronized content.
- [ ] An existing stopped review resumes through its saved launcher metadata and retains comments and its hostname.
- [ ] Stale/failed reviews have clear status and do not masquerade as active daemons.
- [ ] Index actions cannot start arbitrary commands, choose arbitrary upstream addresses, or affect unrelated reviews.
- [ ] Empty, running, stopped, and failed states are demonstrated in UI/integration validation.


## Notes

**2026-11-01T15:49:13Z**

Implemented index in scripts/crit_index.py, integrated on implement/at-sxgj without commits. Four real-Crit index HTTP integration tests pass: five links/context/round/activity/shared-checkout notice, empty/stopped/failed states, saved resume retaining URL/comments, CSRF/origin/exact-action boundaries and HTML escaping. Concurrent observations skip busy persistence lock. Headless Chromium demonstrated five active/stopped/failed cards at 1280px and390px without overflow; real Git/document UI loaded, synthetic comment/Finish/revision retained feedback and targeted same review (approved:false). Two-axis review local findings fixed and re-reviewed; see docs/crit-sessions-validation.md. Local only; no remote HTTPS/human approval implied.
