import json
import tempfile
import unittest
from pathlib import Path

from app.models.task import Task
from app.services.storage_service import StorageService


class TestStorageService(unittest.TestCase):

    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory()
        self.file_path = Path(self.temp_directory.name) / "tasks.json"
        self.storage = StorageService(str(self.file_path))

    def tearDown(self):
        self.temp_directory.cleanup()

    def test_storage_file_is_created(self):
        self.assertTrue(self.file_path.exists())

    def test_empty_storage_returns_empty_list(self):
        tasks = self.storage.load_tasks()

        self.assertEqual(tasks, [])

    def test_save_and_load_tasks(self):
        original_task = Task(
            title="Build FlowPilot",
            description="Test JSON persistence",
            priority="high",
            estimated_hours=5.0,
            actual_hours=3.0,
        )

        self.storage.save_tasks([original_task])
        loaded_tasks = self.storage.load_tasks()

        self.assertEqual(len(loaded_tasks), 1)
        self.assertEqual(loaded_tasks[0].title, original_task.title)
        self.assertEqual(loaded_tasks[0].task_id, original_task.task_id)
        self.assertEqual(loaded_tasks[0].priority, "high")
        self.assertEqual(loaded_tasks[0].actual_hours, 3.0)

    def test_empty_task_list_can_be_saved(self):
        self.storage.save_tasks([])

        self.assertEqual(self.storage.load_tasks(), [])

    def test_invalid_json_raises_error(self):
        self.file_path.write_text("{invalid json", encoding="utf-8")

        with self.assertRaises(ValueError):
            self.storage.load_tasks()

    def test_non_list_json_raises_error(self):
        self.file_path.write_text(
            json.dumps({"title": "Invalid format"}),
            encoding="utf-8",
        )

        with self.assertRaises(ValueError):
            self.storage.load_tasks()


if __name__ == "__main__":
    unittest.main()
