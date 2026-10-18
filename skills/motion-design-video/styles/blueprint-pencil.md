# Blueprint Pencil

One line that never lifts. A single graphite stroke draws the subject, and the whole film is that
stroke transforming from sketch to blueprint to hologram in one continuous take.

## Fits

- Good for: brand intros and showreels, origin stories, idea-to-product narratives, design and
  engineering tools, and anything about making or evolution.
- Weak for: dense explainers with many simultaneous parts, and hype reels that need hard cuts.

## Look

Each stage owns a field, and the line carries through all of them.

| Role | Color |
|------|-------|
| Paper field | `#F1EADB` |
| Graphite line and sketch text | `#3A3A3C` |
| Blueprint field | `#1D3F8C` |
| Blueprint line | `#E8F0FF` |
| Hologram line | `#5CF0FF` |
| Final field | `#0A0A0B` |

Use only the stages the story needs. Paper to blueprint is often enough.

Typography is Geist alone: weight 900 for large words, and 600–800 for small uppercase labels with
8–12% tracking. Where possible, the line traces the letterforms before they fill.

Texture changes per stage: a fine paper tooth at low opacity, then a faint grid on the blueprint,
then soft bloom only on the hologram.

## Motion

- The line's tip is the focal point. Move the viewer's attention by moving the tip.
- Draw with path-length reveals at a steady, hand-like speed that eases slightly into corners.
- Change stages by transformation: the stroke thickens and floods into a blueprint field, and the
  blueprint lines lift and glow into hologram. Never crossfade between stages.
- Drawing is near-linear with gentle ease at starts and stops. Layout changes use a critically
  damped spring.
- The camera stays mostly locked, and pans or pushes slowly to follow the tip when the drawing
  outgrows the frame.

## Rendering

SVG paths with animated stroke reveals, and path morphing between stages with matched point counts
or a shape interpolator. Add the hologram bloom with an SVG blur filter or a canvas blur pass.

## Embraces and Breaks It

- Embraces: a single continuous take, hand-drawn imperfection such as slight wobble and
  overshooting construction lines, and the line becoming letters.
- Breaks it: cuts, fades, several independent lines appearing at once, stock icons, and heavy
  effects on the paper stage.

## Dials

- **Stages:** paper only, paper to blueprint, or all three ending on hologram.
- **Hand:** loose sketchy pencil, or clean technical pen.
- **Ending:** the line resolves into a logo or wordmark, or loops back to its first stroke.

## Pitfalls

- Losing the line: keep one tip moving at a time, and slow it where it draws something important.
- Drawing too much: tracing a complex object eats seconds. Draw only what carries meaning, and
  bring secondary detail in afterward.
