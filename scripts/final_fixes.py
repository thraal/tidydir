#!/usr/bin/env python
"""Apply final fixes for CI."""

import subprocess
import sys

def main():
    """Apply final fixes."""
    print("🔧 Applying final fixes...\n")
    
    # 1. Run black to format
    print("1. Running Black formatter...")
    subprocess.run(["black", "src", "tests"])
    
    # 2. Check for any remaining issues
    print("\n2. Checking for remaining issues...")
    result = subprocess.run(["ruff", "check", "src", "tests"], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ No linting issues found!")
    else:
        print("Output:", result.stdout)
        if "pyproject.toml" in result.stdout:
            print("\n⚠️  Note: The pyproject.toml warning about deprecated settings can be ignored")
            print("    or fixed by updating the [tool.ruff] section in pyproject.toml")
    
    # 3. Run all tests
    print("\n3. Running all tests...")
    test_result = subprocess.run(["pytest", "-v"])
    
    if test_result.returncode == 0:
        print("\n✅ All tests passing!")
        print("\n🎉 Ready to commit and push!")
        print("\nRun:")
        print("  git add -A")
        print("  git commit -m 'Fix: Exclude log files and fix all linting issues'")
        print("  git push origin main")
    else:
        print("\n❌ Some tests failed")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())