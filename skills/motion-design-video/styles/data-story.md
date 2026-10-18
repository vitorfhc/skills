# Data Story

Numbers that move with meaning. Charts build, morph, and annotate themselves, and one highlighted
series carries the story while everything else stays a quiet gray.

## Fits

- Good for: growth and results, research findings, reports, economics, comparisons, metric
  launches, and before-and-after stories.
- Weak for: subjects with no quantitative dimension.

## Look

| Role | Dark | Light |
|------|------|-------|
| Field | `#0E1013` | `#FAFAF7` |
| Context data | `#5B616B` | `#B8BCC4` |
| Story series | `#3D7BFF` | `#2459E0` |
| Positive | `#2FD27A` | `#16A35A` |
| Negative | `#FF5A5F` | `#D93A3F` |
| Text | `#F4F4F4` | `#141518` |

Gray is the main color. The highlight is rare and meaningful.

Typography is Instrument Sans 600–700 for headlines and takeaways, and IBM Plex Mono or Instrument
Sans tabular figures for values and axes. Big-number moments let a single figure fill the frame.

Show one chart per beat, with the takeaway as a short headline stated as the insight, such as
"Revenue tripled in two years", rather than a chart title.

## Motion

- Build charts in reading order: axes, baseline, data, then the annotation that explains them.
- Morph between chart types to show the same data another way, such as bars into a stacked bar
  into a line, preserving each data point's identity and color.
- Count numbers up to land exactly on the true value, in tabular figures so digits do not jitter.
- Draw annotations, such as a circle, an arrow, or a bracket, to point at the insight.
- Easing is cubic in/out for data transitions and a critically damped spring for layout.
- The camera is locked. Zoom into a region by rescaling the axes, not by moving a camera.

## Rendering

SVG with `d3-scale` and `d3-shape` for geometry. Interpolate the data, not the pixels.

## Embraces and Breaks It

- Embraces: honest axes, real data, one highlighted series, annotations, and morphs.
- Breaks it: 3D charts, silently truncated axes, rainbow series, chart junk, and invented numbers
  presented as real.

## Dials

- **Field:** dark, or light.
- **Data:** the user's real data, published data from research, or illustrative numbers labeled as
  such.
- **Density:** one hero number per beat, or full charts.

## Pitfalls

- Fabricated data: never present numbers as real unless they are. Label illustrative values on
  screen.
- Too many series: highlight one and gray the rest.
