#!/usr/bin/env python3
"""Resolve a Discord webhook destination and deliver a payload through curl."""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from urllib.parse import urlencode, urlsplit

import config as webhook_config


COMPONENTS_V2_FLAG = 32768
ALLOWED_FLAGS = 4 | 4096 | COMPONENTS_V2_FLAG
MAX_REDACTED_ERROR = 4096
MAX_COMPONENTS = 40
TOP_LEVEL_FIELDS = {
    "content",
    "username",
    "avatar_url",
    "tts",
    "embeds",
    "allowed_mentions",
    "components",
    "attachments",
    "flags",
    "thread_name",
    "applied_tags",
    "poll",
}


class SendError(Exception):
    """A safe delivery error with a process exit code."""

    def __init__(self, message: str, exit_code: int = 2):
        super().__init__(message)
        self.exit_code = exit_code


def resolve_destination(
    config_path: Path, alias: str | None, explicit_url_stdin: bool
) -> tuple[str, str]:
    aliases = webhook_config.load_config(config_path)

    if alias is not None:
        webhook_config.validate_alias(alias)
        if alias in aliases:
            return aliases[alias], f"alias {alias}"

    if explicit_url_stdin:
        explicit_url = sys.stdin.readline().rstrip("\r\n")
        if explicit_url:
            webhook_config.validate_url(explicit_url)
            return explicit_url, "explicit URL"

    environment_url = os.environ.get("DISCORD_WEBHOOK_URL", "")
    if environment_url:
        webhook_config.validate_url(environment_url)
        return environment_url, "DISCORD_WEBHOOK_URL"

    if alias is not None:
        raise SendError(
            f"unknown webhook alias {alias!r} and no explicit or environment fallback"
        )
    raise SendError(
        "no webhook destination; provide an alias, explicit URL, or DISCORD_WEBHOOK_URL"
    )


def require_string(value: object, label: str, limit: int) -> str:
    if not isinstance(value, str):
        raise SendError(f"{label} must be a string")
    if len(value) > limit:
        raise SendError(f"{label} exceeds {limit} characters")
    return value


def reject_unknown_fields(value: dict, allowed: set[str], label: str) -> None:
    unknown = set(value) - allowed
    if unknown:
        names = ", ".join(sorted(unknown))
        raise SendError(f"{label} contains unsupported fields: {names}")


def validate_embeds(embeds: object) -> bool:
    if not isinstance(embeds, list):
        raise SendError("embeds must be an array")
    if len(embeds) > 10:
        raise SendError("embeds cannot contain more than 10 objects")
    if not embeds:
        return False

    total_characters = 0
    for embed_index, embed in enumerate(embeds):
        label = f"embeds[{embed_index}]"
        if not isinstance(embed, dict):
            raise SendError(f"{label} must be an object")
        reject_unknown_fields(
            embed,
            {
                "title",
                "description",
                "url",
                "timestamp",
                "color",
                "footer",
                "image",
                "thumbnail",
                "author",
                "fields",
            },
            label,
        )

        for key, limit in (("title", 256), ("description", 4096)):
            if key in embed:
                total_characters += len(
                    require_string(embed[key], f"{label}.{key}", limit)
                )

        for key in ("url", "timestamp"):
            if key in embed:
                require_string(embed[key], f"{label}.{key}", 2048)

        if "color" in embed:
            color = embed["color"]
            if (
                isinstance(color, bool)
                or not isinstance(color, int)
                or not 0 <= color <= 0xFFFFFF
            ):
                raise SendError(f"{label}.color must be a decimal RGB integer")

        author = embed.get("author")
        if author is not None:
            if not isinstance(author, dict):
                raise SendError(f"{label}.author must be an object")
            reject_unknown_fields(
                author,
                {"name", "url", "icon_url"},
                f"{label}.author",
            )
            if "name" not in author:
                raise SendError(f"{label}.author.name is required")
            author_name = require_string(author["name"], f"{label}.author.name", 256)
            if not author_name:
                raise SendError(f"{label}.author.name cannot be empty")
            total_characters += len(author_name)
            for key in ("url", "icon_url"):
                if key in author:
                    require_string(author[key], f"{label}.author.{key}", 2048)

        footer = embed.get("footer")
        if footer is not None:
            if not isinstance(footer, dict):
                raise SendError(f"{label}.footer must be an object")
            reject_unknown_fields(
                footer,
                {"text", "icon_url"},
                f"{label}.footer",
            )
            if "text" not in footer:
                raise SendError(f"{label}.footer.text is required")
            footer_text = require_string(footer["text"], f"{label}.footer.text", 2048)
            if not footer_text:
                raise SendError(f"{label}.footer.text cannot be empty")
            total_characters += len(footer_text)
            if "icon_url" in footer:
                require_string(
                    footer["icon_url"],
                    f"{label}.footer.icon_url",
                    2048,
                )

        for media_key in ("image", "thumbnail"):
            media = embed.get(media_key)
            if media is None:
                continue
            if not isinstance(media, dict):
                raise SendError(f"{label}.{media_key} must be an object")
            reject_unknown_fields(media, {"url"}, f"{label}.{media_key}")
            if "url" not in media:
                raise SendError(f"{label}.{media_key}.url is required")
            require_string(media["url"], f"{label}.{media_key}.url", 2048)

        fields = embed.get("fields", [])
        if not isinstance(fields, list):
            raise SendError(f"{label}.fields must be an array")
        if len(fields) > 25:
            raise SendError(f"{label}.fields cannot contain more than 25 objects")
        for field_index, field in enumerate(fields):
            field_label = f"{label}.fields[{field_index}]"
            if not isinstance(field, dict):
                raise SendError(f"{field_label} must be an object")
            reject_unknown_fields(
                field,
                {"name", "value", "inline"},
                field_label,
            )
            if "name" not in field or "value" not in field:
                raise SendError(f"{field_label} requires name and value")
            total_characters += len(
                require_string(field["name"], f"{field_label}.name", 256)
            )
            total_characters += len(
                require_string(field["value"], f"{field_label}.value", 1024)
            )
            if "inline" in field and not isinstance(field["inline"], bool):
                raise SendError(f"{field_label}.inline must be a boolean")

    if total_characters > 6000:
        raise SendError("embed text exceeds 6000 total characters")
    return True


def validate_poll(poll: object) -> bool:
    if not isinstance(poll, dict):
        raise SendError("poll must be an object")
    reject_unknown_fields(
        poll,
        {"question", "answers", "duration", "allow_multiselect", "layout_type"},
        "poll",
    )

    question = poll.get("question")
    if not isinstance(question, dict) or "text" not in question:
        raise SendError("poll.question.text is required")
    reject_unknown_fields(question, {"text"}, "poll.question")
    question_text = require_string(question["text"], "poll.question.text", 300)
    if not question_text:
        raise SendError("poll.question.text cannot be empty")

    answers = poll.get("answers")
    if not isinstance(answers, list) or not 2 <= len(answers) <= 10:
        raise SendError("poll.answers must contain between 2 and 10 answers")
    for answer_index, answer in enumerate(answers):
        label = f"poll.answers[{answer_index}].poll_media"
        if not isinstance(answer, dict) or not isinstance(
            answer.get("poll_media"), dict
        ):
            raise SendError(f"{label} is required")
        reject_unknown_fields(answer, {"poll_media"}, f"poll.answers[{answer_index}]")
        media = answer["poll_media"]
        reject_unknown_fields(media, {"text", "emoji"}, label)
        if "text" not in media:
            raise SendError(f"{label}.text is required")
        answer_text = require_string(media["text"], f"{label}.text", 55)
        if not answer_text:
            raise SendError(f"{label}.text cannot be empty")
        if "emoji" in media:
            emoji = media["emoji"]
            if not isinstance(emoji, dict):
                raise SendError(f"{label}.emoji must be an object")
            supplied = [key for key in ("id", "name") if emoji.get(key)]
            if len(supplied) != 1:
                raise SendError(f"{label}.emoji requires exactly one of id or name")
            reject_unknown_fields(emoji, set(supplied), f"{label}.emoji")
            require_string(emoji[supplied[0]], f"{label}.emoji.{supplied[0]}", 256)

    duration = poll.get("duration", 24)
    if isinstance(duration, bool) or not isinstance(duration, int):
        raise SendError("poll.duration must be an integer number of hours")
    if not 1 <= duration <= 768:
        raise SendError("poll.duration must be between 1 and 768 hours")
    if "allow_multiselect" in poll and not isinstance(poll["allow_multiselect"], bool):
        raise SendError("poll.allow_multiselect must be a boolean")
    if poll.get("layout_type", 1) != 1:
        raise SendError("poll.layout_type currently supports only 1")
    return True


def validate_attachments(attachments: object, file_count: int) -> None:
    if not isinstance(attachments, list):
        raise SendError("attachments must be an array")
    seen_ids: set[int] = set()
    for index, attachment in enumerate(attachments):
        if not isinstance(attachment, dict):
            raise SendError(f"attachments[{index}] must be an object")
        reject_unknown_fields(
            attachment,
            {"id", "filename", "description"},
            f"attachments[{index}]",
        )
        attachment_id = attachment.get("id")
        if isinstance(attachment_id, bool) or not isinstance(attachment_id, int):
            raise SendError(f"attachments[{index}].id must be an integer")
        if attachment_id in seen_ids:
            raise SendError(f"duplicate attachment id: {attachment_id}")
        if not 0 <= attachment_id < file_count:
            raise SendError(f"attachments[{index}].id does not match an uploaded file")
        seen_ids.add(attachment_id)
        if "filename" in attachment:
            filename = require_string(
                attachment["filename"],
                f"attachments[{index}].filename",
                1024,
            )
            if not filename:
                raise SendError(f"attachments[{index}].filename cannot be empty")
        if "description" in attachment:
            require_string(
                attachment["description"],
                f"attachments[{index}].description",
                1024,
            )


def validate_allowed_mentions(allowed_mentions: object) -> None:
    if not isinstance(allowed_mentions, dict):
        raise SendError("allowed_mentions must be an object")
    reject_unknown_fields(
        allowed_mentions,
        {"parse", "users", "roles", "replied_user"},
        "allowed_mentions",
    )

    parse = allowed_mentions.get("parse", [])
    if not isinstance(parse, list) or not all(isinstance(item, str) for item in parse):
        raise SendError("allowed_mentions.parse must be an array of strings")
    allowed_types = {"users", "roles", "everyone"}
    unknown_types = set(parse) - allowed_types
    if unknown_types:
        names = ", ".join(sorted(unknown_types))
        raise SendError(f"allowed_mentions.parse contains unknown types: {names}")
    if len(parse) != len(set(parse)):
        raise SendError("allowed_mentions.parse cannot contain duplicate types")

    for key in ("users", "roles"):
        if key not in allowed_mentions:
            continue
        ids = allowed_mentions[key]
        if (
            not isinstance(ids, list)
            or len(ids) > 100
            or not all(isinstance(item, str) and item.isdigit() for item in ids)
        ):
            raise SendError(
                f"allowed_mentions.{key} must be up to 100 decimal string IDs"
            )
        if key in parse:
            raise SendError(
                f"allowed_mentions cannot combine parse.{key} with explicit {key}"
            )

    if "replied_user" in allowed_mentions and not isinstance(
        allowed_mentions["replied_user"], bool
    ):
        raise SendError("allowed_mentions.replied_user must be a boolean")


def validate_external_media_item(media: object, label: str) -> None:
    if not isinstance(media, dict):
        raise SendError(f"{label} must be an object")
    reject_unknown_fields(media, {"url"}, label)
    if "url" not in media:
        raise SendError(f"{label}.url is required")
    url = require_string(media["url"], f"{label}.url", 2048)
    parsed = urlsplit(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise SendError(
            f"{label}.url must be an external HTTP(S) URL; component file "
            "uploads cannot be combined with incoming-webhook Components V2"
        )


class ComponentValidator:
    """Validate the non-interactive subset accepted by incoming webhooks."""

    def __init__(self) -> None:
        self.count = 0
        self.ids: set[int] = set()

    def register(self, component: object, label: str) -> tuple[dict, int]:
        if not isinstance(component, dict):
            raise SendError(f"{label} must be an object")
        component_type = component.get("type")
        if isinstance(component_type, bool) or not isinstance(component_type, int):
            raise SendError(f"{label}.type must be an integer")

        self.count += 1
        if self.count > MAX_COMPONENTS:
            raise SendError(
                f"components cannot contain more than {MAX_COMPONENTS} total objects"
            )

        if "id" in component:
            component_id = component["id"]
            if (
                isinstance(component_id, bool)
                or not isinstance(component_id, int)
                or not 0 <= component_id <= 0xFFFFFFFF
            ):
                raise SendError(f"{label}.id must be an unsigned 32-bit integer")
            if component_id and component_id in self.ids:
                raise SendError(f"duplicate component id: {component_id}")
            if component_id:
                self.ids.add(component_id)

        return component, component_type

    def validate_text_display(self, component: dict, label: str) -> None:
        reject_unknown_fields(component, {"type", "id", "content"}, label)
        if "content" not in component:
            raise SendError(f"{label}.content is required")
        content = component["content"]
        if not isinstance(content, str) or not content:
            raise SendError(f"{label}.content must be a non-empty string")

    def validate_media_content(self, value: dict, label: str, media_key: str) -> None:
        validate_external_media_item(value.get(media_key), f"{label}.{media_key}")
        if "description" in value:
            require_string(value["description"], f"{label}.description", 1024)
        if "spoiler" in value and not isinstance(value["spoiler"], bool):
            raise SendError(f"{label}.spoiler must be a boolean")

    def validate_thumbnail(self, component: dict, label: str) -> None:
        reject_unknown_fields(
            component,
            {"type", "id", "media", "description", "spoiler"},
            label,
        )
        self.validate_media_content(component, label, "media")

    def validate_media_gallery(self, component: dict, label: str) -> None:
        reject_unknown_fields(component, {"type", "id", "items"}, label)
        items = component.get("items")
        if not isinstance(items, list) or not 1 <= len(items) <= 10:
            raise SendError(f"{label}.items must contain between 1 and 10 objects")
        for index, item in enumerate(items):
            item_label = f"{label}.items[{index}]"
            if not isinstance(item, dict):
                raise SendError(f"{item_label} must be an object")
            reject_unknown_fields(
                item,
                {"media", "description", "spoiler"},
                item_label,
            )
            self.validate_media_content(item, item_label, "media")

    def validate_separator(self, component: dict, label: str) -> None:
        reject_unknown_fields(
            component,
            {"type", "id", "divider", "spacing"},
            label,
        )
        if "divider" in component and not isinstance(component["divider"], bool):
            raise SendError(f"{label}.divider must be a boolean")
        if "spacing" in component and component["spacing"] not in {1, 2}:
            raise SendError(f"{label}.spacing must be 1 or 2")

    def validate_section(self, component: dict, label: str) -> None:
        reject_unknown_fields(
            component,
            {"type", "id", "components", "accessory"},
            label,
        )
        children = component.get("components")
        if not isinstance(children, list) or not 1 <= len(children) <= 3:
            raise SendError(f"{label}.components must contain between 1 and 3 objects")
        for index, child in enumerate(children):
            child_label = f"{label}.components[{index}]"
            child, child_type = self.register(child, child_label)
            if child_type != 10:
                raise SendError(
                    f"{child_label} must be a non-interactive Text Display (type 10)"
                )
            self.validate_text_display(child, child_label)

        accessory_label = f"{label}.accessory"
        accessory, accessory_type = self.register(
            component.get("accessory"), accessory_label
        )
        if accessory_type != 11:
            raise SendError(
                f"{accessory_label} must be a non-interactive Thumbnail (type 11)"
            )
        self.validate_thumbnail(accessory, accessory_label)

    def validate_container(self, component: dict, label: str) -> None:
        reject_unknown_fields(
            component,
            {"type", "id", "components", "accent_color", "spoiler"},
            label,
        )
        color = component.get("accent_color")
        if color is not None and (
            isinstance(color, bool)
            or not isinstance(color, int)
            or not 0 <= color <= 0xFFFFFF
        ):
            raise SendError(f"{label}.accent_color must be a decimal RGB integer")
        if "spoiler" in component and not isinstance(component["spoiler"], bool):
            raise SendError(f"{label}.spoiler must be a boolean")

        children = component.get("components")
        if not isinstance(children, list) or not children:
            raise SendError(f"{label}.components must be a non-empty array")
        for index, child in enumerate(children):
            child_label = f"{label}.components[{index}]"
            self.validate_component(child, child_label, "container")

    def validate_component(self, component: object, label: str, placement: str) -> None:
        component, component_type = self.register(component, label)
        allowed_by_placement = {
            "top": {9, 10, 12, 14, 17},
            "container": {9, 10, 12, 14},
        }
        if component_type == 13:
            raise SendError(
                f"{label} uses File component type 13, but Discord's incoming-"
                "webhook endpoint does not allow files with Components V2"
            )
        if component_type not in allowed_by_placement[placement]:
            raise SendError(
                f"{label} uses interactive or unsupported component type "
                f"{component_type}"
            )

        validators = {
            9: self.validate_section,
            10: self.validate_text_display,
            12: self.validate_media_gallery,
            14: self.validate_separator,
            17: self.validate_container,
        }
        validators[component_type](component, label)


def validate_components(components: object) -> bool:
    if not isinstance(components, list):
        raise SendError("components must be an array")
    if not components:
        raise SendError("components must be a non-empty array")
    validator = ComponentValidator()
    for index, component in enumerate(components):
        validator.validate_component(component, f"components[{index}]", "top")
    return True


def load_and_normalize_payload(payload_path: Path, files: list[Path]) -> dict:
    try:
        payload = json.loads(payload_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SendError(f"payload file does not exist: {payload_path}") from exc
    except OSError as exc:
        raise SendError(f"could not read payload file: {payload_path}") from exc
    except json.JSONDecodeError as exc:
        raise SendError(
            f"payload is not valid JSON at line {exc.lineno}, column {exc.colno}"
        ) from exc

    if not isinstance(payload, dict):
        raise SendError("payload must be a JSON object")
    reject_unknown_fields(payload, TOP_LEVEL_FIELDS, "payload")

    content_present = False
    if "content" in payload:
        content = require_string(payload["content"], "content", 2000)
        content_present = bool(content)

    embeds_present = False
    if "embeds" in payload:
        embeds_present = validate_embeds(payload["embeds"])

    poll_present = False
    if "poll" in payload:
        poll_present = validate_poll(payload["poll"])

    components_present = False
    if "components" in payload:
        components_present = validate_components(payload["components"])

    if not (
        content_present or embeds_present or poll_present or components_present or files
    ):
        raise SendError(
            "payload requires non-empty content, embeds, poll, components, or a file"
        )

    if "allowed_mentions" not in payload:
        payload["allowed_mentions"] = {"parse": []}
    validate_allowed_mentions(payload["allowed_mentions"])

    flags = payload.get("flags", 0)
    if isinstance(flags, bool) or not isinstance(flags, int):
        raise SendError("flags must be an integer")
    if flags < 0 or flags & ~ALLOWED_FLAGS:
        raise SendError(
            "flags may contain only SUPPRESS_EMBEDS (4), "
            "SUPPRESS_NOTIFICATIONS (4096), and IS_COMPONENTS_V2 (32768)"
        )

    if components_present:
        incompatible_fields = [
            field
            for field in ("content", "embeds", "poll", "attachments")
            if field in payload
        ]
        if files:
            incompatible_fields.append("files")
        if incompatible_fields:
            names = ", ".join(incompatible_fields)
            raise SendError(
                "Components V2 cannot be combined with these incoming-webhook "
                f"fields: {names}"
            )
        payload["flags"] = flags | COMPONENTS_V2_FLAG
    elif flags & COMPONENTS_V2_FLAG:
        raise SendError("IS_COMPONENTS_V2 requires non-empty components")

    if "tts" in payload and not isinstance(payload["tts"], bool):
        raise SendError("tts must be a boolean")

    if "username" in payload:
        username = require_string(payload["username"], "username", 80)
        if not username:
            raise SendError("username cannot be empty")

    if "avatar_url" in payload:
        avatar_url = require_string(payload["avatar_url"], "avatar_url", 2048)
        parsed_avatar = urlsplit(avatar_url)
        if parsed_avatar.scheme not in {"http", "https"} or not parsed_avatar.netloc:
            raise SendError("avatar_url must be an HTTP(S) URL")

    if "thread_name" in payload:
        thread_name = require_string(payload["thread_name"], "thread_name", 100)
        if not thread_name:
            raise SendError("thread_name cannot be empty")

    if "applied_tags" in payload:
        applied_tags = payload["applied_tags"]
        if not isinstance(applied_tags, list) or not all(
            isinstance(tag, str) and tag.isdigit() for tag in applied_tags
        ):
            raise SendError("applied_tags must be an array of decimal string IDs")

    if "attachments" in payload:
        validate_attachments(payload["attachments"], len(files))

    return payload


def validate_files(files: list[Path]) -> list[Path]:
    resolved: list[Path] = []
    for file_path in files:
        expanded = file_path.expanduser().resolve()
        if not expanded.is_file():
            raise SendError(f"attachment is not a regular file: {file_path}")
        if not os.access(expanded, os.R_OK):
            raise SendError(f"attachment is not readable: {file_path}")
        resolved.append(expanded)
    return resolved


def quote_curl_form_path(path: Path) -> str:
    escaped = str(path).replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def sanitize(text: str, webhook_url: str) -> str:
    token = urlsplit(webhook_url).path.rstrip("/").rsplit("/", 1)[-1]
    redacted = text.replace(webhook_url, "[REDACTED_WEBHOOK_URL]")
    if token:
        redacted = redacted.replace(token, "[REDACTED_WEBHOOK_TOKEN]")
    return redacted


def redact_error(text: str, webhook_url: str) -> str:
    return sanitize(text, webhook_url)[:MAX_REDACTED_ERROR]


def parse_retry_after(headers: str, body: str) -> float | None:
    retry_after: float | None = None
    for line in headers.splitlines():
        if line.lower().startswith("retry-after:"):
            try:
                retry_after = float(line.split(":", 1)[1].strip())
            except ValueError:
                pass

    if retry_after is None:
        try:
            response = json.loads(body)
        except json.JSONDecodeError:
            response = None
        if isinstance(response, dict):
            value = response.get("retry_after")
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                retry_after = float(value)

    if retry_after is None or not math.isfinite(retry_after) or retry_after < 0:
        return None
    return retry_after


def build_endpoint(
    webhook_url: str, thread_id: str | None, with_components: bool
) -> str:
    parameters: list[tuple[str, str]] = [("wait", "true")]
    if thread_id is not None:
        if not thread_id.isdigit():
            raise SendError("thread_id must contain only decimal digits")
        parameters.append(("thread_id", thread_id))
    if with_components:
        parameters.append(("with_components", "true"))
    return f"{webhook_url}?{urlencode(parameters)}"


def write_private_text(path: Path, contents: str) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
        handle.write(contents)


def run_curl(
    webhook_url: str,
    payload: dict,
    files: list[Path],
    thread_id: str | None,
    rate_limit_retries: int,
    max_rate_limit_wait: float,
) -> str:
    endpoint = build_endpoint(webhook_url, thread_id, "components" in payload)

    with tempfile.TemporaryDirectory(prefix="discord-webhook-send.") as directory:
        temporary_dir = Path(directory)
        os.chmod(temporary_dir, 0o700)
        payload_path = temporary_dir / "payload.json"
        curl_config_path = temporary_dir / "curl.conf"
        headers_path = temporary_dir / "headers.txt"
        body_path = temporary_dir / "body.json"

        write_private_text(
            payload_path,
            json.dumps(payload, ensure_ascii=False, separators=(",", ":")),
        )
        write_private_text(curl_config_path, f'url = "{endpoint}"\n')
        write_private_text(headers_path, "")
        write_private_text(body_path, "")

        command = [
            "curl",
            "--disable",
            "--config",
            str(curl_config_path),
            "--proto",
            "=https",
            "--silent",
            "--show-error",
            "--connect-timeout",
            "10",
            "--max-time",
            "60" if files else "30",
            "--request",
            "POST",
            "--dump-header",
            str(headers_path),
            "--output",
            str(body_path),
            "--write-out",
            "%{http_code}",
        ]
        curl_environment = os.environ.copy()
        curl_environment.pop("DISCORD_WEBHOOK_URL", None)

        if files:
            payload_form_path = quote_curl_form_path(payload_path)
            command.extend(
                [
                    "--form",
                    f"payload_json=<{payload_form_path};type=application/json",
                ]
            )
            for index, file_path in enumerate(files):
                command.extend(
                    [
                        "--form",
                        f"files[{index}]=@{quote_curl_form_path(file_path)}",
                    ]
                )
        else:
            command.extend(
                [
                    "--header",
                    "Content-Type: application/json",
                    "--data-binary",
                    f"@{payload_path}",
                ]
            )

        for attempt in range(rate_limit_retries + 1):
            try:
                result = subprocess.run(
                    command,
                    check=False,
                    capture_output=True,
                    text=True,
                    env=curl_environment,
                )
            except FileNotFoundError as exc:
                raise SendError(
                    "curl is required but was not found on PATH", 127
                ) from exc

            body = body_path.read_text(encoding="utf-8", errors="replace")
            headers = headers_path.read_text(encoding="utf-8", errors="replace")

            if result.returncode != 0:
                details = redact_error(result.stderr.strip(), webhook_url)
                suffix = f": {details}" if details else ""
                raise SendError(
                    "curl transport failed; delivery is uncertain and was not retried"
                    f"{suffix}",
                    75,
                )

            status_text = result.stdout.strip()
            if not re.fullmatch(r"[0-9]{3}", status_text):
                raise SendError("curl did not return a valid HTTP status", 75)
            status = int(status_text)

            if 200 <= status < 300:
                sanitized_body = sanitize(body, webhook_url)
                if sanitized_body:
                    return sanitized_body
                return json.dumps({"ok": True, "http_status": status})

            if status == 429:
                retry_after = parse_retry_after(headers, body)
                if attempt >= rate_limit_retries:
                    raise SendError(
                        f"Discord rate limit persisted after {attempt + 1} attempts",
                        75,
                    )
                if retry_after is None:
                    raise SendError(
                        "Discord returned HTTP 429 without a valid retry interval", 75
                    )
                if retry_after > max_rate_limit_wait:
                    raise SendError(
                        "Discord requested a retry wait longer than "
                        f"{max_rate_limit_wait:g} seconds",
                        75,
                    )
                time.sleep(retry_after)
                continue

            safe_body = redact_error(body.strip(), webhook_url)
            suffix = f": {safe_body}" if safe_body else ""
            if 500 <= status < 600:
                raise SendError(
                    f"Discord returned HTTP {status}; delivery is uncertain and "
                    f"was not retried{suffix}",
                    75,
                )
            raise SendError(f"Discord returned HTTP {status}{suffix}", 22)

    raise SendError("unexpected delivery state", 75)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Send one Discord incoming-webhook message through curl."
    )
    parser.add_argument("--payload", required=True, type=Path)
    parser.add_argument("--alias")
    parser.add_argument(
        "--explicit-url-stdin",
        action="store_true",
        help="read an explicit fallback URL from the first line of stdin",
    )
    parser.add_argument("--file", action="append", type=Path, default=[])
    parser.add_argument("--thread-id")
    parser.add_argument(
        "--config",
        type=Path,
        default=webhook_config.DEFAULT_CONFIG,
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--rate-limit-retries",
        type=int,
        default=3,
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--max-rate-limit-wait",
        type=float,
        default=60,
        help=argparse.SUPPRESS,
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if not 0 <= args.rate_limit_retries <= 10:
            raise SendError("rate-limit retries must be between 0 and 10")
        if not math.isfinite(args.max_rate_limit_wait) or args.max_rate_limit_wait < 0:
            raise SendError(
                "maximum rate-limit wait must be a finite non-negative number"
            )

        webhook_url, _source = resolve_destination(
            args.config.expanduser(), args.alias, args.explicit_url_stdin
        )
        files = validate_files(args.file)
        payload = load_and_normalize_payload(args.payload.expanduser(), files)
        response = run_curl(
            webhook_url,
            payload,
            files,
            args.thread_id,
            args.rate_limit_retries,
            args.max_rate_limit_wait,
        )
        print(response)
        return 0
    except (SendError, webhook_config.ConfigError) as exc:
        exit_code = exc.exit_code if isinstance(exc, SendError) else 2
        print(f"error: {exc}", file=sys.stderr)
        return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
