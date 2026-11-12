"""Core task filtering and query execution service."""

from datetime import datetime
from typing import Dict, List, Optional, Sequence

from models import Task, TaskFilterCriteria, TaskPriority, TaskStatus


class TaskRepository:
    def __init__(self, initial_tasks: Optional[Sequence[Task]] = None) -> None:
        self._tasks: Dict[str, Task] = {}
        if initial_tasks:
            for task in initial_tasks:
                self.add(task)

    def add(self, task: Task) -> None:
        self._tasks[task.id] = task

    def get(self, task_id: str) -> Optional[Task]:
        return self._tasks.get(task_id)

    def list_all(self) -> List[Task]:
        return list(self._tasks.values())


def filter_tasks(tasks: Sequence[Task], criteria: TaskFilterCriteria) -> List[Task]:
    if criteria.due_after and criteria.due_before and criteria.due_after > criteria.due_before:
        raise ValueError("due_after cannot be later than due_before")

    results: List[Task] = []
    normalized_tag = criteria.tag.lower().strip() if criteria.tag else None
    search = criteria.search_query.lower().strip() if criteria.search_query else None

    for task in tasks:
        if criteria.status is not None and task.status != criteria.status:
            continue

        if criteria.priority is not None and task.priority != criteria.priority:
            continue

        if criteria.assignee is not None and task.assignee != criteria.assignee:
            continue

        if criteria.due_before is not None:
            if task.due_date is None or task.due_date > criteria.due_before:
                continue

        if criteria.due_after is not None:
            if task.due_date is None or task.due_date < criteria.due_after:
                continue

        if normalized_tag is not None:
            if not any(normalized_tag == t.lower().strip() for t in task.tags):
                continue

        if search is not None and search not in task.title.lower():
            continue

        results.append(task)

    return results


def sort_tasks(
    tasks: Sequence[Task],
    by: str = "created_at",
    descending: bool = False,
) -> List[Task]:
    valid_keys = {"created_at", "due_date", "priority", "title"}
    if by not in valid_keys:
        raise ValueError(f"Invalid sort key '{by}'. Must be one of {sorted(valid_keys)}")

    priority_weight = {
        TaskPriority.LOW: 1,
        TaskPriority.MEDIUM: 2,
        TaskPriority.HIGH: 3,
        TaskPriority.CRITICAL: 4,
    }

    def sort_key(task: Task):
        if by == "priority":
            return priority_weight.get(task.priority, 0)
        if by == "due_date":
            return (task.due_date is None, task.due_date or datetime.max)
        if by == "title":
            return task.title.lower()
        return task.created_at

    return sorted(tasks, key=sort_key, reverse=descending)


def paginate_tasks(tasks: Sequence[Task], page: int = 1, page_size: int = 10) -> List[Task]:
    if page < 1:
        raise ValueError("page must be an integer greater than or equal to 1")
    if page_size < 1:
        raise ValueError("page_size must be an integer greater than or equal to 1")

    start = (page - 1) * page_size
    end = start + page_size
    return list(tasks[start:end])
