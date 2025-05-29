# TidyDir

Welcome to TidyDir's documentation!

TidyDir is a smart file organizer that automatically categorizes and organizes files in your directories. It's designed to help you keep your Downloads folder (or any other directory) clean and organized.

## Features

- **Smart Categorization**: Automatically categorizes files into 15+ categories
- **Archive Old Files**: Optionally moves old files to an archive directory
- **Preview Mode**: See what will happen before making any changes
- **Detailed Summary**: Get insights about your files
- **Safe Operation**: Checks permissions and handles conflicts gracefully
- **Optional Logging**: Keep track of all operations

## Quick Start

```bash
# Install TidyDir
pip install tidydir

# Organize your Downloads folder (preview mode)
tidydir ~/Downloads --preview

# Actually organize the files
tidydir ~/Downloads
```

## How It Works

TidyDir analyzes files based on their extensions and moves them into appropriate category folders:

```
Downloads/
├── Applications/
├── Archives/
├── Audio/
├── Documents/
├── Images/
├── Videos/
└── archive_20240115/  # Old files
    ├── Documents/
    └── Images/
```

## Next Steps

- [Installation Guide](installation.md)
- [Usage Examples](usage.md)
- [API Reference](api/organizer.md)