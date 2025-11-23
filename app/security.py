"""
Security utilities for input validation and sanitization.
"""
import bleach
import re
from werkzeug.utils import secure_filename
from flask import current_app


def sanitize_text_input(text, max_length=None):
    """
    Sanitize text input to prevent XSS attacks.

    Args:
        text: Input text to sanitize
        max_length: Maximum allowed length (optional)

    Returns:
        Sanitized text
    """
    if not text:
        return ''

    # Strip whitespace
    text = text.strip()

    # Enforce max length if specified
    if max_length and len(text) > max_length:
        text = text[:max_length]

    # Remove any HTML tags and potentially dangerous characters
    # Allow basic formatting but strip scripts and other dangerous content
    allowed_tags = []  # No HTML tags allowed in regular text inputs
    allowed_attrs = {}

    return bleach.clean(text, tags=allowed_tags, attributes=allowed_attrs, strip=True)


def sanitize_html_content(html, max_length=None):
    """
    Sanitize HTML content allowing safe formatting tags.

    Args:
        html: HTML content to sanitize
        max_length: Maximum allowed length (optional)

    Returns:
        Sanitized HTML
    """
    if not html:
        return ''

    # Strip whitespace
    html = html.strip()

    # Enforce max length if specified
    if max_length and len(html) > max_length:
        html = html[:max_length]

    # Allow safe HTML tags for formatting
    allowed_tags = ['p', 'br', 'b', 'i', 'u', 'em', 'strong', 'ul', 'ol', 'li', 'span']
    allowed_attrs = {
        '*': ['class']  # Allow class attribute for styling
    }

    return bleach.clean(html, tags=allowed_tags, attributes=allowed_attrs, strip=True)


def validate_item_number(item_number):
    """
    Validate work item number format.

    Args:
        item_number: Item number to validate

    Returns:
        tuple: (is_valid, error_message)
    """
    if not item_number:
        return False, "Item number is required"

    item_number = item_number.strip()

    # Check length
    if len(item_number) > 50:
        return False, "Item number too long (max 50 characters)"

    # Allow alphanumeric, dashes, underscores, and spaces
    if not re.match(r'^[A-Za-z0-9\s_-]+$', item_number):
        return False, "Item number contains invalid characters"

    return True, None


def validate_text_field(text, field_name, min_length=1, max_length=500, required=True):
    """
    Validate a text field with length constraints.

    Args:
        text: Text to validate
        field_name: Name of field for error messages
        min_length: Minimum required length
        max_length: Maximum allowed length
        required: Whether field is required

    Returns:
        tuple: (is_valid, error_message)
    """
    if not text or not text.strip():
        if required:
            return False, f"{field_name} is required"
        return True, None

    text = text.strip()

    if len(text) < min_length:
        return False, f"{field_name} must be at least {min_length} characters"

    if len(text) > max_length:
        return False, f"{field_name} must not exceed {max_length} characters"

    return True, None


def validate_file_upload(file, allowed_extensions=None):
    """
    Validate file upload for security.

    Args:
        file: FileStorage object from request.files
        allowed_extensions: Set of allowed file extensions

    Returns:
        tuple: (is_valid, error_message)
    """
    if not file or not file.filename:
        return False, "No file provided"

    # Get allowed extensions from config if not provided
    if allowed_extensions is None:
        allowed_extensions = current_app.config.get('ALLOWED_EXTENSIONS', {'jpg', 'jpeg', 'png'})

    # Check file extension
    filename = secure_filename(file.filename)
    if '.' not in filename:
        return False, "File must have an extension"

    ext = filename.rsplit('.', 1)[1].lower()
    if ext not in allowed_extensions:
        return False, f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}"

    # Check file size (if content_length is available)
    max_size = current_app.config.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024)
    if hasattr(file, 'content_length') and file.content_length:
        if file.content_length > max_size:
            return False, f"File size exceeds maximum allowed size of {max_size // (1024*1024)}MB"

    return True, None


def sanitize_filename(filename):
    """
    Sanitize filename to prevent directory traversal and other attacks.

    Args:
        filename: Original filename

    Returns:
        Sanitized filename
    """
    # Use Werkzeug's secure_filename which handles most security concerns
    safe_name = secure_filename(filename)

    # Additional checks
    if not safe_name or safe_name == '':
        return 'unnamed_file'

    # Limit length
    if len(safe_name) > 255:
        # Keep extension but truncate name
        name, ext = safe_name.rsplit('.', 1) if '.' in safe_name else (safe_name, '')
        safe_name = name[:250] + ('.' + ext if ext else '')

    return safe_name


def validate_search_query(query, max_length=200):
    """
    Validate search query to prevent injection attacks.

    Args:
        query: Search query string
        max_length: Maximum allowed query length

    Returns:
        tuple: (is_valid, sanitized_query, error_message)
    """
    if not query:
        return True, '', None

    query = query.strip()

    # Check length
    if len(query) > max_length:
        return False, None, f"Search query too long (max {max_length} characters)"

    # Remove special SQL characters that could be used for injection
    # Keep alphanumeric, spaces, and basic punctuation
    sanitized = re.sub(r'[^\w\s\-.,!?\'"]', '', query)

    return True, sanitized, None


def validate_status(status):
    """
    Validate status is in allowed list.

    Args:
        status: Status value to validate

    Returns:
        tuple: (is_valid, error_message)
    """
    if not status:
        return False, "Status is required"

    allowed_statuses = current_app.config.get('STATUS_OPTIONS', [])

    if status not in allowed_statuses:
        return False, f"Invalid status. Allowed values: {', '.join(allowed_statuses)}"

    return True, None


def validate_crew_member(crew_name):
    """
    Validate crew member is in allowed list.

    Args:
        crew_name: Crew member name to validate

    Returns:
        tuple: (is_valid, error_message)
    """
    if not crew_name:
        return False, "Crew member name is required"

    allowed_crew = current_app.config.get('CREW_MEMBERS', [])

    if crew_name not in allowed_crew:
        return False, "Invalid crew member"

    return True, None


def escape_sql_like(s):
    """
    Escape special characters in SQL LIKE patterns.

    Args:
        s: String to escape

    Returns:
        Escaped string safe for SQL LIKE
    """
    if not s:
        return ''

    # Escape special LIKE characters
    s = s.replace('\\', '\\\\')
    s = s.replace('%', '\\%')
    s = s.replace('_', '\\_')

    return s
