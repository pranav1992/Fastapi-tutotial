class DomainError(Exception):
    """Base class for all domain-level errors"""
    pass


class DuplicateEmployeeID(DomainError):
    def __init__(self, employee_id: str):
        self.employee_id = employee_id
        super().__init__(f"Employee ID '{employee_id}' already exists")


class InvalidUserData(DomainError):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class UserNotFound(DomainError):
    def __init__(self, user_id: str):
        self.user_id = user_id
        super().__init__(f"User '{user_id}' not found")


class DuplicateTaskName(DomainError):
    def __init__(self, task_name: str):
        self.task_name = task_name
        self.message = f"Task with the name '{task_name}' already exists"
        super().__init__(f"Task with the name '{task_name}' already exists")


class TaskNameRequired(DomainError):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class TaskNameLengthExceeded(DomainError):
    def __init__(self, task_name: str, max_length: int):
        self.task_name = task_name
        self.max_length = max_length
        self.message = f"""Task name '{task_name}' exceeds the
                         maximum length of {max_length} characters."""

        super().__init__(self.message)


class TaskNotFound(DomainError):
    def __init__(self, name: str):
        self.name = name
        self.message = f"Task '{name}' not found"
        super().__init__(f"Task '{name}' not found")


class InvalidTaskAssignment(DomainError):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class TaskAlreadyAssigned(DomainError):
    def __init__(self, user_id: str, task_id: str):
        self.user_id = user_id
        self.task_id = task_id
        self.message = f"""User '{user_id}' is already assigned
          to task '{task_id}'"""
        super().__init__(self.message)


class WorkLogNotFound(DomainError):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class WorkLogAlreadyExists(DomainError):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class WorkLogDateRequired(DomainError):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
