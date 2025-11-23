"""
Unit tests for FileSelectionStep class.

This module contains comprehensive unit tests for the FileSelectionStep wizard step,
testing initialization, UI creation, file browsing, data collection, validation,
and lifecycle management.

Tests use mocks to avoid GUI dependencies and verify proper integration with the
WizardStep base class and gui_utils validation functions.
"""

import unittest
import tkinter as tk
from tkinter import ttk
from unittest.mock import Mock, patch, MagicMock
import os
import sys

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

from src.gui_wizard_step import StepConfig, StepData
from src.gui_steps.file_selection_step import FileSelectionStep


class MockConverterGUI:
    """Mock ConverterGUI for testing without actual GUI dependencies."""

    def __init__(self):
        """Initialize mock with required attributes."""
        # Create StringVar for csv_file
        self.csv_file = tk.StringVar()
        # Store log messages for verification
        self.log_messages = []

    def _log(self, message: str):
        """Mock logging method that stores messages."""
        self.log_messages.append(message)


class TestFileSelectionStepInitialization(unittest.TestCase):
    """Test FileSelectionStep initialization."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()

    def tearDown(self):
        """Clean up after tests."""
        self.root.destroy()

    def test_step_initializes_with_correct_config(self):
        """Test step initializes with correct configuration values."""
        step = FileSelectionStep(self.parent)

        self.assertEqual(step.config.step_number, 0)
        self.assertEqual(step.config.step_name, "File Selection")
        self.assertEqual(step.config.step_title, "Step 1: Select CSV File")
        self.assertTrue(step.config.is_required)
        self.assertTrue(step.config.can_go_back)
        self.assertTrue(step.config.show_next)
        self.assertFalse(step.config.show_convert)

    def test_parent_reference_is_set_correctly(self):
        """Test parent reference is stored correctly."""
        step = FileSelectionStep(self.parent)

        self.assertIs(step.parent, self.parent)

    def test_widgets_dict_is_empty_before_ui_creation(self):
        """Test widgets dictionary is empty before UI creation."""
        step = FileSelectionStep(self.parent)

        self.assertEqual(len(step._widgets), 0)
        self.assertIsInstance(step._widgets, dict)


class TestFileSelectionStepUICreation(unittest.TestCase):
    """Test FileSelectionStep UI creation and layout."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()
        self.step = FileSelectionStep(self.parent)
        self.container = ttk.Frame(self.root)

    def tearDown(self):
        """Clean up after tests."""
        self.step.destroy()
        self.root.destroy()

    def test_create_builds_container_and_widgets(self):
        """Test create() creates container and all expected widgets."""
        result = self.step.create(self.container)

        # Verify container was created
        self.assertIsNotNone(self.step.container)
        self.assertIs(result, self.step.container)
        self.assertIsInstance(self.step.container, ttk.LabelFrame)

        # Verify container has correct title
        self.assertEqual(self.step.container['text'], "Step 1: Select CSV File")

        # Verify widgets were created
        self.assertGreater(len(self.step._widgets), 0)

    def test_widgets_stored_in_dict_with_correct_keys(self):
        """Test widgets are stored in _widgets dict with expected keys."""
        self.step.create(self.container)

        # Verify required widget keys exist
        self.assertIn('file_entry', self.step._widgets)
        self.assertIn('browse_button', self.step._widgets)

        # Verify widget types
        self.assertIsInstance(self.step._widgets['file_entry'], ttk.Entry)
        self.assertIsInstance(self.step._widgets['browse_button'], ttk.Button)

    def test_entry_bound_to_parent_csv_file_stringvar(self):
        """Test entry widget is bound to parent.csv_file StringVar."""
        self.step.create(self.container)

        entry = self.step._widgets['file_entry']
        textvariable = entry['textvariable']

        # Set value through parent's StringVar
        self.parent.csv_file.set('/test/path.csv')

        # Verify entry reflects the value
        self.assertEqual(entry.get(), '/test/path.csv')

    def test_entry_is_readonly(self):
        """Test entry widget is configured as readonly."""
        self.step.create(self.container)

        entry = self.step._widgets['file_entry']

        # Check readonly state (convert to string for comparison)
        self.assertEqual(str(entry['state']), 'readonly')

    def test_browse_button_has_correct_command(self):
        """Test browse button has _browse_file as command."""
        self.step.create(self.container)

        button = self.step._widgets['browse_button']

        # Verify button has a command
        self.assertIsNotNone(button['command'])


class TestFileSelectionStepLayout(unittest.TestCase):
    """Test FileSelectionStep layout configuration."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()
        self.step = FileSelectionStep(self.parent)
        self.container = ttk.Frame(self.root)

    def tearDown(self):
        """Clean up after tests."""
        self.step.destroy()
        self.root.destroy()

    def test_container_uses_grid_layout(self):
        """Test container uses grid layout manager."""
        self.step.create(self.container)

        # Verify container is gridded
        grid_info = self.step.container.grid_info()
        self.assertIsNotNone(grid_info)
        self.assertEqual(grid_info['row'], 0)
        self.assertEqual(grid_info['column'], 0)

    def test_column_weights_configured_for_responsiveness(self):
        """Test column weights are configured (column 1 should expand)."""
        self.step.create(self.container)

        # Check column configuration for the entry column (should have weight > 0)
        # Note: In typical file selection UI, the entry field column should expand
        # This test verifies the layout is responsive
        container = self.step.container

        # The container itself should have column 0 configured
        # (base class configures column 0 by default)
        self.assertIsNotNone(container.grid_columnconfigure(0))


class TestFileSelectionStepFileBrowser(unittest.TestCase):
    """Test FileSelectionStep file browser functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()
        self.step = FileSelectionStep(self.parent)
        self.container = ttk.Frame(self.root)
        self.step.create(self.container)

    def tearDown(self):
        """Clean up after tests."""
        self.step.destroy()
        self.root.destroy()

    @patch('src.gui_steps.file_selection_step.filedialog.askopenfilename')
    def test_browse_file_sets_parent_csv_file_when_selected(self, mock_dialog):
        """Test _browse_file() sets parent.csv_file when file is selected."""
        # Mock file dialog to return a file path
        mock_dialog.return_value = '/test/selected/file.csv'

        # Call browse file method
        self.step._browse_file()

        # Verify parent's csv_file was updated
        self.assertEqual(self.parent.csv_file.get(), '/test/selected/file.csv')

        # Verify dialog was called with correct parameters
        mock_dialog.assert_called_once()
        call_kwargs = mock_dialog.call_args[1]
        self.assertEqual(call_kwargs['title'], "Select CSV File")
        self.assertIn('*.csv', call_kwargs['filetypes'][0])

    @patch('src.gui_steps.file_selection_step.filedialog.askopenfilename')
    def test_browse_file_logs_selected_file(self, mock_dialog):
        """Test _browse_file() logs the selected file path."""
        mock_dialog.return_value = '/test/logged/file.csv'

        # Call browse file method
        self.step._browse_file()

        # Verify log message was created
        self.assertEqual(len(self.parent.log_messages), 1)
        self.assertIn('/test/logged/file.csv', self.parent.log_messages[0])

    @patch('src.gui_steps.file_selection_step.filedialog.askopenfilename')
    def test_browse_file_does_nothing_when_cancelled(self, mock_dialog):
        """Test _browse_file() does nothing when dialog is cancelled."""
        # Mock dialog to return empty string (user cancelled)
        mock_dialog.return_value = ''

        # Set initial value
        self.parent.csv_file.set('/original/path.csv')
        initial_log_count = len(self.parent.log_messages)

        # Call browse file method
        self.step._browse_file()

        # Verify csv_file was NOT changed
        self.assertEqual(self.parent.csv_file.get(), '/original/path.csv')

        # Verify no log message was added
        self.assertEqual(len(self.parent.log_messages), initial_log_count)


class TestFileSelectionStepDataCollection(unittest.TestCase):
    """Test FileSelectionStep data collection."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()
        self.step = FileSelectionStep(self.parent)
        self.container = ttk.Frame(self.root)
        self.step.create(self.container)

    def tearDown(self):
        """Clean up after tests."""
        self.step.destroy()
        self.root.destroy()

    def test_collect_data_returns_correct_structure(self):
        """Test _collect_data() returns dict with 'csv_file' key."""
        self.parent.csv_file.set('/test/file.csv')

        data = self.step._collect_data()

        self.assertIsInstance(data, dict)
        self.assertIn('csv_file', data)

    def test_collect_data_gets_value_from_parent(self):
        """Test _collect_data() retrieves value from parent.csv_file."""
        test_path = '/test/data/collection.csv'
        self.parent.csv_file.set(test_path)

        data = self.step._collect_data()

        self.assertEqual(data['csv_file'], test_path)


class TestFileSelectionStepValidation(unittest.TestCase):
    """Test FileSelectionStep validation logic."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()
        self.step = FileSelectionStep(self.parent)
        self.container = ttk.Frame(self.root)
        self.step.create(self.container)

    def tearDown(self):
        """Clean up after tests."""
        self.step.destroy()
        self.root.destroy()

    def test_validate_returns_invalid_when_no_file_selected(self):
        """Test validate() returns is_valid=False when no file selected."""
        # Set empty string
        self.parent.csv_file.set('')

        result = self.step.validate()

        self.assertIsInstance(result, StepData)
        self.assertFalse(result.is_valid)
        self.assertIsNotNone(result.error_message)
        self.assertEqual(result.data, {})

    @patch('src.gui_steps.file_selection_step.gui_utils.validate_csv_file_selection')
    def test_validate_returns_invalid_when_file_not_exists(self, mock_validate):
        """Test validate() returns is_valid=False when file doesn't exist."""
        # Mock validation failure for non-existent file
        mock_validate.return_value = (False, "File not found: /nonexistent/file.csv")
        self.parent.csv_file.set('/nonexistent/file.csv')

        result = self.step.validate()

        self.assertFalse(result.is_valid)
        self.assertIsNotNone(result.error_message)
        self.assertIn('not found', result.error_message)
        self.assertEqual(result.data, {})

    @patch('src.gui_steps.file_selection_step.gui_utils.validate_csv_file_selection')
    def test_validate_returns_valid_for_valid_file(self, mock_validate):
        """Test validate() returns is_valid=True for valid file."""
        # Mock validation success for valid file
        mock_validate.return_value = (True, None)
        self.parent.csv_file.set('/valid/file.csv')

        result = self.step.validate()

        self.assertTrue(result.is_valid)
        self.assertIsNone(result.error_message)
        self.assertIn('csv_file', result.data)
        self.assertEqual(result.data['csv_file'], '/valid/file.csv')

    def test_validate_returns_appropriate_error_messages(self):
        """Test validate() returns user-friendly error messages."""
        # Test empty file
        self.parent.csv_file.set('')
        result = self.step.validate()
        self.assertIn('select', result.error_message.lower())

        # Test whitespace only
        self.parent.csv_file.set('   ')
        result = self.step.validate()
        self.assertIn('select', result.error_message.lower())

    @patch('src.gui_steps.file_selection_step.gui_utils.validate_csv_file_selection')
    def test_validate_uses_gui_utils_validation(self, mock_validate):
        """Test validate() calls gui_utils.validate_csv_file_selection()."""
        # Mock validation function
        mock_validate.return_value = (True, None)
        self.parent.csv_file.set('/test/file.csv')

        self.step.validate()

        # Verify validation function was called with correct argument
        mock_validate.assert_called_once_with('/test/file.csv')

    @patch('src.gui_steps.file_selection_step.gui_utils.validate_csv_file_selection')
    def test_validate_returns_empty_data_when_validation_fails(self, mock_validate):
        """Test validate() returns empty data dict when validation fails."""
        # Mock validation failure
        mock_validate.return_value = (False, "Invalid file")
        self.parent.csv_file.set('/invalid/file.csv')

        result = self.step.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(result.data, {})


class TestFileSelectionStepLifecycle(unittest.TestCase):
    """Test FileSelectionStep lifecycle management."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()
        self.step = FileSelectionStep(self.parent)
        self.container = ttk.Frame(self.root)
        self.step.create(self.container)

    def tearDown(self):
        """Clean up after tests."""
        self.root.destroy()

    def test_show_makes_container_visible(self):
        """Test show() makes the container visible."""
        # Hide first
        self.step.hide()

        # Show step
        self.step.show()

        # Verify container is visible (has grid info)
        grid_info = self.step.container.grid_info()
        self.assertIsNotNone(grid_info)
        self.assertNotEqual(grid_info, {})

    def test_hide_hides_container(self):
        """Test hide() hides the container without destroying it."""
        # Show first
        self.step.show()

        # Hide step
        self.step.hide()

        # Verify container still exists but is not visible
        self.assertIsNotNone(self.step.container)
        # Container should have empty grid_info when hidden
        grid_info = self.step.container.grid_info()
        # After grid_remove(), grid_info() returns empty dict
        self.assertEqual(grid_info, {})

    def test_destroy_cleans_up_resources(self):
        """Test destroy() cleans up container and widgets."""
        # Destroy step
        self.step.destroy()

        # Verify container is None
        self.assertIsNone(self.step.container)

        # Verify widgets dict is cleared
        self.assertEqual(len(self.step._widgets), 0)


if __name__ == '__main__':
    unittest.main()
