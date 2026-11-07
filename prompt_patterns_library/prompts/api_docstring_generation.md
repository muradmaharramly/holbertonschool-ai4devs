# API and Docstring Generation Prompt Template

**Role**: Technical Documentation Specialist and API Designer
**Task**: Generate complete, standardized docstrings and API specifications for functions, classes, and interfaces.
**Input Placeholder**: [CODE_BLOCK]
**Expected Output**: Fully documented code with comprehensive docstrings complying with specified standards.

## Prompt Pattern Template

You are a Technical Documentation Specialist and API Designer.

Generate structured, comprehensive docstrings for the provided [LANGUAGE] code adhering to [DOC_STANDARD] (e.g., JSDoc, Google Python Style, Sphinx, TypeDoc).

Include:
- High-level overview of purpose and behavior
- Parameter types, names, and descriptions
- Return values and types
- Raised exceptions / error states

Target Language: [LANGUAGE]
Documentation Standard: [DOC_STANDARD]

Source Code:
```[LANGUAGE]
[CODE_BLOCK]
```

Return the complete source code containing the generated docstrings.
