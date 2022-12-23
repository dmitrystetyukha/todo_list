import uuid
from typing import List

from model.status import Status
from model.task import Task
from repository.tasks.base import BaseTask


class InmemoryTasks(BaseTask):
    def __init__(self):
        self._tasks = dict()

    def create(self, new_task: Task):
        self._tasks[new_task.id] = new_task

    def get(self, id: uuid.UUID) -> Task:
        if id not in self._tasks:
            raise KeyError

        return self._tasks[id]

    def update(self, new_task: Task):
        if new_task.id in self._tasks:
            self._tasks[id] = new_task

    def delete(self, id: uuid.UUID):
        del self._tasks[id]

    def list(self) -> List[Task]:
        return list(self._tasks.values())

    def search_by_name(self, name_substr: str) -> List[Task]:
        return list(
            filter(lambda task: name_substr in task.name, self._tasks.values())
        )

    def search_by_status(self, status: Status) -> List[Task]:
        return list(
            filter(lambda task: status == task.status, self._tasks.values())
        )
