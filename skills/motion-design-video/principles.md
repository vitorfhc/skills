# Principles

These are the only rules that hold in every style. A style decides how the video looks and moves;
these decide whether it communicates. Everything in the [style cards](styles/index.md) is a
starting point you may bend. When a card and a principle conflict, the principle wins.

## Communicate

- Animate the subject itself, not a description of it. Make invisible relationships visible.
- Give the video one central idea, and let every element serve it.
- Introduce one new idea at a time, and run only one primary motion at once.
- Do not fabricate technical behavior, scientific mechanisms, historical facts, product
  capabilities, or data. When a metaphor simplifies reality, keep the underlying meaning.

## Pacing

> **Warning:** Generated videos consistently run too fast. Viewers need time to read each label,
> follow each movement, and absorb each result before the next change. Err on the side of slow.

| Element | Minimum |
|---------|---------|
| Motion the viewer must follow | 0.6 seconds, and 0.8 to 1.5 seconds for major transformations |
| Hold after each settled change | 1 second before the next change starts |
| On-screen text, settled and legible | 1.5 seconds, or 0.4 seconds per word, whichever is longer |
| Each new idea | About 4 seconds on screen before the next one appears |
| Final frame | 2 seconds, unless the video loops |

- A settled frame that the viewer is reading or absorbing is not idle time.
- When the content does not fit the duration, cut ideas. Never compress these timings.
- Energetic styles get their energy from transitions, contrast, and rhythm, never from shorter
  reading time. A fast cut around a word that holds for its full minimum still reads as fast.
- With a planned voiceover, the narration sets the pace, and these minimums still apply.

## Legibility

- Size text for the smallest screen the video will play on. As a floor, keep essential text at
  least 40 px tall at a short side of 1080.
- Keep strong contrast between text and whatever passes behind it, including textures, grain,
  glow, refraction, and motion blur.
- Keep text short. Never put paragraphs on screen.
- Install every typeface the design system uses before rendering, and confirm in a test frame
  that text renders in it rather than a fallback font.

## Semantic Color

Colors communicate meaning. When a color represents an entity, state, or concept, keep that
association for the whole film. Never change colors arbitrarily between scenes, and use contrast
to direct attention.

## Continuity

The viewer should always know where to look and how the current frame relates to the last.

- Preserve object identity. An object may change position, scale, shape, color, representation, or
  function, but the change must stay visually understandable.
- Motivate every transition. Styles do this differently: a morph, a match cut, a camera flight, a
  cut on the beat. A transition added for its own sake is never motivated.
- Let the ending emerge from what the film established.

## Effects Serve Meaning

No effect is banned in every style, and none is free. Glow, grain, motion blur, particles, camera
shake, bounce, gradients, and 3D all belong in some styles. Use an effect only when you can say
what it tells the viewer or what feeling it carries, and use it consistently once it is
established.

Avoid in every style:

- Stock transition presets and anything that looks like a template.
- Decoration that exists only to fill space, and movement that exists only to fill time.
- Overcrowded compositions and competing visual hierarchies.
- Inconsistent spacing, margins, and alignment.

## Frame

Render with a short side of at least 1080 pixels: 1920 × 1080 for 16:9, 1080 × 1920 for 9:16,
1080 × 1080 for 1:1, and 1080 × 1350 for 4:5. Compose for the chosen aspect ratio from the start
rather than cropping a wide layout. Vertical frames favor stacked arrangements and larger type.

Keep consistent margins and essential labels away from the frame edges. The composition must stay
readable at small playback sizes.

### Vertical Safe Area

On 9:16, platform interface overlays cover the top, bottom, and sides of the frame. Keep every
title, label, and object the viewer must read or follow inside Meta's Reels safe area:

| Margin | Share of frame | At 1080 × 1920 |
|--------|----------------|----------------|
| Top | 14% | 269 px |
| Bottom | 35% | 672 px |
| Left and right | 6% each | 65 px |

This leaves a 950 × 979 px safe area at 1080 × 1920. Backgrounds, structural lines, textures, and
motifs may extend into the margins.

The Instagram profile grid shows 9:16 videos cropped to the central 3:4 band, 1080 × 1440 at
1080 × 1920. The safe area falls inside that band, so keep the opening frame's title inside the
safe area for the grid thumbnail to stay legible.
