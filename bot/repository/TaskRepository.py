import os

from utils.injector import Repository


@Repository
class TaskRepository:

    @classmethod
    def init_repository(cls, tasks_path="/tasks"):
        print(os.path.abspath(".."))
        tasks = {}

        for taskName in os.listdir(tasks_path):
            taskPath = os.path.join(tasks_path, taskName)
            tasks[taskName] = cls._get_statement(taskPath)

        cls.tasks = tasks

    @classmethod
    def _get_statement(cls, task_path: str) -> str:

        for name in os.listdir(task_path):

            if name == "statement.txt":
                with open(os.path.join(task_path, name), "r") as f:
                    return f.read()

        raise Exception(f"Statement for task {task_path} not found")

    @classmethod
    def get_tasks(cls):
        return cls.tasks
