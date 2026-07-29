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
- Use the bundled scripts for generated automation: `config.py` for destinations and `send.py` for
  delivery. Treat the curl snippets in the reference as protocol examples, not script templates.
- Do not send interactive components. Do not edit, fetch, or delete webhook messages.
- Do not ask for confirmation after an explicit send request. Clarify only missing or ambiguous
  destination, content, files, thread, poll, or mention behavior.

## Locate the bundled resources

Set `SKILL_DIR` to the absolute directory containing this `SKILL.md`, using the path supplied by the
host when it loaded the skill. In a generated shell script, require that host-supplied path; never
derive it from `$0`, the current directory, or a filesystem search:

```bash
: "${SKILL_DIR:?Set SKILL_DIR to the discord-webhooks skill directory}"
python3 "$SKILL_DIR/scripts/config.py" init
```

Run `config.py init` before every generated config-management or delivery workflow, even though
the helpers can create the config lazily.

Use:

- `scripts/config.py` for config creation, URL validation, and alias operations.
- `scripts/send.py` for actual delivery. It resolves destination fallbacks, validates and
  normalizes the payload, keeps the URL out of the curl process arguments, handles bounded HTTP
  429 retries, and preserves duplicate-safe failure semantics.
- `references/discord-webhook-api.md` for payload fields, limits, and curl examples. Read it before
  sending anything beyond a basic text message.

## Manage destinations

The helper stores a flat name-to-URL mapping at `~/.discord-webhooks/config.yaml`. It creates the
directory and file when absent, with directory mode `0700` and file mode `0600`.

Initialize the config at the start of any config or send operation:

```bash
python3 "$SKILL_DIR/scripts/config.py" init
```

For sends, `scripts/send.py` resolves destinations in this order:

1. If the user names a destination such as `xablau`, resolve that alias from the config.
2. If the alias is absent, use an explicit webhook URL supplied for this request.
3. Otherwise, use `DISCORD_WEBHOOK_URL` when it is non-empty.
4. If none resolves, ask the user for a saved alias or webhook URL.

Resolve an alias manually only for config inspection or maintenance. Capture it without displaying
its URL:

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

1. Require the host-provided `SKILL_DIR` and run `config.py init`.
2. Translate the user's request into a Discord payload. Require at least one of `content`, `embeds`,
   `poll`, non-interactive `components`, or a file.
3. Include `allowed_mentions.parse: []` unless the user explicitly requests notifications. The
   sender also injects this safe default when the field is absent, but include it in generated
   payloads so their safety is visible.
4. Serialize dynamic content with a JSON serializer. Do not interpolate untrusted text into JSON or
   shell syntax.
5. For Components V2, use only non-interactive display and layout types documented in the
   reference. Do not combine them with `content`, `embeds`, `poll`, or files. Do not put
   `flags: 32768` or `with_components` in a payload sent through `send.py`; the sender adds the
   required flag and query parameter.
6. Put `thread_name` and
   `applied_tags` in the payload when creating a forum or media-channel thread.
7. Write the JSON to a mode-`0600` temporary file and invoke `scripts/send.py`—never call curl
   directly from generated automation. It uses
   `application/json` without files and `multipart/form-data` with `payload_json` and indexed
   `files[n]` parts for attachments.

Use this secure temporary-file pattern in generated shell scripts:

```bash
umask 077
PAYLOAD_FILE="$(mktemp)"
chmod 600 "$PAYLOAD_FILE"
trap 'rm -f "$PAYLOAD_FILE"' EXIT HUP INT TERM
```

Write dynamic payloads with `python3` and `json.dump`; pass values through Python arguments or
environment variables rather than interpolating them into a JSON heredoc.

Send to a named alias, allowing automatic fallback to `DISCORD_WEBHOOK_URL` if the alias is absent:

```bash
python3 "$SKILL_DIR/scripts/send.py" \
  --alias "$DESTINATION" \
  --payload "$PAYLOAD_FILE"
```

When the user supplies an explicit fallback URL, keep it out of process arguments:

```bash
printf '%s\n' "$EXPLICIT_WEBHOOK_URL" |
  python3 "$SKILL_DIR/scripts/send.py" \
    --alias "$DESTINATION" \
    --explicit-url-stdin \
    --payload "$PAYLOAD_FILE"
```

Omit `--alias "$DESTINATION"` when the user supplies only a URL and no destination name.

For a URL-only script that reads `DISCORD_WEBHOOK_URL`, use this exact validation and delivery
shape:

```bash
: "${DISCORD_WEBHOOK_URL:?Set DISCORD_WEBHOOK_URL}"
printf '%s\n' "$DISCORD_WEBHOOK_URL" |
  python3 "$SKILL_DIR/scripts/config.py" validate --stdin
printf '%s\n' "$DISCORD_WEBHOOK_URL" |
  python3 "$SKILL_DIR/scripts/send.py" \
    --explicit-url-stdin \
    --payload "$PAYLOAD_FILE"
```

Add an existing thread and one or more files as needed:

```bash
python3 "$SKILL_DIR/scripts/send.py" \
  --alias "$DESTINATION" \
  --payload "$PAYLOAD_FILE" \
  --thread-id "$THREAD_ID" \
  --file "$FILE_PATH"
```

The sender validates the official Discord URL, permits supported non-interactive components while
rejecting interactive or unsupported types, injects safe mention defaults, validates common
Discord limits, adds `wait=true` (and `with_components=true` when needed), and calls `curl`
immediately. It never performs a general retry after transport errors or HTTP 5xx responses.

Use the curl examples in `references/discord-webhook-api.md` only to understand Discord's raw HTTP
shape. Generated scripts must use `send.py` so URL secrecy, validation, retries, and
duplicate-safe failure behavior remain consistent.

## Handle the response

- Treat a successful 2xx response with `wait=true` as confirmed. Report the destination alias or
  source and returned message ID when available, but never the URL or token.
- The sender handles HTTP 429 by reading `Retry-After` or `retry_after`, waiting that duration, and
  retrying at most three times. A 429 rejects the request, so this bounded retry does not duplicate
  an accepted message.
- On HTTP 400, report Discord's validation error and correct the payload only when the intent is
  unambiguous.
- On HTTP 401, 403, or 404, stop without retrying. Explain that the webhook may be invalid,
  unauthorized, deleted, or unable to post in the target channel.
- On a timeout, transport failure, or HTTP 5xx after a POST, do not automatically resend. Report
  that delivery is uncertain because the message may already have been accepted.
