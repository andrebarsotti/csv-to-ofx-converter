"""
Unit tests for FieldMappingStep class.

This module contains comprehensive unit tests for the FieldMappingStep wizard step,
testing initialization, UI creation, field mapping widgets, composite description UI,
validation, data collection, and lifecycle management.

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
from src.gui_steps.field_mapping_step import FieldMappingStep
from src.constants import NOT_MAPPED, NOT_SELECTED


class NoGetDict(dict):
    """
    Dict subclass without .get() method to work around WizardStep.get_parent_data bug.

    The WizardStep.get_parent_data method checks hasattr(attr, 'get') and calls attr.get()
    with no arguments. This works for Tkinter vars but breaks for dicts since dict.get()
    requires at least one argument. This wrapper prevents the issue by removing the get method.
    """
    def __getattribute__(self, name):
        if name == 'get':
            # Return None to make hasattr return False
            raise AttributeError("'NoGetDict' object has no attribute 'get'")
        return super().__getattribute__(name)


class MockConverterGUI:
    """Mock ConverterGUI for testing without actual GUI dependencies."""

    def __init__(self):
        """Initialize mock with required attributes."""
        # CSV headers for testing
        self.csv_headers = ['Date', 'Amount', 'Description', 'Type']

        # Field mappings dictionary (will be populated by step with StringVars)
        # Use NoGetDict to work around WizardStep.get_parent_data issue with dicts
        self.field_mappings = NoGetDict()

        # Description columns list (will be populated by step)
        # Initialize as empty list like real ConverterGUI
        self.description_columns = []

        # Description separator (will be created by step)
        # Initialize as None, step will create StringVar
        self.description_separator = None

        # Store log messages for verification
        self.log_messages = []

    def _log(self, message: str):
        """Mock logging method that stores messages."""
        self.log_messages.append(message)


class TestFieldMappingStepInitialization(unittest.TestCase):
    """Test FieldMappingStep initialization."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()

    def tearDown(self):
        """Clean up after tests."""
        self.root.destroy()

    def test_step_initializes_with_correct_config(self):
        """Test step initializes with correct configuration values."""
        step = FieldMappingStep(self.parent)

        self.assertEqual(step.config.step_number, 4)
        self.assertEqual(step.config.step_name, "Field Mapping")
        self.assertEqual(step.config.step_title, "Step 5: Map CSV Columns to OFX Fields")

    def test_step_number_is_four(self):
        """Test step_number is 4 (Step 5 is index 4)."""
        step = FieldMappingStep(self.parent)

        self.assertEqual(step.config.step_number, 4)

    def test_step_name_is_field_mapping(self):
        """Test step_name is 'Field Mapping'."""
        step = FieldMappingStep(self.parent)

        self.assertEqual(step.config.step_name, "Field Mapping")

    def test_parent_reference_is_set_correctly(self):
        """Test parent reference is stored correctly."""
        step = FieldMappingStep(self.parent)

        self.assertIs(step.parent, self.parent)

    def test_widgets_dict_is_empty_before_ui_creation(self):
        """Test widgets dictionary is empty before UI creation."""
        step = FieldMappingStep(self.parent)

        self.assertEqual(len(step._widgets), 0)
        self.assertIsInstance(step._widgets, dict)


class TestFieldMappingStepUICreation(unittest.TestCase):
    """Test FieldMappingStep UI creation and widget creation."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()
        self.step = FieldMappingStep(self.parent)
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
        self.assertEqual(self.step.container['text'], "Step 5: Map CSV Columns to OFX Fields")

    def test_create_ui_with_csv_headers(self):
        """Test UI creates successfully when CSV headers are available."""
        # Parent has csv_headers
        self.parent.csv_headers = ['Date', 'Amount', 'Description']

        # Create UI
        self.step.create(self.container)

        # Verify container was created
        self.assertIsNotNone(self.step.container)

        # Verify field mapping widgets were created
        self.assertIn('date_combo', self.step._widgets)
        self.assertIn('amount_combo', self.step._widgets)
        self.assertIn('description_combo', self.step._widgets)

    def test_create_ui_without_csv_headers(self):
        """Test UI shows error message when no CSV headers available."""
        # Remove csv_headers from parent
        self.parent.csv_headers = []

        # Create UI
        self.step.create(self.container)

        # Verify container was created
        self.assertIsNotNone(self.step.container)

        # Verify no field mapping widgets were created (error shown instead)
        self.assertNotIn('date_combo', self.step._widgets)
        self.assertNotIn('amount_combo', self.step._widgets)

    def test_field_mapping_widgets_created(self):
        """Test all 5 field mapping comboboxes are created."""
        self.step.create(self.container)

        # Verify all 5 field combos are created
        self.assertIn('date_combo', self.step._widgets)
        self.assertIn('amount_combo', self.step._widgets)
        self.assertIn('description_combo', self.step._widgets)
        self.assertIn('type_combo', self.step._widgets)
        self.assertIn('id_combo', self.step._widgets)

        # Verify they're all comboboxes
        for field in ['date', 'amount', 'description', 'type', 'id']:
            widget = self.step._widgets[f'{field}_combo']
            self.assertIsInstance(widget, ttk.Combobox)

    def test_composite_description_widgets_created(self):
        """Test all 4 composite column selectors and 4 radio buttons are created."""
        self.step.create(self.container)

        # Verify 4 column selectors
        for i in range(4):
            self.assertIn(f'desc_col_{i}_combo', self.step._widgets)
            widget = self.step._widgets[f'desc_col_{i}_combo']
            self.assertIsInstance(widget, ttk.Combobox)

        # Verify 4 separator radio buttons
        separators = [' ', ' - ', ', ', ' | ']
        for sep in separators:
            self.assertIn(f'sep_radio_{sep}', self.step._widgets)
            widget = self.step._widgets[f'sep_radio_{sep}']
            self.assertIsInstance(widget, ttk.Radiobutton)


class TestFieldMappingStepFieldMappings(unittest.TestCase):
    """Test FieldMappingStep field mapping functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()
        self.step = FieldMappingStep(self.parent)
        self.container = ttk.Frame(self.root)

    def tearDown(self):
        """Clean up after tests."""
        self.step.destroy()
        self.root.destroy()

    def test_field_mappings_initialization(self):
        """Test field_mappings dict is created with StringVars for all fields."""
        # Create UI
        self.step.create(self.container)

        # Verify field_mappings dict was created in parent
        self.assertIsInstance(self.parent.field_mappings, dict)

        # Verify all 5 fields have StringVars
        for field in ['date', 'amount', 'description', 'type', 'id']:
            self.assertIn(field, self.parent.field_mappings)
            self.assertIsInstance(self.parent.field_mappings[field], tk.StringVar)

    def test_field_mapping_options(self):
        """Test field mapping comboboxes have correct options."""
        # Create UI
        self.step.create(self.container)

        # Get date combo for testing
        date_combo = self.step._widgets['date_combo']

        # Verify options are NOT_MAPPED + csv_headers
        values = date_combo['values']
        self.assertEqual(values[0], NOT_MAPPED)
        self.assertIn('Date', values)
        self.assertIn('Amount', values)
        self.assertIn('Description', values)
        self.assertIn('Type', values)

    def test_field_mapping_preservation(self):
        """Test existing field mappings are preserved when UI is rebuilt."""
        # Create UI first time
        self.step.create(self.container)

        # Set some field mappings
        self.parent.field_mappings['date'].set('Date')
        self.parent.field_mappings['amount'].set('Amount')

        # Destroy and recreate
        self.step.destroy()
        self.step = FieldMappingStep(self.parent)
        self.step.create(self.container)

        # Verify mappings are preserved
        self.assertEqual(self.parent.field_mappings['date'].get(), 'Date')
        self.assertEqual(self.parent.field_mappings['amount'].get(), 'Amount')

    def test_field_mapping_binding(self):
        """Test field combos are bound to parent.field_mappings StringVars."""
        # Create UI
        self.step.create(self.container)

        # Get combo widget
        date_combo = self.step._widgets['date_combo']

        # Verify textvariable is bound to parent's StringVar
        # Note: combo['textvariable'] returns variable name string, not object
        # Instead, verify by changing parent var and checking combo value
        self.parent.field_mappings['date'].set('Date')
        self.assertEqual(date_combo.get(), 'Date')

        # Verify changing to another value also works
        self.parent.field_mappings['date'].set('Amount')
        self.assertEqual(date_combo.get(), 'Amount')


class TestFieldMappingStepCompositeDescription(unittest.TestCase):
    """Test FieldMappingStep composite description functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()
        self.step = FieldMappingStep(self.parent)
        self.container = ttk.Frame(self.root)

    def tearDown(self):
        """Clean up after tests."""
        self.step.destroy()
        self.root.destroy()

    def test_composite_columns_initialization(self):
        """Test description_columns list is created with 4 StringVars."""
        # Create UI
        self.step.create(self.container)

        # Verify description_columns list was created in parent
        self.assertIsInstance(self.parent.description_columns, list)
        self.assertEqual(len(self.parent.description_columns), 4)

        # Verify all are StringVars initialized to NOT_SELECTED
        for var in self.parent.description_columns:
            self.assertIsInstance(var, tk.StringVar)
            self.assertEqual(var.get(), NOT_SELECTED)

    def test_composite_separator_options(self):
        """Test 4 radio buttons exist with correct separator values."""
        # Create UI
        self.step.create(self.container)

        # Verify all 4 separator radio buttons exist
        separators = [' ', ' - ', ', ', ' | ']
        for sep in separators:
            self.assertIn(f'sep_radio_{sep}', self.step._widgets)

    def test_composite_default_separator(self):
        """Test default separator is space ' '."""
        # Create UI
        self.step.create(self.container)

        # Verify default separator is space
        self.assertEqual(self.parent.description_separator.get(), ' ')

    def test_composite_binding(self):
        """Test composite widgets are bound to parent variables."""
        # Create UI
        self.step.create(self.container)

        # Verify column combos are bound by changing parent var and checking combo value
        for i in range(4):
            combo = self.step._widgets[f'desc_col_{i}_combo']
            # Set parent var and verify combo reflects it
            self.parent.description_columns[i].set('Date')
            self.assertEqual(combo.get(), 'Date')

        # Verify separator radios are bound by changing parent var and checking value
        # Set to dash separator
        self.parent.description_separator.set(' - ')
        # The active radio should have this value
        # We can't easily check which radio is selected, but we can verify the var works
        self.assertEqual(self.parent.description_separator.get(), ' - ')


class TestFieldMappingStepDataCollection(unittest.TestCase):
    """Test FieldMappingStep data collection functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()
        self.step = FieldMappingStep(self.parent)
        self.container = ttk.Frame(self.root)
        self.step.create(self.container)

    def tearDown(self):
        """Clean up after tests."""
        self.step.destroy()
        self.root.destroy()

    def test_collect_data_returns_correct_structure(self):
        """Test _collect_data() returns correct data structure."""
        # Set some values
        self.parent.field_mappings['date'].set('Date')
        self.parent.field_mappings['amount'].set('Amount')
        self.parent.description_columns[0].set('Description')

        # Collect data
        data = self.step._collect_data()

        # Verify data structure
        self.assertIn('field_mappings', data)
        self.assertIn('description_columns', data)
        self.assertIn('description_separator', data)

        # Verify types
        self.assertIsInstance(data['field_mappings'], dict)
        self.assertIsInstance(data['description_columns'], list)
        self.assertIsInstance(data['description_separator'], str)

    def test_collect_data_field_mappings(self):
        """Test field_mappings dict has all 5 fields with correct values."""
        # Set field mappings
        self.parent.field_mappings['date'].set('Date')
        self.parent.field_mappings['amount'].set('Amount')
        self.parent.field_mappings['description'].set('Description')
        self.parent.field_mappings['type'].set(NOT_MAPPED)
        self.parent.field_mappings['id'].set(NOT_MAPPED)

        # Collect data
        data = self.step._collect_data()
        mappings = data['field_mappings']

        # Verify all 5 fields present
        self.assertEqual(len(mappings), 5)
        self.assertIn('date', mappings)
        self.assertIn('amount', mappings)
        self.assertIn('description', mappings)
        self.assertIn('type', mappings)
        self.assertIn('id', mappings)

        # Verify values
        self.assertEqual(mappings['date'], 'Date')
        self.assertEqual(mappings['amount'], 'Amount')
        self.assertEqual(mappings['description'], 'Description')
        self.assertEqual(mappings['type'], NOT_MAPPED)
        self.assertEqual(mappings['id'], NOT_MAPPED)

    def test_collect_data_composite_description(self):
        """Test description_columns list has 4 entries."""
        # Set composite columns
        self.parent.description_columns[0].set('Date')
        self.parent.description_columns[1].set('Description')
        self.parent.description_columns[2].set(NOT_SELECTED)
        self.parent.description_columns[3].set(NOT_SELECTED)
        self.parent.description_separator.set(' - ')

        # Collect data
        data = self.step._collect_data()

        # Verify composite data
        columns = data['description_columns']
        self.assertEqual(len(columns), 4)
        self.assertEqual(columns[0], 'Date')
        self.assertEqual(columns[1], 'Description')
        self.assertEqual(columns[2], NOT_SELECTED)
        self.assertEqual(columns[3], NOT_SELECTED)

        # Verify separator
        self.assertEqual(data['description_separator'], ' - ')


class TestFieldMappingStepValidation(unittest.TestCase):
    """Test FieldMappingStep validation logic."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()
        self.step = FieldMappingStep(self.parent)
        self.container = ttk.Frame(self.root)
        self.step.create(self.container)

    def tearDown(self):
        """Clean up after tests."""
        self.step.destroy()
        self.root.destroy()

    def test_validate_success_with_required_fields(self):
        """Test validation succeeds when date and amount are mapped."""
        # Map required fields
        self.parent.field_mappings['date'].set('Date')
        self.parent.field_mappings['amount'].set('Amount')
        self.parent.field_mappings['description'].set('Description')

        # Validate
        result = self.step.validate()

        # Should be valid
        self.assertTrue(result.is_valid)
        self.assertIsNone(result.error_message)

    def test_validate_fail_missing_date(self):
        """Test validation fails when date is not mapped."""
        # Map only amount
        self.parent.field_mappings['date'].set(NOT_MAPPED)
        self.parent.field_mappings['amount'].set('Amount')
        self.parent.field_mappings['description'].set('Description')

        # Validate
        result = self.step.validate()

        # Should be invalid
        self.assertFalse(result.is_valid)
        self.assertIsNotNone(result.error_message)
        self.assertIn('date', result.error_message.lower())

    def test_validate_fail_missing_amount(self):
        """Test validation fails when amount is not mapped."""
        # Map only date
        self.parent.field_mappings['date'].set('Date')
        self.parent.field_mappings['amount'].set(NOT_MAPPED)
        self.parent.field_mappings['description'].set('Description')

        # Validate
        result = self.step.validate()

        # Should be invalid
        self.assertFalse(result.is_valid)
        self.assertIsNotNone(result.error_message)
        self.assertIn('amount', result.error_message.lower())

    def test_validate_success_with_description_field(self):
        """Test validation succeeds with description field mapped."""
        # Map required fields + description
        self.parent.field_mappings['date'].set('Date')
        self.parent.field_mappings['amount'].set('Amount')
        self.parent.field_mappings['description'].set('Description')

        # Validate
        result = self.step.validate()

        # Should be valid
        self.assertTrue(result.is_valid)
        self.assertIsNone(result.error_message)

    def test_validate_success_with_composite_description(self):
        """Test validation succeeds with composite description configured."""
        # Map required fields
        self.parent.field_mappings['date'].set('Date')
        self.parent.field_mappings['amount'].set('Amount')
        self.parent.field_mappings['description'].set(NOT_MAPPED)

        # Set composite description
        self.parent.description_columns[0].set('Description')
        self.parent.description_columns[1].set('Type')

        # Validate
        result = self.step.validate()

        # Should be valid
        self.assertTrue(result.is_valid)
        self.assertIsNone(result.error_message)

    def test_validate_fail_no_description(self):
        """Test validation fails when neither description field nor composite is configured."""
        # Map only required fields, no description
        self.parent.field_mappings['date'].set('Date')
        self.parent.field_mappings['amount'].set('Amount')
        self.parent.field_mappings['description'].set(NOT_MAPPED)

        # No composite description
        for col in self.parent.description_columns:
            col.set(NOT_SELECTED)

        # Validate
        result = self.step.validate()

        # Should be invalid
        self.assertFalse(result.is_valid)
        self.assertIsNotNone(result.error_message)
        self.assertIn('description', result.error_message.lower())


class TestFieldMappingStepLifecycle(unittest.TestCase):
    """Test FieldMappingStep lifecycle management."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()
        self.step = FieldMappingStep(self.parent)
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


class TestFieldMappingStepLayout(unittest.TestCase):
    """Test FieldMappingStep layout configuration."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()
        self.step = FieldMappingStep(self.parent)
        self.container = ttk.Frame(self.root)
        self.step.create(self.container)

    def tearDown(self):
        """Clean up after tests."""
        self.step.destroy()
        self.root.destroy()

    def test_configure_layout_sets_column_weight(self):
        """Test _configure_layout() sets column 1 weight for expansion."""
        # Column 1 should have weight=1 for combobox expansion
        # Get column weights by checking grid_columnconfigure
        weight = self.step.container.grid_columnconfigure(1, 'weight')
        self.assertEqual(weight, 1)

    def test_grid_configuration_allows_expansion(self):
        """Test proper grid weights are set for container expansion."""
        # Verify column 1 (combobox column) is expandable
        weight = self.step.container.grid_columnconfigure(1, 'weight')
        self.assertEqual(weight, 1)

        # Verify other columns have default weight (0)
        weight_col0 = self.step.container.grid_columnconfigure(0, 'weight')
        weight_col2 = self.step.container.grid_columnconfigure(2, 'weight')
        # Default weight is typically 0 or empty
        self.assertIn(weight_col0, [0, ''])
        self.assertIn(weight_col2, [0, ''])


class TestFieldMappingStepEdgeCases(unittest.TestCase):
    """Test FieldMappingStep edge cases and error scenarios."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()
        self.step = FieldMappingStep(self.parent)
        self.container = ttk.Frame(self.root)

    def tearDown(self):
        """Clean up after tests."""
        self.step.destroy()
        self.root.destroy()

    def test_handles_missing_csv_headers(self):
        """Test step handles missing csv_headers gracefully."""
        # Set empty csv_headers
        self.parent.csv_headers = []

        # Create should not crash
        self.step.create(self.container)

        # Verify container was created
        self.assertIsNotNone(self.step.container)

    def test_handles_none_csv_headers(self):
        """Test step handles None csv_headers gracefully."""
        # Set None csv_headers
        self.parent.csv_headers = None

        # Create should not crash
        self.step.create(self.container)

        # Verify container was created
        self.assertIsNotNone(self.step.container)

    def test_preserves_partial_mappings(self):
        """Test step preserves partial field mappings on rebuild."""
        # Create initial UI
        self.step.create(self.container)

        # Set partial mappings
        self.parent.field_mappings['date'].set('Date')
        self.parent.field_mappings['amount'].set(NOT_MAPPED)

        # Destroy and recreate
        self.step.destroy()
        self.step = FieldMappingStep(self.parent)
        self.step.create(self.container)

        # Verify partial mappings preserved
        self.assertEqual(self.parent.field_mappings['date'].get(), 'Date')
        self.assertEqual(self.parent.field_mappings['amount'].get(), NOT_MAPPED)

    def test_handles_non_dict_field_mappings(self):
        """Test step handles non-dict field_mappings gracefully."""
        # Set field_mappings to non-dict
        self.parent.field_mappings = None

        # Create should not crash
        self.step.create(self.container)

        # Verify field_mappings was recreated as dict
        self.assertIsInstance(self.parent.field_mappings, dict)

    def test_handles_non_list_description_columns(self):
        """Test step handles non-list description_columns gracefully."""
        # Set description_columns to non-list
        self.parent.description_columns = None

        # Create should not crash
        self.step.create(self.container)

        # Verify description_columns was recreated as list
        self.assertIsInstance(self.parent.description_columns, list)
        self.assertEqual(len(self.parent.description_columns), 4)

    def test_handles_missing_description_separator(self):
        """Test step handles missing description_separator gracefully."""
        # Set description_separator to None
        self.parent.description_separator = None

        # Create should not crash
        self.step.create(self.container)

        # Verify description_separator was created with default
        self.assertIsInstance(self.parent.description_separator, tk.StringVar)
        self.assertEqual(self.parent.description_separator.get(), ' ')


if __name__ == '__main__':
    unittest.main()
