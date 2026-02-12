from app.domain.exceptions import WorkLogAlreadyExists
from fastapi.responses import JSONResponse
from fastapi import Request


def worklog_exception_handler(app):
    @app.exception_handler(WorkLogAlreadyExists)
    def worklog_already_exists_exception_handler(
            request: Request,
            exc: WorkLogAlreadyExists):
        return JSONResponse(
            status_code=409,
            content={"message": exc.message}
        )
