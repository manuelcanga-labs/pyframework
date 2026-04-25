import unittest
from pyframework.http_foundation.server import Server


class TestServer(unittest.TestCase):
    """Unit tests for the Server class."""

    def test_server_init_default_values(self):
        """Test Server initialization with default values."""
        server = Server()
        self.assertEqual(server.host, "127.0.0.1")
        self.assertEqual(server.port, 8000)

    def test_server_init_custom_values(self):
        """Test Server initialization with custom host and port."""
        server = Server(host="0.0.0.0", port=9000)
        self.assertEqual(server.host, "0.0.0.0")
        self.assertEqual(server.port, 9000)
