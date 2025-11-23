"""
Unit tests for OFXConfigStep class.

This module contains comprehensive unit tests for the OFXConfigStep wizard step,
testing initialization, UI creation, widget configuration, data collection,
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
from src.gui_steps.ofx_config_step import OFXConfigStep


class MockConverterGUI:
    """Mock ConverterGUI for testing without actual GUI dependencies."""

    def __init__(self):
        """Initialize mock with required attributes."""
        # Create StringVars for OFX configuration
        self.account_id = tk.StringVar(value='')
        self.bank_name = tk.StringVar(value='')
        self.currency = tk.StringVar(value='BRL')  # Default currency
        # Store log messages for verification
        self.log_messages = []

    def _log(self, message: str):
        """Mock logging method that stores messages."""
        self.log_messages.append(message)


class TestOFXConfigStepInitialization(unittest.TestCase):
    """Test OFXConfigStep initialization."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()

    def tearDown(self):
        """Clean up after tests."""
        self.root.destroy()

    def test_step_initializes_with_correct_config(self):
        """Test step initializes with correct configuration values."""
        step = OFXConfigStep(self.parent)

        self.assertEqual(step.config.step_number, 3)
        self.assertEqual(step.config.step_name, "OFX Configuration")
        self.assertEqual(step.config.step_title, "Step 4: OFX Configuration")
        self.assertTrue(step.config.is_required)
        self.assertTrue(step.config.can_go_back)
        self.assertTrue(step.config.show_next)
        self.assertFalse(step.config.show_convert)

    def test_parent_reference_is_set_correctly(self):
        """Test parent reference is stored correctly."""
        step = OFXConfigStep(self.parent)

        self.assertIs(step.parent, self.parent)

    def test_widgets_dict_is_empty_before_ui_creation(self):
        """Test widgets dictionary is empty before UI creation."""
        step = OFXConfigStep(self.parent)

        self.assertEqual(len(step._widgets), 0)
        self.assertIsInstance(step._widgets, dict)


class TestOFXConfigStepUICreation(unittest.TestCase):
    """Test OFXConfigStep UI creation and widget creation."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()
        self.step = OFXConfigStep(self.parent)
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
        self.assertEqual(self.step.container['text'], "Step 4: OFX Configuration")

        # Verify widgets were created
        self.assertGreater(len(self.step._widgets), 0)

    def test_create_builds_account_id_widgets(self):
        """Test create() builds account ID label and entry widgets."""
        self.step.create(self.container)

        # Verify account_id_entry exists in widgets
        self.assertIn('account_id_entry', self.step._widgets)

        # Verify widget type
        self.assertIsInstance(self.step._widgets['account_id_entry'], ttk.Entry)

        # Verify entry is bound to parent's account_id StringVar
        entry = self.step._widgets['account_id_entry']
        textvariable = entry['textvariable']
        self.assertEqual(str(textvariable), str(self.parent.account_id))

    def test_create_builds_bank_name_widgets(self):
        """Test create() builds bank name label and entry widgets."""
        self.step.create(self.container)

        # Verify bank_name_entry exists in widgets
        self.assertIn('bank_name_entry', self.step._widgets)

        # Verify widget type
        self.assertIsInstance(self.step._widgets['bank_name_entry'], ttk.Entry)

        # Verify entry is bound to parent's bank_name StringVar
        entry = self.step._widgets['bank_name_entry']
        textvariable = entry['textvariable']
        self.assertEqual(str(textvariable), str(self.parent.bank_name))

    def test_create_builds_currency_widgets(self):
        """Test create() builds currency label and combobox widgets."""
        self.step.create(self.container)

        # Verify currency_combo exists in widgets
        self.assertIn('currency_combo', self.step._widgets)

        # Verify widget type
        self.assertIsInstance(self.step._widgets['currency_combo'], ttk.Combobox)

        # Verify combobox is bound to parent's currency StringVar
        combo = self.step._widgets['currency_combo']
        textvariable = combo['textvariable']
        self.assertEqual(str(textvariable), str(self.parent.currency))

    def test_create_builds_help_texts(self):
        """Test create() builds help text labels for each field."""
        self.step.create(self.container)

        # Verify container has children (help texts are labels created but not stored in _widgets)
        children = self.step.container.winfo_children()

        # Find labels among children
        labels = [child for child in children if isinstance(child, ttk.Label)]

        # Should have multiple labels:
        # - Description label
        # - Account ID label
        # - Account ID help text
        # - Bank Name label
        # - Bank Name help text
        # - Currency label
        # - Currency help text
        self.assertGreaterEqual(len(labels), 7)


class TestOFXConfigStepLayout(unittest.TestCase):
    """Test OFXConfigStep layout configuration."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()
        self.step = OFXConfigStep(self.parent)
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

        # Verify column 0 (labels) is fixed weight
        col0_weight = self.step.container.grid_columnconfigure(0)['weight']
        self.assertEqual(col0_weight, 0)

        # Verify column 1 (inputs) is expandable
        col1_weight = self.step.container.grid_columnconfigure(1)['weight']
        self.assertEqual(col1_weight, 1)


class TestOFXConfigStepWidgetBehavior(unittest.TestCase):
    """Test OFXConfigStep widget behavior and configuration."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()
        self.step = OFXConfigStep(self.parent)
        self.container = ttk.Frame(self.root)
        self.step.create(self.container)

    def tearDown(self):
        """Clean up after tests."""
        self.step.destroy()
        self.root.destroy()

    def test_currency_combobox_has_correct_values(self):
        """Test currency combobox has correct currency options."""
        combo = self.step._widgets['currency_combo']

        # Verify combobox values
        values = combo['values']
        self.assertEqual(len(values), 4)
        self.assertIn('BRL', values)
        self.assertIn('USD', values)
        self.assertIn('EUR', values)
        self.assertIn('GBP', values)

    def test_entry_widgets_bind_to_parent_stringvars(self):
        """Test entry widgets are bound to parent StringVars and update correctly."""
        # Set values through parent's StringVars
        self.parent.account_id.set('1234567890')
        self.parent.bank_name.set('Test Bank')
        self.parent.currency.set('USD')

        # Verify entries reflect the values
        account_entry = self.step._widgets['account_id_entry']
        bank_entry = self.step._widgets['bank_name_entry']
        currency_combo = self.step._widgets['currency_combo']

        self.assertEqual(account_entry.get(), '1234567890')
        self.assertEqual(bank_entry.get(), 'Test Bank')
        self.assertEqual(currency_combo.get(), 'USD')

    def test_currency_combobox_is_readonly(self):
        """Test currency combobox is configured as readonly."""
        combo = self.step._widgets['currency_combo']

        # Verify readonly state
        self.assertEqual(str(combo['state']), 'readonly')


class TestOFXConfigStepDataCollection(unittest.TestCase):
    """Test OFXConfigStep data collection."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()
        self.step = OFXConfigStep(self.parent)
        self.container = ttk.Frame(self.root)
        self.step.create(self.container)

    def tearDown(self):
        """Clean up after tests."""
        self.step.destroy()
        self.root.destroy()

    def test_collect_data_returns_correct_structure(self):
        """Test _collect_data() returns dict with correct keys."""
        data = self.step._collect_data()

        self.assertIsInstance(data, dict)
        self.assertIn('account_id', data)
        self.assertIn('bank_name', data)
        self.assertIn('currency', data)

    def test_collect_data_gets_values_from_parent_stringvars(self):
        """Test _collect_data() retrieves values from parent StringVars."""
        # Set test values
        self.parent.account_id.set('9876543210')
        self.parent.bank_name.set('My Bank')
        self.parent.currency.set('EUR')

        data = self.step._collect_data()

        self.assertEqual(data['account_id'], '9876543210')
        self.assertEqual(data['bank_name'], 'My Bank')
        self.assertEqual(data['currency'], 'EUR')


class TestOFXConfigStepValidation(unittest.TestCase):
    """Test OFXConfigStep validation logic."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()
        self.step = OFXConfigStep(self.parent)
        self.container = ttk.Frame(self.root)
        self.step.create(self.container)

    def tearDown(self):
        """Clean up after tests."""
        self.step.destroy()
        self.root.destroy()

    def test_validate_always_returns_valid(self):
        """Test validate() always returns is_valid=True (defaults are always provided)."""
        # Test with default values
        result = self.step.validate()
        self.assertIsInstance(result, StepData)
        self.assertTrue(result.is_valid)

        # Test with custom values
        self.parent.account_id.set('12345')
        self.parent.bank_name.set('Custom Bank')
        self.parent.currency.set('GBP')
        result = self.step.validate()
        self.assertTrue(result.is_valid)

    def test_validate_with_empty_values_still_returns_valid(self):
        """Test validate() returns valid even with empty values (defaults will be used)."""
        # Set empty values
        self.parent.account_id.set('')
        self.parent.bank_name.set('')
        self.parent.currency.set('BRL')  # Currency always has a value

        result = self.step.validate()

        # Should still be valid because defaults are always provided
        self.assertTrue(result.is_valid)
        self.assertIsNone(result.error_message)


class TestOFXConfigStepLifecycle(unittest.TestCase):
    """Test OFXConfigStep lifecycle management."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()
        self.step = OFXConfigStep(self.parent)
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
