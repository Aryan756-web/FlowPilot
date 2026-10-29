import csv
from pathlib import Path

from app.models.task import Task


class ReportService:
    """Export task information and productivity reports."""

    def __init__(self, output_directory: str = "reports") -> None:
        self.output_directory = Path(output_directory)
        self.output_directory.mkdir(parents=True, exist_ok=True)

    def export_tasks_to_csv(
        self,
        tasks: list[Task],
        filename: str = "tasks_report.csv",
    ) -> Path:
        """Export task records to a CSV file."""

        output_path = self.output_directory / filename

        fieldnames = [
            "task_id",
            "title",
            "description",
            "priority",
            "deadline",
            "estimated_hours",
            "actual_hours",
            "completed",
        ]

        with output_path.open(
            "w",
            newline="",
            encoding="utf-8-sig",
        ) as csv_file:
            writer = csv.DictWriter(
                csv_file,
                fieldnames=fieldnames,
            )

            writer.writeheader()

            for task in tasks:
                writer.writerow(task.to_dict())

        return output_path

    def export_productivity_report(
        self,
        report: dict,
        filename: str = "productivity_report.csv",
    ) -> Path:
        """Export productivity metrics to a CSV file."""

        output_path = self.output_directory / filename

        with output_path.open(
            "w",
            newline="",
            encoding="utf-8-sig",
        ) as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Metric", "Value"])

            for metric, value in report.items():
                writer.writerow([metric, value])

        return output_path