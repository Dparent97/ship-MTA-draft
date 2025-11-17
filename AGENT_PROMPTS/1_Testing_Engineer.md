# Agent 1: Testing Engineer

## Branch Information
**Branch Name:** `claude/testing-suite-implementation`
**Estimated Time:** 1-2 days
**Priority:** CRITICAL

## Role & Responsibilities
You are the Testing Engineer responsible for implementing a comprehensive automated testing suite for the Ship Maintenance Tracking Application. Currently, the application has **ZERO automated tests**, which is a critical gap for production readiness.

## Mission Objective
Create a complete testing infrastructure with unit tests, integration tests, and fixtures covering all critical functionality of the application.

## Step-by-Step Tasks

### Phase 1: Setup Testing Infrastructure (2 hours)

1. **Install testing dependencies:**
   ```bash
   pip install pytest pytest-cov pytest-flask pytest-mock faker
   ```

2. **Create testing directory structure:**
   ```bash
   mkdir -p tests/unit tests/integration tests/fixtures
   touch tests/__init__.py
   touch tests/conftest.py
   touch tests/unit/__init__.py
   touch tests/integration/__init__.py
   ```

3. **Create `tests/conftest.py` with fixtures:**
   - Flask app fixture with test config
   - Database fixture with rollback
   - Client fixture for request testing
   - Sample work item fixtures
   - Sample photo fixtures
   - Admin and crew authentication fixtures

4. **Create `pytest.ini` configuration:**
   ```ini
   [pytest]
   testpaths = tests
   python_files = test_*.py
   python_classes = Test*
   python_functions = test_*
   addopts = -v --cov=app --cov-report=html --cov-report=term-missing
   ```

5. **Update `requirements.txt`:**
   Add testing dependencies (pytest, pytest-cov, pytest-flask, pytest-mock, faker)

### Phase 2: Unit Tests (4-6 hours)

Create unit tests for all modules:

1. **`tests/unit/test_models.py`** - Test all SQLAlchemy models:
   - WorkItem creation and validation
   - Photo model relationships
   - Comment model functionality
   - StatusHistory tracking
   - Test model methods and properties

2. **`tests/unit/test_utils.py`** - Test utility functions:
   - `allowed_file()` validation
   - `generate_unique_filename()` uniqueness
   - `resize_image()` image processing
   - `get_next_draft_number()` numbering
   - `format_datetime()` formatting

3. **`tests/unit/test_auth.py`** - Test authentication:
   - Crew login with correct/incorrect password
   - Admin login with correct/incorrect credentials
   - Session management
   - Logout functionality
   - Authentication decorators

4. **`tests/unit/test_docx_generator.py`** - Test document generation:
   - Single document generation
   - Multiple documents generation
   - Photo insertion
   - Template formatting

5. **`tests/unit/test_notifications.py`** - Test notification system:
   - SMS notification sending (mocked Twilio)
   - Error handling
   - Notification content formatting

### Phase 3: Integration Tests (4-6 hours)

Create integration tests for workflows:

1. **`tests/integration/test_crew_workflow.py`:**
   - Crew login → submit work item → success
   - Photo upload with work item
   - Edit existing work item
   - View assigned items
   - HEIC photo conversion workflow

2. **`tests/integration/test_admin_workflow.py`:**
   - Admin login → view dashboard
   - Filter and search work items
   - Change status of work item
   - Assign work item to crew
   - Delete photo from work item
   - Generate DOCX document
   - Batch download documents

3. **`tests/integration/test_status_workflow.py`:**
   - Complete status change workflow
   - Status history creation
   - Assignment notifications
   - Revision workflow

4. **`tests/integration/test_photo_upload.py`:**
   - Upload multiple photos
   - Photo resize verification
   - HEIC to JPEG conversion
   - Photo deletion
   - Maximum photo limit enforcement

### Phase 4: Test Data & Fixtures (2 hours)

1. **Create `tests/fixtures/sample_data.py`:**
   - Sample work items for all statuses
   - Sample crew members
   - Sample photos (use faker or fixtures)
   - Sample comments
   - Sample status history

2. **Create test image files:**
   - Create small test JPG images
   - Create test HEIC file (if possible)
   - Different sizes for resize testing

### Phase 5: Coverage & Documentation (1-2 hours)

1. **Run tests and generate coverage report:**
   ```bash
   pytest --cov=app --cov-report=html --cov-report=term-missing
   ```

2. **Ensure minimum 80% code coverage** for:
   - `app/models.py` - 100%
   - `app/utils.py` - 100%
   - `app/auth.py` - 95%+
   - `app/crew.py` - 85%+
   - `app/admin.py` - 85%+
   - `app/docx_generator.py` - 80%+

3. **Create `tests/README.md` documenting:**
   - How to run tests
   - How to run specific test modules
   - How to generate coverage reports
   - How to add new tests
   - Testing best practices for this project

## Files You MUST Modify/Create

### Create:
- `tests/conftest.py` - Main fixtures
- `tests/pytest.ini` or `pytest.ini` in root
- `tests/unit/test_models.py`
- `tests/unit/test_utils.py`
- `tests/unit/test_auth.py`
- `tests/unit/test_docx_generator.py`
- `tests/unit/test_notifications.py`
- `tests/integration/test_crew_workflow.py`
- `tests/integration/test_admin_workflow.py`
- `tests/integration/test_status_workflow.py`
- `tests/integration/test_photo_upload.py`
- `tests/fixtures/sample_data.py`
- `tests/README.md`

### Modify:
- `requirements.txt` - Add testing dependencies
- `.gitignore` - Add `.coverage`, `htmlcov/`, `.pytest_cache/`

### DO NOT Modify:
- Any production code in `app/` (unless fixing a bug you discover)
- Any templates in `app/templates/`
- Configuration files (`config.py`) unless adding test-specific config
- Deployment files

## Testing Checklist

### Infrastructure:
- [ ] Pytest installed and configured
- [ ] Coverage reporting working
- [ ] Fixtures created and working
- [ ] Test database isolation working

### Unit Tests:
- [ ] All models tested
- [ ] All utility functions tested
- [ ] Authentication tested
- [ ] Document generation tested
- [ ] Notifications tested (mocked)

### Integration Tests:
- [ ] Crew workflow tested end-to-end
- [ ] Admin workflow tested end-to-end
- [ ] Status changes tested
- [ ] Photo uploads tested

### Coverage:
- [ ] Overall coverage > 80%
- [ ] Critical modules > 90%
- [ ] Coverage report generated
- [ ] No untested critical paths

### Documentation:
- [ ] README created with run instructions
- [ ] Fixtures documented
- [ ] Testing patterns established

## Quality Standards

1. **Test Naming:** Use descriptive names: `test_crew_login_with_valid_password_succeeds()`
2. **Assertions:** Each test should have clear, specific assertions
3. **Isolation:** Tests must not depend on each other
4. **Speed:** Keep tests fast (mock external services, use in-memory DB)
5. **Coverage:** Focus on critical paths first, then edge cases
6. **Readability:** Tests should serve as documentation

## Example Test Structure

```python
def test_create_work_item_with_valid_data_succeeds(client, db):
    """Test that a work item can be created with valid data."""
    # Arrange
    work_item_data = {
        'item_number': 'DRAFT_0001',
        'location': 'Engine Room',
        'description': 'Repair main engine',
        'detail': 'Replace damaged gasket',
        'submitter_name': 'Mark'
    }

    # Act
    response = client.post('/crew/submit', data=work_item_data)

    # Assert
    assert response.status_code == 302  # Redirect after success
    work_item = WorkItem.query.filter_by(item_number='DRAFT_0001').first()
    assert work_item is not None
    assert work_item.location == 'Engine Room'
```

## Success Criteria

- ✅ All tests pass
- ✅ Code coverage > 80%
- ✅ Critical paths covered (login, submit, upload, assign, generate)
- ✅ Tests run in < 30 seconds
- ✅ Clear documentation provided
- ✅ CI-ready (can be integrated with GitHub Actions)

## Deliverables

1. Complete `tests/` directory with all test files
2. Working pytest configuration
3. Coverage report showing > 80% coverage
4. `tests/README.md` documentation
5. Updated `requirements.txt` with test dependencies
6. All tests passing locally

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Flask Testing Guide](https://flask.palletsprojects.com/en/3.0.x/testing/)
- [pytest-flask Plugin](https://pytest-flask.readthedocs.io/)
- [Testing SQLAlchemy Applications](https://docs.sqlalchemy.org/en/20/core/connections.html#using-transactions-in-tests)

## Notes

- Use `faker` library to generate realistic test data
- Mock Twilio API calls in notification tests
- Use temporary directories for photo upload tests
- Ensure test database is separate from development database
- Tests should work in CI environment (no local file dependencies)

---

**Ready to start?** Begin with Phase 1 and work through each phase systematically. Good luck!
