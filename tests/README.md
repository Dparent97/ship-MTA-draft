# Flask Application Test Suite

This directory contains a comprehensive test suite for the Ship Maintenance Tracking Application (MTA).

## Test Coverage

**Overall Coverage: 89.26%**

| Module | Coverage | Tests |
|--------|----------|-------|
| app/auth.py | 100.00% | Authentication and login routes |
| app/models.py | 100.00% | Database models and relationships |
| app/notifications.py | 100.00% | SMS notification system |
| app/docx_generator.py | 97.56% | Document generation |
| app/__init__.py | 95.24% | Application factory |
| app/admin.py | 88.10% | Admin dashboard and routes |
| app/crew.py | 80.46% | Crew submission and edit routes |
| app/utils.py | 79.66% | Utility functions |

## Test Structure

```
tests/
├── conftest.py              # Pytest configuration and fixtures
├── test_admin.py           # Admin routes tests (29 tests)
├── test_auth.py            # Authentication tests (18 tests)
├── test_crew.py            # Crew routes tests (21 tests)
├── test_docx_generator.py  # Document generation tests (13 tests)
├── test_models.py          # Database model tests (20 tests)
├── test_notifications.py   # Notification system tests (17 tests)
└── test_utils.py           # Utility function tests (20 tests)
```

**Total: 138 tests**

## Running Tests

### Install Dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Run All Tests

```bash
pytest
```

### Run with Coverage Report

```bash
pytest --cov=app --cov-report=term-missing --cov-report=html
```

This generates:
- Terminal coverage report
- HTML coverage report in `htmlcov/` directory

### Run Specific Test Files

```bash
pytest tests/test_models.py          # Run only model tests
pytest tests/test_auth.py -v         # Run auth tests with verbose output
pytest tests/test_admin.py::TestAdminDashboard  # Run specific test class
```

### Run with Coverage Threshold

```bash
pytest --cov=app --cov-fail-under=80
```

## Test Categories

### 1. Model Tests (test_models.py)
- WorkItem CRUD operations
- Photo management and cascade deletes
- Comment functionality
- StatusHistory tracking
- Model relationships and constraints

### 2. Authentication Tests (test_auth.py)
- Crew login/logout
- Admin login/logout
- Session management
- Permission redirects
- Index route behavior

### 3. Admin Routes Tests (test_admin.py)
- Dashboard filtering and search
- Work item viewing and editing
- Assignment and status updates
- Photo management
- Document downloads (single and batch)
- Admin notes

### 4. Crew Routes Tests (test_crew.py)
- Work item submission
- Photo uploads with validation
- Assigned item editing
- Permission checks
- Status updates

### 5. Utility Tests (test_utils.py)
- File validation
- Unique filename generation
- Image resizing and conversion
- Draft number generation
- Date formatting

### 6. Notification Tests (test_notifications.py)
- Twilio client initialization
- SMS sending with error handling
- Assignment notifications
- Phone number validation

### 7. Document Generation Tests (test_docx_generator.py)
- Single document generation
- Batch document generation
- Photo inclusion
- Metadata and formatting

## Fixtures

### Application Fixtures
- `app`: Flask application with test configuration
- `client`: Test client for making requests
- `init_database`: Fresh database for each test
- `runner`: CLI test runner

### Authentication Fixtures
- `authenticated_admin_client`: Client with admin session
- `authenticated_crew_client`: Client with crew session

### Data Fixtures
- `sample_work_item`: Basic work item for testing
- `sample_work_item_with_photos`: Work item with photos
- `sample_comment`: Comment associated with work item
- `sample_status_history`: Status change record

### Test Data Fixtures
- `test_image`: Small test image (800x600)
- `test_large_image`: Large test image (1920x1080)

## Configuration

### pytest.ini
- Test discovery patterns
- Coverage settings
- Output formatting
- Custom markers

### .coveragerc
- Coverage source paths
- Exclusions
- Report formatting

## Continuous Integration

The test suite is designed to run in CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run tests
  run: |
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
    pytest --cov=app --cov-report=xml --cov-fail-under=80
```

## Writing New Tests

### Test Organization
1. Group related tests in classes
2. Use descriptive test names (test_description_of_behavior)
3. Follow AAA pattern: Arrange, Act, Assert

### Example Test

```python
def test_create_work_item(self, app, init_database):
    """Test creating a new work item."""
    # Arrange
    work_item = WorkItem(
        item_number='TEST_001',
        location='Engine Room',
        description='Oil leak',
        detail='Test detail',
        submitter_name='DP'
    )

    # Act
    db.session.add(work_item)
    db.session.commit()

    # Assert
    assert work_item.id is not None
    assert work_item.status == 'Submitted'
```

## Coverage Goals

- **Minimum Coverage**: 80%
- **Current Coverage**: 89.26%
- **Target Coverage**: Maintain above 85%

### Areas with Lower Coverage
- Exception handling paths (intentionally not fully tested)
- Optional feature paths (HEIC conversion)
- Error logging statements

## Notes

- All tests use SQLite in-memory database
- Tests are isolated and can run in any order
- Fixtures clean up after themselves
- Test images are created programmatically
- No external dependencies required (mocked Twilio API)

## Troubleshooting

### Import Errors
```bash
# Ensure app is in PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:/path/to/ship-MTA-draft"
```

### Database Errors
```bash
# Clear test database
rm -f test.db
```

### Permission Errors
```bash
# Create test directories
mkdir -p uploads data/generated_docs
```

## Documentation

For more information:
- [Testing Documentation](../TESTING_CHECKLIST.md)
- [Application README](../README.md)
- [pytest Documentation](https://docs.pytest.org/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
