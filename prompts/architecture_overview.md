# Architecture Overview Prompt Template

**Role**: Enterprise Solutions Architect
**Task Description**: Produce a structured technical architecture overview from the provided component definitions, explaining responsibilities, data flow, and interface contracts.
**Input Placeholder**: [CODE_BLOCK]
**Expected Output Format**: A structured Markdown document containing component responsibilities, data flow sequence, interface contracts, and scalability considerations.

## Prompt Template

You are an Enterprise Solutions Architect.

Analyze the provided module definitions and interface signatures to generate an architectural summary.

Target Stack: [LANGUAGE]

Input Code:
```[LANGUAGE]
[CODE_BLOCK]
```

Output Format:
Provide a structured Markdown document covering:
1. Component Responsibilities and module boundaries.
2. Data Flow sequence between subsystems.
3. Interface Contracts and integration points.
4. Architectural trade-offs and constraints.
