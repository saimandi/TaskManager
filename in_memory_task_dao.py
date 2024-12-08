from task_dao import TaskDAO
from errors import *
class InMemoryDAO(TaskDAO):
    def __init__(self):
        self.tasks = []
        self.next_id = 1

    def __len__(self):
        return len(self.tasks)

    def _get_unique_id(self):
        unique_id = self.next_id
        self.next_id += 1
        return unique_id

    def get_tasks(self):
        return self.tasks

    def get_task(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                return task
        raise TaskNotFoundError(f"Task with ID {task_id} not found")


    def create_task(self, task):
        if not task.title:
            raise InvalidTaskError("Task must have a title")
        task.id = self._get_unique_id()  # Assign new ID
        self.tasks.append(task)
        return task

    def update_task(self, partial_task):
        existing_task = self.get_task(partial_task.id)
        if not existing_task:
            return TaskNotFoundError(f"Task with ID {partial_task.id} not found")  # Explicitly handle non-existent task
        if partial_task.title is not None:
            existing_task.title = partial_task.title
        if partial_task.description is not None:
            existing_task.description = partial_task.description
        if partial_task.status is not None:
            existing_task.status = partial_task.status
        return existing_task

    def delete_task(self, task_id):
        task = self.get_task(task_id)
        if not task:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")
        self.tasks.remove(task)
        return True


