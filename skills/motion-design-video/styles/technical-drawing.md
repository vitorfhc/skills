# Technical Drawing

The subject as an engineering drawing come to life. An object turns slowly in 3D while its
orthographic views, dimension lines, sections, and callouts draw themselves around it on a sheet.

## Fits

- Good for: how things are built, the history of machines and artifacts, hardware products,
  architecture, mechanisms, and anatomy-of videos.
- Weak for: abstract concepts with no physical form, and emotional brand pieces.

## Look

| Role | Vellum | Blueprint |
|------|--------|-----------|
| Sheet | `#EEF0EA` | `#0E1A2B` |
| Ink and visible edges | `#1B2433` | `#EAF0F7` |
| Construction lines | `#9AA3AE` | `#4A5B73` |
| Dimensions and callouts | `#2F6BD8` | `#7FB2FF` |
| Markup and emphasis | `#D9412B` | `#FF7A5C` |
| Section hatching | Ink at 35% | Ink at 35% |

Typography is IBM Plex Sans Condensed 600–700 in uppercase for titles and callouts, and IBM Plex
Mono for dimensions and part numbers. A title block in the corner with the name, scale, date, and
sheet number makes a strong recurring motif.

Compose a sheet with a border and title block, and arrange the front, top, and side views on shared
axes by projection convention. Line weight carries the hierarchy: thick for visible edges, thin for
dimensions, dashed for hidden edges, and chain lines for centers.

## Motion

- Draw in a draftsman's order: construction lines, visible edges, dimensions, then labels.
- Lock the 3D view and the projections together, so the views update as the object turns.
- Dimension lines extend from the feature, then the number counts up to its value.
- For a section, a cutting plane sweeps across and the cut face fills with hatching.
- Easing is measured and mechanical: exponential in/out for line draws, a critically damped spring
  for arranging views, and no bounce.
- The camera is orthographic. A slow turntable rotation of the object is the main movement.

## Rendering

Three.js with an orthographic camera and edge rendering, such as `EdgesGeometry` with line
segments or an outline pass. Build the object procedurally from lathes, extrusions, and boolean
operations so it needs no assets. Overlay dimensions and text in SVG. Simple objects can be pure
SVG with precomputed projections.

## Embraces and Breaks It

- Embraces: hidden-line dashes, hatching, title blocks, and measurements true to the real object.
- Breaks it: photoreal materials, glow, saturated color fields, handwritten fonts, and measurements
  invented for decoration.

## Dials

- **Sheet:** light vellum, or dark blueprint.
- **Object:** line only, or line with flat shaded fill.
- **Depth:** an overview with key dimensions, or full detail with sections and part callouts.

## Pitfalls

- Fake numbers: research every dimension shown, or label it as illustrative.
- Line soup: too many thin lines blur at phone size. Show fewer views and thicken key edges.
