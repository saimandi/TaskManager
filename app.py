from flask import Flask
from task_resource import TaskResource
from db_task_dao import DBTaskDAO

app = Flask(__name__) # creating Flask instance

task_api = TaskResource(app) # setting up endpoints through API

if __name__ == "__main__":
    app.run()
