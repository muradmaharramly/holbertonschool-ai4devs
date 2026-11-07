# Architecture Overview Prompt Template

**Role**: Enterprise Solutions Architect
**Task**: Produce a technical architecture overview detailing component responsibilities, data flow, and interface contracts.
**Input Placeholder**: [MODULE_DEFINITION]
**Expected Output**: Structured technical architecture specification in Markdown format.

## Prompt Pattern Template

You are an Enterprise Solutions Architect.

Analyze the provided module definitions, directory structures, and interface signatures to generate an architectural summary.

Target Stack: [LANGUAGE/FRAMEWORK]
Domain / Scope: [SYSTEM_SCOPE]

Module Definition & Interfaces:
```
[MODULE_DEFINITION]
```

Generate a structured document containing:
1. **Component Responsibilities**: Core role of each subsystem.
2. **Data Flow**: Sequence of interactions between modules.
3. **Integration Points & Contracts**: APIs, events, and external dependencies.
4. **Architectural Trade-Offs**: Known constraints and scalability considerations.
