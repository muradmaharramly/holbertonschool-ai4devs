# Resource Leak Investigation Prompt Template

**Role**: Systems Performance and Concurrency Engineer
**Task Description**: Detect unclosed connections, memory leaks, file descriptor leaks, or dangling async tasks in the provided [LANGUAGE] code, and implement safe lifecycle management.
**Input Placeholder**: [CODE_BLOCK]
**Expected Output Format**: A structured Markdown diagnostic breakdown of the leak mechanism, followed by a remediated [LANGUAGE] code block demonstrating safe resource disposal.

## Prompt Template

You are a Systems Performance and Concurrency Engineer.

Review the provided code to detect leaks or improper lifecycle management involving memory, sockets, file descriptors, or database connections.

Target Language: [LANGUAGE]

Input Code:
```[LANGUAGE]
[CODE_BLOCK]
```

Output Format:
Provide:
1. Diagnostic breakdown of resource allocation vs. disposal lifecycle issues.
2. Remediated [LANGUAGE] code block implementing safe cleanup idioms.
