#!/usr/bin/env python3
"""A deterministic curl stand-in used by the Discord webhook sender tests."""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path


def option_value(arguments: list[str], option: str) -> str:
    try:
        return arguments[arguments.index(option) + 1]
    except (ValueError, IndexError) as exc:
        raise SystemExit(f"missing fake-curl option: {option}") from exc


def read_attempt() -> int:
    state_path = Path(os.environ["FAKE_CURL_STATE"])
    try:
        attempt = int(state_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        attempt = 0
    state_path.write_text(str(attempt + 1), encoding="utf-8")
    return attempt


def read_url(config_path: Path) -> str:
    contents = config_path.read_text(encoding="utf-8")
    match = re.search(r'^url = "([^"]+)"$', contents, flags=re.MULTILINE)
    if match is None:
        raise SystemExit("fake curl could not find URL in config")
    return match.group(1)


def unquote_form_path(value: str) -> Path | None:
    match = re.search(r'[<@]"((?:[^"\\]|\\.)*)"', value)
    if match is None:
        return None
    path = match.group(1).replace('\\"', '"').replace("\\\\", "\\")
    return Path(path)


def read_payload(arguments: list[str]) -> object | None:
    if "--data-binary" in arguments:
        value = option_value(arguments, "--data-binary")
        if value.startswith("@"):
            return json.loads(Path(value[1:]).read_text(encoding="utf-8"))

    forms = [
        arguments[index + 1]
        for index, argument in enumerate(arguments[:-1])
        if argument == "--form"
    ]
    for form in forms:
        if form.startswith("payload_json=<"):
            path = unquote_form_path(form)
            if path is not None:
                return json.loads(path.read_text(encoding="utf-8"))
    return None


def main() -> int:
    arguments = sys.argv[1:]
    attempt = read_attempt()
    responses = json.loads(os.environ["FAKE_CURL_RESPONSES"])
    response = responses[min(attempt, len(responses) - 1)]

    config_path = Path(option_value(arguments, "--config"))
    output_path = Path(option_value(arguments, "--output"))
    headers_path = Path(option_value(arguments, "--dump-header"))
    url = read_url(config_path)
    payload = read_payload(arguments)
    forms = [
        arguments[index + 1]
        for index, argument in enumerate(arguments[:-1])
        if argument == "--form"
    ]

    record = {
        "attempt": attempt,
        "argv": arguments,
        "discord_webhook_url_in_environment": "DISCORD_WEBHOOK_URL" in os.environ,
        "forms": forms,
        "payload": payload,
        "url": url,
    }
    record_path = Path(os.environ["FAKE_CURL_RECORD"])
    with record_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    status = int(response.get("status", 200))
    headers = response.get("headers", {})
    header_lines = [f"HTTP/1.1 {status} Mock"]
    header_lines.extend(f"{name}: {value}" for name, value in headers.items())
    headers_path.write_text("\r\n".join(header_lines) + "\r\n\r\n", encoding="utf-8")

    body = response.get("body", "")
    if not isinstance(body, str):
        body = json.dumps(body)
    output_path.write_text(body, encoding="utf-8")

    stderr = response.get("stderr", "")
    if stderr:
        print(stderr, file=sys.stderr)
    print(f"{status:03d}", end="")
    return int(response.get("curl_exit", 0))


if __name__ == "__main__":
    raise SystemExit(main())
