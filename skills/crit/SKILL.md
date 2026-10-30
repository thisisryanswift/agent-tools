---
name: crit
description: "Manually requested human review of tickets, documents, or code with Crit."
disable-model-invocation: true
---

# Manual Crit review

Crit is the human review surface alongside Matt's workflow, not a second
engineering pack or an automatic gate. Only start after an explicit Crit request.
In runtimes that ignore invocation metadata, apply this same explicit-request rule.

1. Confirm the requested artifact/scope. A tracker-backed spec is its existing
   `.tickets/<id>.md`, not an exported copy. Completion: know precisely which
   content the user requested for human review.
2. Select the protocol before running a review:
   - **Reef hosted default:** Ryan selected tailnet-only `https://crit.wharfi.sh`
     for manually requested reviews. Read [the hosted protocol](references/hosted.md).
     Stop at missing credentials or an unavailable target rather than changing
     destination. Publishing is explicit and limited to the selected content.
   - **Explicit local review:** read [the local protocol](references/protocol.md).
     Bind with `--host 127.0.0.1 --no-open`; localhost belongs to the execution
     host. Use this branch when requested, not as an automatic hosted fallback.
   - **Other execution host or destination:** establish target/authentication and
     authorization first. Reef credentials are not a portable skill asset.
3. Follow the selected protocol and relay the actual review URL. Hosted sharing
   returns after publication; it does not keep an agent run waiting for a human.
   When the user says feedback is ready, fetch it from the same review state.
4. Read comments and replies, make only authorized changes, and publish another
   round through the same protocol. Resolving comments belongs to the reviewer
   unless requested. Completion: verified readback or a clearly reported blocker.
5. Report the actual approval/pending state. A timeout, empty comment list, or
   stopped daemon is not approval. Approval does not authorize implementation,
   commits, pushes, or broader actions.

If this is only an installation/help request, do not launch a review. Leave other
review sessions and processes alone. This skill adds no hooks or automatic gates.
