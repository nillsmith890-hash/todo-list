import json
import tempfile
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import todo


class TodoStorageTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.tasks_file = Path(self.temp_dir.name) / "tasks.json"
        self.tasks_file_patch = patch.object(todo, "TASKS_FILE", self.tasks_file)
        self.tasks_file_patch.start()

    def tearDown(self):
        self.tasks_file_patch.stop()
        self.temp_dir.cleanup()

    def test_load_tasks_returns_empty_list_when_file_does_not_exist(self):
        self.assertEqual(todo.load_tasks(), [])

    def test_save_and_load_tasks(self):
        tasks = [{"title": "Study Python", "completed": False}]

        self.assertTrue(todo.save_tasks(tasks))
        self.assertEqual(todo.load_tasks(), tasks)

    def test_load_tasks_handles_invalid_json(self):
        self.tasks_file.write_text("not json", encoding="utf-8")

        with patch("sys.stdout", new=StringIO()) as output:
            self.assertEqual(todo.load_tasks(), [])

        self.assertIn("not valid JSON", output.getvalue())

    def test_load_tasks_handles_invalid_task_format(self):
        self.tasks_file.write_text(json.dumps({"title": "Wrong format"}), encoding="utf-8")

        with patch("sys.stdout", new=StringIO()) as output:
            self.assertEqual(todo.load_tasks(), [])

        self.assertIn("invalid format", output.getvalue())


class TodoInputTests(unittest.TestCase):
    def test_add_task_rejects_empty_description(self):
        tasks = []

        with patch("builtins.input", return_value="   "):
            with patch("sys.stdout", new=StringIO()) as output:
                todo.add_task(tasks)

        self.assertEqual(tasks, [])
        self.assertIn("Task cannot be empty", output.getvalue())

    def test_add_task_accepts_valid_description(self):
        tasks = []

        with patch("builtins.input", return_value="Read book"):
            with patch.object(todo, "save_tasks", return_value=True) as save_mock:
                with patch("sys.stdout", new=StringIO()):
                    todo.add_task(tasks)

        self.assertEqual(tasks, [{"title": "Read book", "completed": False}])
        save_mock.assert_called_once_with(tasks)

    def test_get_menu_choice_rejects_invalid_input(self):
        invalid_inputs = ["", "abc", "0", "6"]

        for invalid_input in invalid_inputs:
            with self.subTest(invalid_input=invalid_input):
                with patch("builtins.input", return_value=invalid_input):
                    with patch("sys.stdout", new=StringIO()):
                        self.assertIsNone(todo.get_menu_choice())

    def test_get_menu_choice_accepts_valid_input(self):
        with patch("builtins.input", return_value="3"):
            self.assertEqual(todo.get_menu_choice(), 3)

    def test_get_task_number_rejects_invalid_indices(self):
        tasks = [{"title": "Task A", "completed": False}]
        invalid_inputs = ["", "abc", "0", "2"]

        for invalid_input in invalid_inputs:
            with self.subTest(invalid_input=invalid_input):
                with patch("builtins.input", return_value=invalid_input):
                    with patch("sys.stdout", new=StringIO()):
                        self.assertIsNone(todo.get_task_number(tasks, "Task number: "))

    def test_mark_completed_updates_selected_task(self):
        tasks = [{"title": "Task A", "completed": False}]

        with patch("builtins.input", return_value="1"):
            with patch.object(todo, "save_tasks", return_value=True) as save_mock:
                with patch("sys.stdout", new=StringIO()):
                    todo.mark_completed(tasks)

        self.assertTrue(tasks[0]["completed"])
        save_mock.assert_called_once_with(tasks)

    def test_delete_task_removes_selected_task(self):
        tasks = [{"title": "Task A", "completed": False}]

        with patch("builtins.input", return_value="1"):
            with patch.object(todo, "save_tasks", return_value=True) as save_mock:
                with patch("sys.stdout", new=StringIO()):
                    todo.delete_task(tasks)

        self.assertEqual(tasks, [])
        save_mock.assert_called_once_with(tasks)


if __name__ == "__main__":
    unittest.main()
