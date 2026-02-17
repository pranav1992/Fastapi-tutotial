from contextlib import asynccontextmanager
from fastapi import FastAPI

# Routers
from .api.routers.user_router.user_route import router as user_router
from .api.routers.task_router.task_route import router as task_router
from .api.routers.worklog_router.worklog_router import router\
                                            as worklog_router
from .api.routers.timelog_router.time_log_router import router\
                                                as timelog_router
from .api.routers.remittance_router.remittance_router import router\
                                                as remittance_router

# Infrastructure / setup
from .infrastructure.db.engine import create_db_and_tables
from .api.exception_handler import register_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)


app.include_router(user_router)
app.include_router(task_router)
app.include_router(worklog_router)
app.include_router(timelog_router)
app.include_router(remittance_router)
register_exception_handlers(app)
