# Styles

A library of starting points for the film's look and motion. Each card describes a style that
works in motion design: what it suits, its palette and type, how it moves, how to render it, and
the dials worth asking the user about.

Cards are not rules. Adapt a card to the subject and brand, blend two, or invent a direction when
none fits. Only the [principles](../principles.md) are rules.

Read this catalog during [Style direction](../workflows/style.md), and read only the cards you
shortlist.

## Catalog

| Style | Essence | Best for | Energy | Space |
|-------|---------|----------|--------|-------|
| [Editorial Minimal](editorial-minimal.md) | Precise geometry and type on a dark field | Systems, processes, developer tools, concepts | Calm | 2D |
| [Blueprint Pencil](blueprint-pencil.md) | One unbroken line evolving from sketch to blueprint to hologram | Brand intros, origin stories, making and evolution | Measured | 2D |
| [Technical Drawing](technical-drawing.md) | An engineering sheet drawing itself around a turning object | Machines, artifacts, hardware, architecture | Calm | 2.5D |
| [Halftone Xerox](halftone-xerox.md) | Photocopied zine: dot screens, few inks, misregistration | Launches with attitude, culture, archives, indie products | Punchy | 2D |
| [Kinetic HUD](kinetic-hud.md) | Beat-driven type, interface fragments, camera hits | Product launches, AI and dev tools, hype teasers | High | 2.5D |
| [Refractive Glass](refractive-glass.md) | A hero object of glass bending the scene behind it | Premium brands, logo reveals, clarity and focus | Slow | 3D |
| [Exploded Cutaway](exploded-cutaway.md) | A real object cut open and separated into labeled parts | How physical things work, teardowns, hardware | Measured | 3D |
| [Continuous Flight](continuous-flight.md) | One camera journey through waypoints in a world | Timelines, scale, journeys, geography, roadmaps | Measured | 3D |
| [Soft-Body Toy](soft-body-toy.md) | Squishy gummy objects that squash, bounce, and jiggle | Consumer apps, kids, food, games, mascots | Playful | 3D or 2D |
| [Swiss Kinetic Type](swiss-kinetic-type.md) | Huge type on a strict grid, moving with the sentence | Manifestos, announcements, quotes, talk openers | Rhythmic | 2D |
| [Data Story](data-story.md) | Charts that build, morph, and annotate one highlighted series | Results, research findings, metrics, comparisons | Measured | 2D |

The styles are distilled from the community showcase at
[skillry.dev/ai-videos](https://skillry.dev/ai-videos/opus-5-5) and adapted for rendered video.
Several came from interactive pieces, and their cards explain how to choreograph what a viewer
would have controlled.

## Matching

Start from what the subject is and what the video must do:

| When the subject is… | Consider |
|----------------------|----------|
| A system, protocol, or abstract process | Editorial Minimal, Blueprint Pencil |
| A physical object or mechanism | Exploded Cutaway, Technical Drawing |
| A journey, timeline, or change of scale | Continuous Flight |
| Words, values, or a message | Swiss Kinetic Type, Kinetic HUD |
| Numbers and results | Data Story |
| A product launch | Kinetic HUD, Refractive Glass, Halftone Xerox |
| Something about making, design, or evolution | Blueprint Pencil |
| Playful, consumer, or for kids | Soft-Body Toy |
| Cultural, human, or rebellious | Halftone Xerox |

Then weigh the audience, destination, and tone from the brief. A launch reel for developers on
social feeds and the same launch for investors in a keynote call for different cards.

## Adapting

- **Palette:** keep the card's color roles and remap the values to the brand or subject. Recheck
  contrast after remapping.
- **Type:** swap families for brand fonts while keeping the card's weight and size structure.
- **Motif:** derive the recurring motif from the subject, never from the card's example.
- **Energy:** tune easing, transition density, and camera movement. Never shorten reading holds.
- **Blend:** use one base card plus at most one trait borrowed from another, such as Editorial
  Minimal with a Halftone texture on the opening title. More than that loses the identity.
- **Rendering:** when the environment cannot render what a card needs, choose its lighter variant,
  such as flat 2D for Soft-Body Toy, and say so at the style-frame checkpoint.

## New Styles

When the user describes or references a look that no card covers, write a card for it with the
template below and save it in the video project as `style.md`. Do not edit the skill's own cards.

## Card Template

```markdown
# <Style name>

<Two or three sentences: what the viewer sees and how it feels.>

## Fits
- Good for: …
- Weak for: …

## Look
<Palette as a role table with starting hex values, light or dark variants.>
<Typography: open-source families, weights, treatment.>
<Composition and texture.>

## Motion
<Signature moves, transitions, easing character, camera.>

## Rendering
<Technique and toolchain, and how to keep it frame-deterministic.>

## Embraces and Breaks It
- Embraces: <effects this style uses on purpose>
- Breaks it: <what would ruin it>

## Dials
<Two to four choices worth asking the user, each with its options.>

## Pitfalls
<How this style usually goes wrong, and the fix.>
```
