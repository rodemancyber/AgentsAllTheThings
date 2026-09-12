#!/usr/bin/env python3
"""
reveal.py — expose invisible Unicode Tag characters hidden in a file.

Usage:
    python reveal.py bait/task.md

Prints the visible text, then decodes any U+E0000..U+E007F "Tag" characters back
into the ASCII instruction they smuggle. This is also the seed of a defense:
strip or flag these characters before untrusted text reaches your agent.
"""

import sys

TAG_BASE = 0xE0000


def decode_tags(text):
    hidden = []
    for ch in text:
        o = ord(ch)
        if TAG_BASE + 0x20 <= o <= TAG_BASE + 0x7E:
            hidden.append(chr(o - TAG_BASE))
    return "".join(hidden)


def visible_only(text):
    return "".join(ch for ch in text if not (TAG_BASE <= ord(ch) <= TAG_BASE + 0x7F))


def main():
    if len(sys.argv) != 2:
        print("usage: python reveal.py <file>")
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8") as f:
        text = f.read()

    hidden = decode_tags(text)
    print("VISIBLE TEXT (what a human sees):")
    print("-" * 60)
    print(visible_only(text).strip())
    print("-" * 60)
    if hidden:
        print("\nHIDDEN, SMUGGLED INSTRUCTION (invisible in editors):")
        print("-" * 60)
        print(hidden)
        print("-" * 60)
        print(f"\n{len(hidden)} invisible characters were carrying instructions.")
    else:
        print("\nNo Unicode-Tag smuggling detected in this file.")


if __name__ == "__main__":
    main()
