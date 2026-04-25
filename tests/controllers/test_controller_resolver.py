import unittest
from unittest.mock import patch, MagicMock
from pyframework.controllers.controller_resolver import ControllerResolver


class TestControllerResolver(unittest.TestCase):
    """Unit tests for the ControllerResolver class."""

    def test_resolve_handler_returns_handler(self):
        """Test that resolve_handler returns the handler when found."""
        resolver = ControllerResolver()
        routes = [{"endpoint": "/", "controller": "test.controller"}]
        
        mock_class = MagicMock()
        mock_instance = MagicMock()
        mock_class.return_value = mock_instance
        
        with patch("importlib.import_module", return_value=mock_class):
            handler = resolver.resolve_handler("/", "get", routes)
            self.assertIsNotNone(handler)

    def test_resolve_handler_returns_none_when_not_found(self):
        """Test that resolve_handler returns None when route not found."""
        resolver = ControllerResolver()
        routes = [{"endpoint": "/home", "controller": "test.controller"}]
        
        handler = resolver.resolve_handler("/notfound", "get", routes)
        self.assertIsNone(handler)

    def test_resolve_handler_raises_when_no_controller(self):
        """Test that resolve_handler raises ValueError when no controller."""
        resolver = ControllerResolver()
        routes = [{"endpoint": "/", "controller": None}]
        
        with self.assertRaises(ValueError) as context:
            resolver.resolve_handler("/", "get", routes)
        self.assertIn("No controller associated with route", str(context.exception))

    def test_resolve_handler_raises_when_handler_not_found(self):
        """Test that resolve_handler raises ValueError when handler not found."""
        resolver = ControllerResolver()
        routes = [{"endpoint": "/", "controller": "test.controller"}]
        
        mock_class = type("MockClass", (), {})()
        
        with patch("importlib.import_module", return_value=mock_class):
            with self.assertRaises(ValueError) as context:
                resolver.resolve_handler("/", "get", routes)
        self.assertIn("No handler found", str(context.exception))