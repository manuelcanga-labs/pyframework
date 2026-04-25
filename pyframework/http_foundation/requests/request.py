"""HTTP request module."""

from urllib.parse import parse_qs


class Request:
    """Represents an HTTP request.

    Attributes:
        environ: WSGI environment dictionary containing request details.
    """

    def __init__(self, environ: dict[str, str]) -> None:
        """Initializes the Request instance.

        Args:
            environ: WSGI environment dictionary containing request details.
        """
        self.environ = environ

    def get(self, key: str, default: str = "") -> str:
        """Get a value from the environ dictionary.

        Args:
            key: The key to look up.
            default: Default value if key is not found.

        Returns:
            The value or default.
        """
        return self.environ.get(key, default)

    @property
    def path(self) -> str:
        """Get the request path.

        Returns:
            The PATH_INFO from environ.
        """
        return self.get("PATH_INFO", "/")

    @property
    def method(self) -> str:
        """Get the request method.

        Returns:
            The REQUEST_METHOD from environ, defaults to GET.
        """
        return self.get("REQUEST_METHOD", "GET")

    @property
    def query(self) -> dict[str, list[str]]:
        """Get the query string parameters.

        Returns:
            Dictionary of query parameters (values are lists).
        """
        query_string = self.get("QUERY_STRING", "")
        return parse_qs(query_string)
