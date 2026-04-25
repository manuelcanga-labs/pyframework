"""Controller resolver module."""

import importlib


class ControllerResolver:
    """Resolves HTTP handlers from routes."""

    def __init__(self) -> None:
        """Initializes the ControllerResolver."""
        self._current_route: dict[str, str] | None = None

    def resolve_handler(
        self,
        path: str,
        method: str,
        routes: list[dict[str, str]],
    ):
        """Resolves the handler for the given path and method.

        Args:
            path: Request path.
            method: HTTP method.
            routes: List of route definitions.

        Returns:
            Handler callable.

        Raises:
            ValueError: If no controller is associated with the route.
            ValueError: If no handler is found for the controller.
        """
        for route in routes:
            if route.get("endpoint") != path:
                continue

            controller_path = route.get("controller")
            if not controller_path:
                endpoint = route.get("endpoint")
                raise ValueError(f"No controller associated with route: {endpoint}")

            controller_class = self._get_controller_class(controller_path)

            if controller_class and hasattr(controller_class, method):
                self._current_route = route
                return getattr(controller_class(), method)

            raise ValueError(f"No handler found for controller_path: {controller_path}")

        return None

    @property
    def current_route(self) -> dict[str, str]:
        """Returns the current matched route.

        Raises:
            ValueError: If no route has been matched.
        """
        if self._current_route is None:
            raise ValueError("No route has been matched")
        return self._current_route

    def _get_controller_class(self, controller_path: str):
        """Gets the controller class from the module path.

        Args:
            controller_path: Dot-separated path to the controller module.

        Returns:
            Controller class.
        """
        module = importlib.import_module(controller_path)

        parts = controller_path.split(".")[-1].split("_")
        class_name = "".join(part.capitalize() for part in parts)
        return getattr(module, class_name, None)
