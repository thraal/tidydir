"""Tests for the CLI module."""

from unittest.mock import MagicMock, patch

import pytest

from tidydir.cli import confirm_action, create_parser, main


class TestCLI:
    """Test suite for CLI functionality."""

    def test_create_parser(self):
        """Test argument parser creation."""
        parser = create_parser()

        # Test help
        with pytest.raises(SystemExit):
            parser.parse_args(["--help"])

        # Test basic usage
        args = parser.parse_args(["test_dir"])
        assert args.source == "test_dir"
        assert args.target is None
        assert not args.subdirs
        assert args.days == 365
        assert not args.preview
        assert not args.log

    def test_parser_all_options(self):
        """Test parser with all options."""
        parser = create_parser()
        args = parser.parse_args(
            [
                "source_dir",
                "--target",
                "target_dir",
                "--subdirs",
                "--days",
                "30",
                "--preview",
                "--log",
            ]
        )

        assert args.source == "source_dir"
        assert args.target == "target_dir"
        assert args.subdirs
        assert args.days == 30
        assert args.preview
        assert args.log

    def test_parser_version(self):
        """Test version flag."""
        parser = create_parser()
        with pytest.raises(SystemExit):
            parser.parse_args(["--version"])

    @patch("builtins.input")
    def test_confirm_action_yes(self, mock_input):
        """Test confirm action with yes response."""
        mock_input.return_value = "yes"
        assert confirm_action() is True

        mock_input.return_value = "y"
        assert confirm_action() is True

    @patch("builtins.input")
    def test_confirm_action_no(self, mock_input):
        """Test confirm action with no response."""
        mock_input.return_value = "no"
        assert confirm_action() is False

        mock_input.return_value = "n"
        assert confirm_action() is False

    @patch("builtins.input")
    def test_confirm_action_invalid_then_yes(self, mock_input):
        """Test confirm action with invalid then yes response."""
        mock_input.side_effect = ["invalid", "yes"]
        assert confirm_action() is True
        assert mock_input.call_count == 2

    @patch("tidydir.cli.Path")
    def test_main_source_not_exist(self, mock_path):
        """Test main with non-existent source."""
        mock_path.return_value.exists.return_value = False

        with patch("sys.argv", ["tidydir", "nonexistent"]):
            result = main()
            assert result == 1

    @patch("tidydir.cli.Path")
    def test_main_source_not_directory(self, mock_path):
        """Test main with source that's not a directory."""
        mock_path.return_value.exists.return_value = True
        mock_path.return_value.is_dir.return_value = False

        with patch("sys.argv", ["tidydir", "file.txt"]):
            result = main()
            assert result == 1

    @patch("tidydir.cli.FileOrganizer")
    @patch("tidydir.cli.Path")
    def test_main_preview_mode(self, mock_path, mock_organizer):
        """Test main in preview mode."""
        # Setup mocks
        mock_path.return_value.exists.return_value = True
        mock_path.return_value.is_dir.return_value = True

        mock_org_instance = MagicMock()
        mock_org_instance.check_permissions.return_value = []
        mock_org_instance.preview.return_value = {"test": []}
        mock_organizer.return_value = mock_org_instance

        with patch("sys.argv", ["tidydir", "test_dir", "--preview"]):
            result = main()
            assert result == 0
            mock_org_instance.execute.assert_not_called()

    @patch("tidydir.cli.confirm_action")
    @patch("tidydir.cli.FileOrganizer")
    @patch("tidydir.cli.Path")
    def test_main_cancelled(self, mock_path, mock_organizer, mock_confirm):
        """Test main when user cancels."""
        # Setup mocks
        mock_path.return_value.exists.return_value = True
        mock_path.return_value.is_dir.return_value = True

        mock_org_instance = MagicMock()
        mock_org_instance.check_permissions.return_value = []
        mock_org_instance.preview.return_value = {"test": [{"source": "file.txt"}]}
        mock_organizer.return_value = mock_org_instance

        mock_confirm.return_value = False

        with patch("sys.argv", ["tidydir", "test_dir"]):
            result = main()
            assert result == 0
            mock_org_instance.execute.assert_not_called()

    @patch("tidydir.cli.confirm_action")
    @patch("tidydir.cli.FileOrganizer")
    @patch("tidydir.cli.Path")
    def test_main_execute_success(self, mock_path, mock_organizer, mock_confirm):
        """Test successful execution."""
        # Setup mocks
        mock_path.return_value.exists.return_value = True
        mock_path.return_value.is_dir.return_value = True

        mock_result = MagicMock()
        mock_result.moved_count = 5
        mock_result.total_count = 5

        mock_org_instance = MagicMock()
        mock_org_instance.check_permissions.return_value = []
        mock_org_instance.preview.return_value = {"test": [{"source": "file.txt"}]}
        mock_org_instance.execute.return_value = mock_result
        mock_organizer.return_value = mock_org_instance

        mock_confirm.return_value = True

        with patch("sys.argv", ["tidydir", "test_dir"]):
            result = main()
            assert result == 0
            mock_org_instance.execute.assert_called_once()

    @patch("tidydir.cli.confirm_action")
    @patch("tidydir.cli.FileOrganizer")
    @patch("tidydir.cli.Path")
    def test_main_execute_with_errors(self, mock_path, mock_organizer, mock_confirm):
        """Test execution with some errors."""
        # Setup mocks
        mock_path.return_value.exists.return_value = True
        mock_path.return_value.is_dir.return_value = True

        mock_result = MagicMock()
        mock_result.moved_count = 3
        mock_result.total_count = 5

        mock_org_instance = MagicMock()
        mock_org_instance.check_permissions.return_value = []
        mock_org_instance.preview.return_value = {"test": [{"source": "file.txt"}]}
        mock_org_instance.execute.return_value = mock_result
        mock_organizer.return_value = mock_org_instance

        mock_confirm.return_value = True

        with patch("sys.argv", ["tidydir", "test_dir"]):
            result = main()
            assert result == 1  # Exit code 1 for errors

    @patch("tidydir.cli.FileOrganizer")
    @patch("tidydir.cli.Path")
    def test_main_permission_issues(self, mock_path, mock_organizer):
        """Test main with permission issues."""
        # Setup mocks
        mock_path.return_value.exists.return_value = True
        mock_path.return_value.is_dir.return_value = True

        mock_org_instance = MagicMock()
        mock_org_instance.check_permissions.return_value = ["No write permission"]
        mock_organizer.return_value = mock_org_instance

        with patch("sys.argv", ["tidydir", "test_dir"]):
            result = main()
            assert result == 1
            mock_org_instance.preview.assert_not_called()
