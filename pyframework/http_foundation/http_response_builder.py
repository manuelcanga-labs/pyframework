from collections.abc import Callable

from pyframework.http_foundation.responses.base_response import BaseResponse
from pyframework.status import HTTP_MESSAGES


class HttpResponseBuilder:
    """Builds HTTP responses from BaseResponse objects."""

    def build(
        self,
        response: BaseResponse,
        start_response: Callable[[str, list[tuple[str, str]]], None],
    ) -> list[bytes]:
        """Builds the HTTP response from a BaseResponse object.

        Args:
            response: BaseResponse object containing the response data.
            start_response: WSGI callback to set response status and headers.

        Returns:
            List containing response body as bytes.
        """
        status_text = HTTP_MESSAGES.get(response.status, "Unknown")
        start_response(f"{response.status} {status_text}", list(response.headers.items()))

        if isinstance(response.body, bytes):
            return [response.body]
        return [response.body.encode("utf-8")]