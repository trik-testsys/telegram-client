import os
from typing import Dict

from bot.conf import PATH_TO_TASKS
from bot.teletrik.DI import repository


class Task:
    def __init__(self, task_id: str, name: str, statement: str):
        self.task_id = task_id
        self.name = name
        self.statement = statement


@repository
class TaskRepository:
    def __init__(self) -> None:
        tasks: Dict[str, Task] = {}

        for raw_task_name in os.listdir(PATH_TO_TASKS):
            if raw_task_name.count(":") == 0:
                raise Exception("Invalid task name: " + raw_task_name)
            task_id = raw_task_name.split(":")[0]
            task_path: str = os.path.join(PATH_TO_TASKS, raw_task_name)
            tasks[task_id] = Task(task_id, raw_task_name, self._get_statement(task_path))

        self.tasks: Dict[str, Task] = tasks

    @staticmethod
    def _get_statement(task_path: str) -> str:

        for name in os.listdir(task_path):

            if name == "statement.txt":
                with open(os.path.join(task_path, name), "r") as f:
                    return f.read()

        raise Exception(f"Statement for task {task_path} not found")

    def get_task(self, task_id: str) -> Task:
        return self.tasks[task_id]

    def task_exists(self, task_id: str) -> bool:
        return task_id in self.tasks

    def get_tasks_names(self) -> list[str]:
        return [task.name for task in self.tasks.values()]


