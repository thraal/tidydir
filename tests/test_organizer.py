"""Tests for the FileOrganizer class."""

import os
import tempfile
import shutil
from pathlib import Path
from datetime import datetime, timedelta
import pytest

from tidydir.organizer import FileOrganizer, FileCategory, OrganizeResult
from tidydir.categories import CATEGORY_EXTENSIONS


class TestFileOrganizer:
    """Test suite for FileOrganizer."""

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        # Force cleanup on Windows
        import os
        import stat

        def remove_readonly(func, path, _exc_info):
            """Error handler for Windows readonly files."""
            os.chmod(path, stat.S_IWRITE)
            func(path)

        shutil.rmtree(temp_dir, onerror=remove_readonly)

    @pytest.fixture
    def organizer(self, temp_dir):
        """Create a FileOrganizer instance."""
        return FileOrganizer(source_dir=temp_dir)

    def create_test_file(self, directory: Path, filename: str, old: bool = False) -> Path:
        """Create a test file with optional old timestamp."""
        file_path = directory / filename
        file_path.touch()

        if old:
            # Set file modification time to 400 days ago
            old_time = datetime.now() - timedelta(days=400)
            old_timestamp = old_time.timestamp()
            os.utime(file_path, times=(old_timestamp, old_timestamp))

        return file_path

    def test_init(self, temp_dir):
        """Test FileOrganizer initialization."""
        organizer = FileOrganizer(source_dir=temp_dir)
        assert organizer.source_dir == temp_dir.resolve()
        assert organizer.target_dir == temp_dir.resolve()
        assert not organizer.include_subdirs
        # Check the cutoff is approximately 365 days ago
        expected_cutoff = datetime.now() - timedelta(days=365)
        actual_cutoff = organizer.old_files_cutoff
        # Allow 1 minute difference for test execution time
        assert abs((expected_cutoff - actual_cutoff).total_seconds()) < 60
        assert not organizer.enable_logging

    def test_init_with_target(self, temp_dir):
        """Test FileOrganizer initialization with target directory."""
        target_dir = temp_dir / "target"
        organizer = FileOrganizer(source_dir=temp_dir, target_dir=target_dir)
        assert organizer.source_dir == temp_dir.resolve()
        assert organizer.target_dir == target_dir.resolve()

    def test_get_category(self, organizer):
        """Test file category detection."""
        assert organizer.get_category(Path("test.jpg")) == FileCategory.IMAGES
        assert organizer.get_category(Path("test.pdf")) == FileCategory.DOCUMENTS
        assert organizer.get_category(Path("test.mp3")) == FileCategory.AUDIO
        assert organizer.get_category(Path("test.unknown")) == FileCategory.FILES

    def test_is_old_file(self, temp_dir, organizer):
        """Test old file detection."""
        new_file = self.create_test_file(temp_dir, "new.txt", old=False)
        old_file = self.create_test_file(temp_dir, "old.txt", old=True)

        assert not organizer.is_old_file(new_file)
        assert organizer.is_old_file(old_file)

    def test_check_permissions(self, organizer):
        """Test permission checking."""
        issues = organizer.check_permissions()
        assert len(issues) == 0

    def test_check_permissions_nonexistent(self):
        """Test permission checking with non-existent directory."""
        organizer = FileOrganizer(source_dir="/nonexistent/path")
        issues = organizer.check_permissions()
        assert len(issues) > 0
        assert "does not exist" in issues[0]

    def test_get_files_to_organize(self, temp_dir, organizer):
        """Test file discovery."""
        # Create test files
        self.create_test_file(temp_dir, "test1.txt")
        self.create_test_file(temp_dir, "test2.jpg")

        # Create subdirectory with file
        subdir = temp_dir / "subdir"
        subdir.mkdir()
        self.create_test_file(subdir, "test3.pdf")

        # Test without subdirs
        files = organizer.get_files_to_organize()
        assert len(files) == 2

        # Test with subdirs
        organizer.include_subdirs = True
        files = organizer.get_files_to_organize()
        assert len(files) == 3

    def test_get_target_path(self, temp_dir, organizer):
        """Test target path generation."""
        file_path = Path("test.jpg")

        # Test regular file
        target = organizer.get_target_path(file_path, FileCategory.IMAGES, is_old=False)
        assert target == temp_dir.resolve() / "Images" / "test.jpg"

        # Test old file
        target = organizer.get_target_path(file_path, FileCategory.IMAGES, is_old=True)
        assert "archive_" in str(target)
        assert target.parent.name == "Images"

    def test_get_target_path_conflict(self, temp_dir, organizer):
        """Test target path generation with conflicts."""
        # Create existing file
        images_dir = temp_dir / "Images"
        images_dir.mkdir()
        existing = images_dir / "test.jpg"
        existing.touch()

        file_path = Path("test.jpg")
        target = organizer.get_target_path(file_path, FileCategory.IMAGES, is_old=False)

        assert target == temp_dir.resolve() / "Images" / "test_1.jpg"
        assert len(organizer.conflicts) == 1

    def test_preview(self, temp_dir, organizer):
        """Test preview generation."""
        # Create test files
        self.create_test_file(temp_dir, "image.jpg")
        self.create_test_file(temp_dir, "document.pdf")
        self.create_test_file(temp_dir, "old_file.txt", old=True)

        operations = organizer.preview()

        assert len(operations) > 0
        total_files = sum(len(ops) for ops in operations.values())
        assert total_files == 3

    def test_execute(self, temp_dir, organizer):
        """Test file organization execution."""
        # Create test files
        self.create_test_file(temp_dir, "image.jpg")
        self.create_test_file(temp_dir, "document.pdf")

        result = organizer.execute()

        assert isinstance(result, OrganizeResult)
        assert result.moved_count == 2
        assert result.total_count == 2
        assert len(result.errors) == 0

        # Check files were moved
        assert (temp_dir / "Images" / "image.jpg").exists()
        assert (temp_dir / "Documents" / "document.pdf").exists()
        assert not (temp_dir / "image.jpg").exists()
        assert not (temp_dir / "document.pdf").exists()

    def test_execute_with_errors(self, temp_dir, organizer):
        """Test execution with errors."""
        # Create a file
        self.create_test_file(temp_dir, "test.txt")

        # Create a directory that will cause a conflict
        text_dir = temp_dir / "Text"
        text_dir.mkdir()

        # Try to organize - should handle any errors gracefully
        result = organizer.execute()

        # Even if there are errors, the result should be returned
        assert isinstance(result, OrganizeResult)

    def test_category_extensions_completeness(self):
        """Test that all file categories have extensions defined."""
        for category in FileCategory:
            if category != FileCategory.FILES:  # FILES is the default category
                assert category in CATEGORY_EXTENSIONS
                assert len(CATEGORY_EXTENSIONS[category]) > 0

    def test_extension_map_building(self, organizer):
        """Test extension to category mapping."""
        # Test some known extensions
        assert organizer.ext_to_category.get(".jpg") == FileCategory.IMAGES
        assert organizer.ext_to_category.get(".pdf") == FileCategory.DOCUMENTS
        assert organizer.ext_to_category.get(".mp3") == FileCategory.AUDIO

        # Test case insensitivity through get_category method
        assert organizer.get_category(Path("test.jpg")) == organizer.get_category(Path("test.JPG"))
        assert organizer.get_category(Path("test.PDF")) == FileCategory.DOCUMENTS

    def test_logging_setup(self, temp_dir):
        """Test logging setup."""
        organizer = FileOrganizer(source_dir=temp_dir, enable_logging=True)
        assert organizer.logger is not None

        # Check log file is created after some operation
        organizer.preview()
        log_files = list(temp_dir.glob("tidydir_*.log"))
        assert len(log_files) >= 1

        # Close logging to release file locks
        organizer.close_logging()
