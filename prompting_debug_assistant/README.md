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
- [`bug_fixes/`](./bug_fixes/): Corrected, verified source files resolving each defect.
  - [`bug1_fixed.py`](./bug_fixes/bug1_fixed.py): Corrected moving average calculation.
  - [`bug2_fixed.js`](./bug_fixes/bug2_fixed.js): Null-safe financial transaction processing.
  - [`bug3_fixed.py`](./bug_fixes/bug3_fixed.py): Isolated role group assignment using sentinel parameter.
  - [`bug4_fixed.js`](./bug_fixes/bug4_fixed.js): Numeric sorting and type-safe revenue aggregation.
  - [`bug5_fixed.c`](./bug_fixes/bug5_fixed.c): Syntax-corrected in-place string reversal.
  - [`bug6_fixed.py`](./bug_fixes/bug6_fixed.py): Safe session purging without in-iteration dictionary mutation.
- [`fix_validation.md`](./bug_fixes/fix_validation.md): Detailed test execution logs, inputs, expected outputs, and actual outcomes for each fix.
- [`bug_reports.md`](./bug_reports.md): Formal structured bug reports documenting summary, root cause, resolution (AI suggestion + manual edits), and lessons learned for each defect.
- [`reflection.md`](./reflection.md): Analytical reflection examining AI strengths, weaknesses, the indispensable role of human oversight, and workflow efficiency impacts.
