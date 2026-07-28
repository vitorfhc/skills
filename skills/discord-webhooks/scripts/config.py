#!/usr/bin/env python3
"""Manage named Discord incoming-webhook URLs in a restricted flat YAML file."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlsplit


DEFAULT_CONFIG = Path.home() / ".discord-webhooks" / "config.yaml"
HEADER = "# Discord webhook aliases. Treat this file as secret.\n"
ALIAS_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
ENTRY_PATTERN = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._-]{0,63}):\s*(.+?)\s*$")
WEBHOOK_PATH_PATTERN = re.compile(
    r"^/api(?:/v[0-9]+)?/webhooks/[0-9]+/[A-Za-z0-9._-]+/?$"
)


class ConfigError(Exception):
    """A safe, user-facing config error that never contains a webhook URL."""


def validate_alias(alias: str) -> None:
    if not ALIAS_PATTERN.fullmatch(alias):
        raise ConfigError(
            "alias must be 1-64 characters using letters, digits, dots, underscores, or hyphens"
        )


def validate_url(url: str) -> None:
    try:
        parsed = urlsplit(url)
        port = parsed.port
    except ValueError as exc:
        raise ConfigError("invalid Discord webhook URL") from exc

    hostname = (parsed.hostname or "").lower()
    official_host = (
        hostname == "discord.com"
        or hostname.endswith(".discord.com")
        or hostname == "discordapp.com"
        or hostname.endswith(".discordapp.com")
    )

    if parsed.scheme != "https" or not official_host:
        raise ConfigError("webhook URL must use HTTPS on an official Discord hostname")
    if parsed.username or parsed.password or port not in (None, 443):
        raise ConfigError(
            "webhook URL must not contain credentials or a non-HTTPS port"
        )
    if parsed.query or parsed.fragment:
        raise ConfigError(
            "store the base webhook URL without query parameters or fragments"
        )
    if not WEBHOOK_PATH_PATTERN.fullmatch(parsed.path):
        raise ConfigError("URL is not a standard Discord incoming-webhook URL")


def ensure_config(path: Path) -> None:
    parent_existed = path.parent.exists()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        if not parent_existed or path == DEFAULT_CONFIG:
            os.chmod(path.parent, 0o700)

        if not path.exists():
            try:
                descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            except FileExistsError:
                pass
            else:
                with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
                    handle.write(HEADER)

        if not path.is_file():
            raise ConfigError("config path exists but is not a regular file")
        os.chmod(path, 0o600)
    except OSError as exc:
        raise ConfigError("could not create or secure config file") from exc


def parse_quoted_value(raw_value: str, line_number: int) -> str:
    if not raw_value.startswith('"'):
        raise ConfigError(
            f"line {line_number}: URL must be a double-quoted YAML string"
        )
    try:
        value = json.loads(raw_value)
    except json.JSONDecodeError as exc:
        raise ConfigError(f"line {line_number}: invalid quoted URL") from exc
    if not isinstance(value, str):
        raise ConfigError(f"line {line_number}: URL must be a string")
    return value


def load_config(path: Path) -> dict[str, str]:
    ensure_config(path)
    aliases: dict[str, str] = {}

    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise ConfigError("could not read config file") from exc

    for line_number, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        match = ENTRY_PATTERN.fullmatch(stripped)
        if not match:
            raise ConfigError(
                f'line {line_number}: expected alias: "https://discord.com/api/webhooks/..."'
            )

        alias, raw_value = match.groups()
        if alias in aliases:
            raise ConfigError(f"line {line_number}: duplicate alias {alias!r}")

        value = parse_quoted_value(raw_value, line_number)
        validate_url(value)
        aliases[alias] = value

    return aliases


def write_config(path: Path, aliases: dict[str, str]) -> None:
    ensure_config(path)
    lines = [HEADER.rstrip("\n")]
    for alias in sorted(aliases, key=str.casefold):
        validate_alias(alias)
        validate_url(aliases[alias])
        lines.append(f"{alias}: {json.dumps(aliases[alias], ensure_ascii=False)}")
    contents = "\n".join(lines) + "\n"

    temporary_name: str | None = None
    try:
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=".config.yaml.", dir=path.parent
        )
        os.fchmod(descriptor, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(contents)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_name, path)
        temporary_name = None
        os.chmod(path, 0o600)
    except OSError as exc:
        raise ConfigError("could not update config file") from exc
    finally:
        if temporary_name is not None:
            try:
                os.unlink(temporary_name)
            except FileNotFoundError:
                pass


def read_url_argument(url: str | None, read_stdin: bool) -> str:
    if read_stdin and url is not None:
        raise ConfigError(
            "provide the URL either as an argument or through --stdin, not both"
        )
    if read_stdin:
        value = sys.stdin.readline().rstrip("\r\n")
    elif url is not None:
        value = url
    else:
        raise ConfigError("provide a webhook URL or use --stdin")
    if not value:
        raise ConfigError("webhook URL cannot be empty")
    return value


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Manage ~/.discord-webhooks/config.yaml without exposing saved URLs."
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG,
        help=argparse.SUPPRESS,
    )
    commands = parser.add_subparsers(dest="command", required=True)

    commands.add_parser("init", help="create and secure the config if needed")

    set_parser = commands.add_parser("set", help="save or replace an alias")
    set_parser.add_argument("alias")
    set_parser.add_argument("url", nargs="?")
    set_parser.add_argument(
        "--stdin", action="store_true", help="read the URL from stdin"
    )

    resolve_parser = commands.add_parser("resolve", help="resolve one alias")
    resolve_parser.add_argument("alias")

    commands.add_parser("list", help="list alias names without URLs")

    remove_parser = commands.add_parser("remove", help="remove one alias")
    remove_parser.add_argument("alias")

    validate_parser = commands.add_parser("validate", help="validate without saving")
    validate_parser.add_argument("url", nargs="?")
    validate_parser.add_argument(
        "--stdin", action="store_true", help="read the URL from stdin"
    )

    return parser


def run(args: argparse.Namespace) -> int:
    path: Path = args.config.expanduser()

    if args.command == "init":
        load_config(path)
        print(f"Config ready: {path}")
        return 0

    if args.command == "set":
        validate_alias(args.alias)
        url = read_url_argument(args.url, args.stdin)
        validate_url(url)
        aliases = load_config(path)
        aliases[args.alias] = url
        write_config(path, aliases)
        print(f"Saved webhook alias: {args.alias}")
        return 0

    if args.command == "resolve":
        validate_alias(args.alias)
        aliases = load_config(path)
        if args.alias not in aliases:
            raise ConfigError(f"unknown webhook alias: {args.alias}")
        print(aliases[args.alias])
        return 0

    if args.command == "list":
        aliases = load_config(path)
        for alias in sorted(aliases, key=str.casefold):
            print(alias)
        return 0

    if args.command == "remove":
        validate_alias(args.alias)
        aliases = load_config(path)
        if args.alias not in aliases:
            raise ConfigError(f"unknown webhook alias: {args.alias}")
        del aliases[args.alias]
        write_config(path, aliases)
        print(f"Removed webhook alias: {args.alias}")
        return 0

    if args.command == "validate":
        url = read_url_argument(args.url, args.stdin)
        validate_url(url)
        print("Valid Discord webhook URL")
        return 0

    raise ConfigError("unsupported command")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return run(args)
    except ConfigError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
