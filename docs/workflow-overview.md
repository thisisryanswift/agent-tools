# Our coding workflow

This is a reviewable overview of the setup we have chosen—not a new specification
or another mandatory process.

## The basic shape

```text
Matt's skills       How we clarify, plan, implement, and review
Project tracker     What work exists, its dependencies, and its status
Crit                Where Ryan can give precise human feedback when requested
Specialist tools    Browser, writing, desktop maintenance, and isolated app QA
```

The agent normally executes on **Reef**. Marlin, the phone, and other devices are
clients. Being connected from Marlin does not give the Reef agent access to
Marlin's browser profile or desktop session.

## One engineering baseline

Matt Pocock's 27 promoted skills are installed globally for OpenCode, Claude Code,
Codex, and Antigravity CLI on Reef, using the same pinned upstream revision.
We are not layering Superpowers, Compound Engineering, or pstack over that pack.

Use the amount of workflow the task needs:

- A small understood change can go straight to implementation or test-first work.
- A hard bug starts with a reproducible failure and diagnosis.
- A larger idea can go through clarification, specification, and linked tickets.
- Agent code review checks standards and whether the result matches the request.
- A retrospective can suggest improvements to our tools and working environment.

User-invoked workflows remain explicit choices. Installing the pack does not
automatically start a planning interview, create tickets, or launch implementation.

## Tracker defaults

**Use the project's established tracker. Otherwise, default to `tk`.**

An existing Jira, Linear, GitHub Issues, or other explicitly configured workflow
is an exception to the default, not something to migrate automatically. A GitHub
remote alone does not mean a project uses GitHub Issues.

For `tk` projects:

- Ticket Markdown lives in `.tickets/` in that project checkout.
- A specification lives in a ticket, with child implementation tickets when useful.
- Dependencies use `tk dep`, and `tk ready` identifies unblocked work.
- Record decisions, verification, and blockers as ticket notes.
- Close work after checking its acceptance criteria, not merely after editing files.

We do not require `docs/specs/`, a parallel `.scratch/` backlog, a ticket for every
conversation, or project setup before every task. A separate document is optional
when it serves a real purpose; one artifact remains authoritative.

Tickets persist locally. They do not synchronize across machines unless the
checkout is deliberately synchronized.

## Authorization

Skill instructions describe a workflow; they do not grant permission.

| Request | Boundary |
| --- | --- |
| Fix a bug | Relevant edits and verification; no implied commit or publishing |
| Fix it and commit locally | Local commits allowed; no push |
| Push this branch and open a PR | Those named publishing actions allowed |
| Review this | Findings; not silent fixes or implementation |

Authorization can cover a whole task upfront. It need not become a confirmation
prompt for every step. Preserve pre-existing work and other sessions' changes.
These are agent instructions; runtime permissions remain a separate enforcement layer.

## Crit is manual human review

Ask for Crit when inline feedback would help. A generic review request, completed
specification, or agent code review does not automatically launch it.

```text
Choose the existing ticket, document, or code diff
                    ↓
Ryan explicitly requests Crit
                    ↓
Ryan comments and finishes a review round
                    ↓
Agent addresses authorized comments and replies
                    ↓
Another round if needed; report the actual approval state
```

The agent does not resolve Ryan's comments on his behalf unless asked. Review
approval is not permission to implement a plan, commit, or publish.

Manually requested code and document reviews use independent **Crit CLI**
sessions on Reef. **https://crit.wharfi.sh** lists saved reviews; the launcher
returns a separate `https://<review-id>.crit.wharfi.sh` address for each review.
Connect your device to Tailscale and open that link. The full diff UI works
without a localhost callback or SSH tunnel, and nothing is uploaded to public
`crit.md`.

The agent records an explicit conversation/review identity and waits for that
review's Finish event. After authorized edits, it advances the same review to
the next round. Separate conversations keep separate comments and completion
signals even in one checkout; their underlying files are still shared.

Tailnet access is the outer boundary; review IDs are routing identities rather
than authentication credentials. Other destinations or public exposure require
separate authorization. Legacy Crit Web data and services are retained for
rollback during the remaining runtime-adoption checks; new reviews use the
session protocol.

## Specialists still to review

| Capability | Intended role / open question |
| --- | --- |
| Browser | Decide when to use a Reef-owned browser versus explicitly targeting a client; make login and visibility practical remotely |
| Wayland fixes | On-demand maintenance on the affected graphical workstation, not automatically on Reef |
| Blogging | Preserve Ryan's voice using current edited posts and the real blog repository's checks |
| Isolated workspaces | Hidden desktop/browser app QA on Reef; distinct from Git worktrees and the user's real desktop |

The old test-coverage skill and its dedicated prompts/adapters have been removed.
The installer's tests remain. Specialist tooling has not been upgraded by this
workflow change.

## What this review can validate

This is the first real cross-device Crit review of this integration. The local
CLI, authenticated server access, and a synthetic local comment round have been
checked; the hosted comment/fetch/revision loop still needs this human test.

Useful feedback: which defaults feel right, which steps feel like unnecessary
ceremony, and what is missing for normal remote coding.
