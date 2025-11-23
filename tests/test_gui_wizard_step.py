"""
Unit tests for gui_wizard_step module.

Tests the abstract base class WizardStep and supporting dataclasses
(StepConfig and StepData) for the wizard step framework.
"""

import unittest
import tkinter as tk
from tkinter import ttk
from src.gui_wizard_step import WizardStep, StepConfig, StepData


class MockConverterGUI:
    """Mock ConverterGUI for testing WizardStep."""

    def __init__(self, root=None):
        """Initialize mock parent GUI with common attributes."""
        # Create a root if not provided for StringVar
        if root is None:
            self.root = tk.Tk()
            self.root.withdraw()  # Hide the window
            self._owns_root = True
        else:
            self.root = root
            self._owns_root = False

        self.csv_file = tk.StringVar(master=self.root, value='')
        self.csv_headers = []
        self.csv_data = []
        self.log_messages = []

    def _log(self, message: str):
        """Mock logging method."""
        self.log_messages.append(message)

    def destroy(self):
        """Clean up root if we own it."""
        if self._owns_root and self.root:
            try:
                self.root.destroy()
            except:
                pass


class MockWizardStep(WizardStep):
    """
    Concrete implementation of WizardStep for testing.

    This mock implementation provides minimal functionality to test
    the base class behavior without requiring actual GUI components.
    """

    def __init__(self, parent, config: StepConfig):
        """Initialize mock wizard step."""
        super().__init__(parent, config)
        self.build_ui_called = False
        self.collect_data_called = False
        self.validate_data_called = False
        self.mock_data = {}
        self.mock_validation_result = (True, None)

    def _build_ui(self):
        """Build mock UI elements."""
        self.build_ui_called = True
        # Create a simple label widget for testing
        label = ttk.Label(self.container, text="Mock Step")
        label.grid(row=0, column=0)
        self._widgets['label'] = label

    def _collect_data(self):
        """Collect mock data from UI."""
        self.collect_data_called = True
        return self.mock_data

    def _validate_data(self, data):
        """Validate mock data."""
        self.validate_data_called = True
        return self.mock_validation_result


# === Dataclass Tests ===

class TestStepConfig(unittest.TestCase):
    """Test StepConfig dataclass."""

    def test_step_config_initialization_with_all_fields(self):
        """Test StepConfig initialization with all fields provided."""
        config = StepConfig(
            step_number=0,
            step_name="Test Step",
            step_title="Step 1: Test Step",
            is_required=True,
            can_go_back=True,
            show_next=True,
            show_convert=False
        )

        self.assertEqual(config.step_number, 0)
        self.assertEqual(config.step_name, "Test Step")
        self.assertEqual(config.step_title, "Step 1: Test Step")
        self.assertTrue(config.is_required)
        self.assertTrue(config.can_go_back)
        self.assertTrue(config.show_next)
        self.assertFalse(config.show_convert)

    def test_step_config_initialization_with_defaults(self):
        """Test StepConfig initialization with default values."""
        config = StepConfig(
            step_number=1,
            step_name="Another Step",
            step_title="Step 2: Another Step"
        )

        self.assertEqual(config.step_number, 1)
        self.assertEqual(config.step_name, "Another Step")
        self.assertEqual(config.step_title, "Step 2: Another Step")
        # Check defaults
        self.assertTrue(config.is_required)
        self.assertTrue(config.can_go_back)
        self.assertTrue(config.show_next)
        self.assertFalse(config.show_convert)

    def test_step_config_field_types(self):
        """Test StepConfig field types are correct."""
        config = StepConfig(
            step_number=0,
            step_name="Test",
            step_title="Test Title"
        )

        self.assertIsInstance(config.step_number, int)
        self.assertIsInstance(config.step_name, str)
        self.assertIsInstance(config.step_title, str)
        self.assertIsInstance(config.is_required, bool)
        self.assertIsInstance(config.can_go_back, bool)
        self.assertIsInstance(config.show_next, bool)
        self.assertIsInstance(config.show_convert, bool)

    def test_step_config_custom_values(self):
        """Test StepConfig with custom non-default values."""
        config = StepConfig(
            step_number=5,
            step_name="Final Step",
            step_title="Step 6: Completion",
            is_required=False,
            can_go_back=False,
            show_next=False,
            show_convert=True
        )

        self.assertEqual(config.step_number, 5)
        self.assertFalse(config.is_required)
        self.assertFalse(config.can_go_back)
        self.assertFalse(config.show_next)
        self.assertTrue(config.show_convert)


class TestStepData(unittest.TestCase):
    """Test StepData dataclass."""

    def test_step_data_initialization_with_all_fields(self):
        """Test StepData initialization with all fields provided."""
        data = StepData(
            is_valid=True,
            error_message=None,
            data={'field1': 'value1', 'field2': 'value2'}
        )

        self.assertTrue(data.is_valid)
        self.assertIsNone(data.error_message)
        self.assertEqual(data.data, {'field1': 'value1', 'field2': 'value2'})

    def test_step_data_initialization_with_defaults(self):
        """Test StepData initialization with default values."""
        data = StepData(is_valid=True)

        self.assertTrue(data.is_valid)
        self.assertIsNone(data.error_message)
        self.assertEqual(data.data, {})

    def test_step_data_post_init_with_none_data(self):
        """Test StepData __post_init__ converts None to empty dict."""
        data = StepData(is_valid=False, error_message="Error", data=None)

        self.assertFalse(data.is_valid)
        self.assertEqual(data.error_message, "Error")
        self.assertEqual(data.data, {})
        self.assertIsInstance(data.data, dict)

    def test_step_data_invalid_with_error_message(self):
        """Test StepData for invalid case with error message."""
        data = StepData(
            is_valid=False,
            error_message="Validation failed",
            data={}
        )

        self.assertFalse(data.is_valid)
        self.assertEqual(data.error_message, "Validation failed")
        self.assertEqual(data.data, {})


# === Base Class Lifecycle Tests ===

class TestWizardStepLifecycle(unittest.TestCase):
    """Test WizardStep lifecycle methods."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()
        self.config = StepConfig(
            step_number=0,
            step_name="Test Step",
            step_title="Step 1: Test Step"
        )
        self.step = MockWizardStep(self.parent, self.config)
        self.parent_container = ttk.Frame(self.root)

    def tearDown(self):
        """Clean up test fixtures."""
        try:
            self.root.destroy()
        except:
            pass

    def test_create_method_creates_container(self):
        """Test create() method creates container frame."""
        result = self.step.create(self.parent_container)

        self.assertIsNotNone(self.step.container)
        self.assertIsInstance(self.step.container, ttk.LabelFrame)
        self.assertEqual(result, self.step.container)
        self.assertTrue(self.step.build_ui_called)

    def test_show_method_displays_container(self):
        """Test show() method displays the container."""
        self.step.create(self.parent_container)
        self.step.container.grid_remove()  # Hide it first

        self.step.show()

        # Verify container is gridded (visible)
        grid_info = self.step.container.grid_info()
        self.assertIsNotNone(grid_info)
        self.assertIn('row', grid_info)

    def test_hide_method_hides_container(self):
        """Test hide() method hides the container without destroying it."""
        self.step.create(self.parent_container)
        self.step.show()

        self.step.hide()

        # Container should still exist
        self.assertIsNotNone(self.step.container)
        # But grid_info should be empty when hidden with grid_remove()
        grid_info = self.step.container.grid_info()
        self.assertEqual(grid_info, {})

    def test_destroy_method_cleans_up_resources(self):
        """Test destroy() method destroys container and clears widgets."""
        self.step.create(self.parent_container)
        self.step._widgets['test'] = ttk.Label(self.step.container, text="Test")

        self.step.destroy()

        self.assertIsNone(self.step.container)
        self.assertEqual(self.step._widgets, {})

    def test_full_lifecycle_sequence(self):
        """Test full lifecycle: create -> show -> hide -> destroy."""
        # Create
        container = self.step.create(self.parent_container)
        self.assertIsNotNone(container)
        self.assertTrue(self.step.build_ui_called)

        # Show
        self.step.show()
        grid_info = self.step.container.grid_info()
        self.assertIsNotNone(grid_info)

        # Hide
        self.step.hide()
        self.assertIsNotNone(self.step.container)

        # Destroy
        self.step.destroy()
        self.assertIsNone(self.step.container)
        self.assertEqual(self.step._widgets, {})

    def test_create_sets_container_title(self):
        """Test create() sets the container title from config."""
        self.step.create(self.parent_container)

        # LabelFrame text should match config step_title
        self.assertEqual(self.step.container['text'], self.config.step_title)


# === Helper Methods Tests ===

class TestWizardStepHelperMethods(unittest.TestCase):
    """Test WizardStep helper methods."""

    def setUp(self):
        """Set up test fixtures."""
        self.parent = MockConverterGUI()
        self.config = StepConfig(
            step_number=0,
            step_name="Test Step",
            step_title="Step 1: Test Step"
        )
        self.step = MockWizardStep(self.parent, self.config)

    def tearDown(self):
        """Clean up test fixtures."""
        self.parent.destroy()

    def test_log_calls_parent_log_method(self):
        """Test log() calls parent's _log() method."""
        self.step.log("Test message")

        self.assertEqual(len(self.parent.log_messages), 1)
        self.assertEqual(self.parent.log_messages[0], "Test message")

    def test_get_parent_data_with_string_var(self):
        """Test get_parent_data() retrieves value from StringVar."""
        self.parent.csv_file.set('/path/to/file.csv')

        result = self.step.get_parent_data('csv_file')

        self.assertEqual(result, '/path/to/file.csv')

    def test_get_parent_data_with_regular_attribute(self):
        """Test get_parent_data() retrieves value from regular attribute."""
        self.parent.csv_headers = ['Date', 'Amount', 'Description']

        result = self.step.get_parent_data('csv_headers')

        self.assertEqual(result, ['Date', 'Amount', 'Description'])

    def test_get_parent_data_with_default_value(self):
        """Test get_parent_data() returns default when attribute not found."""
        result = self.step.get_parent_data('nonexistent_key', 'default_value')

        self.assertEqual(result, 'default_value')

    def test_set_parent_data_with_string_var(self):
        """Test set_parent_data() updates StringVar value."""
        self.step.set_parent_data('csv_file', '/new/path/file.csv')

        self.assertEqual(self.parent.csv_file.get(), '/new/path/file.csv')

    def test_set_parent_data_with_regular_attribute(self):
        """Test set_parent_data() updates regular attribute."""
        self.step.set_parent_data('csv_headers', ['Col1', 'Col2'])

        self.assertEqual(self.parent.csv_headers, ['Col1', 'Col2'])


# === Validation Tests ===

class TestWizardStepValidation(unittest.TestCase):
    """Test WizardStep validation orchestration."""

    def setUp(self):
        """Set up test fixtures."""
        self.parent = MockConverterGUI()
        self.config = StepConfig(
            step_number=0,
            step_name="Test Step",
            step_title="Step 1: Test Step"
        )
        self.step = MockWizardStep(self.parent, self.config)

    def tearDown(self):
        """Clean up test fixtures."""
        self.parent.destroy()

    def test_validate_calls_collect_and_validate_methods(self):
        """Test validate() calls both _collect_data() and _validate_data()."""
        self.step.mock_data = {'field': 'value'}
        self.step.mock_validation_result = (True, None)

        result = self.step.validate()

        self.assertTrue(self.step.collect_data_called)
        self.assertTrue(self.step.validate_data_called)

    def test_validate_success_returns_step_data_with_data(self):
        """Test validate() returns StepData with data when validation succeeds."""
        self.step.mock_data = {'field1': 'value1', 'field2': 'value2'}
        self.step.mock_validation_result = (True, None)

        result = self.step.validate()

        self.assertIsInstance(result, StepData)
        self.assertTrue(result.is_valid)
        self.assertIsNone(result.error_message)
        self.assertEqual(result.data, {'field1': 'value1', 'field2': 'value2'})

    def test_validate_failure_returns_step_data_with_error(self):
        """Test validate() returns StepData with error when validation fails."""
        self.step.mock_data = {'field': 'invalid_value'}
        self.step.mock_validation_result = (False, "Invalid data")

        result = self.step.validate()

        self.assertIsInstance(result, StepData)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.error_message, "Invalid data")
        self.assertEqual(result.data, {})  # Data should be empty on failure

    def test_validate_returns_step_data_structure(self):
        """Test validate() returns properly structured StepData."""
        self.step.mock_data = {'test': 'data'}
        self.step.mock_validation_result = (True, None)

        result = self.step.validate()

        # Check structure
        self.assertIsInstance(result, StepData)
        self.assertIsInstance(result.is_valid, bool)
        self.assertIsInstance(result.data, dict)
        # error_message can be None or str
        self.assertTrue(result.error_message is None or
                        isinstance(result.error_message, str))


# === Concrete Implementation Tests ===

class TestConcreteImplementation(unittest.TestCase):
    """Test concrete implementation behavior."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()
        self.config = StepConfig(
            step_number=0,
            step_name="Test Step",
            step_title="Step 1: Test Step"
        )

    def tearDown(self):
        """Clean up test fixtures."""
        try:
            self.root.destroy()
        except:
            pass

    def test_cannot_instantiate_abstract_wizard_step(self):
        """Test that WizardStep cannot be instantiated directly."""
        with self.assertRaises(TypeError):
            step = WizardStep(self.parent, self.config)

    def test_concrete_implementation_works_correctly(self):
        """Test that concrete MockWizardStep implementation works."""
        step = MockWizardStep(self.parent, self.config)

        self.assertIsNotNone(step)
        self.assertEqual(step.parent, self.parent)
        self.assertEqual(step.config, self.config)

    def test_full_lifecycle_with_mock_parent(self):
        """Test full lifecycle with mock parent GUI."""
        step = MockWizardStep(self.parent, self.config)
        parent_container = ttk.Frame(self.root)

        # Create step
        container = step.create(parent_container)
        self.assertIsNotNone(container)
        self.assertTrue(step.build_ui_called)
        self.assertIn('label', step._widgets)

        # Show step
        step.show()
        grid_info = step.container.grid_info()
        self.assertIsNotNone(grid_info)

        # Validate step
        step.mock_data = {'test_field': 'test_value'}
        step.mock_validation_result = (True, None)
        result = step.validate()
        self.assertTrue(result.is_valid)
        self.assertEqual(result.data['test_field'], 'test_value')

        # Hide step
        step.hide()
        self.assertIsNotNone(step.container)

        # Destroy step
        step.destroy()
        self.assertIsNone(step.container)

    def test_data_flow_collection_to_validation(self):
        """Test data flow from collection through validation to return."""
        step = MockWizardStep(self.parent, self.config)

        # Set up test data
        test_data = {
            'csv_file': '/path/to/file.csv',
            'delimiter': ',',
            'decimal_separator': '.'
        }
        step.mock_data = test_data
        step.mock_validation_result = (True, None)

        # Execute validation
        result = step.validate()

        # Verify data flow
        self.assertTrue(step.collect_data_called)
        self.assertTrue(step.validate_data_called)
        self.assertTrue(result.is_valid)
        self.assertEqual(result.data, test_data)

    def test_error_handling_in_validation(self):
        """Test error handling during validation process."""
        step = MockWizardStep(self.parent, self.config)

        # Set up error condition
        step.mock_data = {'invalid': 'data'}
        error_message = "Please select a valid CSV file"
        step.mock_validation_result = (False, error_message)

        # Execute validation
        result = step.validate()

        # Verify error handling
        self.assertFalse(result.is_valid)
        self.assertEqual(result.error_message, error_message)
        self.assertEqual(result.data, {})

    def test_multiple_validate_calls(self):
        """Test that validate() can be called multiple times."""
        step = MockWizardStep(self.parent, self.config)

        # First validation
        step.mock_data = {'field': 'value1'}
        step.mock_validation_result = (True, None)
        result1 = step.validate()
        self.assertTrue(result1.is_valid)
        self.assertEqual(result1.data['field'], 'value1')

        # Second validation with different data
        step.mock_data = {'field': 'value2'}
        step.mock_validation_result = (True, None)
        result2 = step.validate()
        self.assertTrue(result2.is_valid)
        self.assertEqual(result2.data['field'], 'value2')

        # Third validation with error
        step.mock_data = {'field': 'invalid'}
        step.mock_validation_result = (False, "Error occurred")
        result3 = step.validate()
        self.assertFalse(result3.is_valid)
        self.assertEqual(result3.error_message, "Error occurred")

    def test_widget_storage_in_build_ui(self):
        """Test that widgets are properly stored in _widgets dict."""
        step = MockWizardStep(self.parent, self.config)
        parent_container = ttk.Frame(self.root)

        step.create(parent_container)

        # Check that widgets were stored
        self.assertIn('label', step._widgets)
        self.assertIsInstance(step._widgets['label'], ttk.Label)

    def test_configure_layout_is_called(self):
        """Test that _configure_layout() is called during create()."""
        step = MockWizardStep(self.parent, self.config)
        parent_container = ttk.Frame(self.root)

        step.create(parent_container)

        # Check that layout was configured (column 0 should have weight)
        column_config = step.container.grid_columnconfigure(0)
        self.assertIsNotNone(column_config)


if __name__ == '__main__':
    unittest.main()
