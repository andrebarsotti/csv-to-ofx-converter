"""
Unit tests for AdvancedOptionsStep class.

This module contains comprehensive unit tests for the AdvancedOptionsStep wizard step,
testing initialization, UI creation, date formatting, date toggle functionality,
validation, data collection, and lifecycle management.

Tests use mocks to avoid GUI dependencies and verify proper integration with the
WizardStep base class and gui_utils validation functions.
"""

import unittest
import tkinter as tk
from tkinter import ttk
from unittest.mock import Mock, patch, MagicMock, call
import os
import sys

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

from src.gui_wizard_step import StepConfig, StepData
from src.gui_steps.advanced_options_step import AdvancedOptionsStep


class MockConverterGUI:
    """Mock ConverterGUI for testing without actual GUI dependencies."""

    def __init__(self):
        """Initialize mock with required attributes."""
        # Create BooleanVars for checkboxes
        self.invert_values = tk.BooleanVar(value=False)
        self.enable_date_validation = tk.BooleanVar(value=False)

        # Create StringVars for date entries
        self.start_date = tk.StringVar(value='')
        self.end_date = tk.StringVar(value='')

        # Optional entry widgets (set by step)
        self.start_date_entry = None
        self.end_date_entry = None

        # Store log messages for verification
        self.log_messages = []

    def _log(self, message: str):
        """Mock logging method that stores messages."""
        self.log_messages.append(message)


class TestAdvancedOptionsStepInitialization(unittest.TestCase):
    """Test AdvancedOptionsStep initialization."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()

    def tearDown(self):
        """Clean up after tests."""
        self.root.destroy()

    def test_step_initializes_with_correct_config(self):
        """Test step initializes with correct configuration values."""
        step = AdvancedOptionsStep(self.parent)

        self.assertEqual(step.config.step_number, 5)
        self.assertEqual(step.config.step_name, "Advanced Options")
        self.assertEqual(step.config.step_title, "Step 6: Advanced Options")
        self.assertTrue(step.config.is_required)
        self.assertTrue(step.config.can_go_back)
        self.assertTrue(step.config.show_next)
        self.assertFalse(step.config.show_convert)

    def test_step_number_is_five(self):
        """Test step_number is 5 (Step 6 is index 5)."""
        step = AdvancedOptionsStep(self.parent)

        self.assertEqual(step.config.step_number, 5)

    def test_step_name_is_advanced_options(self):
        """Test step_name is 'Advanced Options'."""
        step = AdvancedOptionsStep(self.parent)

        self.assertEqual(step.config.step_name, "Advanced Options")

    def test_parent_reference_is_set_correctly(self):
        """Test parent reference is stored correctly."""
        step = AdvancedOptionsStep(self.parent)

        self.assertIs(step.parent, self.parent)

    def test_widgets_dict_is_empty_before_ui_creation(self):
        """Test widgets dictionary is empty before UI creation."""
        step = AdvancedOptionsStep(self.parent)

        self.assertEqual(len(step._widgets), 0)
        self.assertIsInstance(step._widgets, dict)

    def test_step_config_values_are_correct(self):
        """Test StepConfig has correct values for advanced options step."""
        step = AdvancedOptionsStep(self.parent)

        config = step.config
        self.assertIsInstance(config, StepConfig)
        self.assertEqual(config.step_number, 5)
        self.assertEqual(config.step_name, "Advanced Options")
        self.assertEqual(config.step_title, "Step 6: Advanced Options")


class TestAdvancedOptionsStepUICreation(unittest.TestCase):
    """Test AdvancedOptionsStep UI creation and widget creation."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()
        self.step = AdvancedOptionsStep(self.parent)
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
        self.assertEqual(self.step.container['text'], "Step 6: Advanced Options")

    def test_invert_values_checkbox_created(self):
        """Test invert_values checkbox is created."""
        self.step.create(self.container)

        # Verify invert_values_var is stored in widgets dict
        self.assertIn('invert_values_var', self.step._widgets)

        # Verify it's a BooleanVar
        self.assertIsInstance(self.step._widgets['invert_values_var'], tk.BooleanVar)

    def test_invert_values_checkbox_bound_to_parent(self):
        """Test invert_values checkbox is bound to parent variable."""
        self.step.create(self.container)

        # Verify widget var is the same as parent var
        self.assertIs(self.step._widgets['invert_values_var'], self.parent.invert_values)

    def test_enable_date_validation_checkbox_created(self):
        """Test enable_date_validation checkbox is created."""
        self.step.create(self.container)

        # Verify enable_date_validation_var is stored in widgets dict
        self.assertIn('enable_date_validation_var', self.step._widgets)

        # Verify it's a BooleanVar
        self.assertIsInstance(self.step._widgets['enable_date_validation_var'], tk.BooleanVar)

    def test_enable_date_validation_checkbox_bound_to_parent(self):
        """Test enable_date_validation checkbox is bound to parent variable."""
        self.step.create(self.container)

        # Verify widget var is the same as parent var
        self.assertIs(self.step._widgets['enable_date_validation_var'], self.parent.enable_date_validation)

    def test_start_date_entry_created(self):
        """Test start_date entry is created."""
        self.step.create(self.container)

        # Verify start_date_entry is stored in widgets dict
        self.assertIn('start_date_entry', self.step._widgets)

        # Verify widget type
        self.assertIsInstance(self.step._widgets['start_date_entry'], ttk.Entry)

        # Verify initial state is disabled
        self.assertEqual(str(self.step._widgets['start_date_entry']['state']), 'disabled')

    def test_end_date_entry_created(self):
        """Test end_date entry is created."""
        self.step.create(self.container)

        # Verify end_date_entry is stored in widgets dict
        self.assertIn('end_date_entry', self.step._widgets)

        # Verify widget type
        self.assertIsInstance(self.step._widgets['end_date_entry'], ttk.Entry)

        # Verify initial state is disabled
        self.assertEqual(str(self.step._widgets['end_date_entry']['state']), 'disabled')

    def test_date_vars_stored_in_widgets_dict(self):
        """Test date StringVars are stored in widgets dict."""
        self.step.create(self.container)

        # Verify vars are stored
        self.assertIn('start_date_var', self.step._widgets)
        self.assertIn('end_date_var', self.step._widgets)

        # Verify they're StringVars
        self.assertIsInstance(self.step._widgets['start_date_var'], tk.StringVar)
        self.assertIsInstance(self.step._widgets['end_date_var'], tk.StringVar)

    def test_date_entries_set_on_parent_for_compatibility(self):
        """Test date entry widgets are set on parent for compatibility."""
        self.step.create(self.container)

        # Verify parent has entry attributes
        self.assertIsNotNone(self.parent.start_date_entry)
        self.assertIsNotNone(self.parent.end_date_entry)

        # Verify they're the same as step widgets
        self.assertIs(self.parent.start_date_entry, self.step._widgets['start_date_entry'])
        self.assertIs(self.parent.end_date_entry, self.step._widgets['end_date_entry'])


class TestAdvancedOptionsStepDateFormatting(unittest.TestCase):
    """Test AdvancedOptionsStep date formatting functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()
        self.step = AdvancedOptionsStep(self.parent)
        self.container = ttk.Frame(self.root)
        self.step.create(self.container)

    def tearDown(self):
        """Clean up after tests."""
        self.step.destroy()
        self.root.destroy()

    @patch('src.gui_steps.advanced_options_step.gui_utils.format_date_string')
    @patch('src.gui_steps.advanced_options_step.gui_utils.calculate_cursor_position_after_format')
    def test_format_date_entry_for_start_date(self, mock_calc_cursor, mock_format):
        """Test date auto-formatting for start_date entry."""
        # Setup mocks
        mock_format.return_value = '01/10/2025'
        mock_calc_cursor.return_value = 10

        # Get entry widget
        start_entry = self.step._widgets['start_date_entry']

        # Set a value
        start_entry.delete(0, tk.END)
        start_entry.insert(0, '01102025')

        # Call format method
        self.step._format_date_entry(start_entry)

        # Verify format_date_string was called
        mock_format.assert_called_once_with('01102025')

        # Verify entry value was updated
        self.assertEqual(start_entry.get(), '01/10/2025')

    @patch('src.gui_steps.advanced_options_step.gui_utils.format_date_string')
    @patch('src.gui_steps.advanced_options_step.gui_utils.calculate_cursor_position_after_format')
    def test_format_date_entry_for_end_date(self, mock_calc_cursor, mock_format):
        """Test date auto-formatting for end_date entry."""
        # Setup mocks
        mock_format.return_value = '31/10/2025'
        mock_calc_cursor.return_value = 10

        # Get entry widget
        end_entry = self.step._widgets['end_date_entry']

        # Set a value
        end_entry.delete(0, tk.END)
        end_entry.insert(0, '31102025')

        # Call format method
        self.step._format_date_entry(end_entry)

        # Verify format_date_string was called
        mock_format.assert_called_once_with('31102025')

        # Verify entry value was updated
        self.assertEqual(end_entry.get(), '31/10/2025')

    @patch('src.gui_steps.advanced_options_step.gui_utils.format_date_string')
    @patch('src.gui_steps.advanced_options_step.gui_utils.calculate_cursor_position_after_format')
    def test_cursor_position_maintained_after_formatting(self, mock_calc_cursor, mock_format):
        """Test cursor position is maintained after formatting."""
        # Setup mocks
        mock_format.return_value = '01/10/2025'
        mock_calc_cursor.return_value = 5  # New cursor position

        # Get entry widget
        start_entry = self.step._widgets['start_date_entry']

        # Set a value and cursor position
        start_entry.delete(0, tk.END)
        start_entry.insert(0, '01102025')
        start_entry.icursor(3)  # Set cursor to position 3

        # Call format method
        self.step._format_date_entry(start_entry)

        # Verify calculate_cursor_position_after_format was called
        mock_calc_cursor.assert_called_once_with('01102025', '01/10/2025', 3)

        # Verify cursor position was set to new position
        self.assertEqual(start_entry.index(tk.INSERT), 5)

    @patch('src.gui_steps.advanced_options_step.gui_utils.format_date_string')
    def test_format_date_string_integration(self, mock_format):
        """Test format_date_string is called with correct parameters."""
        # Setup mock
        mock_format.return_value = '15/03/2025'

        # Get entry widget
        start_entry = self.step._widgets['start_date_entry']

        # Set a value
        start_entry.delete(0, tk.END)
        start_entry.insert(0, '15032025')

        # Call format method
        self.step._format_date_entry(start_entry)

        # Verify format_date_string was called with current value
        mock_format.assert_called_once_with('15032025')

    @patch('src.gui_steps.advanced_options_step.gui_utils.format_date_string')
    @patch('src.gui_steps.advanced_options_step.gui_utils.calculate_cursor_position_after_format')
    def test_format_does_not_update_if_no_change(self, mock_calc_cursor, mock_format):
        """Test format does not update entry if formatted value is same."""
        # Setup mock to return same value (no formatting needed)
        mock_format.return_value = '01/10/2025'

        # Get entry widget
        start_entry = self.step._widgets['start_date_entry']

        # Set already-formatted value
        start_entry.delete(0, tk.END)
        start_entry.insert(0, '01/10/2025')

        # Call format method
        self.step._format_date_entry(start_entry)

        # Verify format_date_string was called
        mock_format.assert_called_once_with('01/10/2025')

        # Verify calculate_cursor_position was NOT called (no update)
        mock_calc_cursor.assert_not_called()


class TestAdvancedOptionsStepDateToggle(unittest.TestCase):
    """Test AdvancedOptionsStep date validation toggle functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()
        self.step = AdvancedOptionsStep(self.parent)
        self.container = ttk.Frame(self.root)
        self.step.create(self.container)

    def tearDown(self):
        """Clean up after tests."""
        self.step.destroy()
        self.root.destroy()

    def test_date_entries_disabled_when_validation_disabled(self):
        """Test date entries are disabled when enable_date_validation is False."""
        # Set checkbox to False
        self.parent.enable_date_validation.set(False)

        # Call toggle method
        self.step._toggle_date_inputs()

        # Verify entries are disabled
        self.assertEqual(str(self.step._widgets['start_date_entry']['state']), 'disabled')
        self.assertEqual(str(self.step._widgets['end_date_entry']['state']), 'disabled')

    def test_date_entries_enabled_when_validation_enabled(self):
        """Test date entries are enabled when enable_date_validation is True."""
        # Set checkbox to True
        self.parent.enable_date_validation.set(True)

        # Call toggle method
        self.step._toggle_date_inputs()

        # Verify entries are enabled
        self.assertEqual(str(self.step._widgets['start_date_entry']['state']), 'normal')
        self.assertEqual(str(self.step._widgets['end_date_entry']['state']), 'normal')

    def test_checkbox_toggle_triggers_enable_disable(self):
        """Test checkbox toggle triggers enable/disable correctly."""
        # Start with disabled
        self.parent.enable_date_validation.set(False)
        self.step._toggle_date_inputs()
        self.assertEqual(str(self.step._widgets['start_date_entry']['state']), 'disabled')

        # Toggle to enabled
        self.parent.enable_date_validation.set(True)
        self.step._toggle_date_inputs()
        self.assertEqual(str(self.step._widgets['start_date_entry']['state']), 'normal')

        # Toggle back to disabled
        self.parent.enable_date_validation.set(False)
        self.step._toggle_date_inputs()
        self.assertEqual(str(self.step._widgets['start_date_entry']['state']), 'disabled')

    def test_initial_state_based_on_parent_variable(self):
        """Test initial entry state matches parent variable value."""
        # Create new step with parent that has validation enabled
        self.step.destroy()
        self.parent.enable_date_validation.set(True)
        self.step = AdvancedOptionsStep(self.parent)
        self.step.create(self.container)

        # Initial state should still be disabled (entries always start disabled)
        self.assertEqual(str(self.step._widgets['start_date_entry']['state']), 'disabled')

        # But after toggle, they should be enabled
        self.step._toggle_date_inputs()
        self.assertEqual(str(self.step._widgets['start_date_entry']['state']), 'normal')


class TestAdvancedOptionsStepValidation(unittest.TestCase):
    """Test AdvancedOptionsStep validation logic."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()
        self.step = AdvancedOptionsStep(self.parent)
        self.container = ttk.Frame(self.root)
        self.step.create(self.container)

    def tearDown(self):
        """Clean up after tests."""
        self.step.destroy()
        self.root.destroy()

    def test_validation_succeeds_when_date_validation_disabled(self):
        """Test validation succeeds when date validation is disabled."""
        # Disable date validation
        self.parent.enable_date_validation.set(False)

        # Validate
        result = self.step.validate()

        # Should be valid
        self.assertTrue(result.is_valid)
        self.assertIsNone(result.error_message)

    @patch('src.gui_steps.advanced_options_step.gui_utils.validate_date_range_inputs')
    def test_validation_succeeds_with_valid_date_range(self, mock_validate):
        """Test validation succeeds with valid date range."""
        # Setup mock
        mock_validate.return_value = (True, None)

        # Enable date validation and set dates
        self.parent.enable_date_validation.set(True)
        self.parent.start_date.set('01/10/2025')
        self.parent.end_date.set('31/10/2025')

        # Validate
        result = self.step.validate()

        # Verify validate_date_range_inputs was called
        mock_validate.assert_called_once_with('01/10/2025', '31/10/2025')

        # Should be valid
        self.assertTrue(result.is_valid)
        self.assertIsNone(result.error_message)

    @patch('src.gui_steps.advanced_options_step.gui_utils.validate_date_range_inputs')
    def test_validation_fails_with_invalid_date_format(self, mock_validate):
        """Test validation fails with invalid date format."""
        # Setup mock
        mock_validate.return_value = (False, "Invalid date format")

        # Enable date validation and set invalid dates
        self.parent.enable_date_validation.set(True)
        self.parent.start_date.set('invalid')
        self.parent.end_date.set('31/10/2025')

        # Validate
        result = self.step.validate()

        # Verify validate_date_range_inputs was called
        mock_validate.assert_called_once_with('invalid', '31/10/2025')

        # Should be invalid
        self.assertFalse(result.is_valid)
        self.assertIsNotNone(result.error_message)
        self.assertEqual(result.error_message, "Invalid date format")

    @patch('src.gui_steps.advanced_options_step.gui_utils.validate_date_range_inputs')
    def test_validation_fails_when_start_date_after_end_date(self, mock_validate):
        """Test validation fails when start_date > end_date."""
        # Setup mock
        mock_validate.return_value = (False, "Start date must be before end date")

        # Enable date validation and set invalid range
        self.parent.enable_date_validation.set(True)
        self.parent.start_date.set('31/10/2025')
        self.parent.end_date.set('01/10/2025')

        # Validate
        result = self.step.validate()

        # Verify validate_date_range_inputs was called
        mock_validate.assert_called_once_with('31/10/2025', '01/10/2025')

        # Should be invalid
        self.assertFalse(result.is_valid)
        self.assertIsNotNone(result.error_message)

    @patch('src.gui_steps.advanced_options_step.gui_utils.validate_date_range_inputs')
    def test_validation_uses_gui_utils_function(self, mock_validate):
        """Test validation uses gui_utils.validate_date_range_inputs()."""
        # Setup mock
        mock_validate.return_value = (True, None)

        # Enable date validation
        self.parent.enable_date_validation.set(True)
        self.parent.start_date.set('01/01/2025')
        self.parent.end_date.set('31/12/2025')

        # Validate
        self.step.validate()

        # Verify gui_utils function was called
        mock_validate.assert_called_once_with('01/01/2025', '31/12/2025')


class TestAdvancedOptionsStepDataCollection(unittest.TestCase):
    """Test AdvancedOptionsStep data collection functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()
        self.step = AdvancedOptionsStep(self.parent)
        self.container = ttk.Frame(self.root)
        self.step.create(self.container)

    def tearDown(self):
        """Clean up after tests."""
        self.step.destroy()
        self.root.destroy()

    def test_collect_data_returns_all_four_fields(self):
        """Test _collect_data() returns all four fields."""
        # Set some values
        self.parent.invert_values.set(True)
        self.parent.enable_date_validation.set(True)
        self.parent.start_date.set('01/10/2025')
        self.parent.end_date.set('31/10/2025')

        # Collect data
        data = self.step._collect_data()

        # Verify all fields are present
        self.assertIn('invert_values', data)
        self.assertIn('enable_date_validation', data)
        self.assertIn('start_date', data)
        self.assertIn('end_date', data)

    def test_collected_data_matches_parent_values(self):
        """Test collected data matches parent values."""
        # Set specific values
        self.parent.invert_values.set(True)
        self.parent.enable_date_validation.set(False)
        self.parent.start_date.set('15/03/2025')
        self.parent.end_date.set('20/05/2025')

        # Collect data
        data = self.step._collect_data()

        # Verify values match
        self.assertEqual(data['invert_values'], True)
        self.assertEqual(data['enable_date_validation'], False)
        self.assertEqual(data['start_date'], '15/03/2025')
        self.assertEqual(data['end_date'], '20/05/2025')

    @patch('src.gui_steps.advanced_options_step.gui_utils.validate_date_range_inputs')
    def test_validate_returns_correct_step_data_structure(self, mock_validate):
        """Test validate() returns correct StepData structure."""
        # Setup mock
        mock_validate.return_value = (True, None)

        # Set values
        self.parent.invert_values.set(False)
        self.parent.enable_date_validation.set(True)
        self.parent.start_date.set('01/01/2025')
        self.parent.end_date.set('31/12/2025')

        # Validate
        result = self.step.validate()

        # Verify StepData structure
        self.assertIsInstance(result, StepData)
        self.assertTrue(result.is_valid)
        self.assertIsNone(result.error_message)

        # Verify data contains all fields
        self.assertIn('invert_values', result.data)
        self.assertIn('enable_date_validation', result.data)
        self.assertIn('start_date', result.data)
        self.assertIn('end_date', result.data)

        # Verify data values
        self.assertEqual(result.data['invert_values'], False)
        self.assertEqual(result.data['enable_date_validation'], True)
        self.assertEqual(result.data['start_date'], '01/01/2025')
        self.assertEqual(result.data['end_date'], '31/12/2025')


class TestAdvancedOptionsStepLifecycle(unittest.TestCase):
    """Test AdvancedOptionsStep lifecycle management."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()
        self.step = AdvancedOptionsStep(self.parent)
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

    def test_show_calls_toggle_date_inputs(self):
        """Test show() calls _toggle_date_inputs to restore state."""
        # Set date validation enabled
        self.parent.enable_date_validation.set(True)

        # Show should call toggle_date_inputs which enables entries
        self.step.show()

        # Verify entries are enabled
        self.assertEqual(str(self.step._widgets['start_date_entry']['state']), 'normal')
        self.assertEqual(str(self.step._widgets['end_date_entry']['state']), 'normal')

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


class TestAdvancedOptionsStepGetOrCreateParentVar(unittest.TestCase):
    """Test AdvancedOptionsStep _get_or_create_parent_var helper method."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()
        self.step = AdvancedOptionsStep(self.parent)

    def tearDown(self):
        """Clean up after tests."""
        self.root.destroy()

    def test_get_existing_parent_variable(self):
        """Test _get_or_create_parent_var returns existing parent variable."""
        # Parent already has invert_values
        existing_var = self.parent.invert_values

        # Get variable
        result = self.step._get_or_create_parent_var('invert_values', tk.BooleanVar, False)

        # Verify it's the same object
        self.assertIs(result, existing_var)

    def test_create_new_parent_variable_if_not_exists(self):
        """Test _get_or_create_parent_var creates new variable if not exists."""
        # Remove attribute if it exists
        if hasattr(self.parent, 'new_var'):
            delattr(self.parent, 'new_var')

        # Get/create variable
        result = self.step._get_or_create_parent_var('new_var', tk.StringVar, 'default')

        # Verify new variable was created
        self.assertIsNotNone(result)
        self.assertIsInstance(result, tk.StringVar)
        self.assertEqual(result.get(), 'default')

        # Verify it was stored in parent
        self.assertTrue(hasattr(self.parent, 'new_var'))
        self.assertIs(self.parent.new_var, result)

    def test_created_variable_has_correct_type_and_default(self):
        """Test created variable has correct type and default value."""
        # Create BooleanVar
        bool_var = self.step._get_or_create_parent_var('test_bool', tk.BooleanVar, True)
        self.assertIsInstance(bool_var, tk.BooleanVar)
        self.assertTrue(bool_var.get())

        # Create StringVar
        str_var = self.step._get_or_create_parent_var('test_str', tk.StringVar, 'test')
        self.assertIsInstance(str_var, tk.StringVar)
        self.assertEqual(str_var.get(), 'test')


if __name__ == '__main__':
    unittest.main()
