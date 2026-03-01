/**
 * git-ai plugin for OpenCode
 *
 * This plugin integrates git-ai with OpenCode to track AI-generated code.
 * It uses the tool.execute.before and tool.execute.after events to create
 * checkpoints that mark code changes as human or AI-authored.
 *
 * Installation:
 *   - Copy to ~/.config/opencode/plugin/git-ai.ts (global)
 *   - Or to .opencode/plugin/git-ai.ts (project-local)
 *
 * Requirements:
 *   - git-ai must be installed and available in PATH
 *   - OpenCode plugin SDK (@opencode-ai/plugin)
 *
 * @see https://github.com/acunniffe/git-ai
 * @see https://opencode.ai/docs/plugins/
 */

import type { Plugin } from "@opencode-ai/plugin"

// Tools that modify files and should be tracked
const FILE_EDIT_TOOLS = ["edit", "write"]

export const GitAiPlugin: Plugin = async (ctx) => {
  const { $, directory, worktree, client } = ctx

  // Check if git-ai is installed
  let gitAiInstalled = false
  try {
    await $`git-ai --version`.quiet()
    gitAiInstalled = true
  } catch {
    // git-ai not installed, plugin will be a no-op
    if (client) {
      client.tui.showToast({
        body: { 
          message: "git-ai not found in PATH - code tracking disabled", 
          variant: "warning"
        },
      })
    }
  }

  if (!gitAiInstalled) {
    return {}
  }

  const repoWorkingDir = worktree || directory

  // Check if we're actually in a git repository
  let isGitRepo = false
  try {
    await $`git -C ${repoWorkingDir} rev-parse --git-dir`.quiet()
    isGitRepo = true
  } catch {}

  if (!isGitRepo) {
    if (client) {
      client.tui.showToast({
        body: { 
          message: "Not in a git repository - AI code changes will NOT be tracked", 
          variant: "warning"
        },
      })
    }
    return {}
  }

  // Track pending edits by callID so we can reference them in the after hook
  const pendingEdits = new Map<string, string>()

  return {
    "tool.execute.before": async (input, output) => {
      // Only intercept file editing tools
      if (!FILE_EDIT_TOOLS.includes(input.tool)) {
        return
      }

      // Extract file path from tool arguments (args are in output, not input)
      const filePath = output.args?.filePath as string | undefined
      if (!filePath) {
        return
      }

      // Store filePath for the after hook
      pendingEdits.set(input.callID, filePath)

      try {
        // Create human checkpoint before AI edit
        // This marks any changes since the last checkpoint as human-authored
        const hookInput = JSON.stringify({
          type: "human",
          repo_working_dir: repoWorkingDir,
          will_edit_filepaths: [filePath],
        })

        await $`echo ${hookInput} | git-ai checkpoint agent-v1 --hook-input stdin`.quiet()
      } catch (error) {
        // Log but don't fail - git-ai errors shouldn't break the agent
        console.error("[git-ai] Failed to create human checkpoint:", error)
      }
    },

    "tool.execute.after": async (input, _output) => {
      // Only intercept file editing tools
      if (!FILE_EDIT_TOOLS.includes(input.tool)) {
        return
      }

      // Get the filePath we stored in the before hook
      const filePath = pendingEdits.get(input.callID)
      pendingEdits.delete(input.callID)

      if (!filePath) {
        return
      }

      try {
        // Create AI checkpoint after edit
        // This marks the changes made by this tool call as AI-authored
        const hookInput = JSON.stringify({
          type: "ai_agent",
          repo_working_dir: repoWorkingDir,
          agent_name: "opencode",
          // Note: model and conversation_id would ideally come from session context
          // For now we use placeholders - transcript support can be added later
          model: "unknown",
          conversation_id: `opencode-${Date.now()}`,
          edited_filepaths: [filePath],
          transcript: {
            messages: [],
          },
        })

        await $`echo ${hookInput} | git-ai checkpoint agent-v1 --hook-input stdin`.quiet()
      } catch (error) {
        // Log but don't fail - git-ai errors shouldn't break the agent
        console.error("[git-ai] Failed to create AI checkpoint:", error)
      }
    },
  }
}
