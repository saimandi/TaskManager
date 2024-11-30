from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from in_memory_task_dao import InMemoryDAO


class TaskResource:
    def __init__(self, app, dao=None):
        self.app = app
        if dao:
            self.dao = dao
        else:
            self.dao = InMemoryDAO()
        self.setup_endpoints()
        self.setup_error_handlers()

    def setup_endpoints(self):
        @self.app.route('/tasks', methods=['GET'])
        def get_tasks():
            tasks = self.dao.get_tasks()
            return (jsonify(tasks), 200

        @self.app.route('/tasks/<int:task_id>', methods=['GET']))  # get specific task
        def get_task(task_id):
            task = self.dao.get_task(task_id)
            if task:
                return jsonify(task), 200
            else:
                abort(404, description="Task not found")

        @self.app.route('/tasks/<int:task_id>', methods=['DELETE'])  # delete specific task
        def delete_task(task_id):
            success = self.dao.delete_task(task_id)  # Delete task from DAO
            if success:
                return '', 204  # No content
            else:
                abort(404, description="Task not found")

        @self.app.route('/tasks', methods=['POST'])  # create task
        def create_task():
            if request.content_type != 'application/json' or request.json is None:
                abort(415, description="Invalid request format")

            if 'title' not in request.json:  # title is required
                abort(400, description="Title is required")

            new_task = self.dao.create_task(request.json["title"],
                                            request.json.get("description", ""))  # Create task via DAO
            return jsonify(new_task), 201  # Created

        @self.app.route('/tasks/<int:task_id>', methods=['PATCH'])  # Update task with specific task ID
        def update_task(task_id):
            task = self.dao.get_task(task_id)
            if task is None:
                abort(404, description="Task not found")

            if request.content_type != 'application/json':
                abort(415, description="Unsupported media type")

            try:
                data = request.get_json()
            except:
                abort(415, description="Invalid JSON format")

            if data is None:
                abort(400, description="Request body must contain JSON data")

            updated_task = self.dao.update_task(task_id, **data)  # Update task via DAO
            return jsonify(updated_task), 200  # OK

    def setup_error_handlers(self):
        @self.app.errorhandler(400)
        def handle_bad_request(error):
            response = jsonify({"message": error.description})
            response.status_code = 400
            return response

        @self.app.errorhandler(404)
        def handle_not_found(error):
            response = jsonify({"message": error.description})
            response.status_code = 404
            return response

        @self.app.errorhandler(415)
        def handle_invalid_request_format(error):
            response = jsonify({"message": error.description})
            response.status_code = 415
            return response
