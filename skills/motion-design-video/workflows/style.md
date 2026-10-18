# Style Direction

Find the look and feel the user wants with a second round of questions, right after the brief.
Propose concrete directions for the user to react to. Never ask the user to design.

## 1. Shortlist

Read the brief and the [style catalog](../styles/index.md). Shortlist two or three directions
that fit the subject, objective, audience, destination, and tone, and read only those cards.

A direction can be a card as written, a card adapted to the subject, a blend of two, or one you
invent. Pitch each in terms of this video, saying what the viewer will actually see. "The lookup
drawn as one pencil line hopping across a blueprint" beats "Blueprint Pencil".

Make the shortlist varied. Three shades of the same look give the user nothing to choose between.

When the brief includes brand guidelines or references, start from them: shortlist the cards
closest to them and adapt each toward the brand.

## 2. Ask About the Look

Ask with `AskUserQuestion`, following the same mechanics as [Clarify](clarify.md).

The first question offers the directions, recommended first. Give each option a `preview` with a
small ASCII mockup of a key frame, the palette's hex values, and the typefaces. Add a fourth option,
`Your call`, whose description says you will choose and pitch it at the style-frame checkpoint.

Then add a question for every other dimension of the look that is still open and would visibly
change the video:

| Dimension | What the answer decides |
|-----------|-------------------------|
| Energy | Calm and measured, confident, or punchy and kinetic |
| Brand | A free hand, the brand's colors and fonts, or matching a reference |
| Light or dark | When the shortlisted directions work both ways and the destination does not decide |
| Texture | Clean vector, printed and tactile, or rendered 3D, when the shortlist spans them |

Rules for choosing:

- Ask as many questions as the look needs, and no more. Do not ask what the brief already answers.
- Ask about taste, never about craft. Palettes, easing, layouts, and camera moves are yours to
  decide.
- Tailor every question and option to the subject.

Example first call for a DNS explainer for developers:

```json
{
  "questions": [
    {
      "question": "Which look fits the DNS video?",
      "header": "Style",
      "multiSelect": false,
      "options": [
        {
          "label": "Editorial Minimal (Recommended)",
          "description": "Precise diagrams on a dark field. The resolver chain builds hop by hop with crisp labels.",
          "preview": "┌────────────────────────────┐\n│  browser ──▶ resolver      │\n│                 │          │\n│        root ◀───┘          │\n│         └──▶ .com ──▶ ns1  │\n│  RESOLVING example.com     │\n└────────────────────────────┘\n#07080A #F5F5F5 #1B3ED2 #45F0DD\nGeist / Geist Mono"
        },
        {
          "label": "Blueprint Pencil",
          "description": "One pencil line follows the query across a blueprint, drawing each server as it arrives.",
          "preview": "┌────────────────────────────┐\n│ ~~~~~~~~~~~~~~~~~~~~~~~╮   │\n│  ( browser )           │   │\n│        ╰~~~~~~~( root )╯   │\n│                    ╰~~~▶   │\n│  WHERE IS example.com?     │\n└────────────────────────────┘\n#F1EADB #3A3A3C #1D3F8C #5CF0FF\nGeist"
        },
        {
          "label": "Continuous Flight",
          "description": "The camera rides the query across a map of the internet, stopping at each server it asks.",
          "preview": "┌────────────────────────────┐\n│        ·     ·        ◉    │\n│   ·       ╱‾‾‾‾‾‾‾‾‾‾      │\n│      ◉‾‾‾╱   ·      ·      │\n│  ROOT SERVER · hop 2 of 4  │\n└────────────────────────────┘\n#05060A #F4F1EA #FFC65C\nInstrument Serif / Geist Mono"
        },
        {
          "label": "Your call",
          "description": "I choose the direction and show it to you as style frames before animating."
        }
      ]
    },
    {
      "question": "How should the DNS video feel?",
      "header": "Energy",
      "multiSelect": false,
      "options": [
        {"label": "Calm and precise (Recommended)", "description": "Unhurried moves, long holds, room to read every hop."},
        {"label": "Confident", "description": "Brisker transitions with the same reading holds."},
        {"label": "Punchy", "description": "Beat-driven cuts and impacts, fewer words on screen."}
      ]
    }
  ]
}
```

## 3. Refine the Chosen Direction

When the answers arrive, read the chosen card's Dials. Ask a second call with only the dials that
the brief and earlier answers have not settled and that would visibly change the video. Often that
is one or two questions, sometimes none. Skip the call when nothing material is open.

When the user picks `Other` and describes or links their own look, study the reference, ask for it
if it is missing, and write a custom card from the [template](../styles/index.md#card-template).
When the user picks `Your call`, choose yourself and record the choice as an assumption.

If the user declines to answer, proceed with the recommended options and say so in one line.

## 4. Output

Append the style direction to the brief:

- The base card or custom card, and any blend.
- How it adapts to this subject: the palette remap, the motif idea, and any type swaps.
- The answer to every dial asked, and your choices for the rest, recorded as assumptions.

Wait for the answers to each call before continuing. Continue with [Research](research.md).
