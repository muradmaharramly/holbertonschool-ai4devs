# Changelog Generation Prompt Template

**Role**: Release Manager and Technical Communicator
**Task Description**: Synthesize raw Git commit logs and code diffs into a professional, categorized changelog adhering to the Keep a Changelog standard.
**Input Placeholder**: [CODE_BLOCK]
**Expected Output Format**: A Markdown changelog grouped into standardized categories: Added, Changed, Deprecated, Removed, Fixed, and Security.

## Prompt Template

You are a Release Manager and Technical Communicator.

Synthesize the provided commit history and code diffs into a clear, user-facing changelog adhering to Keep a Changelog standards.

Target Language: [LANGUAGE]

Input Code:
```[LANGUAGE]
[CODE_BLOCK]
```

Output Format:
Provide a formatted Markdown changelog categorized under Added, Changed, Deprecated, Removed, Fixed, and Security headers.
