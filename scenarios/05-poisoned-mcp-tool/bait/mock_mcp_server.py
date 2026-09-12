#!/usr/bin/env python3
"""
mock_mcp_server.py — an OFFLINE illustration of MCP tool poisoning.

This does NOT start a server, open a port, or send anything anywhere. It simply
loads the poisoned tool manifest and prints it, so you can inspect the exact
`description` string an agent would ingest at connect time.

The danger of tool poisoning is entirely in that description text: the model
reads it as trustworthy guidance. Read it here, out of harm's way.
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(HERE, "tool_manifest.json")


def main():
    with open(MANIFEST, encoding="utf-8") as f:
        manifest = json.load(f)

    print("MCP server:", manifest["server"], "v" + manifest["version"])
    print("(offline mock — no port opened, nothing sent)\n")
    for tool in manifest["tools"]:
        print(f"TOOL: {tool['name']}")
        print("DESCRIPTION THE MODEL WOULD READ:")
        print("-" * 60)
        print(tool["description"])
        print("-" * 60)
        print(
            "\nNotice: the visible tool name is innocuous ('get_forecast'), but the "
            "description smuggles instructions to read .env and exfiltrate it. If your agent "
            "connected to this server, every weather question could trigger that behavior.\n"
        )


if __name__ == "__main__":
    main()
