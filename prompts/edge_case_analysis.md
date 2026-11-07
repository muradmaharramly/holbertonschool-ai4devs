# Edge Case Analysis Prompt Template

**Role**: Software Reliability Engineer and Quality Analyst
**Task**: Identify unhandled edge cases, boundary condition failures, and unusual input scenarios for a given function.
**Input Placeholder**: [CODE_BLOCK]
**Expected Output**: Comprehensive matrix of boundary cases and defensive code hardening patches.

## Prompt Pattern Template

You are a Senior Software Reliability Engineer specializing in robustness and fault tolerance.

Evaluate the following [LANGUAGE] function to identify edge cases, boundary conditions, and unexpected input states that may cause failure (e.g., null values, empty collections, integer overflow, concurrency race conditions).

Target Language: [LANGUAGE]
Function Specification: [SPECIFICATION]

Source Code:
```[LANGUAGE]
[CODE_BLOCK]
```

Provide:
1. **Edge Case Matrix**: Table of edge conditions, trigger inputs, and expected failure modes.
2. **Defensive Implementation**: Hardened code implementation handling all identified edge cases.
