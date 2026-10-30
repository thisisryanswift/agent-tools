# Ticket reconciliation — 2026-10-24

Reviewed all 16 open tickets against recent project-scoped CASS history, repository
files, GitHub activity, and bounded read-only checks. Result: **15 open, 6 closed**
(one newly closed). Existing closed tickets were not re-audited.

Only this repository's tickets and documentation were edited. No runtime changes,
chezmoi applies, model downloads, deployments, commits, or pushes were performed.
Absence of completion evidence is not proof that work never happened; uncertain
items remain open rather than being silently closed or declared failed.

## Disposition

| Ticket | Result | Evidence / remaining work |
| --- | --- | --- |
| `at-vuyt` | **Closed** | Live SSH checks on both Marlin and Tortoise: chezmoi HEAD `daa44a4` includes `1626e64`; installed pre-push hook has the terminal check and passes scoped `chezmoi verify`. No push attempted. |
| `at-lek9` | Open; partial work recorded | All four obsolete CASS unit files still exist in chezmoi. Disabled on Reef now; October 22 history reports disabled on all three hosts. Remove the managed sources and arrange scoped retirement. |
| `at-qdtv` | Open; verified | Reef's live `paseo.service` is active but absent from chezmoi's managed files/source. |
| `at-iv51` | Open | Parent for unfinished toolkit deployment/verification. Fresh `make check` and four installer tests pass; not deployment evidence. |
| `at-zvo9` | Open; unverified | No completed per-runtime discovery inventory or selected-consumer migration record found. This reconciliation did not perform that inventory. |
| `at-duwo` | Open; verified | `prompts/brainstorming-prompt.md` still mandates phases, questions for simple work, and committing a design. |
| `at-ohwo` | Open; blocked | Existing dependencies on `at-zvo9` and `at-duwo` remain unresolved. No selected-runtime deployment was certified. |
| `at-th8j` | Open; description corrected | Browser Harness has a substantial uncommitted overlay, an unpublished Harness 0.1.13 candidate, and unresolved release-review/rollout gates. Local candidate evidence is not target-host verification. |
| `at-ukn0` | Open | `evals/README.md` remains a migration map and reports no counted toolkit model runs. No newer completed evaluation record found here. |
| `at-oln2` | Open; partial verification | Reef still configures the two remote manual SSH export sources. Archived search results do not prove fresh multi-host collection or client access. Acceptance tests remain unverified. |
| `at-e8na` | Open; unverified | No completion evidence found for the specific Paseo/OpenCode permission, interruption, and attachment checks. No interactive smoke test run. |
| `at-gi68` | Open; unverified | Physical Reef GUI check has no recorded completion. No desktop interaction attempted. |
| `at-v2cb` | Open; description corrected | Zoho main is still 3 ahead / 24 behind; GitHub main matches local origin/main `9e50547`. Slack trigger is currently untracked, with no commit in current local refs—not merely an unpushed commit. |
| `at-hoh7` | Open; optional | Current `cass models status` reports embedding models absent. Lexical search remains usable; no download authorized by this audit. |
| `at-n0p3` | Open; optional/unverified | No completion evidence for the three desktop upgrades. The old beta.3 inventory and 0.11.0 target are historical; recheck installed/current desired versions before acting. |
| `at-l6dt` | Open; optional/unverified | No completed Hermes media-client review found. Reconfirm whether it is still wanted before scheduling it. |

## Important corrections

- The October 23 synchronization report is corroborated by live checks, so the
  Marlin/Tortoise pre-push fix is no longer pending.
- Disabling obsolete CASS services did **not** retire their chezmoi sources.
- The Browser Harness ticket's old two-file/version-bump description was stale.
  Its own `docs/restart-checkpoint.md`, `bhw-revw`, and `bhw-roll` distinguish
  unpublished candidate testing from approval and live rollout. Those files were
  read, not executed as instructions; no work in that project was resumed.
- The October 20 claim that the Zoho Slack trigger was committed conflicts with
  current local Git evidence. The ticket and consolidation snapshot now describe
  the observed state without guessing where a historical commit went.

## Evidence and limitations

GitHub's agent-tools main was checked at `3c0931f`; the local checkout started clean
at the same revision. The PR listing returned no entries. Zoho's main was checked
read-only through GitHub and matched the local tracking ref; no fetch was needed.
Related repositories were inspected only for the ticket claims above, not audited
or modified in full. Desktop behavior, Hermes, cross-host CASS latency, and actual
provider skill discovery were not freshly tested.

CASS searches use a retained lexical snapshot whose freshness is not checked.
Complete bounded messages were opened for the key historical claims. The archive
snapshot is evidence of what was recorded, not a current machine-health check.
Canonical coordinates retained for follow-up:

| source_id | source_path | conversation_id | message_index | Relevance |
| --- | --- | --- | --- | --- |
| `local` | `/home/rswift/.claude/projects/-home-rswift-dev-personal-agent-tools/27224e64-9c9b-4af7-bfaf-98093d6eda2e.jsonl` | 4818 | 1668 | October 20 ticket creation and original priorities. |
| `local` | `/home/rswift/.claude/projects/-home-rswift-dev-personal-agent-tools/c27f751b-b195-4e36-b322-d2e09594d4ca.jsonl` | 4942 | 359 | October 22 obsolete-unit disabling and cross-machine CASS design. |
| `local` | `/home/rswift/.claude/projects/-home-rswift-dev-personal-agent-tools/c27f751b-b195-4e36-b322-d2e09594d4ca.jsonl` | 4942 | 730 | October 23 report that Reef/Marlin/Tortoise match chezmoi. |
| `local` | `/home/rswift/.claude/projects/-home-rswift-dev-personal-agent-tools/c27f751b-b195-4e36-b322-d2e09594d4ca.jsonl` | 4942 | 950 | October 24 handoff; cross-machine CASS explicitly still open. |
