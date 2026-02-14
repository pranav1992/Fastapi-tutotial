
from sqlmodel import Session, select
from app.domain.schema import TaskData
from ..models import Task
from app.domain.exceptions import TaskNotFound


class TaskRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, task: TaskData):
        orm = Task(
            name=task.name,
            name_lower=task.name.lower(),
            description=task.description
        )
        self.session.add(orm)
        self.session.commit()
        self.session.refresh(orm)
        return orm

    def get_task_by_name(self, task: TaskData):
        task = Task.select().where(Task.name_lower == task.lower_name).first()
        if not task:
            raise TaskNotFound(task.lower_name)
        return task

    def get_all_tasks(self):
        return self.session.exec(select(Task)).all()

    # def create_worklog_for_month(
    #     self,
    #     user_id: Union[UUID, str],
    #     task_id: Union[UUID, str],
    #     target_date: Optional[date] = None,
    # ):
    #     current = target_date or date.today()
    #     user_uuid = UUID(str(user_id))
    #     task_uuid = UUID(str(task_id))

    #     worklog = WorkLog(
    #         user_id=user_uuid,
    #         task_id=task_uuid,
    #         year=current.year,
    #         month=current.month,
    #     )
    #     # Avoid duplicate worklogs for the same user/task/month
    #     existing = self.session.exec(
    #         select(WorkLog).where(
    #             WorkLog.user_id == user_uuid,
    #             WorkLog.task_id == task_uuid,
    #             WorkLog.year == current.year,
    #             WorkLog.month == current.month,
    #         )
    #     ).first()
    #     if existing:
    #         return existing

    #     self.session.add(worklog)
    #     self.session.commit()
    #     self.session.refresh(worklog)
    #     return worklog
