#!/usr/bin/env python
"""Debug script to test subdirectory organization."""

import tempfile
import shutil
from pathlib import Path

# Add src to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from tidydir import FileOrganizer


def test_subdirs():
    """Test subdirectory organization."""
    # Create temp directory
    test_dir = Path(tempfile.mkdtemp()).resolve()
    print(f"Test directory: {test_dir}")
    
    try:
        # Create structure
        subdir = test_dir / "subdir"
        subdir.mkdir()
        nested_file = subdir / "nested.txt"
        nested_file.write_text("nested content")
        
        print(f"Created file: {nested_file}")
        print(f"File exists: {nested_file.exists()}")
        
        # Create organizer
        organizer = FileOrganizer(source_dir=test_dir, include_subdirs=True)
        
        # Get files
        files = organizer.get_files_to_organize()
        print(f"\nFiles found: {len(files)}")
        for f in files:
            print(f"  - {f}")
        
        # Preview
        operations = organizer.preview()
        print(f"\nOperations preview:")
        for target_dir, ops in operations.items():
            print(f"  {target_dir}:")
            for op in ops:
                print(f"    - {op.source} -> {op.target}")
        
        # Execute
        result = organizer.execute()
        print(f"\nExecution result:")
        print(f"  Moved: {result.moved_count}/{result.total_count}")
        print(f"  Errors: {len(result.errors)}")
        if result.errors:
            for src, err in result.errors:
                print(f"    - {src}: {err}")
        
        # Check results
        print(f"\nChecking results:")
        text_dir = test_dir / "Text"
        print(f"  Text dir exists: {text_dir.exists()}")
        if text_dir.exists():
            print(f"  Files in Text: {list(text_dir.iterdir())}")
        
        print(f"  Original file exists: {nested_file.exists()}")
        
        # List all files
        print(f"\nAll files in test_dir:")
        for f in test_dir.rglob("*"):
            if f.is_file():
                print(f"  - {f.relative_to(test_dir)}")
                
    finally:
        # Cleanup
        shutil.rmtree(test_dir)
        print(f"\nCleaned up {test_dir}")


if __name__ == "__main__":
    test_subdirs()