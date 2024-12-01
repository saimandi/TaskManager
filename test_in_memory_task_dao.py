import unittest
from flask import Flask
from in_memory_task_dao import InMemoryDAO

class TestInMemoryDAO(unittest.TestCase):
    def setUp(self):
        self.dao = InMemoryDAO()

    def test_create_task(self):
        new_task = self.dao.create_task("Task 1", "Description of task 1")
        self.assertEqual(new_task["title"], "Task 1")
        self.assertEqual(new_task["description"], "Description of task 1")
        self.assertEqual(new_task["status"], "Pending")
        self.assertIn("id", new_task)
        self.assertEqual(len(self.dao.get_tasks()), 1)

    def test_get_tasks(self):
        self.dao.create_task("Task 1", "Description of task 1")
        self.dao.create_task("Task 2", "Description of task 2")
        tasks = self.dao.get_tasks()
        self.assertEqual(len(tasks), 2)

    def test_get_task(self):
        task_1 = self.dao.create_task("Task 1", "Description of task 1")
        task_2 = self.dao.create_task("Task 2", "Description of task 2")
        self.assertEqual(task_2["id"], self.dao.get_task(task_2["id"])["id"])
        self.assertIsNone(self.dao.get_task(99))

    def test_update_task(self):
        task_1 = self.dao.create_task("Task 1", "Description of task 1")
        task_2 = self.dao.create_task("Task 2", "Description of task 2")
        updated_task_2 = self.dao.update_task(task_2["id"], "Updated Task 2", "Updated description of task 2")
        self.assertEqual(updated_task_2["title"], "Updated Task 2")
        self.assertEqual(updated_task_2["description"], "Updated description of task 2")
        self.assertEqual(updated_task_2["status"], "Pending")
        self.assertIn("id", updated_task_2)

        self.assertIsNone(self.dao.update_task(99, "Updated Task 99"))

    def test_delete_task(self):
        task_1 = self.dao.create_task("Task 1", "Description of task 1")
        task_2 = self.dao.create_task("Task 2", "Description of task 2")
        self.assertTrue(self.dao.delete_task(task_1["id"]))
        self.assertFalse(self.dao.delete_task(99))
        self.assertEqual(len(self.dao.get_tasks()), 1)


    if __name__ == "__main__":
        unittest.main()
