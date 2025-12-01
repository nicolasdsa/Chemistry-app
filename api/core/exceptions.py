class NotFoundError(Exception):
    """Raised when a requested resource is not found."""


class ConflictError(Exception):
    """Raised when a conflict with existing data occurs."""


class BadRequestError(Exception):
    """Raised when the client sends invalid data or violates business rules."""
