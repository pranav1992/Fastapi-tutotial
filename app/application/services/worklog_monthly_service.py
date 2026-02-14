# from sqlalchemy.exc import IntegrityError
# from app.infrastructure.db.models import WorkLog


# class MonthlyWorkLogService:
#     def __init__(self, assignment_repo, worklog_repo, session):
#         self.assignment_repo = assignment_repo
#         self.worklog_repo = worklog_repo
#         self.session = session

#     def create_monthly_worklogs(self, year: int, month: int):
#         assignments = self.assignment_repo.get_active_assignments()

#         for assignment in assignments:
#             try:
#                 worklog = WorkLog(
#                     user_id=assignment.user_id,
#                     task_id=assignment.task_id,
#                     year=year,
#                     month=month,
#                 )
#                 self.session.add(worklog)

#             except IntegrityError:
#                 # Worklog already exists → ignore (idempotent)
#                 self.session.rollback()
#                 continue

#         self.session.commit()
