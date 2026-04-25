import json
from pyframework.responses.base_response import BaseResponse


class ResponseJson(BaseResponse):
    """JSON HTTP response object.

    Attributes:
        data: Dictionary to serialize to JSON.
        status_code: HTTP status code. Defaults to 200.
    """

    def __init__(self, data: dict, status_code: int = 200, headers: dict[str, str] = None) -> None:
        """Initializes the ResponseJson.

        Args:
            data: Dictionary to serialize to JSON.
            status_code: HTTP status code. Defaults to 200.
            headers: Additional headers to add.
        """
        super().__init__()
        self._body = json.dumps(data)
        self._status = status_code
        self._headers.update(headers or {})
        self._headers.update({"Content-Type": "application/json"})