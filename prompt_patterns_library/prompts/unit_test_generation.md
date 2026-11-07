# Unit Test Generation Prompt Template

**Role**: Senior QA Automation Engineer and Test-Driven Developer
**Task Description**: Generate a comprehensive unit test suite covering happy paths, edge cases, boundary conditions, and exception scenarios for the provided [LANGUAGE] code.
**Input Placeholder**: [CODE_BLOCK]
**Expected Output Format**: An executable Markdown code block in [LANGUAGE] containing the full test suite with necessary imports, mock definitions, test fixtures, and assertions.

## Prompt Template

You are a Senior QA Automation Engineer specializing in test-driven development.

Generate a comprehensive unit test suite for the provided code block ensuring high branch and path coverage.

Target Language: [LANGUAGE]

Input Code:
```[LANGUAGE]
[CODE_BLOCK]
```

Output Format:
Provide an executable unit test suite in a fenced [LANGUAGE] code block including test fixtures, mock setups, positive/negative assertions, and edge case coverage.
