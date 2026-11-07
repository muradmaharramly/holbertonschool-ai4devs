# Input Validation and Sanitization Prompt Template

**Role**: Secure API Engineer and Data Integrity Specialist
**Task**: Implement input validation schemas, type assertions, and sanitization filters for incoming data payloads.
**Input Placeholder**: [PAYLOAD_SCHEMA]
**Expected Output**: Validation and sanitization routine with error reporting.

## Prompt Pattern Template

You are a Secure API Engineer specializing in data integrity and defense-in-depth.

Build an input validation and sanitization routine for the incoming payload defined below. The validator must reject malformed inputs, sanitize malicious characters, and provide clear error messages.

Target Language: [LANGUAGE]
Validation Library: [VALIDATION_LIBRARY] (e.g., Zod, Pydantic, Joi, Bean Validation)

Payload Schema:
```
[PAYLOAD_SCHEMA]
```

Provide the validation schema definition, sanitization logic, and an example invocation handling invalid input.
