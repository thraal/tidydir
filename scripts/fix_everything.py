#!/usr/bin/env python
"""Fix all CI issues in one go."""

import subprocess
import sys
from pathlib import Path

# Duplicate extensions to remove (extension: category)
DUPLICATES_TO_REMOVE = {
    # In VIDEOS
    ".m1v": "VIDEOS",
    ".m2v": "VIDEOS", 
    ".m2ts": "VIDEOS",
    ".m2t": "VIDEOS",
    # In THREE_D
    ".x3db": "THREE_D",
    ".stl": "THREE_D",  # Keep the first occurrence
    # In AUDIO
    ".aac": "AUDIO",  # Keep the first occurrence
    ".tta": "AUDIO",  # Keep the first occurrence
    ".ymf": "AUDIO",  # Keep the first occurrence
    # In EBOOKS
    ".lit": "EBOOKS",  # Keep the first occurrence
    ".prc": "EBOOKS",  # Keep the first occurrence
    ".ebx": "EBOOKS",  # Keep the first occurrence
    ".htx": "EBOOKS",  
    ".kfx": "EBOOKS",  # Keep the first occurrence
    ".lrs": "EBOOKS",  # Keep the first occurrence
    ".lrx": "EBOOKS",  # Keep the first occurrence
    ".mbp": "EBOOKS",  # Keep the first occurrence
    ".odt": "EBOOKS",
    ".oeb": "EBOOKS",  # Keep the first occurrence
    ".pdb": "EBOOKS",  # Keep the first occurrence
    ".pef": "EBOOKS",  # Keep the first occurrence
    # In SPREADSHEETS
    ".wks": "SPREADSHEETS",  # Keep the first occurrence
    # In PRESENTATIONS
    ".sdd": "PRESENTATIONS",  # Keep the first occurrence
    ".sxi": "PRESENTATIONS",  # Keep the first occurrence
}

def fix_categories_file():
    """Remove duplicate extensions from categories.py"""
    categories_file = Path("src/tidydir/categories.py")
    
    # Read the file
    content = categories_file.read_text()
    
    # Track which extensions we've seen in each category
    # This is a simple approach - remove lines that have duplicate extensions
    lines = content.split('\n')
    new_lines = []
    current_category = None
    seen_in_category = set()
    
    for line in lines:
        # Detect category changes
        if "FileCategory." in line and ": {" in line:
            current_category = line.strip().split('.')[1].split(':')[0]
            seen_in_category = set()
            new_lines.append(line)
        # Check for extension lines
        elif line.strip().startswith('"') and line.strip().endswith('",'):
            ext = line.strip().strip('",')
            if ext not in seen_in_category:
                seen_in_category.add(ext)
                new_lines.append(line)
            else:
                print(f"Removing duplicate {ext} from {current_category}")
        else:
            new_lines.append(line)
    
    # Write back
    categories_file.write_text('\n'.join(new_lines))
    print("✅ Fixed duplicate extensions in categories.py")

def fix_test_integration():
    """Fix issues in test_integration.py"""
    test_file = Path("tests/test_integration.py")
    content = test_file.read_text()
    
    # Fix long lines
    content = content.replace(
        '), f"Nested file should be found when include_subdirs=True. Found files: {[str(f) for f in files]}"',
        '), (\n            f"Nested file should be found when include_subdirs=True. "\n            f"Found files: {[str(f) for f in files]}"\n        )'
    )
    
    content = content.replace(
        '), f"Text directory exists but is empty. Contents of test_dir: {list(test_dir.rglob(\'*\'))}"',
        '), (\n                f"Text directory exists but is empty. "\n                f"Contents of test_dir: {list(test_dir.rglob(\'*\'))}"\n            )'
    )
    
    # Fix assert False
    content = content.replace(
        'assert (\n                False\n            ), f"Text directory doesn\'t exist. Directories found: {[d.name for d in dirs]}"',
        'raise AssertionError(\n                f"Text directory doesn\'t exist. Directories found: {[d.name for d in dirs]}"\n            )'
    )
    
    # Fix unused variables
    content = content.replace(
        'result = organizer.execute()\n\n        # Files should be in target directory',
        'organizer.execute()\n\n        # Files should be in target directory'
    )
    
    content = content.replace(
        'operations = organizer.preview()\n\n        # Check files haven\'t moved',
        'organizer.preview()\n\n        # Check files haven\'t moved'
    )
    
    content = content.replace(
        'result = organizer.execute()\n\n        # Force close all handlers',
        'organizer.execute()\n\n        # Force close all handlers'
    )
    
    test_file.write_text(content)
    print("✅ Fixed test_integration.py issues")

def main():
    """Fix all issues."""
    print("🔧 Fixing all CI issues...\n")
    
    # 1. Fix duplicate extensions
    print("1. Fixing duplicate extensions...")
    fix_categories_file()
    
    # 2. Fix test issues
    print("\n2. Fixing test file issues...")
    fix_test_integration()
    
    # 3. Run black
    print("\n3. Running Black formatter...")
    subprocess.run(["black", "src", "tests"])
    
    # 4. Run ruff fix
    print("\n4. Running Ruff auto-fix...")
    subprocess.run(["ruff", "check", "--fix", "src", "tests"])
    
    # 5. Check remaining issues
    print("\n5. Checking for remaining issues...")
    result = subprocess.run(["ruff", "check", "src", "tests"], capture_output=True)
    
    if result.returncode == 0:
        print("\n✅ All issues fixed!")
        print("\nNow run: pytest")
    else:
        print("\n⚠️  Some issues may remain. Run: ruff check src tests")
    
    return result.returncode

if __name__ == "__main__":
    sys.exit(main())