# Refractive Glass

Objects made of glass and light. Shapes, letters, or a product's symbol are rendered as thick
refractive glass that bends the scene behind it, turning slowly under soft studio light.

## Fits

- Good for: premium product and brand intros, logo reveals, hero moments inside a longer film, and
  abstract ideas about clarity, lenses, transparency, or focus.
- Weak for: diagrams with many labels, since refraction distorts what is behind it, and
  environments without GPU rendering.

## Look

| Role | Dark studio | Light studio |
|------|-------------|--------------|
| Field | `#0C0D10`, or a soft sweep from `#1A1C22` | `#F3F3F5`, with gray shadows |
| Refraction backdrop | Bold type or stripes in the accent | Same |
| Glass tint | Near-colorless with a faint accent tint | Same |
| Highlights | `#FFFFFF` | `#FFFFFF` |
| Accent | `#7B5CFF`, or the brand color | Same |
| Text | `#F2F2F2` | `#111216` |

Typography is Inter Tight 600–800, large and calm, set on flat planes beside or behind the glass,
never inside it where refraction scrambles it. Small labels use Inter Tight 500 with wide tracking.

Compose one hero object, centered or on a third, with generous negative space and a backdrop
pattern for the glass to bend. Shadows and caustics ground it.

## Motion

- Slow and weighty: turntable rotation, gentle drift, and glass forms merging into the next shape.
- Make refraction tell the story, such as a lens sliding over a blurred word to bring it into
  focus.
- The camera dollies or orbits slowly with long in/out easing.
- Easing is long sine or cubic in/out, with no snaps.

## Rendering

Three.js `MeshPhysicalMaterial` with transmission, thickness, an index of refraction around
1.45–1.5, and near-zero roughness, lit by an environment map. A raymarched signed-distance shader
suits morphing glass. Render frames through a headless browser with GPU access, and render a style
frame early because transmission is expensive and sensitive to the toolchain.

## Embraces and Breaks It

- Embraces: caustics, subtle chromatic dispersion at edges, soft bloom on highlights, and depth of
  field.
- Breaks it: busy backgrounds, many objects, fast cuts, flat icons beside the glass, and harsh
  lighting.

## Dials

- **Studio:** dark, or light.
- **Hero:** the brand mark, a symbolic shape from the subject, or the key word set in glass.
- **Dispersion:** clean glass, or prismatic rainbow edges.

## Pitfalls

- Black or noisy transmission: confirm the headless renderer supports it, or fall back to
  raymarching or a matcap fake.
- Nothing to refract: glass over a flat background looks like gray plastic. Always put something
  behind it.
