from fastapi import Request
from fastapi.responses import JSONResponse

from app.domain.exceptions import (
    DuplicateEmployeeID,
    InvalidUserData,
    UserNotFound,
)


def user_exception_handlers(app):

    @app.exception_handler(DuplicateEmployeeID)
    async def duplicate_employee_handler(
        request: Request,
        exc: DuplicateEmployeeID
    ):
        return JSONResponse(
            status_code=409,
            content={
                "detail": f"Employee ID '{exc.employee_id}' already exists"
            }
        )

    @app.exception_handler(InvalidUserData)
    async def invalid_user_data_handler(
        request: Request,
        exc: InvalidUserData
    ):
        return JSONResponse(
            status_code=400,
            content={"detail": exc.message}
        )

    @app.exception_handler(UserNotFound)
    async def user_not_found_handler(
        request: Request,
        exc: UserNotFound
    ):
        return JSONResponse(
            status_code=404,
            content={"detail": f"User '{exc.user_id}' not found"}
        )
