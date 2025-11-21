"""
Tests for GUI Balance Manager Module
=====================================
Unit tests for the BalanceManager class that handles balance preview
and transaction management.

These tests verify balance calculations, transaction processing, and
data formatting without requiring a GUI display server.
"""

import unittest
from src.gui_balance_manager import BalanceManager, BalancePreviewData
from src.constants import NOT_MAPPED


class MockParentGUI:
    """Mock ConverterGUI for testing BalanceManager."""

    def __init__(self):
        """Initialize mock parent GUI."""
        pass


class TestBalancePreviewData(unittest.TestCase):
    """Test BalancePreviewData class."""

    def test_balance_preview_data_initialization(self):
        """Test BalancePreviewData initialization."""
        data = BalancePreviewData(
            initial_balance=100.0,
            total_credits=50.0,
            total_debits=30.0,
            calculated_final_balance=120.0,
            transaction_count=5,
            transactions=[{'date': '2025-01-01'}]
        )

        self.assertEqual(data.initial_balance, 100.0)
        self.assertEqual(data.total_credits, 50.0)
        self.assertEqual(data.total_debits, 30.0)
        self.assertEqual(data.calculated_final_balance, 120.0)
        self.assertEqual(data.transaction_count, 5)
        self.assertEqual(len(data.transactions), 1)

    def test_balance_preview_data_to_dict(self):
        """Test BalancePreviewData conversion to dictionary."""
        data = BalancePreviewData(
            initial_balance=100.0,
            total_credits=50.0,
            total_debits=30.0,
            calculated_final_balance=120.0,
            transaction_count=5,
            transactions=[]
        )

        result = data.to_dict()

        self.assertIsInstance(result, dict)
        self.assertEqual(result['initial_balance'], 100.0)
        self.assertEqual(result['total_credits'], 50.0)
        self.assertEqual(result['total_debits'], 30.0)
        self.assertEqual(result['calculated_final_balance'], 120.0)
        self.assertEqual(result['transaction_count'], 5)
        self.assertIsInstance(result['transactions'], list)


class TestBalanceManager(unittest.TestCase):
    """Test BalanceManager class."""

    def setUp(self):
        """Set up test fixtures."""
        self.parent = MockParentGUI()
        self.manager = BalanceManager(self.parent)

    def test_balance_manager_initialization(self):
        """Test BalanceManager initialization."""
        self.assertIsNotNone(self.manager)
        self.assertEqual(self.manager.parent, self.parent)

    def test_calculate_balance_preview_empty_data(self):
        """Test balance calculation with empty CSV data."""
        result = self.manager.calculate_balance_preview(
            initial_balance_str='100.00',
            csv_data=[],
            field_mappings={'date': 'Date', 'amount': 'Amount',
                            'description': 'Description', 'type': NOT_MAPPED},
            description_columns=[],
            description_separator=' ',
            delimiter=',',
            decimal_separator='.',
            invert_values=False,
            deleted_transactions=set()
        )

        self.assertIsInstance(result, BalancePreviewData)
        self.assertEqual(result.initial_balance, 100.0)
        self.assertEqual(result.total_credits, 0.0)
        self.assertEqual(result.total_debits, 0.0)
        self.assertEqual(result.calculated_final_balance, 100.0)
        self.assertEqual(result.transaction_count, 0)

    def test_calculate_balance_preview_with_transactions(self):
        """Test balance calculation with transaction data."""
        csv_data = [
            {'Date': '2025-01-01', 'Amount': '100.00', 'Description': 'Credit'},
            {'Date': '2025-01-02', 'Amount': '-50.00', 'Description': 'Debit'}
        ]

        result = self.manager.calculate_balance_preview(
            initial_balance_str='0.00',
            csv_data=csv_data,
            field_mappings={'date': 'Date', 'amount': 'Amount',
                            'description': 'Description', 'type': NOT_MAPPED},
            description_columns=[],
            description_separator=' ',
            delimiter=',',
            decimal_separator='.',
            invert_values=False,
            deleted_transactions=set()
        )

        self.assertEqual(result.transaction_count, 2)
        self.assertEqual(result.total_credits, 100.0)
        self.assertEqual(result.total_debits, 50.0)
        self.assertEqual(result.calculated_final_balance, 50.0)

    def test_calculate_balance_preview_with_deleted_transactions(self):
        """Test balance calculation excluding deleted transactions."""
        csv_data = [
            {'Date': '2025-01-01', 'Amount': '100.00', 'Description': 'Credit'},
            {'Date': '2025-01-02', 'Amount': '-50.00', 'Description': 'Debit'},
            {'Date': '2025-01-03', 'Amount': '25.00', 'Description': 'Credit'}
        ]

        result = self.manager.calculate_balance_preview(
            initial_balance_str='0.00',
            csv_data=csv_data,
            field_mappings={'date': 'Date', 'amount': 'Amount',
                            'description': 'Description', 'type': NOT_MAPPED},
            description_columns=[],
            description_separator=' ',
            delimiter=',',
            decimal_separator='.',
            invert_values=False,
            deleted_transactions={1}  # Delete the debit transaction
        )

        self.assertEqual(result.transaction_count, 2)
        self.assertEqual(result.total_credits, 125.0)
        self.assertEqual(result.total_debits, 0.0)
        self.assertEqual(result.calculated_final_balance, 125.0)

    def test_calculate_balance_preview_with_invert_values(self):
        """Test balance calculation with inverted values."""
        csv_data = [
            {'Date': '2025-01-01', 'Amount': '100.00', 'Description': 'Credit'},
            {'Date': '2025-01-02', 'Amount': '-50.00', 'Description': 'Debit'}
        ]

        result = self.manager.calculate_balance_preview(
            initial_balance_str='0.00',
            csv_data=csv_data,
            field_mappings={'date': 'Date', 'amount': 'Amount',
                            'description': 'Description', 'type': NOT_MAPPED},
            description_columns=[],
            description_separator=' ',
            delimiter=',',
            decimal_separator='.',
            invert_values=True,  # Invert values
            deleted_transactions=set()
        )

        # After inversion: 100.00 -> -100.00 (debit), -50.00 -> 50.00 (credit)
        self.assertEqual(result.transaction_count, 2)
        self.assertEqual(result.total_credits, 50.0)
        self.assertEqual(result.total_debits, 100.0)
        self.assertEqual(result.calculated_final_balance, -50.0)

    def test_format_balance_labels(self):
        """Test formatting balance information for labels."""
        balance_info = BalancePreviewData(
            initial_balance=100.0,
            total_credits=50.0,
            total_debits=30.0,
            calculated_final_balance=120.0,
            transaction_count=5,
            transactions=[]
        )

        labels = self.manager.format_balance_labels(balance_info)

        self.assertIn('total_credits', labels)
        self.assertIn('50.00', labels['total_credits'])
        self.assertIn('total_debits', labels)
        self.assertIn('30.00', labels['total_debits'])
        self.assertIn('calculated_balance', labels)
        self.assertIn('120.00', labels['calculated_balance'])
        self.assertIn('transaction_count', labels)
        self.assertIn('5', labels['transaction_count'])

    def test_get_transaction_preview_values(self):
        """Test formatting transactions for treeview display."""
        transactions = [
            {'date': '2025-01-01', 'description': 'Test Transaction',
             'amount': 100.0, 'type': 'CREDIT', 'date_status': 'valid'},
            {'date': '2025-01-02', 'description': 'Long description ' * 10,
             'amount': -50.0, 'type': 'DEBIT', 'date_status': 'before'}
        ]

        result = self.manager.get_transaction_preview_values(transactions)

        self.assertEqual(len(result), 2)
        # Check first transaction
        date, desc, amount, ttype, tags = result[0]
        self.assertEqual(date, '2025-01-01')
        self.assertEqual(desc, 'Test Transaction')
        self.assertEqual(amount, '100.00')
        self.assertEqual(ttype, 'CREDIT')
        self.assertEqual(tags, [])
        # Check second transaction (truncated description, has tag)
        date, desc, amount, ttype, tags = result[1]
        self.assertEqual(len(desc), 50)  # Truncated to 50 chars
        self.assertEqual(tags, ['date_before'])

    def test_validate_balance_input(self):
        """Test balance input validation."""
        # Test valid inputs
        self.assertTrue(self.manager.validate_balance_input('1', '100'))
        self.assertTrue(self.manager.validate_balance_input('1', '-100'))
        self.assertTrue(self.manager.validate_balance_input('1', '100.50'))
        self.assertTrue(self.manager.validate_balance_input('1', '-100.50'))
        self.assertTrue(self.manager.validate_balance_input('1', ''))
        self.assertTrue(self.manager.validate_balance_input('1', '-'))

        # Deletion is always allowed
        self.assertTrue(self.manager.validate_balance_input('0', 'anything'))

        # Test invalid inputs
        self.assertFalse(self.manager.validate_balance_input('1', 'abc'))
        self.assertFalse(self.manager.validate_balance_input('1', '100.50.25'))

    def test_format_final_balance(self):
        """Test final balance formatting."""
        result = self.manager.format_final_balance(123.456)
        self.assertEqual(result, '123.46')

        result = self.manager.format_final_balance(-50.0)
        self.assertEqual(result, '-50.00')

    def test_get_date_status_for_transaction(self):
        """Test getting date status for a transaction."""
        cached_info = {
            'transactions': [
                {'row_idx': 0, 'date_status': 'valid'},
                {'row_idx': 1, 'date_status': 'before'},
                {'row_idx': 2, 'date_status': 'after'}
            ]
        }

        self.assertEqual(
            self.manager.get_date_status_for_transaction(0, cached_info),
            'valid'
        )
        self.assertEqual(
            self.manager.get_date_status_for_transaction(1, cached_info),
            'before'
        )
        self.assertEqual(
            self.manager.get_date_status_for_transaction(2, cached_info),
            'after'
        )
        self.assertEqual(
            self.manager.get_date_status_for_transaction(99, cached_info),
            'valid'
        )
        self.assertEqual(
            self.manager.get_date_status_for_transaction(0, None),
            'valid'
        )

    def test_should_show_date_actions(self):
        """Test determining if date actions should be shown."""
        # Should show for 'before' status with validation enabled
        self.assertTrue(
            self.manager.should_show_date_actions('before', True)
        )
        # Should show for 'after' status with validation enabled
        self.assertTrue(
            self.manager.should_show_date_actions('after', True)
        )
        # Should not show for 'valid' status
        self.assertFalse(
            self.manager.should_show_date_actions('valid', True)
        )
        # Should not show if validation disabled
        self.assertFalse(
            self.manager.should_show_date_actions('before', False)
        )

    def test_get_date_action_label_texts(self):
        """Test getting date action label texts."""
        # Test with 'keep' action selected
        labels = self.manager.get_date_action_label_texts('keep')
        self.assertIn('✓', labels['keep'])
        self.assertNotIn('✓', labels['adjust'])
        self.assertNotIn('✓', labels['exclude'])

        # Test with 'adjust' action selected
        labels = self.manager.get_date_action_label_texts('adjust')
        self.assertNotIn('✓', labels['keep'])
        self.assertIn('✓', labels['adjust'])
        self.assertNotIn('✓', labels['exclude'])

        # Test with 'exclude' action selected
        labels = self.manager.get_date_action_label_texts('exclude')
        self.assertNotIn('✓', labels['keep'])
        self.assertNotIn('✓', labels['adjust'])
        self.assertIn('✓', labels['exclude'])


if __name__ == '__main__':
    unittest.main()
