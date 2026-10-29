from typing import Optional

from app.models.task import Task
from app.services.storage_service import StorageService


class TaskService:
    """Manage tasks and persist changes to JSON storage."""

    def __init__(
        self,
        storage: Optional[StorageService] = None,
    ) -> None:
        self.storage = storage or StorageService()

        loaded_tasks = self.storage.load_tasks()

        self.tasks: dict[str, Task] = {
            task.task_id: task for task in loaded_tasks
        }

    def _persist(self) -> None:
        """Save all current tasks to persistent storage."""
        self.storage.save_tasks(self.get_all_tasks())

    def create_task(
        self,
        title: str,
        description: str = "",
        priority: str = "medium",
        deadline: Optional[str] = None,
        estimated_hours: float = 0.0,
    ) -> Task:
        task = Task(
            title=title,
            description=description,
            priority=priority,
            deadline=deadline,
            estimated_hours=estimated_hours,
        )

        self.tasks[task.task_id] = task
        self._persist()

        return task

    def get_all_tasks(self) -> list[Task]:
        return list(self.tasks.values())

    def get_task_by_id(self, task_id: str) -> Task:
        task = self.tasks.get(task_id)

        if task is None:
            raise ValueError(f"Task not found: {task_id}")

        return task

    def update_task(self, task_id: str, **updates) -> Task:
        task = self.get_task_by_id(task_id)

        allowed_fields = {
            "title",
            "description",
            "priority",
            "deadline",
            "estimated_hours",
            "actual_hours",
        }

        invalid_fields = set(updates) - allowed_fields

        if invalid_fields:
            raise ValueError(
                f"Invalid fields: {', '.join(sorted(invalid_fields))}"
            )

        data = task.to_dict()
        data.update(updates)

        updated_task = Task.from_dict(data)
        self.tasks[task_id] = updated_task
        self._persist()

        return updated_task

    def complete_task(self, task_id: str) -> Task:
        task = self.get_task_by_id(task_id)
        task.mark_completed()
        self._persist()

        return task

    def delete_task(self, task_id: str) -> bool:
        task = self.tasks.pop(task_id, None)

        if task is None:
            raise ValueError(f"Task not found: {task_id}")

        self._persist()

        return True
