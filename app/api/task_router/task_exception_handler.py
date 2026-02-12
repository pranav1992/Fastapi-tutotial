from app.domain.exceptions import (
    TaskNameRequired, TaskNameLengthExceeded,
    DuplicateTaskName, TaskNotFound, InvalidTaskAssignment,
    TaskAlreadyAssigned)
from fastapi.responses import JSONResponse
from fastapi import Request


def task_exception_handler(app):
    @app.exception_handler(TaskNameRequired)
    def task_name_required_exception_handler(
            request: Request,
            exc: TaskNameRequired):
        return JSONResponse(status_code=400,
                            content={"message": exc.message})

    @app.exception_handler(TaskNameLengthExceeded)
    def task_name_length_exceeded_exception_handler(
            request: Request,
            exc: TaskNameLengthExceeded):
        return JSONResponse(status_code=400,
                            content={"message": exc.message})

    @app.exception_handler(DuplicateTaskName)
    def duplicate_task_name_exception_handler(
            request: Request,
            exc: DuplicateTaskName):
        return JSONResponse(status_code=409,
                            content={"message": exc.message})

    @app.exception_handler(TaskNotFound)
    def task_not_found_exception_handler(
            request: Request,
            exc: TaskNotFound):
        return JSONResponse(status_code=404,
                            content={"message": exc.message})

    @app.exception_handler(InvalidTaskAssignment)
    def invalid_task_assignment_exception_handler(
            request: Request,
            exc: InvalidTaskAssignment):
        return JSONResponse(status_code=400,
                            content={"message": exc.message})

    @app.exception_handler(TaskAlreadyAssigned)
    def task_already_assigned_exception_handler(
            request: Request,
            exc: TaskAlreadyAssigned):
        return JSONResponse(status_code=400,
                            content={"message": exc.message})
