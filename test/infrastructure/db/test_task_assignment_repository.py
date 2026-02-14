from app.infrastructure.db.repositories.task_assignment_repo import TaskAssignmentRepository


def test_task_assignment_create_success(session):
    repo = TaskAssignmentRepository(session)

    assignment = repo.task_assignment_to_user(
        user_id="11111111-1111-1111-1111-111111111111",
        task_id="22222222-2222-2222-2222-222222222222",
    )

    assert assignment.id is not None
    assert str(assignment.user_id) == "11111111-1111-1111-1111-111111111111"
    assert str(assignment.task_id) == "22222222-2222-2222-2222-222222222222"
    assert assignment.active is True
