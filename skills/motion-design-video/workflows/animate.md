# Animate

Implement the storyboard with the design system. Motion is the primary storytelling mechanism.

Prioritize:

- Smooth continuity.
- Precise timing.
- Meaningful transformations.
- Readability.
- Spatial consistency.
- Professional easing.

## Motion Language

Prefer **transformation over replacement**. Objects should evolve naturally from one state into
another.

### Continuous Transformation

Whenever possible, derive each new scene from existing visual elements:

- Lines becoming shapes.
- Shapes becoming letters.
- Letters becoming diagrams.
- Diagrams becoming interfaces.
- Interfaces becoming abstract compositions.
- Numbers becoming geometric objects.
- Objects becoming data visualizations.
- Grids transforming into other spatial structures.
- Boundaries becoming paths.
- Components merging into larger systems.

These examples define a visual vocabulary, not a required storyboard. Choose transformations that
are appropriate to the subject.

### Object Identity

Preserve recognizable properties when objects transform. An object may change its position,
scale, rotation, shape, color, representation, or function, but its transition should remain
visually understandable.

When a transformation represents a conceptual relationship, that relationship should be
recognizable through the animation.

### Transitions

Favor:

- Shape morphing.
- Geometric unfolding.
- Path transformations.
- Object merging and separation.
- Mask-based reveals.
- Spatial reorganization.
- Typographic transformations.
- Continuous line motion.
- Structural expansion and contraction.

Avoid disconnected scene transitions. The viewer should perceive the video as one coherent visual
system.

## Physics and Timing

Motion should feel precise, controlled, and intentional.

### Pacing

Generated animations consistently run too fast. Set every timing on the slow side, then check it.

| Element | Minimum |
|---------|---------|
| Motion the viewer must follow | 0.6 seconds, and 0.8 to 1.5 seconds for major transformations |
| Hold after each settled change | 1 second before the next change starts |
| On-screen text, settled and legible | 1.5 seconds, or 0.4 seconds per word, whichever is longer |
| Each new idea | About 4 seconds on screen before the next one appears |
| Final frame | 2 seconds, unless the video loops |

- Introduce one new idea at a time, and run only one primary motion at once.
- A settled frame that the viewer is reading or absorbing is not idle time.
- When the content does not fit the duration, cut ideas. Never compress these timings.
- With a planned voiceover, the narration sets the pace, and these minimums still apply.

Before rendering, write out the timeline as a table of beats with their motion and hold times, and
fix anything below these minimums.

### Easing

For positioning, prefer critically damped spring behavior:

`f(t) = 1 - (1 + ωt)e^(-ωt)`

Choose `ω` based on the intended motion speed. This approaches the destination smoothly without
overshooting.

| Motion | Interpolation |
|--------|---------------|
| Positioning | Critically damped spring |
| Wipes, presses, and exits | Exponential ease-in/out |
| Continuous movement | Linear |
| Discrete state changes | Stepped |

Avoid exaggerated elastic effects.

### Rhythm

Establish a deliberate motion rhythm. Synchronize animations that communicate related events. Use
timing to create anticipation, emphasis, cause and effect, contrast, visual progression, and
resolution.

When appropriate, synchronize animation with an underlying beat. Do not force an arbitrary BPM or
fixed scene duration. The subject should determine the pacing.

With a planned voiceover, time each beat to its narration line in the storyboard, and render
without an audio track so the narration can be laid over it.

### Motion Density

Maintain visual activity without overwhelming the audience. Avoid:

- Long periods without meaningful change.
- Several unrelated animations competing for attention.
- Excessive simultaneous transformations.
- Movement that exists only to fill time.

Allow complex ideas enough time to become understandable. Use faster transitions when the
relationship is already established, but never go below the minimums in Pacing.

## Camera and Space

Default to a locked, front-facing, orthographic camera. The composition should feel like a
precisely designed canvas.

Prefer moving objects over moving the camera. Objects may rotate, translate, scale, deform,
unfold, intersect, separate, or rearrange spatially. Represent depth through layering,
perspective, or geometric construction when appropriate.

Avoid unnecessary camera movement. If the subject genuinely benefits from camera movement, use it
deliberately and consistently. Do not introduce cinematic motion merely to create spectacle.

## Typography as Motion

Text should participate in the visual storytelling:

- Words transforming into geometric shapes.
- Letters assembling from lines.
- Characters revealing through masks.
- Labels emerging from objects.
- Numbers interpolating between values.
- Text compressing into structural elements.
- Equations transforming into visual representations.
- Typography following paths.
- Words becoming components of diagrams.

Prefer short, meaningful text. Avoid large paragraphs inside the video. Use typography to reinforce
the central idea rather than narrate every visible action.

Maintain readability. Important text should remain visible long enough to be understood. Use
strong typographic moments selectively.

## Render

Choose an animation toolchain that the environment can actually execute and render. Render at the
resolution and aspect ratio from the design system.

## Output

The animation source and, when rendering succeeds, the rendered video file.

Continue with [Review and deliver](review.md).
