# AI Code Review Simulator

This module simulates real-world pull request and code review workflows, providing clean domain entities, querying capabilities, and unit tests designed for AI-driven and human code review evaluation.

## Architecture

- `models.py`: Domain models (`Task`, `TaskStatus`, `TaskPriority`, `TaskFilterCriteria`).
- `tasks.py`: Querying engine containing filtering, sorting, and pagination routines.
- `tests/test_tasks.py`: Unit test suite covering edge cases and criteria combinations.
- `pr_description.md`: Pull Request submission details following standard engineering review templates.

## Running Tests

Execute the unit tests using Python's standard test runner:

```bash
python -m unittest discover -s tests -v
```
