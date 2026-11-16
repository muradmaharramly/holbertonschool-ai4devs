#!/usr/bin/env python3
"""Utility script to count words and validate 500-700 word constraints."""
import os
import sys

def get_word_count(filepath: str) -> int:
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    return len(text.split())

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "reflection.md"
    if not os.path.exists(target):
        for candidate in [
            "prompt_patterns_library/reflection.md",
            "reflection.md",
            "prompts/reflection.md",
        ]:
            if os.path.exists(candidate):
                target = candidate
                break

    if not os.path.exists(target):
        print(f"File not found: {target}")
        sys.exit(1)

    count = get_word_count(target)
    print(f"Word count: {count}")
    if 500 <= count <= 700:
        print("PASS: Word count is within 500-700 range.")
        sys.exit(0)
    else:
        print(f"FAIL: Word count {count} is outside 500-700 range.")
        sys.exit(1)

if __name__ == "__main__":
    main()
