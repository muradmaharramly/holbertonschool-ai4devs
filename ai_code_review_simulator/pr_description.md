# Pull Request: Add Task Filtering and Query Execution Feature

## Summary
Implements comprehensive task filtering, multi-attribute sorting, and pagination mechanisms for the task management engine. This feature enables consumers to query tasks dynamically across multiple dimensions including completion status, priority tier, due date boundaries, tag categorization, assignee identity, and keyword search.

## Changes
- **Updated `models.py`**:
  - Defined `TaskStatus` and `TaskPriority` enumerations with explicit domain values.
  - Extended `Task` entity with `tags`, `assignee`, `created_at`, `due_date`, and domain method `is_overdue()`.
  - Introduced `TaskFilterCriteria` data transfer object for structured query parameters.
- **Added `tasks.py`**:
  - Implemented `TaskRepository` for in-memory task aggregation and indexed lookup.
  - Implemented `filter_tasks()` supporting multi-criteria filtering with date range validation and case-insensitive tag matching.
  - Implemented `sort_tasks()` supporting stable ordering by priority, due date, title, and creation timestamp.
  - Implemented `paginate_tasks()` with offset-based slicing and input validation.
- **Added `tests/test_tasks.py`**:
  - Created 12 unit tests validating filtering behaviors, edge cases (invalid ranges, empty results), priority sorting, pagination bounds, and domain logic.

## Context
- **Scope**: ~140 LOC implementation + ~125 LOC test suite.
- **Related Issue**: Resolves #42 (Support flexible task filtering and query execution).
- **Motivation**: Users and downstream services require granular filtering capabilities to inspect pending, overdue, and priority-ranked items without loading entire datasets into memory or writing bespoke sorting routines.
- **Verification**: All 12 unit tests pass cleanly with `python -m unittest discover -s tests -v`.
