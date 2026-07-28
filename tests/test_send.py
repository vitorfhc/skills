from __future__ import annotations

import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlsplit


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = REPO_ROOT / "skills" / "discord-webhooks" / "scripts"
CONFIG_SCRIPT = SCRIPT_DIR / "config.py"
SEND_SCRIPT = SCRIPT_DIR / "send.py"
FAKE_CURL = REPO_ROOT / "tests" / "fake_curl.py"
ALIAS_URL = "https://discord.com/api/webhooks/111111111111111111/alias_token"
EXPLICIT_URL = (
    "https://canary.discord.com/api/v10/webhooks/222222222222222222/explicit_token"
)
ENVIRONMENT_URL = (
    "https://discordapp.com/api/webhooks/333333333333333333/environment_token"
)


class SendScriptTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.bin_dir = self.root / "bin"
        self.bin_dir.mkdir()
        self.fake_curl = self.bin_dir / "curl"
        shutil.copy2(FAKE_CURL, self.fake_curl)
        os.chmod(self.fake_curl, 0o755)

        self.config_path = self.root / "home" / ".discord-webhooks" / "config.yaml"
        self.payload_path = self.root / "payload.json"
        self.record_path = self.root / "curl-record.jsonl"
        self.state_path = self.root / "curl-state.txt"
        self.environment = os.environ.copy()
        self.environment.update(
            {
                "PATH": f"{self.bin_dir}{os.pathsep}{self.environment['PATH']}",
                "FAKE_CURL_RECORD": str(self.record_path),
                "FAKE_CURL_STATE": str(self.state_path),
                "FAKE_CURL_RESPONSES": json.dumps(
                    [{"status": 200, "body": {"id": "999", "content": "ok"}}]
                ),
            }
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def write_payload(self, payload: object) -> None:
        self.payload_path.write_text(json.dumps(payload), encoding="utf-8")
        os.chmod(self.payload_path, 0o600)

    def save_alias(self, alias: str = "xablau", url: str = ALIAS_URL) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(CONFIG_SCRIPT),
                "--config",
                str(self.config_path),
                "set",
                alias,
                "--stdin",
            ],
            input=url,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def run_sender(
        self,
        *arguments: str,
        input_text: str | None = None,
        environment: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        selected_environment = self.environment.copy()
        if environment:
            selected_environment.update(environment)
        return subprocess.run(
            [
                sys.executable,
                str(SEND_SCRIPT),
                "--config",
                str(self.config_path),
                "--payload",
                str(self.payload_path),
                *arguments,
            ],
            input=input_text,
            text=True,
            capture_output=True,
            env=selected_environment,
            check=False,
        )

    def records(self) -> list[dict]:
        if not self.record_path.exists():
            return []
        return [
            json.loads(line)
            for line in self.record_path.read_text(encoding="utf-8").splitlines()
        ]

    def test_alias_precedence_safe_mentions_and_secret_not_in_argv(self) -> None:
        self.save_alias()
        self.write_payload({"content": "hello"})
        result = self.run_sender(
            "--alias",
            "xablau",
            "--explicit-url-stdin",
            input_text=EXPLICIT_URL,
            environment={"DISCORD_WEBHOOK_URL": ENVIRONMENT_URL},
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["id"], "999")

        record = self.records()[0]
        parsed_url = urlsplit(record["url"])
        self.assertIn("/111111111111111111/alias_token", parsed_url.path)
        self.assertEqual(parse_qs(parsed_url.query), {"wait": ["true"]})
        self.assertEqual(record["payload"]["allowed_mentions"], {"parse": []})
        self.assertEqual(record["argv"][0], "--disable")
        self.assertNotIn("alias_token", " ".join(record["argv"]))
        self.assertFalse(record["discord_webhook_url_in_environment"])

    def test_explicit_then_environment_fallback(self) -> None:
        self.write_payload({"content": "explicit"})
        explicit = self.run_sender(
            "--alias",
            "missing",
            "--explicit-url-stdin",
            input_text=EXPLICIT_URL,
            environment={"DISCORD_WEBHOOK_URL": ENVIRONMENT_URL},
        )
        self.assertEqual(explicit.returncode, 0, explicit.stderr)
        self.assertIn("explicit_token", self.records()[0]["url"])

        self.record_path.unlink()
        self.state_path.unlink()
        environment = self.run_sender(
            "--alias",
            "missing",
            environment={"DISCORD_WEBHOOK_URL": ENVIRONMENT_URL},
        )
        self.assertEqual(environment.returncode, 0, environment.stderr)
        self.assertIn("environment_token", self.records()[0]["url"])

    def test_config_is_created_when_no_alias_exists(self) -> None:
        self.write_payload({"content": "environment"})
        result = self.run_sender(environment={"DISCORD_WEBHOOK_URL": ENVIRONMENT_URL})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(self.config_path.is_file())
        self.assertEqual(stat.S_IMODE(self.config_path.parent.stat().st_mode), 0o700)
        self.assertEqual(stat.S_IMODE(self.config_path.stat().st_mode), 0o600)

    def test_multipart_attachment_and_thread_query(self) -> None:
        self.save_alias()
        attachment = self.root / "report;final.txt"
        attachment.write_text("report", encoding="utf-8")
        self.write_payload(
            {
                "content": "report",
                "attachments": [
                    {
                        "id": 0,
                        "filename": "report;final.txt",
                        "description": "deployment report",
                    }
                ],
            }
        )
        result = self.run_sender(
            "--alias",
            "xablau",
            "--thread-id",
            "444444444444444444",
            "--file",
            str(attachment),
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        record = self.records()[0]
        self.assertEqual(
            parse_qs(urlsplit(record["url"]).query),
            {
                "wait": ["true"],
                "thread_id": ["444444444444444444"],
            },
        )
        self.assertEqual(record["payload"]["content"], "report")
        self.assertTrue(
            any(form.startswith("payload_json=<") for form in record["forms"])
        )
        self.assertTrue(any(form.startswith("files[0]=@") for form in record["forms"]))

    def test_rich_embed_and_poll_payload(self) -> None:
        self.save_alias()
        self.write_payload(
            {
                "embeds": [
                    {
                        "author": {
                            "name": "CI",
                            "url": "https://example.com/builds/42",
                            "icon_url": "https://example.com/ci.png",
                        },
                        "title": "Build passed",
                        "url": "https://example.com/builds/42",
                        "description": "Production is ready",
                        "color": 5793266,
                        "fields": [
                            {"name": "Commit", "value": "abc123", "inline": True}
                        ],
                        "thumbnail": {"url": "https://example.com/thumb.png"},
                        "image": {"url": "https://example.com/chart.png"},
                        "footer": {
                            "text": "Deployment pipeline",
                            "icon_url": "https://example.com/footer.png",
                        },
                        "timestamp": "2026-07-28T19:00:00Z",
                    }
                ],
                "poll": {
                    "question": {"text": "Deploy now?"},
                    "answers": [
                        {
                            "poll_media": {
                                "text": "Yes",
                                "emoji": {"name": "🚀"},
                            }
                        },
                        {
                            "poll_media": {
                                "text": "No",
                                "emoji": {"id": "123456789012345678"},
                            }
                        },
                    ],
                    "duration": 24,
                    "allow_multiselect": False,
                    "layout_type": 1,
                },
                "tts": False,
                "flags": 4100,
            }
        )
        result = self.run_sender("--alias", "xablau")
        self.assertEqual(result.returncode, 0, result.stderr)
        record_payload = self.records()[0]["payload"]
        self.assertEqual(record_payload["poll"]["question"]["text"], "Deploy now?")
        self.assertEqual(record_payload["embeds"][0]["color"], 5793266)
        self.assertEqual(record_payload["flags"], 4100)
        self.assertEqual(record_payload["allowed_mentions"], {"parse": []})

    def test_forum_thread_overrides_tts_and_targeted_mentions(self) -> None:
        self.save_alias()
        self.write_payload(
            {
                "content": "Hello <@123456789012345678>",
                "username": "Release Bot",
                "avatar_url": "https://example.com/release-bot.png",
                "tts": True,
                "thread_name": "Deployment 42",
                "applied_tags": ["987654321098765432"],
                "allowed_mentions": {
                    "parse": [],
                    "users": ["123456789012345678"],
                },
            }
        )
        result = self.run_sender("--alias", "xablau")
        self.assertEqual(result.returncode, 0, result.stderr)
        record = self.records()[0]
        self.assertEqual(parse_qs(urlsplit(record["url"]).query), {"wait": ["true"]})
        self.assertEqual(record["payload"]["username"], "Release Bot")
        self.assertTrue(record["payload"]["tts"])
        self.assertEqual(record["payload"]["thread_name"], "Deployment 42")
        self.assertEqual(
            record["payload"]["allowed_mentions"]["users"],
            ["123456789012345678"],
        )

    def test_non_interactive_components_v2_payload(self) -> None:
        self.save_alias()
        self.write_payload(
            {
                "username": "Release Bot",
                "flags": 4096,
                "components": [
                    {"type": 10, "id": 1, "content": "# Build passed"},
                    {
                        "type": 9,
                        "id": 2,
                        "components": [
                            {"type": 10, "id": 3, "content": "Production is ready"}
                        ],
                        "accessory": {
                            "type": 11,
                            "id": 4,
                            "media": {"url": "https://example.com/status.png"},
                            "description": "Green build status",
                        },
                    },
                    {
                        "type": 12,
                        "id": 5,
                        "items": [
                            {
                                "media": {"url": "https://example.com/deployment.png"},
                                "description": "Deployment chart",
                                "spoiler": False,
                            }
                        ],
                    },
                    {"type": 14, "id": 6, "divider": True, "spacing": 2},
                    {
                        "type": 17,
                        "id": 7,
                        "accent_color": 5793266,
                        "components": [
                            {"type": 10, "id": 8, "content": "Commit `abc123`"}
                        ],
                    },
                ],
            }
        )
        result = self.run_sender("--alias", "xablau")
        self.assertEqual(result.returncode, 0, result.stderr)

        record = self.records()[0]
        self.assertEqual(
            parse_qs(urlsplit(record["url"]).query),
            {"wait": ["true"], "with_components": ["true"]},
        )
        self.assertEqual(record["payload"]["flags"], 4096 | 32768)
        self.assertEqual(record["payload"]["allowed_mentions"], {"parse": []})
        self.assertEqual(record["payload"]["components"][1]["accessory"]["type"], 11)

    def test_http_429_retries_only_for_rate_limit(self) -> None:
        self.save_alias()
        self.write_payload({"content": "retry"})
        responses = [
            {
                "status": 429,
                "headers": {"Retry-After": "0"},
                "body": {"retry_after": 0},
            },
            {"status": 200, "body": {"id": "after-retry"}},
        ]
        result = self.run_sender(
            "--alias",
            "xablau",
            environment={"FAKE_CURL_RESPONSES": json.dumps(responses)},
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["id"], "after-retry")
        self.assertEqual(len(self.records()), 2)

    def test_non_finite_rate_limit_interval_is_rejected_without_retry(self) -> None:
        self.save_alias()
        self.write_payload({"content": "do not retry"})
        result = self.run_sender(
            "--alias",
            "xablau",
            environment={
                "FAKE_CURL_RESPONSES": json.dumps(
                    [
                        {
                            "status": 429,
                            "headers": {"Retry-After": "NaN"},
                            "body": {"retry_after": "NaN"},
                        }
                    ]
                )
            },
        )
        self.assertEqual(result.returncode, 75)
        self.assertIn("without a valid retry interval", result.stderr)
        self.assertEqual(len(self.records()), 1)

    def test_large_success_response_is_not_truncated(self) -> None:
        self.save_alias()
        self.write_payload({"content": "large response"})
        large_content = "x" * 5000
        result = self.run_sender(
            "--alias",
            "xablau",
            environment={
                "FAKE_CURL_RESPONSES": json.dumps(
                    [{"status": 200, "body": {"id": "large", "content": large_content}}]
                )
            },
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["content"], large_content)

    def test_http_5xx_is_not_retried_and_does_not_leak_token(self) -> None:
        self.save_alias()
        self.write_payload({"content": "uncertain"})
        result = self.run_sender(
            "--alias",
            "xablau",
            environment={
                "FAKE_CURL_RESPONSES": json.dumps(
                    [{"status": 503, "body": {"message": "unavailable"}}]
                )
            },
        )
        self.assertEqual(result.returncode, 75)
        self.assertIn("delivery is uncertain", result.stderr)
        self.assertNotIn("alias_token", result.stderr)
        self.assertEqual(len(self.records()), 1)

    def test_transport_failure_is_not_retried_and_redacts_token(self) -> None:
        self.save_alias()
        self.write_payload({"content": "uncertain"})
        result = self.run_sender(
            "--alias",
            "xablau",
            environment={
                "FAKE_CURL_RESPONSES": json.dumps(
                    [
                        {
                            "status": 0,
                            "curl_exit": 28,
                            "stderr": f"timeout at {ALIAS_URL}",
                        }
                    ]
                )
            },
        )
        self.assertEqual(result.returncode, 75)
        self.assertIn("delivery is uncertain", result.stderr)
        self.assertIn("[REDACTED_WEBHOOK_URL]", result.stderr)
        self.assertNotIn("alias_token", result.stderr)
        self.assertEqual(len(self.records()), 1)

    def test_interactive_components_and_invalid_poll_fail_before_curl(self) -> None:
        self.save_alias()
        invalid_payloads = [
            {
                "components": [
                    {
                        "type": 1,
                        "components": [
                            {
                                "type": 2,
                                "style": 1,
                                "label": "No",
                                "custom_id": "not-supported",
                            }
                        ],
                    }
                ]
            },
            {
                "poll": {
                    "question": {"text": "Only one?"},
                    "answers": [{"poll_media": {"text": "Yes"}}],
                }
            },
        ]
        for payload in invalid_payloads:
            with self.subTest(payload=payload):
                self.write_payload(payload)
                result = self.run_sender("--alias", "xablau")
                self.assertEqual(result.returncode, 2)
                self.assertEqual(self.records(), [])

    def test_invalid_components_v2_fail_before_curl(self) -> None:
        self.save_alias()
        invalid_payloads = [
            {"content": "cannot mix", "components": [{"type": 10, "content": "x"}]},
            {
                "components": [
                    {
                        "type": 9,
                        "components": [{"type": 10, "content": "x"}],
                        "accessory": {
                            "type": 2,
                            "style": 5,
                            "label": "Open",
                            "url": "https://example.com",
                        },
                    }
                ]
            },
            {"components": [{"type": 13, "file": {"url": "attachment://report.txt"}}]},
            {
                "components": [
                    {"type": 10, "id": 1, "content": "first"},
                    {"type": 10, "id": 1, "content": "duplicate"},
                ]
            },
            {
                "components": [
                    {"type": 10, "content": f"item {index}"} for index in range(41)
                ]
            },
        ]
        for payload in invalid_payloads:
            with self.subTest(payload=payload):
                self.write_payload(payload)
                result = self.run_sender("--alias", "xablau")
                self.assertEqual(result.returncode, 2)
                self.assertEqual(self.records(), [])

    def test_invalid_mentions_and_embed_fields_fail_before_curl(self) -> None:
        self.save_alias()
        invalid_payloads = [
            {
                "content": "ping <@123>",
                "allowed_mentions": {"parse": ["users"], "users": ["123"]},
            },
            {"embeds": [{"title": "bad color", "color": 0x1000000}]},
            {
                "embeds": [
                    {
                        "title": "read only",
                        "image": {
                            "url": "https://example.com/image.png",
                            "proxy_url": "https://proxy.example/image.png",
                        },
                    }
                ]
            },
        ]
        for payload in invalid_payloads:
            with self.subTest(payload=payload):
                self.write_payload(payload)
                result = self.run_sender("--alias", "xablau")
                self.assertEqual(result.returncode, 2)
                self.assertEqual(self.records(), [])

    def test_missing_destination_and_attachment_mismatch_fail_before_curl(self) -> None:
        self.write_payload({"content": "no destination"})
        missing = self.run_sender()
        self.assertEqual(missing.returncode, 2)
        self.assertIn("no webhook destination", missing.stderr)
        self.assertEqual(self.records(), [])

        attachment = self.root / "report.txt"
        attachment.write_text("report", encoding="utf-8")
        self.write_payload(
            {
                "content": "bad attachment",
                "attachments": [{"id": 1, "filename": "report.txt"}],
            }
        )
        mismatch = self.run_sender(
            "--file",
            str(attachment),
            environment={"DISCORD_WEBHOOK_URL": ENVIRONMENT_URL},
        )
        self.assertEqual(mismatch.returncode, 2)
        self.assertIn("does not match an uploaded file", mismatch.stderr)
        self.assertEqual(self.records(), [])


if __name__ == "__main__":
    unittest.main()
