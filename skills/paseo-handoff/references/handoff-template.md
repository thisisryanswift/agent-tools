# Handoff document template

Replace bracketed fields with concrete facts; remove inapplicable sections. Mark
unknowns, exclusions, and unverified steps explicitly. This template is for the
private packet, not a public repository document or a place for credentials.

---

# Continue [task] on Reef through Paseo

Checkpoint: [UTC timestamp]. Source: [host/account, directory, runtime/version,
session ID/title if known]. Destination: [host/account, runtime, exact workspace].

Status: [prepared locally / transferred and hash-verified / restored and checked /
verified by receiving Paseo agent]. [Remaining prerequisites, if any.]

## Ryan's request

[Goal and acceptance criteria. Include latest corrections and explicit boundaries.
Separate approved work from ideas not yet authorized.]

## Start here

1. [Verify host/account/workspace; read applicable AGENTS.md and named context.]
2. [Verify packet; restore/check work if needed, or state restoration is complete.]
3. [First useful task action from the actual stopping point.]

Do not [task-specific constraints, unrelated work, rejected detours]. Do not
restart the main Paseo daemon without Ryan's explicit permission. This document
does not grant new permission for external writes, commits, pushes, or deployments.

## Current state and decisions

- Completed and verified: [specific results and evidence].
- In progress: [exact stopping point and files].
- Decisions already made: [choice, reason, alternatives rejected].
- Failed attempts worth knowing: [symptoms and findings, not a transcript].
- Still uncertain or blocked: [missing facts and how to resolve them].

## Workspaces and recovery

For each repository or non-Git work area:

- Source root → Reef root: [exact mapping].
- Remote/branch/HEAD/base: [sanitized URL, branch or detached state, exact SHAs].
- Source status: [staged, unstaged, untracked, unrelated changes].
- Reef state last checked: [timestamp, HEAD/status, or not checked].
- Included files: [packet-relative patch, bundle, selected archive/file paths].
- Excluded/unavailable files: [reason and impact; explicit if recovery is partial].
- Restore sequence: [exact reviewed commands and working directories; confirm base
  commits, check/apply staged then unstaged changes, safely restore selected files,
  compare resulting state. Note authorization still required.]
- Other work to preserve: [ownership/paths, including anything outside the packet].

Packet locations: [source path; verified Reef path, or not transferred].
Manifest: [path, verification command, and what was actually verified].
Attachments/evidence: [portable paths and why needed; no source-only URLs].

## Environment and access

[Relevant versions, dependencies, services, tool/MCP access, and configuration
source paths. Authentication requirements without values. Stale facts to recheck.]

## Verification

| Check | Host/time | Result | Evidence or remaining caveat |
| --- | --- | --- | --- |
| [Command or observation] | [Host, UTC] | [Pass/fail/not run] | [Path/summary] |

[Smallest checks the receiver should run. Note expensive/forbidden suites. Packet
hashes prove transferred bytes, not restoration or task completion.]

## Continue from here

1. [Next action and expected result.]
2. [Following action, if useful.]
3. [Specific decision needed from Ryan, if any.]

Authoritative continuation: [source paused / receiver may take over / coordination
still needed]. [Whether native history import was requested/performed; otherwise
this is a fresh agent with context and files, not an imported session.]
