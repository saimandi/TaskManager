import unittest
from in_memory_task_dao import InMemoryDAO
from task_resource import Task
from errors import TaskNotFoundError, InvalidTaskError  # Import custom errors

class TestInMemoryDAO(unittest.TestCase):
    def setUp(self):
        self.dao = InMemoryDAO()

    def test_create_task(self):
        new_task = self.dao.create_task(Task("Task 1", "Description of task 1", "Pending"))
        self.assertEqual(new_task.get_title(), "Task 1")
        self.assertEqual(new_task.get_description(), "Description of task 1")
        self.assertEqual(new_task.get_status(), "Pending")
        self.assertIsNotNone(new_task.get_id())
        self.assertEqual(len(self.dao.get_tasks()), 1)

        # Test creating a task without a title
        with self.assertRaises(InvalidTaskError) as context:
            self.dao.create_task(Task())
        self.assertEqual(str(context.exception), "Task must have a title")

    def test_get_tasks(self):
        self.dao.create_task(Task("Task 1", "Description of task 1", "Pending"))
        self.dao.create_task(Task("Task 2", "Description of task 2", "Pending"))
        tasks = self.dao.get_tasks()
        self.assertEqual(len(tasks), 2)

    def test_get_task(self):
        task_1 = self.dao.create_task(Task("Task 1", "Description of task 1", "Pending"))
        task_2 = self.dao.create_task(Task("Task 2", "Description of task 2", "Pending"))

        self.assertEqual(task_2.get_id(), self.dao.get_task(task_2.get_id()).get_id())

        # Test getting a non-existent task
        with self.assertRaises(TaskNotFoundError) as context:
            self.dao.get_task(99)
        self.assertEqual(str(context.exception), "Task with ID 99 not found")

    def test_update_task(self):
        task_1 = self.dao.create_task(Task("Task 1", "Description of task 1", "Pending"))
        task_2 = self.dao.create_task(Task("Task 2", "Description of task 2", "Pending"))
        partial_task_2 = Task(title="Updated Task 2", status="Done")
        partial_task_2.id = task_2.get_id()

        updated_task_2 = self.dao.update_task(partial_task_2)
        self.assertEqual(updated_task_2.get_id(), task_2.get_id())
        self.assertEqual(updated_task_2.get_title(), "Updated Task 2")
        self.assertEqual(updated_task_2.get_description(), "Description of task 2")
        self.assertEqual(updated_task_2.get_status(), "Done")

        # Test updating a non-existent task
        non_existent_task = Task(title="Non-existent task", status="Done")
        non_existent_task.id = 99
        with self.assertRaises(TaskNotFoundError) as context:
            self.dao.update_task(non_existent_task)
        self.assertEqual(str(context.exception), "Task with ID 99 not found")

    def test_delete_task(self):
        task_1 = self.dao.create_task(Task("Task 1", "Description of task 1", "Pending"))
        task_2 = self.dao.create_task(Task("Task 2", "Description of task 2", "Pending"))

        self.assertTrue(self.dao.delete_task(task_1.get_id()))
        self.assertEqual(len(self.dao), 1)

        # Test deleting a non-existent task
        with self.assertRaises(TaskNotFoundError) as context:
            self.dao.delete_task(99)
        self.assertEqual(str(context.exception), "Task with ID 99 not found")

if __name__ == "__main__":
    unittest.main()
