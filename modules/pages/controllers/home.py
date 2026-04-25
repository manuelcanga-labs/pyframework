"""Home controller."""

from pyframework.http_foundation.responses import Response


class Home:
    """Home page controller."""

    def get(self, request):
        """Handle GET requests."""
        return Response("<h1>Hola mundo</h1>")
