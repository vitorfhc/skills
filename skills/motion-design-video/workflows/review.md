# Review and Deliver

Evaluate the final render against the quality criteria, revise weak sections, deliver, then offer
the user a round of revisions.

## Review

Review the rendered output, not only the source. Inspect frames at key moments and at each
transition.

Check:

- Does the video honor the creative brief from [Clarify](clarify.md) and the direction from
  [Style direction](style.md)?
- Does it match the approved style frames, and does it address every note from the draft
  checkpoint?
- Does the video communicate its intended message?
- Is every major animation meaningful?
- Are transitions visually coherent?
- Is typography readable at phone size, including over textures and effects?
- Are colors consistent with their semantic roles?
- Does the runtime match the duration in the brief?
- Does the frame match the aspect ratio and resolution in the brief?
- Does the file match the export settings in [Animate](animate.md)? Check the frame rate, codec,
  and pixel format with `ffprobe`.
- Does the text render in the planned typefaces rather than a fallback font?
- On 9:16, is everything essential inside the safe area in the [principles](../principles.md)?
- Does every timing meet the pacing minimums in the [principles](../principles.md)? Audit the beat
  timeline, and slow down or cut anything that rushes.
- With a planned voiceover, does each beat leave time for its narration line, and does every
  timestamp in the voiceover script match the final render? Without one, does the video
  communicate its message silently?
- Are complex ideas adequately explained?
- Does the animation feel original rather than templated?
- Are there factual inaccuracies, or numbers presented as real that are not?
- Does every effect carry meaning, and does the film avoid the effects its design system rules out?

Revise weak sections and re-render before delivering.

## Quality Standard

The final result should resemble work produced by an experienced motion-design studio. It should
combine:

| Quality | Standard |
|---------|----------|
| Art direction | A distinctive and consistent visual identity. |
| Motion design | Precise choreography, excellent easing, and purposeful transitions. |
| Typography | Confident, disciplined, high-quality type composition. |
| Storytelling | A clear narrative progression appropriate to the subject. |
| Communication | Visual clarity and an effective central message. |
| Technical execution | Clean rendering, accurate alignment, smooth animation, and reliable output. |

The result should feel deliberately designed from first principles. Avoid anything that resembles
a generic motion-graphics template.

## Deliver

Unless the user or the brief specifies otherwise, deliver a complete, polished video:

- The aspect ratio from the brief, with a short side of at least 1080 pixels when supported.
- The duration from the brief.
- With a planned voiceover, the final [Voiceover script](voiceover-script.md) next to the video.
- On-screen text in the language of the user's request.
- The approved design system.

If the environment cannot render or export a video, do not claim the video was produced. Instead,
provide the most useful supported production deliverable, such as an executable animation project
or a detailed production specification, and clearly identify what remains unrendered.

In the final response, state the output path, duration, aspect ratio, resolution, frame rate,
style, voiceover plan, voiceover script path when there is one, and any assumptions recorded in the
brief.

## Revisions

After delivering, ask with `AskUserQuestion` whether the video is done, with options such as
`Done (Recommended)`, `Small tweaks`, and `Rework a section`, letting the user name the changes in
notes. For tweaks, return to [Animate](animate.md), re-render, review again, and redeliver. For a
change of look, return to the checkpoint in [Design system](design-system.md).
