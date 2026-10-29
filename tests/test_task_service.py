import tempfile
import unittest
from pathlib import Path

from app.services.storage_service import StorageService
from app.services.task_service import TaskService


class TestTaskService(unittest.TestCase):

    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory()

        storage_path = Path(self.temp_directory.name) / "tasks.json"
        storage = StorageService(str(storage_path))

        self.service = TaskService(storage=storage)

    def tearDown(self):
        self.temp_directory.cleanup()

    def test_create_task(self):
        task = self.service.create_task(
            title="Build FlowPilot",
            priority="high",
            estimated_hours=5.0,
        )

        self.assertEqual(task.title, "Build FlowPilot")
        self.assertEqual(len(self.service.get_all_tasks()), 1)

    def test_get_task_by_id(self):
        task = self.service.create_task(title="Test retrieval")

        retrieved_task = self.service.get_task_by_id(task.task_id)

        self.assertEqual(retrieved_task.task_id, task.task_id)

    def test_get_nonexistent_task(self):
        with self.assertRaises(ValueError):
            self.service.get_task_by_id("nonexistent-id")

    def test_update_task(self):
        task = self.service.create_task(title="Original title")

        updated_task = self.service.update_task(
            task.task_id,
            title="Updated title",
            priority="high",
        )

        self.assertEqual(updated_task.title, "Updated title")
        self.assertEqual(updated_task.priority, "high")

    def test_reject_invalid_update_field(self):
        task = self.service.create_task(title="Test task")

        with self.assertRaises(ValueError):
            self.service.update_task(
                task.task_id,
                completed=True,
            )

    def test_complete_task(self):
        task = self.service.create_task(title="Complete me")

        completed_task = self.service.complete_task(task.task_id)

        self.assertTrue(completed_task.completed)

    def test_delete_task(self):
        task = self.service.create_task(title="Delete me")

        result = self.service.delete_task(task.task_id)

        self.assertTrue(result)
        self.assertEqual(self.service.get_all_tasks(), [])

    def test_delete_nonexistent_task(self):
        with self.assertRaises(ValueError):
            self.service.delete_task("nonexistent-id")


if __name__ == "__main__":
    unittest.main()
