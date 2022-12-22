import json
import uuid
from datetime import datetime
from json import JSONDecodeError

from aiohttp import web
from model.status import Status
from model.task import Task
from usecase import TaskUseCase

from .encoder import CustomJSONEncoder


class TaskHTTPController:
    def __init__(self, usecase: TaskUseCase) -> None:
        self._usecase = usecase
        self._server = web.Application()
        self._server.add_routes(
            [
                web.post("/tasks", self.create),
                web.patch("/tasks/{id}", self.update),
                web.get("/tasks/{id}", self.get),
                web.get(
                    "/tasks/list?limit={limit}&offset={offset}", self.list
                ),
                web.get("/tasks/search_by?name={name}", self.search_by_name),
                web.get(
                    "/tasks/search_by?status={status}", self.search_by_status
                ),
            ]
        )

    def run(self):
        web.run_app(self._server)

    async def create(self, request: web.Request):

        try:
            body: dict = await request.json()
        except JSONDecodeError as e:
            return web.HTTPBadRequest(text=f"Need JSON; {str(e)}")

        if "name" not in body:
            raise web.HTTPBadRequest(text="Name field is requred")

        if "status" not in body:
            raise web.HTTPBadRequest(text="Status field is requred")

        try:
            status = Status(body["status"])
        except ValueError:
            raise web.HTTPBadRequest(text="invalid status value")

        task = Task(
            id=uuid.uuid4(),
            name=body["name"],
            status=status,
            created_at=datetime.now(),
        )

        try:
            self._usecase.create(task)
        except Exception as e:
            raise web.HTTPInternalServerError(
                text=f"Internal Server Error {str(e)}"
            )

        return web.Response(text=f"Task with id {task.id} was created")

    async def get(self, request: web.Request):

        id = request.match_info["id"]
        try:
            task = self._usecase.get(uuid.UUID(id))
        except Exception as e:
            raise web.HTTPInternalServerError(
                text=f"Internal server error. {str(e)}"
            )

        resp = json.dumps(task, cls=CustomJSONEncoder)
        return web.Response(text=resp)

    async def update(self, request: web.Request):

        try:
            body: dict = await request.json()
        except JSONDecodeError as e:
            return web.HTTPBadRequest(text=f"Need JSON; {str(e)}")

        if "name" not in body:
            raise web.HTTPBadRequest(text="Name field is requred")

        if "status" not in body:
            raise web.HTTPBadRequest(text="Status field is requred")

        try:
            task: Task = self._usecase.get(uuid.UUID(request.match_info["id"]))
        except Exception as e:
            raise web.HTTPInternalServerError(
                text=f"Internal server error! {str(e)}"
            )

        try:
            task.name = body["name"]
        except Exception as e:
            raise web.HTTPInternalServerError(text=f"need JSON; {str(e)}")

        try:
            task.status = task["status"]
        except ValueError as e:
            raise web.HTTPInternalServerError(
                text=f"Internal server error! {str(e)}"
            )

        self._usecase.update(task)
        return web.Response(text=f"Task {task.id} updated! ")

    async def delete(self, request: web.Request):
        try:
            self._usecase.delete(request.match_info["id"])
        except Exception as e:
            raise web.HTTPInternalServerError(
                text=f"Internal server error! {str(e)}"
            )

    async def list(self, limit, offset):
        try:
            task_list = self._usecase.list()
        except Exception as e:
            raise web.HTTPInternalServerError(
                text=f"Internal server error! {str(e)}"
            )

        if limit == 0 or limit > len(task_list):
            limit = len(task_list)

        if (offset + limit) > len(task_list):
            raise web.HTTPBadRequest(
                text="Offset + limit more than list length"
            )

        start_idx = offset
        end_idx = limit - 1
        task_list = task_list[start_idx:end_idx]
        resp = json.dumps(task_list, cls=CustomJSONEncoder)
        return web.Response(text=resp)

    async def search_by_name(self, request: web.Request):
        name_substr = request.match_info("name")
        return self._usecase.search_by_name(name_substr)

    async def search_by_status(self, request: web.Request):
        status = request.match_info("status")
        return self._usecase.search_by_status(status)
