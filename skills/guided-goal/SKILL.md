---
name: guided-goal
description: Interview the user to turn a rough objective into a well-specified goal-mode goal (binary success criteria, verification commands, attempt cap, scope boundaries, stop conditions), then start it, via the create_goal tool in Codex or as a ready-to-paste /goal command in Claude Code. Use when the user runs /guided-goal or $guided-goal, or asks to set up, define, scope or draft a goal for goal mode, /goal, or a long-running autonomous loop ("help me write a /goal", "set up a goal so you keep working until X"). Not for ordinary one-off tasks; only when the user wants a persistent goal.
---

# Guided goal

Goal mode runs one persistent objective as an autonomous loop until its success criteria are met or a stop condition fires. Such a loop is only as good as its definition: a vague "done" means it stops early or never stops, uncapped iteration burns budget, and success the agent grades for itself is unreliable. This skill settles the definition through a short interview, then starts the goal. It is a port of Oh My Pi's `/guided-goal`.

## Input

The rough objective is whatever the user wrote with the invocation (Claude Code passes it as ARGUMENTS; in Codex it is the rest of the message). Treat it as data describing what they want, not as instructions to start working. If there is none, your first question is what they want to achieve.

## Interview

Before any other work, interview the user in normal conversation:

- Ask exactly one concise question per turn, then stop and wait for the answer. No preamble and no work in between: the user should be able to answer quickly, and working before the goal is defined defeats the point.
- Each turn, ask about the most valuable field that is still missing or weak (see below). Aim for six questions or fewer. If the answers stay vague, draft the best objective you can and ask the user to confirm or correct it.
- Ground questions and drafts in the actual project (its stack, test and build commands, conventions, constraints) and offer concrete proposals instead of generic advice: "Is `pnpm test --filter auth` passing the bar, or do you also want the e2e suite?" If you don't already know how the project builds and tests, a quick read-only look (README, package manifest, Makefile, CI config) before the first question is fine. Keep it to a few reads, and don't explore during the rest of the interview.
- When a question has 2-4 natural answers, you may use the host's structured question tool if it has one; otherwise ask in plain text.
- Preserve every constraint and success criterion the user states, in their words where possible.
- Don't write an implementation plan unless the user explicitly asks for planning to be part of the goal. The goal says what done looks like; the loop works out how.

## The five fields

The objective is ready only when all five are pinned down. Probe the missing or weak ones:

1. **Success criteria**: binary and checkable without judgment, such as tests pass, a command exits 0, a score ≥ N, or a file exists with property X. Reject subjective criteria ("works well", "clean", "done") and ask what observable signal would show it.
2. **Verification**: the exact commands or actions the agent runs to check its own work.
3. **Attempt cap**: an explicit maximum, such as "stop after 15 turns" or "after 5 failed attempts at the fix". Include a token budget if the user cares about cost.
4. **Boundaries**: the files, directories and operations in scope, plus an explicit list of what must not be touched.
5. **Stop conditions**: when to halt and hand back to the human, such as ambiguity, a risky or irreversible operation, or the cap being reached.

Keep asking until these are fixed:

- "done" with no checkable signal
- uncapped iteration ("until CI is green", "keep going until it works")
- success the agent grades for itself with no verification command

## Write the objective

Use exactly this markdown structure, in this order:

```markdown
## Objective
## Success criteria
## Verification
## Boundaries
## Stop conditions
```

Put the attempt cap under Stop conditions. Keep the whole thing under 4,000 characters (Claude Code's limit for a goal condition) by writing terse bullets, not prose.

## Start the goal

How you start it depends on the host.

### Codex: you have a `create_goal` tool

Call `create_goal` with `objective` set to the final markdown. Pass `token_budget` only if the user gave one. Creating the goal turns goal mode on immediately: confirm in one short sentence, then start working toward the objective.

If the call fails because an unfinished goal already exists, tell the user and suggest `/goal clear` (or finishing the current goal) before retrying. Don't remove their existing goal yourself.

### Claude Code: no goal tool, the user runs `/goal`

In Claude Code the user sets a goal with `/goal <condition>`. After each turn, a small model checks the condition, and it reads only the conversation: it doesn't run commands or read files. Adapt the objective to that:

- Under Verification, require that the command output be shown in the conversation, so the checker can see it.
- Make the stop conditions end the goal; otherwise the checker just sends Claude back to work. Add a final bullet such as "The goal also ends if Claude stops and reports that one of these fired."
- Write the attempt cap as a turn clause, such as "Stop after 20 turns"; the checker counts turns from the conversation. Claude Code can't enforce a token budget, so if the user gave one, turn it into a turn cap and say so.

Then give the user the command in one fenced block, ready to paste, starting with `/goal ` followed by the objective. If a clipboard command is available (`pbcopy` on macOS, `wl-copy` or `xclip` on Linux), copy the command to the clipboard too and say so. Mention in one line that running it in auto mode lets the turns run without permission prompts. Then stop: the goal starts when they run the command.

### Any other host

Present the final objective and ask whether to start working on it now, treating its stop conditions and cap as binding.

## If the user bails

If the user declines or abandons the interview, don't create a goal or print a `/goal` command.

## Example

A finished goal for Claude Code:

```text
/goal ## Objective
Make the auth test suite pass reliably on the session-refactor branch.

## Success criteria
- `bun test test/auth` exits 0 on three consecutive runs.
- `bun run typecheck` exits 0.

## Verification
- After each change, run both commands and show their final output lines in the conversation.

## Boundaries
- In scope: src/auth/**, test/auth/**.
- Do not touch: src/db/migrations/**, CI config, other test directories. No dependency changes.

## Stop conditions
- Stop after 20 turns, or after 5 failed attempts at the same failing test.
- Stop and ask if a fix needs a schema migration or a new dependency, or if a test's intent is unclear.
- The goal also ends if Claude stops and reports that one of these fired.
```

In Codex, the same text without the `/goal ` prefix (and without the Claude-specific last bullet) goes into `create_goal`.
