# Resource Leak Investigation Prompt Template

**Role**: Systems Performance and Concurrency Engineer
**Task**: Investigate unclosed I/O streams, memory leaks, dangling connections, or thread starvation in the target code.
**Input Placeholder**: [CODE_BLOCK]
**Expected Output**: Leak root cause identification accompanied by reliable resource disposal patterns.

## Prompt Pattern Template

You are a Systems Performance and Concurrency Engineer.

Review the following [LANGUAGE] implementation to identify leaks or improper lifecycle management involving database connections, sockets, file descriptors, memory references, or asynchronous tasks.

Target Language: [LANGUAGE]
Runtime Context: [RUNTIME_CONTEXT]

Source Code:
```[LANGUAGE]
[CODE_BLOCK]
```

Provide:
1. **Leak Diagnosis**: Detailed explanation of resource allocation vs. disposal lifecycle issues.
2. **Remediated Code**: Implementation using idiomatic cleanup mechanisms (e.g., context managers, try-with-resources, defer, RAII).
