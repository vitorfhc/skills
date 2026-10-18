# Clarify

Ask the user clarifying questions about their prompt before researching or designing. The answers
become the creative brief that every later workflow follows.

## 1. Read the Request

Read the prompt and any attached material, such as brand guidelines, logos, product screenshots,
scripts, or reference videos. Note what it already settles: subject, objective, audience, tone,
duration, format, language, and delivery constraints.

Check whether the `duration` parameter is set, either as `duration=<length>` in the skill arguments
or the request, or as a length stated in plain language.

Do not research the subject yet. The questions are about the user's intent, not subject facts.

## 2. Choose the Questions

Duration is required. Ask for it unless the `duration` parameter already sets it.

Then add a question for every other dimension that is still open and would materially change the
video:

| Dimension | What the answer decides |
|-----------|-------------------------|
| Objective | Explainer, product showcase, brand introduction, promotion, conceptual piece, or technical visualization |
| Audience | Prior knowledge, depth of explanation, and vocabulary |
| Central message | The one idea the viewer must understand, remember, or feel |
| Visual direction | The default identity, an existing brand, or a different mood |
| Format | Aspect ratio and destination, such as a website, social feed, or talk |
| Ending | A seamless loop or a definitive conclusion, such as a call to action |
| Audio | Silent, synced to a supplied music track, or timed for a voiceover |

Rules for choosing:

- There is no fixed number of questions. Ask as many as the request needs, and no more. Every
  question should change the video.
- Ask about intent, never about craft. Scenes, keyframes, transitions, layers, camera, timing, and
  visual metaphors are yours to decide.
- Do not ask what the prompt or parameters already answer clearly.
- Tailor each question and its options to the subject. "Who is the DNS video for?" beats "Who is
  the audience?".

## 3. Ask

Ask with `AskUserQuestion`:

- It accepts up to four questions per call. Put the duration and the most consequential questions
  in the first call. When more remain, ask them in another call after the answers arrive.
- Give each question a `header` chip of 12 characters or fewer, such as `Audience`, `Duration`, or
  `Format`.
- Give each two to four concrete, mutually exclusive `options`, each with a `description` of what
  choosing it changes in the video. The user can always pick "Other", so never add one.
- Put the option you recommend first and append `(Recommended)` to its label.
- For duration, offer lengths that suit the subject and destination, and describe what each length
  can cover. The user can enter any other length under "Other".
- Set `multiSelect: true` only when choices can combine, such as which product features to show.
- Add a `preview` only when an ASCII mockup or palette sample helps compare visual directions.

Example for "Make a motion-design video about how DNS resolution works":

```json
{
  "questions": [
    {
      "question": "How long should the DNS video be?",
      "header": "Duration",
      "multiSelect": false,
      "options": [
        {"label": "30 seconds (Recommended)", "description": "The full lookup from browser to authoritative server."},
        {"label": "15 seconds", "description": "Only the delegation chain, with no detail."},
        {"label": "60 seconds", "description": "Adds caching and TTLs after the lookup."},
        {"label": "2 minutes", "description": "Adds record types and a failure case."}
      ]
    },
    {
      "question": "Who is the DNS video for?",
      "header": "Audience",
      "multiSelect": false,
      "options": [
        {"label": "Developers (Recommended)", "description": "Name resolvers, record types, and TTLs with technical labels."},
        {"label": "General public", "description": "Show the lookup as a journey with minimal jargon."},
        {"label": "Students", "description": "Build up hop by hop and define each component."}
      ]
    },
    {
      "question": "What should viewers remember after watching?",
      "header": "Message",
      "multiSelect": false,
      "options": [
        {"label": "Delegation chain (Recommended)", "description": "Root, TLD, and authoritative servers each point to the next."},
        {"label": "Caching speed", "description": "Most lookups never leave the local resolver."},
        {"label": "Fragility", "description": "One misconfigured record can take a site offline."}
      ]
    },
    {
      "question": "Where will the video be shown?",
      "header": "Format",
      "multiSelect": false,
      "options": [
        {"label": "Website or talk (Recommended)", "description": "16:9 with a definitive ending."},
        {"label": "Social feed", "description": "9:16 vertical with a fast opening hook."},
        {"label": "Background loop", "description": "16:9 seamless loop with minimal text."}
      ]
    }
  ]
}
```

Wait for the answers. Do not start research, design, or implementation in the same turn.

If `AskUserQuestion` is unavailable, ask the same questions in one message as a numbered list with
lettered options, and wait for the reply. If the user declines to answer, proceed with the
recommended options and say so in one line.

## 4. Write the Brief

Turn the parameters and answers into a short internal creative brief:

- Subject and objective.
- Audience and depth.
- Central message.
- Visual direction and brand constraints.
- Duration, aspect ratio, ending, and audio.
- Anything the user wrote under "Other" or in notes, verbatim when it is a constraint.

For anything still open, choose the recommended default and record it as an assumption. The brief
overrides the defaults in SKILL.md wherever they conflict.

Continue with [Research](research.md).
