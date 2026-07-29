from __future__ import annotations

import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_SCRIPT = REPO_ROOT / "skills" / "discord-webhooks" / "scripts" / "config.py"
URL_ONE = "https://discord.com/api/webhooks/111111111111111111/first_token"
URL_TWO = "https://canary.discord.com/api/v10/webhooks/222222222222222222/second_token"


class ConfigScriptTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.config_path = self.root / "private" / "config.yaml"

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def run_config(
        self, *arguments: str, input_text: str | None = None
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(CONFIG_SCRIPT),
                "--config",
                str(self.config_path),
                *arguments,
            ],
            input=input_text,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_full_alias_lifecycle_and_permissions(self) -> None:
        initialized = self.run_config("init")
        self.assertEqual(initialized.returncode, 0, initialized.stderr)
        self.assertEqual(stat.S_IMODE(self.config_path.parent.stat().st_mode), 0o700)
        self.assertEqual(stat.S_IMODE(self.config_path.stat().st_mode), 0o600)

        saved_two = self.run_config("set", "xablau", "--stdin", input_text=URL_TWO)
        saved_one = self.run_config("set", "alerts", "--stdin", input_text=URL_ONE)
        self.assertEqual(saved_two.returncode, 0, saved_two.stderr)
        self.assertEqual(saved_one.returncode, 0, saved_one.stderr)
        self.assertNotIn("second_token", saved_two.stdout)
        self.assertNotIn("first_token", saved_one.stdout)

        listed = self.run_config("list")
        self.assertEqual(listed.stdout, "alerts\nxablau\n")
        self.assertNotIn("token", listed.stdout)

        resolved = self.run_config("resolve", "xablau")
        self.assertEqual(resolved.stdout.strip(), URL_TWO)

        removed = self.run_config("remove", "xablau")
        self.assertEqual(removed.returncode, 0, removed.stderr)
        missing = self.run_config("resolve", "xablau")
        self.assertEqual(missing.returncode, 2)
        self.assertNotIn("second_token", missing.stderr)

    def test_writer_produces_flat_sorted_yaml(self) -> None:
        self.run_config("set", "zeta", "--stdin", input_text=URL_TWO)
        self.run_config("set", "alpha", "--stdin", input_text=URL_ONE)
        self.assertEqual(
            self.config_path.read_text(encoding="utf-8"),
            "# Discord webhook aliases. Treat this file as secret.\n"
            f'alpha: "{URL_ONE}"\n'
            f'zeta: "{URL_TWO}"\n',
        )

    def test_rejects_non_discord_query_and_invalid_port_without_leaking(self) -> None:
        invalid_urls = [
            "https://example.com/api/webhooks/123/token",
            f"{URL_ONE}?wait=true",
            "https://discord.com:bad/api/webhooks/123/token",
        ]
        for invalid_url in invalid_urls:
            with self.subTest(invalid_url=invalid_url):
                result = self.run_config("validate", "--stdin", input_text=invalid_url)
                self.assertEqual(result.returncode, 2)
                self.assertNotIn(invalid_url, result.stderr)
                self.assertNotIn("token", result.stderr)

    def test_rejects_webhook_urls_in_process_arguments(self) -> None:
        for command in ("set", "validate"):
            with self.subTest(command=command):
                arguments = (
                    (command, "alerts", URL_ONE)
                    if command == "set"
                    else (command, URL_ONE)
                )
                result = self.run_config(*arguments)
                self.assertEqual(result.returncode, 2)
                self.assertIn("use --stdin", result.stderr)
                self.assertNotIn(URL_ONE, result.stderr)
                self.assertNotIn("first_token", result.stderr)

    def test_rejects_malformed_and_duplicate_entries(self) -> None:
        self.config_path.parent.mkdir(mode=0o700)
        self.config_path.write_text(
            f'alerts: "{URL_ONE}"\nalerts: "{URL_TWO}"\n',
            encoding="utf-8",
        )
        os.chmod(self.config_path, 0o600)
        duplicate = self.run_config("list")
        self.assertEqual(duplicate.returncode, 2)
        self.assertIn("duplicate alias", duplicate.stderr)
        self.assertNotIn("token", duplicate.stderr)

        self.config_path.write_text("alerts: not-quoted\n", encoding="utf-8")
        malformed = self.run_config("list")
        self.assertEqual(malformed.returncode, 2)
        self.assertIn("double-quoted YAML string", malformed.stderr)


if __name__ == "__main__":
    unittest.main()
