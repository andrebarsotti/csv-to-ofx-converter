"""
Unit tests for DataPreviewStep class.

This module contains comprehensive unit tests for the DataPreviewStep wizard step,
testing initialization, UI creation, CSV loading, data population, validation,
and lifecycle management.

Tests use mocks to avoid GUI dependencies and verify proper integration with the
WizardStep base class, CSVParser, and gui_utils validation functions.
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
from src.gui_steps.data_preview_step import DataPreviewStep


class MockConverterGUI:
    """Mock ConverterGUI for testing without actual GUI dependencies."""

    def __init__(self):
        """Initialize mock with required attributes."""
        # Create StringVars for file and format
        self.csv_file = tk.StringVar()
        self.delimiter = tk.StringVar(value=',')
        self.decimal_separator = tk.StringVar(value='.')

        # CSV data attributes (not StringVars)
        self.csv_headers = []
        self.csv_data = []

        # Current step tracking
        self.current_step = 0

        # Widgets that will be set by DataPreviewStep
        self.preview_tree = None
        self.preview_stats_label = None

        # Store log messages for verification
        self.log_messages = []

    def _log(self, message: str):
        """Mock logging method that stores messages."""
        self.log_messages.append(message)


class TestDataPreviewStepInitialization(unittest.TestCase):
    """Test DataPreviewStep initialization."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()

    def tearDown(self):
        """Clean up after tests."""
        self.root.destroy()

    def test_step_initializes_with_correct_config(self):
        """Test step initializes with correct configuration values."""
        step = DataPreviewStep(self.parent)

        self.assertEqual(step.config.step_number, 2)
        self.assertEqual(step.config.step_name, "Data Preview")
        self.assertEqual(step.config.step_title, "Step 3: Preview CSV Data")
        self.assertTrue(step.config.is_required)
        self.assertTrue(step.config.can_go_back)
        self.assertTrue(step.config.show_next)
        self.assertFalse(step.config.show_convert)

    def test_step_number_is_two(self):
        """Test step_number is 2 (Step 3 is index 2)."""
        step = DataPreviewStep(self.parent)

        self.assertEqual(step.config.step_number, 2)

    def test_step_name_is_data_preview(self):
        """Test step_name is 'Data Preview'."""
        step = DataPreviewStep(self.parent)

        self.assertEqual(step.config.step_name, "Data Preview")

    def test_parent_reference_is_set_correctly(self):
        """Test parent reference is stored correctly."""
        step = DataPreviewStep(self.parent)

        self.assertIs(step.parent, self.parent)

    def test_widgets_dict_is_empty_before_ui_creation(self):
        """Test widgets dictionary is empty before UI creation."""
        step = DataPreviewStep(self.parent)

        self.assertEqual(len(step._widgets), 0)
        self.assertIsInstance(step._widgets, dict)

    def test_reload_requested_flag_initialized_false(self):
        """Test _reload_requested flag is initialized to False."""
        step = DataPreviewStep(self.parent)

        self.assertFalse(step._reload_requested)


class TestDataPreviewStepUICreation(unittest.TestCase):
    """Test DataPreviewStep UI creation and widget creation."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()
        self.step = DataPreviewStep(self.parent)
        self.container = ttk.Frame(self.root)

    def tearDown(self):
        """Clean up after tests."""
        self.step.destroy()
        self.root.destroy()

    def test_create_builds_container(self):
        """Test create() creates container successfully."""
        result = self.step.create(self.container)

        # Verify container was created
        self.assertIsNotNone(self.step.container)
        self.assertIs(result, self.step.container)
        self.assertIsInstance(self.step.container, ttk.LabelFrame)

        # Verify container has correct title
        self.assertEqual(self.step.container['text'], "Step 3: Preview CSV Data")

    def test_treeview_widget_created(self):
        """Test Treeview widget is created for data preview."""
        self.step.create(self.container)

        # Verify preview_tree is stored in widgets dict
        self.assertIn('preview_tree', self.step._widgets)

        # Verify widget type
        self.assertIsInstance(self.step._widgets['preview_tree'], ttk.Treeview)

    def test_vertical_scrollbar_created(self):
        """Test vertical scrollbar is created for Treeview."""
        self.step.create(self.container)

        # Find the tree frame and verify scrollbar exists
        tree = self.step._widgets['preview_tree']
        parent_frame = tree.master

        # Find scrollbar among siblings
        scrollbars = [child for child in parent_frame.winfo_children()
                     if isinstance(child, ttk.Scrollbar)]

        # Should have vertical scrollbar
        vertical_scrollbars = [sb for sb in scrollbars
                               if str(sb['orient']) == 'vertical']
        self.assertEqual(len(vertical_scrollbars), 1)

    def test_horizontal_scrollbar_created(self):
        """Test horizontal scrollbar is created for Treeview."""
        self.step.create(self.container)

        # Find the tree frame and verify scrollbar exists
        tree = self.step._widgets['preview_tree']
        parent_frame = tree.master

        # Find scrollbar among siblings
        scrollbars = [child for child in parent_frame.winfo_children()
                     if isinstance(child, ttk.Scrollbar)]

        # Should have horizontal scrollbar
        horizontal_scrollbars = [sb for sb in scrollbars
                                if str(sb['orient']) == 'horizontal']
        self.assertEqual(len(horizontal_scrollbars), 1)

    def test_reload_button_created(self):
        """Test reload button is created."""
        self.step.create(self.container)

        # Find reload button by searching for buttons with 'Reload' text
        container_children = self.step.container.winfo_children()

        # Find the info frame (first frame)
        info_frame = None
        for child in container_children:
            if isinstance(child, ttk.Frame):
                info_frame = child
                break

        self.assertIsNotNone(info_frame)

        # Find button in info frame
        buttons = [child for child in info_frame.winfo_children()
                  if isinstance(child, ttk.Button)]

        self.assertEqual(len(buttons), 1)
        self.assertIn('Reload', buttons[0]['text'])

    def test_stats_label_created(self):
        """Test statistics label is created."""
        self.step.create(self.container)

        # Verify stats_label is stored in widgets dict
        self.assertIn('stats_label', self.step._widgets)

        # Verify widget type
        self.assertIsInstance(self.step._widgets['stats_label'], ttk.Label)

    def test_preview_tree_set_on_parent(self):
        """Test preview_tree is set on parent for compatibility."""
        self.step.create(self.container)

        # Verify parent has preview_tree attribute
        self.assertIsNotNone(self.parent.preview_tree)
        self.assertIs(self.parent.preview_tree, self.step._widgets['preview_tree'])

    def test_stats_label_set_on_parent(self):
        """Test preview_stats_label is set on parent for compatibility."""
        self.step.create(self.container)

        # Verify parent has preview_stats_label attribute
        self.assertIsNotNone(self.parent.preview_stats_label)
        self.assertIs(self.parent.preview_stats_label, self.step._widgets['stats_label'])


class TestDataPreviewStepLayout(unittest.TestCase):
    """Test DataPreviewStep layout configuration."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()
        self.step = DataPreviewStep(self.parent)
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

    def test_container_configured_for_responsive_layout(self):
        """Test container is configured with proper weights for responsive layout."""
        self.step.create(self.container)

        # Verify column 0 has weight (should expand)
        self.assertIsNotNone(self.step.container.grid_columnconfigure(0))

        # Verify row 1 has weight (tree should expand vertically)
        self.assertIsNotNone(self.step.container.grid_rowconfigure(1))


class TestDataPreviewStepCSVLoading(unittest.TestCase):
    """Test DataPreviewStep CSV data loading functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()
        self.step = DataPreviewStep(self.parent)
        self.container = ttk.Frame(self.root)
        self.step.create(self.container)

    def tearDown(self):
        """Clean up after tests."""
        self.step.destroy()
        self.root.destroy()

    @patch('src.gui_steps.data_preview_step.CSVParser')
    @patch('src.gui_steps.data_preview_step.gui_utils.format_preview_stats')
    def test_load_csv_data_success(self, mock_format_stats, mock_parser_class):
        """Test successful CSV data loading."""
        # Mock CSV parser
        mock_parser = Mock()
        mock_parser.parse_file.return_value = (
            ['Date', 'Description', 'Amount'],
            [
                {'Date': '2025-01-01', 'Description': 'Test 1', 'Amount': '100.00'},
                {'Date': '2025-01-02', 'Description': 'Test 2', 'Amount': '200.00'}
            ]
        )
        mock_parser_class.return_value = mock_parser
        mock_format_stats.return_value = "Showing 2 of 2 rows"

        # Set CSV file path
        self.parent.csv_file.set('/test/file.csv')

        # Load CSV data
        self.step._load_csv_data()

        # Verify parser was created with correct format
        mock_parser_class.assert_called_once_with(delimiter=',', decimal_separator='.')

        # Verify parse_file was called
        mock_parser.parse_file.assert_called_once_with('/test/file.csv')

        # Verify data was stored in parent
        self.assertEqual(len(self.parent.csv_headers), 3)
        self.assertEqual(len(self.parent.csv_data), 2)
        self.assertEqual(self.parent.csv_headers, ['Date', 'Description', 'Amount'])

    @patch('src.gui_steps.data_preview_step.CSVParser')
    @patch('src.gui_steps.data_preview_step.gui_utils.format_preview_stats')
    def test_load_csv_data_with_force_reload(self, mock_format_stats, mock_parser_class):
        """Test CSV loading with force_reload=True."""
        # Setup initial data
        self.parent.csv_headers = ['Old']
        self.parent.csv_data = [{'Old': 'data'}]

        # Mock CSV parser
        mock_parser = Mock()
        mock_parser.parse_file.return_value = (
            ['New', 'Headers'],
            [{'New': 'data1', 'Headers': 'data2'}]
        )
        mock_parser_class.return_value = mock_parser
        mock_format_stats.return_value = "Showing 1 of 1 rows"

        # Set CSV file path
        self.parent.csv_file.set('/test/file.csv')

        # Load with force_reload
        self.step._load_csv_data(force_reload=True)

        # Verify new data was loaded
        self.assertEqual(self.parent.csv_headers, ['New', 'Headers'])
        self.assertEqual(len(self.parent.csv_data), 1)

    def test_load_csv_data_raises_when_no_file_selected(self):
        """Test load_csv_data raises ValueError when no file is selected."""
        # Don't set csv_file (empty by default)

        # Verify exception is raised
        with self.assertRaises(ValueError) as context:
            self.step._load_csv_data()

        self.assertIn("No CSV file selected", str(context.exception))


class TestDataPreviewStepDataPopulation(unittest.TestCase):
    """Test DataPreviewStep data population in Treeview."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()
        self.step = DataPreviewStep(self.parent)
        self.container = ttk.Frame(self.root)
        self.step.create(self.container)

    def tearDown(self):
        """Clean up after tests."""
        self.step.destroy()
        self.root.destroy()

    @patch('src.gui_steps.data_preview_step.gui_utils.format_preview_stats')
    def test_populate_preview_with_empty_data(self, mock_format_stats):
        """Test populating preview with empty CSV data."""
        mock_format_stats.return_value = "No data"

        # Set empty data
        self.parent.csv_headers = []
        self.parent.csv_data = []

        # Populate preview
        self.step._populate_preview()

        # Verify tree is empty
        tree = self.step._widgets['preview_tree']
        self.assertEqual(len(tree.get_children()), 0)

    @patch('src.gui_steps.data_preview_step.gui_utils.format_preview_stats')
    def test_populate_preview_with_less_than_100_rows(self, mock_format_stats):
        """Test populating preview with < 100 rows shows all rows."""
        mock_format_stats.return_value = "Showing 50 of 50 rows"

        # Create test data with 50 rows
        headers = ['Col1', 'Col2']
        data = [{'Col1': f'val1_{i}', 'Col2': f'val2_{i}'} for i in range(50)]

        self.parent.csv_headers = headers
        self.parent.csv_data = data

        # Populate preview
        self.step._populate_preview()

        # Verify all 50 rows are shown
        tree = self.step._widgets['preview_tree']
        self.assertEqual(len(tree.get_children()), 50)

        # Verify format_preview_stats was called correctly
        mock_format_stats.assert_called_once_with(50, 50, max_preview=100)

    @patch('src.gui_steps.data_preview_step.gui_utils.format_preview_stats')
    def test_populate_preview_with_more_than_100_rows(self, mock_format_stats):
        """Test populating preview with > 100 rows limits to 100."""
        mock_format_stats.return_value = "Showing 100 of 150 rows"

        # Create test data with 150 rows
        headers = ['Col1', 'Col2']
        data = [{'Col1': f'val1_{i}', 'Col2': f'val2_{i}'} for i in range(150)]

        self.parent.csv_headers = headers
        self.parent.csv_data = data

        # Populate preview
        self.step._populate_preview()

        # Verify only 100 rows are shown
        tree = self.step._widgets['preview_tree']
        self.assertEqual(len(tree.get_children()), 100)

        # Verify format_preview_stats was called with correct values
        mock_format_stats.assert_called_once_with(100, 150, max_preview=100)

    @patch('src.gui_steps.data_preview_step.gui_utils.format_preview_stats')
    def test_populate_preview_configures_tree_columns(self, mock_format_stats):
        """Test populate_preview configures Treeview columns correctly."""
        mock_format_stats.return_value = "Stats"

        # Create test data
        headers = ['Date', 'Description', 'Amount']
        data = [{'Date': '2025-01-01', 'Description': 'Test', 'Amount': '100.00'}]

        self.parent.csv_headers = headers
        self.parent.csv_data = data

        # Populate preview
        self.step._populate_preview()

        # Verify tree columns are configured
        tree = self.step._widgets['preview_tree']
        self.assertEqual(list(tree['columns']), headers)

        # Verify show mode is 'headings' (no tree column)
        self.assertEqual(tree['show'], 'headings')


class TestDataPreviewStepValidation(unittest.TestCase):
    """Test DataPreviewStep validation logic."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()
        self.step = DataPreviewStep(self.parent)
        self.container = ttk.Frame(self.root)
        self.step.create(self.container)

    def tearDown(self):
        """Clean up after tests."""
        self.step.destroy()
        self.root.destroy()

    def test_validate_fails_when_no_data_loaded(self):
        """Test validation fails when no CSV data is loaded."""
        # Don't load any data (empty by default)

        result = self.step.validate()

        self.assertIsInstance(result, StepData)
        self.assertFalse(result.is_valid)
        self.assertIsNotNone(result.error_message)
        self.assertIn("No CSV data loaded", result.error_message)

    def test_validate_fails_when_csv_data_is_empty_list(self):
        """Test validation fails when csv_data is empty list."""
        # Set empty list
        self.parent.csv_data = []

        result = self.step.validate()

        self.assertFalse(result.is_valid)
        self.assertIsNotNone(result.error_message)

    def test_validate_succeeds_when_data_is_loaded(self):
        """Test validation succeeds when data is loaded (≥1 row)."""
        # Set test data
        self.parent.csv_headers = ['Date', 'Amount']
        self.parent.csv_data = [{'Date': '2025-01-01', 'Amount': '100.00'}]

        result = self.step.validate()

        self.assertTrue(result.is_valid)
        self.assertIsNone(result.error_message)
        self.assertIn('csv_headers', result.data)
        self.assertIn('csv_data', result.data)

    def test_validate_returns_correct_data_structure(self):
        """Test validate returns correct data structure with headers and data."""
        # Set test data
        headers = ['Col1', 'Col2']
        data = [{'Col1': 'val1', 'Col2': 'val2'}]

        self.parent.csv_headers = headers
        self.parent.csv_data = data

        result = self.step.validate()

        self.assertTrue(result.is_valid)
        self.assertEqual(result.data['csv_headers'], headers)
        self.assertEqual(result.data['csv_data'], data)
        self.assertIn('reload_requested', result.data)


class TestDataPreviewStepLifecycle(unittest.TestCase):
    """Test DataPreviewStep lifecycle management."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()
        self.step = DataPreviewStep(self.parent)
        self.container = ttk.Frame(self.root)
        self.step.create(self.container)

    def tearDown(self):
        """Clean up after tests."""
        self.root.destroy()

    @patch('src.gui_steps.data_preview_step.CSVParser')
    @patch('src.gui_steps.data_preview_step.gui_utils.format_preview_stats')
    def test_show_loads_data_on_first_display(self, mock_format_stats, mock_parser_class):
        """Test show() loads CSV data on first display when not already loaded."""
        # Mock CSV parser
        mock_parser = Mock()
        mock_parser.parse_file.return_value = (
            ['Date', 'Amount'],
            [{'Date': '2025-01-01', 'Amount': '100.00'}]
        )
        mock_parser_class.return_value = mock_parser
        mock_format_stats.return_value = "Showing 1 of 1 rows"

        # Set CSV file path
        self.parent.csv_file.set('/test/file.csv')

        # Ensure data is not loaded yet
        self.assertEqual(len(self.parent.csv_data), 0)

        # Show step (should trigger load)
        self.step.show()

        # Verify data was loaded
        self.assertEqual(len(self.parent.csv_data), 1)
        mock_parser.parse_file.assert_called_once()

    @patch('src.gui_steps.data_preview_step.CSVParser')
    @patch('src.gui_steps.data_preview_step.gui_utils.format_preview_stats')
    def test_show_does_not_reload_when_data_exists(self, mock_format_stats, mock_parser_class):
        """Test show() does not reload when data already exists."""
        mock_format_stats.return_value = "Stats"

        # Set existing data
        self.parent.csv_headers = ['Date']
        self.parent.csv_data = [{'Date': '2025-01-01'}]

        # Mock parser (should not be called)
        mock_parser = Mock()
        mock_parser_class.return_value = mock_parser

        # Show step
        self.step.show()

        # Verify parser was NOT called
        mock_parser.parse_file.assert_not_called()

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
        grid_info = self.step.container.grid_info()
        self.assertEqual(grid_info, {})

    def test_destroy_cleans_up_resources(self):
        """Test destroy() cleans up container and widgets."""
        # Destroy step
        self.step.destroy()

        # Verify container is None
        self.assertIsNone(self.step.container)

        # Verify widgets dict is cleared
        self.assertEqual(len(self.step._widgets), 0)


class TestDataPreviewStepReloadButton(unittest.TestCase):
    """Test DataPreviewStep reload button functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()
        self.step = DataPreviewStep(self.parent)
        self.container = ttk.Frame(self.root)
        self.step.create(self.container)

    def tearDown(self):
        """Clean up after tests."""
        self.step.destroy()
        self.root.destroy()

    @patch('src.gui_steps.data_preview_step.CSVParser')
    @patch('src.gui_steps.data_preview_step.gui_utils.format_preview_stats')
    def test_reload_button_triggers_data_reload(self, mock_format_stats, mock_parser_class):
        """Test reload button click triggers CSV data reload."""
        # Mock CSV parser
        mock_parser = Mock()
        mock_parser.parse_file.return_value = (
            ['New', 'Headers'],
            [{'New': 'data1', 'Headers': 'data2'}]
        )
        mock_parser_class.return_value = mock_parser
        mock_format_stats.return_value = "Showing 1 of 1 rows"

        # Set CSV file path
        self.parent.csv_file.set('/test/file.csv')

        # Set old data
        self.parent.csv_headers = ['Old']
        self.parent.csv_data = [{'Old': 'data'}]

        # Simulate reload button click
        self.step._on_reload_clicked()

        # Verify new data was loaded
        self.assertEqual(self.parent.csv_headers, ['New', 'Headers'])
        mock_parser.parse_file.assert_called_once()

    @patch('src.gui_steps.data_preview_step.CSVParser')
    def test_reload_button_resets_reload_flag_on_success(self, mock_parser_class):
        """Test reload button resets _reload_requested flag after successful reload."""
        # Mock CSV parser
        mock_parser = Mock()
        mock_parser.parse_file.return_value = (['Col'], [{'Col': 'val'}])
        mock_parser_class.return_value = mock_parser

        self.parent.csv_file.set('/test/file.csv')

        # Trigger reload
        self.step._on_reload_clicked()

        # Verify flag was reset
        self.assertFalse(self.step._reload_requested)

    @patch('src.gui_steps.data_preview_step.CSVParser')
    def test_reload_button_logs_success_message(self, mock_parser_class):
        """Test reload button logs success message on successful reload."""
        # Mock CSV parser
        mock_parser = Mock()
        mock_parser.parse_file.return_value = (['Col'], [{'Col': 'val'}])
        mock_parser_class.return_value = mock_parser

        self.parent.csv_file.set('/test/file.csv')

        # Clear log messages
        self.parent.log_messages = []

        # Trigger reload
        self.step._on_reload_clicked()

        # Verify success log was created
        success_logs = [msg for msg in self.parent.log_messages
                       if 'reloaded successfully' in msg]
        self.assertEqual(len(success_logs), 1)


if __name__ == '__main__':
    unittest.main()
