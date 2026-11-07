# Prompt Use Cases

## Code Quality
- **Refactoring**
  - **Goal**: Improve readability, reduce cognitive complexity, and boost algorithmic performance
  - **Input**: Source function or method in [LANGUAGE]
  - **Output**: Optimized code + explanation of modifications
- **Style Enforcement**
  - **Goal**: Enforce consistent naming conventions, formatting, and language-specific idioms
  - **Input**: Unformatted code snippet in [LANGUAGE]
  - **Output**: Rewritten code compliant with specified style guidelines
- **Code Smell Detection**
  - **Goal**: Identify anti-patterns, duplicated logic, dead code, and high coupling
  - **Input**: Code module or class in [LANGUAGE]
  - **Output**: List of identified code smells with actionable remediation proposals

## Debugging
- **Runtime Error Diagnosis**
  - **Goal**: Identify the root cause of an unexpected exception or crash
  - **Input**: Stack trace, error logs, and relevant source code in [LANGUAGE]
  - **Output**: Root cause explanation + corrected code patch
- **Edge Case Analysis**
  - **Goal**: Discover unhandled boundary conditions, null/empty states, and unexpected inputs
  - **Input**: Function signature and current implementation in [LANGUAGE]
  - **Output**: Enumeration of potential failure edge cases + defensive code adjustments
- **Resource Leak Investigation**
  - **Goal**: Detect unclosed connections, memory leaks, and unresolved async operations
  - **Input**: Resource management or concurrent code block in [LANGUAGE]
  - **Output**: Diagnosis of leak sources + safe resource cleanup pattern

## Documentation
- **API and Docstring Generation**
  - **Goal**: Produce standardized docstrings and API documentation
  - **Input**: Function, class, or public interface in [LANGUAGE]
  - **Output**: Complete documentation block following conventions like JSDoc, Sphinx, or Docstrings
- **Architecture Overview**
  - **Goal**: Provide high-level technical documentation for a component or service
  - **Input**: Directory structure, schema definitions, and key interfaces in [LANGUAGE/FRAMEWORK]
  - **Output**: Structured technical overview detailing responsibilities, dependencies, and data flow
- **Changelog and Release Notes Generation**
  - **Goal**: Translate raw commits and code differences into clear, user-facing release notes
  - **Input**: Git commit logs or unified diff between versions
  - **Output**: Markdown-formatted changelog grouped by Features, Fixes, and Breaking Changes

## Testing
- **Unit Test Generation**
  - **Goal**: Produce comprehensive test suites covering valid execution paths and error scenarios
  - **Input**: Target function implementation in [LANGUAGE] and testing framework [TEST_FRAMEWORK]
  - **Output**: Executable unit test suite with mock definitions and assertions
- **Mock Data Generation**
  - **Goal**: Generate realistic mock datasets and fixture objects for testing
  - **Input**: Data schema, interface definition, or sample object in [FORMAT/LANGUAGE]
  - **Output**: Valid synthetic dataset matching schema constraints in JSON or fixture format
- **Regression Test Synthesis**
  - **Goal**: Create automated tests reproducing an identified bug before applying a fix
  - **Input**: Bug description, expected vs. actual behavior, and code snippet in [LANGUAGE]
  - **Output**: Targeted test case verifying bug reproduction and subsequent resolution

## Security
- **Vulnerability Scanning**
  - **Goal**: Identify common security vulnerabilities like injection flaws, SSRF, or insecure deserialization
  - **Input**: Controller, route handler, or query logic in [LANGUAGE]
  - **Output**: Vulnerability audit summary + hardened code implementation
- **Input Sanitization and Validation**
  - **Goal**: Implement defensive validation and sanitization for external user input
  - **Input**: Data transfer object or request payload schema in [LANGUAGE]
  - **Output**: Validation schema and sanitization routines
- **Secret Detection and Remediation**
  - **Goal**: Detect hardcoded API keys, passwords, or tokens and replace them with secure abstractions
  - **Input**: Configuration files or codebase extract
  - **Output**: Sanitized code + configuration using environment variables or secret manager patterns

## Code Modernization
- **Syntax and Feature Upgrade**
  - **Goal**: Upgrade legacy language syntax to modern language versions and standards
  - **Input**: Legacy code snippet in [LANGUAGE] and target version [TARGET_VERSION]
  - **Output**: Refactored code utilizing modern language constructs
- **Framework Migration**
  - **Goal**: Migrate components or modules from an obsolete library/framework to a modern alternative
  - **Input**: Source code in [SOURCE_FRAMEWORK] and target framework [TARGET_FRAMEWORK]
  - **Output**: Functionally equivalent code rewritten using target framework paradigms
- **Cross-Language Translation**
  - **Goal**: Translate algorithms or utilities from one programming language to another
  - **Input**: Source code in [SOURCE_LANGUAGE] and target language [TARGET_LANGUAGE]
  - **Output**: Idiomatic implementation translated into [TARGET_LANGUAGE]
