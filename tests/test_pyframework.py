import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
from pyframework.pyframework import PyFramework


class TestPyFramework(unittest.TestCase):
    """Unit tests for the PyFramework class."""

    def test_init_default_config_dir(self):
        """Test PyFramework initialization with default config directory."""
        with patch.object(PyFramework, "bootstrap", return_value=None):
            app = PyFramework()
            self.assertEqual(app.config_dir, Path("config"))

    def test_init_custom_config_dir(self):
        """Test PyFramework initialization with custom config directory."""
        with patch.object(PyFramework, "bootstrap", return_value=None):
            app = PyFramework(config_dir="/custom/config")
            self.assertEqual(app.config_dir, Path("/custom/config"))

    def test_init_routes_loaded_from_config(self):
        """Test that routes are loaded from config file."""
        app = PyFramework()
        self.assertIsInstance(app.routes, list)
        self.assertGreater(len(app.routes), 0)

    def test_bootstrap_no_routes_file_raises_error(self):
        """Test that bootstrap raises error when routes.py is missing."""
        from pathlib import Path
        original_exists = Path.exists

        def mock_exists(self):
            return False

        with patch.object(Path, "exists", mock_exists):
            app = PyFramework.__new__(PyFramework)
            app.config_dir = Path("fake")
            app._routes = []
            with self.assertRaises(FileNotFoundError):
                app.bootstrap()

    def test_init_routes_loaded_from_config(self):
        """Test that routes are loaded from config file."""
        app = PyFramework()
        self.assertIsInstance(app.routes, list)
        self.assertGreater(len(app.routes), 0)

    def test_routes_property_returns_routes(self):
        """Test that routes property returns _routes."""
        app = PyFramework()
        app._routes = [{"endpoint": "/test", "controller": "test"}]
        self.assertEqual(app.routes, [{"endpoint": "/test", "controller": "test"}])

    def test_load_controller_returns_handler_result(self):
        """Test that load_controller returns handler result."""
        from pyframework.responses import Response
        app = PyFramework()
        app._routes = [{"endpoint": "/", "controller": "test.controller"}]
        start_response = MagicMock()
        
        mock_response = Response("result")
        
        with patch.object(app, "_extract_controller", return_value=lambda e: mock_response):
            result = app.load_controller({"PATH_INFO": "/"}, start_response)
            self.assertEqual(result, [b"result"])

    def test_load_controller_sets_response_headers(self):
        """Test that load_controller sets correct response headers."""
        from pyframework.responses import Response
        app = PyFramework()
        app._routes = [{"endpoint": "/", "controller": "test.controller"}]
        start_response = MagicMock()
        
        mock_response = Response("response")
        
        def mock_get(controller_path, method):
            return lambda e: mock_response
        
        with patch.object(app, "_extract_controller", side_effect=mock_get):
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