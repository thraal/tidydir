#!/usr/bin/env python
"""Fix all linting issues in the project."""

import subprocess
import sys

def run_command(cmd: list[str]) -> int:
    """Run a command and return exit code."""
    print(f"Running: {' '.join(cmd)}")
    return subprocess.call(cmd)

def main():
    """Fix all linting issues."""
    print("🔧 Fixing all linting issues...\n")
    
    # First, run black to format everything
    print("1. Running Black formatter...")
    if run_command(["black", "src", "tests"]) != 0:
        print("❌ Black formatting failed")
        return 1
    
    # Then run ruff with fix
    print("\n2. Running Ruff with auto-fix...")
    if run_command(["ruff", "check", "--fix", "src", "tests"]) != 0:
        print("❌ Some Ruff issues couldn't be auto-fixed")
        # Continue anyway
    
    # Check if there are remaining issues
    print("\n3. Checking remaining issues...")
    result = run_command(["ruff", "check", "src", "tests"])
    
    if result == 0:
        print("\n✅ All linting issues fixed!")
    else:
        print("\n⚠️  Some issues remain that need manual fixing")
        print("Run 'ruff check src tests' to see remaining issues")
    
    return result

if __name__ == "__main__":
    sys.exit(main())