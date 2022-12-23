from asyncio import Task
from typing import List
from uuid import UUID

from model import Status
from repository.tasks import BaseTask


class TaskUseCase:
    def __init__(self, tasks: BaseTask):
        self._tasks = tasks

    def get(self, id: UUID):
        return self._tasks.get(id)

    def create(self, new_task: UUID):
        self._tasks.create(new_task)

    def update(self, new_task: Task):
        self._tasks.update(new_task)

    def delete(self, id: UUID):
        self._tasks.delete(id)

    def list(self) -> List[Task]:
        return self._tasks.list()

    def search_by_name(self, name_substr: str) -> List[Task]:
        return self._tasks.search_by_name(name_substr)

    def search_by_status(self, status: Status) -> List[Task]:
        return self._tasks.search_by_status(status)
