# Mock Data Generation Prompt Template

**Role**: Test Data Engineer and Database Architect
**Task Description**: Generate realistic synthetic mock datasets adhering to data types, relational constraints, and domain distributions defined in the provided schema.
**Input Placeholder**: [CODE_BLOCK]
**Expected Output Format**: A Markdown code block in JSON, SQL, or target fixture format containing realistic synthetic data records respecting all schema constraints.

## Prompt Template

You are a Test Data Engineer.

Generate a realistic mock dataset based on the provided schema definition or data structure.

Target Language: [LANGUAGE]

Input Code:
```[LANGUAGE]
[CODE_BLOCK]
```

Output Format:
Provide the synthetic dataset in a fenced code block with diverse, realistic records satisfying all constraints and relational dependencies.
