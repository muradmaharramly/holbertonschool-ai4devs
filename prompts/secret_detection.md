# Secret Detection and Remediation Prompt Template

**Role**: DevSecOps and Infrastructure Security Engineer
**Task**: Detect hardcoded credentials, API keys, certificates, or tokens, and replace them with secure environment abstractions.
**Input Placeholder**: [CODE_BLOCK]
**Expected Output**: Sanitized code and environment variable configuration template.

## Prompt Pattern Template

You are a DevSecOps Engineer auditing source code for embedded secrets.

Review the following file to identify any hardcoded secrets (e.g., API keys, database passwords, private keys, JWT secrets).

Target Language/Format: [LANGUAGE/FORMAT]
Secret Management Tool: [SECRET_TOOL] (e.g., Vault, AWS Secrets Manager, Dotenv)

Code / Configuration:
```
[CODE_BLOCK]
```

Provide:
1. **Identified Secrets**: Inventory of leaked or hardcoded sensitive items.
2. **Remediated Source**: Code refactored to fetch values securely at runtime.
3. **Configuration Template**: Example `.env.example` or secret reference template.
