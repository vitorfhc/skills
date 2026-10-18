# Continuous Flight

One unbroken camera journey. The camera travels through a world, such as space, a planet, a city,
a map, a timeline corridor, or a microscopic scale, and stops at waypoints where each idea lives
before flying on to the next.

## Fits

- Good for: timelines and futures, changes of scale, journeys and supply chains, geography,
  history across eras, and roadmaps.
- Weak for: mechanisms that happen in one place, and dense side-by-side comparisons.

## Look

| Role | Color |
|------|-------|
| Void or sky | `#05060A` |
| World surface | Real data, such as map tiles, planet textures, or terrain, graded with restraint |
| Waypoint marker | `#FFC65C` |
| Path | `#FFFFFF` at 60% |
| Text | `#F4F1EA` |
| Secondary text | `#8A93A6` |

Typography is Instrument Serif for waypoint titles and dates, large and cinematic, and Geist Mono
for coordinates, distances, and years.

Treat each waypoint as a composed shot with its title in a consistent position. A path line
connecting the waypoints keeps the journey legible.

## Motion

- The journey is the transition. Fly from waypoint to waypoint and never cut.
- Ease out of each hold, travel, and ease into the next waypoint. Each arrival holds long enough to
  read the stop.
- Build depth with scale and parallax: near objects move fast and far objects slowly.
- A recurring readout, such as a date or distance counter, ticks during flight and ties the motion
  to meaning.
- Move along a smooth spline with long cubic or quintic in/out easing, and ease the look-at target
  too. No shake.

## Rendering

Three.js with a perspective camera on a Catmull-Rom spline, sampled by frame number. Use real data
textures where available, such as NASA's public-domain planetary maps or Natural Earth, and add fog
and atmosphere for depth.

## Embraces and Breaks It

- Embraces: real data, vast scale, atmosphere, depth of field on arrival, and ticking counters.
- Breaks it: cuts, jittery handheld moves, too many waypoints, and travel so fast the viewer loses
  orientation.

## Dials

- **World:** space, Earth or a map, an abstract timeline corridor, or the microscopic.
- **Stops:** how many waypoints. Fewer is better, about one per 6–10 seconds.
- **Tone:** awe and cinema, or clean and informational.

## Pitfalls

- Motion sickness: limit angular velocity and keep the horizon stable.
- Travel eats time: budget 1.5–3 seconds of flight between stops into the duration.
- Licensing: use public-domain or openly licensed maps and textures, and credit them.
