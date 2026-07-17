"""Pytest configuration and shared fixtures."""

import pytest

from app import create_app


@pytest.fixture
def app():
    """Create application instance configured for testing."""
    application = create_app("testing")
    yield application


@pytest.fixture
def client(app):
    """Flask test client."""
    return app.test_client()
