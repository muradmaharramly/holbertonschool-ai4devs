# Prompting Debug Assistant

## Overview
A hands-on collection of flawed code samples and structured debugging scenarios designed to evaluate, test, and improve AI-assisted debugging workflows.

## Contents
- [`bug_snippets/`](./bug_snippets/): Directory containing multi-language buggy code snippets (Python, JavaScript, C) covering distinct categories of software defects.
  - [`bug1.py`](./bug_snippets/bug1.py): Numerical moving average off-by-one error (Python).
  - [`bug2.js`](./bug_snippets/bug2.js): Unhandled null property access runtime exception (JavaScript).
  - [`bug3.py`](./bug_snippets/bug3.py): Mutable default argument logical state leakage (Python).
  - [`bug4.js`](./bug_snippets/bug4.js): Lexicographical sorting and string concatenation type coercion (JavaScript).
  - [`bug5.c`](./bug_snippets/bug5.c): Semicolon syntax error in string reversal (C).
  - [`bug6.py`](./bug_snippets/bug6.py): Dictionary size mutation during iteration runtime error (Python).
- [`bug_descriptions.md`](./bug_descriptions.md): Structured Markdown documentation describing each bug's intended behavior, issue type, and technical failure mechanics.
- [`ai_debug_log.md`](./bug_snippets/ai_debug_log.md): AI-assisted debugging interaction logs capturing root-cause diagnosis, suggested fixes, alternative approaches evaluated, and verification results.
