"""Tests for utility functions."""
import pytest
import os
from PIL import Image
from app.utils import allowed_file, generate_unique_filename, resize_image, get_next_draft_number, format_datetime
from app.models import WorkItem
from app import db
from datetime import datetime
import tempfile


class TestAllowedFile:
    """Test allowed_file function."""

    def test_allowed_extensions(self, app):
        """Test that allowed extensions return True."""
        with app.app_context():
            assert allowed_file('photo.jpg') is True
            assert allowed_file('photo.jpeg') is True
            assert allowed_file('photo.png') is True
            assert allowed_file('photo.heic') is True
            assert allowed_file('photo.heif') is True

    def test_disallowed_extensions(self, app):
        """Test that disallowed extensions return False."""
        with app.app_context():
            assert allowed_file('document.pdf') is False
            assert allowed_file('script.py') is False
            assert allowed_file('archive.zip') is False
            assert allowed_file('video.mp4') is False

    def test_case_insensitive(self, app):
        """Test that file extension check is case-insensitive."""
        with app.app_context():
            assert allowed_file('photo.JPG') is True
            assert allowed_file('photo.JPEG') is True
            assert allowed_file('photo.PNG') is True
            assert allowed_file('photo.HEIC') is True

    def test_no_extension(self, app):
        """Test files without extensions."""
        with app.app_context():
            assert allowed_file('filename') is False
            assert allowed_file('') is False

    def test_multiple_dots(self, app):
        """Test filenames with multiple dots."""
        with app.app_context():
            assert allowed_file('my.photo.jpg') is True
            assert allowed_file('my.photo.txt') is False


class TestGenerateUniqueFilename:
    """Test generate_unique_filename function."""

    def test_preserves_extension(self):
        """Test that the original extension is preserved."""
        filename = generate_unique_filename('photo.jpg')
        assert filename.endswith('.jpg')

        filename = generate_unique_filename('image.png')
        assert filename.endswith('.png')

    def test_generates_unique_names(self):
        """Test that multiple calls generate different filenames."""
        filename1 = generate_unique_filename('photo.jpg')
        filename2 = generate_unique_filename('photo.jpg')
        assert filename1 != filename2

    def test_uses_uuid_format(self):
        """Test that generated filename uses UUID format."""
        filename = generate_unique_filename('photo.jpg')
        # UUID hex is 32 characters + extension
        name_without_ext = filename.rsplit('.', 1)[0]
        assert len(name_without_ext) == 32
        # Should be all hex characters
        assert all(c in '0123456789abcdef' for c in name_without_ext)

    def test_lowercase_extension(self):
        """Test that extension is converted to lowercase."""
        filename = generate_unique_filename('photo.JPG')
        assert filename.endswith('.jpg')


class TestResizeImage:
    """Test resize_image function."""

    def test_resize_large_image(self, app):
        """Test resizing an image larger than max width."""
        with app.app_context():
            # Create a temporary large image
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
                img = Image.new('RGB', (1920, 1080), color='red')
                img.save(tmp.name, 'JPEG')
                tmp_path = tmp.name

            try:
                width, height, new_path = resize_image(tmp_path, max_width=576)
                assert width == 576
                assert height == int(1080 * (576 / 1920))
                assert new_path == tmp_path

                # Verify the image was actually resized on disk
                with Image.open(tmp_path) as resized_img:
                    assert resized_img.width == 576
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)

    def test_no_resize_for_small_image(self, app):
        """Test that small images are not resized."""
        with app.app_context():
            # Create a temporary small image
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
                img = Image.new('RGB', (400, 300), color='blue')
                img.save(tmp.name, 'JPEG')
                tmp_path = tmp.name

            try:
                width, height, new_path = resize_image(tmp_path, max_width=576)
                assert width == 400
                assert height == 300
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)

    def test_converts_rgba_to_rgb(self, app):
        """Test that RGBA images are converted to RGB."""
        with app.app_context():
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                img = Image.new('RGBA', (800, 600), color=(255, 0, 0, 128))
                img.save(tmp.name, 'PNG')
                tmp_path = tmp.name

            try:
                width, height, new_path = resize_image(tmp_path, max_width=576)
                with Image.open(tmp_path) as resized_img:
                    assert resized_img.mode == 'RGB'
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)

    def test_maintains_aspect_ratio(self, app):
        """Test that aspect ratio is maintained during resize."""
        with app.app_context():
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
                img = Image.new('RGB', (1200, 800), color='green')
                img.save(tmp.name, 'JPEG')
                tmp_path = tmp.name

            try:
                width, height, new_path = resize_image(tmp_path, max_width=576)
                # Original aspect ratio: 1200/800 = 1.5
                # New aspect ratio should be close to 1.5
                aspect_ratio = width / height
                assert abs(aspect_ratio - 1.5) < 0.01
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)

    def test_handles_palette_mode(self, app):
        """Test that palette mode images are converted properly."""
        with app.app_context():
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                img = Image.new('P', (800, 600))
                img.save(tmp.name, 'PNG')
                tmp_path = tmp.name

            try:
                width, height, new_path = resize_image(tmp_path, max_width=576)
                with Image.open(tmp_path) as resized_img:
                    assert resized_img.mode == 'RGB'
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)


class TestGetNextDraftNumber:
    """Test get_next_draft_number function."""

    def test_returns_default_when_no_drafts_exist(self, app, init_database):
        """Test that default draft number is returned when no drafts exist."""
        with app.app_context():
            next_num = get_next_draft_number()
            assert next_num == 'DRAFT_0020'

    def test_increments_from_existing_drafts(self, app, init_database):
        """Test that the next draft number increments from existing drafts."""
        with app.app_context():
            # Create some draft work items
            work_item1 = WorkItem(
                item_number='DRAFT_0020',
                location='Test',
                ns_equipment='Test',
                description='Test',
                detail='Test',
                submitter_name='DP'
            )
            work_item2 = WorkItem(
                item_number='DRAFT_0021',
                location='Test',
                ns_equipment='Test',
                description='Test',
                detail='Test',
                submitter_name='DP'
            )
            db.session.add(work_item1)
            db.session.add(work_item2)
            db.session.commit()

            next_num = get_next_draft_number()
            assert next_num == 'DRAFT_0022'

    def test_handles_non_sequential_drafts(self, app, init_database):
        """Test that it finds the max draft number even if non-sequential."""
        with app.app_context():
            work_item1 = WorkItem(
                item_number='DRAFT_0020',
                location='Test',
                ns_equipment='Test',
                description='Test',
                detail='Test',
                submitter_name='DP'
            )
            work_item2 = WorkItem(
                item_number='DRAFT_0025',
                location='Test',
                ns_equipment='Test',
                description='Test',
                detail='Test',
                submitter_name='DP'
            )
            db.session.add(work_item1)
            db.session.add(work_item2)
            db.session.commit()

            next_num = get_next_draft_number()
            assert next_num == 'DRAFT_0026'

    def test_ignores_non_draft_items(self, app, init_database):
        """Test that non-DRAFT items are ignored."""
        with app.app_context():
            work_item = WorkItem(
                item_number='0101',
                location='Test',
                ns_equipment='Test',
                description='Test',
                detail='Test',
                submitter_name='DP'
            )
            db.session.add(work_item)
            db.session.commit()

            next_num = get_next_draft_number()
            assert next_num == 'DRAFT_0020'

    def test_pads_number_with_zeros(self, app, init_database):
        """Test that numbers are zero-padded to 4 digits."""
        with app.app_context():
            work_item = WorkItem(
                item_number='DRAFT_0099',
                location='Test',
                ns_equipment='Test',
                description='Test',
                detail='Test',
                submitter_name='DP'
            )
            db.session.add(work_item)
            db.session.commit()

            next_num = get_next_draft_number()
            assert next_num == 'DRAFT_0100'


class TestFormatDatetime:
    """Test format_datetime function."""

    def test_formats_datetime_correctly(self):
        """Test that datetime is formatted correctly."""
        dt = datetime(2024, 1, 15, 14, 30, 45)
        formatted = format_datetime(dt)
        assert formatted == '2024-01-15 14:30'

    def test_handles_none(self):
        """Test that None returns empty string."""
        formatted = format_datetime(None)
        assert formatted == ''

    def test_formats_different_dates(self):
        """Test formatting various dates."""
        dt1 = datetime(2023, 12, 31, 23, 59, 59)
        assert format_datetime(dt1) == '2023-12-31 23:59'

        dt2 = datetime(2024, 1, 1, 0, 0, 0)
        assert format_datetime(dt2) == '2024-01-01 00:00'

        dt3 = datetime(2024, 6, 15, 9, 5, 30)
        assert format_datetime(dt3) == '2024-06-15 09:05'
