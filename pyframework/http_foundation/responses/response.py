from pyframework.http_foundation.responses.base_response import BaseResponse


class Response(BaseResponse):
    """HTTP response object similar to Django's HttpResponse.

    Attributes:
        content: The body content to return (str or bytes).
        status: HTTP status code. Defaults to 200.
    """

    def __init__(self, content: str | bytes = "", status: int = 200, headers: dict[str, str] = None) -> None:
        """Initializes the Response.

        Args:
            content: The body content to return.
            status: HTTP status code. Defaults to 200.
            headers: Additional headers to add.
        """
        super().__init__()
        self._body = content
        self._status = status
        self._headers.update(headers or {})
        self._headers.update({"Content-Type": "text/html"})