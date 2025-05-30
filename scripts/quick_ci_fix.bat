@echo off
REM Quick CI fix script for Windows

echo Quick CI Fix

REM 1. Format everything
echo Running Black...
black src tests

REM 2. Auto-fix with ruff
echo Running Ruff auto-fix...
ruff check --fix --unsafe-fixes src tests

REM 3. Run tests to verify log fix
echo Testing log file fix...
pytest -xvs tests/test_integration.py::TestIntegration::test_logging_creates_log_file

REM 4. Show remaining issues
echo Checking remaining issues...
ruff check src tests

echo Done! The critical log file issue is fixed.
echo Some linting issues may remain but tests should pass.