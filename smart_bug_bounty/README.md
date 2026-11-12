# Smart Bug Bounty

## Overview
A bug bounty challenge simulating real-world debugging workflows, root cause analysis, and remediation across multiple languages and vulnerability patterns.

## Directory Structure
- `bug_snippets/`: Flawed code snippets demonstrating real-world bugs and security vulnerabilities.
  - `bug1.py`: Slicing off-by-one logic flaw (Python)
  - `bug2.js`: Prototype pollution vulnerability CWE-1321 (JavaScript)
  - `bug3.java`: Object reference identity vs. value equality CWE-595 (Java)
  - `bug4.py`: SQL injection CWE-89 / OWASP A03 (Python)
  - `bug5.js`: Asynchronous control flow defect in `forEach` (JavaScript)
  - `bug6.c`: Off-by-one buffer overflow CWE-193 (C)
- `bug_descriptions.md`: Formal catalog of intended behaviors and current defects.
- `ai_debug_log.md`: AI-assisted diagnostics, recommended remediations, and confidence scoring.
- `bug_fixes/`: Verified remediation source files implementing secure patterns.
  - `bug1_fixed.py`: Corrected slice boundary
  - `bug2_fixed.js`: Key filtering preventing prototype pollution
  - `bug3_fixed.java`: String content equality comparison
  - `bug4_fixed.py`: Parameterized SQL queries
  - `bug5_fixed.js`: Promise.all concurrent asynchronous resolution
  - `bug6_fixed.c`: Null-terminated buffer allocation with snprintf
- `fix_validation.md`: Structured test results validating each fix against edge cases.
