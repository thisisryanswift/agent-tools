---
description: "Identifies missing test coverage in changed code"
mode: all
temperature: 0.1
color: "#e5c07b"
tools:
  write: false
  edit: false
  bash: true
  read: true
  grep: true
  glob: true
  list: true
  skill: true
permission:
  bash:
    "*": deny
    "git diff*": allow
    "git log*": allow
    "git show*": allow
    "git status*": allow
    "git branch*": allow
    "timeout 30 rg *": allow
---

prompt: {file:../prompts/tests-prompt.md}
