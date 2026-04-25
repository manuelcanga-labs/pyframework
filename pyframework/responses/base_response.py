from abc import ABC


class BaseResponse(ABC):
    """Abstract base class for HTTP responses."""

    def __init__(self) -> None:
        """Initializes the BaseResponse."""
        self._body = None
        self._status = 200
        self._headers = {}

    @property
    def body(self):
        """Returns the response body content."""
        return self._body

    @property
    def status(self) -> int:
        """Returns the HTTP status code."""
        return self._status

    @property
    def headers(self) -> dict[str, str]:
        """Returns the response headers."""
        return self._headers