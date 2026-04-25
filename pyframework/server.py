from collections.abc import Callable, Iterable
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
        self.host = host
        self.port = port

    def up(self, callback: Callable) -> None:
        """Starts the HTTP server and serves forever.

        Args:
            callback: WSGI callable to handle requests.
        """
        server = make_server(self.host, self.port, callback)
        print(f"Serving on http://{self.host}:{self.port}")
        server.serve_forever()