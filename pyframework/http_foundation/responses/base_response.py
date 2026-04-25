"""Base response module."""

from abc import ABC

from ..status import HTTP_MESSAGES


class BaseResponse(ABC):
    """Abstract base class for HTTP responses."""

    def __init__(self) -> None:
        """Initializes the BaseResponse."""
        self._body = None
        self._status = 200
        self._headers = {}

    @property
    def body(self) -> list[bytes]:
        """Returns the response body as bytes list."""
        return [self._body if isinstance(self._body, bytes) else self._body.encode("utf-8")]

    @property
    def status(self) -> int:
        """Returns the HTTP status code."""
        return self._status

    @property
    def headers(self) -> dict[str, str]:
        """Returns the response headers."""
        return self._headers

    @property
    def status_msg(self) -> str:
        """Returns the HTTP status message."""
        return HTTP_MESSAGES.get(self.status, "Unknown")
