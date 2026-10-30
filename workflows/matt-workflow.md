# Global Matt workflow defaults

Use this guide for tracker, specification, triage, and wayfinding operations in
Matt Pocock's skills. It supplies tracker context when a project has no
`docs/agents/issue-tracker.md`; do not require a setup ceremony just to use it.
Project instructions and an explicitly configured project tracker take precedence.

## Select the tracker

1. Read relevant project instructions and existing tracker configuration. Preserve
   an established Jira, Linear, GitHub, GitLab, beads, or other workflow. A GitHub
   remote alone does not establish GitHub Issues as the tracker.
2. An established `.tickets/` directory uses `tk`. If project instructions name a
   different tracker as authoritative, follow them; ask if the evidence conflicts.
3. With no established alternative, use `tk` as the global default. Initialize
   `.tickets/` only when authorized work actually needs durable tracking, in the
   project checkout, not in the home directory or on every exploratory turn.

Do not bulk-migrate projects, replace tracker settings, or create a parallel
`.scratch/` backlog. Existing projects are exceptions, not migration targets.
In Matt's terminology, `tk` is a custom/"other" tracker with local storage, not
the built-in `.scratch/<feature>/issues/` local-files convention. This guide is
the provided tracker configuration unless a project overrides it.

## Specifications and tickets

- A specification lives in the configured tracker. For `tk`, create a ticket
  containing the actual specification, usually an `epic` tagged `spec` when it
  will own implementation children. A small change can use a single task/bug.
- Keep Matt's specification substance: problem, solution, user stories where
  useful, decisions, testing, acceptance criteria, and out-of-scope work.
- Do not require `docs/specs/` or duplicate a specification into a document.
  Separate documents are optional for genuinely useful format/size reasons;
  link them from the ticket and designate one authoritative version.
- Slice larger specs into self-contained, verifiable implementation tickets with
  the spec as parent. Create IDs before wiring dependency edges.
- Preserve a project's existing glossary/ADR conventions. Running a tracker skill
  does not authorize inventing domain docs or changing an existing doc layout.

## tk operation mapping

Run `tk help` for the installed command contract. Ticket IDs come from the tool;
never invent them. Markdown files in `.tickets/` are the authoritative records.

| Matt operation | tk operation |
| --- | --- |
| Create a larger spec | `tk create "Spec: Title" -t epic --tags spec -d "Full specification"` |
| Create a small task or bug | `tk create "Title" -t task -d "Requirements and acceptance criteria"` (use `-t bug` for a bug) |
| Create a child | `tk create "Title" --parent <spec-id> -d "Self-contained task"` |
| Read a ticket | `tk show <id>`; read its `.tickets/<id>.md` when full Markdown is needed |
| List work | `tk ls`, `tk ready`, `tk blocked`; inspect parent/tags to select the relevant frontier |
| Add a blocking edge | `tk dep <dependent-id> <blocker-id>` |
| Validate the graph | `tk dep cycle`, `tk dep tree <id>` |
| Start work | `tk start <id>`; avoid claiming a ticket another session is already working |
| Record a comment/decision/result | `tk add-note <id> "Evidence, decision, or blocker"` |
| Finish or reopen | `tk close <id>`, `tk reopen <id>` |

Use CLI operations for supported changes. For description/type/tag edits without
a CLI command, re-read and narrowly edit the ticket Markdown, preserving frontmatter,
IDs, dependencies, and other sessions' notes. Check `tk show` afterward.
Do not silently assign work to another person. `tk start` is a state transition,
not an atomic multi-agent lock; coordinate concurrent claims explicitly.

`tk` lifecycle statuses remain `open`, `in_progress`, and `closed`. Matt's optional
triage roles are tags, not replacement lifecycle states: `needs-triage`,
`needs-info`, `ready-for-agent`, `ready-for-human`, or `wontfix`. Preserve existing
tag mappings, apply roles only during requested triage, and keep at most one state
role per triaged ticket. Category roles (`bug`, `enhancement`) may also be tags.
When rejecting work, record the reason; closed does not necessarily mean implemented.

For wayfinding, use an epic tagged `wayfinder:map`, child decision tickets tagged
by kind, and native `tk dep` edges. Record resolutions as notes and maintain the
map's decision index. Wayfinding does not authorize implementation or pushing a
research branch; publish only when separately authorized.

Complete implementation tickets only after checking their acceptance criteria and
recording actual verification or explicit limitations. Complete a parent only when
its own outcome is met, not merely because a child closed. Dependencies do not
automatically grant execution authority or cause auto-closure.

Ticket files persist locally. Git synchronization, commits, pushes, and external
tracker writes retain their authorization requirements. Existing tracker exceptions
use that tracker's operations instead of translating them into local tk copies.

## Crit is optional human review

Start Crit only when the user names Crit or explicitly invokes its skill. A generic
"review this" request, `code-review`, or completing a spec does not start Crit.
The approved hosted target for requested reviews is https://crit.wharfi.sh
(tailnet-only). Load the `crit` skill for hosted publication and feedback fetch;
use local mode only when explicitly requested. It can review a `.tickets/<id>.md`
file directly; no duplicate spec document is needed. Other upload destinations or
network exposure require separate authorization. Crit approval is scoped feedback,
not permission to commit, publish beyond the review, execute a plan, or broaden the task.
