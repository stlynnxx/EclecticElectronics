"""Tests for the static Flask routes that only render a template.

Each route is exercised with Flask's test client and must return HTTP 200
when its template is available. No live server is started and no
production files are written.

Run from the repository root:

    pip install -r requirements.txt pytest
    python -m pytest tests/test_static_routes.py
"""

import os
import sys

import pytest

# Make the repository root importable so `import app` works from tests/.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app as flask_app  # noqa: E402

# Simple GET routes whose handlers only render a template.
STATIC_ROUTES = [
    "/",
    "/about",
    "/contact",
    "/positive",
    "/magicpython",
    "/software",
    "/quote",
    "/gallery",
    "/review",
    "/security",
    "/password",
    "/eclecticAI",
    "/trivia",
]


@pytest.fixture()
def client():
    flask_app.config.update(TESTING=True)
    return flask_app.test_client()


@pytest.mark.parametrize("route", STATIC_ROUTES)
def test_static_route_returns_200(client, route):
    response = client.get(route)
    assert response.status_code == 200
