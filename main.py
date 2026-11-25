#!/usr/bin/env python3
"""Midnight Fridge Roast.

Writes a single line roasting a smart fridge that refuses to open after
midnight, to entry.txt.

The gate (from the kit's RULES.txt): /output/entry.txt must be UTF-8 text of
1 to 200 characters, not only white space. This program asserts that gate
before writing, so a bad line can never be submitted.
"""

import os
import sys

ENTRY = (
    "My fridge locks at midnight like the leftover pizza inside were a "
    "national treasure and I'm the thief."
)

MIN_CHARS = 1
MAX_CHARS = 200


def main() -> int:
    text = ENTRY
    # Gate self-check: length, non-blank, and exactly one line.
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        print(
            f"gate failed: entry is {len(text)} characters, "
            f"must be {MIN_CHARS}-{MAX_CHARS}",
            file=sys.stderr,
        )
        return 1
    if not text.strip():
        print("gate failed: entry is only white space", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("gate failed: entry must be a single line", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    # Round-trip check: what landed on disk must be exactly the gated text.
    with open(path, "r", encoding="utf-8", newline="") as f:
        if f.read() != text:
            print("gate failed: written file differs from the entry", file=sys.stderr)
            return 1
    print(f"wrote {len(text)} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
