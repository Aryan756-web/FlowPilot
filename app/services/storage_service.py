import json
from pathlib import Path

from app.models.task import Task


class StorageService:
    def __init__(self, file_path: str = "data/tasks.json"):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.file_path.exists():
            self._write_tasks([])

    def _write_tasks(self, tasks: list[dict]) -> None:
        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=4)

    def save_tasks(self, tasks: list[Task]) -> None:
        task_data = [task.to_dict() for task in tasks]
        self._write_tasks(task_data)

    def load_tasks(self) -> list[Task]:
        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                task_data = json.load(file)

            if not isinstance(task_data, list):
                raise ValueError("Task data must be a JSON list.")

            return [Task.from_dict(item) for item in task_data]

        except json.JSONDecodeError as exc:
            raise ValueError(
                f"Invalid JSON in storage file: {self.file_path}"
            ) from exc