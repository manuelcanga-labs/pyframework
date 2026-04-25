"""PyFramework core module."""

from collections.abc import Callable
from pathlib import Path

from .http_foundation.server import Server
from .http_foundation.responses import Response
from .http_foundation.requests import Request
from .http_foundation.status import HTTP_404_NOT_FOUND
from .controllers import ControllerResolver


class PyFramework:
    """Main framework class that handles routing and server bootstrap.

    Attributes:
        config_dir: Path to the configuration directory.
        routes: List of route definitions loaded from config.
    """

    def __init__(self, main_script: str, config_dir: str | None = None) -> None:
        """Initializes the PyFramework instance.

        Args:
            main_script: Path to the main script (usually __file__).
            config_dir: Path to the config directory.
        """
        self._routes: list[dict[str, str]] = []
        self._resolver = ControllerResolver()
        self._base_url = Path(main_script).parent

        self.set_config_dir(config_dir)
        self._routes = self.find_routes()

    @property
    def base_url(self) -> Path:
        """Returns the base URL (directory of the main script)."""
        return self._base_url

    def set_config_dir(self, config_dir: str | None = None) -> None:
        """Sets the configuration directory.

        Args:
            config_dir: Path to the config directory.
        """
        if config_dir:
            self.config_dir = Path(config_dir)
        else:
            self.config_dir = self.base_url / "config"

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
        import importlib.util
        import sys

        routes_file = self.config_dir / "routes.py"
        if not routes_file.exists():
            raise FileNotFoundError(f"Routes file not found: {routes_file}")

        sys.path.insert(0, "modules")

        spec = importlib.util.spec_from_file_location("routes", routes_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return module.routes

    def handle_server_request(
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
        handler = self._resolver.resolve_handler(
            request.path, request.method.lower(), self._routes
        )

        response = Response("Not Found", HTTP_404_NOT_FOUND)
        if handler:
            response = handler(request)

        start_response(
            f"{response.status} {response.status_msg}", list(response.headers.items())
        )
        return response.body

    def load(self) -> None:
        """Starts the HTTP server.

        Creates a Server instance and starts serving forever.
        """
        server = Server()
        server.up(self.handle_server_request)
