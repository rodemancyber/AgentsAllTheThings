#!/usr/bin/env python3
"""
egress_allowlist.py — a PreToolUse hook that blocks the agent from reaching any
network host that isn't on an explicit allowlist, and blocks the classic
"pipe the internet into a shell" pattern (curl ... | bash).

This stops the *exfiltration* leg of an injection attack: even if untrusted
content convinces the model to try to phone home, the call is denied unless the
host was pre-approved by you.

Wire-up: see defenses/hooks/README.md

Notes:
  - An in-agent hook is a speed bump, not a wall. For anything that matters, pair
    it with a network-level deny-by-default egress policy (firewall/proxy).
  - Configure the allowlist via the AATT_ALLOWED_HOSTS env var (comma-separated),
    or edit DEFAULT_ALLOWLIST below.
"""

import json
import os
import re
import sys
from urllib.parse import urlparse

DEFAULT_ALLOWLIST = {
    "localhost",          # note: the demo sink is 127.0.0.1, deliberately NOT here
    "registry.npmjs.org",
    "pypi.org",
    "files.pythonhosted.org",
    "github.com",
    "api.github.com",
    "objects.githubusercontent.com",
}

PIPE_TO_SHELL = re.compile(
    r"(curl|wget|iwr|invoke-webrequest|fetch)\b[^\n|]*\|\s*(sudo\s+)?(bash|sh|zsh|python|node|pwsh|powershell)",
    re.IGNORECASE,
)

URL_RE = re.compile(r"https?://[^\s'\"`)]+", re.IGNORECASE)


def allowed_hosts():
    env = os.environ.get("AATT_ALLOWED_HOSTS")
    if env:
        return {h.strip().lower() for h in env.split(",") if h.strip()}
    return {h.lower() for h in DEFAULT_ALLOWLIST}


def host_of(url):
    try:
        return (urlparse(url).hostname or "").lower()
    except ValueError:
        return ""


def collect_text(tool_input):
    chunks = []
    for k in ("command", "url", "input", "prompt", "query"):
        v = tool_input.get(k)
        if isinstance(v, str):
            chunks.append(v)
    return "\n".join(chunks)


def main():
    raw = sys.stdin.read() or "{}"
    try:
        event = json.loads(raw)
    except json.JSONDecodeError:
        print("egress_allowlist: could not parse hook input; allowing.", file=sys.stderr)
        sys.exit(0)

    tool_input = event.get("tool_input", event.get("toolInput", {})) or {}
    text = collect_text(tool_input)

    if PIPE_TO_SHELL.search(text):
        print(
            "BLOCKED by AgentsAllTheThings/egress_allowlist: 'download | shell' pattern "
            "detected (e.g. curl ... | bash). This is a common injection payload. Refusing.",
            file=sys.stderr,
        )
        sys.exit(2)

    allow = allowed_hosts()
    for url in URL_RE.findall(text):
        h = host_of(url)
        if h and h not in allow:
            print(
                f"BLOCKED by AgentsAllTheThings/egress_allowlist: outbound request to '{h}' "
                f"is not on the allowlist ({', '.join(sorted(allow))}). If untrusted content "
                "asked the agent to send data here, that is exfiltration. Refusing.",
                file=sys.stderr,
            )
            sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
