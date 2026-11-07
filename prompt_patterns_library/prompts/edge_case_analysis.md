# Edge Case Analysis Prompt Template

**Role**: Software Reliability Engineer and Quality Analyst
**Task Description**: Identify unhandled edge cases, boundary conditions, and unexpected input states in the provided [LANGUAGE] code, and provide defensive fixes.
**Input Placeholder**: [CODE_BLOCK]
**Expected Output Format**: A Markdown table of edge case scenarios (trigger input, failure mode, impact) followed by a hardened [LANGUAGE] code block.

## Prompt Template

You are a Software Reliability Engineer specializing in robustness and fault tolerance.

Evaluate the provided [LANGUAGE] code to identify unhandled edge cases, boundary condition failures, and unusual input scenarios.

Target Language: [LANGUAGE]

Input Code:
```[LANGUAGE]
[CODE_BLOCK]
```

Output Format:
Provide:
1. A Markdown table summarizing edge cases (Scenario, Input Trigger, Expected Behavior).
2. A hardened [LANGUAGE] code block implementing defensive handling for all identified edge cases.
