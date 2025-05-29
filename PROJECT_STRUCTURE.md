# TidyDir Project Structure

```
tidydir/
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI/CD workflow
├── docs/                       # Documentation source files
│   └── index.md               # Documentation homepage
├── src/
│   └── tidydir/               # Main package
│       ├── __init__.py        # Package initialization
│       ├── categories.py      # File category definitions
│       ├── cli.py            # Command-line interface
│       ├── organizer.py      # Core organization logic
│       └── py.typed          # PEP 561 type marker
├── tests/                     # Test suite
│   ├── __init__.py
│   ├── conftest.py           # Pytest configuration
│   └── test_organizer.py     # Organizer tests
├── .gitignore                # Git ignore file (Python)
├── .pre-commit-config.yaml   # Pre-commit hooks configuration
├── CHANGELOG.md              # Version history
├── CONTRIBUTING.md           # Contribution guidelines
├── LICENSE                   # AGPLv3 license
├── Makefile                  # Development tasks
├── mkdocs.yml               # Documentation configuration
├── pyproject.toml           # Package configuration (PEP 517/518)
├── README.md                # Project documentation
├── requirements-dev.txt     # Development dependencies
└── setup.py                 # Backward compatibility

```

## Key Files

- **pyproject.toml**: Modern Python packaging configuration
- **src/tidydir/organizer.py**: Core file organization logic
- **src/tidydir/cli.py**: Command-line interface
- **src/tidydir/categories.py**: File extension to category mappings
- **tests/**: Comprehensive test suite with pytest
- **.github/workflows/ci.yml**: Automated testing and linting
- **mkdocs.yml**: Documentation configuration

## Development Commands

```bash
# Install for development
make install-dev

# Run tests
make test

# Format code
make format

# Run linting
make lint

# Type checking
make type-check

# Build package
make build

# Clean artifacts
make clean
```