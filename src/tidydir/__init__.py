"""
TidyDir - A smart file organizer that automatically categorizes files in directories.

This package provides functionality to organize files into categories based on their
file extensions, with support for archiving old files and preview mode.
"""

from tidydir.categories import CATEGORY_EXTENSIONS
from tidydir.organizer import FileCategory, FileOrganizer, OrganizeResult

__version__ = "0.1.0"
__author__ = "thraal"
__email__ = "thraal@gmail.com"
__all__ = ["FileOrganizer", "FileCategory", "OrganizeResult", "CATEGORY_EXTENSIONS"]
