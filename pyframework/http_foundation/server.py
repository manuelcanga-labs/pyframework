"""HTTP server module."""

from collections.abc import Callable
from wsgiref.simple_server import make_server


class Server:
    """HTTP server wrapper using wsgiref.

    Attributes:
        host: Host address to bind to.
        port: Port number to listen on.
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 8000) -> None:
        """Initializes the Server.

        Args:
            host: Host address to bind to. Defaults to "127.0.0.1".
            port: Port number to listen on. Defaults to 8000.
        """
        self._host = host
        self._port = port

    def up(self, callback: Callable) -> None:
        """Starts the HTTP server and serves forever.

        Args:
            callback: WSGI callable to handle requests.
        """
        server = make_server(self._host, self._port, callback)
        print(f"Serving on http://{self._host}:{self._port}")
        server.serve_forever()

    def info(self) -> dict[str, str | int]:
        """Returns server information.

        Returns:
            Dictionary with host and port information.
        """
        return {"host": self._host, "port": self._port}
