import csv
import tempfile
import unittest
from pathlib import Path

from app.analytics.productivity_analyzer import ProductivityAnalyzer
from app.models.task import Task
from app.services.report_service import ReportService


class TestReportService(unittest.TestCase):

    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory()
        self.output_directory = Path(self.temp_directory.name)
        self.service = ReportService(str(self.output_directory))

    def tearDown(self):
        self.temp_directory.cleanup()

    def test_export_tasks_to_csv(self):
        tasks = [
            Task(
                title="Build FlowPilot",
                priority="high",
                estimated_hours=5.0,
                actual_hours=3.0,
                completed=True,
            )
        ]

        output_path = self.service.export_tasks_to_csv(tasks)

        self.assertTrue(output_path.exists())

        with output_path.open(
            "r",
            newline="",
            encoding="utf-8-sig",
        ) as csv_file:
            rows = list(csv.DictReader(csv_file))

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["title"], "Build FlowPilot")
        self.assertEqual(rows[0]["priority"], "high")
        self.assertEqual(rows[0]["completed"], "True")

    def test_export_empty_task_list(self):
        output_path = self.service.export_tasks_to_csv([])

        self.assertTrue(output_path.exists())

        with output_path.open(
            "r",
            newline="",
            encoding="utf-8-sig",
        ) as csv_file:
            rows = list(csv.DictReader(csv_file))

        self.assertEqual(rows, [])

    def test_export_productivity_report(self):
        tasks = [
            Task(
                title="Completed task",
                estimated_hours=4.0,
                actual_hours=2.0,
                completed=True,
            )
        ]

        report = ProductivityAnalyzer(tasks).generate_report()

        output_path = self.service.export_productivity_report(report)

        self.assertTrue(output_path.exists())

        with output_path.open(
            "r",
            newline="",
            encoding="utf-8-sig",
        ) as csv_file:
            rows = list(csv.DictReader(csv_file))

        metrics = {row["Metric"]: row["Value"] for row in rows}

        self.assertEqual(metrics["total_tasks"], "1")
        self.assertEqual(metrics["completed_tasks"], "1")
        self.assertEqual(metrics["actual_hours"], "2.0")

    def test_custom_filename(self):
        tasks = [Task(title="Custom filename test")]

        output_path = self.service.export_tasks_to_csv(
            tasks,
            filename="custom_tasks.csv",
        )

        self.assertEqual(output_path.name, "custom_tasks.csv")
        self.assertTrue(output_path.exists())


if __name__ == "__main__":
    unittest.main()
