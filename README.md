# TidyDir

[![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)

A smart file organizer that automatically categorizes and organizes files in your directories.

## Features

- **Smart Categorization**: Automatically categorizes files into 15+ categories including Documents, Images, Videos, Code, and more
- **Archive Old Files**: Optionally moves files older than a specified threshold to an archive directory
- **Preview Mode**: See what will happen before making any changes
- **Detailed Summary**: Get insights about your files before and after organization
- **Safe Operation**: Checks permissions and handles conflicts gracefully
- **Optional Logging**: Keep track of all operations performed

## Categories

TidyDir organizes files into the following categories:

- **Applications**: .exe, .msi, .app, .deb, .rpm, .dmg, .pkg, .appimage
- **Archives**: .zip, .tar, .gz, .rar, .7z, .bz2, .xz, .tgz
- **Audio**: .mp3, .wav, .flac, .aac, .ogg, .wma, .m4a, .opus
- **Code**: .c, .cpp, .h, .java, .cs, .go, .rs, .swift, .kt
- **Documents**: .pdf, .doc, .docx, .odt, .rtf, .tex, .wpd
- **Ebooks**: .epub, .mobi, .azw, .azw3, .fb2, .lit, .pdb
- **Images**: .jpg, .jpeg, .png, .gif, .bmp, .svg, .ico, .tiff, .webp
- **Scripts**: .py, .js, .sh, .bat, .ps1, .rb, .pl, .php, .bash
- **Videos**: .mp4, .avi, .mkv, .mov, .wmv, .flv, .webm, .m4v
- And more...

Files that don't match any category are placed in a "Files" directory.

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/thraal/tidydir.git
cd tidydir

# Install in development mode
pip install -e .
```

### Using pip (when published)

```bash
pip install tidydir
```

## Usage

### Basic Usage

Organize files in your Downloads folder:

```bash
tidydir ~/Downloads
```

### Preview Mode

See what will happen without making changes:

```bash
tidydir ~/Downloads --preview
```

### Options

```bash
tidydir [SOURCE] [OPTIONS]

Options:
  -t, --target PATH          Target directory (default: source directory)
  -s, --subdirs             Include subdirectories
  -d, --days N              Days threshold for old files (default: 365)
  -p, --preview             Preview only, don't move files
  -l, --log                 Enable logging to file
  -h, --help                Show help message
```

### Examples

```bash
# Organize Downloads to a different directory
tidydir ~/Downloads --target ~/Organized

# Include subdirectories
tidydir ~/Downloads --subdirs

# Archive files older than 180 days
tidydir ~/Downloads --days 180

# Preview with logging
tidydir ~/Downloads --preview --log

# Full organization with all options
tidydir ~/Downloads --target ~/Organized --subdirs --days 180 --log
```

## Directory Structure

After organization, your directory will look like:

```
Downloads/
├── Applications/
│   └── setup.exe
├── Documents/
│   └── report.pdf
├── Images/
│   ├── photo1.jpg
│   └── photo2.png
└── archive_20240115/
    ├── Archives/
    │   └── old_backup.zip
    └── Videos/
        └── old_video.mp4
```

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/thraal/tidydir.git
cd tidydir

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests with coverage
pytest

# Run specific test file
pytest tests/test_organizer.py

# Run with verbose output
pytest -v
```

### Code Quality

```bash
# Format code
black src tests

# Lint code
ruff check src tests

# Type check
mypy src
```

### Building Documentation

```bash
# Install docs dependencies
pip install -e ".[docs]"

# Serve documentation locally
mkdocs serve

# Build documentation
mkdocs build
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the GNU Affero General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Author

**thraal** - [thraal@gmail.com](mailto:thraal@gmail.com)

## Acknowledgments

- Thanks to all contributors who help improve TidyDir
- Inspired by the need to keep directories organized automatically