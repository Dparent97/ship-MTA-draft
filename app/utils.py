from PIL import Image
import os
from werkzeug.utils import secure_filename
from flask import current_app
import uuid


def allowed_file(filename: str) -> bool:
    """Return True if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def generate_unique_filename(original_filename: str) -> str:
    """Generate a unique filename while preserving the original extension."""
    ext = original_filename.rsplit('.', 1)[1].lower()
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    return unique_name


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
    """Return the next available DRAFT number starting at DRAFT_0020.

    Note: This function is cached for 60 seconds to reduce database load.
    Cache is cleared when new work items are submitted.
    """
    from app.models import WorkItem
    from app import db, cache
    from sqlalchemy import func

    # Try to get from cache first
    cached_value = cache.get('next_draft_number')
    if cached_value:
        return cached_value

    try:
        # Use SQL to find the maximum draft number directly in the database
        # This is much more efficient than fetching all items
        result = db.session.query(
            func.max(WorkItem.item_number)
        ).filter(
            WorkItem.item_number.like('DRAFT_%')
        ).scalar()

        if not result:
            next_draft = 'DRAFT_0020'
        else:
            try:
                # Extract the number from the max draft number
                current_max = int(result.replace('DRAFT_', ''))
                next_num = current_max + 1
                next_draft = f'DRAFT_{next_num:04d}'
            except ValueError:
                # If parsing fails, start from default
                next_draft = 'DRAFT_0020'

        # Cache the result for 60 seconds
        cache.set('next_draft_number', next_draft, timeout=60)
        return next_draft
    except Exception as e:
        # If there's any error (like empty database), return default
        print(f"Error in get_next_draft_number: {e}")
        return 'DRAFT_0020'


def format_datetime(dt) -> str:
    """Format datetime objects for display."""
    if dt:
        return dt.strftime('%Y-%m-%d %H:%M')
    return ''
