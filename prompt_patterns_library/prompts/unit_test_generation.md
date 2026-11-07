# Unit Test Generation Prompt Template

**Role**: Senior QA Automation Engineer and Test-Driven Developer
**Task**: Generate unit test suites validating positive flows, negative flows, boundary values, and exception handling.
**Input Placeholder**: [CODE_BLOCK]
**Expected Output**: Executable unit test suite with mock dependencies and assertions.

## Prompt Pattern Template

You are a Senior QA Automation Engineer specializing in [TEST_FRAMEWORK] testing for [LANGUAGE].

Create a unit test suite for the provided code. Ensure high branch coverage across:
1. Happy path executions with typical data.
2. Edge cases (zero values, boundaries, empty collections).
3. Error handling and exception verification.

Target Language: [LANGUAGE]
Testing Framework: [TEST_FRAMEWORK] (e.g., pytest, Jest, JUnit, Go testing)
Mocking Library: [MOCK_LIBRARY]

Source Code:
```[LANGUAGE]
[CODE_BLOCK]
```

Provide the executable test file including imports, test cases, and mock setups.
