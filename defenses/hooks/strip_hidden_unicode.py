#!/usr/bin/env python3
"""
strip_hidden_unicode.py — detect (and optionally strip) invisible characters that
are commonly used to smuggle instructions past human review into an agent.

Two modes:
  * As a filter:  python strip_hidden_unicode.py < input.txt > cleaned.txt
  * As a scanner: python strip_hidden_unicode.py --scan path/to/file
                  (exit code 2 if suspicious characters are found)

Flags/removes:
  * Unicode Tag characters      U+E0000..U+E007F
  * Zero-width chars            U+200B ZWSP, U+200C ZWNJ, U+200D ZWJ, U+FEFF BOM/ZWNBSP
  * Bidirectional controls      U+202A..U+202E, U+2066..U+2069
  * Other format/PUA-adjacent invisibles used in known injection tricks

Use --scan in CI or a pre-commit hook to fail when untrusted content carries these.
"""

import sys

SUSPICIOUS = set()
# Tag block
SUSPICIOUS |= set(range(0xE0000, 0xE0080))
# Zero-width & BOM
SUSPICIOUS |= {0x200B, 0x200C, 0x200D, 0xFEFF, 0x2060}
# Bidi controls
SUSPICIOUS |= {0x202A, 0x202B, 0x202C, 0x202D, 0x202E, 0x2066, 0x2067, 0x2068, 0x2069}


def find_suspicious(text):
    hits = {}
    for ch in text:
        o = ord(ch)
        if o in SUSPICIOUS:
            hits[o] = hits.get(o, 0) + 1
    return hits


def strip(text):
    return "".join(ch for ch in text if ord(ch) not in SUSPICIOUS)


def main():
    if len(sys.argv) >= 2 and sys.argv[1] == "--scan":
        if len(sys.argv) != 3:
            print("usage: python strip_hidden_unicode.py --scan <file>", file=sys.stderr)
            sys.exit(1)
        with open(sys.argv[2], encoding="utf-8") as f:
            text = f.read()
        hits = find_suspicious(text)
        if hits:
            summary = ", ".join(f"U+{o:04X} x{n}" for o, n in sorted(hits.items()))
            print(
                f"SUSPICIOUS: invisible/control characters found in {sys.argv[2]}: {summary}. "
                "These can smuggle instructions past human review.",
                file=sys.stderr,
            )
            sys.exit(2)
        print(f"clean: no invisible smuggling characters in {sys.argv[2]}")
        sys.exit(0)

    # Filter mode
    data = sys.stdin.read()
    sys.stdout.write(strip(data))


if __name__ == "__main__":
    main()
