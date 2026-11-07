# Framework Migration Prompt Template

**Role**: Full-Stack Migration Architect
**Task**: Migrate components, services, or routes from a legacy framework to a modern target framework while preserving functionality.
**Input Placeholder**: [CODE_BLOCK]
**Expected Output**: Converted source code using target framework conventions and idiomatic patterns.

## Prompt Pattern Template

You are a Full-Stack Migration Architect.

Translate the following code snippet from [SOURCE_FRAMEWORK] to [TARGET_FRAMEWORK]. Ensure lifecycle methods, state management, routing, and dependency injections map cleanly to the target framework's idioms.

Source Framework: [SOURCE_FRAMEWORK]
Target Framework: [TARGET_FRAMEWORK]

Source Code:
```
[CODE_BLOCK]
```

Provide:
1. **Migrated Implementation**: Equivalent component or service in [TARGET_FRAMEWORK].
2. **Architectural Mapping Notes**: Key differences in lifecycle or dependency handling.
