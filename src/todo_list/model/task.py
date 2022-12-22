import datetime
import uuid
from dataclasses import dataclass

from .status import Status


@dataclass
class Task:
    id: uuid.UUID
    name: str
    status: Status
    created_at: datetime
