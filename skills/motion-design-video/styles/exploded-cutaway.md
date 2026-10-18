# Exploded Cutaway

The subject taken apart in front of the viewer. A realistic object turns, cuts open, and separates
into its components along their assembly axes, each part labeled with a leader line, while its
mechanism runs.

## Fits

- Good for: how physical things work, such as engines, watches, cameras, organs, devices, and
  buildings, as well as product teardowns and hardware launches.
- Weak for: software, abstract ideas, and anything without parts.

The pieces behind this style were interactive models with orbit controls and an Explode button. In
a video, you are the viewer's hands: choreograph the orbit, choose the order things open, and time
each reveal.

## Look

| Role | Color |
|------|-------|
| Studio field | `#15171B`, with a soft floor gradient |
| Materials | True to the subject: brushed metal, gold, plastic, tissue |
| Cut faces | A flat accent such as `#FF6A3D`, so a cut reads as a cut |
| Leader lines and labels | `#F2F2F2` |
| Active flow | From the subject, such as red and blue blood, colored light beams, or airflow |

Typography is Barlow Condensed 600 in uppercase for part names, Barlow 500 for short descriptions,
and IBM Plex Mono for specifications.

Keep the object large in frame, with labels in clean columns to the sides, connected by leader
lines to anchor points on the parts. Labels never overlap parts.

## Motion

A choreographed sequence replaces the interaction:

1. Hero: the whole object in a slow orbit.
2. Cut: a cutting plane slices a section away, or the shell turns to x-ray.
3. Explode: parts separate along their assembly axes, staggered from the outside in, and settle.
4. Explain: the mechanism runs inside, such as gears turning, air compressing, blood flowing, or
   light bending to a sensor, while labels appear one at a time.
5. Reassemble, or hold the exploded view.

- The camera orbits and dollies slowly with eased moves, and reframes between steps rather than
  during an explanation.
- Explode distances use a critically damped spring. Mechanisms run linearly at true ratios.

## Rendering

Three.js with physically based materials and an environment map. Build the object procedurally
from lathes, extrusions, and instanced gears, or load a model the user supplies. Project label
anchors to screen space each frame and draw the leader lines as an overlay. Drive the camera and
every part from the frame number, with no orbit controls and no real-time clock.

## Embraces and Breaks It

- Embraces: true mechanisms, accurate part order, x-ray and section views, and flow visualization.
- Breaks it: parts flying in arbitrary directions, every label at once, invented components, and
  gratuitous spinning.

## Dials

- **Realism:** photoreal materials, or clean stylized flat shading with outlines.
- **Depth:** major assemblies only, or every named part.
- **Ending:** a reassembled hero shot, or a held exploded view.

## Pitfalls

- Wrong anatomy: research the real part order and mechanism, and label every simplification.
- Label clutter: show one label per idea for its reading time, then dim it.
- Spectacle without explanation: always follow the explode with the mechanism working.
