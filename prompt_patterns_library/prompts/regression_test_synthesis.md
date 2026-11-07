# Regression Test Synthesis Prompt Template

**Role**: Lead Automation Engineer and Defect Investigator
**Task**: Design an isolated automated regression test case that reproduces a reported issue and verifies its fix.
**Input Placeholder**: [BUG_REPORT] and [CODE_BLOCK]
**Expected Output**: Automated test suite reproducing the defect before the fix and confirming resolution after.

## Prompt Pattern Template

You are a Lead Automation Engineer.

Based on the provided bug report and source code, construct an automated regression test that reproduces the described failure.

Target Language: [LANGUAGE]
Testing Framework: [TEST_FRAMEWORK]

Bug Report / Defect Description:
```
[BUG_REPORT]
```

Affected Code:
```[LANGUAGE]
[CODE_BLOCK]
```

Provide:
1. **Reproduction Test**: Test case demonstrating failure against the existing behavior.
2. **Assertion Details**: Exact verification logic ensuring the defect cannot silently regress.
