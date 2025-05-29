#!/usr/bin/env python
"""Run code quality checks without pre-commit."""

import subprocess
import sys
from pathlib import Path

def run_command(cmd: list[str], description: str) -> bool:
    """Run a command and return success status."""
    print(f"\n🔍 {description}...")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} passed")
            return True
        else:
            print(f"❌ {description} failed")
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error running {description}: {e}")
        return False

def main():
    """Run all code quality checks."""
    # Find project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    # Change to project root
    import os
    os.chdir(project_root)
    
    checks = [
        (["black", "--check", "src", "tests"], "Black formatting check"),
        (["ruff", "check", "src", "tests"], "Ruff linting"),
        (["mypy", "src"], "MyPy type checking"),
        (["pytest", "--no-cov", "-q"], "Quick test run"),
    ]
    
    all_passed = True
    for cmd, description in checks:
        if not run_command(cmd, description):
            all_passed = False
    
    if all_passed:
        print("\n✅ All checks passed!")
        return 0
    else:
        print("\n❌ Some checks failed. Run 'make format' to fix formatting issues.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
