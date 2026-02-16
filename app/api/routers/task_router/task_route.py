from fastapi import APIRouter
from app.domain.schema import (
    TaskData, TaskResponse, TaskAssignmentCreate, TaskAssignmentRead)
from sqlmodel import Session
from fastapi import Depends
from app.infrastructure.db.session import get_session
from app.infrastructure.db.repositories.task_repo import TaskRepository
from app.infrastructure.db.repositories.task_assignment_repo\
    import TaskAssignmentRepository
from app.application.services.task_service import TaskService
from app.application.services.task_assignment_service\
                                        import TaskAssignmentService

router = APIRouter(prefix="/tasks")


@router.post("/create-task/")
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


@router.post("/create-task-assignment/", response_model=TaskAssignmentRead)
async def assign_task(data: TaskAssignmentCreate,
                      session: Session = Depends(get_session)):
    repo = TaskAssignmentRepository(session)
    service = TaskAssignmentService(repo)
    return service.create_task_assignment(data)


@router.get("/get-task-assignments/", response_model=list[TaskAssignmentRead])
async def get_all_users_user_id(
        user_id, session: Session = Depends(get_session)):
    repo = TaskAssignmentRepository(session)
    service = TaskAssignmentService(repo)
    return service.get_task_assignments_by_user_id(user_id)


@router.get("/get-task-assignments/", response_model=list[TaskAssignmentRead])
async def get_all_users_task_id(
        task_id, session: Session = Depends(get_session)):
    repo = TaskAssignmentRepository(session)
    service = TaskAssignmentService(repo)
    return service.get_task_assignment_(task_id)


@router.get("/get-all-assigned-tasks/",
            response_model=list[TaskAssignmentRead])
async def get_all_assigned_tasks(session: Session = Depends(get_session)):
    repo = TaskAssignmentRepository(session)
    service = TaskAssignmentService(repo)
    return service.get_all_task_assignments()
