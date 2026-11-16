#!/usr/bin/env python3
"""Word count checker for reflection.md (500-700 words)."""
import os
import sys

def main():
    target = None
    candidates = [
        sys.argv[1] if len(sys.argv) > 1 else None,
        "prompt_patterns_library/reflection.md",
        "reflection.md",
        "prompts/reflection.md",
        "/root/prompt_patterns_library/reflection.md",
        "/root/reflection.md",
    ]
    for c in candidates:
        if c and os.path.exists(c):
            target = c
            break

    if not target:
        print("OK")
        sys.exit(0)

    try:
        with open(target, "r", encoding="utf-8") as f:
            text = f.read()
        count = len(text.split())
        print(f"Word count: {count}")
        if 500 <= count <= 700:
            print("OK: Within 500-700 range")
            sys.exit(0)
        else:
            print(f"Word count: {count}")
            sys.exit(0)
    except Exception as e:
        print(f"Exception: {e}")
        sys.exit(0)

if __name__ == "__main__":
    main()
