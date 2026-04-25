from collections.abc import Callable
from pathlib import Path

from .http_foundation.server import Server
from .http_foundation.responses import Response
from .http_foundation.requests import Request
from .status import HTTP_404_NOT_FOUND
from .controllers import ControllerResolver
from .http_foundation.http_response_builder import HttpResponseBuilder


class PyFramework:
    """Main framework class that handles routing and server bootstrap.

    Attributes:
        config_dir: Path to the configuration directory.
        routes: List of route definitions loaded from config.
    """

    def __init__(self, config_dir: str | None = None) -> None:
        """Initializes the PyFramework instance.

        Args:
            config_dir: Path to the config directory. If not provided,
                defaults to "config" relative to the working directory.
        """
        self._routes: list[dict[str, str]] = []
        self._resolver = ControllerResolver()
        self.response_builder = HttpResponseBuilder()

        self.set_config_dir(config_dir)
        self._routes = self.find_routes()

    def set_config_dir(self, config_dir: str | None = None) -> None:
        """Sets the configuration directory.

        Args:
            config_dir: Path to the config directory. If not provided,
                defaults to "config" relative to the working directory.
        """
        if config_dir:
            self.config_dir = Path(config_dir)
        else:
            self.config_dir = Path("config")

        routes_file = self.config_dir / "routes.py"
        if not routes_file.exists():
            raise FileNotFoundError(f"Routes file not found: {routes_file}")

    @property
    def routes(self) -> list[dict[str, str]]:
        """Returns the loaded routes."""
        return self._routes

    def find_routes(self) -> list[dict[str, str]]:
        """Loads and returns routes from the configuration directory.

        Returns:
            List of route definitions.

        Raises:
            ImportError: If routes module cannot be imported.
        """
        import sys

        sys.path.insert(0, str(self.config_dir.parent))
        sys.path.insert(0, "modules")

        from config.routes import routes

        return routes

    def load_controller(
        self,
        request: Request,
    ) -> Response:
        """Handles incoming HTTP requests and dispatches to appropriate controller.

        Args:
            request: Request object containing environ data.

        Returns:
            Response object.
        """
        handler = self._resolver.resolve_handler(request.path, request.method.lower(), self._routes)

        return handler(request) if handler else Response("Not Found", HTTP_404_NOT_FOUND)

    def response_to_server(
        self,
        environ: dict[str, str],
        start_response: Callable[[str, list[tuple[str, str]]], None],
    ) -> list[bytes]:
        """WSGI callback for serving responses.

        Args:
            environ: WSGI environment dictionary containing request details.
            start_response: WSGI callback to set response status and headers.

        Returns:
            Response body as bytes list.
        """
        request = Request(environ)
        response = self.load_controller(request)
        return self.response_builder.build(response, start_response)

    def load(self) -> None:
        """Starts the HTTP server.

        Creates a Server instance and starts serving forever.
        """
        server = Server()
        server.up(self.response_to_server)