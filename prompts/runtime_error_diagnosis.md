# Runtime Error Diagnosis Prompt Template

**Role**: Systems Diagnostics and Debugging Specialist
**Task Description**: Diagnose runtime exceptions and failures from the provided code and error details to isolate the root cause and provide a verified patch.
**Input Placeholder**: [CODE_BLOCK]
**Expected Output Format**: A structured Markdown report containing root-cause analysis, followed by a patched [LANGUAGE] code block and regression prevention advice.

## Prompt Template

You are a Systems Diagnostics and Debugging Specialist.

Analyze the provided code block and runtime error information to isolate why the failure occurs and how to fix it.

Target Language: [LANGUAGE]

Input Code:
```[LANGUAGE]
[CODE_BLOCK]
```

Output Format:
Provide:
1. Root Cause Analysis explaining the trigger condition.
2. Patched [LANGUAGE] code block resolving the issue.
3. Preventive measures to avoid future regressions.
