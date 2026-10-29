import unittest

from app.models.task import Task


class TestTask(unittest.TestCase):

    def test_task_creation(self):
        task = Task(
            title="Build FlowPilot",
            priority="high",
            estimated_hours=5.0,
        )

        self.assertEqual(task.title, "Build FlowPilot")
        self.assertEqual(task.priority, "high")
        self.assertEqual(task.estimated_hours, 5.0)
        self.assertFalse(task.completed)
        self.assertTrue(task.task_id)

    def test_empty_title_is_rejected(self):
        with self.assertRaises(ValueError):
            Task(title="   ")

    def test_invalid_priority_is_rejected(self):
        with self.assertRaises(ValueError):
            Task(title="Test task", priority="urgent")

    def test_negative_hours_are_rejected(self):
        with self.assertRaises(ValueError):
            Task(title="Test task", estimated_hours=-1)

    def test_invalid_deadline_is_rejected(self):
        with self.assertRaises(ValueError):
            Task(title="Test task", deadline="29-10-2026")

    def test_mark_completed(self):
        task = Task(title="Test task")
        task.mark_completed()

        self.assertTrue(task.completed)

    def test_dictionary_conversion(self):
        task = Task(
            title="Test task",
            priority="medium",
            estimated_hours=2.0,
        )

        restored_task = Task.from_dict(task.to_dict())

        self.assertEqual(restored_task.title, task.title)
        self.assertEqual(restored_task.task_id, task.task_id)
        self.assertEqual(
            restored_task.estimated_hours,
            task.estimated_hours,
        )


if __name__ == "__main__":
    unittest.main()
