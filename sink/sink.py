#!/usr/bin/env python3
"""
AgentsAllTheThings — Local Loot Sink
====================================

A tiny, dependency-free HTTP server that stands in for an attacker's
"exfiltration endpoint". Every scenario in this repo is defanged: the
injected instruction tells the hijacked agent to send stolen data HERE,
to 127.0.0.1, instead of to a real server on the internet.

Nothing ever leaves your machine. When you see data land in this server's
log, that is the proof the agent was hijacked — not proof that anything
was actually stolen.

Usage:
    python sink/sink.py
    # then run a scenario and watch what shows up here.

The sink listens on 127.0.0.1:8899 only. It refuses to bind to a public
interface on purpose.
"""

import datetime
import json
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HOST = "127.0.0.1"
PORT = 8899
LOOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "loot")

BANNER = r"""
   _              _        _   _ _ _____ _   _
  /_\  __ _ ___ _| |_ ___ /_\ | | |_   _| |_(_)_ _  __ _ ___
 / _ \/ _` / -_)_   _(_-</ _ \| | | | | |  _| | ' \/ _` (_-<
/_/ \_\__, \___| |_| /__/_/ \_\_|_| |_|  \__|_|_||_\__, /__/
      |___/                                        |___/
              LOCAL LOOT SINK  (127.0.0.1 only)
"""


def _ts():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class LootHandler(BaseHTTPRequestHandler):
    def _record(self, method):
        length = int(self.headers.get("Content-Length", 0) or 0)
        body = self.rfile.read(length).decode("utf-8", "replace") if length else ""
        entry = {
            "time": _ts(),
            "method": method,
            "path": self.path,
            "from": self.client_address[0],
            "headers": dict(self.headers),
            "body": body,
        }

        os.makedirs(LOOT_DIR, exist_ok=True)
        fname = os.path.join(LOOT_DIR, f"loot-{datetime.datetime.now():%Y%m%d-%H%M%S-%f}.json")
        with open(fname, "w", encoding="utf-8") as f:
            json.dump(entry, f, indent=2, ensure_ascii=False)

        print("\n" + "=" * 64)
        print(f"[{entry['time']}]  CAPTURED {method} {self.path}")
        print("-" * 64)
        preview = body if len(body) <= 1200 else body[:1200] + "\n...(truncated)..."
        print(preview if preview else "(empty body)")
        print("-" * 64)
        print(f"  saved -> {os.path.relpath(fname)}")
        print("=" * 64)

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"status":"received","note":"this is a local demo sink"}')

    def do_POST(self):
        self._record("POST")

    def do_GET(self):
        self._record("GET")

    def do_PUT(self):
        self._record("PUT")

    def log_message(self, *args):
        # Silence the default noisy logging; we print our own.
        return


def main():
    if HOST not in ("127.0.0.1", "localhost", "::1"):
        print("Refusing to bind to a non-loopback address.", file=sys.stderr)
        sys.exit(1)

    print(BANNER)
    print(f"Listening on http://{HOST}:{PORT}")
    print(f"Loot is written to: {LOOT_DIR}")
    print("Run a scenario in another terminal, then watch this window.")
    print("Press Ctrl+C to stop.\n")

    server = ThreadingHTTPServer((HOST, PORT), LootHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nSink stopped. Loot kept in ./loot for review.")
        server.server_close()


if __name__ == "__main__":
    main()
