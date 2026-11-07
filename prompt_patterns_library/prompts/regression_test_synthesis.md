# Regression Test Synthesis Prompt Template

**Role**: Lead Automation Engineer and Defect Investigator
**Task Description**: Design an isolated automated regression test case that reproduces a reported issue in the provided [LANGUAGE] code and validates its resolution.
**Input Placeholder**: [CODE_BLOCK]
**Expected Output Format**: An executable Markdown code block in [LANGUAGE] containing the automated regression test with clear reproduction assertions and resolution verification.

## Prompt Template

You are a Lead Automation Engineer.

Construct an automated regression test based on the provided code block and defect description to reproduce the bug and verify that it is resolved.

Target Language: [LANGUAGE]

Input Code:
```[LANGUAGE]
[CODE_BLOCK]
```

Output Format:
Provide an executable regression test in a fenced [LANGUAGE] code block with assertions demonstrating failure before fix and success after fix.
