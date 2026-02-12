from app.domain.exceptions import (
    DuplicateTaskName, TaskNameRequired,
    TaskNameLengthExceeded)


def test_duplicate_task_name_exception():
    exc = DuplicateTaskName("123")

    assert exc.task_name == "123"
    assert "already exists" in str(exc)


def test_task_name_required_exception():
    exc = TaskNameRequired("Task name cannot be empty")

    assert exc.message == "Task name cannot be empty"
    assert "Task name cannot be empty" in str(exc)


def test_task_name_length_exceeded_exception():
    exc = TaskNameLengthExceeded("pranav", 3)

    assert exc.task_name == "pranav"
    assert exc.max_length == 3
