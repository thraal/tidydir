"""Core file organization functionality."""

from __future__ import annotations

import os
import shutil
import logging
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import DefaultDict, Optional
from collections import defaultdict

from tidydir.categories import FileCategory, CATEGORY_EXTENSIONS


@dataclass
class FileOperation:
    """Represents a file operation to be performed."""

    source: Path
    target: Path
    category: FileCategory
    is_old: bool


@dataclass
class OrganizeResult:
    """Result of file organization operation."""

    moved_count: int
    total_count: int
    errors: list[tuple[Path, str]] = field(default_factory=list)
    conflicts: list[tuple[Path, Path]] = field(default_factory=list)


class FileOrganizer:
    """Main class for organizing files into categories."""

    def __init__(
        self,
        source_dir: str | Path,
        target_dir: Optional[str | Path] = None,
        include_subdirs: bool = False,
        old_files_days: int = 365,
        enable_logging: bool = False,
    ) -> None:
        """
        Initialize the FileOrganizer.

        Args:
            source_dir: Source directory to organize
            target_dir: Target directory (defaults to source_dir)
            include_subdirs: Whether to include subdirectories
            old_files_days: Age threshold for old files in days
            enable_logging: Whether to enable logging to file
        """
        self.source_dir = Path(source_dir).resolve()
        self.target_dir = Path(target_dir).resolve() if target_dir else self.source_dir
        self.include_subdirs = include_subdirs
        self.old_files_cutoff = datetime.now() - timedelta(days=old_files_days)
        self.enable_logging = enable_logging

        # Create extension to category mapping
        self.ext_to_category = self._build_extension_map()

        # Track operations
        self.conflicts: list[tuple[Path, Path]] = []
        self.errors: list[tuple[Path, str]] = []

        # Setup logging if enabled
        self.logger: Optional[logging.Logger] = self._setup_logging() if enable_logging else None

    def __del__(self) -> None:
        """Cleanup when object is deleted."""
        self.close_logging()

    def _build_extension_map(self) -> dict[str, FileCategory]:
        """Build a mapping from file extensions to categories."""
        ext_map: dict[str, FileCategory] = {}
        for category, extensions in CATEGORY_EXTENSIONS.items():
            for ext in extensions:
                ext_map[ext.lower()] = category
        return ext_map

    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration."""
        log_filename = f'tidydir_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        log_file = self.target_dir / log_filename

        # Ensure target directory exists
        self.target_dir.mkdir(parents=True, exist_ok=True)

        # Create a unique logger for this instance
        logger_name = f"tidydir.{id(self)}"
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)

        # Clear any existing handlers
        logger.handlers.clear()

        # Create formatters and handlers
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        file_handler = logging.FileHandler(log_file, mode="a")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # Log initial message to ensure file is created
        logger.info(f"TidyDir logging started for {self.source_dir}")

        return logger

    def close_logging(self) -> None:
        """Close all logging handlers to release file locks."""
        if self.logger:
            for handler in self.logger.handlers[:]:
                handler.close()
                self.logger.removeHandler(handler)

    def get_category(self, file_path: Path) -> FileCategory:
        """
        Determine the category for a file based on its extension.

        Args:
            file_path: Path to the file

        Returns:
            The file category
        """
        ext = file_path.suffix.lower()
        return self.ext_to_category.get(ext, FileCategory.FILES)

    def is_old_file(self, file_path: Path) -> bool:
        """
        Check if file is older than the cutoff date.

        Args:
            file_path: Path to the file

        Returns:
            True if file is older than cutoff
        """
        try:
            mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
            return mtime < self.old_files_cutoff
        except OSError:
            # If we can't read the file stats, consider it not old
            return False

    def check_permissions(self) -> list[str]:
        """
        Check read/write permissions for source and target directories.

        Returns:
            List of permission issues
        """
        issues: list[str] = []

        # Check source directory
        if not self.source_dir.exists():
            issues.append(f"Source directory does not exist: {self.source_dir}")
        elif not os.access(self.source_dir, os.R_OK):
            issues.append(f"No read permission for source: {self.source_dir}")

        # Check target directory
        if self.target_dir.exists():
            if not os.access(self.target_dir, os.W_OK):
                issues.append(f"No write permission for target: {self.target_dir}")
        else:
            parent = self.target_dir.parent
            if not os.access(parent, os.W_OK):
                issues.append(f"No write permission to create target: {self.target_dir}")

        return issues

    def get_files_to_organize(self) -> list[Path]:
        """
        Get list of files to organize.

        Returns:
            List of file paths to organize
        """
        files: list[Path] = []

        try:
            if self.include_subdirs:
                files = [item for item in self.source_dir.rglob("*") if item.is_file()]
            else:
                files = [item for item in self.source_dir.iterdir() if item.is_file()]
        except OSError as e:
            if self.logger:
                self.logger.error(f"Error reading directory: {e}")

        return files

    def get_target_path(self, file_path: Path, category: FileCategory, is_old: bool) -> Path:
        """
        Determine the target path for a file.

        Args:
            file_path: Source file path
            category: File category
            is_old: Whether the file is old

        Returns:
            Target path for the file
        """
        if is_old:
            archive_dir = f"archive_{datetime.now().strftime('%Y%m%d')}"
            base_dir = self.target_dir / archive_dir / category.value
        else:
            base_dir = self.target_dir / category.value

        target_path = base_dir / file_path.name

        # Handle conflicts
        if target_path.exists():
            stem = file_path.stem
            suffix = file_path.suffix
            counter = 1
            while target_path.exists():
                target_path = base_dir / f"{stem}_{counter}{suffix}"
                counter += 1
            self.conflicts.append((file_path, target_path))

        return target_path

    def preview(self) -> DefaultDict[str, list[FileOperation]]:
        """
        Generate preview of operations without executing them.

        Returns:
            Dictionary mapping target directories to file operations
        """
        files = self.get_files_to_organize()
        operations: DefaultDict[str, list[FileOperation]] = defaultdict(list)

        # Reset conflicts for new preview
        self.conflicts.clear()

        for file_path in files:
            category = self.get_category(file_path)
            is_old = self.is_old_file(file_path)
            target_path = self.get_target_path(file_path, category, is_old)

            operation = FileOperation(
                source=file_path, target=target_path, category=category, is_old=is_old
            )

            operations[str(target_path.parent)].append(operation)

        return operations

    def print_preview(self, operations: DefaultDict[str, list[FileOperation]]) -> None:
        """
        Print preview in tree format.

        Args:
            operations: Dictionary of operations to preview
        """
        print("\n=== PREVIEW ===\n")

        if not operations:
            print("No files to organize.")
            return

        # Organize by directory structure
        tree: DefaultDict[FileCategory, list[FileOperation]] = defaultdict(list)
        archive_tree: DefaultDict[FileCategory, list[FileOperation]] = defaultdict(list)

        for parent_dir, file_ops in operations.items():
            parent_path = Path(parent_dir)
            # Check if it's in an archive directory
            if any("archive_" in part for part in parent_path.parts):
                try:
                    category = FileCategory(parent_path.name)
                    archive_tree[category].extend(file_ops)
                except ValueError:
                    # If the directory name doesn't match a category, skip it
                    continue
            else:
                try:
                    category = FileCategory(parent_path.name)
                    tree[category].extend(file_ops)
                except ValueError:
                    # If the directory name doesn't match a category, skip it
                    continue

        # Print main target directory structure
        print(f"📁 {self.target_dir.name}/")

        # Print regular categories
        for category, file_ops in sorted(tree.items()):
            print(f"├── 📁 {category.value}/")
            for file_op in file_ops[:3]:  # Show first 3 files
                print(f"│   └── 📄 {file_op.source.name}")
            if len(file_ops) > 3:
                print(f"│   └── ... and {len(file_ops) - 3} more files")

        # Print archive directory if there are old files
        if archive_tree:
            archive_name = f"archive_{datetime.now().strftime('%Y%m%d')}"
            print(f"└── 📁 {archive_name}/")
            for category, file_ops in sorted(archive_tree.items()):
                print(f"    ├── 📁 {category.value}/")
                for file_op in file_ops[:3]:  # Show first 3 files
                    print(f"    │   └── 📄 {file_op.source.name}")
                if len(file_ops) > 3:
                    print(f"    │   └── ... and {len(file_ops) - 3} more files")

        # Print summary
        print("\n=== SUMMARY ===")
        total_files = sum(len(file_ops) for file_ops in operations.values())
        print(f"Total files to organize: {total_files}")

        # Category breakdown
        category_counts: DefaultDict[FileCategory, int] = defaultdict(int)
        old_files_count = 0
        for file_ops in operations.values():
            for file_op in file_ops:
                category_counts[file_op.category] += 1
                if file_op.is_old:
                    old_files_count += 1

        print("\nFiles by category:")
        for category, count in sorted(category_counts.items()):
            print(f"  {category.value}: {count}")

        # Calculate days threshold from cutoff
        days_threshold = (datetime.now() - self.old_files_cutoff).days
        print(f"\nOld files (>{days_threshold} days): {old_files_count}")

        if self.conflicts:
            print(f"\n⚠️  Conflicts detected: {len(self.conflicts)} files will be renamed")
            for source, target in self.conflicts[:5]:
                print(f"  {source.name} → {target.name}")
            if len(self.conflicts) > 5:
                print(f"  ... and {len(self.conflicts) - 5} more")

    def execute(self) -> OrganizeResult:
        """
        Execute the file organization.

        Returns:
            Result of the organization operation
        """
        operations = self.preview()

        if not operations:
            return OrganizeResult(moved_count=0, total_count=0)

        # Create directories
        for parent_dir in operations:
            Path(parent_dir).mkdir(parents=True, exist_ok=True)

        # Move files
        total = sum(len(file_ops) for file_ops in operations.values())
        moved = 0

        # Reset errors for new execution
        self.errors.clear()

        print(f"\nMoving {total} files...")

        for file_ops in operations.values():
            for file_op in file_ops:
                try:
                    shutil.move(str(file_op.source), str(file_op.target))
                    moved += 1

                    if self.logger:
                        self.logger.info(f"Moved: {file_op.source} → {file_op.target}")

                    if moved % 50 == 0:
                        print(f"Progress: {moved}/{total} files moved")

                except Exception as e:
                    self.errors.append((file_op.source, str(e)))
                    if self.logger:
                        self.logger.error(f"Failed to move {file_op.source}: {e}")

        print(f"\n✅ Completed: {moved}/{total} files organized")

        if self.errors:
            print(f"\n❌ Errors: {len(self.errors)} files failed")
            for file_path, error in self.errors[:5]:
                print(f"  {file_path.name}: {error}")
            if len(self.errors) > 5:
                print(f"  ... and {len(self.errors) - 5} more")

        return OrganizeResult(
            moved_count=moved, total_count=total, errors=self.errors, conflicts=self.conflicts
        )
