import unittest
from flask import Flask
from db_task_dao import db, DBTaskDAO, Task

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

class TestDBTaskDAO(unittest.TestCase):
    @classmethod
    def setUpClass(cls): # creates a new DB for the test class
        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls): # delete DB for test class
        with app.app_context():
            db.drop_all()

    def setUp(self): # reset the database before each test method to prevent interference
        self.dao = DBTaskDAO(db)
        with app.app_context():
            db.session.query(Task).delete()
            db.session.commit()

    def test_create_task(self):
        task_data = {"title": "Test Task 1", "description": "Description 1", "status": "Pending"}
        with app.app_context():
            new_task = self.dao.create_task(task_data)
            self.assertIsNotNone(new_task.id)
            self.assertEqual(new_task.title, "Test Task 1")
            self.assertEqual(new_task.description, "Description 1")
            self.assertEqual(new_task.status, "Pending")

    def test_get_all_tasks(self):
        task1 = {"title": "Task 1", "description": "Description 1"}
        task2 = {"title": "Task 2", "description": "Description 2"}
        with app.app_context():
            self.dao.create_task(task1)
            self.dao.create_task(task2)
            tasks = self.dao.get_all_tasks()
            self.assertEqual(len(tasks), 2)

    def test_get_task(self):
        task_data = {"title": "Test Task"}
        with app.app_context():
            created_task = self.dao.create_task(task_data)
            retrieved_task = self.dao.get_task(created_task.id)
            self.assertEqual(retrieved_task.id, created_task.id)

    def test_update_task(self):
        task_data = {"title": "Old Task"}
        with app.app_context():
            created_task = self.dao.create_task(task_data)
            updated_task = self.dao.update_task(created_task.id, {"title": "New Task", "status": "Completed"})
            self.assertEqual(updated_task.title, "New Task")
            self.assertEqual(updated_task.status, "Completed")

    def test_delete_task(self):
        task_data = {"title": "Delete Task"}
        with app.app_context():
            created_task = self.dao.create_task(task_data)
            result = self.dao.delete_task(created_task.id)
            self.assertTrue(result)
            self.assertIsNone(self.dao.get_task(created_task.id))

if __name__ == '__main__':
    unittest.main()
