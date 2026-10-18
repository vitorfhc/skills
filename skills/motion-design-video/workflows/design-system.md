# Design System

Turn the style direction into a design system for this film, prove it with style frames, and agree
on it with the user before animating.

## 1. Build the System

Start from the chosen card and the style direction, and fit them to the storyboard. The card is a
starting point. Bend it wherever the subject, brand, or story is better served, and keep what you
change consistent across the film.

Define:

- Typefaces, weights, and sizes for every kind of text.
- Color roles mapped to the specific entities, states, and concepts in the storyboard.
- Texture, rendering technique, and toolchain.
- Motion character: easing families, signature moves, transition vocabulary, and camera behavior.
- The effects the film uses and what each one means, and the effects it avoids.
- Frame size, margins, safe areas, and layout grid.

Check the system against the [principles](../principles.md): legibility at phone size, contrast
through every texture and effect, semantic color, and the safe area on 9:16.

## 2. Render Style Frames

Render two or three still frames at final resolution with the real toolchain and fonts:

- The opening frame.
- The densest beat.
- The ending or the most important moment.

Style frames prove that the environment can render the style, including 3D, shaders, and fonts,
before any animation is built on it. When it cannot, adapt the system now.

Inspect each frame yourself and fix what is off before showing it. Then combine the frames into one
contact sheet, such as `ffmpeg -i 1.png -i 2.png -i 3.png -filter_complex hstack=inputs=3 sheet.png`,
using `vstack` for wide frames.

## 3. Checkpoint

Show the user the contact sheet path, with one line per frame naming the beat and what to look at.
Then ask with `AskUserQuestion` how the frames look, with options tailored to the film, such as:

- `Looks right (Recommended)`: animate in this system.
- `Adjust details`: palette, type, or texture changes, described in notes.
- `Try another direction`: return to the shortlist from [Style direction](style.md).

The user reacts. You translate reactions into design decisions. When a reaction is vague, such as
"make it pop more", render two specific variants and ask which one is closer. Re-render the
changed frames and ask again until the user approves.

## Output

The approved design system and style frames.

Continue with [Animate](animate.md).
