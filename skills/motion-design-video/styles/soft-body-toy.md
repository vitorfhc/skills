# Soft-Body Toy

A playful world of squishy, glossy objects. Gummy shapes wobble, squash, and bounce, type is
chunky and springy, and everything looks like a toy the viewer wants to touch.

## Fits

- Good for: consumer apps, kids and families, food and candy, games, festive openers, friendly
  onboarding, and mascots.
- Weak for: serious, technical, or sensitive subjects, and luxury restraint.

The pieces behind this style were real-time physics games and song-synced 3D openers. In a video,
author the squash and stretch with springs, or bake a simulation with a fixed timestep and seeded
inputs, so every render is identical.

## Look

| Role | Color |
|------|-------|
| Field | `#FFF4E8` cream, or a saturated `#FFD84D` |
| Gummy one | `#FF5A7A` |
| Gummy two | `#36C5F0` |
| Gummy three | `#7BE495` |
| Gummy four | `#FFB13B` |
| Ink and text | `#2A1B3D` |

Gummies look translucent: a lighter rim, a darker core, and a glossy specular highlight.

Typography is Fredoka 600–700 or Baloo 2 800 for titles, with letters that can wobble on their
own, and the same family at 500 for labels.

Keep objects large and chunky on a ground plane with soft contact shadows, under bright, even
light.

## Motion

- Squash and stretch while preserving volume: stretch one axis by `s` and scale the others by
  `1/√s`.
- Bounce with decay using an underdamped spring with a damping ratio of 0.3–0.5. Overshoot is the
  point.
- Anticipate big moves, and follow landings with a jiggle.
- Land on the beat when there is music.
- The camera is gentle and playful, with small bumps on impacts.

## Rendering

Three.js with `MeshPhysicalMaterial` using transmission and thickness for gummies, or a Fresnel rim
to fake subsurface scattering, plus a vertex wobble driven by a spring per object. A flat variant
uses SVG or canvas with squash transforms. Bake any physics at a fixed timestep and look it up by
frame.

## Embraces and Breaks It

- Embraces: bounce, overshoot, jiggle, glossy highlights, candy color, and beat-synced landings.
- Breaks it: limp linear motion, muddy color, many objects colliding at once, and harsh shadows.

## Dials

- **Dimension:** 3D gummy, or flat 2D cartoon.
- **Bounciness:** a gentle wobble, or full rubber.
- **Palette:** candy brights, or the brand's colors made squishy.

## Pitfalls

- Chaos: bounce makes everything move. Keep one primary squishy action at a time and let the rest
  rest.
- Wobbly text: let letters settle completely before their reading hold begins.
