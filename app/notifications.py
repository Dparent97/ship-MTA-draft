"""SMS Notification System using Twilio."""
import logging
from flask import current_app
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException


logger = logging.getLogger(__name__)


def get_twilio_client():
    """Initialize and return Twilio client."""
    account_sid = current_app.config.get('TWILIO_ACCOUNT_SID')
    auth_token = current_app.config.get('TWILIO_AUTH_TOKEN')

    if not account_sid or not auth_token:
        logger.warning('Twilio credentials not configured')
        return None

    return Client(account_sid, auth_token)


def send_sms(to_number, message):
    """
    Send SMS message via Twilio.

    Args:
        to_number: Phone number in E.164 format (e.g., +1234567890)
        message: Message body to send

    Returns:
        bool: True if sent successfully, False otherwise
    """
    if not to_number:
        logger.warning('No phone number provided for SMS')
        return False

    from_number = current_app.config.get('TWILIO_FROM_NUMBER')
    if not from_number:
        logger.warning('Twilio from-number not configured')
        return False

    client = get_twilio_client()
    if not client:
        return False

    try:
        message = client.messages.create(
            body=message,
            from_=from_number,
            to=to_number
        )
        logger.info(f'SMS sent successfully to {to_number}, SID: {message.sid}')
        return True
    except TwilioRestException as e:
        logger.error(f'Twilio error sending SMS to {to_number}: {e.msg} (code: {e.code})')
        return False
    except Exception as e:
        logger.error(f'Unexpected error sending SMS to {to_number}: {str(e)}')
        return False


def send_assignment_notification(work_item, assigned_to, revision_notes=None):
    """
    Send SMS notification when work item is assigned to crew member.

    Args:
        work_item: WorkItem model instance
        assigned_to: Crew member name (e.g., 'DP', 'AL')
        revision_notes: Optional revision notes from admin

    Returns:
        bool: True if sent successfully, False otherwise
    """
    if not current_app.config.get('ENABLE_NOTIFICATIONS'):
        logger.debug('Notifications disabled, skipping SMS')
        return False

    # Get crew member's phone number
    crew_phones = current_app.config.get('CREW_PHONES', {})
    phone_number = crew_phones.get(assigned_to)

    if not phone_number:
        logger.warning(f'No phone number configured for crew member: {assigned_to}')
        return False

    # Build SMS message
    item_number = work_item.item_number
    status = work_item.status

    message_parts = [
        f"Work Item Assigned: {item_number}",
        f"Status: {status}",
    ]

    if revision_notes:
        message_parts.append(f"Notes: {revision_notes}")

    # Add crew login link
    crew_login_url = current_app.config.get('CREW_LOGIN_URL', 'http://localhost:5000/crew/login')
    message_parts.append(f"View at: {crew_login_url}")

    message = "\n\n".join(message_parts)

    # Send SMS
    success = send_sms(phone_number, message)

    if success:
        logger.info(f'Assignment notification sent to {assigned_to} for item {item_number}')
    else:
        logger.error(f'Failed to send assignment notification to {assigned_to} for item {item_number}')

    return success
