"""Task models and data structures for task management."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Task:
    id: str
    title: str
    status: TaskStatus
    priority: TaskPriority
    due_date: Optional[datetime] = None
    tags: List[str] = field(default_factory=list)
    assignee: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)

    def is_overdue(self, reference_time: Optional[datetime] = None) -> bool:
        if self.due_date is None or self.status == TaskStatus.COMPLETED:
            return False
        current = reference_time or datetime.utcnow()
        return self.due_date < current


@dataclass
class TaskFilterCriteria:
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_before: Optional[datetime] = None
    due_after: Optional[datetime] = None
    tag: Optional[str] = None
    assignee: Optional[str] = None
    search_query: Optional[str] = None
