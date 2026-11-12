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
