"""Command-line interface for TidyDir."""

import sys
import argparse
from pathlib import Path

from tidydir import __version__
from tidydir.organizer import FileOrganizer


def create_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser."""
    parser = argparse.ArgumentParser(
        prog='tidydir',
        description='Organize files into categories based on their type',
        epilog='Example: tidydir ~/Downloads --preview --subdirs',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        'source',
        help='Source directory to organize'
    )
    
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )
    
    parser.add_argument(
        '-t', '--target', '--target-dir',
        help='Target directory (default: source directory)'
    )
    
    parser.add_argument(
        '-s', '--subdirs', '--include-subdirs',
        action='store_true',
        help='Include subdirectories (default: False)'
    )
    
    parser.add_argument(
        '-d', '--days', '--old-files-days',
        type=int,
        default=365,
        help='Days threshold for old files (default: 365)'
    )
    
    parser.add_argument(
        '-p', '--preview',
        action='store_true',
        help='Preview only, don\'t move files'
    )
    
    parser.add_argument(
        '-l', '--log', '--enable-logging',
        action='store_true',
        help='Enable logging to file'
    )
    
    return parser


def confirm_action(prompt: str = "Proceed? (yes/no): ") -> bool:
    """
    Ask user for confirmation.
    
    Args:
        prompt: The prompt to display
        
    Returns:
        True if user confirms, False otherwise
    """
    while True:
        response = input(prompt).lower().strip()
        if response in ('yes', 'y'):
            return True
        elif response in ('no', 'n'):
            return False
        else:
            print("Please answer 'yes' or 'no'")


def main() -> int:
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Validate source directory
    source_path = Path(args.source)
    if not source_path.exists():
        print(f"❌ Error: Source directory does not exist: {source_path}")
        return 1
    
    if not source_path.is_dir():
        print(f"❌ Error: Source path is not a directory: {source_path}")
        return 1
    
    # Create organizer
    try:
        organizer = FileOrganizer(
            source_dir=args.source,
            target_dir=args.target,
            include_subdirs=args.subdirs,
            old_files_days=args.days,
            enable_logging=args.log
        )
    except Exception as e:
        print(f"❌ Error initializing organizer: {e}")
        return 1
    
    # Check permissions
    issues = organizer.check_permissions()
    if issues:
        print("❌ Permission issues detected:")
        for issue in issues:
            print(f"  - {issue}")
        return 1
    
    # Preview operations
    try:
        operations = organizer.preview()
        organizer.print_preview(operations)
    except Exception as e:
        print(f"❌ Error during preview: {e}")
        return 1
    
    # If no files to organize
    if not operations:
        print("\nNo files to organize.")
        return 0
    
    # If preview mode, exit here
    if args.preview:
        print("\n(Preview mode - no files were moved)")
        return 0
    
    # Confirm action
    if not confirm_action("\nProceed with organization? (yes/no): "):
        print("Operation cancelled")
        return 0
    
    # Execute organization
    try:
        result = organizer.execute()
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation interrupted by user")
        return 130  # Standard exit code for SIGINT
    except Exception as e:
        print(f"\n❌ Error during execution: {e}")
        return 1
    
    # Return appropriate exit code
    return 0 if result.moved_count == result.total_count else 1


if __name__ == '__main__':
    sys.exit(main())
