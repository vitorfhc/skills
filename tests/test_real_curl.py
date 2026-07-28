from __future__ import annotations

import json
import os
import queue
import shutil
import ssl
import subprocess
import sys
import tempfile
import threading
import unittest
from email import policy
from email.parser import BytesParser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = REPO_ROOT / "skills" / "discord-webhooks" / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))
import send as webhook_send  # noqa: E402


class CaptureHandler(BaseHTTPRequestHandler):
    captures: queue.Queue[dict] = queue.Queue()

    def do_POST(self) -> None:
        length = int(self.headers["Content-Length"])
        body = self.rfile.read(length)
        self.captures.put(
            {
                "body": body,
                "content_type": self.headers["Content-Type"],
                "path": self.path,
            }
        )
        response = json.dumps({"id": "local-real-curl"}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def log_message(self, _format: str, *_arguments: object) -> None:
        return


@unittest.skipUnless(shutil.which("curl"), "curl is required")
@unittest.skipUnless(shutil.which("openssl"), "openssl is required")
class RealCurlMultipartTests(unittest.TestCase):
    def test_private_config_and_multipart_form_reach_local_https_server(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            certificate = root / "certificate.pem"
            private_key = root / "private-key.pem"
            generated = subprocess.run(
                [
                    "openssl",
                    "req",
                    "-x509",
                    "-newkey",
                    "rsa:2048",
                    "-nodes",
                    "-keyout",
                    str(private_key),
                    "-out",
                    str(certificate),
                    "-days",
                    "1",
                    "-subj",
                    "/CN=localhost",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(generated.returncode, 0, generated.stderr)

            server = HTTPServer(("127.0.0.1", 0), CaptureHandler)
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(certificate, private_key)
            server.socket = context.wrap_socket(server.socket, server_side=True)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()

            try:
                payload_path = root / "payload.json"
                attachment_path = root / 'report;"final".txt'
                curl_config = root / "curl.conf"
                response_path = root / "response.json"
                headers_path = root / "headers.txt"
                payload = {
                    "content": "real curl multipart",
                    "allowed_mentions": {"parse": []},
                    "attachments": [
                        {
                            "id": 0,
                            "filename": attachment_path.name,
                            "description": "local integration fixture",
                        }
                    ],
                }
                payload_path.write_text(json.dumps(payload), encoding="utf-8")
                attachment_path.write_text("fixture-body", encoding="utf-8")
                endpoint = (
                    f"https://localhost:{server.server_port}/api/webhooks/"
                    "123/test?wait=true&thread_id=456"
                )
                curl_config.write_text(f'url = "{endpoint}"\n', encoding="utf-8")
                os.chmod(curl_config, 0o600)

                command = [
                    "curl",
                    "--disable",
                    "--config",
                    str(curl_config),
                    "--insecure",
                    "--proto",
                    "=https",
                    "--silent",
                    "--show-error",
                    "--request",
                    "POST",
                    "--dump-header",
                    str(headers_path),
                    "--output",
                    str(response_path),
                    "--write-out",
                    "%{http_code}",
                    "--form",
                    "payload_json=<"
                    f"{webhook_send.quote_curl_form_path(payload_path)}"
                    ";type=application/json",
                    "--form",
                    f"files[0]=@{webhook_send.quote_curl_form_path(attachment_path)}",
                ]
                sent = subprocess.run(
                    command,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(sent.returncode, 0, sent.stderr)
                self.assertEqual(sent.stdout, "200")
                self.assertEqual(
                    json.loads(response_path.read_text(encoding="utf-8"))["id"],
                    "local-real-curl",
                )

                captured = CaptureHandler.captures.get(timeout=2)
                self.assertEqual(
                    captured["path"],
                    "/api/webhooks/123/test?wait=true&thread_id=456",
                )
                pseudo_message = (
                    f"Content-Type: {captured['content_type']}\r\n"
                    "MIME-Version: 1.0\r\n\r\n"
                ).encode() + captured["body"]
                message = BytesParser(policy=policy.default).parsebytes(pseudo_message)
                parts = {
                    part.get_param("name", header="content-disposition"): part
                    for part in message.iter_parts()
                }
                self.assertEqual(
                    json.loads(parts["payload_json"].get_payload(decode=True)),
                    payload,
                )
                self.assertEqual(
                    parts["files[0]"].get_payload(decode=True), b"fixture-body"
                )
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=2)


if __name__ == "__main__":
    unittest.main()
