import unittest
from pyframework.http_foundation.requests import Request


class TestRequest(unittest.TestCase):
    """Unit tests for the Request class."""

    def test_path_returns_path_info(self):
        """Test that path returns PATH_INFO from environ."""
        request = Request({"PATH_INFO": "/users/123", "REQUEST_METHOD": "GET"})
        self.assertEqual(request.path, "/users/123")

    def test_path_returns_default_when_missing(self):
        """Test that path returns default when PATH_INFO is missing."""
        request = Request({"REQUEST_METHOD": "GET"})
        self.assertEqual(request.path, "/")

    def test_method_returns_request_method(self):
        """Test that method returns REQUEST_METHOD from environ."""
        request = Request({"REQUEST_METHOD": "POST"})
        self.assertEqual(request.method, "POST")

    def test_method_returns_default_when_missing(self):
        """Test that method returns default when REQUEST_METHOD is missing."""
        request = Request({})
        self.assertEqual(request.method, "GET")

    def test_query_returns_parsed_params(self):
        """Test that query returns parsed query string parameters."""
        request = Request({"QUERY_STRING": "name=john&age=30"})
        self.assertEqual(request.query, {"name": ["john"], "age": ["30"]})

    def test_query_returns_empty_when_no_params(self):
        """Test that query returns empty dict when no query string."""
        request = Request({})
        self.assertEqual(request.query, {})

    def test_form_returns_parsed_data(self):
        """Test that form returns parsed form data."""
        environ = {
            "CONTENT_TYPE": "application/x-www-form-urlencoded",
            "wsgi.input": __import__("io").BytesIO(b"name=john&age=30"),
        }
        request = Request(environ)
        self.assertEqual(request.form, {"name": ["john"], "age": ["30"]})

    def test_form_returns_empty_when_wrong_content_type(self):
        """Test that form returns empty dict when content type is not form."""
        request = Request({"CONTENT_TYPE": "application/json"})
        self.assertEqual(request.form, {})