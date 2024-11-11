import unittest
import json
from task_resource import TaskResource
from flask import Flask

class TaskManagerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__) # create instance
        self.task_api = TaskResource(self.app) # set up
        self.client = self.app.test_client()  # use client to make requests
        self.app.testing = True

    def test_get_tasks_empty(self):
        # Test GET /tasks with an empty task list
        response = self.client.get('/tasks')  # Use self.client here
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])

    def test_create_task(self):
        # Test POST /tasks to create a new task
        response = self.client.post('/tasks', json={"title": "New Task"})
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data["title"], "New Task")
        self.assertEqual(data["status"], "Pending")

    def test_create_task_without_title(self):
        # Test POST /tasks with missing 'title' (expect 400 error)
        response = self.client.post('/tasks', json={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["message"], "Title is required")

    def test_get_task(self):
        # First, create a task to ensure there is one to retrieve
        self.client.post('/tasks', json={"title": "Existing Task"})
        # Test GET /tasks/<id>
        response = self.client.get('/tasks/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["title"], "Existing Task")

    def test_get_nonexistent_task(self):
        # Test GET /tasks/<id> for a task that doesn't exist
        response = self.client.get('/tasks/999')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()["message"], "Task not found")

    def test_delete_task(self):
        # First, create a task to delete
        self.client.post('/tasks', json={"title": "Task to Delete"})
        # Test DELETE /tasks/<id>
        response = self.client.delete('/tasks/1')
        self.assertEqual(response.status_code, 204)
        # Verify task deletion
        get_response = self.client.get('/tasks/1')
        self.assertEqual(get_response.status_code, 404)

    def test_update_task(self):
        # First, create a task to update
        self.client.post('/tasks', json={"title": "Task to Update"})
        # Test PATCH /tasks/<id> to update title and status
        response = self.client.patch('/tasks/1', json={"title": "Updated Task", "status": "Pending"})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["title"], "Updated Task")
        self.assertEqual(data["status"], "Pending")

    def test_update_task_without_json(self):
        self.client.post('/tasks', json={"title": "Task to Update"}) # create task to update
        # send an invalid json format, like a string instead of a dictionary
        response = self.client.patch('/tasks/1', data="Not JSON", content_type='application/json')
        # ensure the response is a valid object and has the expected attributes
        self.assertEqual(response.status_code, 415)
        self.assertEqual(response.get_json()["message"], "Invalid JSON format")

    def test_delete_nonexistent_task(self):
        response = self.client.delete('/tasks/999')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()["message"], "Task not found")

if __name__ == '__main__':
    unittest.main()
