from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, default="")
    status = db.Column(db.String(50), default="Pending")

    def __repr__(self):
        return f"<Task id={self.id} title={self.title}>"


class DBTaskDAO:
    def __init__(self, db_instance):
        self.db = db_instance

    def get_all_tasks(self):
        return Task.query.all()

    def get_task(self, task_id):
        return self.db.session.get(Task, task_id)  # Updated

    def create_task(self, task):
        new_task = Task(
            title=task.get("title"),
            description=task.get("description", ""),
            status=task.get("status", "Pending"),
        )
        self.db.session.add(new_task)
        self.db.session.commit()
        return new_task

    def update_task(self, task_id, task):
        existing_task = self.db.session.get(Task, task_id)  # Updated
        if existing_task is None:
            return None

        if "title" in task:
            existing_task.title = task["title"]
        if "description" in task:
            existing_task.description = task["description"]
        if "status" in task:
            existing_task.status = task["status"]

        self.db.session.commit()
        return existing_task

    def delete_task(self, task_id):
        task = self.db.session.get(Task, task_id)  # Updated
        if task:
            self.db.session.delete(task)
            self.db.session.commit()
            return True
        return False
