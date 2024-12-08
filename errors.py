class TaskNotFoundError(Exception):
    """Raised when a task is not found."""
    pass

class InvalidTaskError(Exception):
    """Raised when a task is invalid (e.g., missing title)."""
    pass
