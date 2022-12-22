from controller.http import TaskHTTPController
from repository.tasks import InmemoryTasks
from usecase import TaskUseCase

inmemory_tasks = InmemoryTasks()
task_usecase = TaskUseCase(inmemory_tasks)
http_controller = TaskHTTPController(task_usecase)

http_controller.run()
