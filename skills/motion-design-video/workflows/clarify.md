# Clarify

Ask the user clarifying questions about their prompt before researching or designing. The answers
become the creative brief that every later workflow follows.

## 1. Read the Request

Read the prompt and any attached material, such as brand guidelines, logos, product screenshots,
scripts, or reference videos. Note what it already settles: subject, objective, audience, tone,
duration, aspect ratio, voiceover, language, and delivery constraints.

Check which parameters are set, either as `name=value` in the skill arguments or the request, or in
plain language: `duration`, `aspect`, and `voiceover`.

Do not research the subject yet. The questions are about the user's intent, not subject facts.

## 2. Choose the Questions

Duration, aspect ratio, and voiceover are required. Ask for each one that its parameter does not
already set.

Then add a question for every other dimension that is still open and would materially change the
video:

| Dimension | What the answer decides |
|-----------|-------------------------|
| Objective | Explainer, product showcase, brand introduction, promotion, conceptual piece, or technical visualization |
| Audience | Prior knowledge, depth of explanation, and vocabulary |
| Central message | The one idea the viewer must understand, remember, or feel |
| Visual direction | The default identity, an existing brand, or a different mood |
| Destination | Website, social feed, talk, or presentation, which shapes the opening hook and pacing |
| Ending | A seamless loop or a definitive conclusion, such as a call to action |
| Music | Silent, or synced to a music track the user supplies |

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

- It accepts up to four questions per call. Put the required questions first, then the most
  consequential ones. When more remain, ask them in another call after the answers arrive.
- Give each question a `header` chip of 12 characters or fewer, such as `Duration`, `Aspect`, or
  `Voiceover`.
- Give each two to four concrete, mutually exclusive `options`, each with a `description` of what
  choosing it changes in the video. The user can always pick "Other", so never add one.
- Put the option you recommend first and append `(Recommended)` to its label.
- For duration, offer lengths that suit the subject and describe what each length can cover.
- For aspect ratio, offer ratios that suit likely destinations, such as `9:16` for Reels and other
  vertical short-form video, `16:9` for websites and talks, `1:1` or `4:5` for social feeds.
  Recommend `9:16` unless the request points to a website, talk, or presentation.
- For voiceover, ask whether narration will be recorded over the video later, and describe how
  each answer changes text density and pacing.
- The user can enter any other value under "Other".
- Set `multiSelect: true` only when choices can combine, such as which product features to show.
- Add a `preview` only when an ASCII mockup or palette sample helps compare visual directions.

Example first call for "Make a motion-design video about how DNS resolution works":

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
      "question": "Which aspect ratio should the video use?",
      "header": "Aspect",
      "multiSelect": false,
      "options": [
        {"label": "9:16 (Recommended)", "description": "Vertical frame for Reels, Shorts, and TikTok."},
        {"label": "16:9", "description": "Wide frame for websites, talks, and YouTube."},
        {"label": "1:1", "description": "Square frame for social feeds."},
        {"label": "4:5", "description": "Portrait frame for Instagram and LinkedIn feeds."}
      ]
    },
    {
      "question": "Will narration be recorded over the video later?",
      "header": "Voiceover",
      "multiSelect": false,
      "options": [
        {"label": "No voiceover (Recommended)", "description": "Visuals and on-screen text carry the whole message."},
        {"label": "Voiceover later", "description": "Leaves room for narration, keeps text sparse, and includes a full voiceover script."}
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
    }
  ]
}
```

A second call would then ask about the central message.

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
- Duration, aspect ratio, and voiceover.
- Destination, ending, and music.
- Anything the user wrote under "Other" or in notes, verbatim when it is a constraint.

For anything still open, choose the recommended default and record it as an assumption. The brief
overrides the defaults in SKILL.md wherever they conflict.

Continue with [Research](research.md).
