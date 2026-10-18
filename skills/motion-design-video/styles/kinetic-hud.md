# Kinetic HUD

A launch reel at full throttle. Kinetic type lands on the beat, interface fragments and terminal
lines fly past, the camera hits and recovers, and everything resolves into a cinematic logo.

## Fits

- Good for: product launches, AI and developer tools, event openers, hype teasers, and promos for
  social feeds where energy is the message.
- Weak for: careful explanations, sensitive subjects, and audiences who need time with each idea.

## Look

| Role | Color |
|------|-------|
| Deep field | `#060A24` |
| Primary | `#3D40FE` |
| Text | `#FFFFFF` |
| Ice highlight | `#CFE4FF` |
| Active signal | `#7CF7FF` |
| Alert | `#FF5470` |

Typography is Space Grotesk 700 for kinetic words, huge and often one word per hit, and JetBrains
Mono for HUD readouts, terminal lines, timestamps, and coordinates.

Compose around a central focal word or object surrounded by HUD furniture: corner brackets, ticking
counters, scan lines, crosshairs, labeled telemetry, and terminal panes. Build depth with layered
planes.

## Motion

- Drive everything from a tempo, taken from the music track or assumed at 100–130 BPM, and land
  hits on the beat.
- Words punch in with a small overshoot and settle, tracking snaps, and words replace words on the
  beat.
- Camera hits push or shake on impact and decay over 6–10 frames.
- Use motion blur on fast moves, glow on active elements, and sparks on impacts.
- Transition with whip moves between planes, light sweeps, match cuts on shape, and hard cuts on
  the beat.
- End slower: a cinematic logo reveal with a light sweep, a settle, and a long hold.
- Easing has a fast attack and a long exponential settle, with overshoot on impacts.

Energy lives in the transitions. Each key word still holds for its full reading time, with the cuts
happening around it.

## Rendering

Canvas or WebGL, or a 2.5D stack of SVG or DOM layers with 3D transforms, with Three.js for depth
planes. Make motion blur by accumulating several sub-frame samples per output frame, and glow with
a blur-and-add pass. Seed particles from the frame number.

## Embraces and Breaks It

- Embraces: motion blur, glow, camera hits, particles, scan lines, HUD furniture, terminal UI, and
  beat cuts.
- Breaks it: long static diagrams, gentle crossfades, pastel softness, and HUD readouts that are
  noise unrelated to the subject.

## Dials

- **Intensity:** a controlled launch reel, or maximal hype.
- **Primary color:** electric blue, or the brand's color in the primary role.
- **Music:** synced to a supplied track, or cut to an assumed tempo for later scoring.

## Pitfalls

- Unreadable: give every key word its reading hold, and cut around it rather than through it.
- Effect soup: pick one signature hit, such as a blue light sweep, and repeat it instead of using
  every effect at once.
- Fake interface: make terminal lines and HUD numbers say real things about the product or subject.
