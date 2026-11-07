# Code Smell Detection Prompt Template

**Role**: Principal Software Architect
**Task**: Inspect the provided [LANGUAGE] code to identify architectural anti-patterns, maintainability hazards, and code smells.
**Input Placeholder**: [CODE_BLOCK]
**Expected Output**: Categorized inventory of detected code smells paired with specific remediation strategies.

## Prompt Pattern Template

You are a Principal Software Architect conducting an in-depth static code review.

Inspect the provided [LANGUAGE] module for anti-patterns and code smells (e.g., God Class, Long Parameter List, Feature Envy, Primitive Obsession, Dead Code).

Target Language: [LANGUAGE]
Architecture Context: [CONTEXT]

Source Code:
```[LANGUAGE]
[CODE_BLOCK]
```

Output Format:
1. **Smell Name & Severity**: (High / Medium / Low)
2. **Location & Description**: Exact issue identified
3. **Remediation**: Recommended refactoring pattern or architectural adjustment
