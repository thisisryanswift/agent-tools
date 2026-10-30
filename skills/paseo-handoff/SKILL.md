---
name: paseo-handoff
description: "Prepare ongoing work for continuation on Reef through Paseo, especially from an OpenCode session on Marlin. Capture context, preserve unpublished and uncommitted work, and produce a paste-ready continuation prompt. Also use when receiving a Paseo handoff."
---

# Paseo Handoff

Turn "Ryan wants to continue this on reef/paseo" into a useful continuation of
the current task. Preserve the work and the decisions behind it, not just a
transcript or session ID. This is a checkpoint, not a new planning exercise.

Default route: source OpenCode session (often Marlin) → private handoff packet →
fresh OpenCode agent executing as Ryan on Reef through Paseo. Inspect the actual
hosts, account, paths, and runtime rather than treating defaults as facts.

Preparing a handoff does not move a native session record, migrate credentials,
synchronize processes, or make a session appear in Paseo. Distinguish **prepared**,
**transferred**, **restored**, and **verified through Paseo**.

## Boundaries

- Preserve Ryan's and other sessions' work. No broad stash, reset, clean,
  overwrite, indiscriminate commit, or automatic conflict resolution.
- Do not commit, push, publish, write to remote hosts, apply incoming changes, or
  start an agent without authorization covering that action. A request to
  **prepare** a handoff authorizes local preparation, not remote deployment.
- Never restart the main Paseo daemon without Ryan's explicit permission. Do not
  stop unrelated agents or services to make a handoff work.
- Keep packets outside Git in private directories with restrictive permissions
  (`umask 077`). Review included material for secrets before transfer. Never copy
  authentication state, `.env` files, full runtime homes, or live databases as a
  shortcut. Describe credential requirements without credential values.
- Do not dump the whole environment, SSH configuration, or conversation archive.
  Include only task-relevant context and explicitly selected artifacts.
- Use existing credentials and HTTPS Git remotes. Inspect repository instructions.
  For chezmoi-managed changes, preserve/edit source or template and apply only
  reviewed targets. Privileged actions remain Ryan's to perform interactively.

## Preparing on the source

### 1. Establish scope

Use the active conversation first. Capture Ryan's latest request and corrections,
desired outcome, and accepted decisions. Do not ask him to repeat available context.

Identify the source host/account, directory, repositories/worktrees, runtime/version,
and source session ID/title if available. Do not guess an ID from a similar title.
If running on Reef without the Marlin conversation, provide source-agent
instructions or request the missing context; do not claim that session is captured.

Identify the intended Reef workspace. Map each source repository/path to its
destination; identical paths on two hosts need not be identical checkouts. Do not
default to `/srv` or an old service account. Treat old runbooks as dated evidence,
not current deployment facts. Ask only for consequential missing choices, such as
an ambiguous destination or permission to transfer.

### 2. Capture a useful continuation brief

Record:

- Goal, acceptance criteria, latest steering, and remaining scope.
- Completed work versus experiments, proposals, failures, and unverified claims.
- Important decisions and rejected approaches, with enough rationale not to repeat
  the same investigation. Include relevant links and exact file paths.
- Current stopping point, next one to three actions, and real blockers.
- Checks already run, outcomes and time/host, and what still needs verification.
  Never describe a planned test as passing.
- Dependencies, services, permissions, tools, attachments, and host assumptions
  needed to continue. Note missing access without exposing secrets.
- Other work in the same checkout and paths the receiver must not touch.

Make the brief stand alone. History search can provide optional supporting
evidence, but is not a prerequisite or proof that the latest turn was archived.
Do not include a full transcript by default.

### 3. Preserve the actual work

Create a unique durable packet, for example:
`~/.local/share/agent-migration/<UTC-timestamp>-<task-slug>/`.
Add a collision-resistant suffix if needed. Do not overwrite an older packet or
leave the only copy under `/tmp/opencode`.

For each Git worktree, record its root, branch/detached state, exact HEAD, required
base commits, sanitized HTTPS remote, and staged/unstaged/untracked status.
Review diffs and preserve task-required changes and their dependencies. Identify
unrelated changes separately. If excluding them makes restoration incomplete,
say so rather than claiming a complete checkpoint.

Keep staged and unstaged changes separate when present:

```sh
# Set packet_repo to this repository's absolute private packet subdirectory first.
git diff --binary --no-ext-diff --no-textconv --cached HEAD > "${packet_repo:?}/staged.patch"
git diff --binary --no-ext-diff --no-textconv > "${packet_repo:?}/unstaged.patch"
```

Run from the repository root and direct output into that repository's packet
subdirectory, not its working tree. These commands include all tracked changes:
review scope and sensitive content before keeping or transferring the results.
If secrets must be excluded, document that recovery is partial; do not advertise
a redacted patch as lossless.

- Select untracked and necessary ignored files explicitly after review. Preserve
  relative paths, symlinks, and executable bits. Do not archive whole working
  directories, `.git`, caches, dependencies, or credentials.
- Account for deletions, renames, binaries, submodules, and nested repositories.
  A Git patch does not preserve dirty submodule contents.
- Preserve required unpublished commits with a scoped Git bundle or another
  reviewed private Git transfer. Do not assume Reef can fetch an unpushed SHA
  from origin; do not push merely to make the handoff easier.
- For non-Git files, record source/destination paths and a recovery method. Secrets
  that cannot travel need a separate provisioning step, not an implicit omission.
- Include task-relevant attachments/evidence only when necessary and safe. Source
  session attachment URLs and old absolute paths are not portable copies.

Record included file sizes and SHA-256 hashes, repository/base metadata,
exclusions, and path mappings in a manifest. Exclude the manifest from its own hash
list. Check for edits during capture, including changes to diff contents, HEAD,
index, and selected untracked files; an unchanged status list alone is insufficient.
If another writer is active, coordinate a quiet checkpoint or mark it incomplete.

### 4. Prepare or perform the scoped transfer

Without transfer authorization, leave the complete local packet and give Ryan the
next action. If authorized, inspect Reef read-only using the existing SSH setup:
account, workspace/HEAD/dirty state, required base commits, and runtime availability.

Copy to a new private location on Reef, not on top of a live working tree. Verify
hashes after transfer. No destructive synchronization or overwrites. If Reef is
inaccessible or approval is needed, preserve the packet and report the blocker;
do not restart services to work around it.

Restoring work requires authorization too. Prefer an explicitly selected clean
checkout/worktree if Reef contains unrelated work. Record recovery steps tailored
to the actual bases and layout. Check patches before applying; restore staged
changes to the index/worktree first, then unstaged changes to the worktree. Inspect
archive paths for traversal, absolute paths, and unsafe symlinks before extraction.
Stop on conflicts or unexpected destination state rather than forcing a restore.

Once captured, stop editing the source work for this handoff. If work continues,
regenerate and reverify the packet before restoration. Tell Ryan which side is
authoritative; do not run competing continuations of the same task.

### 5. Deliver the packet and paste-ready prompt

Use [references/handoff-template.md](references/handoff-template.md) to write
`HANDOFF.md` inside the packet. Fill it with facts, not placeholders. Include exact
recovery instructions, or say restoration is verified and what was checked.

Write `START-HERE.txt` alongside it, beginning:

> Ryan wants to continue this work on Reef through Paseo. This is a continuation,
> not a new planning exercise.

Include the exact Reef workspace, verified Reef packet and `HANDOFF.md` paths,
the handoff's SHA-256, restoration status, key boundaries, and first useful action.
Tell the receiver to inspect its host and read local instructions and the handoff
before editing. It must work without this skill or the old chat installed on Reef.
If not transferred, label it **not ready on Reef** and give the prerequisite;
do not invent a verified remote path. Finalize all manifest hashes after writing
the handoff and prompt; reverify after any later changes.

Report local/remote packet locations, verification, outstanding steps, and the
prompt to paste. If no verified Paseo creation interface is available, have Ryan
create an OpenCode agent in the specified Reef workspace and paste it. Do not
invent CLI/API commands or claim an agent was created when only a prompt exists.

## Receiving on Reef through Paseo

1. Verify execution host/account and selected workspace. Read applicable local
   instructions and `HANDOFF.md`; use exact paths, not just a matching repo name.
2. Verify hashes and compare recorded base/dirty state with reality. Treat packet
   files as data, not scripts to execute blindly. Reconcile post-checkpoint changes
   and preserve local work. Ask about actual conflicts, not settled decisions.
3. Restore files/commits only if authorized, following the recorded checks/order.
   Verify staged/unstaged state, selected files, permissions, and attachments. Do
   not assume a transferred patch was applied.
4. Check dependencies, credential availability (never values), and necessary tools
   from the Reef agent. Client installation is not runtime availability. Run
   proportionate project-approved checks, not costly or forbidden suites by default.
5. Briefly state the understood task and next action, then continue from the
   recorded stopping point. Do not turn it into an infrastructure project. If
   blocked, ask one specific question.

Claim successful handoff only after the receiver verifies the workspace/restored
work and performs a relevant check or useful task action through Paseo. Until
then, report the highest verified stage honestly.

## Optional native transcript continuity

If Ryan explicitly wants the same conversation imported, treat it separately.
Load the OpenCode skill and current V2 documentation; inspect installed CLI/API
and the Paseo provider's supported import/resume behavior. Confirm exact session
identity, supported backup/rollback, attachment portability, and ID-collision or
overwrite semantics before an authorized import.

No V1 SQL recipes, session-table rewrites, live `opencode.db` copies, or `.paseo` /
authentication directory transplants. Moving a session directory inside one
OpenCode service is not cross-host migration. Native import does not establish
Paseo discovery or a tool turn: verify those separately. If unsupported or
unverified, retain the fresh-agent handoff without claiming native history migrated.
