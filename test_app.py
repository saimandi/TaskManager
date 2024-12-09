import unittest
from flask import Flask
from in_memory_task_dao import InMemoryDAO
from db_task_dao import db, DBTaskDAO, DBTask
from task_resource import TaskResource
from abc import ABC


class TaskManagerBaseTestCase(unittest.TestCase):
    dao_class = None  # Default DAO class

    def setUp(self):
        if self.dao_class is None:
            self.skipTest("Base class: dao_class not defined")
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(self.app)
        self.client = self.app.test_client()  # Set up test client
        if self.dao_class == DBTaskDAO:
            with self.app.app_context():
                db.create_all()
            self.dao = self.dao_class(db)
            with self.app.app_context():
                db.session.query(DBTask).delete()
                db.session.commit()
        elif self.dao_class == InMemoryDAO:
            self.dao = InMemoryDAO()

        self.resource = TaskResource(self.app, self.dao)


    def tearDown(self):
        if isinstance(self.dao, DBTaskDAO):  # Ensure DB teardown only for DBTaskDAO
            with self.app.app_context():
                db.session.remove()
                db.drop_all()

    def test_get_tasks_empty(self):
        response = self.client.get('/tasks')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])

    def test_create_task(self):
        response = self.client.post('/tasks', json={"title": "New Task"})
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data["title"], "New Task")
        self.assertEqual(data["description"], "")
        self.assertEqual(data["status"], "Pending")

    # def test_get_task(self):
    #     self.client.post('/tasks', json={"title": "Existing Task"})
    #     response = self.client.get('/tasks/1')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.get_json()["title"], "Existing Task")
    #
    # def test_update_task(self):
    #     self.client.post('/tasks', json={"title": "Task to Update"})
    #     response = self.client.patch('/tasks/1', json={"title": "Updated Task", "status": "Completed"})
    #     self.assertEqual(response.status_code, 200)
    #     data = response.get_json()
    #     self.assertEqual(data["title"], "Updated Task")
    #     self.assertEqual(data["status"], "Completed")
    #
    # def test_delete_task(self):
    #     self.client.post('/tasks', json={"title": "Task to Delete"})
    #     response = self.client.delete('/tasks/1')
    #     self.assertEqual(response.status_code, 204)
    #     get_response = self.client.get('/tasks/1')
    #     self.assertEqual(get_response.status_code, 404)

# class TestInMemoryDAO(TaskManagerBaseTestCase):
#     dao_class = InMemoryDAO


class TestDBTaskDAO(TaskManagerBaseTestCase):
     dao_class = DBTaskDAO

#     def setUp(self):
#         print("1")
#         # super().setUp()  # Comment this line temporarily
#         print("2")
#         with self.app.app_context():
#             db.create_all()
#             # Initialize DBTaskDAO with the database instance
#             self.dao = self.dao_class(db)
#             print("3")

#
if __name__ == '__main__':
    # unittest.main()
    unittest.main(defaultTest='TestInMemoryDAO')

