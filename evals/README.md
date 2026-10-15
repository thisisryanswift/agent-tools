# Evaluation migration map

Status: source triage only, 2026-10-01. No counted model runs for this toolkit.
`make check` validates structure; `make test` validates the local installer.
Neither measures skill quality or proves discovery in a target runtime.

## Existing assets

The existing manual harness lives at
`~/.local/share/chezmoi/dot_agents/evaluations/`, source revision
`7552c3fc03a1bb4c2a7dd5501048b5e0abf1115a`. Its README and coverage matrix report no
counted runs. It includes fixture builders, test doubles, frozen arms, manifests,
schemas, and grading records pinned to OpenCode 1.18.10 behavior.

Keep those frozen inputs in place while porting selected cases. Its V1 launcher,
`debug config`/`debug skill` assumptions, built-in skill manifest, and environment
isolation cannot be treated as OpenCode V2 equivalents. A V2 service may own the
execution environment separately from the client process.

## Case decisions

| Existing case | Useful content | Porting decision |
| --- | --- | --- |
| RT-01, substantial routing and bypass | Trigger precision and avoiding irrelevant skills | Redesign for explicit task relevance and current stock agents; remove mandatory substantial-work routing. |
| DA-01, durable design approval | Preserving decisions and resuming with correct context | Retain relevant approval/continuity scenarios; remove blanket Crit/hash-bound design gates. |
| TW-01, Ticket workflow | Recovering partially completed work and reporting blockers | Reuse when Ticket is actually selected for a project; no global ticket ceremony. |
| WT-01, worktree safety | Mixed ownership and pre-existing user changes | Prioritize preservation fixtures; modernize runtime/config assumptions. |
| RB-01, risk boundaries | Authorized vs unauthorized effects and fake-secret handling | Keep concrete user-instruction boundaries; align expectations with current permissions instead of requiring speculative warnings. |
| ED-01, engineering discipline | Root-cause fixes, useful tests, read-only review | Retain substantive checks; remove unconditional test-first/review delegation requirements. |
| CE-01, completion evidence | Accurate, scoped, non-fabricated results | Prioritize; distinguish structural checks, task outcomes, and deployment evidence. |
| IP-01, integrated pilot | End-to-end task evidence and continuity | Replace the old routing/approval/Ticket sequence with a real Reef/Paseo workflow after milestone A. |

## First useful comparison

Start with a small review/test-coverage set: a real bug, an apparent bug disproved
by surrounding context, sound code, and a fixture containing pre-existing user
edits. Compare a stock runtime against the same runtime with the selected skill.
Hold model/version, prompt, repository state, tools, and permissions fixed.

Measure correct findings, false positives, severity, preservation of user work,
completion, and cost/time. Test discovery/triggering separately from the output
quality of an explicitly loaded skill. Use deterministic evidence where possible
and independent judgment for findings that require it.

Capture runtime/client/model versions, toolkit revision, selected skills and
discovered paths, fixture/prompt hashes, tool-call evidence, final diff, and grading
criteria. Use fresh disposable run roots under `/tmp/opencode`; keep credentials
and unrelated personal state out of retained artifacts. Repeat comparisons enough
to describe variability rather than treating one pass as general support.

Hermes writing/browser tasks need their own role-specific cases. They should not
inherit coding-only skill selections or be scored on matching an OpenCode ceremony.
