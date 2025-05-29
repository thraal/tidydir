.PHONY: help install install-dev test test-cov lint format type-check clean build docs check

help:
	@echo "Available commands:"
	@echo "  make install      Install the package"
	@echo "  make install-dev  Install with development dependencies"
	@echo "  make test         Run tests"
	@echo "  make test-cov     Run tests with coverage"
	@echo "  make lint         Run linting (ruff)"
	@echo "  make format       Format code (black)"
	@echo "  make type-check   Run type checking (mypy)"
	@echo "  make check        Run all code quality checks"
	@echo "  make clean        Clean build artifacts"
	@echo "  make build        Build distribution packages"
	@echo "  make docs         Build documentation"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev,docs]"
	pre-commit install

test:
	pytest

test-cov:
	pytest --cov=tidydir --cov-report=html --cov-report=term-missing

lint:
	ruff check src tests

format:
	black src tests
	ruff check --fix src tests

type-check:
	mypy src

check: format lint type-check test

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build

docs:
	mkdocs build

docs-serve:
	mkdocs serve