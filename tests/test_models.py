"""
Tests for database models.
"""
import pytest
from app.models import db, MaintenanceRequest


def test_database_connection(app, db):
    """Test that database connection works."""
    with app.app_context():
        assert db is not None
        assert db.engine is not None


def test_create_maintenance_request(app, db):
    """Test creating a maintenance request."""
    with app.app_context():
        request = MaintenanceRequest(
            ship_name="Test Ship",
            department="Engineering",
            problem_description="Test problem",
            submitted_by="Test User",
            submitted_by_phone="1234567890"
        )
        db.session.add(request)
        db.session.commit()

        assert request.id is not None
        assert request.ship_name == "Test Ship"
        assert request.status == "pending"


def test_maintenance_request_string_representation(app, db):
    """Test MaintenanceRequest __repr__ method."""
    with app.app_context():
        request = MaintenanceRequest(
            ship_name="Test Ship",
            department="Engineering",
            problem_description="Test problem",
            submitted_by="Test User",
            submitted_by_phone="1234567890"
        )
        assert "MaintenanceRequest" in repr(request) or "Test Ship" in str(request)


def test_query_maintenance_requests(app, db):
    """Test querying maintenance requests."""
    with app.app_context():
        # Create multiple requests
        for i in range(3):
            request = MaintenanceRequest(
                ship_name=f"Ship {i}",
                department="Engineering",
                problem_description=f"Problem {i}",
                submitted_by="Test User",
                submitted_by_phone="1234567890"
            )
            db.session.add(request)
        db.session.commit()

        # Query all requests
        requests = MaintenanceRequest.query.all()
        assert len(requests) >= 3
