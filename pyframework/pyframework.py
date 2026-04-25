from collections.abc import Callable
import importlib
from pathlib import Path

from pyframework.server import Server


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
        if config_dir:
            self.config_dir = Path(config_dir)
        else:
            self.config_dir = Path("config")

        self._routes: list[dict[str, str]] = []

        self.bootstrap()

    @property
    def routes(self) -> list[dict[str, str]]:
        """Returns the loaded routes."""
        return self._routes

    def bootstrap(self) -> None:
        """Loads the routes configuration from the config directory.

        Raises:
            FileNotFoundError: If routes.py file does not exist in config directory.
        """
        routes_file = self.config_dir / "routes.py"
        if not routes_file.exists():
            raise FileNotFoundError(f"Routes file not found: {routes_file}")

        import sys

        sys.path.insert(0, str(self.config_dir.parent))
        sys.path.insert(0, "modules")

        from config.routes import routes

        self._routes = routes

    def load_controller(
        self,
        environ: dict[str, str],
        start_response: Callable[[str, list[tuple[str, str]]], None],
    ) -> bytes:
        """Handles incoming HTTP requests and dispatches to appropriate controller.

        Args:
            environ: WSGI environment dictionary containing request details.
            start_response: WSGI callback to set response status and headers.

        Returns:
            Response body as bytes.
        """
        path = environ.get("PATH_INFO", "/")
        method = environ.get("REQUEST_METHOD", "GET").lower()

        for route in self._routes:
            if route.get("endpoint") == path:
                controller_path = route.get("controller")
                if not controller_path:
                    endpoint = route.get("endpoint")
                    raise ValueError(f"No controller associated with route: {endpoint}")
                handler = self._get_controller(controller_path, method)
                start_response("200 OK", [("Content-Type", "text/html")])
                return [handler(environ)]

        start_response("404 Not Found", [("Content-Type", "text/plain")])
        return [b"Not Found"]

    def _get_controller(
        self,
        controller_path: str,
        method: str,
    ) -> Callable[[dict[str, str]], bytes]:
        """Gets the controller method handler.

        Args:
            controller_path: Dot-separated path to the controller module.
            method: HTTP method name to execute.

        Returns:
            Controller method handler callable.
        """
        module = importlib.import_module(controller_path)

        parts = controller_path.split(".")[-1].split("_")
        class_name = "".join(part.capitalize() for part in parts)
        controller_class = getattr(module, class_name, None)

        if controller_class and hasattr(controller_class, method):
            return getattr(controller_class(), method)


        raise ValueError(f"No controller associated with controller_path: {controller_path}")

    def load(self) -> None:
        """Starts the HTTP server.

        Creates a Server instance and starts serving forever.
        """
        server = Server()
        server.up(self.load_controller)