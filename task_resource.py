from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from in_memory_task_dao import InMemoryDAO

class Task:
    def __init__(self, title=None, description=None, status=None):
        self.title = title
        self.description = description
        self.status = status
    def get_title(self):
        return self.title
    def get_description(self):
        return self.description
    def get_status(self):
        return self.status
    def to_json(self):
        return {"title": self.title, "description":self.description, "status":self.status}
    @staticmethod
    def from_json(json_task):
        return Task(json_task.get("title"), json_task.get("description"), json_task.get("status"))

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
        def get_tasks(): # provides list of all tasks in json format
            tasks = self.dao.get_tasks() # gets list of task objects
            list_tasks = [task.to_json() for task in tasks] # convert to list of jsons
            return jsonify(list_tasks), 200 # return in a json format

        @self.app.route('/tasks/<int:task_id>', methods=['GET'])  # get specific task
        def get_task(task_id):
            task = self.dao.get_task(task_id) # provide ID to DAO, receive Task() object
            if task:
                return jsonify(task.to_json()), 200 # convert to json and OK status code
            else:
                abort(404, description="Task not found")

        @self.app.route('/tasks/<int:task_id>', methods=['DELETE'])  # delete specific task
        def delete_task(task_id):
            success = self.dao.delete_task(task_id)  # provide ID to DAO, recieve true or false based on success/failure
            if success:
                return '', 204  # No content
            else:
                abort(404, description="Task not found")

        @self.app.route('/tasks', methods=['POST'])  # create task
        def create_task():
            if request.content_type != 'application/json' or request.json is None:
                abort(415, description="Invalid request format")

            if 'title' not in request.json:  # title is required for creation of task
                abort(400, description="Title is required")

            new_task = Task(request.json["title"],request.json.get("description", ""), request.json.get("status", "")) # dissect and create Task()
            self.dao.create_task(new_task)
            # new_task = self.dao.create_task(request.json["title"],
            #                                 request.json.get("description", ""))  # Create task via DAO

            return jsonify(new_task.to_json()), 201  # return json with CREATED

        @self.app.route('/tasks/<int:task_id>', methods=['PATCH'])  # Update task with specific task ID
        def update_task(task_id):
            task = self.dao.get_task(task_id) # check if task exists
            if task is None:
                abort(404, description="Task not found")

            if request.content_type != 'application/json':
                abort(415, description="Unsupported media type")

            try:
                data = request.get_json() # collect json
            except:
                abort(415, description="Invalid JSON format")

            if data is None:
                abort(400, description="Request body must contain JSON data")

            partial_task = Task.from_json(data) # create task object populated partially
            updated_task = self.dao.update_task(partial_task) # send partial task data

            return jsonify(updated_task.to_json()), 200

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
