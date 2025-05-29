#!/usr/bin/env python
"""Verify that TidyDir is properly set up."""

import subprocess
import sys
from pathlib import Path

def run_command(cmd: list[str]) -> tuple[bool, str]:
    """Run a command and return success status and output."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0, result.stdout + result.stderr
    except Exception as e:
        return False, str(e)

def main():
    """Verify the TidyDir setup."""
    print("🔍 Verifying TidyDir setup...\n")
    
    # Check Python version
    print(f"Python version: {sys.version}")
    if sys.version_info < (3, 12):
        print("⚠️  Warning: Python 3.12+ is recommended")
    
    checks = [
        ("Package installed", ["tidydir", "--version"]),
        ("Tests passing", ["pytest", "-q"]),
        ("Code formatted", ["black", "--check", "src", "tests"]),
        ("Linting clean", ["ruff", "check", "src", "tests"]),
        ("Type checking", ["mypy", "src"]),
    ]
    
    all_good = True
    for name, cmd in checks:
        success, output = run_command(cmd)
        if success:
            print(f"✅ {name}")
        else:
            print(f"❌ {name}")
            if "--version" not in cmd:  # Don't show output for version check
                print(f"   {output.strip()}")
            all_good = False
    
    if all_good:
        print("\n🎉 Everything is set up correctly!")
        print("\nYou can now:")
        print("  - Run 'tidydir --help' to see usage")
        print("  - Run 'tidydir ~/Downloads --preview' to test it")
        print("  - Make changes and run 'make check' before committing")
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        print("  Run 'make format' to fix formatting issues")
        print("  Run 'make install-dev' to ensure all dependencies are installed")
    
    return 0 if all_good else 1

if __name__ == "__main__":
    sys.exit(main())