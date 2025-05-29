# TidyDir Setup Instructions

Follow these steps to set up your TidyDir project on GitHub:

## 1. Clone Your Repository

```bash
git clone https://github.com/thraal/tidydir.git
cd tidydir
```

## 2. Create Project Structure

Create the following directory structure:
```bash
mkdir -p src/tidydir
mkdir -p tests
mkdir -p docs
mkdir -p .github/workflows
```

## 3. Copy Files

Place each file from this chat in its corresponding location:

### Root Directory Files:
- `pyproject.toml`
- `README.md`
- `CONTRIBUTING.md`
- `CHANGELOG.md`
- `Makefile`
- `mkdocs.yml`
- `setup.py`
- `requirements-dev.txt`
- `.pre-commit-config.yaml`

### Source Files (src/tidydir/):
- `__init__.py`
- `categories.py`
- `organizer.py`
- `cli.py`
- `py.typed`

### Test Files (tests/):
- `__init__.py`
- `conftest.py`
- `test_organizer.py`

### GitHub Actions (.github/workflows/):
- `ci.yml`

### Documentation (docs/):
- `index.md`

## 4. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

## 5. Verify Installation

```bash
# Run tests
pytest

# Check the CLI works
tidydir --version
tidydir --help

# Run code quality checks
make format
make lint
make type-check
```

## 6. Copy the Original Organizer Code

Take the original file organizer code from earlier in our conversation and integrate it into `src/tidydir/organizer.py`. The structure is already set up to use it.

## 7. Initial Git Commit

```bash
# Add all files
git add .

# Make initial commit
git commit -m "Initial commit: TidyDir project structure"

# Push to GitHub
git push origin main
```

## 8. Enable GitHub Actions

GitHub Actions should automatically run when you push. Check the Actions tab in your repository to see the CI pipeline running.

## 9. Optional: Set Up Documentation Site

If you want to host documentation on GitHub Pages:

1. Go to Settings → Pages in your GitHub repository
2. Set Source to "Deploy from a branch"
3. Choose "gh-pages" branch (create it if needed)
4. Run `mkdocs gh-deploy` to deploy docs

## 10. Start Developing!

You're now ready to enhance TidyDir. Some ideas:
- Add more file categories
- Create a GUI version
- Add cloud storage support
- Implement undo functionality
- Add configuration file support

## Troubleshooting

If you encounter issues:

1. **Import errors**: Make sure you're in the virtual environment and have run `pip install -e .`
2. **Permission errors**: Check file permissions, especially on Unix systems
3. **Type checking errors**: Ensure you have Python 3.12+ installed
4. **Test failures**: Check that all test files are in the correct locations

## Project Status Badges

Add these badges to your README.md:

```markdown
[![CI](https://github.com/thraal/tidydir/actions/workflows/ci.yml/badge.svg)](https://github.com/thraal/tidydir/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
```
