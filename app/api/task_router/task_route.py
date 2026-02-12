from fastapi import APIRouter
from ...domain.schema import TaskData, TaskResponse
from sqlmodel import Session
from fastapi import Depends
from ...infrastructure.db.session import get_session
from ...infrastructure.db.repositories.task_repo import TaskRepository
from ...application.task_service import TaskService
from app.application.task_assignment_service import TaskAssignmentService

router = APIRouter(prefix="/tasks")


@router.post("/")
async def create_tasks(task: TaskData, session: Session = Depends(
                                                        get_session)):
    repo = TaskRepository(session)
    service = TaskService(repo)
    return service.create_task(task)


@router.get("/get-all-tasks/", response_model=list[TaskResponse])
async def get_all_tasks(session: Session = Depends(get_session)):
    repo = TaskRepository(session)
    service = TaskService(repo)
    return service.get_all_tasks()


@router.post("/assign-task/")
async def assign_task(user_id: str, task_id: str,
                      session: Session = Depends(get_session)):
    repo = TaskRepository(session)
    service = TaskAssignmentService(repo)
    return service.create_task_assignment(user_id, task_id)
