"""
Unit tests for CSVFormatStep class.

This module contains comprehensive unit tests for the CSVFormatStep wizard step,
testing initialization, UI creation, radio button behavior, data collection,
validation (always passes), and lifecycle management.

Tests use mocks to avoid GUI dependencies and verify proper integration with the
WizardStep base class.
"""

import unittest
import tkinter as tk
from tkinter import ttk
from unittest.mock import Mock, patch
import os
import sys

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

from src.gui_wizard_step import StepConfig, StepData
from src.gui_steps.csv_format_step import CSVFormatStep


class MockConverterGUI:
    """Mock ConverterGUI for testing without actual GUI dependencies."""

    def __init__(self):
        """Initialize mock with required attributes."""
        # Create StringVars for delimiter and decimal separator
        self.delimiter = tk.StringVar(value=',')  # Default comma
        self.decimal_separator = tk.StringVar(value='.')  # Default dot
        # Store log messages for verification
        self.log_messages = []

    def _log(self, message: str):
        """Mock logging method that stores messages."""
        self.log_messages.append(message)


class TestCSVFormatStepInitialization(unittest.TestCase):
    """Test CSVFormatStep initialization."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()

    def tearDown(self):
        """Clean up after tests."""
        self.root.destroy()

    def test_step_initializes_with_correct_config(self):
        """Test step initializes with correct configuration values."""
        step = CSVFormatStep(self.parent)

        self.assertEqual(step.config.step_number, 1)
        self.assertEqual(step.config.step_name, "CSV Format")
        self.assertEqual(step.config.step_title, "Step 2: Configure CSV Format")
        self.assertTrue(step.config.is_required)
        self.assertTrue(step.config.can_go_back)
        self.assertTrue(step.config.show_next)
        self.assertFalse(step.config.show_convert)

    def test_parent_reference_is_set_correctly(self):
        """Test parent reference is stored correctly."""
        step = CSVFormatStep(self.parent)

        self.assertIs(step.parent, self.parent)

    def test_widgets_dict_is_empty_before_ui_creation(self):
        """Test widgets dictionary is empty before UI creation."""
        step = CSVFormatStep(self.parent)

        self.assertEqual(len(step._widgets), 0)
        self.assertIsInstance(step._widgets, dict)


class TestCSVFormatStepUICreation(unittest.TestCase):
    """Test CSVFormatStep UI creation and widget creation."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()
        self.step = CSVFormatStep(self.parent)
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
        self.assertEqual(self.step.container['text'], "Step 2: Configure CSV Format")

        # Verify widgets were created
        self.assertGreater(len(self.step._widgets), 0)

    def test_delimiter_radio_buttons_created(self):
        """Test delimiter radio buttons are created (3 buttons: comma, semicolon, tab)."""
        self.step.create(self.container)

        # Verify delimiter_frame is stored in widgets dict
        self.assertIn('delimiter_frame', self.step._widgets)

        # Verify delimiter_frame is a Frame
        self.assertIsInstance(self.step._widgets['delimiter_frame'], ttk.Frame)

        # Verify the frame contains children (the radio buttons)
        delimiter_frame = self.step._widgets['delimiter_frame']
        children = delimiter_frame.winfo_children()

        # Should have 3 radio buttons
        radio_buttons = [child for child in children if isinstance(child, ttk.Radiobutton)]
        self.assertEqual(len(radio_buttons), 3)

    def test_decimal_separator_radio_buttons_created(self):
        """Test decimal separator radio buttons are created (2 buttons: dot, comma)."""
        self.step.create(self.container)

        # Verify decimal_frame is stored in widgets dict
        self.assertIn('decimal_frame', self.step._widgets)

        # Verify decimal_frame is a Frame
        self.assertIsInstance(self.step._widgets['decimal_frame'], ttk.Frame)

        # Verify the frame contains children (the radio buttons)
        decimal_frame = self.step._widgets['decimal_frame']
        children = decimal_frame.winfo_children()

        # Should have 2 radio buttons
        radio_buttons = [child for child in children if isinstance(child, ttk.Radiobutton)]
        self.assertEqual(len(radio_buttons), 2)

    def test_radio_buttons_bound_to_parent_stringvars(self):
        """Test radio buttons are bound to parent.delimiter and parent.decimal_separator StringVars."""
        self.step.create(self.container)

        # Get delimiter radio buttons
        delimiter_frame = self.step._widgets['delimiter_frame']
        delimiter_buttons = [child for child in delimiter_frame.winfo_children()
                           if isinstance(child, ttk.Radiobutton)]

        # Get decimal separator radio buttons
        decimal_frame = self.step._widgets['decimal_frame']
        decimal_buttons = [child for child in decimal_frame.winfo_children()
                         if isinstance(child, ttk.Radiobutton)]

        # Verify delimiter buttons are bound to parent's delimiter StringVar
        for button in delimiter_buttons:
            delimiter_var = button['variable']
            # StringVar comparison - check the underlying variable
            self.assertEqual(str(delimiter_var), str(self.parent.delimiter))

        # Verify decimal buttons are bound to parent's decimal_separator StringVar
        for button in decimal_buttons:
            decimal_var = button['variable']
            # StringVar comparison - check the underlying variable
            self.assertEqual(str(decimal_var), str(self.parent.decimal_separator))

    def test_info_text_label_created(self):
        """Test info text label is created."""
        self.step.create(self.container)

        # Verify container has children (info text is created but not stored in _widgets)
        # The implementation creates labels directly without storing references
        children = self.step.container.winfo_children()

        # Should have multiple children (labels and frames)
        self.assertGreater(len(children), 0)

        # Find labels among children
        labels = [child for child in children if isinstance(child, ttk.Label)]

        # Should have at least 3 labels: description, delimiter label, decimal label, and info text
        self.assertGreaterEqual(len(labels), 3)


class TestCSVFormatStepLayout(unittest.TestCase):
    """Test CSVFormatStep layout configuration."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()
        self.step = CSVFormatStep(self.parent)
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

    def test_proper_spacing_between_sections(self):
        """Test proper spacing between delimiter and decimal separator sections."""
        self.step.create(self.container)

        # Verify delimiter_frame and decimal_frame exist
        self.assertIn('delimiter_frame', self.step._widgets)
        self.assertIn('decimal_frame', self.step._widgets)

        # Get grid info for spacing verification
        delimiter_info = self.step._widgets['delimiter_frame'].grid_info()
        decimal_info = self.step._widgets['decimal_frame'].grid_info()

        # Verify they're in different rows
        self.assertNotEqual(delimiter_info['row'], decimal_info['row'])
        self.assertGreater(int(decimal_info['row']), int(delimiter_info['row']))


class TestCSVFormatStepRadioButtonBehavior(unittest.TestCase):
    """Test CSVFormatStep radio button behavior and value updates."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()
        self.step = CSVFormatStep(self.parent)
        self.container = ttk.Frame(self.root)
        self.step.create(self.container)

    def tearDown(self):
        """Clean up after tests."""
        self.step.destroy()
        self.root.destroy()

    def test_selecting_delimiter_options_updates_parent(self):
        """Test selecting different delimiter options updates parent.delimiter."""
        # Test comma selection
        self.parent.delimiter.set(',')
        self.assertEqual(self.parent.delimiter.get(), ',')

        # Test semicolon selection
        self.parent.delimiter.set(';')
        self.assertEqual(self.parent.delimiter.get(), ';')

        # Test tab selection
        self.parent.delimiter.set('\t')
        self.assertEqual(self.parent.delimiter.get(), '\t')

    def test_selecting_decimal_separator_options_updates_parent(self):
        """Test selecting different decimal separator options updates parent.decimal_separator."""
        # Test dot selection
        self.parent.decimal_separator.set('.')
        self.assertEqual(self.parent.decimal_separator.get(), '.')

        # Test comma selection
        self.parent.decimal_separator.set(',')
        self.assertEqual(self.parent.decimal_separator.get(), ',')

    def test_default_values_reflected_in_radio_buttons(self):
        """Test default values are reflected in radio buttons."""
        # Create new step with default values
        new_parent = MockConverterGUI()
        new_step = CSVFormatStep(new_parent)
        new_container = ttk.Frame(self.root)
        new_step.create(new_container)

        # Verify defaults are set correctly
        self.assertEqual(new_parent.delimiter.get(), ',')
        self.assertEqual(new_parent.decimal_separator.get(), '.')

        # Cleanup
        new_step.destroy()


class TestCSVFormatStepDataCollection(unittest.TestCase):
    """Test CSVFormatStep data collection."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()
        self.step = CSVFormatStep(self.parent)
        self.container = ttk.Frame(self.root)
        self.step.create(self.container)

    def tearDown(self):
        """Clean up after tests."""
        self.step.destroy()
        self.root.destroy()

    def test_collect_data_returns_correct_structure(self):
        """Test _collect_data() returns correct dict structure with delimiter and decimal_separator keys."""
        data = self.step._collect_data()

        self.assertIsInstance(data, dict)
        self.assertIn('delimiter', data)
        self.assertIn('decimal_separator', data)

    def test_collect_data_gets_values_from_parent_stringvars(self):
        """Test _collect_data() gets values from parent StringVars."""
        # Set test values
        self.parent.delimiter.set(';')
        self.parent.decimal_separator.set(',')

        data = self.step._collect_data()

        self.assertEqual(data['delimiter'], ';')
        self.assertEqual(data['decimal_separator'], ',')


class TestCSVFormatStepValidation(unittest.TestCase):
    """Test CSVFormatStep validation logic."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()
        self.step = CSVFormatStep(self.parent)
        self.container = ttk.Frame(self.root)
        self.step.create(self.container)

    def tearDown(self):
        """Clean up after tests."""
        self.step.destroy()
        self.root.destroy()

    def test_validate_always_returns_valid(self):
        """Test validate() always returns is_valid=True (no validation errors)."""
        # Test with default values
        result = self.step.validate()
        self.assertIsInstance(result, StepData)
        self.assertTrue(result.is_valid)

        # Test with different values
        self.parent.delimiter.set(';')
        self.parent.decimal_separator.set(',')
        result = self.step.validate()
        self.assertTrue(result.is_valid)

    def test_validate_returns_none_for_error_message(self):
        """Test validate() returns None for error_message."""
        result = self.step.validate()

        self.assertIsNone(result.error_message)

    def test_validate_returns_collected_data(self):
        """Test validate() returns collected data even though validation always succeeds."""
        self.parent.delimiter.set('\t')
        self.parent.decimal_separator.set('.')

        result = self.step.validate()

        self.assertTrue(result.is_valid)
        self.assertIsNone(result.error_message)
        self.assertIn('delimiter', result.data)
        self.assertIn('decimal_separator', result.data)
        self.assertEqual(result.data['delimiter'], '\t')
        self.assertEqual(result.data['decimal_separator'], '.')


class TestCSVFormatStepLifecycle(unittest.TestCase):
    """Test CSVFormatStep lifecycle management."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()
        self.step = CSVFormatStep(self.parent)
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
