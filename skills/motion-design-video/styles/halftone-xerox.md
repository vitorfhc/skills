# Halftone Xerox

Photocopied zine energy. Everything looks printed: halftone dots, two or three inks, misregistered
plates, toner grain, and a stuttering frame rate that makes motion feel hand-cranked.

## Fits

- Good for: launches with attitude, music and culture, indie products, histories and archives, DIY
  or punk tone, and anything that should feel human and tactile.
- Weak for: precise technical explainers with dense labels, and luxury or ultra-clean brands.

## Look

| Role | Color |
|------|-------|
| Paper | `#EDE8DC` |
| Black ink | `#141414` |
| Spot ink | `#FF4D8D` fluorescent pink, or `#FF6C2F` riso orange |
| Second spot ink, optional | `#2F55FF` riso blue |

The inks are the palette, with two or three in total including black. Give each ink a meaning so
semantic color still holds.

Typography is Archivo Black for headlines, set huge and cropped by the frame, and Space Mono for
small labels that read like typed captions. Type can carry slight misregistration and ink spread.

Texture is the identity:

- Halftone screens for imagery and shapes, with dot size from luminance and a different screen
  angle per ink.
- Misregistration of 2–6 px between ink plates, drifting slightly over time.
- Toner grain, paper fibers, darkened photocopy edges, and occasional copier streaks.

## Motion

- Animate on twos or threes, holding each drawing for two or three frames inside the 30 fps export,
  and let the texture change on each held frame.
- Camera moves are welcome: punch-ins, slow pushes, and whip pans that smear into halftone.
- Let an anchor motif from the subject carry the film and react to the rhythm, such as a pair of
  eyes that blink on the beat.
- Cut on the beat, and slide collage layers in like pasted paper.
- Easing is a snappy ease-out, and a small overshoot is in character.

## Rendering

Canvas 2D, or a WebGL fragment shader for the halftone screen that samples luminance and computes a
dot radius in a rotated cell. Render each ink as its own layer and multiply-blend onto the paper.
Seed all grain and jitter from the frame number so every render is identical.

## Embraces and Breaks It

- Embraces: stepped motion, grain, misregistration, bold cropping, cut-and-paste collage, and
  beat-synced moments.
- Breaks it: smooth gradients, glossy 3D, clean vector perfection, more than three inks, and glow.

## Dials

- **Inks:** black and one spot color, or black and two.
- **Grit:** light print texture, or a heavily degraded copy.
- **Frame feel:** smooth 30 fps under the print texture, or stepped on twos.

## Pitfalls

- Texture eats legibility: set text on flat paper or solid ink, and keep halftone off small type.
- Flicker: boiling texture on large flat areas strobes. Hold texture steady there.
- Speed: stepped motion changes the feel, not the pace. The pacing minimums still apply.
