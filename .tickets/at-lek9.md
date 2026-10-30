---
id: at-lek9
status: open
deps: []
links: [at-oln2]
created: 2026-10-20T23:40:40Z
type: task
priority: 1
assignee: Ryan Swift
tags: [chezmoi, cass]
---
# Retire old cass/cass-sync units from chezmoi

chezmoi still ships cass.service/.timer and cass-sync.service/.timer (ExecStart ~/.local/bin/cass). Replaced by cass schedule's cass-incremental/cass-nightly. Disabled on Reef; check Marlin/Tortoise before removing (add to .chezmoiremove).


## Notes

**2026-10-22T16:16:30Z**

2026-10-22: the old units are now disabled on all three hosts. Tortoise had cass.service + cass-sync.timer enabled and Marlin had cass.service + cass.timer enabled; both failed on the stale ~/.local/bin/cass path. Safe to remove from chezmoi and add to .chezmoiremove. See at-oln2 for the cross-machine design.

**2026-10-24T23:17:59Z**

Still open: all four obsolete unit files remain in the local chezmoi source.
Reef reports cass.service, cass.timer, cass-sync.service, and cass-sync.timer
disabled; cass-incremental.timer and cass-nightly.timer are active. The October
22 CASS session confirms disabling the old units on Marlin and Tortoise, but
disabling is not source retirement. No source removal or chezmoi apply was done.
