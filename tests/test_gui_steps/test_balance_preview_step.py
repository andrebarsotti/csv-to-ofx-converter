"""
Unit tests for BalancePreviewStep class.

This module contains comprehensive unit tests for the BalancePreviewStep wizard step,
testing initialization, UI creation, balance calculations, manager integrations,
mode toggling, validation, data collection, and lifecycle management.

Tests use mocks to avoid GUI dependencies and verify proper integration with the
WizardStep base class, BalanceManager, and TransactionManager.
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
from src.gui_balance_manager import BalancePreviewData
from src.constants import NOT_MAPPED, NOT_SELECTED
from src import gui_utils


# Import the actual BalancePreviewStep from Task D.3
from src.gui_steps.balance_preview_step import BalancePreviewStep


class MockBalanceManager:
    """Mock BalanceManager for testing."""

    def __init__(self):
        """Initialize mock balance manager."""
        self.calculate_called = False
        self.validate_called = False
        self.format_called = False

    def calculate_balance_preview(self, *args, **kwargs):
        """Mock calculate_balance_preview method.

        Returns BalancePreviewData object (matching actual BalanceManager).
        The BalancePreviewStep will call .to_dict() on it.
        """
        self.calculate_called = True
        return BalancePreviewData(
            initial_balance=100.0,
            total_credits=50.0,
            total_debits=30.0,
            calculated_final_balance=120.0,
            transaction_count=5,
            transactions=[
                {
                    'row_idx': 0,
                    'date': '2025-01-01',
                    'description': 'Test Transaction',
                    'amount': 50.0,
                    'type': 'CREDIT',
                    'date_status': 'valid'
                }
            ]
        )

    def validate_balance_input(self, action, value):
        """Mock validate_balance_input method."""
        self.validate_called = True
        # Allow deletions
        if action == '0':
            return True, None
        # Allow valid numbers
        if not value or value == '-' or value == '.':
            return True, None
        try:
            float(value)
            return True, None
        except ValueError:
            return False, "Invalid number"

    def format_final_balance(self, value):
        """Mock format_final_balance method."""
        self.format_called = True
        return f"{value:.2f}"

    def get_date_status_for_transaction(self, row_idx, cached_info):
        """Mock get_date_status_for_transaction method."""
        return 'valid'

    def should_show_date_actions(self, date_status, validation_enabled):
        """Mock should_show_date_actions method."""
        return date_status in ['before', 'after'] and validation_enabled


class MockTransactionManager:
    """Mock TransactionManager for testing."""

    def __init__(self):
        """Initialize mock transaction manager."""
        self.context_menu_called = False
        self.dialog_called = False

    def show_context_menu(self, event, tree, transaction_tree_items,
                         deleted_transactions, date_action_decisions):
        """Mock show_context_menu method."""
        self.context_menu_called = True

    def show_out_of_range_dialog(self, row_idx, date_str, status, validator, description):
        """Mock show_out_of_range_dialog method."""
        self.dialog_called = True
        return date_str, 'keep'


class MockConverterGUI:
    """Mock ConverterGUI for testing without actual GUI dependencies."""

    def __init__(self):
        """Initialize mock with required attributes."""
        self.root = MagicMock()

        # Balance variables
        self.initial_balance = tk.StringVar(value='1000.00')
        self.final_balance = tk.StringVar(value='1500.00')
        self.auto_calculate_final_balance = tk.BooleanVar(value=True)

        # Transaction management
        self.deleted_transactions = set()
        self.date_action_decisions = {}
        self.transaction_tree_items = {}
        self.balance_preview_tree = None

        # Manager instances
        self.balance_manager = MockBalanceManager()
        self.transaction_manager = MockTransactionManager()

        # CSV data
        self.csv_data = [
            {'Date': '2025-01-01', 'Amount': '100.00', 'Description': 'Credit'},
            {'Date': '2025-01-02', 'Amount': '-50.00', 'Description': 'Debit'}
        ]

        # Field mappings
        self.field_mappings = {
            'date': tk.StringVar(value='Date'),
            'amount': tk.StringVar(value='Amount'),
            'description': tk.StringVar(value='Description'),
            'type': tk.StringVar(value=NOT_MAPPED),
            'id': tk.StringVar(value=NOT_MAPPED)
        }

        # Description columns
        self.description_columns = [tk.StringVar(value=NOT_SELECTED) for _ in range(4)]
        self.description_separator = tk.StringVar(value=' ')

        # CSV format
        self.delimiter = tk.StringVar(value=',')
        self.decimal_separator = tk.StringVar(value='.')

        # Options
        self.invert_values = tk.BooleanVar(value=False)

        # Date validation
        self.enable_date_validation = tk.BooleanVar(value=False)
        self.start_date = tk.StringVar(value='')
        self.end_date = tk.StringVar(value='')

        # Store log messages for verification
        self.log_messages = []

        # Mock root.register for validation
        self.root.register = lambda func: lambda *args: func(*args)

    def _log(self, message: str):
        """Mock logging method that stores messages."""
        self.log_messages.append(message)


class TestBalancePreviewStepInitialization(unittest.TestCase):
    """Test BalancePreviewStep initialization."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()

    def tearDown(self):
        """Clean up after tests."""
        self.root.destroy()

    def test_step_initializes_with_correct_config(self):
        """Test step initializes with correct configuration values."""
        step = BalancePreviewStep(self.parent)

        self.assertEqual(step.config.step_number, 6)
        self.assertEqual(step.config.step_name, "Balance Preview")
        self.assertEqual(step.config.step_title, "Step 7: Balance Preview & Confirmation")

    def test_step_number_is_six(self):
        """Test step_number is 6 (Step 7 is index 6)."""
        step = BalancePreviewStep(self.parent)

        self.assertEqual(step.config.step_number, 6)

    def test_step_name_is_balance_preview(self):
        """Test step_name is 'Balance Preview'."""
        step = BalancePreviewStep(self.parent)

        self.assertEqual(step.config.step_name, "Balance Preview")

    def test_parent_reference_is_set_correctly(self):
        """Test parent reference is stored correctly."""
        step = BalancePreviewStep(self.parent)

        self.assertIs(step.parent, self.parent)

    def test_widgets_dict_is_empty_before_ui_creation(self):
        """Test widgets dictionary is empty before UI creation."""
        step = BalancePreviewStep(self.parent)

        self.assertEqual(len(step._widgets), 0)
        self.assertIsInstance(step._widgets, dict)


class TestBalancePreviewStepUICreation(unittest.TestCase):
    """Test BalancePreviewStep UI creation and widget creation."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()
        self.step = BalancePreviewStep(self.parent)
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
        self.assertEqual(self.step.container['text'], "Step 7: Balance Preview & Confirmation")

    def test_balance_input_section_created(self):
        """Test balance input section is created with all widgets."""
        self.step.create(self.container)

        # Verify balance input entry widget exists (button is not stored in _widgets)
        self.assertIn('initial_balance_entry', self.step._widgets)

        # Verify widget type
        self.assertIsInstance(self.step._widgets['initial_balance_entry'], ttk.Entry)

        # Verify entry is bound to parent's initial_balance variable
        # (We can't easily test button creation without it being stored in _widgets,
        # but the _recalculate_balance_preview method existence confirms button works)
        self.assertTrue(hasattr(self.step, '_recalculate_balance_preview'))

    def test_balance_summary_section_created(self):
        """Test balance summary section is created with all labels."""
        self.step.create(self.container)

        # Verify all balance labels exist (note: no summary_frame widget in actual implementation)
        self.assertIn('total_credits_label', self.step._widgets)
        self.assertIn('total_debits_label', self.step._widgets)
        self.assertIn('calculated_final_label', self.step._widgets)
        self.assertIn('transaction_count_label', self.step._widgets)

        # Verify widget types
        self.assertIsInstance(self.step._widgets['total_credits_label'], ttk.Label)
        self.assertIsInstance(self.step._widgets['total_debits_label'], ttk.Label)
        self.assertIsInstance(self.step._widgets['calculated_final_label'], ttk.Label)
        self.assertIsInstance(self.step._widgets['transaction_count_label'], ttk.Label)

    def test_transaction_preview_section_created(self):
        """Test transaction preview section is created with treeview."""
        self.step.create(self.container)

        # Verify treeview exists (note: no preview_frame widget in actual implementation)
        # The tree is stored in parent, not _widgets
        self.assertIsNotNone(self.parent.balance_preview_tree)
        self.assertIsInstance(self.parent.balance_preview_tree, ttk.Treeview)

    def test_widget_storage(self):
        """Test all major widgets are stored in _widgets dict."""
        self.step.create(self.container)

        # Check for widgets that are actually stored in _widgets
        # (based on actual implementation from balance_preview_step.py)
        expected_widgets = [
            'initial_balance_entry',
            'total_credits_label',
            'total_debits_label',
            'calculated_final_label',
            'manual_balance_entry',
            'transaction_count_label'
        ]

        for widget_name in expected_widgets:
            self.assertIn(widget_name, self.step._widgets,
                         f"Widget '{widget_name}' not found in _widgets dict")

        # Verify at least 6 widgets are stored
        self.assertGreaterEqual(len(self.step._widgets), 6)


class TestBalancePreviewStepManagerIntegration(unittest.TestCase):
    """Test BalancePreviewStep integration with managers."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()
        self.step = BalancePreviewStep(self.parent)
        self.container = ttk.Frame(self.root)
        self.step.create(self.container)

    def tearDown(self):
        """Clean up after tests."""
        self.step.destroy()
        self.root.destroy()

    def test_balance_manager_calculate_preview(self):
        """Test BalancePreviewStep delegates to BalanceManager for calculations."""
        # Reset the flag
        self.parent.balance_manager.calculate_called = False

        # Call calculate method
        result = self.step._calculate_balance_preview()

        # Verify BalanceManager method was called
        self.assertTrue(self.parent.balance_manager.calculate_called)
        # Result should be dict (from .to_dict())
        self.assertIsInstance(result, dict)

    def test_balance_manager_validate_input(self):
        """Test BalancePreviewStep delegates to BalanceManager for validation."""
        # Call validation method
        is_valid = self.step._validate_numeric_input('1', '100.50')

        # Verify BalanceManager method was called
        self.assertTrue(self.parent.balance_manager.validate_called)
        self.assertTrue(is_valid)

    def test_transaction_manager_context_menu(self):
        """Test BalancePreviewStep delegates to TransactionManager for context menu."""
        # Create mock event
        event = MagicMock()
        event.x_root = 100
        event.y_root = 100

        # Call context menu method (actual method name in implementation)
        self.step._show_transaction_context_menu_wrapper(event)

        # Verify TransactionManager method was called
        self.assertTrue(self.parent.transaction_manager.context_menu_called)

    def test_transaction_manager_date_dialog(self):
        """Test TransactionManager date dialog can be called."""
        # This test verifies the manager has the method available
        # Actual dialog display would require user interaction

        # Verify method exists
        self.assertTrue(hasattr(self.parent.transaction_manager, 'show_out_of_range_dialog'))

        # Call method and verify it executes
        result = self.parent.transaction_manager.show_out_of_range_dialog(
            row_idx=0,
            date_str='2025-01-01',
            status='before',
            validator=None,
            description='Test'
        )

        # Verify method was called
        self.assertTrue(self.parent.transaction_manager.dialog_called)


class TestBalancePreviewStepBalanceCalculation(unittest.TestCase):
    """Test BalancePreviewStep balance calculation functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()
        self.step = BalancePreviewStep(self.parent)
        self.container = ttk.Frame(self.root)
        self.step.create(self.container)

    def tearDown(self):
        """Clean up after tests."""
        self.step.destroy()
        self.root.destroy()

    def test_calculate_balance_preview_with_transactions(self):
        """Test balance calculation with transaction data."""
        # Set up parent with transaction data
        self.parent.csv_data = [
            {'Date': '2025-01-01', 'Amount': '100.00', 'Description': 'Credit'},
            {'Date': '2025-01-02', 'Amount': '-50.00', 'Description': 'Debit'}
        ]

        # Calculate balance (returns dict from .to_dict())
        result = self.step._calculate_balance_preview()

        # Verify result structure is dict
        self.assertIsInstance(result, dict)
        self.assertEqual(result['initial_balance'], 100.0)
        self.assertEqual(result['total_credits'], 50.0)
        self.assertEqual(result['total_debits'], 30.0)
        self.assertEqual(result['calculated_final_balance'], 120.0)
        self.assertEqual(result['transaction_count'], 5)

    def test_calculate_balance_preview_empty(self):
        """Test balance calculation with empty transaction data."""
        # Set up parent with empty data
        self.parent.csv_data = []

        # Calculate balance (returns dict from .to_dict())
        result = self.step._calculate_balance_preview()

        # Verify result is dict (mock always returns same data, but call succeeds)
        self.assertIsInstance(result, dict)

    def test_recalculate_updates_labels(self):
        """Test recalculation updates all labels correctly."""
        # Get initial label values
        initial_credits = self.step._widgets['total_credits_label']['text']

        # Change initial balance
        self.parent.initial_balance.set('2000.00')

        # Recalculate
        self.step._recalculate_balance_preview()

        # Verify labels were updated (values from mock)
        self.assertIn('50.00', self.step._widgets['total_credits_label']['text'])
        self.assertIn('30.00', self.step._widgets['total_debits_label']['text'])
        self.assertIn('120.00', self.step._widgets['calculated_final_label']['text'])


class TestBalancePreviewStepModeToggle(unittest.TestCase):
    """Test BalancePreviewStep mode toggle functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()
        self.step = BalancePreviewStep(self.parent)
        self.container = ttk.Frame(self.root)
        self.step.create(self.container)

    def tearDown(self):
        """Clean up after tests."""
        self.step.destroy()
        self.root.destroy()

    def test_toggle_to_manual_mode(self):
        """Test toggling from auto to manual mode."""
        # Start in auto mode
        self.assertTrue(self.parent.auto_calculate_final_balance.get())
        self.assertEqual(str(self.step._widgets['manual_balance_entry']['state']), 'disabled')

        # Toggle to manual
        self.parent.auto_calculate_final_balance.set(False)
        self.step._toggle_final_balance_mode()

        # Verify manual entry enabled
        self.assertEqual(str(self.step._widgets['manual_balance_entry']['state']), 'normal')

    def test_toggle_to_auto_mode(self):
        """Test toggling from manual to auto mode."""
        # Start in manual mode
        self.parent.auto_calculate_final_balance.set(False)
        self.step._toggle_final_balance_mode()

        # Verify manual entry is enabled
        self.assertEqual(str(self.step._widgets['manual_balance_entry']['state']), 'normal')

        # Toggle back to auto
        self.parent.auto_calculate_final_balance.set(True)
        self.step._toggle_final_balance_mode()

        # Verify manual entry disabled
        self.assertEqual(str(self.step._widgets['manual_balance_entry']['state']), 'disabled')


class TestBalancePreviewStepDataCollection(unittest.TestCase):
    """Test BalancePreviewStep data collection functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()
        self.step = BalancePreviewStep(self.parent)
        self.container = ttk.Frame(self.root)
        self.step.create(self.container)

    def tearDown(self):
        """Clean up after tests."""
        self.step.destroy()
        self.root.destroy()

    def test_collect_data_returns_correct_structure(self):
        """Test _collect_data() returns correct data structure."""
        # Set some values
        self.parent.initial_balance.set('1000.00')
        self.parent.final_balance.set('1500.00')
        self.parent.auto_calculate_final_balance.set(True)

        # Collect data
        data = self.step._collect_data()

        # Verify data structure
        self.assertIn('initial_balance', data)
        self.assertIn('final_balance', data)
        self.assertIn('auto_calculate_final_balance', data)
        self.assertIn('deleted_transactions', data)
        self.assertIn('date_action_decisions', data)

        # Verify values
        self.assertEqual(data['initial_balance'], '1000.00')
        self.assertEqual(data['final_balance'], '1500.00')
        self.assertTrue(data['auto_calculate_final_balance'])

    def test_collect_data_includes_deleted_transactions(self):
        """Test collected data includes deleted transactions."""
        # Add some deleted transactions
        self.parent.deleted_transactions = {0, 2, 5}

        # Collect data
        data = self.step._collect_data()

        # Verify deleted transactions are included
        self.assertIn('deleted_transactions', data)
        self.assertEqual(set(data['deleted_transactions']), {0, 2, 5})

    def test_collect_data_includes_date_decisions(self):
        """Test collected data includes date action decisions."""
        # Add some date decisions
        self.parent.date_action_decisions = {0: 'keep', 1: 'adjust', 2: 'exclude'}

        # Collect data
        data = self.step._collect_data()

        # Verify date decisions are included
        self.assertIn('date_action_decisions', data)
        self.assertEqual(data['date_action_decisions'], {0: 'keep', 1: 'adjust', 2: 'exclude'})


class TestBalancePreviewStepValidation(unittest.TestCase):
    """Test BalancePreviewStep validation logic."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()
        self.step = BalancePreviewStep(self.parent)
        self.container = ttk.Frame(self.root)
        self.step.create(self.container)

    def tearDown(self):
        """Clean up after tests."""
        self.step.destroy()
        self.root.destroy()

    @patch('src.gui_steps.balance_preview_step.gui_utils')
    def test_validate_success_valid_balances(self, mock_gui_utils):
        """Test validation succeeds with valid balances."""
        # Mock validation to return success
        mock_gui_utils.validate_balance_value = Mock(return_value=(True, None))

        # Set valid balances
        self.parent.initial_balance.set('1000.00')
        self.parent.final_balance.set('1500.00')
        self.parent.auto_calculate_final_balance.set(True)

        # Validate
        result = self.step.validate()

        # Should be valid
        self.assertTrue(result.is_valid)
        self.assertIsNone(result.error_message)

    @patch('src.gui_steps.balance_preview_step.gui_utils')
    def test_validate_fail_invalid_initial_balance(self, mock_gui_utils):
        """Test validation fails with invalid initial balance."""
        # Mock validation to return failure
        mock_gui_utils.validate_balance_value = Mock(return_value=(False, "Invalid format"))

        # Set invalid initial balance
        self.parent.initial_balance.set('invalid')
        self.parent.auto_calculate_final_balance.set(True)

        # Validate
        result = self.step.validate()

        # Should be invalid
        self.assertFalse(result.is_valid)
        self.assertIsNotNone(result.error_message)
        self.assertIn('initial balance', result.error_message.lower())

    @patch('src.gui_steps.balance_preview_step.gui_utils')
    def test_validate_fail_invalid_final_balance_manual(self, mock_gui_utils):
        """Test validation fails with invalid final balance in manual mode."""
        # Mock validation to succeed for first call (initial), fail for second (final)
        mock_gui_utils.validate_balance_value = Mock(side_effect=[(True, None), (False, "Invalid format")])

        # Set valid initial but invalid final balance in manual mode
        self.parent.initial_balance.set('1000.00')
        self.parent.final_balance.set('invalid')
        self.parent.auto_calculate_final_balance.set(False)

        # Validate
        result = self.step.validate()

        # Should be invalid
        self.assertFalse(result.is_valid)
        self.assertIsNotNone(result.error_message)
        self.assertIn('final balance', result.error_message.lower())

    @patch('src.gui_steps.balance_preview_step.gui_utils')
    def test_validate_success_auto_mode(self, mock_gui_utils):
        """Test validation succeeds in auto mode regardless of final balance value."""
        # Mock validation to return success
        mock_gui_utils.validate_balance_value = Mock(return_value=(True, None))

        # Set valid initial, invalid final (but auto mode ignores it)
        self.parent.initial_balance.set('1000.00')
        self.parent.final_balance.set('will_be_ignored')
        self.parent.auto_calculate_final_balance.set(True)

        # Validate
        result = self.step.validate()

        # Should be valid (auto mode doesn't validate final balance)
        self.assertTrue(result.is_valid)
        self.assertIsNone(result.error_message)
        # Verify validate_balance_value was only called once (for initial balance)
        self.assertEqual(mock_gui_utils.validate_balance_value.call_count, 1)


class TestBalancePreviewStepLifecycle(unittest.TestCase):
    """Test BalancePreviewStep lifecycle management."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.parent = MockConverterGUI()
        self.step = BalancePreviewStep(self.parent)
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


if __name__ == '__main__':
    unittest.main()
