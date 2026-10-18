# Animate

Implement the storyboard in the approved design system. Motion is the primary storytelling
mechanism. Show the user a draft before the final render.

## Motion Language

The design system sets the motion character: how things ease, how scenes connect, and how the
camera behaves. Within it, every movement should reveal something, such as a relationship, a
cause, or a change of state.

Transformation is the strongest default in motion design. Deriving new elements from existing ones
lets the viewer follow. Draw on this vocabulary, not as a storyboard:

- Lines becoming shapes, shapes becoming letters, letters becoming diagrams.
- Numbers becoming geometry, and objects becoming data.
- Grids reorganizing, boundaries becoming paths, and components merging into systems.
- Mask reveals, unfolding, morphing, splitting, and merging.

Styles also connect scenes by camera flight, match cuts, beat cuts, or physical action. Use what the
design system calls for, and keep object identity as the [principles](../principles.md) require.

## Timeline

Before implementing, write the timeline as a table of beats with their motion and hold times.
Check it against the Pacing section of the [principles](../principles.md), and fix anything that
rushes.

## Easing Toolkit

Choose easing that matches the design system's motion character:

| Character | Tool |
|-----------|------|
| Precise settle, no overshoot | Critically damped spring |
| Playful overshoot and jiggle | Underdamped spring |
| Crisp wipes, presses, and exits | Exponential in/out |
| Cinematic camera and long moves | Cubic or quintic in/out |
| Continuous movement | Linear |
| Discrete state changes | Stepped |
| Hand-made feel | Holding each drawing for two or three frames |

The critically damped spring is `f(t) = 1 - (1 + ωt)e^(-ωt)`. It settles without overshoot and
is 99% settled at `ωt ≈ 6.6`, so derive `ω` from the motion's duration in seconds:
`ω = 6.6 / duration`.

| Duration | ω |
|----------|---|
| 0.6 s | 11 |
| 0.8 s | 8.3 |
| 1.0 s | 6.6 |
| 1.5 s | 4.4 |

The underdamped spring with damping ratio `ζ < 1` is
`f(t) = 1 - e^(-ζωt)(cos(ω_d t) + (ζ / √(1 - ζ²)) sin(ω_d t))`, where `ω_d = ω√(1 - ζ²)`. Lower
`ζ` bounces more: 0.3 is rubbery and 0.7 barely overshoots.

## Rhythm

Establish a deliberate motion rhythm. Synchronize animations that communicate related events. Use
timing to create anticipation, emphasis, cause and effect, contrast, progression, and resolution.

When appropriate, synchronize animation with an underlying beat. With a music track, land key
moments on it. Without one, let the subject set the pace rather than an arbitrary BPM.

With a planned voiceover, time each beat to its narration line in the storyboard, and render
without an audio track so the narration can be laid over it.

## Motion Density

Keep meaningful change on screen without overwhelming the viewer. Avoid long stretches without
change, several unrelated animations competing for attention, and movement that exists only to
fill time. Use faster transitions once a relationship is established, but never go below the
pacing minimums.

## Camera

Follow the design system. Whatever the camera does, keep it consistent, and move it only when the
movement carries meaning, such as following a path, revealing scale, or reframing for the next
idea.

## Typography as Motion

Text should take part in the storytelling:

- Words transforming into shapes, and letters assembling from lines.
- Characters revealed through masks, and labels emerging from objects.
- Numbers interpolating between values.
- Equations transforming into visual representations.
- Words becoming components of diagrams, or following paths.

Use strong typographic moments selectively, and let moving text land before its reading hold
begins.

## Render Deterministically

A video renders frame by frame, often slower than real time. Several styles come from interactive
or real-time pieces, so adapt their techniques:

- Derive every value from the frame number, as `t = frame / fps`. Never read a wall clock,
  `requestAnimationFrame` timestamps, or `Date.now()`.
- Seed all randomness, such as grain, particles, and jitter, from a fixed seed and the frame number.
- Replace interactions, such as orbit controls, buttons, hover, and drag, with choreographed camera
  moves and timed events.
- Bake physics ahead of time at a fixed timestep and look it up by frame, or author it with springs.
- Wait for fonts, textures, and models to load before capturing the first frame.
- Make motion blur by accumulating sub-frame samples, not with a real-time effect.

Choose a toolchain that the environment can actually execute and render, as the style frames
proved.

## Draft and Checkpoint

Render a draft of the whole video with final timing. When rendering is slow, render it at half the
final resolution. Make a contact sheet of one frame every few seconds, such as
`ffmpeg -i draft.mp4 -vf "fps=1/4,scale=480:-1,tile=4x3" -frames:v 1 draft-sheet.png`.

Watch the draft yourself first. Check pacing, legibility, and the principles, and fix obvious
problems before showing it.

Then show the user the draft and contact sheet paths, and ask with `AskUserQuestion` how it feels,
with options tailored to what is most uncertain, such as:

- `Ready for final (Recommended)`: render at full quality.
- `Pacing`: some moments feel too fast or too slow, named in notes.
- `Change a moment`: a beat to rework, named in notes.
- `Look`: something in the style feels off.

Translate the reaction into craft changes yourself. Re-render the draft after substantial changes
and ask again. When the user wants it faster, tighten transitions and cut beats before shortening
reading holds, and say so when a request would break the pacing minimums.

## Final Render

Render at the final resolution and aspect ratio. Install every typeface the design system uses
before rendering, such as from Google Fonts or npm, and confirm in a test frame that text uses
them rather than a fallback font.

Export with settings that every major platform accepts:

| Setting | Value |
|---------|-------|
| Frame rate | 30 fps, constant |
| Codec | H.264, High profile |
| Pixel format | `yuv420p` |
| Quality | CRF 18 or lower |
| Container | `.mp4` with `faststart` |
| Audio | AAC when the brief includes a music track, otherwise none |

With ffmpeg: `-r 30 -c:v libx264 -profile:v high -pix_fmt yuv420p -crf 18 -movflags +faststart`.

## Output

The animation source, the approved draft, and the final rendered video.

Continue with [Review and deliver](review.md).
