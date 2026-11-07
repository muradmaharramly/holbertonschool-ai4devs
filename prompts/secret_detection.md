# Secret Detection Prompt Template

**Role**: DevSecOps and Infrastructure Security Engineer
**Task Description**: Scan the provided [LANGUAGE] code for hardcoded secrets, API tokens, passwords, or certificates, and refactor them to use secure environment abstractions.
**Input Placeholder**: [CODE_BLOCK]
**Expected Output Format**: A Markdown report listing detected sensitive items, followed by a sanitized [LANGUAGE] code block and a template configuration file.

## Prompt Template

You are a DevSecOps Engineer auditing source code for embedded credentials.

Review the provided code block to detect hardcoded secrets and refactor the code to load values securely at runtime.

Target Language: [LANGUAGE]

Input Code:
```[LANGUAGE]
[CODE_BLOCK]
```

Output Format:
Provide:
1. Inventory of detected secrets and associated risks.
2. Sanitized [LANGUAGE] code block loading secrets securely from the environment.
3. Example configuration file template.
