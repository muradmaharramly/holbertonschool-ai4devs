# Code Smell Detection Prompt Template

**Role**: Principal Software Architect
**Task Description**: Inspect the provided [LANGUAGE] code to detect code smells, anti-patterns, duplicated logic, and maintainability risks.
**Input Placeholder**: [CODE_BLOCK]
**Expected Output Format**: A structured Markdown report listing each detected code smell, its severity rating, location description, and a recommended remediation pattern.

## Prompt Template

You are a Principal Software Architect conducting static code analysis.

Analyze the provided code to identify anti-patterns, code smells, and coupling issues.

Target Language: [LANGUAGE]

Input Code:
```[LANGUAGE]
[CODE_BLOCK]
```

Output Format:
Provide a structured Markdown report with:
- Smell Name & Severity (High / Medium / Low)
- Location & Description
- Recommended Remediation Strategy
