from .routers.user_router.user_exception_handler\
                                            import user_exception_handlers
from .routers.task_router.task_exception_handler\
                                            import task_exception_handler
from .routers.worklog_router.worklog_exception_handler\
                                            import worklog_exception_handler


def register_exception_handlers(app):
    user_exception_handlers(app)
    task_exception_handler(app)
    worklog_exception_handler(app)
