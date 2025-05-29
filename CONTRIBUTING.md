# Contributing to TidyDir

Thank you for your interest in contributing to TidyDir! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct: be respectful, inclusive, and considerate of others.

## How to Contribute

### Reporting Bugs

1. Check the [issue tracker](https://github.com/thraal/tidydir/issues) to see if the bug has already been reported
2. If not, create a new issue with:
   - A clear, descriptive title
   - Steps to reproduce the issue
   - Expected behavior
   - Actual behavior
   - System information (OS, Python version)

### Suggesting Features

1. Check the issue tracker for similar feature requests
2. Create a new issue with the "enhancement" label
3. Describe the feature and its use case

### Contributing Code

1. Fork the repository
2. Create a new branch for your feature/fix
3. Write code following our style guide
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/tidydir.git
cd tidydir

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

## Style Guide

- Follow PEP 8
- Use type hints (Python 3.12+ style)
- Maximum line length: 100 characters
- Use Black for formatting
- Use Ruff for linting

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=tidydir

# Run specific test
pytest tests/test_organizer.py::TestFileOrganizer::test_preview
```

## Documentation

- Update docstrings for any new/modified functions
- Update README.md if adding new features
- Add entries to CHANGELOG.md
- Build docs locally: `mkdocs serve`

## Pull Request Process

1. Update CHANGELOG.md with your changes
2. Ensure all tests pass
3. Run linting and formatting: `make format lint type-check`
4. Update documentation if needed
5. Submit PR with clear description

## Release Process

Releases are managed by maintainers. The process is:

1. Update version in `pyproject.toml` and `src/tidydir/__init__.py`
2. Update CHANGELOG.md
3. Create a git tag
4. GitHub Actions will automatically build and can publish to PyPI
