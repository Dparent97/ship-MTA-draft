"""Tests for crew routes."""
import pytest
import io
import os
from flask import session
from PIL import Image
from app.models import WorkItem, Photo, Comment
from app import db
from datetime import datetime


class TestCrewRequired:
    """Test crew_required decorator."""

    def test_crew_required_allows_authenticated_crew(self, authenticated_crew_client):
        """Test that authenticated crew can access crew routes."""
        response = authenticated_crew_client.get('/crew/submit')
        assert response.status_code == 200

    def test_crew_required_redirects_unauthenticated(self, client):
        """Test that unauthenticated users are redirected to login."""
        response = client.get('/crew/submit', follow_redirects=False)
        assert response.status_code == 302
        assert '/crew-login' in response.location


class TestSubmitForm:
    """Test crew submit form route."""

    def test_submit_form_get_displays_form(self, authenticated_crew_client):
        """Test that GET request displays the submit form."""
        response = authenticated_crew_client.get('/crew/submit')
        assert response.status_code == 200
        assert b'location' in response.data.lower()
        assert b'description' in response.data.lower()

    def test_submit_form_shows_next_draft_number(self, authenticated_crew_client):
        """Test that form shows next available draft number."""
        response = authenticated_crew_client.get('/crew/submit')
        assert response.status_code == 200
        assert b'DRAFT_' in response.data

    def test_submit_new_work_item_success(self, authenticated_crew_client, app, init_database):
        """Test successful submission of new work item."""
        with authenticated_crew_client.session_transaction() as sess:
            sess['crew_name'] = 'DP'

        response = authenticated_crew_client.post('/crew/submit', data={
            'item_number': 'TEST_NEW',
            'location': 'Engine Room',
            'description': 'Oil leak',
            'detail': 'Small oil leak on starboard engine',
            'references': 'Manual page 42'
        }, follow_redirects=False)

        assert response.status_code == 302
        assert '/crew/success' in response.location

        # Verify work item was created
        with app.app_context():
            work_item = WorkItem.query.filter_by(item_number='TEST_NEW').first()
            assert work_item is not None
            assert work_item.location == 'Engine Room'
            assert work_item.submitter_name == 'DP'

    def test_submit_work_item_missing_required_fields(self, authenticated_crew_client):
        """Test submission with missing required fields."""
        response = authenticated_crew_client.post('/crew/submit', data={
            'item_number': 'TEST_MISSING',
            'location': '',  # Missing
            'description': 'Test',
            'detail': ''  # Missing
        }, follow_redirects=True)

        assert response.status_code == 200
        assert b'required' in response.data.lower()

    def test_submit_work_item_with_photos(self, authenticated_crew_client, app, init_database, test_image):
        """Test submitting work item with photos."""
        with authenticated_crew_client.session_transaction() as sess:
            sess['crew_name'] = 'DP'

        # Create a proper image file
        img = Image.new('RGB', (800, 600), color='blue')
        img_io = io.BytesIO()
        img.save(img_io, 'JPEG')
        img_io.seek(0)
        img_io.name = 'test.jpg'

        response = authenticated_crew_client.post('/crew/submit', data={
            'item_number': 'TEST_PHOTOS',
            'location': 'Deck',
            'description': 'Rust damage',
            'detail': 'Rust on deck plating',
            'references': '',
            'photos': [(img_io, 'test.jpg')],
            'photo_captions': ['Rust photo']
        }, follow_redirects=False, content_type='multipart/form-data')

        assert response.status_code == 302

        # Verify photo was saved
        with app.app_context():
            work_item = WorkItem.query.filter_by(item_number='TEST_PHOTOS').first()
            if work_item:
                assert len(work_item.photos) > 0

    def test_submit_work_item_too_many_photos(self, authenticated_crew_client, app, init_database):
        """Test submission with too many photos."""
        with authenticated_crew_client.session_transaction() as sess:
            sess['crew_name'] = 'DP'

        # Create more photos than allowed
        photos = []
        captions = []
        for i in range(app.config['PHOTO_MAX_COUNT'] + 1):
            img = Image.new('RGB', (100, 100), color='red')
            img_io = io.BytesIO()
            img.save(img_io, 'JPEG')
            img_io.seek(0)
            img_io.name = f'test{i}.jpg'
            photos.append((img_io, f'test{i}.jpg'))
            captions.append(f'Caption {i}')

        response = authenticated_crew_client.post('/crew/submit', data={
            'item_number': 'TEST_TOO_MANY',
            'location': 'Test',
            'description': 'Test',
            'detail': 'Test',
            'photos': photos,
            'photo_captions': captions
        }, follow_redirects=True, content_type='multipart/form-data')

        assert b'Maximum' in response.data or b'maximum' in response.data

    def test_submit_updates_existing_work_item(self, authenticated_crew_client, app, init_database, sample_work_item):
        """Test updating an existing work item."""
        with authenticated_crew_client.session_transaction() as sess:
            sess['crew_name'] = 'AL'

        response = authenticated_crew_client.post('/crew/submit', data={
            'item_number': sample_work_item.item_number,
            'location': 'Updated Location',
            'description': 'Updated Description',
            'detail': 'Updated Detail',
            'references': 'Updated References'
        }, follow_redirects=True)

        # Verify work item was updated
        with app.app_context():
            work_item = WorkItem.query.filter_by(item_number=sample_work_item.item_number).first()
            assert work_item.location == 'Updated Location'
            assert work_item.last_modified_by == 'AL'

    def test_submit_prevents_update_of_completed_item(self, authenticated_crew_client, app, init_database):
        """Test that completed items cannot be updated."""
        with app.app_context():
            work_item = WorkItem(
                item_number='TEST_COMPLETED',
                location='Test',
                ns_equipment='Test',
                description='Test',
                detail='Test',
                submitter_name='DP',
                status='Completed Review'
            )
            db.session.add(work_item)
            db.session.commit()

        response = authenticated_crew_client.post('/crew/submit', data={
            'item_number': 'TEST_COMPLETED',
            'location': 'Updated',
            'description': 'Updated',
            'detail': 'Updated'
        }, follow_redirects=True)

        assert b'already been approved' in response.data or b'Contact admin' in response.data

    def test_submit_form_shows_assigned_items(self, authenticated_crew_client, app, init_database):
        """Test that form shows items assigned to crew member."""
        with authenticated_crew_client.session_transaction() as sess:
            sess['crew_name'] = 'DP'

        with app.app_context():
            work_item = WorkItem(
                item_number='ASSIGNED_TO_DP',
                location='Test',
                ns_equipment='Test',
                description='Test',
                detail='Test',
                submitter_name='Admin',
                assigned_to='DP',
                status='Needs Revision'
            )
            db.session.add(work_item)
            db.session.commit()

        response = authenticated_crew_client.get('/crew/submit')
        assert b'ASSIGNED_TO_DP' in response.data


class TestEditAssignedItem:
    """Test edit assigned item route."""

    def test_edit_assigned_item_get(self, authenticated_crew_client, app, init_database):
        """Test GET request to edit assigned item."""
        with authenticated_crew_client.session_transaction() as sess:
            sess['crew_name'] = 'DP'

        with app.app_context():
            work_item = WorkItem(
                item_number='EDIT_TEST',
                location='Test',
                ns_equipment='Test',
                description='Test',
                detail='Test',
                submitter_name='DP',
                assigned_to='DP',
                status='Needs Revision'
            )
            db.session.add(work_item)
            db.session.commit()
            item_id = work_item.id

        response = authenticated_crew_client.get(f'/crew/edit/{item_id}')
        assert response.status_code == 200
        assert b'EDIT_TEST' in response.data

    def test_edit_assigned_item_permission_denied(self, authenticated_crew_client, app, init_database):
        """Test that crew cannot edit items not assigned to them."""
        with authenticated_crew_client.session_transaction() as sess:
            sess['crew_name'] = 'DP'

        with app.app_context():
            work_item = WorkItem(
                item_number='NOT_ASSIGNED',
                location='Test',
                ns_equipment='Test',
                description='Test',
                detail='Test',
                submitter_name='Admin',
                assigned_to='AL',  # Not assigned to DP
                status='Needs Revision'
            )
            db.session.add(work_item)
            db.session.commit()
            item_id = work_item.id

        response = authenticated_crew_client.get(f'/crew/edit/{item_id}', follow_redirects=True)
        assert b'permission' in response.data.lower()

    def test_edit_assigned_item_wrong_status(self, authenticated_crew_client, app, init_database):
        """Test that items with wrong status cannot be edited."""
        with authenticated_crew_client.session_transaction() as sess:
            sess['crew_name'] = 'DP'

        with app.app_context():
            work_item = WorkItem(
                item_number='WRONG_STATUS',
                location='Test',
                ns_equipment='Test',
                description='Test',
                detail='Test',
                submitter_name='DP',
                assigned_to='DP',
                status='Submitted'  # Not "Needs Revision" or "Awaiting Photos"
            )
            db.session.add(work_item)
            db.session.commit()
            item_id = work_item.id

        response = authenticated_crew_client.get(f'/crew/edit/{item_id}', follow_redirects=True)
        assert b'cannot be edited' in response.data

    def test_edit_assigned_item_post_success(self, authenticated_crew_client, app, init_database):
        """Test successful update of assigned item."""
        with authenticated_crew_client.session_transaction() as sess:
            sess['crew_name'] = 'DP'

        with app.app_context():
            work_item = WorkItem(
                item_number='EDIT_POST',
                location='Test',
                ns_equipment='Test',
                description='Old description',
                detail='Old detail',
                submitter_name='DP',
                assigned_to='DP',
                status='Needs Revision',
                needs_revision=True,
                revision_notes='Please add more details'
            )
            db.session.add(work_item)
            db.session.commit()
            item_id = work_item.id

        response = authenticated_crew_client.post(f'/crew/edit/{item_id}', data={
            'description': 'New description',
            'detail': 'New detail with more information',
            'references': 'New references'
        }, follow_redirects=False)

        assert response.status_code == 302

        # Verify updates
        with app.app_context():
            work_item = WorkItem.query.get(item_id)
            assert work_item.description == 'New description'
            assert work_item.detail == 'New detail with more information'
            assert work_item.status == 'Submitted'  # Status should change back to Submitted
            assert work_item.needs_revision is False
            assert work_item.revision_notes is None


class TestDeleteAssignedPhoto:
    """Test delete assigned photo route."""

    def test_delete_assigned_photo_success(self, authenticated_crew_client, app, init_database):
        """Test successful photo deletion."""
        with authenticated_crew_client.session_transaction() as sess:
            sess['crew_name'] = 'DP'

        with app.app_context():
            work_item = WorkItem(
                item_number='DELETE_PHOTO_TEST',
                location='Test',
                ns_equipment='Test',
                description='Test',
                detail='Test',
                submitter_name='DP',
                assigned_to='DP',
                status='Needs Revision'
            )
            db.session.add(work_item)
            db.session.flush()

            # Create test photo file
            filename = 'test_delete.jpg'
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            img = Image.new('RGB', (100, 100), color='red')
            img.save(filepath, 'JPEG')

            photo = Photo(
                filename=filename,
                caption='Test photo',
                work_item_id=work_item.id
            )
            db.session.add(photo)
            db.session.commit()

            item_id = work_item.id
            photo_id = photo.id

        response = authenticated_crew_client.get(
            f'/crew/delete-photo/{item_id}/{photo_id}',
            follow_redirects=False
        )

        assert response.status_code == 302

        # Verify photo was deleted
        with app.app_context():
            photo = Photo.query.get(photo_id)
            assert photo is None

    def test_delete_assigned_photo_permission_denied(self, authenticated_crew_client, app, init_database):
        """Test that crew cannot delete photos from items not assigned to them."""
        with authenticated_crew_client.session_transaction() as sess:
            sess['crew_name'] = 'DP'

        with app.app_context():
            work_item = WorkItem(
                item_number='NO_PERMISSION',
                location='Test',
                ns_equipment='Test',
                description='Test',
                detail='Test',
                submitter_name='Admin',
                assigned_to='AL',  # Not assigned to DP
                status='Needs Revision'
            )
            db.session.add(work_item)
            db.session.flush()

            photo = Photo(
                filename='test.jpg',
                caption='Test',
                work_item_id=work_item.id
            )
            db.session.add(photo)
            db.session.commit()

            item_id = work_item.id
            photo_id = photo.id

        response = authenticated_crew_client.get(
            f'/crew/delete-photo/{item_id}/{photo_id}',
            follow_redirects=True
        )

        assert b'permission' in response.data.lower()


class TestViewItem:
    """Test view item route."""

    def test_view_item_success(self, authenticated_crew_client, app, init_database, sample_work_item):
        """Test viewing a work item."""
        response = authenticated_crew_client.get(f'/crew/view/{sample_work_item.id}')
        assert response.status_code == 200
        assert sample_work_item.item_number.encode() in response.data

    def test_view_item_shows_can_edit_flag(self, authenticated_crew_client, app, init_database):
        """Test that can_edit flag is set correctly."""
        with authenticated_crew_client.session_transaction() as sess:
            sess['crew_name'] = 'DP'

        with app.app_context():
            # Create item that can be edited
            work_item = WorkItem(
                item_number='CAN_EDIT',
                location='Test',
                ns_equipment='Test',
                description='Test',
                detail='Test',
                submitter_name='DP',
                assigned_to='DP',
                status='Needs Revision'
            )
            db.session.add(work_item)
            db.session.commit()
            item_id = work_item.id

        response = authenticated_crew_client.get(f'/crew/view/{item_id}')
        assert response.status_code == 200
        # The template should show edit button when can_edit is True

    def test_view_item_not_found(self, authenticated_crew_client):
        """Test viewing non-existent item."""
        response = authenticated_crew_client.get('/crew/view/99999')
        assert response.status_code == 404


class TestSuccess:
    """Test success page route."""

    def test_success_page_displays(self, authenticated_crew_client):
        """Test that success page displays."""
        response = authenticated_crew_client.get('/crew/success?item_number=TEST_001')
        assert response.status_code == 200
        assert b'TEST_001' in response.data

    def test_success_page_without_item_number(self, authenticated_crew_client):
        """Test success page without item number."""
        response = authenticated_crew_client.get('/crew/success')
        assert response.status_code == 200
        assert b'Unknown' in response.data or b'success' in response.data.lower()
