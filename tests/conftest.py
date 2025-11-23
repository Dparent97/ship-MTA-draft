"""Pytest configuration and fixtures for the test suite."""
import os
import pytest
import tempfile
from app import create_app, db
from app.models import WorkItem, Photo, Comment, StatusHistory
from datetime import datetime
from PIL import Image
import io


@pytest.fixture(scope='session')
def app():
    """Create and configure a test application instance."""
    # Create a temporary directory for test files
    test_dir = tempfile.mkdtemp()
    upload_folder = os.path.join(test_dir, 'uploads')
    generated_docs = os.path.join(test_dir, 'generated_docs')
    os.makedirs(upload_folder, exist_ok=True)
    os.makedirs(generated_docs, exist_ok=True)

    # Create test configuration
    class TestConfig:
        TESTING = True
        SECRET_KEY = 'test-secret-key'
        SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        WTF_CSRF_ENABLED = False
        UPLOAD_FOLDER = upload_folder
        GENERATED_DOCS_FOLDER = generated_docs
        MAX_CONTENT_LENGTH = 16 * 1024 * 1024
        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'heic', 'heif'}
        PHOTO_MAX_WIDTH = 576
        PHOTO_MIN_COUNT = 0
        PHOTO_MAX_COUNT = 6
        CREW_PASSWORD = 'test_crew_password'
        ADMIN_USERNAME = 'test_admin'
        ADMIN_PASSWORD = 'test_admin_password'
        CREW_MEMBERS = ['DP', 'AL', 'Test User']
        EV_YARD_ITEMS = ['0101 - Test Item']
        DRAFT_ITEMS = ['DRAFT_0001 - Test Draft']
        STATUS_OPTIONS = [
            'Submitted',
            'In Review by DP',
            'In Review by AL',
            'Needs Revision',
            'Awaiting Photos',
            'Completed Review',
        ]
        ENABLE_NOTIFICATIONS = False
        TWILIO_ACCOUNT_SID = None
        TWILIO_AUTH_TOKEN = None
        TWILIO_FROM_NUMBER = None
        CREW_LOGIN_URL = 'http://localhost:5000/crew/login'
        CREW_PHONES = {}

    # Create app with test config
    app = create_app()
    app.config.from_object(TestConfig)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

    # Cleanup test directory
    import shutil
    shutil.rmtree(test_dir, ignore_errors=True)


@pytest.fixture(scope='function')
def client(app):
    """Create a test client."""
    return app.test_client()


@pytest.fixture(scope='function')
def runner(app):
    """Create a test CLI runner."""
    return app.test_cli_runner()


@pytest.fixture(scope='function')
def init_database(app):
    """Initialize the database for each test."""
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()
        db.create_all()


@pytest.fixture
def sample_work_item(app, init_database):
    """Create a sample work item for testing."""
    work_item = WorkItem(
        item_number='TEST_001',
        location='Test Location',
        ns_equipment='Test Equipment',
        description='Test Description',
        detail='Test Detail',
        references='Test References',
        submitter_name='DP',
        status='Submitted',
        submitted_at=datetime.utcnow(),
        original_submitter='DP'
    )
    db.session.add(work_item)
    db.session.commit()
    return work_item


@pytest.fixture
def sample_work_item_with_photos(app, init_database, sample_work_item):
    """Create a sample work item with photos."""
    # Create test image
    img = Image.new('RGB', (800, 600), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, 'JPEG')
    img_bytes.seek(0)

    # Save to upload folder
    filename = 'test_photo.jpg'
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    with open(filepath, 'wb') as f:
        f.write(img_bytes.read())

    # Create photo record
    photo = Photo(
        filename=filename,
        caption='Test Caption',
        work_item_id=sample_work_item.id
    )
    db.session.add(photo)
    db.session.commit()

    return sample_work_item


@pytest.fixture
def sample_comment(app, init_database, sample_work_item):
    """Create a sample comment."""
    comment = Comment(
        work_item_id=sample_work_item.id,
        author_name='DP',
        comment_text='Test comment',
        is_admin=False,
        created_at=datetime.utcnow()
    )
    db.session.add(comment)
    db.session.commit()
    return comment


@pytest.fixture
def sample_status_history(app, init_database, sample_work_item):
    """Create a sample status history entry."""
    history = StatusHistory(
        work_item_id=sample_work_item.id,
        old_status='Submitted',
        new_status='In Review by DP',
        changed_by='admin',
        notes='Test notes',
        changed_at=datetime.utcnow()
    )
    db.session.add(history)
    db.session.commit()
    return history


@pytest.fixture
def authenticated_crew_client(client):
    """Create a client with crew authentication."""
    with client.session_transaction() as sess:
        sess['crew_authenticated'] = True
        sess['crew_name'] = 'DP'
    return client


@pytest.fixture
def authenticated_admin_client(client):
    """Create a client with admin authentication."""
    with client.session_transaction() as sess:
        sess['is_admin'] = True
    return client


@pytest.fixture
def test_image():
    """Create a test image file."""
    img = Image.new('RGB', (800, 600), color='blue')
    img_bytes = io.BytesIO()
    img.save(img_bytes, 'JPEG')
    img_bytes.seek(0)
    img_bytes.name = 'test.jpg'
    return img_bytes


@pytest.fixture
def test_large_image():
    """Create a large test image file."""
    img = Image.new('RGB', (1920, 1080), color='green')
    img_bytes = io.BytesIO()
    img.save(img_bytes, 'JPEG')
    img_bytes.seek(0)
    img_bytes.name = 'test_large.jpg'
    return img_bytes
