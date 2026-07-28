---
name: discord-webhooks
description: Send messages through Discord incoming webhooks with curl and manage named webhook destinations. Use when the user asks to send or post a Discord webhook; send text, rich embeds, polls, TTS, files or attachments, forum or thread messages, username or avatar overrides, mention controls, or notification flags; or save, list, resolve, or remove aliases in ~/.discord-webhooks/config.yaml. Sending only; do not edit or delete webhook messages or create interactive components.
---

# Discord Webhooks

Send an explicitly requested webhook immediately after resolving the destination and payload. Use
Discord's incoming webhook endpoint directly with `curl`.

## Guardrails

- Treat every webhook URL as a secret because it contains a token.
- Never print, log, commit, summarize, or include a webhook URL in the final response.
- Never place a literal webhook URL in an example. Keep the resolved value in `WEBHOOK_URL`.
- Never persist a URL unless the user explicitly asks to save it as an alias.
- Never follow redirects when sending. Require HTTPS and validate the URL with the bundled helper.
- Default to `"allowed_mentions": {"parse": []}`. Enable only the exact mentions the user requests.
- Always add `wait=true` so Discord confirms creation and returns the message.
- Do not send interactive components. Do not edit, fetch, or delete webhook messages.
- Do not ask for confirmation after an explicit send request. Clarify only missing or ambiguous
  destination, content, files, thread, poll, or mention behavior.

## Locate the bundled resources

Set `SKILL_DIR` to the absolute directory containing this `SKILL.md`, using the path supplied by the
host when it loaded the skill. Do not search the whole filesystem.

Use:

- `scripts/config.py` for config creation, URL validation, and alias operations.
- `references/discord-webhook-api.md` for payload fields, limits, and curl examples. Read it before
  sending anything beyond a basic text message.

## Manage destinations

The helper stores a flat name-to-URL mapping at `~/.discord-webhooks/config.yaml`. It creates the
directory and file when absent, with directory mode `0700` and file mode `0600`.

Initialize the config at the start of any config or send operation:

```bash
python3 "$SKILL_DIR/scripts/config.py" init
```

Resolve destinations in this order:

1. If the user names a destination such as `xablau`, resolve that alias from the config.
2. If the alias is absent, use an explicit webhook URL supplied for this request.
3. Otherwise, use `DISCORD_WEBHOOK_URL` when it is non-empty.
4. If none resolves, ask the user for a saved alias or webhook URL.

Capture an alias without displaying its URL:

```bash
WEBHOOK_URL="$(python3 "$SKILL_DIR/scripts/config.py" resolve "$DESTINATION")"
```

Validate any explicit or environment-provided URL before sending:

```bash
printf '%s\n' "$WEBHOOK_URL" |
  python3 "$SKILL_DIR/scripts/config.py" validate --stdin
```

Support these explicit alias-management requests:

```bash
# Save or replace an alias without passing the URL as a process argument.
printf '%s\n' "$WEBHOOK_URL" |
  python3 "$SKILL_DIR/scripts/config.py" set "$DESTINATION" --stdin

# List names only. Never resolve or display their URLs for a list request.
python3 "$SKILL_DIR/scripts/config.py" list

# Remove an alias.
python3 "$SKILL_DIR/scripts/config.py" remove "$DESTINATION"
```

Do not silently save a fallback URL under a missing alias.

## Send a message

1. Resolve and validate `WEBHOOK_URL`.
2. Translate the user's request into a Discord payload. Require at least one of `content`, `embeds`,
   `poll`, or a file.
3. Add `allowed_mentions.parse: []` unless the user explicitly requests notifications.
4. Serialize dynamic content with a JSON serializer. Do not interpolate untrusted text into JSON or
   shell syntax.
5. Use `application/json` for messages without files. Use `multipart/form-data` with
   `payload_json` and indexed `files[n]` parts for attachments.
6. Add `thread_id` as a query parameter for an existing thread. Put `thread_name` and
   `applied_tags` in the payload when creating a forum or media-channel thread.
7. Execute immediately with `curl`. Do not use a general POST retry option because an ambiguous
   timeout or server error could duplicate a message.

Basic text pattern:

```bash
curl --proto '=https' \
  --silent --show-error --fail-with-body \
  --connect-timeout 10 --max-time 30 \
  --request POST \
  --header 'Content-Type: application/json' \
  --data-binary @- \
  "${WEBHOOK_URL}?wait=true" <<'JSON'
{
  "content": "Deployment completed.",
  "allowed_mentions": {"parse": []}
}
JSON
```

For dynamic content, write a mode-`0600` temporary payload with `python3` and `json.dump`, send it
with `--data-binary "@$PAYLOAD_FILE"`, then remove it. Keep temporary response bodies mode `0600`
too.

## Handle the response

- Treat a successful 2xx response with `wait=true` as confirmed. Report the destination alias or
  source and returned message ID when available, but never the URL or token.
- On HTTP 429, read `Retry-After` or `retry_after`, wait that duration, and retry at most three
  times. A 429 rejects the request, so this bounded retry does not duplicate an accepted message.
- On HTTP 400, report Discord's validation error and correct the payload only when the intent is
  unambiguous.
- On HTTP 401, 403, or 404, stop without retrying. Explain that the webhook may be invalid,
  unauthorized, deleted, or unable to post in the target channel.
- On a timeout, transport failure, or HTTP 5xx after a POST, do not automatically resend. Report
  that delivery is uncertain because the message may already have been accepted.
