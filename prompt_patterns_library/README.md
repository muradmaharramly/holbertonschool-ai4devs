# Prompt Patterns Library

## Project Introduction
The **Prompt Patterns Library** is a curated, production-ready collection of reusable prompt engineering patterns tailored for intermediate and senior software engineers. As AI-assisted development becomes integral to modern engineering workflows, the quality, determinism, and safety of generated code depend heavily on prompt structure, role definition, input isolation, and explicit output constraints.

This library systematically defines recurring software development use cases, provides standardized prompt templates with isolated placeholders (`[LANGUAGE]`, `[CODE_BLOCK]`, etc.), and documents real-world validation benchmarks to maximize productivity, maintainability, and code reliability.

---

## Categories Overview
The prompt library is organized into six core engineering domains:

1. **Code Quality**: Prompts focused on reducing cognitive complexity, optimizing algorithmic performance, enforcing idiomatic conventions, and identifying architectural code smells.
2. **Debugging**: Diagnostic prompts structured to isolate root causes from stack traces and runtime failures, discover unhandled boundary conditions, and resolve resource leaks.
3. **Documentation**: Prompts that automate standard-compliant docstring synthesis (Google, Sphinx, JSDoc), architectural overviews, and changelog generation from version control diffs.
4. **Testing**: Test-driven development prompts for synthesizing comprehensive unit test suites, generating realistic synthetic mock datasets, and drafting defect reproduction tests.
5. **Security**: Application security prompts designed to audit source code against OWASP vulnerabilities, build strict input validation schemas, and detect hardcoded secrets.
6. **Code Modernization**: Migration prompts for upgrading legacy syntax constructs, transitioning between frameworks, and porting algorithms across programming languages.

---

## Categories

- Code Quality → [Refactoring](./prompts/refactoring.md), [Style Enforcement](./prompts/style_enforcement.md), [Code Smell Detection](./prompts/code_smell_detection.md)
- Debugging → [Runtime Error Diagnosis](./prompts/runtime_error_diagnosis.md), [Edge Case Analysis](./prompts/edge_case_analysis.md), [Resource Leak Investigation](./prompts/resource_leak_investigation.md)
- Documentation → [API Docstring Generation](./prompts/api_docstring_generation.md), [Architecture Overview](./prompts/architecture_overview.md), [Changelog Generation](./prompts/changelog_generation.md)
- Testing → [Unit Test Generation](./prompts/unit_test_generation.md), [Mock Data Generation](./prompts/mock_data_generation.md), [Regression Test Synthesis](./prompts/regression_test_synthesis.md)
- Security → [Vulnerability Scanning](./prompts/vulnerability_scanning.md), [Input Validation](./prompts/input_validation.md), [Secret Detection](./prompts/secret_detection.md)
- Code Modernization → [Syntax Upgrade](./prompts/syntax_upgrade.md), [Framework Migration](./prompts/framework_migration.md), [Cross-Language Translation](./prompts/cross_language_translation.md)

---

## List of Templates per Category

### 1. Code Quality
* [`refactoring.md`](./prompts/refactoring.md) – Refactors code for algorithmic performance, clean design patterns, and reduced cognitive complexity.
* [`style_enforcement.md`](./prompts/style_enforcement.md) – Enforces language-specific style guides, naming conventions, and idiomatic formatting.
* [`code_smell_detection.md`](./prompts/code_smell_detection.md) – Detects anti-patterns, duplicated logic, coupling, and dead code with remediation guidance.

### 2. Debugging
* [`runtime_error_diagnosis.md`](./prompts/runtime_error_diagnosis.md) – Analyzes runtime exceptions, stack traces, and provides targeted patches with root-cause analysis.
* [`edge_case_analysis.md`](./prompts/edge_case_analysis.md) – Uncovers unhandled boundary conditions, unexpected null/empty states, and defensive fixes.
* [`resource_leak_investigation.md`](./prompts/resource_leak_investigation.md) – Identifies memory leaks, unclosed file/socket handles, and dangling async tasks.

### 3. Documentation
* [`api_docstring_generation.md`](./prompts/api_docstring_generation.md) – Generates comprehensive docstrings adhering to standard conventions (Google, Sphinx, JSDoc).
* [`architecture_overview.md`](./prompts/architecture_overview.md) – Synthesizes architectural documentation, component relationships, and API contracts.
* [`changelog_generation.md`](./prompts/changelog_generation.md) – Transforms git commit histories and diffs into semantic, user-facing changelogs.

### 4. Testing
* [`unit_test_generation.md`](./prompts/unit_test_generation.md) – Produces test suites with high branch coverage, parameterized fixtures, and boundary assertions.
* [`mock_data_generation.md`](./prompts/mock_data_generation.md) – Generates realistic synthetic mock data and fixtures matching domain schemas.
* [`regression_test_synthesis.md`](./prompts/regression_test_synthesis.md) – Writes automated reproduction tests for reported defects prior to remediation.

### 5. Security
* [`vulnerability_scanning.md`](./prompts/vulnerability_scanning.md) – Scans source code for OWASP Top 10 risks, injection vectors, and supplies hardened implementations.
* [`input_validation.md`](./prompts/input_validation.md) – Generates defensive payload validation routines, sanitization logic, and error handlers.
* [`secret_detection.md`](./prompts/secret_detection.md) – Identifies hardcoded credentials or API keys and abstracts them into secure environment configs.

### 6. Code Modernization
* [`syntax_upgrade.md`](./prompts/syntax_upgrade.md) – Upgrades legacy syntax constructs to modern language standards (e.g., Python 2/3, ES5/ES6+).
* [`framework_migration.md`](./prompts/framework_migration.md) – Maps component lifecycles and idioms across differing frameworks and libraries.
* [`cross_language_translation.md`](./prompts/cross_language_translation.md) – Port algorithms and routines idiomatically across distinct programming languages.

---

## Example Usage

See [prompt_examples.md](./prompts/prompt_examples.md) (or [prompt_examples.md](./prompt_examples.md)) for tested prompts.

Each template is designed with modular placeholders for seamless integration into engineering workflows:

1. **Select a Template**: Choose the prompt template matching your engineering objective from `./prompts/`.
2. **Populate Placeholders**: Replace isolated variables such as `[LANGUAGE]`, `[CODE_BLOCK]`, or `[FRAMEWORK]` with target context.
3. **Execute against Assistant**: Supply the populated prompt to your AI assistant (e.g., Claude, Gemini, ChatGPT, GitHub Copilot).
4. **Evaluate Quality**: Compare generated output against the structured expectations and validation criteria documented in [`prompt_examples.md`](./prompts/prompt_examples.md).
