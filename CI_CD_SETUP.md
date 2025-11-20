# CI/CD Pipeline Documentation

## Overview

This document describes the Continuous Integration and Continuous Deployment (CI/CD) pipeline for the Ship Maintenance Tracking Application.

## Table of Contents

- [CI/CD Pipeline Documentation](#cicd-pipeline-documentation)
  - [Overview](#overview)
  - [Table of Contents](#table-of-contents)
  - [Architecture](#architecture)
  - [GitHub Actions Workflows](#github-actions-workflows)
    - [1. CI Workflow (`.github/workflows/ci.yml`)](#1-ci-workflow-githubworkflowsciyml)
    - [2. CD Workflow (`.github/workflows/cd.yml`)](#2-cd-workflow-githubworkflowscdyml)
    - [3. CodeQL Security Analysis (`.github/workflows/codeql.yml`)](#3-codeql-security-analysis-githubworkflowscodeqlyml)
    - [4. Dependency Updates (`.github/workflows/dependency-updates.yml`)](#4-dependency-updates-githubworkflowsdependency-updatesyml)
  - [Code Quality Tools](#code-quality-tools)
    - [Black](#black)
    - [Flake8](#flake8)
    - [Pylint](#pylint)
    - [Bandit](#bandit)
    - [isort](#isort)
  - [Pre-commit Hooks](#pre-commit-hooks)
    - [Installation](#installation)
    - [Usage](#usage)
    - [Available Hooks](#available-hooks)
  - [Testing](#testing)
    - [Running Tests Locally](#running-tests-locally)
    - [Test Coverage](#test-coverage)
    - [Writing Tests](#writing-tests)
  - [Deployment](#deployment)
    - [Staging Deployment](#staging-deployment)
    - [Production Deployment](#production-deployment)
  - [Environment Variables](#environment-variables)
    - [Required Secrets](#required-secrets)
  - [Development Workflow](#development-workflow)
  - [Docker Support](#docker-support)
    - [Building the Image](#building-the-image)
    - [Running the Container](#running-the-container)
  - [Monitoring and Alerts](#monitoring-and-alerts)
  - [Troubleshooting](#troubleshooting)
    - [CI Pipeline Failures](#ci-pipeline-failures)
    - [Deployment Issues](#deployment-issues)
  - [Best Practices](#best-practices)
  - [Contributing](#contributing)

## Architecture

The CI/CD pipeline is built using GitHub Actions and consists of multiple workflows:

```
┌─────────────┐
│   Git Push  │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│         CI Pipeline                  │
├─────────────────────────────────────┤
│ • Code Quality Checks               │
│ • Security Scanning                 │
│ • Unit Tests                        │
│ • Integration Tests                 │
│ • Build Verification                │
└──────┬──────────────────────────────┘
       │
       ▼ (on main branch or tag)
┌─────────────────────────────────────┐
│         CD Pipeline                  │
├─────────────────────────────────────┤
│ • Database Migrations               │
│ • Staging Deployment                │
│ • Smoke Tests                       │
│ • Production Deployment (tags only) │
│ • Docker Image Build & Push         │
└─────────────────────────────────────┘
```

## GitHub Actions Workflows

### 1. CI Workflow (`.github/workflows/ci.yml`)

**Triggers:**
- Push to `main`, `develop`, or `claude/**` branches
- Pull requests to `main` or `develop`

**Jobs:**

1. **Test Job**
   - Runs tests on Python 3.9, 3.10, and 3.11
   - Uses PostgreSQL 15 service container
   - Executes pytest with coverage reporting
   - Uploads coverage to Codecov

2. **Lint Job**
   - Runs Black code formatter check
   - Executes Flake8 linting
   - Runs Pylint static analysis
   - Performs Bandit security scan
   - Uploads security reports as artifacts

3. **Dependency Check Job**
   - Runs Safety security audit on dependencies
   - Identifies known vulnerabilities

4. **Build Job**
   - Verifies application can be built
   - Tests application startup

### 2. CD Workflow (`.github/workflows/cd.yml`)

**Triggers:**
- Push to `main` branch (staging)
- Tags matching `v*` pattern (production)
- Manual workflow dispatch

**Jobs:**

1. **Deploy to Staging**
   - Runs on main branch pushes
   - Executes database migrations
   - Deploys to Railway staging environment
   - Runs health checks

2. **Deploy to Production**
   - Runs on version tags (e.g., v1.0.0)
   - Creates pre-deployment backup
   - Executes database migrations
   - Deploys to Railway production environment
   - Runs smoke tests
   - Creates GitHub release
   - Supports rollback on failure

3. **Docker Build**
   - Builds Docker image
   - Pushes to Docker Hub
   - Uses BuildKit caching for faster builds

### 3. CodeQL Security Analysis (`.github/workflows/codeql.yml`)

**Triggers:**
- Push to `main` or `develop`
- Pull requests to `main` or `develop`
- Weekly schedule (Mondays at 6 AM UTC)
- Manual workflow dispatch

**Features:**
- Analyzes Python and JavaScript code
- Identifies security vulnerabilities
- Runs security and quality queries
- Creates security alerts

### 4. Dependency Updates (`.github/workflows/dependency-updates.yml`)

**Triggers:**
- Weekly schedule (Mondays at 9 AM UTC)
- Manual workflow dispatch

**Features:**
- Checks for outdated dependencies
- Runs security audit with Safety
- Creates GitHub issues for updates
- Creates security alerts for vulnerabilities

## Code Quality Tools

### Black

**Purpose:** Python code formatter

**Configuration:** `pyproject.toml`

```bash
# Format code
black app/ config.py run.py

# Check without modifying
black --check app/ config.py run.py
```

### Flake8

**Purpose:** Python linting and style guide enforcement

**Configuration:** `.flake8`

```bash
# Run Flake8
flake8 app/ config.py run.py
```

### Pylint

**Purpose:** Static code analysis

**Configuration:** `.pylintrc` and `pyproject.toml`

```bash
# Run Pylint
pylint app/ config.py run.py
```

### Bandit

**Purpose:** Security vulnerability scanner

**Configuration:** `pyproject.toml`

```bash
# Run Bandit
bandit -r app/

# Generate JSON report
bandit -r app/ -f json -o bandit-report.json
```

### isort

**Purpose:** Import statement sorting

**Configuration:** `pyproject.toml`

```bash
# Sort imports
isort app/ config.py run.py

# Check without modifying
isort --check app/ config.py run.py
```

## Pre-commit Hooks

Pre-commit hooks automatically run checks before each commit to ensure code quality.

### Installation

```bash
# Install pre-commit
pip install pre-commit

# Install the git hooks
pre-commit install

# Install hooks for commit messages
pre-commit install --hook-type commit-msg
```

### Usage

```bash
# Run on all files
pre-commit run --all-files

# Run on staged files (automatic on commit)
git commit -m "Your message"

# Skip hooks (not recommended)
git commit -m "Your message" --no-verify

# Update hooks to latest versions
pre-commit autoupdate
```

### Available Hooks

1. **Basic Checks:**
   - Trailing whitespace removal
   - End-of-file fixer
   - YAML/JSON/TOML validation
   - Large file detection
   - Merge conflict detection
   - Private key detection

2. **Python Formatting:**
   - Black formatter
   - isort import sorting

3. **Linting:**
   - Flake8 with plugins
   - Pylint

4. **Security:**
   - Bandit security scanner
   - Safety dependency checker
   - Detect-secrets

## Testing

### Running Tests Locally

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_app.py

# Run with verbose output
pytest -v

# Run tests matching a pattern
pytest -k "test_model"
```

### Test Coverage

```bash
# Generate coverage report
pytest --cov=app --cov-report=html

# View report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

Target: Maintain >80% code coverage

### Writing Tests

Tests are located in the `tests/` directory:

- `tests/conftest.py` - Pytest fixtures and configuration
- `tests/test_app.py` - Application tests
- `tests/test_models.py` - Model tests
- `tests/test_routes.py` - Route/view tests

Example test:

```python
def test_create_maintenance_request(app, db):
    """Test creating a maintenance request."""
    with app.app_context():
        request = MaintenanceRequest(
            ship_name="Test Ship",
            department="Engineering",
            problem_description="Test problem"
        )
        db.session.add(request)
        db.session.commit()
        assert request.id is not None
```

## Deployment

### Staging Deployment

**Automatic:**
- Triggered on push to `main` branch
- Deploys to staging environment
- No manual approval required

**Manual:**
```bash
# Via GitHub CLI
gh workflow run cd.yml -f environment=staging

# Via GitHub UI
Actions → CD → Run workflow → Select "staging"
```

### Production Deployment

**Automatic:**
- Triggered by version tags (e.g., `v1.0.0`)
- Requires all CI checks to pass
- Creates GitHub release

**Process:**
```bash
# Create and push a version tag
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

**Manual:**
```bash
# Via GitHub CLI
gh workflow run cd.yml -f environment=production

# Via GitHub UI
Actions → CD → Run workflow → Select "production"
```

## Environment Variables

### Required Secrets

Configure these secrets in GitHub repository settings (Settings → Secrets and variables → Actions):

**Staging:**
- `STAGING_DATABASE_URL` - PostgreSQL connection string
- `STAGING_SECRET_KEY` - Flask secret key

**Production:**
- `PRODUCTION_DATABASE_URL` - PostgreSQL connection string
- `PRODUCTION_SECRET_KEY` - Flask secret key

**Deployment:**
- `RAILWAY_TOKEN` - Railway API token for staging
- `RAILWAY_TOKEN_PRODUCTION` - Railway API token for production

**Docker:**
- `DOCKER_USERNAME` - Docker Hub username
- `DOCKER_PASSWORD` - Docker Hub password/token

**Optional:**
- `CODECOV_TOKEN` - Codecov upload token
- `TWILIO_ACCOUNT_SID` - Twilio account SID
- `TWILIO_AUTH_TOKEN` - Twilio auth token

## Development Workflow

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Install pre-commit hooks:**
   ```bash
   pip install -r requirements-dev.txt
   pre-commit install
   ```

3. **Make your changes and test:**
   ```bash
   # Run tests
   pytest

   # Run linting
   flake8 app/
   pylint app/

   # Format code
   black app/
   isort app/
   ```

4. **Commit your changes:**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   # Pre-commit hooks will run automatically
   ```

5. **Push and create a pull request:**
   ```bash
   git push origin feature/your-feature-name
   # Create PR on GitHub
   ```

6. **Wait for CI checks:**
   - All CI checks must pass
   - Review code coverage
   - Address any security warnings

7. **Merge to main:**
   - Automatically deploys to staging
   - Monitor deployment

8. **Release to production:**
   ```bash
   git checkout main
   git pull origin main
   git tag -a v1.0.0 -m "Release v1.0.0"
   git push origin v1.0.0
   ```

## Docker Support

### Building the Image

```bash
# Build locally
docker build -t ship-mta:latest .

# Build with specific platform
docker build --platform linux/amd64 -t ship-mta:latest .
```

### Running the Container

```bash
# Run with environment variables
docker run -d \
  -p 5001:5001 \
  -e DATABASE_URL="postgresql://..." \
  -e SECRET_KEY="your-secret-key" \
  --name ship-mta \
  ship-mta:latest

# Run with .env file
docker run -d \
  -p 5001:5001 \
  --env-file .env \
  --name ship-mta \
  ship-mta:latest
```

## Monitoring and Alerts

**GitHub Actions:**
- All workflow runs visible in Actions tab
- Email notifications on failure (configurable)
- Status badges available

**Security Alerts:**
- Dependabot alerts for vulnerable dependencies
- CodeQL security alerts
- Weekly security audits

**Coverage Reports:**
- Codecov integration
- Coverage reports in PR comments
- Trend tracking

## Troubleshooting

### CI Pipeline Failures

**Test Failures:**
```bash
# Run locally to debug
pytest -v

# Check specific test
pytest tests/test_app.py::test_name -v
```

**Linting Failures:**
```bash
# Format code
black app/
isort app/

# Check issues
flake8 app/
pylint app/
```

**Coverage Below Threshold:**
```bash
# Generate coverage report
pytest --cov=app --cov-report=html

# View uncovered lines
coverage report -m
```

### Deployment Issues

**Database Migration Failures:**
- Check database credentials
- Verify migration scripts
- Check database connectivity

**Application Won't Start:**
- Verify environment variables
- Check application logs
- Test locally with same configuration

**Health Check Failures:**
- Verify health check endpoint
- Check application is listening on correct port
- Review application logs

## Best Practices

1. **Always run tests locally** before pushing
2. **Keep dependencies updated** - review weekly update issues
3. **Monitor security alerts** - address vulnerabilities promptly
4. **Maintain test coverage** above 80%
5. **Use conventional commits** for clear history
6. **Review pre-commit hook output** - don't skip hooks
7. **Test deployments in staging** before production
8. **Tag releases properly** with semantic versioning
9. **Document breaking changes** in commit messages
10. **Monitor CI/CD pipeline** regularly

## Contributing

When contributing to this project:

1. Follow the development workflow above
2. Ensure all tests pass
3. Maintain or improve code coverage
4. Address all linting warnings
5. Update documentation as needed
6. Add tests for new features
7. Follow security best practices
8. Use pre-commit hooks

---

**Last Updated:** 2025-11-17
**Maintained By:** Development Team
