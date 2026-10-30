---
id: at-qdtv
status: open
deps: []
links: []
created: 2026-10-20T23:40:40Z
type: task
priority: 1
assignee: Ryan Swift
tags: [chezmoi, reef]
---
# Adopt paseo.service into chezmoi (Reef-only)

~/.config/systemd/user/paseo.service is live but unmanaged; paseo-hub.service already is. Add it Reef-only in .chezmoiignore.tmpl next to paseo-hub.

## Notes

**2026-10-24T23:17:59Z**

Still open: Reef's paseo.service is active with FragmentPath
/home/rswift/.config/systemd/user/paseo.service. Scoped `chezmoi managed` returns
no source for it, and the chezmoi source has paseo-hub.service but no paseo.service.
This check did not inspect credentials or change/restart either service.
