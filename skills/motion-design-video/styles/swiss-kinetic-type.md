# Swiss Kinetic Type

Typography is the whole film. A strict grid, huge sans-serif words, flush-left rags, hard color
blocks, and words that move with the rhythm of the sentence.

## Fits

- Good for: manifestos, brand values, announcements, quotes, talk and conference openers, and any
  message where the words are the idea.
- Weak for: mechanisms or objects that need to be shown, and dense text.

## Look

| Role | Color |
|------|-------|
| Field | `#F5F3EE` |
| Text | `#0D0D0D` |
| Signal | `#E8231B` |
| Block | `#0D0D0D`, or `#1F3BFF` |

Use two colors plus one signal, and invert scenes, such as white on red or on black, for emphasis.

Typography is Inter Tight 800–900 for display, with leading around 0.9 and negative tracking at
large sizes, and Inter Tight 500 for small labels with tabular figures. Push size contrast to the
extreme: one word fills the frame beside a small caption.

Snap everything to a visible or implied modular grid, such as 12 columns, in asymmetric layouts
with rules and blocks as structure.

## Motion

- Words move in grid units: they slide along rows, reveal from their baselines through masks, and
  swap in place.
- Rhythm follows speech, and stressed syllables land with bigger moves.
- Color blocks wipe across the grid, and a letter can scale up to become the next field.
- Easing is crisp exponential in/out, with snaps for discrete changes.
- The camera is locked. The grid is the stage.

## Rendering

SVG or DOM with real font metrics, and clip-path masks for reveals. Check kerning in a test frame.

## Embraces and Breaks It

- Embraces: extreme scale contrast, hard cuts on rhythm, color inversion, and the grid as visible
  structure.
- Breaks it: decorative illustration, gradients, drop shadows, centering everything, and more than
  two type families.

## Dials

- **Palette:** off-white, black, and red, or the brand's colors.
- **Grid:** visible, with rules and numbers, or implied.
- **Tempo:** a measured reading pace, or rhythmic beat cuts.

## Pitfalls

- Too much text: one phrase per beat, held for its reading time.
- Reading against motion: a moving word cannot be read. Let it land, then hold.
