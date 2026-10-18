---
name: motion-design-video
description: >
  Create premium motion-design videos about any subject. Clarify the brief and the look with the
  user, research the topic, develop a visual narrative, and animate it in a style chosen together,
  such as editorial minimal, blueprint line drawing, halftone print, kinetic HUD, refractive
  glass, exploded 3D cutaways, or continuous camera flights, with checkpoints on style frames and
  a draft. Use for explainers, product showcases, educational videos, conceptual animations,
  introductions, promotional content, and technical visualizations.
---

# Motion Design Video

Create a visually sophisticated motion-design video about the user's chosen subject. Act as an
experienced creative director, motion designer, visual storyteller, and subject-matter researcher.

Transform the subject into a compelling visual experience, not an animated written explanation.
The result should resemble a premium motion-design production: intentional composition, precise
animation, excellent typography, and coherent visual storytelling.

## Parameters

| Parameter | Values | Example |
|-----------|--------|---------|
| `duration` | Seconds or minutes, such as `15s`, `45s`, `2m`, or `1m30s` | `duration=45s` |
| `aspect` | Width to height, such as `16:9`, `9:16`, `1:1`, or `4:5` | `aspect=9:16` |
| `voiceover` | `yes` when narration will be recorded over the video later, otherwise `no`. `yes` adds a voiceover script to the deliverables. | `voiceover=yes` |

```text
/motion-design-video duration=45s aspect=9:16 voiceover=yes how DNS resolution works
```

Read parameters as `name=value` from the skill arguments or the user's request. Plain language
also sets them, such as "a 45-second vertical video that we will narrate later". Ask for every
unset parameter during [Clarify](workflows/clarify.md).

## Workflows

Run these workflows in order. Read each file when you reach its step, not before. Each workflow
ends with an output that the next one builds on. At every checkpoint, wait for the user's answer
before continuing.

| Step | Workflow | Output | Checkpoint |
|------|----------|--------|------------|
| 1 | [Clarify](workflows/clarify.md) | Creative brief, including every parameter | Questions about intent and format |
| 2 | [Style direction](workflows/style.md) | Chosen style and how it adapts | Questions about the look |
| 3 | [Research](workflows/research.md) | Verified claims, central message, visual opportunities | — |
| 4 | [Concept and structure](workflows/concept.md) | Visual concept, motifs, internal storyboard | — |
| 5 | [Design system](workflows/design-system.md) | Design system and approved style frames | Style frames |
| 6 | [Animate](workflows/animate.md) | Approved draft and final render | Draft video |
| 7 | [Review and deliver](workflows/review.md) | Verified final deliverable | Revisions |

Never skip Clarify or Style direction. Skip Research only when the subject needs no factual
grounding, such as a purely abstract piece.

When `voiceover` is `yes`, also follow [Voiceover script](workflows/voiceover-script.md): draft
it in step 4 and finalize it in step 7.

## Rules and Freedom

The [principles](principles.md) are the only hard rules: communication, pacing, legibility,
semantic color, continuity, effects that serve meaning, and the frame. Read them before the design
system and keep them through review.

Everything about the look is open. The [style cards](styles/index.md) are starting points that
show what a style can be. Adapt them, blend them, bend them for the subject, or invent a new
direction when none fits.

## Pacing

> **Warning:** Generated videos consistently run too fast. Viewers need time to read each label,
> follow each movement, and absorb each result before the next change. Err on the side of slow.

Follow the minimum timings in the Pacing section of the [principles](principles.md). When the
content does not fit the duration, cut ideas. Never speed up the motion to make it fit.

## Non-negotiables

- Run [Clarify](workflows/clarify.md) and then [Style direction](workflows/style.md) before
  researching or designing anything, and ask their questions with the `AskUserQuestion` tool.
- Never choose the duration, aspect ratio, or voiceover plan yourself. Take each from its parameter
  or ask for it.
- Ask the user about intent and taste, and show concrete proposals to react to. Never ask the user
  for scenes, keyframes, transitions, layer structures, camera placement, animation timing, or
  visual metaphors. Those decisions are yours.
- Show style frames before animating and a draft before the final render, and wait for the user's
  reaction to each.
- Do not fabricate technical behavior, scientific mechanisms, historical facts, product
  capabilities, or data.
- Never claim a video was produced unless it was rendered. Follow the delivery rules in
  [Review and deliver](workflows/review.md).

## Defaults

Apply these unless the user or the creative brief says otherwise:

- A short side of at least 1080 pixels, such as 1920 × 1080 for 16:9.
- 30 frames per second, exported as an H.264 MP4 with the settings in
  [Animate](workflows/animate.md).
- On-screen text in the language of the user's request.

There is no default style. [Style direction](workflows/style.md) chooses one with the user.

## Creative Priorities

1. Communicate the central idea.
2. Establish a distinctive visual identity.
3. Use motion to reveal relationships.
4. Maintain visual continuity.
5. Eliminate unnecessary elements.

Every visual decision must contribute to the narrative, aesthetic, or communication objective.

## Final Principle

**Do not animate a description of the subject. Animate the subject itself.**

Make invisible relationships visible. Make abstract ideas tangible. Use motion to communicate
meaning. Every frame should feel intentional.
