from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from datetime import datetime

tasks = [] # in memory tasks

class TaskResource:
	def __init__(self, app): # require Flask instance
		self.app = app
		self.tasks = [] #{id: X, title: X, description: X, status: X}
		self.setup_endpoints() # define endpoints of REST API
		self.setup_error_handlers()

	def _find_task(self, task_id): # helper function to return task object from provided task_id
		for task in self.tasks:
			if task_id == task["id"]:
				return task

	def setup_endpoints(self):
		@self.app.route('/tasks', methods=['GET']) # get all tasks
		def get_tasks():
			return jsonify(self.tasks), 200 # sending request back to client containing data(json of tasks) and HTTP status code (can also be headers)
			# 200 = OK

		@self.app.route('/tasks/<int:task_id>', methods=['GET']) # get specific task
		def get_task(task_id):
			task = self._find_task(task_id)
			if task:
				return jsonify(task), 200
			else:
				abort(404, description="Task not found") # triggers Flask's automatic error handling system which will provide the client with an error with the status code and description in the response body in the "error key

		@self.app.route('/tasks/<int:task_id>', methods=['DELETE']) # delete specific task
		def delete_task(task_id):
			task = self._find_task(task_id)
			if task:
				self.tasks.remove(task)
				return '', 204 # 204 = No Content
			else:
				abort(404, description="Task not found") # 404 = Not Found

		@self.app.route('/tasks', methods=['POST']) # create task
		def create_task():
			if request.content_type != 'application/json' or request.json is None:
				abort(415, description="Invalid request format") # 415 = Unsupported media type

			if 'title' not in request.json: # title required
				abort(400, description="Title is required") # 400 = Bad request

			new_task = {
				"id": len(self.tasks) + 1 if self.tasks else 1, # generate task ID
				"title": request.json["title"],
				"description": request.json.get("description", ""), # parse input
				"status": "Pending"
			}
			self.tasks.append(new_task)
			return jsonify(new_task), 201 # 201 = Created

		@self.app.route('/tasks/<int:task_id>', methods=['PATCH'])  # Update task with specific task ID
		def update_task(task_id):
			# Find the task by ID
			task = self._find_task(task_id)
			if task is None: # task with specified ID DNE
				abort(404, description="Task not found")

			if request.content_type != 'application/json':
				abort(415, description="Unsupported media type")
			try:
				data = request.get_json()
			except:
				abort(415, description="Invalid JSON format") # maybe should be 400

			# Ensure we have JSON data to update
			if data is None:
				abort(400, description="Request body must contain JSON data")

			# Parse and update fields if provided
			task["title"] = data.get("title", task["title"])
			task["description"] = data.get("description", task["description"])
			task["status"] = data.get("status", task["status"])

			return jsonify(task), 200  # 200 = OK

	def setup_error_handlers(self):
		# abort() allows you to specify response code and description, which is provided in the HTTP response body, but will not be provided
		# Flask will provide standard HTML error page with this, not structured data like JSON
		# error handlers allows you to customize the error response as ecpected
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



