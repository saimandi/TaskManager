from task_dao import TaskDAO
from task_resource import Task

class InMemoryDAO(TaskDAO):
    def __init__(self):
        self.tasks = []

    def get_tasks(self):
        return self.tasks

    def get_task(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                return task

    def create_task(self, task):
        task_id = len(self.tasks) + 1 if self.tasks else 1
        new_task = {
            "id": task_id,
            "title": task.get("title"),
            "description": task.get("description", ""),
            "status": task.get("status", "Pending")
        }
        self.tasks.append(new_task)
        return new_task

    def update_task(self, task_id, title=None, description=None, status=None):
        # Find and update a task
        task = self.get_task(task_id)
        if task:
            if title is not None:
                task["title"] = title
            if description is not None:
                task["description"] = description
            if status is not None:
                task["status"] = status
            return task

    def delete_task(self, task_id):
        task = self.get_task(task_id)
        if task:
            self.tasks.remove(task)
            return True
        return False
