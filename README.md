# Agent skills

Reusable, standalone agent skills published by Vitor Falcão.

## Discord Webhooks

`discord-webhooks` sends Discord incoming webhooks with `curl` and manages named webhook
destinations in `~/.discord-webhooks/config.yaml`.

It supports text, embeds, polls, TTS, attachments, forum and thread messages, username and avatar
overrides, safe mentions, notification flags, and non-interactive Components V2 layouts. It
intentionally excludes interactive components and message editing or deletion. A bundled sender
validates payloads and destinations, keeps webhook URLs out of curl process arguments, handles
Discord rate limits, and avoids automatic retries when delivery could be ambiguous.

Install it with [`npx skills`](https://github.com/vercel-labs/skills):

```bash
npx --yes skills add vitorfhc/skills --skill discord-webhooks
```

For a non-interactive global Codex installation:

```bash
npx --yes skills add vitorfhc/skills \
  --skill discord-webhooks \
  --agent codex \
  --global \
  --yes
```

Example requests after installation:

```text
Save this Discord webhook as xablau: <webhook URL>
Send "deployment completed" to the xablau Discord webhook
Send report.txt to xablau with an embed and no notifications
List my Discord webhook aliases
Remove the xablau webhook alias
```

The skill creates the config when needed and secures the directory and file with modes `0700` and
`0600`. The config is a flat YAML mapping:

```yaml
xablau: "https://discord.com/api/webhooks/..."
alerts: "https://discord.com/api/webhooks/..."
```

Webhook URLs contain secret tokens. Do not commit, print, or share the config.

## Motion Design Video

`motion-design-video` turns a subject into a premium motion-design video: researched, storyboarded,
and animated with precise typography, geometric transformations, continuous transitions, and a
consistent design system. It suits explainers, product showcases, brand introductions, promotional
content, and technical visualizations.

The skill works as a back-and-forth with you, using Claude Code's `AskUserQuestion` tool, or plain
messages for agents without it:

1. **Clarify:** questions about the goal, audience, and format. Length, aspect ratio, and voiceover
   are always your choice, so it asks for each one you do not set as a parameter.
2. **Style direction:** a second round about the look, offering two or three directions tailored to
   your subject, with ASCII previews and palettes, then refining the chosen one.
3. **Design:** after researching and storyboarding, it renders style frames for your approval.
4. **Animation:** it renders a draft and asks for your reaction before the final render.
5. **Review:** it checks the final render, delivers it, and offers a round of revisions.

It never asks you to design scenes, timing, or transitions; it proposes and you react. The only hard
rules live in `principles.md`: pacing, legibility, semantic color, continuity, safe areas, and
effects that serve meaning. The look comes from a library of style cards in `styles/`, which the
agent adapts, blends, or extends with a custom card for your reference:

| Style | Essence |
|-------|---------|
| Editorial Minimal | Precise geometry and type on a dark field |
| Blueprint Pencil | One unbroken line evolving from sketch to blueprint to hologram |
| Technical Drawing | An engineering sheet drawing itself around a turning object |
| Halftone Xerox | Photocopied zine with dot screens, few inks, and misregistration |
| Kinetic HUD | Beat-driven type, interface fragments, and camera hits |
| Refractive Glass | A hero object of glass bending the scene behind it |
| Exploded Cutaway | A real object cut open and separated into labeled parts |
| Continuous Flight | One camera journey through waypoints in a world |
| Soft-Body Toy | Squishy gummy objects that squash, bounce, and jiggle |
| Swiss Kinetic Type | Huge type on a strict grid, moving with the sentence |
| Data Story | Charts that build, morph, and annotate one highlighted series |

It renders with a short side of at least 1080 pixels. It bundles no renderer. The agent animates
with the tools available in its environment and reports anything it could not render.

Install it with:

```bash
npx --yes skills add vitorfhc/skills --skill motion-design-video
```

Example requests after installation:

```text
Make a motion-design video explaining how DNS resolution works
Create a 15-second product intro for our CLI tool
Animate the idea of compound interest as an abstract loop
```

Set any of these parameters up front to skip its question:

| Parameter | Values |
|-----------|--------|
| `duration` | Seconds or minutes, such as `45s`, `2m`, or `1m30s` |
| `aspect` | Width to height, such as `16:9`, `9:16`, `1:1`, or `4:5` |
| `voiceover` | `yes` when narration will be recorded over the video later, otherwise `no` |

```text
/motion-design-video duration=45s aspect=9:16 voiceover=yes how DNS resolution works
```

In agents without slash commands, include the same `name=value` pairs or plain language, such as
"a 45-second vertical video we will narrate later", in the request. With `voiceover=yes`, the video
leaves room for narration, keeps on-screen text sparse, and ships with a voiceover script next to
the video: timestamped cues with what is on screen, the exact words to say, delivery direction,
sync points, and a pronunciation guide.

## Guided Goal

`guided-goal` turns a rough objective into a well-defined goal for goal mode, the persistent
autonomous loop behind `/goal` in Claude Code and Codex. It is a port of Oh My Pi's `/guided-goal`.

It interviews you one question at a time, six questions or fewer, until five things are settled:

1. **Success criteria** that can be checked without judgment, such as tests passing or a command
   exiting 0.
2. **Verification:** the exact commands the agent runs to check its own work.
3. **Attempt cap:** a maximum number of turns or tries. In Codex it also asks for a token budget,
   the only limit Codex enforces; elsewhere the budget is optional.
4. **Boundaries:** what is in scope and what must not be touched.
5. **Stop conditions:** when the agent halts and hands control back to you.

It then writes the goal under fixed headings (Objective, Success criteria, Verification, Boundaries,
Stop conditions) and starts it:

- **Codex:** it calls Codex's `create_goal` tool with the token budget and starts working. Codex
  ends a goal only when the agent marks it complete, or blocked after the same blocker recurs on
  three turns, so the goal tells the agent to stop working and mark it blocked when a stop condition
  fires.
- **Claude Code:** the model cannot set a goal itself, so it hands you a ready `/goal` command and
  copies it to the clipboard when a shell is available. Claude Code's goal checker reads only the
  conversation, so the goal requires the agent to show its verification output and makes the stop
  conditions end the goal.

Install it with:

```bash
npx --yes skills add vitorfhc/skills --skill guided-goal
```

Example requests after installation:

```text
/guided-goal make the flaky auth tests pass
$guided-goal migrate the billing module to the new API client
Help me write a /goal for splitting utils.ts into smaller modules
```

## Development

Run the deterministic test suite with:

```bash
python3 -m unittest discover -s tests -v
```

The tests use a curl stand-in plus a local HTTPS fixture for real multipart `curl` coverage. They do
not contact Discord or send live messages.

## Sources

The Discord Webhooks skill incorporates the
[Discord Webhooks Guide](https://birdie0.github.io/discord-webhooks-guide/discord_webhook.html) and
cross-checks it against the current
[official Discord webhook documentation](https://docs.discord.com/developers/resources/webhook#execute-webhook).

The Motion Design Video style cards are distilled from the community showcase at
[skillry.dev/ai-videos](https://skillry.dev/ai-videos/opus-5-5), adapted from interactive and
real-time pieces where needed so they render as video.

The Guided Goal interview is adapted from the `/guided-goal` prompt in
[Oh My Pi](https://github.com/can1357/oh-my-pi) (MIT), and its hand-off follows the documented
behavior of [Claude Code's `/goal`](https://code.claude.com/docs/en/goal) and Codex's
[`create_goal` tool](https://github.com/openai/codex/blob/main/codex-rs/ext/goal/src/spec.rs).

## License

[MIT](LICENSE)
