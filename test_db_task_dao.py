import unittest
from flask import Flask
from db_task_dao import db, DBTaskDAO, DBTask
from task_resource import Task
from errors import *

# Setup Flask application and database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

class TestDBTaskDAO(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Create a new database for the test class."""
        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        """Drop the database for the test class."""
        with app.app_context():
            db.drop_all()

    def setUp(self):
        """Reset the database before each test to prevent interference."""
        self.dao = DBTaskDAO(db)
        with app.app_context():
            db.session.query(DBTask).delete()
            db.session.commit()

    def test_create_task(self):
        """Test creating a new task."""
        task = Task("Test Task 1", "Description 1", "Pending")
        with app.app_context():
            new_task = self.dao.create_task(task)
            self.assertIsNotNone(new_task.id)
            self.assertEqual(new_task.get_title(), "Test Task 1")
            self.assertEqual(new_task.get_description(), "Description 1")
            self.assertEqual(new_task.get_status(), "Pending")

    def test_get_tasks(self):
        """Test retrieving all tasks."""
        task1 = Task("Test Task 1", "Description 1", "Pending")
        task2 = Task("Test Task 2", "Description 2", "Pending")
        with app.app_context():
            self.dao.create_task(task1)
            self.dao.create_task(task2)
            tasks = self.dao.get_tasks()
            self.assertEqual(len(tasks), 2)

    def test_get_task(self):
        """Test retrieving a single task by ID."""
        task1 = Task("Test Task 1", "Description 1", "Pending")
        with app.app_context():
            created_task = self.dao.create_task(task1)
            retrieved_task = self.dao.get_task(created_task.get_id())
            self.assertEqual(retrieved_task.get_id(), created_task.get_id())
            self.assertEqual(retrieved_task.get_title(), "Test Task 1")
            self.assertEqual(retrieved_task.get_description(), "Description 1")
            self.assertEqual(retrieved_task.get_status(), "Pending")

    def test_update_task(self):
        """Test updating an existing task."""
        task = Task("Old Task", "Old Description", "Pending")
        with app.app_context():
            created_task = self.dao.create_task(task)
            created_task.title = "New Task"
            created_task.status = "Completed"
            updated_task = self.dao.update_task(created_task)
            self.assertEqual(updated_task.get_title(), "New Task")
            self.assertEqual(updated_task.get_status(), "Completed")

    def test_delete_task(self):
        """Test deleting a task by ID."""
        task = Task("Delete Task", "Description", "Pending")
        with app.app_context():
            created_task = self.dao.create_task(task)
            result = self.dao.delete_task(created_task.get_id())
            self.assertTrue(result)
            with self.assertRaises(TaskNotFoundError):
                self.dao.get_task(created_task.get_id())

if __name__ == '__main__':
    unittest.main()
