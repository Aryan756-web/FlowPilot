from datetime import date

import pandas as pd

from app.models.task import Task


class ProductivityAnalyzer:
    """Analyze task data and generate productivity reports."""

    def __init__(self, tasks: list[Task]) -> None:
        self.tasks = tasks

    def _to_dataframe(self) -> pd.DataFrame:
        """Convert task objects into a Pandas DataFrame."""

        records = [
            {
                "task_id": task.task_id,
                "title": task.title,
                "priority": task.priority,
                "deadline": task.deadline,
                "estimated_hours": task.estimated_hours,
                "actual_hours": task.actual_hours,
                "completed": task.completed,
            }
            for task in self.tasks
        ]

        return pd.DataFrame(
            records,
            columns=[
                "task_id",
                "title",
                "priority",
                "deadline",
                "estimated_hours",
                "actual_hours",
                "completed",
            ],
        )

    def generate_report(self) -> dict:
        """Calculate overall productivity metrics."""

        dataframe = self._to_dataframe()

        total_tasks = len(dataframe)
        completed_tasks = int(dataframe["completed"].sum())
        pending_tasks = total_tasks - completed_tasks

        completion_rate = (
            round((completed_tasks / total_tasks) * 100, 2)
            if total_tasks > 0
            else 0.0
        )

        today = date.today().isoformat()

        overdue_mask = (
            dataframe["deadline"].notna()
            & (dataframe["deadline"] < today)
            & (~dataframe["completed"])
        )

        overdue_tasks = int(overdue_mask.sum())

        estimated_hours = round(
            float(dataframe["estimated_hours"].sum()), 2
        )

        actual_hours = round(
            float(dataframe["actual_hours"].sum()), 2
        )

        time_variance = round(
            actual_hours - estimated_hours, 2
        )

        time_efficiency = (
            round((estimated_hours / actual_hours) * 100, 2)
            if actual_hours > 0
            else None
        )

        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "completion_rate_percent": completion_rate,
            "overdue_tasks": overdue_tasks,
            "estimated_hours": estimated_hours,
            "actual_hours": actual_hours,
            "time_variance_hours": time_variance,
            "time_efficiency_percent": time_efficiency,
        }

    def tasks_by_priority(self) -> dict[str, int]:
        """Count tasks grouped by priority."""

        dataframe = self._to_dataframe()

        priority_counts = dataframe["priority"].value_counts()

        return {
            priority: int(priority_counts.get(priority, 0))
            for priority in ("high", "medium", "low")
        }