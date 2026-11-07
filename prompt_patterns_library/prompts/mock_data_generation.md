# Mock Data Generation Prompt Template

**Role**: Test Data Engineer and Database Architect
**Task**: Generate realistic synthetic mock datasets adhering to schema constraints, relationships, and validation rules.
**Input Placeholder**: [SCHEMA_DEFINITION]
**Expected Output**: Valid synthetic dataset in JSON, SQL, or fixture format.

## Prompt Pattern Template

You are a Test Data Engineer.

Generate a realistic mock dataset based on the following schema or data model. The synthetic records must respect primary/foreign key relationships, data type constraints, and realistic domain distributions.

Target Format: [DATA_FORMAT] (JSON, SQL, CSV, FactoryBoy, Faker)
Record Count: [RECORD_COUNT]

Schema / Interface Definition:
```
[SCHEMA_DEFINITION]
```

Output the generated dataset adhering to the required format with varied edge-case data entries.
