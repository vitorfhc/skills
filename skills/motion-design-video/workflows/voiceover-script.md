# Voiceover Script

When `voiceover` is `yes`, deliver a voiceover script with the video: a complete guide a narrator
can record from, synced to the picture.

- Draft it during [Concept and structure](concept.md). The narration sets the beat timing.
- Time the animation to it during [Animate](animate.md).
- Finalize it during [Review and deliver](review.md), with every timestamp measured from the final
  render.

Save it next to the video as `<video-name>.voiceover.md`, written in the language of the user's
request.

## Header

- Title and subject.
- Video file name, total runtime, and aspect ratio.
- Narration word count and average pace, such as "64 words at 1.9 words per second".
- Voice direction for the whole piece: tone, energy, and listener, such as "calm and confident,
  explaining to a fellow developer".

## Cue Table

One row per narration line or silence, in order, covering the whole runtime with no gaps:

| Column | Content |
|--------|---------|
| Time | Start and end as `MM:SS.s`, such as `00:04.5–00:09.0` |
| On screen | What the viewer sees during the cue, in a few words |
| Narration | The exact words to say, or *(silence)* |
| Direction | Tone, stressed words, pauses, and sync points |

Mark a sync point whenever a word must land on a visual event. Name the word and the timestamp,
such as "Say **resolver** as it turns cyan at 00:09.2".

Example:

| Time | On screen | Narration | Direction |
|------|-----------|-----------|-----------|
| 00:00.0–00:01.5 | Empty grid; a single line draws in | *(silence)* | Lead-in. |
| 00:01.5–00:08.0 | The line becomes an address bar typing `example.com` | "Every visit to a website starts with a question: where is it?" | Curious, unhurried. Stress **where**. |
| 00:08.0–00:14.5 | The query travels to a resolver, which turns cyan | "Your computer asks a resolver, which does the searching for you." | Say **resolver** as it turns cyan at 00:10.0. |

## Pronunciation

List every name, acronym, and technical term a narrator might misread, with how to say it, such as
"TTL: tee-tee-ell".

## Writing Rules

- Write for the ear: short sentences, one idea per sentence, active voice, plain words.
- Fit each line into its cue at no more than about 2.2 words per second (130 words per minute),
  ending at least half a second before the cue does: words ≤ 2.2 × (cue seconds − 0.5).
- Count the words of every line against its cue length. Never let a line overrun its cue.
- Complement the on-screen text. Never read it aloud word for word, and never contradict it.
- State only what [Research](research.md) verified.
