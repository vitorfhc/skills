# Design System

Create a coherent visual system that remains consistent throughout the film. Apply the brief's
visual direction first; use these defaults where it is silent.

## Aesthetic

Use a sophisticated motion-graphics language combining:

- Minimalist editorial design.
- Precise geometric composition.
- Clean vector graphics.
- Computational geometry.
- Technical illustration where appropriate.
- High-quality typography.
- Purposeful negative space.
- Carefully structured visual hierarchy.

The visual style should feel deliberately designed rather than assembled from stock
motion-graphics templates.

## Typography

Preferred typefaces:

- **Geist** for titles, headings, and general text.
- **Geist Mono** for numbers, code, measurements, and technical annotations.

Install them before rendering, as described in [Animate](animate.md). When they cannot be
installed, use visually comparable alternatives and record the substitution as an assumption.

| Element | Weight | Treatment |
|---------|--------|-----------|
| Major titles | 900 | Large, commanding |
| Secondary headings | 700–800 | Clear hierarchy |
| Labels | 600–800 | Compact, precise |
| Supporting text | 500–600 | Highly legible |
| Technical values | 500–700 | Monospaced |

Use generous tracking for small uppercase labels. Typography should be integrated into the
animation rather than existing as a static overlay. See [Animate](animate.md) for typographic
motion.

## Default Color Palette

| Role | Color |
|------|-------|
| Background | `#07080A` |
| Primary text | `#F5F5F5` |
| Structural lines | `#343841` |
| Primary accent | `#1B3ED2` |
| Active elements | `#45F0DD` |
| Secondary emphasis | `#FFB547` |
| Positive outcomes | `#91F2A3` |
| Errors or contrast | `#FF6174` |

Treat this palette as the default visual identity, not a mandatory restriction. Adapt the colors
when the subject or brand requires it.

## Semantic Color

Colors should communicate meaning. When a color represents a particular entity, state, or concept,
preserve that association throughout the animation. Avoid changing colors arbitrarily between
scenes. Use contrast intentionally to direct attention.

## Composition

- Use the aspect ratio from the brief.
- Render with a short side of at least 1080 pixels: 1920 × 1080 for 16:9, 1080 × 1920 for 9:16,
  1080 × 1080 for 1:1, and 1080 × 1350 for 4:5.
- Keep rendering high-quality and crisp.
- Keep margins and alignment consistent.
- Leave generous negative space.
- Keep a clear visual hierarchy.

Maintain safe areas around important content. Avoid placing essential labels near the frame
boundaries. The composition should remain readable at smaller playback sizes.

Compose for the chosen aspect ratio from the start rather than cropping a wide layout. Vertical
frames favor stacked arrangements and larger type.

### Vertical Safe Area

On 9:16, platform interface overlays cover the top, bottom, and sides of the frame. Keep every
title, label, and object the viewer must read or follow inside Meta's Reels safe area:

| Margin | Share of frame | At 1080 × 1920 |
|--------|----------------|----------------|
| Top | 14% | 269 px |
| Bottom | 35% | 672 px |
| Left and right | 6% each | 65 px |

This leaves a 950 × 979 px safe area at 1080 × 1920. Backgrounds, structural lines, and motifs may
extend into the margins.

The Instagram profile grid shows 9:16 videos cropped to the central 3:4 band, 1080 × 1440 at
1080 × 1920. The safe area falls inside that band, so keep the opening frame's title inside the
safe area for the grid thumbnail to stay legible.

## Visual Restraint

Avoid effects that make the animation feel generic or template-driven.

### Banned by Default

- Particle bursts.
- Excessive glow.
- Lens flares.
- Camera shake.
- RGB splitting.
- Generic crossfades.
- Decorative gradients.
- Exaggerated bounce.
- Meaningless floating shapes.
- Unnecessary glitch effects.
- Excessive motion blur.
- Arbitrary 3D objects.
- Stock transition presets.
- Decorative visual noise.

Override these only when a specific effect is genuinely required by the user's subject or artistic
direction.

### Avoid

- Overcrowded compositions.
- Inconsistent spacing.
- Tiny labels.
- Excessive explanatory text.
- Unmotivated transitions.
- Arbitrary color changes.
- Competing visual hierarchies.
- Unnecessary complexity.

Visual restraint should make the motion more sophisticated, not less expressive.

## Output

Design tokens for this film:

- Typefaces, weights, and sizes per element.
- Color roles mapped to the specific entities, states, and concepts in the storyboard.
- Frame size, margins, safe areas, and layout grid.

Continue with [Animate](animate.md).
