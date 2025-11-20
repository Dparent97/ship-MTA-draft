# Makefile for Ship Maintenance Tracking Application

.PHONY: help install install-dev test test-cov lint format clean run docker-build docker-run pre-commit

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install production dependencies
	pip install --upgrade pip
	pip install -r requirements.txt

install-dev:  ## Install development dependencies
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pre-commit install

test:  ## Run tests
	pytest

test-cov:  ## Run tests with coverage report
	pytest --cov=app --cov-report=html --cov-report=term-missing
	@echo "Coverage report generated in htmlcov/index.html"

test-watch:  ## Run tests in watch mode
	pytest-watch

lint:  ## Run all linting tools
	@echo "Running Black..."
	black --check app/ config.py run.py
	@echo "\nRunning isort..."
	isort --check app/ config.py run.py
	@echo "\nRunning Flake8..."
	flake8 app/ config.py run.py
	@echo "\nRunning Pylint..."
	pylint app/ config.py run.py
	@echo "\nRunning Bandit..."
	bandit -r app/

format:  ## Format code with Black and isort
	black app/ config.py run.py
	isort app/ config.py run.py
	@echo "Code formatted successfully!"

security:  ## Run security checks
	@echo "Running Bandit security scan..."
	bandit -r app/
	@echo "\nRunning Safety dependency check..."
	safety check

pre-commit:  ## Run pre-commit hooks on all files
	pre-commit run --all-files

clean:  ## Clean up generated files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov/
	rm -rf dist/
	rm -rf build/
	@echo "Cleaned up generated files!"

run:  ## Run the development server
	python run.py

run-prod:  ## Run with Gunicorn (production-like)
	gunicorn --bind 0.0.0.0:5001 --workers 4 run:app

docker-build:  ## Build Docker image
	docker build -t ship-mta:latest .

docker-run:  ## Run Docker container
	docker run -d -p 5001:5001 --env-file .env --name ship-mta ship-mta:latest

docker-stop:  ## Stop Docker container
	docker stop ship-mta
	docker rm ship-mta

db-init:  ## Initialize database
	python -c "from app import create_app; from app.models import db; app = create_app(); app.app_context().push(); db.create_all()"

db-migrate:  ## Run database migrations
	python migrate_add_admin_notes.py

shell:  ## Start Python shell with app context
	python -c "from app import create_app; app = create_app(); app.app_context().push(); import code; code.interact(local=locals())"

deps-update:  ## Check for outdated dependencies
	pip list --outdated

deps-tree:  ## Show dependency tree
	pip install pipdeptree
	pipdeptree

coverage-report:  ## Open coverage report in browser
	@if [ -f htmlcov/index.html ]; then \
		python -m webbrowser htmlcov/index.html; \
	else \
		echo "Run 'make test-cov' first to generate coverage report"; \
	fi

ci:  ## Run CI checks locally
	@echo "Running CI checks locally..."
	@make format
	@make lint
	@make security
	@make test-cov
	@echo "\n✅ All CI checks passed!"

.DEFAULT_GOAL := help
