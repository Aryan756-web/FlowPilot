import tempfile
import unittest
from pathlib import Path

from app.services.storage_service import StorageService
from app.services.task_service import TaskService


class TestPersistence(unittest.TestCase):

    def test_tasks_survive_service_restart(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            storage_path = Path(temp_dir) / "tasks.json"

            # Start the first service.
            first_storage = StorageService(str(storage_path))
            first_service = TaskService(storage=first_storage)

            # Create a task and save it.
            original_task = first_service.create_task(
                title="Test persistent storage",
                priority="high",
                estimated_hours=4.0,
            )

            original_task_id = original_task.task_id

            # Simulate restarting the application.
            second_storage = StorageService(str(storage_path))
            second_service = TaskService(storage=second_storage)

            # Verify that the task was restored.
            restored_task = second_service.get_task_by_id(
                original_task_id
            )

            self.assertEqual(
                restored_task.title,
                "Test persistent storage",
            )
            self.assertEqual(restored_task.priority, "high")
            self.assertEqual(restored_task.estimated_hours, 4.0)

    def test_completion_status_survives_restart(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            storage_path = Path(temp_dir) / "tasks.json"

            first_service = TaskService(
                storage=StorageService(str(storage_path))
            )

            task = first_service.create_task(title="Complete this task")
            first_service.complete_task(task.task_id)

            # Create a new service using the same file.
            second_service = TaskService(
                storage=StorageService(str(storage_path))
            )

            restored_task = second_service.get_task_by_id(task.task_id)

            self.assertTrue(restored_task.completed)


if __name__ == "__main__":
    unittest.main()
