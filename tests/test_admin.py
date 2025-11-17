"""Tests for admin routes."""
import pytest
import io
import os
from flask import session
from PIL import Image
from app.models import WorkItem, Photo, StatusHistory
from app import db
from datetime import datetime


class TestAdminRequired:
    """Test admin_required decorator."""

    def test_admin_required_allows_authenticated_admin(self, authenticated_admin_client):
        """Test that authenticated admin can access admin routes."""
        response = authenticated_admin_client.get('/admin/dashboard')
        assert response.status_code == 200

    def test_admin_required_redirects_unauthenticated(self, client):
        """Test that unauthenticated users are redirected to login."""
        response = client.get('/admin/dashboard', follow_redirects=False)
        assert response.status_code == 302
        assert '/admin-login' in response.location

    def test_admin_required_blocks_crew(self, authenticated_crew_client):
        """Test that crew members cannot access admin routes."""
        response = authenticated_crew_client.get('/admin/dashboard', follow_redirects=False)
        assert response.status_code == 302


class TestAdminDashboard:
    """Test admin dashboard route."""

    def test_dashboard_displays_work_items(self, authenticated_admin_client, app, init_database, sample_work_item):
        """Test that dashboard displays work items."""
        response = authenticated_admin_client.get('/admin/dashboard')
        assert response.status_code == 200
        assert sample_work_item.item_number.encode() in response.data

    def test_dashboard_filter_by_status(self, authenticated_admin_client, app, init_database):
        """Test filtering by status."""
        with app.app_context():
            # Create items with different statuses
            item1 = WorkItem(
                item_number='FILTER_1',
                location='Test',
                ns_equipment='Test',
                description='Test',
                detail='Test',
                submitter_name='DP',
                status='Submitted'
            )
            item2 = WorkItem(
                item_number='FILTER_2',
                location='Test',
                ns_equipment='Test',
                description='Test',
                detail='Test',
                submitter_name='DP',
                status='Completed Review'
            )
            db.session.add(item1)
            db.session.add(item2)
            db.session.commit()

        response = authenticated_admin_client.get('/admin/dashboard?status=Submitted')
        assert b'FILTER_1' in response.data

    def test_dashboard_search(self, authenticated_admin_client, app, init_database):
        """Test search functionality."""
        with app.app_context():
            item = WorkItem(
                item_number='SEARCH_TEST',
                location='Engine Room',
                ns_equipment='Test',
                description='Unique search term xyz123',
                detail='Test',
                submitter_name='DP'
            )
            db.session.add(item)
            db.session.commit()

        response = authenticated_admin_client.get('/admin/dashboard?search=xyz123')
        assert b'SEARCH_TEST' in response.data

    def test_dashboard_sort_by_date_desc(self, authenticated_admin_client, app, init_database):
        """Test sorting by date descending."""
        response = authenticated_admin_client.get('/admin/dashboard?sort=date_desc')
        assert response.status_code == 200

    def test_dashboard_sort_by_item_number(self, authenticated_admin_client, app, init_database):
        """Test sorting by item number."""
        response = authenticated_admin_client.get('/admin/dashboard?sort=item_number')
        assert response.status_code == 200


class TestViewItem:
    """Test view item route."""

    def test_view_item_displays_details(self, authenticated_admin_client, sample_work_item):
        """Test viewing work item details."""
        response = authenticated_admin_client.get(f'/admin/view/{sample_work_item.id}')
        assert response.status_code == 200
        assert sample_work_item.item_number.encode() in response.data
        assert sample_work_item.description.encode() in response.data

    def test_view_item_not_found(self, authenticated_admin_client):
        """Test viewing non-existent item."""
        response = authenticated_admin_client.get('/admin/view/99999')
        assert response.status_code == 404


class TestEditItem:
    """Test edit item route."""

    def test_edit_item_success(self, authenticated_admin_client, app, init_database, sample_work_item):
        """Test successful item editing."""
        response = authenticated_admin_client.post(f'/admin/edit/{sample_work_item.id}', data={
            'item_number': 'EDITED_001',
            'location': 'New Location',
            'description': 'New Description',
            'detail': 'New Detail',
            'references': 'New References'
        }, follow_redirects=False)

        assert response.status_code == 302

        # Verify updates
        with app.app_context():
            work_item = WorkItem.query.get(sample_work_item.id)
            assert work_item.item_number == 'EDITED_001'
            assert work_item.location == 'New Location'

    def test_edit_item_with_photos(self, authenticated_admin_client, app, init_database, sample_work_item):
        """Test editing item with new photos."""
        img = Image.new('RGB', (800, 600), color='green')
        img_io = io.BytesIO()
        img.save(img_io, 'JPEG')
        img_io.seek(0)

        response = authenticated_admin_client.post(
            f'/admin/edit/{sample_work_item.id}',
            data={
                'item_number': sample_work_item.item_number,
                'location': sample_work_item.location,
                'description': sample_work_item.description,
                'detail': sample_work_item.detail,
                'references': '',
                'new_photos[]': [(img_io, 'new_photo.jpg')],
                'new_photo_captions[]': ['New photo caption']
            },
            content_type='multipart/form-data',
            follow_redirects=False
        )

        assert response.status_code == 302


class TestAssignItem:
    """Test assign item route."""

    def test_assign_item_success(self, authenticated_admin_client, app, init_database, sample_work_item):
        """Test successful assignment."""
        with authenticated_admin_client.session_transaction() as sess:
            sess['crew_name'] = 'Admin'

        response = authenticated_admin_client.post(f'/admin/assign/{sample_work_item.id}', data={
            'status': 'Needs Revision',
            'assigned_to': 'DP',
            'revision_notes': 'Please add more photos'
        }, follow_redirects=False)

        assert response.status_code == 302

        # Verify assignment
        with app.app_context():
            work_item = WorkItem.query.get(sample_work_item.id)
            assert work_item.assigned_to == 'DP'
            assert work_item.status == 'Needs Revision'
            assert work_item.revision_notes == 'Please add more photos'
            assert work_item.needs_revision is True

    def test_assign_item_creates_history(self, authenticated_admin_client, app, init_database, sample_work_item):
        """Test that assignment creates status history."""
        with authenticated_admin_client.session_transaction() as sess:
            sess['crew_name'] = 'Admin'

        old_status = sample_work_item.status

        response = authenticated_admin_client.post(f'/admin/assign/{sample_work_item.id}', data={
            'status': 'In Review by DP',
            'assigned_to': 'DP',
            'revision_notes': 'Test notes'
        }, follow_redirects=False)

        # Verify history was created
        with app.app_context():
            history = StatusHistory.query.filter_by(work_item_id=sample_work_item.id).first()
            assert history is not None
            assert history.new_status == 'In Review by DP'


class TestUpdateStatus:
    """Test update status route."""

    def test_update_status_success(self, authenticated_admin_client, app, init_database, sample_work_item):
        """Test successful status update."""
        response = authenticated_admin_client.post(f'/admin/update-status/{sample_work_item.id}', data={
            'status': 'Completed Review'
        }, follow_redirects=False)

        assert response.status_code == 302

        # Verify status
        with app.app_context():
            work_item = WorkItem.query.get(sample_work_item.id)
            assert work_item.status == 'Completed Review'

    def test_update_status_invalid(self, authenticated_admin_client, sample_work_item):
        """Test updating to invalid status."""
        response = authenticated_admin_client.post(f'/admin/update-status/{sample_work_item.id}', data={
            'status': 'Invalid Status'
        }, follow_redirects=True)

        assert b'Invalid' in response.data


class TestDownloadSingle:
    """Test download single item route."""

    def test_download_single_success(self, authenticated_admin_client, app, init_database, sample_work_item):
        """Test downloading single work item as docx."""
        response = authenticated_admin_client.get(f'/admin/download/{sample_work_item.id}')

        # Should return a file
        assert response.status_code == 200
        assert response.content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'

    def test_download_single_not_found(self, authenticated_admin_client):
        """Test downloading non-existent item."""
        response = authenticated_admin_client.get('/admin/download/99999', follow_redirects=True)
        # Should redirect with error message
        assert response.status_code == 200


class TestDownloadBatch:
    """Test download batch route."""

    def test_download_batch_success(self, authenticated_admin_client, app, init_database):
        """Test downloading multiple items as zip."""
        with app.app_context():
            # Create multiple items
            items = []
            for i in range(3):
                item = WorkItem(
                    item_number=f'BATCH_{i}',
                    location='Test',
                    ns_equipment='Test',
                    description='Test',
                    detail='Test',
                    submitter_name='DP'
                )
                db.session.add(item)
                items.append(item)
            db.session.commit()
            item_ids = [item.id for item in items]

        response = authenticated_admin_client.post('/admin/download-batch', data={
            'item_ids[]': item_ids
        })

        assert response.status_code == 200
        assert response.content_type == 'application/zip'

    def test_download_batch_no_items(self, authenticated_admin_client):
        """Test downloading with no items selected."""
        response = authenticated_admin_client.post('/admin/download-batch', data={
            'item_ids[]': []
        }, follow_redirects=True)

        assert b'No items selected' in response.data


class TestDeleteItem:
    """Test delete item route."""

    def test_delete_item_success(self, authenticated_admin_client, app, init_database):
        """Test successful item deletion."""
        with app.app_context():
            item = WorkItem(
                item_number='DELETE_ME',
                location='Test',
                ns_equipment='Test',
                description='Test',
                detail='Test',
                submitter_name='DP'
            )
            db.session.add(item)
            db.session.commit()
            item_id = item.id

        response = authenticated_admin_client.post(f'/admin/delete/{item_id}', follow_redirects=False)
        assert response.status_code == 302

        # Verify deletion
        with app.app_context():
            item = WorkItem.query.get(item_id)
            assert item is None

    def test_delete_item_with_photos(self, authenticated_admin_client, app, init_database, sample_work_item_with_photos):
        """Test deleting item with photos."""
        item_id = sample_work_item_with_photos.id

        response = authenticated_admin_client.post(f'/admin/delete/{item_id}', follow_redirects=False)
        assert response.status_code == 302

        # Verify deletion
        with app.app_context():
            item = WorkItem.query.get(item_id)
            assert item is None


class TestDownloadPhoto:
    """Test download photo route."""

    def test_download_photo_success(self, authenticated_admin_client, app, init_database, sample_work_item_with_photos):
        """Test downloading a single photo."""
        photo = sample_work_item_with_photos.photos[0]

        response = authenticated_admin_client.get(
            f'/admin/download-photo/{sample_work_item_with_photos.id}/{photo.id}'
        )

        assert response.status_code == 200

    def test_download_photo_wrong_work_item(self, authenticated_admin_client, app, init_database):
        """Test downloading photo with mismatched work item."""
        with app.app_context():
            item1 = WorkItem(
                item_number='ITEM1',
                location='Test',
                ns_equipment='Test',
                description='Test',
                detail='Test',
                submitter_name='DP'
            )
            item2 = WorkItem(
                item_number='ITEM2',
                location='Test',
                ns_equipment='Test',
                description='Test',
                detail='Test',
                submitter_name='DP'
            )
            db.session.add(item1)
            db.session.add(item2)
            db.session.flush()

            photo = Photo(
                filename='test.jpg',
                caption='Test',
                work_item_id=item1.id
            )
            db.session.add(photo)
            db.session.commit()

            # Try to access photo via wrong work item
            response = authenticated_admin_client.get(
                f'/admin/download-photo/{item2.id}/{photo.id}',
                follow_redirects=True
            )

            assert b'Invalid photo' in response.data


class TestDeletePhoto:
    """Test delete photo route."""

    def test_delete_photo_success(self, authenticated_admin_client, app, init_database, sample_work_item_with_photos):
        """Test successful photo deletion."""
        photo = sample_work_item_with_photos.photos[0]
        photo_id = photo.id

        response = authenticated_admin_client.get(
            f'/admin/delete-photo/{sample_work_item_with_photos.id}/{photo_id}',
            follow_redirects=False
        )

        assert response.status_code == 302

        # Verify deletion
        with app.app_context():
            photo = Photo.query.get(photo_id)
            assert photo is None

    def test_delete_photo_wrong_work_item(self, authenticated_admin_client, app, init_database):
        """Test deleting photo with mismatched work item."""
        with app.app_context():
            item1 = WorkItem(
                item_number='ITEM1',
                location='Test',
                ns_equipment='Test',
                description='Test',
                detail='Test',
                submitter_name='DP'
            )
            item2 = WorkItem(
                item_number='ITEM2',
                location='Test',
                ns_equipment='Test',
                description='Test',
                detail='Test',
                submitter_name='DP'
            )
            db.session.add(item1)
            db.session.add(item2)
            db.session.flush()

            photo = Photo(
                filename='test.jpg',
                caption='Test',
                work_item_id=item1.id
            )
            db.session.add(photo)
            db.session.commit()

            response = authenticated_admin_client.get(
                f'/admin/delete-photo/{item2.id}/{photo.id}',
                follow_redirects=True
            )

            assert b'Invalid photo' in response.data


class TestSaveAdminNotes:
    """Test save admin notes route."""

    def test_save_admin_notes_success(self, authenticated_admin_client, app, init_database, sample_work_item):
        """Test saving admin notes."""
        response = authenticated_admin_client.post(f'/admin/save-admin-notes/{sample_work_item.id}', data={
            'admin_notes': 'Important internal note about this item'
        }, follow_redirects=False)

        assert response.status_code == 302

        # Verify notes were saved
        with app.app_context():
            work_item = WorkItem.query.get(sample_work_item.id)
            assert work_item.admin_notes == 'Important internal note about this item'
            assert work_item.admin_notes_updated_at is not None

    def test_save_empty_admin_notes(self, authenticated_admin_client, app, init_database, sample_work_item):
        """Test saving empty admin notes."""
        response = authenticated_admin_client.post(f'/admin/save-admin-notes/{sample_work_item.id}', data={
            'admin_notes': ''
        }, follow_redirects=False)

        assert response.status_code == 302

        # Verify notes were cleared
        with app.app_context():
            work_item = WorkItem.query.get(sample_work_item.id)
            assert work_item.admin_notes == ''


class TestServeUpload:
    """Test serve upload route."""

    def test_serve_upload_success(self, authenticated_admin_client, app, init_database, sample_work_item_with_photos):
        """Test serving uploaded photo."""
        photo = sample_work_item_with_photos.photos[0]

        response = authenticated_admin_client.get(f'/admin/uploads/{photo.filename}')
        assert response.status_code == 200
