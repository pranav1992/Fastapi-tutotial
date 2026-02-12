from app.domain.exceptions import DuplicateEmployeeID, InvalidUserData


def test_duplicate_employee_id_exception():
    exc = DuplicateEmployeeID("123")

    assert exc.employee_id == "123"
    assert "already exists" in str(exc)


def test_invalid_user_data_exception():
    exc = InvalidUserData("Name cannot be empty")

    assert str(exc) == "Name cannot be empty"

    exc = InvalidUserData("Employee ID is required")

    assert str(exc) == "Employee ID is required"