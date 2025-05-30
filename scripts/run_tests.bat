@echo off
REM Run all tests with coverage and formatting checks

echo Running code formatters...
black src tests
ruff check --fix src tests

echo.
echo Running type checking...
mypy src

echo.
echo Running tests with coverage...
pytest --cov=tidydir --cov-report=term-missing -v

echo.
echo Coverage summary:
coverage report

echo.
echo All checks complete!