---
id: at-lek9
status: open
deps: []
links: []
created: 2026-10-20T23:40:40Z
type: task
priority: 1
assignee: Ryan Swift
tags: [chezmoi, cass]
---
# Retire old cass/cass-sync units from chezmoi

chezmoi still ships cass.service/.timer and cass-sync.service/.timer (ExecStart ~/.local/bin/cass). Replaced by cass schedule's cass-incremental/cass-nightly. Disabled on Reef; check Marlin/Tortoise before removing (add to .chezmoiremove).

