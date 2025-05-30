#!/bin/bash
# Run all tests with coverage and formatting checks.

echo "🧹 Running code formatters..."
black src tests
ruff check --fix src tests

echo -e "\nRunning type checking..."
mypy src

echo -e "\nRunning tests with coverage..."
pytest --cov=tidydir --cov-report=term-missing -v

echo -e "\nCoverage summary:"
coverage report

echo -e "\nAll checks complete!"