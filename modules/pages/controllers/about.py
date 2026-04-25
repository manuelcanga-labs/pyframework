"""About controller."""

from pyframework.http_foundation.responses import ResponseJson


class About:
    """About page controller."""

    def get(self, _request):
        """Handle GET requests."""
        data = {
            "name": "PyFramework",
            "description": "A lightweight Python web framework inspired by Symfony and Flask",
            "version": "0.1.0",
            "repository": "https://github.com/manuelcanga-labs/pyframework",
            "author": "Manuel Canga",
            "license": "MIT",
        }
        return ResponseJson(data)
