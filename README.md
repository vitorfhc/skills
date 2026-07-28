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

## Development

Run the deterministic test suite with:

```bash
python3 -m unittest discover -s tests -v
```

The tests use a curl stand-in plus a local HTTPS fixture for real multipart `curl` coverage. They do
not contact Discord or send live messages.

## Sources

The skill incorporates the
[Discord Webhooks Guide](https://birdie0.github.io/discord-webhooks-guide/discord_webhook.html) and
cross-checks it against the current
[official Discord webhook documentation](https://docs.discord.com/developers/resources/webhook#execute-webhook).

## License

[MIT](LICENSE)
