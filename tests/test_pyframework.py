"""PyFramework tests module."""

import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
from pyframework.pyframework import PyFramework


class TestPyFramework(unittest.TestCase):
    """Unit tests for the PyFramework class."""

    def test_init_default_config_dir_is_based_on_main_script(self):
        """Test PyFramework uses main_script parent for config by default."""
        with patch.object(Path, "exists", return_value=True):
            with patch.object(PyFramework, "find_routes", return_value=[]):
                app = PyFramework(__file__)
                self.assertEqual(app.config_dir, Path(__file__).parent / "config")

    def test_init_custom_config_dir(self):
        """Test PyFramework initialization with custom config directory."""
        with patch.object(Path, "exists", return_value=True):
            with patch.object(PyFramework, "find_routes", return_value=[]):
                app = PyFramework(__file__, config_dir="/custom/config")
                self.assertEqual(app.config_dir, Path("/custom/config"))

    def test_init_routes_loaded_from_config(self):
        """Test that routes are loaded from config file."""
        with patch.object(Path, "exists", return_value=True):
            with patch.object(PyFramework, "find_routes", return_value=[]):
                app = PyFramework(__file__)
                self.assertIsInstance(app.routes, list)
                self.assertEqual(app.routes, [])

    def test_find_routes_no_routes_file_raises_error(self):
        """Test that find_routes raises error when routes.py is missing."""
        with patch.object(Path, "exists", return_value=False):
            with self.assertRaises(FileNotFoundError):
                PyFramework(__file__)

    def test_routes_property_returns_routes(self):
        """Test that routes property returns _routes."""
        with patch.object(Path, "exists", return_value=True):
            with patch.object(PyFramework, "find_routes", return_value=[]):
                app = PyFramework(__file__)
                app._routes = [{"endpoint": "/test", "controller": "test"}]
                self.assertEqual(
                    app.routes, [{"endpoint": "/test", "controller": "test"}]
                )

    def test_handle_server_request_returns_handler_result(self):
        """Test that handle_server_request returns handler result."""
        from pyframework.http_foundation.responses import Response

        with patch.object(Path, "exists", return_value=True):
            with patch.object(PyFramework, "find_routes", return_value=[]):
                app = PyFramework(__file__)
                app._routes = [{"endpoint": "/", "controller": "test.controller"}]

                mock_response = Response("result")
                start_response = MagicMock()

                with patch.object(
                    app._resolver,
                    "resolve_handler",
                    return_value=lambda r: mock_response,
                ):
                    result = app.handle_server_request(
                        {"PATH_INFO": "/", "REQUEST_METHOD": "GET"}, start_response
                    )
                    self.assertEqual(result, [b"result"])

    def test_handle_server_request_sets_response_headers(self):
        """Test that handle_server_request sets correct response headers."""
        from pyframework.http_foundation.responses import Response

        with patch.object(Path, "exists", return_value=True):
            with patch.object(PyFramework, "find_routes", return_value=[]):
                app = PyFramework(__file__)
                app._routes = [{"endpoint": "/", "controller": "test.controller"}]

                mock_response = Response("response")
                start_response = MagicMock()

                with patch.object(
                    app._resolver,
                    "resolve_handler",
                    return_value=lambda r: mock_response,
                ):
                    result = app.handle_server_request(
                        {"PATH_INFO": "/", "REQUEST_METHOD": "GET"}, start_response
                    )
                    start_response.assert_called_once_with(
                        "200 OK", [("Content-Type", "text/html")]
                    )
                    self.assertEqual(result, [b"response"])

    @patch("pyframework.pyframework.Server")
    def test_load_creates_and_starts_server(self, mock_server):
        """Test that load creates a Server and calls up."""
        mock_server_instance = MagicMock()
        mock_server.return_value = mock_server_instance

        with patch.object(Path, "exists", return_value=True):
            with patch.object(PyFramework, "find_routes", return_value=[]):
                app = PyFramework(__file__)
                app.load()

                mock_server.assert_called_once()
                mock_server_instance.up.assert_called_once_with(
                    app.handle_server_request
                )
