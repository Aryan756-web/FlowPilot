import unittest
from datetime import date, timedelta

from app.analytics.productivity_analyzer import ProductivityAnalyzer
from app.models.task import Task


class TestProductivityAnalyzer(unittest.TestCase):

    def test_report_with_multiple_tasks(self):
        tasks = [
            Task(
                title="Completed task",
                priority="high",
                estimated_hours=5.0,
                actual_hours=3.0,
                completed=True,
            ),
            Task(
                title="Pending task",
                priority="medium",
                estimated_hours=2.0,
                actual_hours=1.0,
                completed=False,
            ),
        ]

        report = ProductivityAnalyzer(tasks).generate_report()

        self.assertEqual(report["total_tasks"], 2)
        self.assertEqual(report["completed_tasks"], 1)
        self.assertEqual(report["pending_tasks"], 1)
        self.assertEqual(report["completion_rate_percent"], 50.0)
        self.assertEqual(report["estimated_hours"], 7.0)
        self.assertEqual(report["actual_hours"], 4.0)
        self.assertEqual(report["time_variance_hours"], -3.0)
        self.assertEqual(report["time_efficiency_percent"], 175.0)

    def test_empty_task_list(self):
        report = ProductivityAnalyzer([]).generate_report()

        self.assertEqual(report["total_tasks"], 0)
        self.assertEqual(report["completed_tasks"], 0)
        self.assertEqual(report["pending_tasks"], 0)
        self.assertEqual(report["completion_rate_percent"], 0.0)
        self.assertEqual(report["overdue_tasks"], 0)
        self.assertEqual(report["time_efficiency_percent"], None)

    def test_overdue_pending_task(self):
        yesterday = (date.today() - timedelta(days=1)).isoformat()

        tasks = [
            Task(
                title="Overdue task",
                deadline=yesterday,
                completed=False,
            )
        ]

        report = ProductivityAnalyzer(tasks).generate_report()

        self.assertEqual(report["overdue_tasks"], 1)

    def test_completed_overdue_task_is_not_counted(self):
        yesterday = (date.today() - timedelta(days=1)).isoformat()

        tasks = [
            Task(
                title="Completed overdue task",
                deadline=yesterday,
                completed=True,
            )
        ]

        report = ProductivityAnalyzer(tasks).generate_report()

        self.assertEqual(report["overdue_tasks"], 0)

    def test_tasks_by_priority(self):
        tasks = [
            Task(title="Task 1", priority="high"),
            Task(title="Task 2", priority="high"),
            Task(title="Task 3", priority="medium"),
            Task(title="Task 4", priority="low"),
        ]

        result = ProductivityAnalyzer(tasks).tasks_by_priority()

        self.assertEqual(
            result,
            {"high": 2, "medium": 1, "low": 1},
        )

    def test_zero_actual_hours_has_no_efficiency_percentage(self):
        tasks = [
            Task(
                title="Not started",
                estimated_hours=4.0,
                actual_hours=0.0,
            )
        ]

        report = ProductivityAnalyzer(tasks).generate_report()

        self.assertIsNone(report["time_efficiency_percent"])


if __name__ == "__main__":
    unittest.main()
