# Discord incoming webhook reference

Use this reference for send-only incoming webhooks. Do not use message edit, delete, fetch, or
interactive-component endpoints.

## Sources and authority

This reference incorporates the payload anatomy and examples from the
[Discord Webhooks Guide](https://birdie0.github.io/discord-webhooks-guide/discord_webhook.html).
Discord's current official documentation is authoritative when it differs:

- [Webhook resource and Execute Webhook](https://docs.discord.com/developers/resources/webhook#execute-webhook)
- [Component reference](https://docs.discord.com/developers/components/reference)
- [Message embeds and allowed mentions](https://docs.discord.com/developers/resources/message)
- [Poll request objects](https://docs.discord.com/developers/resources/poll#poll-create-request-object)
- [Uploading files](https://docs.discord.com/developers/reference#uploading-files)
- [Rate limits](https://docs.discord.com/developers/topics/rate-limits)

## Execute endpoint

Send `POST` requests to the secret URL Discord provides:

```text
https://discord.com/api/webhooks/{webhook.id}/{webhook.token}
```

Always add `wait=true`. Without it, Discord can return `204` and some unsaved messages may not
surface an error.

Supported query parameters:

| Parameter | Purpose |
| --- | --- |
| `wait=true` | Wait for confirmation and return the created message. |
| `thread_id=<snowflake>` | Send to an existing thread and unarchive it if necessary. |
| `with_components=true` | Respect non-interactive components sent by an incoming webhook. |

Set `with_components=true` only when sending the supported non-interactive Components V2 payloads
described below.

## JSON and form fields

At least one of `content`, `embeds`, `poll`, `components`, or `files[n]` is required.

| Field | Purpose and constraints |
| --- | --- |
| `content` | Message text, up to 2,000 characters. |
| `username` | Override the webhook's display name for this send. |
| `avatar_url` | Override the webhook's avatar with an HTTP(S) image URL. |
| `tts` | Send as text-to-speech when `true` and permitted. |
| `embeds` | Up to 10 rich embed objects, with 6,000 total text characters across them. |
| `allowed_mentions` | Control which textual mentions notify users. |
| `components` | Non-interactive Components V2 display and layout objects. |
| `files[n]` | Indexed multipart file parts such as `files[0]`. |
| `payload_json` | JSON-encoded non-file fields in a multipart request. |
| `attachments` | Metadata for uploaded files; IDs must match each `files[n]` index. |
| `flags` | `4` suppresses embeds, `4096` suppresses notifications, and `32768` enables Components V2. |
| `thread_name` | Create a thread in a forum or media channel. |
| `applied_tags` | Tag IDs to apply with `thread_name` in a forum or media channel. |
| `poll` | Create a poll with question, answers, duration, and selection behavior. |

## Mentions

Suppress all notifications by default:

```json
{"allowed_mentions":{"parse":[]}}
```

Only enable a mention type when the user explicitly asks. Mention syntax must also appear in the
content:

- User: `<@USER_ID>`
- Role: `<@&ROLE_ID>`
- Everyone or here: `@everyone` or `@here`

When specifying exact `users` or `roles` IDs, do not also include the same type in `parse`. A valid
targeted example is:

```json
{
  "content": "Hello <@123456789012345678>",
  "allowed_mentions": {
    "parse": [],
    "users": ["123456789012345678"]
  }
}
```

## Embeds

Webhook embeds support `title`, `description`, `url`, decimal `color`, `timestamp`, `author`,
`fields`, `thumbnail`, `image`, and `footer`. Do not send read-only fields such as `type`,
`provider`, `video`, proxy URLs, dimensions, or generated metadata.

Important limits:

| Embed value | Limit |
| --- | --- |
| Embed count | 10 |
| `title` | 256 characters |
| `description` | 4,096 characters |
| Fields | 25 per embed |
| `field.name` | 256 characters |
| `field.value` | 1,024 characters |
| `footer.text` | 2,048 characters |
| `author.name` | 256 characters |
| All textual embed fields combined | 6,000 characters across the message |

Convert a hex color to its decimal integer before sending, for example `0x5865F2` becomes
`5793266`.

## Polls

A poll request contains:

- `question.text`: question, up to 300 characters.
- `answers`: up to 10 entries, each with `poll_media.text` up to 55 characters and an optional
  emoji. Use `emoji.name` for built-in emoji or `emoji.id` for custom emoji.
- `duration`: integer hours, default 24, maximum 768 (32 days).
- `allow_multiselect`: boolean, default `false`.
- `layout_type`: currently `1`.

## Non-interactive components

Incoming webhooks may send non-interactive Components V2 when the request includes
`with_components=true` and the message has the `IS_COMPONENTS_V2` flag (`32768`). The bundled
sender adds both automatically when a valid `components` array is present.

Supported types:

| Type | Name | Placement and key constraints |
| --- | --- | --- |
| `9` | Section | Top-level or inside a Container; one to three Text Display children and one Thumbnail accessory. |
| `10` | Text Display | Top-level, inside a Section, or inside a Container; requires non-empty Markdown `content`. |
| `11` | Thumbnail | Only as a Section accessory; requires an external HTTP(S) `media.url`. |
| `12` | Media Gallery | Top-level or inside a Container; one to ten items with external HTTP(S) media URLs. |
| `14` | Separator | Top-level or inside a Container; optional boolean `divider` and spacing `1` or `2`. |
| `17` | Container | Top-level only; groups supported children and may set `accent_color` and `spoiler`. |

The sender rejects Action Rows, Buttons, Selects, inputs, and every other interactive or modal
component. It also rejects the File component (`13`) in this incoming-webhook flow: Discord's
Execute Webhook documentation says an `IS_COMPONENTS_V2` webhook message cannot include
`files[n]`, while a File component requires an uploaded `attachment://` reference. Send a normal
attachment without `components` instead.

Components V2 messages:

- Cannot contain `content`, `embeds`, `poll`, `attachments`, or uploaded `files[n]`.
- Can contain at most 40 component objects in total, including nested objects and accessories.
- May assign optional unique unsigned 32-bit integer `id` values. Discord treats `0` as unset.
- Still use `allowed_mentions`; Text Display mentions notify only when explicitly enabled.
- May use only external HTTP(S) media in this skill because file uploads are incompatible with this
  incoming-webhook request shape.

## Files

Use `multipart/form-data` whenever files are present:

- Put all non-file fields in the `payload_json` form part.
- Name each upload `files[n]`, starting at `files[0]`.
- Match each attachment metadata `id` to its `n`.
- Use `attachment://filename.ext` in an embed image, thumbnail, author icon, or footer icon to
  reference an uploaded image.
- Respect Discord's current per-file and request limits; they vary with account and server limits.
- Verify local paths and file sizes before sending.

## Curl examples

Assume `WEBHOOK_URL` already contains a validated, secret base URL. Never replace it with a literal
URL in commands or documentation. These examples show Discord's raw HTTP protocol. When producing
an executable workflow for a user, invoke `scripts/send.py` instead; it runs curl with the URL in a
private curl config and applies the safety rules from `SKILL.md`.

### Text, username, avatar, TTS, and flags

```bash
curl --proto '=https' \
  --silent --show-error --fail-with-body \
  --connect-timeout 10 --max-time 30 \
  --request POST \
  --header 'Content-Type: application/json' \
  --data-binary @- \
  "${WEBHOOK_URL}?wait=true" <<'JSON'
{
  "content": "Build completed.",
  "username": "Release Bot",
  "avatar_url": "https://example.com/release-bot.png",
  "tts": false,
  "flags": 4096,
  "allowed_mentions": {"parse": []}
}
JSON
```

### Rich embed

```bash
curl --proto '=https' \
  --silent --show-error --fail-with-body \
  --connect-timeout 10 --max-time 30 \
  --request POST \
  --header 'Content-Type: application/json' \
  --data-binary @- \
  "${WEBHOOK_URL}?wait=true" <<'JSON'
{
  "allowed_mentions": {"parse": []},
  "embeds": [
    {
      "author": {
        "name": "CI",
        "url": "https://example.com/builds/42",
        "icon_url": "https://example.com/ci.png"
      },
      "title": "Build 42 passed",
      "url": "https://example.com/builds/42",
      "description": "**Production** is ready.",
      "color": 5793266,
      "fields": [
        {"name": "Commit", "value": "`abc1234`", "inline": true},
        {"name": "Duration", "value": "2m 14s", "inline": true}
      ],
      "thumbnail": {"url": "https://example.com/thumb.png"},
      "image": {"url": "https://example.com/chart.png"},
      "footer": {
        "text": "Deployment pipeline",
        "icon_url": "https://example.com/footer.png"
      },
      "timestamp": "2026-07-28T19:00:00Z"
    }
  ]
}
JSON
```

### Poll

```bash
curl --proto '=https' \
  --silent --show-error --fail-with-body \
  --connect-timeout 10 --max-time 30 \
  --request POST \
  --header 'Content-Type: application/json' \
  --data-binary @- \
  "${WEBHOOK_URL}?wait=true" <<'JSON'
{
  "allowed_mentions": {"parse": []},
  "poll": {
    "question": {"text": "When should we deploy?"},
    "answers": [
      {"poll_media": {"text": "Now", "emoji": {"name": "🚀"}}},
      {"poll_media": {"text": "Tomorrow", "emoji": {"name": "🌅"}}}
    ],
    "duration": 24,
    "allow_multiselect": false,
    "layout_type": 1
  }
}
JSON
```

### Non-interactive Components V2

This raw-curl example includes `flags: 32768` and `with_components=true` because Discord requires
them at the HTTP layer. Do not copy either into a payload passed to `scripts/send.py`; the bundled
sender adds both automatically.

```bash
curl --proto '=https' \
  --silent --show-error --fail-with-body \
  --connect-timeout 10 --max-time 30 \
  --request POST \
  --header 'Content-Type: application/json' \
  --data-binary @- \
  "${WEBHOOK_URL}?wait=true&with_components=true" <<'JSON'
{
  "flags": 32768,
  "allowed_mentions": {"parse": []},
  "components": [
    {
      "type": 17,
      "accent_color": 5793266,
      "components": [
        {"type": 10, "content": "# Build passed\nProduction is ready."},
        {"type": 14, "divider": true, "spacing": 1},
        {
          "type": 12,
          "items": [
            {
              "media": {"url": "https://example.com/deployment.png"},
              "description": "Deployment status"
            }
          ]
        }
      ]
    }
  ]
}
JSON
```

### File with attachment metadata

```bash
curl --proto '=https' \
  --silent --show-error --fail-with-body \
  --connect-timeout 10 --max-time 60 \
  --request POST \
  --form-string 'payload_json={"content":"Report attached.","allowed_mentions":{"parse":[]},"attachments":[{"id":0,"filename":"report.txt","description":"Plain-text deployment report"}]}' \
  --form 'files[0]=@./report.txt;type=text/plain' \
  "${WEBHOOK_URL}?wait=true"
```

### Uploaded image inside an embed

```bash
curl --proto '=https' \
  --silent --show-error --fail-with-body \
  --connect-timeout 10 --max-time 60 \
  --request POST \
  --form-string 'payload_json={"allowed_mentions":{"parse":[]},"embeds":[{"title":"Metrics","image":{"url":"attachment://chart.png"}}],"attachments":[{"id":0,"filename":"chart.png","description":"Deployment metrics chart"}]}' \
  --form 'files[0]=@./chart.png;type=image/png' \
  "${WEBHOOK_URL}?wait=true"
```

### Existing thread

```bash
curl --proto '=https' \
  --silent --show-error --fail-with-body \
  --connect-timeout 10 --max-time 30 \
  --request POST \
  --header 'Content-Type: application/json' \
  --data-binary '{"content":"Thread update.","allowed_mentions":{"parse":[]}}' \
  "${WEBHOOK_URL}?wait=true&thread_id=${THREAD_ID}"
```

Require `THREAD_ID` to contain only decimal digits before using it in a query string.

### New forum or media-channel thread

```bash
curl --proto '=https' \
  --silent --show-error --fail-with-body \
  --connect-timeout 10 --max-time 30 \
  --request POST \
  --header 'Content-Type: application/json' \
  --data-binary @- \
  "${WEBHOOK_URL}?wait=true" <<'JSON'
{
  "thread_name": "Deployment 42",
  "applied_tags": ["123456789012345678"],
  "content": "Deployment completed.",
  "allowed_mentions": {"parse": []}
}
JSON
```

## Dynamic JSON

For user-supplied text, serialize rather than interpolating:

```bash
PAYLOAD_FILE="$(mktemp)"
chmod 600 "$PAYLOAD_FILE"
python3 - "$PAYLOAD_FILE" "$CONTENT" <<'PY'
import json
import sys

with open(sys.argv[1], "w", encoding="utf-8") as payload:
    json.dump(
        {
            "content": sys.argv[2],
            "allowed_mentions": {"parse": []},
        },
        payload,
        ensure_ascii=False,
    )
PY

curl --proto '=https' \
  --silent --show-error --fail-with-body \
  --connect-timeout 10 --max-time 30 \
  --request POST \
  --header 'Content-Type: application/json' \
  --data-binary "@$PAYLOAD_FILE" \
  "${WEBHOOK_URL}?wait=true"

rm -f "$PAYLOAD_FILE"
```

Use a trap or equivalent cleanup when an interruption could leave the temporary file behind.
