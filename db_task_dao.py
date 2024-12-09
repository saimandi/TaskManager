from flask_sqlalchemy import SQLAlchemy
from task_dao import TaskDAO
from errors import *
from task_resource import Task
db = SQLAlchemy()


class DBTask(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, default="")
    status = db.Column(db.String(50), default="Pending")

    def __repr__(self):
        return f"<Task id={self.id} title={self.title}>"


class DBTaskDAO(TaskDAO):
    def __init__(self, db_instance):
        self.db = db_instance

    def __len__(self):
        return self.db.session.query(DBTask).count()

    def get_tasks(self):
        db_tasks = DBTask.query.all()
        tasks = []
        for db_task in db_tasks:
            task = Task(title=db_task.title, description=db_task.description, status=db_task.status)
            task.id = db_task.id
            tasks.append(task)
        return tasks

    def get_task(self, task_id):
        db_task = self.db.session.get(DBTask, task_id)
        if not db_task:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")
        task = Task(title=db_task.title, description=db_task.description, status=db_task.status)
        task.id = db_task.id
        return task

    def create_task(self, task):
        if not task.title:
            raise InvalidTaskError("Task must have a title")
        new_task = DBTask(
            title=task.get_title(),
            description=task.get_description(),
            status=task.get_status(),
        )
        self.db.session.add(new_task)
        self.db.session.commit()
        task.id = new_task.id
        return task

    def update_task(self, partial_task):
        db_task = self.db.session.get(DBTask, partial_task.get_id())
        if not db_task:
            raise TaskNotFoundError(f"Task with ID {partial_task.get_id()} not found")
        if partial_task.title is not None:
            db_task.title = partial_task.title
        if partial_task.description is not None:
            db_task.description = partial_task.description
        if partial_task.status is not None:
            db_task.status = partial_task.status
        self.db.session.commit()
        updated_task = Task(title=db_task.title, description=db_task.description, status=db_task.status)
        updated_task.id = db_task.id
        return updated_task

    def delete_task(self, task_id):
        db_task = self.db.session.get(DBTask, task_id)
        if not db_task:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")
        self.db.session.delete(db_task)
        self.db.session.commit()
        return True
