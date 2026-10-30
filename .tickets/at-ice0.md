---
id: at-ice0
status: closed
deps: []
links: []
created: 2026-10-30T19:50:52Z
type: bug
priority: 2
assignee: Ryan Swift
tags: [crit, docs]
---
# Align global Crit policy and docs with approved hosted reviews

Ryan reported Claude receiving local-only Crit guidance after the hosted rollout and authorized correction. Update chezmoi source templates and scoped live global instructions for all four Reef runtimes; align current repository guidance with manual Crit -> approved tailnet target https://crit.wharfi.sh and explicit-local-only fallback. Preserve credentials, service settings, unrelated uncommitted changes, and historical ticket notes. Verify template rendering, live instruction agreement, no stale current-doc defaults, and existing tests. Record already-completed real human comment/fetch review without claiming an unperformed revision or automatic notification.


## Notes

**2026-10-30T19:51:57Z**

Updated shared chezmoi instruction template for Claude/Codex/Gemini and separate OpenCode template with identical explicit manual-only hosted policy: approved https://crit.wharfi.sh target, load Crit for publish/fetch, local only on explicit request, other destinations/exposure require authorization. Applied only four Reef instruction files. Verified exact Crit-block agreement and byte-identical unrelated text in each file, preserving Gemini memories. Updated README, skill catalog, consolidation status, rollout, canonical workflow guide and deployment record; historical ticket notes and explicit-local reference remain intact. Corrected hosted review record to reflect real test-comment fetch and explicit completion without claiming a revision. Added regression test; twelve tests, make check, scoped chezmoi verify and both diff checks pass. No stale identified current-doc defaults remain. Credentials, services and other hosts untouched; no commits/pushes. Existing Claude conversations may retain old text and should reread the global instruction/skill or use a fresh session.
