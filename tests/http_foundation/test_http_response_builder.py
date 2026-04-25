import unittest
from unittest.mock import MagicMock
from pyframework.http_foundation.http_response_builder import HttpResponseBuilder
from pyframework.http_foundation.responses import Response


class TestHttpResponseBuilder(unittest.TestCase):
    """Unit tests for the HttpResponseBuilder class."""

    def test_build_returns_response_body(self):
        """Test that build returns the response body as bytes."""
        builder = HttpResponseBuilder()
        response = Response("Hello World")
        start_response = MagicMock()

        result = builder.build(response, start_response)

        self.assertEqual(result, [b"Hello World"])

    def test_build_calls_start_response_with_status(self):
        """Test that build calls start_response with correct status."""
        builder = HttpResponseBuilder()
        response = Response("Hello", 200)
        start_response = MagicMock()

        builder.build(response, start_response)

        start_response.assert_called_once()
        call_args = start_response.call_args[0]
        self.assertIn("200 OK", call_args[0])

    def test_build_calls_start_response_with_headers(self):
        """Test that build calls start_response with headers."""
        builder = HttpResponseBuilder()
        response = Response("Hello")
        start_response = MagicMock()

        builder.build(response, start_response)

        start_response.assert_called_once()
        call_args = start_response.call_args[0]
        self.assertIn("Content-Type", call_args[1][0][0])

    def test_build_with_bytes_body(self):
        """Test that build works with bytes body."""
        builder = HttpResponseBuilder()
        response = Response(b"Hello Bytes")
        start_response = MagicMock()

        result = builder.build(response, start_response)

        self.assertEqual(result, [b"Hello Bytes"])

    def test_build_with_404_status(self):
        """Test that build works with 404 status."""
        builder = HttpResponseBuilder()
        response = Response("Not Found", 404)
        start_response = MagicMock()

        builder.build(response, start_response)

        call_args = start_response.call_args[0]
        self.assertIn("404", call_args[0])
