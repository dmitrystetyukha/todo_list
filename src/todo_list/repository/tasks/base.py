import abc
import uuid
from typing import List

from model.status import Status
from model.task import Task


class BaseTask(abc.ABC):
    @abc.abstractmethod
    def get(self, id: uuid.UUID):
        raise NotImplementedError()

    @abc.abstractmethod
    def create(self, new_task: Task):
        raise NotImplementedError()

    @abc.abstractmethod
    def update(self, id: uuid.UUID, new_task: Task):
        raise NotImplementedError()

    @abc.abstractmethod
    def delete(self, id: uuid.UUID):
        raise NotImplementedError()

    @abc.abstractmethod
    def list(self, limit: int, offset: int) -> List[Task]:
        raise NotImplementedError()

    @abc.abstractmethod
    def search_by_name(self, name_substr: str) -> List[Task]:
        raise NotImplementedError()

    @abc.abstractmethod
    def search_by_status(self, status: Status) -> List[Task]:
        raise NotImplementedError()
