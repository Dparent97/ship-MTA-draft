"""Tests for SMS notification system."""
import pytest
from unittest.mock import Mock, patch, MagicMock
from app.notifications import get_twilio_client, send_sms, send_assignment_notification
from twilio.base.exceptions import TwilioRestException


class TestGetTwilioClient:
    """Test get_twilio_client function."""

    def test_returns_client_with_valid_credentials(self, app):
        """Test that client is returned with valid credentials."""
        with app.app_context():
            app.config['TWILIO_ACCOUNT_SID'] = 'test_sid'
            app.config['TWILIO_AUTH_TOKEN'] = 'test_token'

            with patch('app.notifications.Client') as mock_client:
                client = get_twilio_client()
                mock_client.assert_called_once_with('test_sid', 'test_token')

    def test_returns_none_without_account_sid(self, app):
        """Test that None is returned when account SID is missing."""
        with app.app_context():
            app.config['TWILIO_ACCOUNT_SID'] = None
            app.config['TWILIO_AUTH_TOKEN'] = 'test_token'

            client = get_twilio_client()
            assert client is None

    def test_returns_none_without_auth_token(self, app):
        """Test that None is returned when auth token is missing."""
        with app.app_context():
            app.config['TWILIO_ACCOUNT_SID'] = 'test_sid'
            app.config['TWILIO_AUTH_TOKEN'] = None

            client = get_twilio_client()
            assert client is None


class TestSendSMS:
    """Test send_sms function."""

    def test_send_sms_success(self, app):
        """Test successful SMS sending."""
        with app.app_context():
            app.config['TWILIO_ACCOUNT_SID'] = 'test_sid'
            app.config['TWILIO_AUTH_TOKEN'] = 'test_token'
            app.config['TWILIO_FROM_NUMBER'] = '+1234567890'

            mock_message = Mock()
            mock_message.sid = 'test_message_sid'

            mock_client = Mock()
            mock_client.messages.create.return_value = mock_message

            with patch('app.notifications.get_twilio_client', return_value=mock_client):
                result = send_sms('+1987654321', 'Test message')

                assert result is True
                mock_client.messages.create.assert_called_once_with(
                    body='Test message',
                    from_='+1234567890',
                    to='+1987654321'
                )

    def test_send_sms_no_phone_number(self, app):
        """Test sending SMS without phone number."""
        with app.app_context():
            result = send_sms(None, 'Test message')
            assert result is False

            result = send_sms('', 'Test message')
            assert result is False

    def test_send_sms_no_from_number(self, app):
        """Test sending SMS without configured from number."""
        with app.app_context():
            app.config['TWILIO_FROM_NUMBER'] = None

            result = send_sms('+1987654321', 'Test message')
            assert result is False

    def test_send_sms_no_client(self, app):
        """Test sending SMS when client cannot be created."""
        with app.app_context():
            app.config['TWILIO_FROM_NUMBER'] = '+1234567890'

            with patch('app.notifications.get_twilio_client', return_value=None):
                result = send_sms('+1987654321', 'Test message')
                assert result is False

    def test_send_sms_twilio_exception(self, app):
        """Test handling of Twilio exceptions."""
        with app.app_context():
            app.config['TWILIO_ACCOUNT_SID'] = 'test_sid'
            app.config['TWILIO_AUTH_TOKEN'] = 'test_token'
            app.config['TWILIO_FROM_NUMBER'] = '+1234567890'

            mock_client = Mock()
            mock_client.messages.create.side_effect = TwilioRestException(
                status=400,
                uri='/test',
                msg='Invalid phone number',
                code=21211
            )

            with patch('app.notifications.get_twilio_client', return_value=mock_client):
                result = send_sms('+1987654321', 'Test message')
                assert result is False

    def test_send_sms_general_exception(self, app):
        """Test handling of general exceptions."""
        with app.app_context():
            app.config['TWILIO_ACCOUNT_SID'] = 'test_sid'
            app.config['TWILIO_AUTH_TOKEN'] = 'test_token'
            app.config['TWILIO_FROM_NUMBER'] = '+1234567890'

            mock_client = Mock()
            mock_client.messages.create.side_effect = Exception('Network error')

            with patch('app.notifications.get_twilio_client', return_value=mock_client):
                result = send_sms('+1987654321', 'Test message')
                assert result is False


class TestSendAssignmentNotification:
    """Test send_assignment_notification function."""

    def test_send_assignment_notification_success(self, app, sample_work_item):
        """Test successful assignment notification."""
        with app.app_context():
            app.config['ENABLE_NOTIFICATIONS'] = True
            app.config['CREW_PHONES'] = {'DP': '+1234567890'}
            app.config['CREW_LOGIN_URL'] = 'http://test.com/crew/login'

            with patch('app.notifications.send_sms', return_value=True) as mock_send:
                result = send_assignment_notification(sample_work_item, 'DP', 'Test notes')

                assert result is True
                mock_send.assert_called_once()

                call_args = mock_send.call_args
                assert call_args[0][0] == '+1234567890'

                message = call_args[0][1]
                assert 'TEST_001' in message
                assert 'DP' in message or 'Test notes' in message

    def test_send_assignment_notification_disabled(self, app, sample_work_item):
        """Test notification when notifications are disabled."""
        with app.app_context():
            app.config['ENABLE_NOTIFICATIONS'] = False

            result = send_assignment_notification(sample_work_item, 'DP')
            assert result is False

    def test_send_assignment_notification_no_phone(self, app, sample_work_item):
        """Test notification when crew member has no phone number."""
        with app.app_context():
            app.config['ENABLE_NOTIFICATIONS'] = True
            app.config['CREW_PHONES'] = {}

            result = send_assignment_notification(sample_work_item, 'DP')
            assert result is False

    def test_send_assignment_notification_with_revision_notes(self, app, sample_work_item):
        """Test notification includes revision notes when provided."""
        with app.app_context():
            app.config['ENABLE_NOTIFICATIONS'] = True
            app.config['CREW_PHONES'] = {'DP': '+1234567890'}

            with patch('app.notifications.send_sms', return_value=True) as mock_send:
                result = send_assignment_notification(
                    sample_work_item,
                    'DP',
                    'Please add more photos'
                )

                assert result is True
                call_args = mock_send.call_args
                message = call_args[0][1]
                assert 'Please add more photos' in message

    def test_send_assignment_notification_without_revision_notes(self, app, sample_work_item):
        """Test notification without revision notes."""
        with app.app_context():
            app.config['ENABLE_NOTIFICATIONS'] = True
            app.config['CREW_PHONES'] = {'AL': '+1987654321'}

            with patch('app.notifications.send_sms', return_value=True) as mock_send:
                result = send_assignment_notification(sample_work_item, 'AL', None)

                assert result is True
                call_args = mock_send.call_args
                message = call_args[0][1]
                assert 'TEST_001' in message

    def test_send_assignment_notification_includes_login_url(self, app, sample_work_item):
        """Test that notification includes crew login URL."""
        with app.app_context():
            app.config['ENABLE_NOTIFICATIONS'] = True
            app.config['CREW_PHONES'] = {'DP': '+1234567890'}
            app.config['CREW_LOGIN_URL'] = 'https://example.com/login'

            with patch('app.notifications.send_sms', return_value=True) as mock_send:
                result = send_assignment_notification(sample_work_item, 'DP')

                call_args = mock_send.call_args
                message = call_args[0][1]
                assert 'https://example.com/login' in message

    def test_send_assignment_notification_sms_failure(self, app, sample_work_item):
        """Test handling of SMS sending failure."""
        with app.app_context():
            app.config['ENABLE_NOTIFICATIONS'] = True
            app.config['CREW_PHONES'] = {'DP': '+1234567890'}

            with patch('app.notifications.send_sms', return_value=False):
                result = send_assignment_notification(sample_work_item, 'DP')
                assert result is False
