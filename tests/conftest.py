"""
Pytest configuration and fixtures for testing the Ship MTA application.
"""
import os
import tempfile
import pytest
from app import create_app
from app.models import db as _db


@pytest.fixture(scope="session")
def app():
    """Create and configure a new app instance for each test session."""
    # Create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()

    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{db_path}",
        "SECRET_KEY": "test-secret-key",
        "WTF_CSRF_ENABLED": False,
    })

    # Create the database and load test data
    with app.app_context():
        _db.create_all()

    yield app

    # Cleanup
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture(scope="function")
def client(app):
    """Create a test client for the app."""
    return app.test_client()


@pytest.fixture(scope="function")
def runner(app):
    """Create a test runner for the app's Click commands."""
    return app.test_cli_runner()


@pytest.fixture(scope="function")
def db(app):
    """Create a fresh database for each test."""
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.remove()
        _db.drop_all()


@pytest.fixture(scope="function")
def session(db):
    """Create a database session for testing."""
    connection = db.engine.connect()
    transaction = connection.begin()

    session = db.create_scoped_session(
        options={"bind": connection, "binds": {}}
    )
    db.session = session

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def auth_client(client, db):
    """Create an authenticated test client."""
    # Add authentication logic here if needed
    return client
