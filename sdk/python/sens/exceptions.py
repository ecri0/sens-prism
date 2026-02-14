"""Sens Prism exception classes."""


class SensError(Exception):
    """Base exception for all Sens errors."""

    def __init__(self, message: str, code: str = None, details: dict = None):
        """Initialize a SensError.

        Args:
            message: Human-readable error message
            code: Machine-readable error code (e.g., SENS_001)
            details: Additional error details as a dictionary
        """
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}

    def __str__(self) -> str:
        """Return string representation of the error."""
        if self.code:
            return f"[{self.code}] {self.message}"
        return self.message


class SensAuthError(SensError):
    """Raised when authentication fails.

    This includes invalid API keys, expired tokens, and missing credentials.
    """

    pass


class SensRateLimitError(SensError):
    """Raised when rate limits are exceeded.

    Includes retry_after information for backoff timing.
    """

    def __init__(self, message: str, retry_after: int = None, **kwargs):
        """Initialize a SensRateLimitError.

        Args:
            message: Error message
            retry_after: Seconds to wait before retrying
            **kwargs: Additional arguments passed to SensError
        """
        super().__init__(message, **kwargs)
        self.retry_after = retry_after


class SensNotFoundError(SensError):
    """Raised when a requested resource is not found.

    This includes missing documents, invalid query IDs, etc.
    """

    pass


class SensValidationError(SensError):
    """Raised when request validation fails.

    This includes malformed requests, missing required fields, etc.
    """

    pass


class SensConflictError(SensError):
    """Raised when request conflicts with current resource state.

    Example: querying a document that's still processing.
    """

    pass


class SensPayloadTooLargeError(SensError):
    """Raised when uploaded file exceeds size limits."""

    pass


class SensServiceUnavailableError(SensError):
    """Raised when the Sens service is temporarily unavailable."""

    def __init__(self, message: str, retry_after: int = None, **kwargs):
        """Initialize a SensServiceUnavailableError.

        Args:
            message: Error message
            retry_after: Seconds to wait before retrying
            **kwargs: Additional arguments passed to SensError
        """
        super().__init__(message, **kwargs)
        self.retry_after = retry_after
