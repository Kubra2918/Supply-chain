from typing import Dict
from model import Task


def compute_task(task: Task, all_tasks: Dict[str, Task]) -> None:
    if not task.dependencies:
        task.start = 0
        task.end = task.duration
        return

    possible_starts = []

    for dep_name, dep_type, lag in task.dependencies:
        dep_task = all_tasks[dep_name]

        if dep_type == "finish":
            possible_starts.append(dep_task.end + lag)
        elif dep_type == "start":
            possible_starts.append(dep_task.start + lag)

    task.start = max(possible_starts)
    task.end = task.start + task.duration


def get_task_order(all_tasks: Dict[str, Task]) -> list[str]:
    remaining = set(all_tasks.keys())
    order = []

    while remaining:
        progress = False

        for task_name in list(remaining):
            task = all_tasks[task_name]

            dependency_names = [dep_name for dep_name, _, _ in task.dependencies]

            if all(dep in order for dep in dependency_names):
                order.append(task_name)
                remaining.remove(task_name)
                progress = True

        if not progress:
            raise ValueError("Impossible de trouver un ordre valide.")

    return order


def solve_project(tasks: Dict[str, Task]) -> Dict[str, Task]:
    order = get_task_order(tasks)

    for name in order:
        compute_task(tasks[name], tasks)

    return tasks