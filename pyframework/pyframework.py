from collections.abc import Callable
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

        from config.routes import routes

        self._routes = routes

    def run_controller(
        self,
        environ: dict[str, str],
        start_response: Callable[[str, list[tuple[str, str]]], None],
    ) -> list[bytes]:
        """Handles incoming HTTP requests and dispatches to appropriate controller.

        Args:
            environ: WSGI environment dictionary containing request details.
            start_response: WSGI callback to set response status and headers.

        Returns:
            List containing response body as bytes.
        """
        start_response("200 OK", [("Content-Type", "text/html")])
        return [b"Hola mundo"]

    def load(self) -> None:
        """Starts the HTTP server.

        Creates a Server instance and starts serving forever.
        """
        server = Server()
        server.up(self.run_controller)