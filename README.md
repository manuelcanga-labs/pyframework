# PyFramework

A lightweight web framework built with Python for learning purposes.

## Installation

No external dependencies required (uses Python's built-in `wsgiref`).

## Usage

```python
from pyframework import PyFramework

app = PyFramework()
app.bootstrap()
app.load()
```

Then open http://localhost:8000 in your browser.

## Structure

```
pyframework/
├── pyframework/       # Core framework
│   ├── server.py
│   └── pyframework.py
├── config/           # Application configuration
│   └── routes.py
└── app.py           # Application entry point
```

## Requirements

- Python 3.12+