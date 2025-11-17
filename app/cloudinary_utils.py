"""Cloudinary utilities for cloud-based file storage."""

import os
import tempfile
import uuid
from io import BytesIO
from typing import Tuple, Optional
from PIL import Image
import cloudinary
import cloudinary.uploader
import cloudinary.api
from flask import current_app
from werkzeug.datastructures import FileStorage
import requests


def configure_cloudinary():
    """Configure Cloudinary with credentials from app config."""
    if current_app.config.get('USE_CLOUDINARY'):
        cloudinary.config(
            cloud_name=current_app.config['CLOUDINARY_CLOUD_NAME'],
            api_key=current_app.config['CLOUDINARY_API_KEY'],
            api_secret=current_app.config['CLOUDINARY_API_SECRET'],
            secure=True
        )


def process_image(file_storage: FileStorage, max_width: int = 576) -> Tuple[BytesIO, str]:
    """
    Process an uploaded image file: resize and convert HEIC to JPEG.

    Args:
        file_storage: The uploaded file from Flask request
        max_width: Maximum width for the image

    Returns:
        Tuple of (BytesIO buffer with processed image, file extension)
    """
    # Try to import pillow_heif for HEIC support
    try:
        from pillow_heif import register_heif_opener
        register_heif_opener()
    except ImportError:
        pass  # HEIC support not available

    # Open the image from the file storage
    img = Image.open(file_storage.stream)

    # Convert to RGB if needed (handles RGBA, LA, P modes)
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

    # Save to BytesIO buffer as JPEG
    buffer = BytesIO()
    img.save(buffer, 'JPEG', quality=85, optimize=True)
    buffer.seek(0)

    return buffer, 'jpg'


def upload_image_to_cloudinary(file_storage: FileStorage, folder: str = 'work_items') -> dict:
    """
    Upload an image to Cloudinary after processing it.

    Args:
        file_storage: The uploaded file from Flask request
        folder: Cloudinary folder to organize uploads

    Returns:
        Dictionary with 'public_id', 'url', 'secure_url', 'width', 'height'
    """
    configure_cloudinary()

    # Process the image (resize, convert HEIC to JPEG)
    max_width = current_app.config.get('PHOTO_MAX_WIDTH', 576)
    image_buffer, ext = process_image(file_storage, max_width)

    # Generate a unique public_id
    public_id = f"{folder}/{uuid.uuid4().hex}"

    # Upload to Cloudinary
    upload_result = cloudinary.uploader.upload(
        image_buffer,
        public_id=public_id,
        format='jpg',
        resource_type='image',
        overwrite=False,
        quality='auto:good',
        fetch_format='auto'
    )

    return {
        'public_id': upload_result['public_id'],
        'url': upload_result['url'],
        'secure_url': upload_result['secure_url'],
        'width': upload_result['width'],
        'height': upload_result['height'],
        'format': upload_result['format']
    }


def delete_image_from_cloudinary(public_id: str) -> bool:
    """
    Delete an image from Cloudinary.

    Args:
        public_id: The Cloudinary public_id of the image

    Returns:
        True if deletion was successful, False otherwise
    """
    configure_cloudinary()

    try:
        result = cloudinary.uploader.destroy(public_id, resource_type='image')
        return result.get('result') == 'ok'
    except Exception as e:
        current_app.logger.error(f"Error deleting image from Cloudinary: {e}")
        return False


def get_cloudinary_url(public_id: str, transformation: Optional[dict] = None) -> str:
    """
    Get the URL for a Cloudinary image with optional transformations.

    Args:
        public_id: The Cloudinary public_id of the image
        transformation: Optional transformation parameters

    Returns:
        The secure URL for the image
    """
    configure_cloudinary()

    if transformation:
        return cloudinary.CloudinaryImage(public_id).build_url(**transformation)
    else:
        return cloudinary.CloudinaryImage(public_id).build_url(secure=True)


def download_image_from_cloudinary(public_id: str) -> Optional[str]:
    """
    Download an image from Cloudinary to a temporary file for DOCX generation.

    Args:
        public_id: The Cloudinary public_id of the image

    Returns:
        Path to the temporary file, or None if download failed
    """
    configure_cloudinary()

    try:
        # Get the image URL
        url = get_cloudinary_url(public_id)

        # Download the image
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Save to a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
        temp_file.write(response.content)
        temp_file.close()

        return temp_file.name
    except Exception as e:
        current_app.logger.error(f"Error downloading image from Cloudinary: {e}")
        return None


def is_cloudinary_enabled() -> bool:
    """Check if Cloudinary is enabled and configured."""
    return current_app.config.get('USE_CLOUDINARY', False)
