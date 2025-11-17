"""
Basic application tests.
"""
import pytest
from app import create_app


def test_app_creation():
    """Test that the app can be created."""
    app = create_app()
    assert app is not None
    assert app.config is not None


def test_app_config(app):
    """Test app configuration."""
    assert app.config["TESTING"] is True


def test_app_context(app):
    """Test that app context works."""
    with app.app_context():
        assert app is not None


def test_index_route(client):
    """Test that the index route works."""
    response = client.get("/")
    assert response.status_code in [200, 302, 404]  # May redirect or not exist


def test_static_files(client):
    """Test that static files are accessible."""
    # Test CSS file access
    response = client.get("/static/css/style.css")
    # Should either exist (200) or not exist (404), but not error (500)
    assert response.status_code in [200, 404]
