import os


def _get_statement(task_path: str) -> str:

    for name in os.listdir(task_path):

        if name == "statement.txt":
            with open(os.path.join(task_path, name), "r") as f:
                return f.read()

    raise Exception(f"Statement for task {task_path} not found")


def load_tasks(tasks_path: str) -> dict[str, str]:
    tasks = {}

    for taskName in os.listdir(tasks_path):
        taskPath = os.path.join(tasks_path, taskName)
        tasks[taskName] = _get_statement(taskPath)

    return tasks
