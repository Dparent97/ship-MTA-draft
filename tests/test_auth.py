"""Tests for authentication routes."""
import pytest
from flask import session


class TestIndexRoute:
    """Test the index/landing page route."""

    def test_index_redirects_to_crew_login_when_not_authenticated(self, client):
        """Test that index redirects to crew login for unauthenticated users."""
        response = client.get('/', follow_redirects=False)
        assert response.status_code == 302
        assert '/crew-login' in response.location

    def test_index_redirects_to_admin_dashboard_when_admin(self, authenticated_admin_client):
        """Test that index redirects to admin dashboard for authenticated admins."""
        response = authenticated_admin_client.get('/', follow_redirects=False)
        assert response.status_code == 302
        assert '/admin/dashboard' in response.location

    def test_index_redirects_to_crew_submit_when_crew_authenticated(self, authenticated_crew_client):
        """Test that index redirects to crew submit form for authenticated crew."""
        response = authenticated_crew_client.get('/', follow_redirects=False)
        assert response.status_code == 302
        assert '/crew/submit' in response.location


class TestCrewLogin:
    """Test crew login functionality."""

    def test_crew_login_page_loads(self, client):
        """Test that crew login page loads successfully."""
        response = client.get('/crew-login')
        assert response.status_code == 200
        assert b'password' in response.data.lower()

    def test_crew_login_success(self, client, app):
        """Test successful crew login."""
        response = client.post('/crew-login', data={
            'password': app.config['CREW_PASSWORD'],
            'crew_name': 'DP'
        }, follow_redirects=False)

        assert response.status_code == 302
        assert '/crew/submit' in response.location

        # Verify session was set
        with client.session_transaction() as sess:
            assert sess['crew_authenticated'] is True
            assert sess['crew_name'] == 'DP'

    def test_crew_login_invalid_password(self, client):
        """Test crew login with invalid password."""
        response = client.post('/crew-login', data={
            'password': 'wrong_password',
            'crew_name': 'DP'
        }, follow_redirects=True)

        assert response.status_code == 200
        assert b'Invalid password' in response.data

        # Verify session was not set
        with client.session_transaction() as sess:
            assert 'crew_authenticated' not in sess

    def test_crew_login_missing_crew_name(self, client, app):
        """Test crew login with missing crew name."""
        response = client.post('/crew-login', data={
            'password': app.config['CREW_PASSWORD'],
            'crew_name': ''
        }, follow_redirects=True)

        assert response.status_code == 200
        assert b'Invalid password' in response.data or b'crew name not selected' in response.data

    def test_crew_login_shows_crew_members(self, client, app):
        """Test that crew login page shows available crew members."""
        response = client.get('/crew-login')
        assert response.status_code == 200

        # Check that crew members from config are displayed
        for member in app.config['CREW_MEMBERS']:
            assert member.encode() in response.data

    def test_crew_login_session_is_permanent(self, client, app):
        """Test that crew login creates a permanent session."""
        response = client.post('/crew-login', data={
            'password': app.config['CREW_PASSWORD'],
            'crew_name': 'DP'
        }, follow_redirects=False)

        with client.session_transaction() as sess:
            assert sess.permanent is True


class TestAdminLogin:
    """Test admin login functionality."""

    def test_admin_login_page_loads(self, client):
        """Test that admin login page loads successfully."""
        response = client.get('/admin-login')
        assert response.status_code == 200
        assert b'username' in response.data.lower()
        assert b'password' in response.data.lower()

    def test_admin_login_success(self, client, app):
        """Test successful admin login."""
        response = client.post('/admin-login', data={
            'username': app.config['ADMIN_USERNAME'],
            'password': app.config['ADMIN_PASSWORD']
        }, follow_redirects=False)

        assert response.status_code == 302
        assert '/admin/dashboard' in response.location

        # Verify session was set
        with client.session_transaction() as sess:
            assert sess['is_admin'] is True

    def test_admin_login_invalid_username(self, client, app):
        """Test admin login with invalid username."""
        response = client.post('/admin-login', data={
            'username': 'wrong_user',
            'password': app.config['ADMIN_PASSWORD']
        }, follow_redirects=True)

        assert response.status_code == 200
        assert b'Invalid admin credentials' in response.data

    def test_admin_login_invalid_password(self, client, app):
        """Test admin login with invalid password."""
        response = client.post('/admin-login', data={
            'username': app.config['ADMIN_USERNAME'],
            'password': 'wrong_password'
        }, follow_redirects=True)

        assert response.status_code == 200
        assert b'Invalid admin credentials' in response.data

    def test_admin_login_session_is_permanent(self, client, app):
        """Test that admin login creates a permanent session."""
        response = client.post('/admin-login', data={
            'username': app.config['ADMIN_USERNAME'],
            'password': app.config['ADMIN_PASSWORD']
        }, follow_redirects=False)

        with client.session_transaction() as sess:
            assert sess.permanent is True


class TestLogout:
    """Test logout functionality."""

    def test_crew_logout(self, authenticated_crew_client):
        """Test crew member logout."""
        # Verify crew is authenticated
        with authenticated_crew_client.session_transaction() as sess:
            assert sess.get('crew_authenticated') is True

        # Logout
        response = authenticated_crew_client.get('/logout', follow_redirects=False)

        assert response.status_code == 302
        assert '/crew-login' in response.location

        # Verify session was cleared
        with authenticated_crew_client.session_transaction() as sess:
            assert 'crew_authenticated' not in sess
            assert 'crew_name' not in sess

    def test_admin_logout(self, authenticated_admin_client):
        """Test admin logout."""
        # Verify admin is authenticated
        with authenticated_admin_client.session_transaction() as sess:
            assert sess.get('is_admin') is True

        # Logout
        response = authenticated_admin_client.get('/logout', follow_redirects=False)

        assert response.status_code == 302
        assert '/admin-login' in response.location

        # Verify session was cleared
        with authenticated_admin_client.session_transaction() as sess:
            assert 'is_admin' not in sess

    def test_logout_clears_all_session_data(self, client):
        """Test that logout clears all session data."""
        # Set up session with multiple keys
        with client.session_transaction() as sess:
            sess['crew_authenticated'] = True
            sess['crew_name'] = 'DP'
            sess['is_admin'] = False
            sess['other_data'] = 'test'

        # Logout
        client.get('/logout')

        # Verify all session data is cleared
        with client.session_transaction() as sess:
            assert len(sess) == 0

    def test_logout_when_not_authenticated(self, client):
        """Test logout when user is not authenticated."""
        response = client.get('/logout', follow_redirects=False)
        assert response.status_code == 302
        # Should redirect to crew login by default
        assert '/crew-login' in response.location
