---
name: ryan-blog
description: Turn project notes, agent sessions, or rough drafts into Ryan-style blog posts. Use when writing or editing personal technical essays for Ryan's blog.
---

# Ryan Blog

Find the main lesson. Do not summarize the entire session.

## Source of truth

Use Ryan's current edited posts in `~/dev/blogs/posts/` as the style source. Locate
the blog checkout on the execution host if that path is unavailable. Read two or
three recent relevant posts before writing; the older ToolHive essay is useful
history, not the sole voice template.

Representative starting points:

- `posts/2026-04-25-Taming-MCPs-Skills-and-Agent-Chaos-with-ToolHive/index.md`
- `posts/2026-04-26-How-are-you-managing-git-gh-access-with-Agents/index.md`
- `posts/2026-04-29-forking-paseo-mobile-vibe-coding-for-me/index.md`
- `posts/2026-04-30-building-zellij-agent-tools/index.md`

Read enough of the source work to distinguish the actual outcome from proposals,
failed attempts, and tool noise. When available, compare an agent draft with Ryan's
subsequent edits in Git: those edits are evidence of taste.

## Workflow

1. Identify the human problem and one reusable lesson.
2. Gather project notes or the relevant session. For OpenCode V2, consult
   `opencode session export --help` and use the intended server/session. Read
   user/assistant text and relevant results; do not include hidden reasoning or
   credentials in the post.
3. Read current blog examples and choose only the moments supporting the lesson.
4. Draft under `posts/<date>-<slug>/index.md`, unless Ryan asks for inline text.
5. Follow the blog repository's current checks; its existing workflow uses
   `uv run dev-check posts/<date>-<slug>` when available.
6. Report the draft path, check result, and any unresolved factual questions.

## Voice

Write in first-person singular, as a working developer explaining what happened:

- Plainspoken, pragmatic, curious, lightly self-deprecating.
- Specific about tools and workflow, honest about failures and uncertainty.
- Short paragraphs, contractions, and occasional fragments.
- Technical detail in service of the story.
- Modest practical conclusions rather than a triumphant launch announcement.

Avoid corporate phrasing, hype, unnecessary jargon, explaining basics to
developers, and pretending agent output was perfect. Prefer Ryan's framing over
the agent's account of how much work it performed.

## Structure

A useful compact arc:

1. The personal problem.
2. What Ryan tried.
3. What worked and where it got weird.
4. The lesson and what remains unresolved.

Two to four headings are often enough. Start with why Ryan cared, not product
background or setup instructions. Pick the title late, after the thesis is clear.
A short italic TLDR can help a longer narrative.

Include concrete artifacts, real prompts, and screenshots when they support the
story. One compact “what got built” section is usually sufficient. Keep Markdown
lists flat and paragraphs readable on a phone. Do not invent screenshots or add
frontmatter unless the surrounding posts use it.

One memorable line or small, specific joke can help. Do not force several. Avoid
SEO-driven wording and product-release language.

## Session-to-post judgment

- Preserve Ryan's role as decision-maker and taste-filter.
- Include mistakes when they explain the result or changed the direction.
- Distinguish implemented, verified, proposed, and unfinished work.
- Keep messy real prompts when they add useful texture.
- Compress implementation inventories, command sequences, and review ceremonies.
- Include permission, authentication, or security detours only when central to the
  lesson; recurring themes do not belong in every post.
- Exclude unrelated private information, hidden reasoning, and tool metadata.

The good focus of the ToolHive essay was that using many agents made tools,
configuration, and authentication hard to maintain. Its point was not a recap of
every action in a 383-message session. The same editing rule applies to new work.

## Editing an existing draft

Preserve a draft that already works. Suggest small grammar, rhythm, or factual
fixes; do not replace the whole post unless asked or the structure is broken.
Keep Ryan's casual wording when it works. Flag sentences that feel too corporate,
braggy, or vague.

Watch what Ryan removes: agent narration, exhaustive inventories, tangential
permission stories, and polished conclusions. Watch what he keeps: concrete
prompts, candid failures, practical artifacts, and moments where taste corrected
the agent.

## Quality bar

- Does the opening explain why Ryan cared?
- Is the main lesson obvious?
- Is there a concrete artifact or experience behind the claims?
- Are failures and limitations represented accurately?
- Could the post be 20% shorter?
- Does it sound like someone who actually used the tools?
- Does it match current edited posts more than an earlier agent draft?
