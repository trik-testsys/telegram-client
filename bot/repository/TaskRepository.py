import os

from bot.conf import PATH_TO_TASKS
from bot.teletrik.DI import repository


@repository
class TaskRepository:

    def __init__(self):
        tasks = {}

        for task_name in os.listdir(PATH_TO_TASKS):
            task_path = os.path.join(PATH_TO_TASKS, task_name)
            tasks[task_name] = self._get_statement(task_path)

        self.tasks = tasks

    def _get_statement(self, task_path: str) -> str:

        for name in os.listdir(task_path):

            if name == "statement.txt":
                with open(os.path.join(task_path, name), "r") as f:
                    return f.read()

        raise Exception(f"Statement for task {task_path} not found")

    def get_tasks(self):
        return self.tasks
