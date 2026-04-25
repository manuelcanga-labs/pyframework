import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
from pyframework.pyframework import PyFramework


class TestPyFramework(unittest.TestCase):
    """Unit tests for the PyFramework class."""

    def test_init_default_config_dir(self):
        """Test PyFramework initialization with default config directory."""
        app = PyFramework()
        self.assertEqual(app.config_dir, Path("config"))

    def test_init_custom_config_dir(self):
        """Test PyFramework initialization with custom config directory."""
        with patch.object(PyFramework, "find_routes", return_value=[]):
            with patch.object(Path, "exists", return_value=True):
                app = PyFramework(config_dir="/custom/config")
                self.assertEqual(app.config_dir, Path("/custom/config"))

    def test_init_routes_loaded_from_config(self):
        """Test that routes are loaded from config file."""
        app = PyFramework()
        self.assertIsInstance(app.routes, list)
        self.assertGreater(len(app.routes), 0)

    def test_find_routes_no_routes_file_raises_error(self):
        """Test that find_routes raises error when routes.py is missing."""
        from pathlib import Path

        def mock_exists(self):
            return False

        with patch.object(Path, "exists", mock_exists):
            app = PyFramework.__new__(PyFramework)
            app._routes = []
            with self.assertRaises(FileNotFoundError):
                app.set_config_dir("fake")

    def test_routes_property_returns_routes(self):
        """Test that routes property returns _routes."""
        app = PyFramework()
        app._routes = [{"endpoint": "/test", "controller": "test"}]
        self.assertEqual(app.routes, [{"endpoint": "/test", "controller": "test"}])

    def test_load_controller_returns_handler_result(self):
        """Test that load_controller returns handler result."""
        from pyframework.http_foundation.responses import Response
        app = PyFramework()
        app._routes = [{"endpoint": "/", "controller": "test.controller"}]
        start_response = MagicMock()
        
        mock_response = Response("result")
        
        with patch.object(app._resolver, "resolve_handler", return_value=lambda e: mock_response):
            result = app.load_controller({"PATH_INFO": "/"}, start_response)
            self.assertEqual(result, [b"result"])

    def test_load_controller_sets_response_headers(self):
        """Test that load_controller sets correct response headers."""
        from pyframework.http_foundation.responses import Response
        app = PyFramework()
        app._routes = [{"endpoint": "/", "controller": "test.controller"}]
        start_response = MagicMock()
        
        mock_response = Response("response")
        
        with patch.object(app._resolver, "resolve_handler", return_value=lambda e: mock_response):
            result = app.load_controller({"PATH_INFO": "/"}, start_response)
            start_response.assert_called_once_with(
                "200 OK", [("Content-Type", "text/html")]
            )
            self.assertEqual(result, [b"response"])

    @patch("pyframework.pyframework.Server")
    def test_load_creates_and_starts_server(self, mock_server):
        """Test that load creates a Server and calls up."""
        mock_server_instance = MagicMock()
        mock_server.return_value = mock_server_instance

        app = PyFramework()
        app.load()

        mock_server.assert_called_once()
        mock_server_instance.up.assert_called_once_with(app.load_controller)