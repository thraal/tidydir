#!/usr/bin/env python
"""Fix duplicate extensions in categories.py"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from tidydir.categories import CATEGORY_EXTENSIONS


def find_duplicates():
    """Find all duplicate extensions across categories."""
    all_extensions = {}
    duplicates = []
    
    for category, extensions in CATEGORY_EXTENSIONS.items():
        for ext in extensions:
            if ext in all_extensions:
                duplicates.append((ext, all_extensions[ext], category))
            else:
                all_extensions[ext] = category
    
    return duplicates


def main():
    """Find and report duplicate extensions."""
    duplicates = find_duplicates()
    
    if duplicates:
        print("Found duplicate extensions:")
        for ext, cat1, cat2 in duplicates:
            print(f"  {ext}: in both {cat1} and {cat2}")
    else:
        print("No duplicate extensions found!")
    
    # Also check for duplicates within each category
    print("\nChecking for duplicates within categories:")
    for category, extensions in CATEGORY_EXTENSIONS.items():
        ext_list = list(extensions)
        seen = set()
        for ext in ext_list:
            if ext in seen:
                print(f"  {ext} is duplicated in {category}")
            seen.add(ext)


if __name__ == "__main__":
    main()