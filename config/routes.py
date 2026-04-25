"""Routes configuration module."""

routes = [
    {"endpoint": "/", "controller": "modules.pages.controllers.home"},
    {"endpoint": "/about", "controller": "modules.pages.controllers.about.about"},
]
