import unittest
from datetime import datetime, timedelta

from models import Task, TaskFilterCriteria, TaskPriority, TaskStatus
from tasks import TaskRepository, filter_tasks, paginate_tasks, sort_tasks


class TestTaskFilteringAndManagement(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 11, 12, 12, 0, 0)
        self.tasks = [
            Task(
                id="task-1",
                title="Implement OAuth2 authentication",
                status=TaskStatus.IN_PROGRESS,
                priority=TaskPriority.HIGH,
                due_date=self.now + timedelta(days=2),
                tags=["backend", "security"],
                assignee="alice",
                created_at=self.now - timedelta(days=3),
            ),
            Task(
                id="task-2",
                title="Write unit tests for checkout flow",
                status=TaskStatus.PENDING,
                priority=TaskPriority.CRITICAL,
                due_date=self.now - timedelta(days=1),
                tags=["qa", "testing"],
                assignee="bob",
                created_at=self.now - timedelta(days=2),
            ),
            Task(
                id="task-3",
                title="Update API documentation",
                status=TaskStatus.COMPLETED,
                priority=TaskPriority.LOW,
                due_date=self.now + timedelta(days=5),
                tags=["docs"],
                assignee="alice",
                created_at=self.now - timedelta(days=1),
            ),
            Task(
                id="task-4",
                title="Database index optimization",
                status=TaskStatus.PENDING,
                priority=TaskPriority.MEDIUM,
                due_date=None,
                tags=["database", "performance"],
                assignee="charlie",
                created_at=self.now,
            ),
        ]

    def test_filter_by_status(self):
        criteria = TaskFilterCriteria(status=TaskStatus.PENDING)
        results = filter_tasks(self.tasks, criteria)
        self.assertEqual(len(results), 2)
        self.assertTrue(all(t.status == TaskStatus.PENDING for t in results))

    def test_filter_by_priority(self):
        criteria = TaskFilterCriteria(priority=TaskPriority.CRITICAL)
        results = filter_tasks(self.tasks, criteria)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].id, "task-2")

    def test_filter_by_due_date_range(self):
        criteria = TaskFilterCriteria(
            due_after=self.now,
            due_before=self.now + timedelta(days=3),
        )
        results = filter_tasks(self.tasks, criteria)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].id, "task-1")

    def test_filter_invalid_date_range_raises_error(self):
        criteria = TaskFilterCriteria(
            due_after=self.now + timedelta(days=5),
            due_before=self.now,
        )
        with self.assertRaises(ValueError):
            filter_tasks(self.tasks, criteria)

    def test_filter_by_tag_case_insensitive(self):
        criteria = TaskFilterCriteria(tag="BACKEND")
        results = filter_tasks(self.tasks, criteria)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].id, "task-1")

    def test_filter_by_search_query(self):
        criteria = TaskFilterCriteria(search_query="optimization")
        results = filter_tasks(self.tasks, criteria)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].id, "task-4")

    def test_is_overdue(self):
        overdue_task = self.tasks[1]
        completed_task = self.tasks[2]
        future_task = self.tasks[0]

        self.assertTrue(overdue_task.is_overdue(reference_time=self.now))
        self.assertFalse(completed_task.is_overdue(reference_time=self.now))
        self.assertFalse(future_task.is_overdue(reference_time=self.now))

    def test_sort_tasks_by_priority(self):
        sorted_tasks = sort_tasks(self.tasks, by="priority", descending=True)
        priorities = [t.priority for t in sorted_tasks]
        expected = [
            TaskPriority.CRITICAL,
            TaskPriority.HIGH,
            TaskPriority.MEDIUM,
            TaskPriority.LOW,
        ]
        self.assertEqual(priorities, expected)

    def test_sort_tasks_by_invalid_key(self):
        with self.assertRaises(ValueError):
            sort_tasks(self.tasks, by="unsupported_field")

    def test_paginate_tasks(self):
        page_1 = paginate_tasks(self.tasks, page=1, page_size=2)
        page_2 = paginate_tasks(self.tasks, page=2, page_size=2)
        page_3 = paginate_tasks(self.tasks, page=3, page_size=2)

        self.assertEqual(len(page_1), 2)
        self.assertEqual(page_1[0].id, "task-1")
        self.assertEqual(len(page_2), 2)
        self.assertEqual(page_2[0].id, "task-3")
        self.assertEqual(len(page_3), 0)

    def test_paginate_invalid_arguments(self):
        with self.assertRaises(ValueError):
            paginate_tasks(self.tasks, page=0, page_size=10)
        with self.assertRaises(ValueError):
            paginate_tasks(self.tasks, page=1, page_size=-1)

    def test_task_repository(self):
        repo = TaskRepository(self.tasks[:2])
        self.assertEqual(len(repo.list_all()), 2)
        self.assertIsNotNone(repo.get("task-1"))
        self.assertIsNone(repo.get("non-existent"))

        repo.add(self.tasks[2])
        self.assertEqual(len(repo.list_all()), 3)


if __name__ == "__main__":
    unittest.main()
