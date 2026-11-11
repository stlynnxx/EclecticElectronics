"""Shared fixtures for the EclecticElectronics test suite.

Run the tests from the repository root:

    pip install -r requirements.txt pytest
    python -m pytest

The tests use Flask's test client only: no live server is started and no
production data files are written.
"""

import os
import sys

import pytest

# Make the repository root importable so `import app` works from tests/.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app as flask_app  # noqa: E402


@pytest.fixture()
def app():
    flask_app.config.update(TESTING=True)
    return flask_app


@pytest.fixture()
def client(app):
    return app.test_client()
