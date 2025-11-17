from PIL import Image
import os
from werkzeug.utils import secure_filename
from flask import current_app
import uuid
import imghdr
import logging

# Configure logging for file uploads
logger = logging.getLogger(__name__)


def allowed_file(filename: str) -> bool:
    """Return True if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def validate_image_file(file_stream) -> bool:
    """
    Validate that the file is actually an image by checking its MIME type.
    This prevents malicious files from being uploaded with image extensions.

    Args:
        file_stream: File-like object to validate

    Returns:
        bool: True if file is a valid image, False otherwise
    """
    try:
        # Save current position
        pos = file_stream.tell()

        # Read header to detect image type
        header = file_stream.read(512)
        file_stream.seek(pos)  # Reset position

        # Check if it's a valid image format using imghdr
        image_type = imghdr.what(None, header)

        # Also try to open with PIL as a secondary check
        if image_type:
            try:
                Image.open(file_stream).verify()
                file_stream.seek(pos)  # Reset position after verify
                return True
            except Exception as e:
                logger.warning(f"PIL verification failed: {e}")
                file_stream.seek(pos)
                return False

        # For HEIC/HEIF files (not detected by imghdr)
        if header[:4] == b'ftyp' or header[4:8] == b'ftyp':
            # Basic HEIC/HEIF signature check
            try:
                file_stream.seek(pos)
                Image.open(file_stream).verify()
                file_stream.seek(pos)
                return True
            except Exception:
                file_stream.seek(pos)
                return False

        return False
    except Exception as e:
        logger.error(f"Error validating image file: {e}")
        return False


def generate_unique_filename(original_filename: str) -> str:
    """Generate a unique filename while preserving the original extension."""
    ext = original_filename.rsplit('.', 1)[1].lower()
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    return unique_name


def log_file_upload(filename: str, user: str, file_size: int, work_item_id: int = None) -> None:
    """
    Log file upload for security auditing.

    Args:
        filename: Name of the uploaded file
        user: Username of the uploader
        file_size: Size of the file in bytes
        work_item_id: Associated work item ID (if applicable)
    """
    logger.info(
        f"File upload: filename={filename}, user={user}, size={file_size} bytes, "
        f"work_item_id={work_item_id or 'N/A'}"
    )


def resize_image(image_path: str, max_width: int = 576) -> tuple[int, int]:
    """Resize an image in-place to the specified max width while maintaining aspect ratio.
    Converts HEIC/HEIF to JPEG automatically."""
    try:
        # Try to import pillow_heif for HEIC support
        try:
            from pillow_heif import register_heif_opener
            register_heif_opener()
        except ImportError:
            pass  # HEIC support not available, will use Pillow's native support if any
        
        with Image.open(image_path) as img:
            # Convert to RGB if needed
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')

            # Resize if needed
            if img.width > max_width:
                ratio = max_width / img.width
                new_height = int(img.height * ratio)
                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)

            # Always save as JPEG (converts HEIC to JPEG)
            # Change extension to .jpg if it was HEIC
            if image_path.lower().endswith(('.heic', '.heif')):
                image_path = image_path.rsplit('.', 1)[0] + '.jpg'
            
            img.save(image_path, 'JPEG', quality=85, optimize=True)
            return img.width, img.height, image_path
    except Exception as e:
        print(f"Error processing image {image_path}: {e}")
        raise


def get_next_draft_number() -> str:
    """Return the next available DRAFT number starting at DRAFT_0020."""
    from app.models import WorkItem
    
    try:
        existing_items = WorkItem.query.filter(WorkItem.item_number.like('DRAFT_%')).all()

        if not existing_items:
            return 'DRAFT_0020'

        numbers = []
        for item in existing_items:
            try:
                numbers.append(int(item.item_number.replace('DRAFT_', '')))
            except ValueError:
                continue

        next_num = max(numbers) + 1 if numbers else 20
        return f'DRAFT_{next_num:04d}'
    except Exception as e:
        # If there's any error (like empty database), return default
        print(f"Error in get_next_draft_number: {e}")
        return 'DRAFT_0020'


def format_datetime(dt) -> str:
    """Format datetime objects for display."""
    if dt:
        return dt.strftime('%Y-%m-%d %H:%M')
    return ''
