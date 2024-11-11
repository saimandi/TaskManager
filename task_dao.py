class TaskDAO:
    def get_all_tasks(self):
        raise NotImplementedError

    def get_task(self, task_id):
        raise NotImplementedError

    def create_task(self, task):
        raise NotImplementedError

    def update_task(self, task_id, task):
        raise NotImplementedError

    def delete_task(self, task_id):
        raise NotImplementedError
