from contextlib import asynccontextmanager
from fastapi import FastAPI
from .api.user_router.user_route import router as router
from .api.task_router.task_route import router as task_router
from .api.worklog_router.worklog_router import router as worklog_router
from .infrastructure.db.engine import create_db_and_tables
from .api.exception_handler import (
    register_exception_handlers,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)


app.include_router(router)
app.include_router(task_router)
app.include_router(worklog_router)
register_exception_handlers(app)
