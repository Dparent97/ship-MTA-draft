# Agent 4: DevOps Engineer

## Branch Information
**Branch Name:** `claude/cicd-pipeline-setup`
**Estimated Time:** 3-5 hours
**Priority:** HIGH

## Role & Responsibilities
You are the DevOps Engineer responsible for establishing a complete CI/CD pipeline, automating code quality checks, and streamlining the development workflow. Currently, the project has no automated testing, linting, or deployment pipeline.

## Mission Objective
Implement a comprehensive CI/CD pipeline using GitHub Actions, configure code quality tools (linting, formatting, type checking), and establish best practices for development workflow.

## Current State

**No CI/CD exists:**
- No automated testing on pull requests
- No code quality checks
- No automated deployment
- No pre-commit hooks
- No code formatting standards enforced
- Manual deployment to Railway

## Step-by-Step Tasks

### Phase 1: Code Quality Tools Setup (1-2 hours)

1. **Install development dependencies:**
   ```bash
   pip install black flake8 isort mypy bandit safety
   ```

2. **Create `requirements-dev.txt`:**
   ```txt
   # Code Quality
   black==23.12.1
   flake8==7.0.0
   flake8-docstrings==1.7.0
   isort==5.13.2
   mypy==1.8.0

   # Security
   bandit==1.7.6
   safety==3.0.1

   # Testing (from Agent 1)
   pytest==7.4.3
   pytest-cov==4.1.0
   pytest-flask==1.3.0
   pytest-mock==3.12.0
   faker==22.0.0
   ```

3. **Configure Black (code formatter):**

   Create `pyproject.toml`:
   ```toml
   [tool.black]
   line-length = 100
   target-version = ['py311']
   include = '\.pyi?$'
   extend-exclude = '''
   /(
       \.git
       | \.venv
       | venv
       | build
       | dist
       | migrations
   )/
   '''
   ```

4. **Configure Flake8 (linter):**

   Create `.flake8`:
   ```ini
   [flake8]
   max-line-length = 100
   extend-ignore = E203, W503, E501
   exclude =
       .git,
       __pycache__,
       venv,
       .venv,
       build,
       dist,
       migrations,
       *.egg-info
   per-file-ignores =
       __init__.py:F401
   max-complexity = 10
   ```

5. **Configure isort (import sorting):**

   Add to `pyproject.toml`:
   ```toml
   [tool.isort]
   profile = "black"
   line_length = 100
   skip_gitignore = true
   known_first_party = ["app"]
   ```

6. **Configure mypy (type checking):**

   Create `mypy.ini`:
   ```ini
   [mypy]
   python_version = 3.11
   warn_return_any = True
   warn_unused_configs = True
   disallow_untyped_defs = False  # Gradually enforce
   ignore_missing_imports = True

   [mypy-tests.*]
   ignore_errors = True
   ```

7. **Configure Bandit (security linter):**

   Create `.bandit`:
   ```yaml
   exclude_dirs:
       - /tests/
       - /venv/
       - /.venv/
   skips:
       - B101  # assert_used (OK in tests)
   ```

### Phase 2: Pre-commit Hooks (1 hour)

1. **Install pre-commit:**
   ```bash
   pip install pre-commit
   ```

2. **Create `.pre-commit-config.yaml`:**
   ```yaml
   repos:
     - repo: https://github.com/pre-commit/pre-commit-hooks
       rev: v4.5.0
       hooks:
         - id: trailing-whitespace
         - id: end-of-file-fixer
         - id: check-yaml
         - id: check-added-large-files
           args: ['--maxkb=5000']
         - id: check-json
         - id: check-toml
         - id: check-merge-conflict
         - id: debug-statements

     - repo: https://github.com/psf/black
       rev: 23.12.1
       hooks:
         - id: black
           language_version: python3.11

     - repo: https://github.com/pycqa/isort
       rev: 5.13.2
       hooks:
         - id: isort

     - repo: https://github.com/pycqa/flake8
       rev: 7.0.0
       hooks:
         - id: flake8
           additional_dependencies: [flake8-docstrings]

     - repo: https://github.com/PyCQA/bandit
       rev: 1.7.6
       hooks:
         - id: bandit
           args: ['-c', '.bandit']
   ```

3. **Install pre-commit hooks:**
   ```bash
   pre-commit install
   ```

4. **Test pre-commit hooks:**
   ```bash
   pre-commit run --all-files
   ```

5. **Create `Makefile` for common tasks:**
   ```makefile
   .PHONY: format lint test security clean

   format:
   	black app/ tests/
   	isort app/ tests/

   lint:
   	flake8 app/ tests/
   	mypy app/

   test:
   	pytest tests/ -v --cov=app --cov-report=term-missing

   security:
   	bandit -r app/ -c .bandit
   	safety check

   clean:
   	find . -type d -name __pycache__ -exec rm -rf {} +
   	find . -type f -name '*.pyc' -delete
   	rm -rf .pytest_cache .coverage htmlcov/ .mypy_cache/

   install:
   	pip install -r requirements.txt
   	pip install -r requirements-dev.txt

   install-hooks:
   	pre-commit install

   all: format lint test security
   ```

### Phase 3: GitHub Actions CI/CD (2-3 hours)

1. **Create `.github/workflows/` directory:**
   ```bash
   mkdir -p .github/workflows
   ```

2. **Create `.github/workflows/ci.yml` - Main CI Pipeline:**
   ```yaml
   name: CI Pipeline

   on:
     push:
       branches: [ main, develop, claude/* ]
     pull_request:
       branches: [ main, develop ]

   jobs:
     lint-and-format:
       name: Code Quality Checks
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4

         - name: Set up Python
           uses: actions/setup-python@v4
           with:
             python-version: '3.11'

         - name: Cache dependencies
           uses: actions/cache@v3
           with:
             path: ~/.cache/pip
             key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt') }}
             restore-keys: |
               ${{ runner.os }}-pip-

         - name: Install dependencies
           run: |
             python -m pip install --upgrade pip
             pip install -r requirements.txt
             pip install -r requirements-dev.txt

         - name: Run Black (format check)
           run: black --check app/ tests/

         - name: Run isort (import check)
           run: isort --check-only app/ tests/

         - name: Run Flake8 (linting)
           run: flake8 app/ tests/

         - name: Run mypy (type checking)
           run: mypy app/ || true  # Don't fail on type errors initially

     security:
       name: Security Checks
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4

         - name: Set up Python
           uses: actions/setup-python@v4
           with:
             python-version: '3.11'

         - name: Install dependencies
           run: |
             pip install bandit safety

         - name: Run Bandit (security linting)
           run: bandit -r app/ -c .bandit

         - name: Run Safety (dependency check)
           run: safety check --json || true  # Don't fail initially

     test:
       name: Run Tests
       runs-on: ubuntu-latest
       strategy:
         matrix:
           python-version: ['3.11']
       steps:
         - uses: actions/checkout@v4

         - name: Set up Python ${{ matrix.python-version }}
           uses: actions/setup-python@v4
           with:
             python-version: ${{ matrix.python-version }}

         - name: Install dependencies
           run: |
             python -m pip install --upgrade pip
             pip install -r requirements.txt
             pip install -r requirements-dev.txt

         - name: Run tests with coverage
           run: |
             pytest tests/ -v --cov=app --cov-report=xml --cov-report=term-missing

         - name: Upload coverage to Codecov
           uses: codecov/codecov-action@v3
           with:
             files: ./coverage.xml
             fail_ci_if_error: false

     build:
       name: Test Build
       runs-on: ubuntu-latest
       needs: [lint-and-format, security, test]
       steps:
         - uses: actions/checkout@v4

         - name: Set up Python
           uses: actions/setup-python@v4
           with:
             python-version: '3.11'

         - name: Install dependencies
           run: |
             pip install -r requirements.txt

         - name: Test application startup
           run: |
             export FLASK_ENV=production
             export SECRET_KEY=test-secret-key
             export ADMIN_PASSWORD=test-admin
             export CREW_PASSWORD=test-crew
             python -c "from app import create_app; app = create_app(); print('App created successfully')"
   ```

3. **Create `.github/workflows/deploy.yml` - Auto-deploy to Railway:**
   ```yaml
   name: Deploy to Railway

   on:
     push:
       branches: [ main ]
     workflow_dispatch:  # Allow manual trigger

   jobs:
     deploy:
       name: Deploy to Production
       runs-on: ubuntu-latest
       if: github.ref == 'refs/heads/main'
       steps:
         - uses: actions/checkout@v4

         - name: Install Railway CLI
           run: npm install -g @railway/cli

         - name: Deploy to Railway
           env:
             RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
           run: railway up --detach

         - name: Notify deployment
           run: |
             echo "Deployment to Railway initiated"
             echo "Check Railway dashboard for status"
   ```

4. **Create `.github/workflows/dependency-update.yml` - Automated dependency updates:**
   ```yaml
   name: Dependency Updates

   on:
     schedule:
       - cron: '0 0 * * 0'  # Weekly on Sunday
     workflow_dispatch:

   jobs:
     update-dependencies:
       name: Check for Updates
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4

         - name: Set up Python
           uses: actions/setup-python@v4
           with:
             python-version: '3.11'

         - name: Install dependencies
           run: pip install pip-tools

         - name: Check for outdated packages
           run: |
             pip list --outdated
             echo "Review outdated packages and update manually"

         - name: Security check
           run: |
             pip install safety
             safety check --json || true
   ```

5. **Create `.github/workflows/pr-labeler.yml` - Auto-label PRs:**
   ```yaml
   name: PR Labeler

   on:
     pull_request:
       types: [opened, edited, synchronize]

   jobs:
     label:
       name: Label PR
       runs-on: ubuntu-latest
       steps:
         - uses: actions/labeler@v4
           with:
             repo-token: ${{ secrets.GITHUB_TOKEN }}
   ```

6. **Create `.github/labeler.yml` - PR label configuration:**
   ```yaml
   backend:
     - app/**/*.py

   frontend:
     - app/templates/**/*
     - app/static/**/*

   tests:
     - tests/**/*

   documentation:
     - '**/*.md'
     - docs/**/*

   dependencies:
     - requirements*.txt
     - pyproject.toml

   ci-cd:
     - .github/workflows/**/*
   ```

### Phase 4: Repository Setup (30 minutes)

1. **Create `.github/PULL_REQUEST_TEMPLATE.md`:**
   ```markdown
   ## Description
   Brief description of changes

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update
   - [ ] Performance improvement
   - [ ] Security fix

   ## Testing
   - [ ] All existing tests pass
   - [ ] New tests added (if applicable)
   - [ ] Manual testing completed

   ## Checklist
   - [ ] Code follows project style guidelines (Black, Flake8)
   - [ ] Self-review completed
   - [ ] Comments added for complex logic
   - [ ] Documentation updated
   - [ ] No new warnings introduced
   - [ ] Security considerations reviewed

   ## Related Issues
   Closes #(issue number)

   ## Screenshots (if applicable)
   Add screenshots here
   ```

2. **Create `.github/ISSUE_TEMPLATE/bug_report.md`:**
   ```markdown
   ---
   name: Bug Report
   about: Report a bug or unexpected behavior
   title: '[BUG] '
   labels: bug
   assignees: ''
   ---

   ## Bug Description
   Clear description of the bug

   ## Steps to Reproduce
   1. Go to '...'
   2. Click on '...'
   3. See error

   ## Expected Behavior
   What should happen

   ## Actual Behavior
   What actually happens

   ## Environment
   - Browser: [e.g., Chrome 120]
   - Device: [e.g., iPhone 12]
   - OS: [e.g., iOS 17]

   ## Screenshots
   If applicable, add screenshots

   ## Additional Context
   Any other relevant information
   ```

3. **Create `.github/ISSUE_TEMPLATE/feature_request.md`:**
   ```markdown
   ---
   name: Feature Request
   about: Suggest a new feature or enhancement
   title: '[FEATURE] '
   labels: enhancement
   assignees: ''
   ---

   ## Feature Description
   Clear description of the proposed feature

   ## Problem it Solves
   What problem does this feature address?

   ## Proposed Solution
   How should this feature work?

   ## Alternatives Considered
   Other approaches you've considered

   ## Additional Context
   Any other relevant information
   ```

4. **Update `.gitignore`:**
   ```gitignore
   # Python
   __pycache__/
   *.py[cod]
   *$py.class
   *.so
   .Python
   build/
   develop-eggs/
   dist/
   downloads/
   eggs/
   .eggs/
   lib/
   lib64/
   parts/
   sdist/
   var/
   wheels/
   *.egg-info/
   .installed.cfg
   *.egg

   # Virtual environments
   venv/
   .venv/
   ENV/
   env/

   # IDE
   .vscode/
   .idea/
   *.swp
   *.swo
   *~

   # Testing
   .pytest_cache/
   .coverage
   htmlcov/
   .tox/

   # Type checking
   .mypy_cache/
   .dmypy.json
   dmypy.json

   # Database
   *.db
   *.sqlite
   *.sqlite3

   # Uploaded files
   uploads/
   generated_docs/

   # Environment variables
   .env

   # OS
   .DS_Store
   Thumbs.db

   # Security
   security.log
   ```

### Phase 5: Documentation (1 hour)

1. **Create `CONTRIBUTING.md`:**
   ```markdown
   # Contributing to Ship Maintenance Tracker

   ## Development Setup

   1. Clone the repository
   2. Create virtual environment: `python -m venv venv`
   3. Activate: `source venv/bin/activate` (Unix) or `venv\Scripts\activate` (Windows)
   4. Install dependencies: `make install`
   5. Install pre-commit hooks: `make install-hooks`
   6. Run tests: `make test`

   ## Code Quality

   We use several tools to maintain code quality:
   - **Black** - Code formatting
   - **isort** - Import sorting
   - **Flake8** - Linting
   - **mypy** - Type checking
   - **Bandit** - Security linting

   Run all checks: `make all`

   ## Workflow

   1. Create a feature branch: `git checkout -b feature/your-feature`
   2. Make changes
   3. Run tests: `make test`
   4. Run code quality checks: `make format lint`
   5. Commit with descriptive message
   6. Push and create pull request

   ## Commit Messages

   Follow Conventional Commits:
   - `feat:` New feature
   - `fix:` Bug fix
   - `docs:` Documentation
   - `style:` Formatting
   - `refactor:` Code restructuring
   - `test:` Adding tests
   - `chore:` Maintenance

   ## Pull Request Process

   1. Ensure all tests pass
   2. Update documentation
   3. Fill out PR template
   4. Request review
   5. Address feedback
   6. Squash and merge

   ## Code Style

   - Follow PEP 8
   - Use type hints where possible
   - Write docstrings for functions
   - Keep functions small and focused
   - Add tests for new features
   ```

2. **Update `README.md` with CI/CD badges:**
   ```markdown
   # Arrowhead MTA 26

   ![CI Pipeline](https://github.com/YOUR_USERNAME/ship-MTA-draft/workflows/CI%20Pipeline/badge.svg)
   ![Coverage](https://codecov.io/gh/YOUR_USERNAME/ship-MTA-draft/branch/main/graph/badge.svg)
   ![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)
   ![License](https://img.shields.io/badge/license-Proprietary-red.svg)

   ## Development

   See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

   ### Quick Commands
   ```bash
   make install        # Install dependencies
   make format         # Format code
   make lint          # Run linters
   make test          # Run tests
   make security      # Security checks
   make all           # Run all checks
   ```
   ```

## Files You MUST Create/Modify

### Create:
- `requirements-dev.txt` - Development dependencies
- `pyproject.toml` - Black, isort configuration
- `.flake8` - Flake8 configuration
- `mypy.ini` - mypy configuration
- `.bandit` - Bandit configuration
- `.pre-commit-config.yaml` - Pre-commit hooks
- `Makefile` - Common development tasks
- `.github/workflows/ci.yml` - Main CI pipeline
- `.github/workflows/deploy.yml` - Deployment workflow
- `.github/workflows/dependency-update.yml` - Dependency checks
- `.github/workflows/pr-labeler.yml` - Auto-label PRs
- `.github/labeler.yml` - Label configuration
- `.github/PULL_REQUEST_TEMPLATE.md` - PR template
- `.github/ISSUE_TEMPLATE/bug_report.md` - Bug report template
- `.github/ISSUE_TEMPLATE/feature_request.md` - Feature request template
- `CONTRIBUTING.md` - Contribution guidelines

### Modify:
- `.gitignore` - Add tool-specific ignores
- `README.md` - Add CI badges and development instructions

### DO NOT Modify:
- Application code in `app/`
- Existing configuration files

## Quality Checklist

### Code Quality Tools:
- [ ] Black installed and configured
- [ ] Flake8 installed and configured
- [ ] isort installed and configured
- [ ] mypy installed and configured
- [ ] Bandit installed and configured
- [ ] All tools run successfully on codebase

### Pre-commit Hooks:
- [ ] Pre-commit installed
- [ ] Hooks configured
- [ ] Hooks run on all files successfully

### CI/CD:
- [ ] GitHub Actions workflows created
- [ ] CI pipeline runs on push/PR
- [ ] All jobs pass successfully
- [ ] Code coverage reported
- [ ] Security checks run
- [ ] Auto-deploy configured

### Documentation:
- [ ] README updated with badges
- [ ] CONTRIBUTING.md created
- [ ] PR template created
- [ ] Issue templates created
- [ ] Makefile documented

### Repository Setup:
- [ ] .gitignore comprehensive
- [ ] Labels configured
- [ ] Branch protection recommended

## Success Criteria

- ✅ All code quality tools installed and working
- ✅ Pre-commit hooks preventing bad commits
- ✅ GitHub Actions CI pipeline running
- ✅ All tests pass in CI
- ✅ Code coverage reported
- ✅ Security checks integrated
- ✅ Auto-deployment configured
- ✅ Documentation complete

## Deliverables

1. Complete code quality tool setup
2. Working pre-commit hooks
3. GitHub Actions CI/CD pipelines
4. Repository templates and guidelines
5. Updated documentation
6. Makefile for common tasks

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Black Documentation](https://black.readthedocs.io/)
- [Flake8 Documentation](https://flake8.pycqa.org/)
- [Pre-commit](https://pre-commit.com/)
- [Conventional Commits](https://www.conventionalcommits.org/)

## Notes

- Test workflows locally with [act](https://github.com/nektos/act)
- Consider adding code coverage requirements (e.g., minimum 80%)
- Set up branch protection rules on GitHub
- Configure Dependabot for automated dependency updates
- Consider adding performance benchmarking

---

**Ready to start?** Begin with Phase 1 (Code Quality Tools) and test each tool before moving forward!
