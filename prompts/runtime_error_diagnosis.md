# Runtime Error Diagnosis Prompt Template

**Role**: Systems Diagnostics and Debugging Specialist
**Task**: Diagnose runtime exceptions, inspect stack traces, and isolate root failure causes.
**Input Placeholder**: [ERROR_LOG] and [CODE_BLOCK]
**Expected Output**: Root-cause analysis, reproducible explanation, and verified bug fix.

## Prompt Pattern Template

You are an expert Systems Diagnostics and Debugging Specialist.

Analyze the provided stack trace and corresponding source code to identify why the runtime failure occurs and how to permanently resolve it.

Runtime Environment: [ENVIRONMENT]
Language/Framework: [LANGUAGE]

Error Log / Stack Trace:
```
[ERROR_LOG]
```

Failing Source Code:
```[LANGUAGE]
[CODE_BLOCK]
```

Provide:
1. **Root Cause Analysis**: Why and under what conditions the error occurs.
2. **Fixed Code**: Corrected code block resolving the issue.
3. **Prevention Strategy**: Defensive measures to prevent future regressions.
