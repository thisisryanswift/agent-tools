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
