"""Tests for database models."""
import pytest
from datetime import datetime
from app.models import WorkItem, Photo, Comment, StatusHistory
from app import db


class TestWorkItem:
    """Test WorkItem model."""

    def test_create_work_item(self, app, init_database):
        """Test creating a new work item."""
        work_item = WorkItem(
            item_number='TEST_001',
            location='Engine Room',
            ns_equipment='Main Engine',
            description='Oil leak',
            detail='Small oil leak detected on starboard side',
            references='Reference manual page 42',
            submitter_name='DP',
            status='Submitted'
        )
        db.session.add(work_item)
        db.session.commit()

        # Verify the work item was created
        assert work_item.id is not None
        assert work_item.item_number == 'TEST_001'
        assert work_item.location == 'Engine Room'
        assert work_item.description == 'Oil leak'
        assert work_item.status == 'Submitted'
        assert work_item.submitted_at is not None

    def test_work_item_repr(self, sample_work_item):
        """Test WorkItem string representation."""
        assert repr(sample_work_item) == '<WorkItem TEST_001>'

    def test_work_item_unique_item_number(self, app, init_database):
        """Test that item numbers must be unique."""
        work_item1 = WorkItem(
            item_number='UNIQUE_001',
            location='Location 1',
            ns_equipment='Equipment 1',
            description='Description 1',
            detail='Detail 1',
            submitter_name='DP'
        )
        db.session.add(work_item1)
        db.session.commit()

        # Try to create another with same item_number
        work_item2 = WorkItem(
            item_number='UNIQUE_001',
            location='Location 2',
            ns_equipment='Equipment 2',
            description='Description 2',
            detail='Detail 2',
            submitter_name='AL'
        )
        db.session.add(work_item2)

        with pytest.raises(Exception):  # SQLAlchemy IntegrityError
            db.session.commit()

    def test_work_item_relationships(self, sample_work_item_with_photos):
        """Test WorkItem relationships with photos, comments, history."""
        assert len(sample_work_item_with_photos.photos) > 0
        assert sample_work_item_with_photos.photos[0].work_item_id == sample_work_item_with_photos.id

    def test_work_item_cascade_delete_photos(self, app, init_database, sample_work_item_with_photos):
        """Test that deleting work item cascades to photos."""
        work_item_id = sample_work_item_with_photos.id
        photo_count = len(sample_work_item_with_photos.photos)

        assert photo_count > 0

        # Delete work item
        db.session.delete(sample_work_item_with_photos)
        db.session.commit()

        # Verify photos were deleted
        remaining_photos = Photo.query.filter_by(work_item_id=work_item_id).all()
        assert len(remaining_photos) == 0

    def test_work_item_assignment_fields(self, app, init_database):
        """Test work item assignment and revision fields."""
        work_item = WorkItem(
            item_number='TEST_002',
            location='Bridge',
            ns_equipment='Navigation',
            description='GPS issue',
            detail='GPS not responding',
            submitter_name='AL',
            assigned_to='DP',
            needs_revision=True,
            revision_notes='Need more details',
            original_submitter='AL',
            last_modified_by='DP',
            last_modified_at=datetime.utcnow()
        )
        db.session.add(work_item)
        db.session.commit()

        assert work_item.assigned_to == 'DP'
        assert work_item.needs_revision is True
        assert work_item.revision_notes == 'Need more details'
        assert work_item.original_submitter == 'AL'

    def test_work_item_admin_notes(self, app, init_database):
        """Test admin notes fields."""
        work_item = WorkItem(
            item_number='TEST_003',
            location='Deck',
            ns_equipment='Crane',
            description='Hydraulic issue',
            detail='Pressure drop',
            submitter_name='Mark',
            admin_notes='Priority item - schedule ASAP',
            admin_notes_updated_at=datetime.utcnow()
        )
        db.session.add(work_item)
        db.session.commit()

        assert work_item.admin_notes == 'Priority item - schedule ASAP'
        assert work_item.admin_notes_updated_at is not None


class TestPhoto:
    """Test Photo model."""

    def test_create_photo(self, app, init_database, sample_work_item):
        """Test creating a photo."""
        photo = Photo(
            filename='test_photo.jpg',
            caption='Test photo caption',
            work_item_id=sample_work_item.id
        )
        db.session.add(photo)
        db.session.commit()

        assert photo.id is not None
        assert photo.filename == 'test_photo.jpg'
        assert photo.caption == 'Test photo caption'
        assert photo.work_item_id == sample_work_item.id

    def test_photo_repr(self, app, init_database, sample_work_item):
        """Test Photo string representation."""
        photo = Photo(
            filename='engine_leak.jpg',
            caption='Oil leak on engine',
            work_item_id=sample_work_item.id
        )
        db.session.add(photo)
        db.session.commit()

        assert repr(photo) == '<Photo engine_leak.jpg>'

    def test_photo_backref(self, sample_work_item_with_photos):
        """Test Photo backref to WorkItem."""
        photo = sample_work_item_with_photos.photos[0]
        assert photo.work_item == sample_work_item_with_photos


class TestComment:
    """Test Comment model."""

    def test_create_comment(self, app, init_database, sample_work_item):
        """Test creating a comment."""
        comment = Comment(
            work_item_id=sample_work_item.id,
            author_name='DP',
            comment_text='This needs to be addressed urgently',
            is_admin=False
        )
        db.session.add(comment)
        db.session.commit()

        assert comment.id is not None
        assert comment.author_name == 'DP'
        assert comment.comment_text == 'This needs to be addressed urgently'
        assert comment.is_admin is False
        assert comment.created_at is not None

    def test_comment_repr(self, sample_comment):
        """Test Comment string representation."""
        assert repr(sample_comment) == '<Comment by DP>'

    def test_comment_admin_flag(self, app, init_database, sample_work_item):
        """Test admin comment flag."""
        admin_comment = Comment(
            work_item_id=sample_work_item.id,
            author_name='Admin',
            comment_text='Admin comment',
            is_admin=True
        )
        db.session.add(admin_comment)
        db.session.commit()

        assert admin_comment.is_admin is True

    def test_comment_cascade_delete(self, app, init_database, sample_work_item, sample_comment):
        """Test that deleting work item cascades to comments."""
        work_item_id = sample_work_item.id

        # Delete work item
        db.session.delete(sample_work_item)
        db.session.commit()

        # Verify comment was deleted
        remaining_comments = Comment.query.filter_by(work_item_id=work_item_id).all()
        assert len(remaining_comments) == 0


class TestStatusHistory:
    """Test StatusHistory model."""

    def test_create_status_history(self, app, init_database, sample_work_item):
        """Test creating a status history entry."""
        history = StatusHistory(
            work_item_id=sample_work_item.id,
            old_status='Submitted',
            new_status='In Review by DP',
            changed_by='admin',
            notes='Assigned to DP for review'
        )
        db.session.add(history)
        db.session.commit()

        assert history.id is not None
        assert history.old_status == 'Submitted'
        assert history.new_status == 'In Review by DP'
        assert history.changed_by == 'admin'
        assert history.notes == 'Assigned to DP for review'
        assert history.changed_at is not None

    def test_status_history_repr(self, sample_status_history, sample_work_item):
        """Test StatusHistory string representation."""
        expected = f'<StatusHistory {sample_work_item.id}: In Review by DP>'
        assert repr(sample_status_history) == expected

    def test_status_history_no_old_status(self, app, init_database, sample_work_item):
        """Test status history can have null old_status (initial creation)."""
        history = StatusHistory(
            work_item_id=sample_work_item.id,
            old_status=None,
            new_status='Submitted',
            changed_by='DP'
        )
        db.session.add(history)
        db.session.commit()

        assert history.old_status is None
        assert history.new_status == 'Submitted'

    def test_status_history_cascade_delete(self, app, init_database, sample_work_item, sample_status_history):
        """Test that deleting work item cascades to status history."""
        work_item_id = sample_work_item.id

        # Delete work item
        db.session.delete(sample_work_item)
        db.session.commit()

        # Verify history was deleted
        remaining_history = StatusHistory.query.filter_by(work_item_id=work_item_id).all()
        assert len(remaining_history) == 0
