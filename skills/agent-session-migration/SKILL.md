---
name: agent-session-migration
description: Move an OpenCode V2 session to the correct project directory, or transfer an exported session between servers. Use when a conversation was started in the wrong workspace or needs to be resumed elsewhere.
---

# OpenCode Session Migration

Use OpenCode's session tools and API to change session location. A session's
directory belongs to its agent server, which may be on a different machine from
the client. Moving the session does not transfer repositories or credentials.

## Identify the operation

- **Wrong directory on the same server:** move the existing session.
- **Continue from another client:** connect to the same server and resume the
  existing session; a client change alone does not require migration.
- **Transfer to another server:** use that version's session export/import path.

Check `opencode --version` and use the V2 documentation:
https://opencode.ai/v2/docs/api
https://opencode.ai/v2/docs/cli

The older V1 SQLite recipe is historical material, not a V2 migration procedure.
Do not edit the database, WAL files, or service registration to move a session.

## Find the exact session and target

1. Confirm which server owns the session. Use its existing authenticated client
   connection; preserve an explicit `--server` choice for every CLI operation.
2. List sessions in the current project:

   ```bash
   opencode session list --format json
   ```

3. For a session in another project, use the server-wide API search. URL-encode
   the title fragment and confirm the returned ID, title, and location:

   ```bash
   opencode api get '/api/session?search=TITLE_FRAGMENT&limit=20'
   opencode api get /api/session/SESSION_ID
   ```

4. Confirm the target directory exists on the server and contains the intended
   repository/worktree. Inspect its applicable instructions and current Git state.
   Use the exact session ID, not a bulk title match.

## Move on the same server

Prefer the exposed `opencode.session_move` tool when available. Pass the target
`directory`; include `sessionID` when moving a session other than the current one.

The V2 API alternative is:

```bash
opencode api post /api/session/SESSION_ID/move \
  --data '{"directory":"/absolute/server/path/to/repository"}'
```

Use a JSON encoder when constructing the payload from arbitrary paths. The move
may be queued in the session inbox; inspect its response and verify the session's
eventual location rather than assuming admission means completion.

```bash
opencode api get /api/session/SESSION_ID
```

Confirm the same session ID now has the intended `location.directory`. Resume it
from the intended client/server connection and check the working directory before
making project changes. Report a still-pending move as pending.

## Transfer between servers

Read `opencode session export --help` and `opencode session import --help` on the
actual versions first. Use the full native export for a restorable transfer;
sanitized exports are for sharing and may omit content needed for restoration.

```bash
opencode session export SESSION_ID > /private/transfer/session.json
opencode session import /private/transfer/session.json
```

Run each command against its intended source or destination server. Keep the
export private and transfer it through the user's approved path. Check the
destination's handling of existing IDs before importing; do not assume V1 merge
or project-attachment behavior. After import, verify the returned session ID,
messages, and destination location. Use the move API if the location needs changing.

## Report

Report the session ID, source/destination server and directory, operation used,
verification result, and any pending action. Include the private export path when
a transfer was needed. Do not claim a session move migrated its tools, repository,
browser profile, credentials, or runtime capabilities.
