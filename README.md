# PyFramework

> **Note:** I built this lightweight Python web framework in a morning session as a learning exercise.

A lightweight Python web framework inspired by Symfony and Flask, built for learning purposes.

## Requirements

- Python 3.12+

## Installation

No external dependencies required (uses Python's built-in `wsgiref`).

## Usage

```python
from pyframework import PyFramework

app = PyFramework(__file__)
app.load()
```

Then open http://localhost:8080 in your browser.

## Structure

```
pyframework/
├── pyframework/
│   ├── __init__.py
│   └── pyframework.py          # Core framework class
├── controllers/
│   └── controller_resolver.py # Resolves controllers from routes
└── http_foundation/
    ├── server.py              # WSGI server wrapper
    ├── status.py              # HTTP status constants
    ├── requests/
    │   └── request.py         # Request class (path, method, query)
    └── responses/
        ├── base_response.py
        ├── response.py        # Text response
        └── response_json.py   # JSON response
config/
├── routes.py                  # Application routes
modules/
└── pages/controllers/        # Application controllers
    ├── home/
    └── about/
tests/
├── http_foundation/
│   ├── test_request.py
│   └── test_server.py
├── controllers/
│   └── test_controller_resolver.py
└── test_pyframework.py
```

## Request

The `Request` class provides:

- `request.path` - Request path (PATH_INFO)
- `request.method` - HTTP method (GET, POST, etc.)
- `request.query` - Query string parameters

## Responses

- `Response(body, status)` - Text response
- `ResponseJson(data)` - JSON response

## Routes

Routes are defined in `config/routes.py`:

```python
routes = [
    {"endpoint": "/", "controller": "modules.pages.controllers.home"},
    {"endpoint": "/about", "controller": "modules.pages.controllers.about.about"},
]
```

## Author

- **Manuel Canga** - [GitHub](https://github.com/manuelcanga-labs/pyframework)

## License

MIT