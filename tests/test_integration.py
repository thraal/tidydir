"""Integration tests for TidyDir."""

import os
import shutil
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from tidydir import FileOrganizer


class TestIntegration:
    """Integration tests that test the full workflow."""

    @pytest.fixture
    def test_dir(self):
        """Create a test directory with various files."""
        test_dir = Path(tempfile.mkdtemp()).resolve()  # Resolve path immediately

        # Create test files
        files = [
            "document.pdf",
            "photo.jpg",
            "music.mp3",
            "video.mp4",
            "archive.zip",
            "script.py",
            "data.json",
            "unknown.xyz",
        ]

        for filename in files:
            (test_dir / filename).touch()

        # Create an old file
        old_file = test_dir / "old_document.pdf"
        old_file.touch()
        old_time = datetime.now() - timedelta(days=400)
        os.utime(old_file, times=(old_time.timestamp(), old_time.timestamp()))

        # Create subdirectory with files
        subdir = test_dir / "subdir"
        subdir.mkdir()
        (subdir / "nested.txt").touch()

        yield test_dir

        # Cleanup
        def remove_readonly(func, path, _):
            """Error handler for Windows readonly files."""
            if os.name == "nt":
                import stat

                os.chmod(path, stat.S_IWRITE)
            func(path)

        shutil.rmtree(test_dir, onerror=remove_readonly)

    def test_full_organization(self, test_dir):
        """Test complete file organization workflow."""
        organizer = FileOrganizer(source_dir=test_dir)

        # Check permissions
        issues = organizer.check_permissions()
        assert len(issues) == 0

        # Preview
        operations = organizer.preview()
        assert len(operations) > 0

        # Execute
        result = organizer.execute()
        assert result.moved_count > 0
        assert result.moved_count == result.total_count
        assert len(result.errors) == 0

        # Verify files were moved
        assert (test_dir / "Documents" / "document.pdf").exists()
        assert (test_dir / "Images" / "photo.jpg").exists()
        assert (test_dir / "Audio" / "music.mp3").exists()
        assert (test_dir / "Videos" / "video.mp4").exists()
        assert (test_dir / "Archives" / "archive.zip").exists()
        assert (test_dir / "Scripts" / "script.py").exists()
        assert (test_dir / "Text" / "data.json").exists()
        assert (test_dir / "Files" / "unknown.xyz").exists()

        # Check old file was archived
        archive_dirs = list(test_dir.glob("archive_*"))
        assert len(archive_dirs) == 1
        assert (archive_dirs[0] / "Documents" / "old_document.pdf").exists()

        # Original files should be gone
        assert not (test_dir / "document.pdf").exists()
        assert not (test_dir / "photo.jpg").exists()

    def test_simple_subdirectory_organization(self, test_dir):
        """Simple test for subdirectory file organization."""
        # Create a simple structure
        subdir = test_dir / "mysubdir"
        subdir.mkdir()
        test_file = subdir / "test.txt"
        test_file.write_text("test content")

        # Verify file exists
        assert test_file.exists()

        # Organize with subdirs
        organizer = FileOrganizer(source_dir=test_dir, include_subdirs=True)

        # Check file is found
        files = organizer.get_files_to_organize()
        assert any(f.name == "test.txt" for f in files), "File in subdirectory should be found"

        # Execute
        result = organizer.execute()
        assert result.moved_count >= 1, "At least one file should be moved"
        assert len(result.errors) == 0, f"No errors expected, but got: {result.errors}"

        # Check file was moved
        assert (test_dir / "Text" / "test.txt").exists(), "File should be in Text directory"
        assert not test_file.exists(), "Original file should be gone"

    def test_organization_with_subdirs(self, test_dir):
        """Test organization including subdirectories."""
        # First, verify the nested file exists
        nested_file_path = test_dir / "subdir" / "nested.txt"
        assert nested_file_path.exists(), f"Nested file should exist at {nested_file_path}"

        organizer = FileOrganizer(source_dir=test_dir, include_subdirs=True)

        # Get files to organize
        files = organizer.get_files_to_organize()
        nested_files = [f for f in files if f.name == "nested.txt"]
        assert len(nested_files) == 1, (
            f"Nested file should be found when include_subdirs=True. "
            f"Found files: {[str(f) for f in files]}"
        )

        # Execute organization
        result = organizer.execute()

        # Check if there were any errors
        if result.errors:
            print(f"Errors during execution: {result.errors}")

        # The file should have been moved to Text directory
        expected_location = test_dir / "Text" / "nested.txt"

        # Debug: Check what files exist in the Text directory
        text_dir = test_dir / "Text"
        if text_dir.exists():
            text_files = list(text_dir.iterdir())
            assert len(text_files) > 0, (
                "Text directory exists but is empty. "
                f"Contents of test_dir: {list(test_dir.rglob('*'))}"
            )
            assert (
                expected_location.exists()
            ), f"nested.txt not found in Text dir. Files in Text: {[f.name for f in text_files]}"
        else:
            # If Text directory doesn't exist, list what directories do exist
            dirs = [d for d in test_dir.iterdir() if d.is_dir()]
            raise AssertionError(
                f"Text directory doesn't exist. Directories found: {[d.name for d in dirs]}"
            )

        # Original file should be gone
        assert not nested_file_path.exists(), "Original nested file should be gone"

    def test_organization_with_target(self, test_dir):
        """Test organization to different target directory."""
        target_dir = test_dir / "organized"
        organizer = FileOrganizer(source_dir=test_dir, target_dir=target_dir)

        organizer.execute()

        # Files should be in target directory
        assert (target_dir / "Documents" / "document.pdf").exists()
        assert (target_dir / "Images" / "photo.jpg").exists()

        # Source files should be gone
        assert not (test_dir / "document.pdf").exists()
        assert not (test_dir / "photo.jpg").exists()

    def test_organization_with_conflicts(self, test_dir):
        """Test handling of filename conflicts."""
        # Create Images directory with existing file
        images_dir = test_dir / "Images"
        images_dir.mkdir()
        (images_dir / "photo.jpg").touch()

        organizer = FileOrganizer(source_dir=test_dir)
        result = organizer.execute()

        # Both files should exist with different names
        assert (images_dir / "photo.jpg").exists()
        assert (images_dir / "photo_1.jpg").exists()
        assert len(result.conflicts) > 0

    def test_dry_run_preview(self, test_dir):
        """Test that preview doesn't move files."""
        organizer = FileOrganizer(source_dir=test_dir)

        # Get file count before preview
        files_before = list(test_dir.glob("*.*"))

        # Preview
        organizer.preview()

        # Check files haven't moved
        files_after = list(test_dir.glob("*.*"))
        assert len(files_before) == len(files_after)
        assert all(f.exists() for f in files_before)

    def test_logging_creates_log_file(self, test_dir):
        """Test that logging creates a log file."""
        # Create at least one file to ensure something gets logged
        test_file = test_dir / "test.txt"
        test_file.write_text("test content")

        organizer = FileOrganizer(source_dir=test_dir, enable_logging=True)

        # Execute organization
        organizer.execute()

        # Force close all handlers to ensure file is written
        organizer.close_logging()

        # Small delay for file system
        import time

        time.sleep(0.2)

        # Check log file was created - it should NOT be moved
        log_files = list(test_dir.glob("tidydir_*.log"))

        # If not found in root, check if it was moved to Text (which would be a bug)
        if len(log_files) == 0:
            text_dir = test_dir / "Text"
            if text_dir.exists():
                moved_logs = list(text_dir.glob("tidydir_*.log"))
                if moved_logs:
                    raise AssertionError(
                        f"Log file was incorrectly moved to Text directory: {moved_logs}"
                    )

            # Debug: list all files in directory
            all_files = list(test_dir.rglob("tidydir_*.log"))
            print(f"Log files found anywhere: {all_files}")

        assert (
            len(log_files) >= 1
        ), f"Expected at least 1 log file in {test_dir}, found {len(log_files)}"

        # Check log has content (use the first log file)
        if log_files:
            log_content = log_files[0].read_text()
            assert len(log_content) > 0, "Log file should have content"
