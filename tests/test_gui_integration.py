"""
Integration tests for the Converter GUI.

These tests verify that the GUI components work together correctly
and that user workflows function as expected.
"""

import unittest
import tkinter as tk
import tempfile
import os
import sys
from src.csv_to_ofx_converter import ConverterGUI

# Skip all GUI tests if SKIP_GUI_TESTS environment variable is set
if os.environ.get('SKIP_GUI_TESTS'):
    raise unittest.SkipTest("GUI tests are disabled in CI environment")


class TestGUIIntegration(unittest.TestCase):
    """Integration tests for ConverterGUI class."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a hidden root window for testing
        self.root = tk.Tk()
        self.root.withdraw()  # Hide window during tests

        # Create GUI instance
        self.gui = ConverterGUI(self.root)

        # Create a temporary CSV file for testing
        self.temp_csv = tempfile.NamedTemporaryFile(
            mode='w', suffix='.csv', delete=False, encoding='utf-8')
        self.temp_csv.write('Date,Description,Amount\n')
        self.temp_csv.write('2025-01-15,Test Transaction,100.50\n')
        self.temp_csv.write('2025-01-16,Another Transaction,-50.25\n')
        self.temp_csv.close()

    def tearDown(self):
        """Clean up test fixtures."""
        # Close GUI window
        try:
            self.root.destroy()
        except Exception:
            pass

        # Remove temporary file
        if os.path.exists(self.temp_csv.name):
            os.unlink(self.temp_csv.name)

    def test_gui_initialization(self):
        """Test that GUI initializes correctly."""
        self.assertIsNotNone(self.gui)
        self.assertEqual(self.gui.current_step, 0)
        self.assertEqual(len(self.gui.steps), 7)
        self.assertEqual(self.gui.steps[0], "File Selection")

    def test_initial_step_is_file_selection(self):
        """Test that GUI starts on file selection step."""
        self.assertEqual(self.gui.current_step, 0)
        # Back button should be disabled on first step
        self.assertEqual(str(self.gui.back_btn['state']), 'disabled')

    def test_step_progression_without_file_fails(self):
        """Test that user cannot progress without selecting a file."""
        # Try to go to next step without selecting file
        initial_step = self.gui.current_step
        result = self.gui._validate_current_step()

        # Should fail validation
        self.assertFalse(result)
        # Should remain on same step
        self.assertEqual(self.gui.current_step, initial_step)

    def test_step_progression_with_valid_file(self):
        """Test that user can progress with valid file selection."""
        # Set a valid CSV file
        self.gui.csv_file.set(self.temp_csv.name)

        # Should pass validation
        result = self.gui._validate_current_step()
        self.assertTrue(result)

        # Progress to next step
        self.gui._go_next()
        self.assertEqual(self.gui.current_step, 1)

    def test_back_navigation(self):
        """Test that back button works correctly."""
        # Progress to step 2
        self.gui.csv_file.set(self.temp_csv.name)
        self.gui._go_next()
        self.assertEqual(self.gui.current_step, 1)

        # Go back
        self.gui._go_back()
        self.assertEqual(self.gui.current_step, 0)

        # Back button should be disabled on first step
        self.assertEqual(str(self.gui.back_btn['state']), 'disabled')

    def test_csv_data_loading(self):
        """Test that CSV data loads correctly."""
        # Set CSV file
        self.gui.csv_file.set(self.temp_csv.name)

        # Load CSV data
        self.gui._load_csv_data()

        # Verify data loaded
        self.assertEqual(len(self.gui.csv_headers), 3)
        self.assertIn('Date', self.gui.csv_headers)
        self.assertIn('Description', self.gui.csv_headers)
        self.assertIn('Amount', self.gui.csv_headers)
        self.assertEqual(len(self.gui.csv_data), 2)

    def test_field_mappings_initialization(self):
        """Test that field mappings are initialized."""
        # Load CSV data first
        self.gui.csv_file.set(self.temp_csv.name)
        self.gui._load_csv_data()

        # Progress to field mapping step (step 4, index 4)
        for _ in range(4):
            self.gui._show_step(self.gui.current_step + 1)

        # Field mappings should exist
        self.assertIn('date', self.gui.field_mappings)
        self.assertIn('amount', self.gui.field_mappings)
        self.assertIn('description', self.gui.field_mappings)

    def test_delimiter_and_decimal_separator_defaults(self):
        """Test that delimiter and decimal separator have correct defaults."""
        self.assertEqual(self.gui.delimiter.get(), ',')
        self.assertEqual(self.gui.decimal_separator.get(), '.')

    def test_invert_values_default(self):
        """Test that invert values is disabled by default."""
        self.assertFalse(self.gui.invert_values.get())

    def test_date_validation_default(self):
        """Test that date validation is disabled by default."""
        self.assertFalse(self.gui.enable_date_validation.get())

    def test_initial_balance_default(self):
        """Test that initial balance defaults to 0.00."""
        self.assertEqual(self.gui.initial_balance.get(), '0.00')

    def test_auto_calculate_final_balance_default(self):
        """Test that auto-calculate final balance is enabled by default."""
        self.assertTrue(self.gui.auto_calculate_final_balance.get())

    def test_clear_resets_to_initial_state(self):
        """Test that clear button resets GUI to initial state."""
        # Make some changes
        self.gui.csv_file.set(self.temp_csv.name)
        self.gui.delimiter.set(';')
        self.gui.account_id.set('12345')
        self.gui._go_next()

        # Clear
        self.gui._clear()

        # Verify reset
        self.assertEqual(self.gui.csv_file.get(), '')
        self.assertEqual(self.gui.delimiter.get(), ',')
        self.assertEqual(self.gui.account_id.get(), '')
        self.assertEqual(self.gui.current_step, 0)
        self.assertEqual(len(self.gui.csv_data), 0)

    def test_deleted_transactions_tracking(self):
        """Test that deleted transactions are tracked correctly."""
        self.assertEqual(len(self.gui.deleted_transactions), 0)

        # Add a deleted transaction
        self.gui.deleted_transactions.add(0)
        self.assertEqual(len(self.gui.deleted_transactions), 1)

        # Clear should reset
        self.gui._clear()
        self.assertEqual(len(self.gui.deleted_transactions), 0)

    def test_date_action_decisions_tracking(self):
        """Test that date action decisions are tracked correctly."""
        self.assertEqual(len(self.gui.date_action_decisions), 0)

        # Add a date action decision
        self.gui.date_action_decisions[0] = 'adjust'
        self.assertEqual(self.gui.date_action_decisions[0], 'adjust')

        # Clear should reset
        self.gui._clear()
        self.assertEqual(len(self.gui.date_action_decisions), 0)


if __name__ == '__main__':
    unittest.main()
