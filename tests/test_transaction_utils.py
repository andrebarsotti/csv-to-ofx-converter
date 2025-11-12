"""
Unit tests for transaction_utils module.
Tests all utility functions for transaction processing without UI dependencies.
"""

import unittest
import sys
import os

# Add parent directory to path to import src modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.transaction_utils import (
    build_transaction_description,
    determine_transaction_type,
    extract_transaction_id,
    calculate_balance_summary,
    validate_field_mappings,
    parse_balance_value
)
from src.constants import NOT_MAPPED, NOT_SELECTED


class TestBuildTransactionDescription(unittest.TestCase):
    """Test cases for build_transaction_description function."""

    def test_single_column_description(self):
        """Test building description from single column."""
        row = {'memo': 'Purchase at store', 'amount': '100.00'}
        result = build_transaction_description(
            row=row,
            desc_col='memo',
            description_columns=[],
            separator=' ',
            use_composite=False
        )
        self.assertEqual(result, 'Purchase at store')

    def test_composite_description_two_columns(self):
        """Test building composite description from two columns."""
        row = {'memo': 'Purchase', 'vendor': 'Store A', 'amount': '100.00'}
        result = build_transaction_description(
            row=row,
            desc_col='memo',
            description_columns=['memo', 'vendor'],
            separator=' - ',
            use_composite=True
        )
        self.assertEqual(result, 'Purchase - Store A')

    def test_composite_description_multiple_columns(self):
        """Test building composite description from multiple columns."""
        row = {
            'date': '2025-01-01',
            'memo': 'Purchase',
            'vendor': 'Store A',
            'category': 'Food',
            'amount': '100.00'
        }
        result = build_transaction_description(
            row=row,
            desc_col='memo',
            description_columns=['memo', 'vendor', 'category'],
            separator=' | ',
            use_composite=True
        )
        self.assertEqual(result, 'Purchase | Store A | Food')

    def test_composite_description_with_not_selected(self):
        """Test composite description skips NOT_SELECTED columns."""
        row = {'memo': 'Purchase', 'vendor': 'Store A', 'category': 'Food'}
        result = build_transaction_description(
            row=row,
            desc_col='memo',
            description_columns=[NOT_SELECTED, 'memo', 'vendor'],
            separator=' - ',
            use_composite=True
        )
        self.assertEqual(result, 'Purchase - Store A')

    def test_composite_description_missing_columns(self):
        """Test composite description handles missing columns."""
        row = {'memo': 'Purchase', 'amount': '100.00'}
        result = build_transaction_description(
            row=row,
            desc_col='memo',
            description_columns=['memo', 'vendor', 'category'],
            separator=' - ',
            use_composite=True
        )
        self.assertEqual(result, 'Purchase')

    def test_composite_description_empty_values(self):
        """Test composite description skips empty values."""
        row = {'memo': 'Purchase', 'vendor': '', 'category': 'Food'}
        result = build_transaction_description(
            row=row,
            desc_col='memo',
            description_columns=['memo', 'vendor', 'category'],
            separator=' - ',
            use_composite=True
        )
        self.assertEqual(result, 'Purchase - Food')

    def test_composite_description_whitespace_values(self):
        """Test composite description skips whitespace-only values."""
        row = {'memo': 'Purchase', 'vendor': '   ', 'category': 'Food'}
        result = build_transaction_description(
            row=row,
            desc_col='memo',
            description_columns=['memo', 'vendor', 'category'],
            separator=' - ',
            use_composite=True
        )
        self.assertEqual(result, 'Purchase - Food')

    def test_composite_description_all_empty(self):
        """Test composite description returns 'Transaction' when all values empty."""
        row = {'memo': '', 'vendor': '', 'category': ''}
        result = build_transaction_description(
            row=row,
            desc_col='memo',
            description_columns=['memo', 'vendor', 'category'],
            separator=' - ',
            use_composite=True
        )
        self.assertEqual(result, 'Transaction')

    def test_composite_description_different_separators(self):
        """Test composite description with different separators."""
        row = {'memo': 'Purchase', 'vendor': 'Store A'}

        # Space separator
        result = build_transaction_description(
            row, 'memo', ['memo', 'vendor'], ' ', True)
        self.assertEqual(result, 'Purchase Store A')

        # Comma separator
        result = build_transaction_description(
            row, 'memo', ['memo', 'vendor'], ', ', True)
        self.assertEqual(result, 'Purchase, Store A')

        # Pipe separator
        result = build_transaction_description(
            row, 'memo', ['memo', 'vendor'], ' | ', True)
        self.assertEqual(result, 'Purchase | Store A')

    def test_single_column_missing(self):
        """Test single column description when column is missing."""
        row = {'amount': '100.00'}
        result = build_transaction_description(
            row=row,
            desc_col='memo',
            description_columns=[],
            separator=' ',
            use_composite=False
        )
        self.assertEqual(result, 'Transaction')


class TestDetermineTransactionType(unittest.TestCase):
    """Test cases for determine_transaction_type function."""

    def test_type_column_valid_debit(self):
        """Test type determination when column has valid DEBIT value."""
        result = determine_transaction_type(
            type_col='type',
            row={'type': 'DEBIT', 'amount': '100.00'},
            amount=100.0
        )
        self.assertEqual(result, 'DEBIT')

    def test_type_column_valid_credit(self):
        """Test type determination when column has valid CREDIT value."""
        result = determine_transaction_type(
            type_col='type',
            row={'type': 'CREDIT', 'amount': '100.00'},
            amount=-100.0
        )
        self.assertEqual(result, 'CREDIT')

    def test_type_column_lowercase(self):
        """Test type determination handles lowercase values."""
        result = determine_transaction_type(
            type_col='type',
            row={'type': 'debit'},
            amount=100.0
        )
        self.assertEqual(result, 'DEBIT')

    def test_type_column_invalid_infers_from_negative_amount(self):
        """Test type inferred from amount when column has invalid value."""
        result = determine_transaction_type(
            type_col='type',
            row={'type': 'INVALID'},
            amount=-50.0
        )
        self.assertEqual(result, 'DEBIT')

    def test_type_column_invalid_infers_from_positive_amount(self):
        """Test type inferred from amount when column has invalid value."""
        result = determine_transaction_type(
            type_col='type',
            row={'type': 'INVALID'},
            amount=50.0
        )
        self.assertEqual(result, 'CREDIT')

    def test_type_column_not_mapped_negative_amount(self):
        """Test type inferred from negative amount when column not mapped."""
        result = determine_transaction_type(
            type_col=NOT_MAPPED,
            row={},
            amount=-100.0
        )
        self.assertEqual(result, 'DEBIT')

    def test_type_column_not_mapped_positive_amount(self):
        """Test type inferred from positive amount when column not mapped."""
        result = determine_transaction_type(
            type_col=NOT_MAPPED,
            row={},
            amount=100.0
        )
        self.assertEqual(result, 'CREDIT')

    def test_type_column_not_mapped_zero_amount(self):
        """Test type for zero amount (should be CREDIT as >= 0)."""
        result = determine_transaction_type(
            type_col=NOT_MAPPED,
            row={},
            amount=0.0
        )
        self.assertEqual(result, 'CREDIT')

    def test_type_column_missing_from_row(self):
        """Test type determination when column is not in row."""
        result = determine_transaction_type(
            type_col='type',
            row={'amount': '100.00'},
            amount=-50.0
        )
        self.assertEqual(result, 'DEBIT')


class TestExtractTransactionId(unittest.TestCase):
    """Test cases for extract_transaction_id function."""

    def test_id_column_mapped_and_present(self):
        """Test extracting ID when column is mapped and present."""
        result = extract_transaction_id(
            id_col='trans_id',
            row={'trans_id': 'TXN123', 'amount': '100.00'}
        )
        self.assertEqual(result, 'TXN123')

    def test_id_column_mapped_but_missing(self):
        """Test extracting ID when column is mapped but not in row."""
        result = extract_transaction_id(
            id_col='trans_id',
            row={'amount': '100.00'}
        )
        self.assertIsNone(result)

    def test_id_column_not_mapped(self):
        """Test extracting ID when column is not mapped."""
        result = extract_transaction_id(
            id_col=NOT_MAPPED,
            row={'trans_id': 'TXN123', 'amount': '100.00'}
        )
        self.assertIsNone(result)

    def test_id_column_empty_value(self):
        """Test extracting ID when value is empty string."""
        result = extract_transaction_id(
            id_col='trans_id',
            row={'trans_id': '', 'amount': '100.00'}
        )
        self.assertEqual(result, '')

    def test_id_column_numeric_value(self):
        """Test extracting numeric ID value."""
        result = extract_transaction_id(
            id_col='trans_id',
            row={'trans_id': '12345'}
        )
        self.assertEqual(result, '12345')


class TestCalculateBalanceSummary(unittest.TestCase):
    """Test cases for calculate_balance_summary function."""

    def test_balance_with_credits_and_debits(self):
        """Test balance calculation with both credits and debits."""
        transactions = [
            {'amount': 100.0},
            {'amount': -50.0},
            {'amount': 25.0},
            {'amount': -10.0}
        ]
        result = calculate_balance_summary(transactions, 1000.0)

        self.assertEqual(result['initial_balance'], 1000.0)
        self.assertEqual(result['total_credits'], 125.0)
        self.assertEqual(result['total_debits'], 60.0)
        self.assertEqual(result['calculated_final_balance'], 1065.0)
        self.assertEqual(result['transaction_count'], 4)

    def test_balance_only_credits(self):
        """Test balance calculation with only credit transactions."""
        transactions = [
            {'amount': 100.0},
            {'amount': 50.0},
            {'amount': 25.0}
        ]
        result = calculate_balance_summary(transactions, 500.0)

        self.assertEqual(result['total_credits'], 175.0)
        self.assertEqual(result['total_debits'], 0.0)
        self.assertEqual(result['calculated_final_balance'], 675.0)

    def test_balance_only_debits(self):
        """Test balance calculation with only debit transactions."""
        transactions = [
            {'amount': -100.0},
            {'amount': -50.0},
            {'amount': -25.0}
        ]
        result = calculate_balance_summary(transactions, 500.0)

        self.assertEqual(result['total_credits'], 0.0)
        self.assertEqual(result['total_debits'], 175.0)
        self.assertEqual(result['calculated_final_balance'], 325.0)

    def test_balance_empty_transactions(self):
        """Test balance calculation with no transactions."""
        result = calculate_balance_summary([], 1000.0)

        self.assertEqual(result['initial_balance'], 1000.0)
        self.assertEqual(result['total_credits'], 0.0)
        self.assertEqual(result['total_debits'], 0.0)
        self.assertEqual(result['calculated_final_balance'], 1000.0)
        self.assertEqual(result['transaction_count'], 0)

    def test_balance_zero_initial(self):
        """Test balance calculation with zero initial balance."""
        transactions = [
            {'amount': 100.0},
            {'amount': -50.0}
        ]
        result = calculate_balance_summary(transactions, 0.0)

        self.assertEqual(result['calculated_final_balance'], 50.0)

    def test_balance_negative_initial(self):
        """Test balance calculation with negative initial balance."""
        transactions = [
            {'amount': 100.0}
        ]
        result = calculate_balance_summary(transactions, -50.0)

        self.assertEqual(result['calculated_final_balance'], 50.0)

    def test_balance_zero_amounts(self):
        """Test balance calculation with zero amount transactions."""
        transactions = [
            {'amount': 0.0},
            {'amount': 0.0}
        ]
        result = calculate_balance_summary(transactions, 1000.0)

        self.assertEqual(result['total_credits'], 0.0)
        self.assertEqual(result['total_debits'], 0.0)
        self.assertEqual(result['calculated_final_balance'], 1000.0)

    def test_balance_missing_amount_key(self):
        """Test balance calculation handles missing amount key."""
        transactions = [
            {'amount': 100.0},
            {'description': 'No amount'},
            {'amount': -50.0}
        ]
        result = calculate_balance_summary(transactions, 1000.0)

        # Missing amount treated as 0.0
        self.assertEqual(result['calculated_final_balance'], 1050.0)
        self.assertEqual(result['transaction_count'], 3)


class TestValidateFieldMappings(unittest.TestCase):
    """Test cases for validate_field_mappings function."""

    def test_all_required_fields_mapped(self):
        """Test validation passes when all required fields are mapped."""
        mappings = {
            'date': 'Date',
            'amount': 'Amount',
            'description': 'Description'
        }
        is_valid, error = validate_field_mappings(mappings, ['date', 'amount'])

        self.assertTrue(is_valid)
        self.assertIsNone(error)

    def test_required_field_not_mapped(self):
        """Test validation fails when required field is NOT_MAPPED."""
        mappings = {
            'date': 'Date',
            'amount': NOT_MAPPED,
            'description': 'Description'
        }
        is_valid, error = validate_field_mappings(mappings, ['date', 'amount'])

        self.assertFalse(is_valid)
        self.assertIn('amount', error)
        self.assertIn('not mapped', error.lower())

    def test_required_field_missing_from_mappings(self):
        """Test validation fails when required field is missing."""
        mappings = {
            'date': 'Date',
            'description': 'Description'
        }
        is_valid, error = validate_field_mappings(mappings, ['date', 'amount'])

        self.assertFalse(is_valid)
        self.assertIn('amount', error)

    def test_multiple_required_fields_first_fails(self):
        """Test validation returns error for first unmapped field."""
        mappings = {
            'date': NOT_MAPPED,
            'amount': NOT_MAPPED
        }
        is_valid, error = validate_field_mappings(mappings, ['date', 'amount'])

        self.assertFalse(is_valid)
        self.assertIn('date', error)

    def test_empty_required_fields_list(self):
        """Test validation passes with empty required fields list."""
        mappings = {
            'date': NOT_MAPPED,
            'amount': NOT_MAPPED
        }
        is_valid, error = validate_field_mappings(mappings, [])

        self.assertTrue(is_valid)
        self.assertIsNone(error)

    def test_optional_fields_not_checked(self):
        """Test validation ignores fields not in required list."""
        mappings = {
            'date': 'Date',
            'amount': 'Amount',
            'description': NOT_MAPPED,
            'type': NOT_MAPPED
        }
        is_valid, error = validate_field_mappings(mappings, ['date', 'amount'])

        self.assertTrue(is_valid)
        self.assertIsNone(error)


class TestParseBalanceValue(unittest.TestCase):
    """Test cases for parse_balance_value function."""

    def test_parse_valid_positive_number(self):
        """Test parsing valid positive number string."""
        result = parse_balance_value('1000.50')
        self.assertEqual(result, 1000.5)

    def test_parse_valid_negative_number(self):
        """Test parsing valid negative number string."""
        result = parse_balance_value('-500.25')
        self.assertEqual(result, -500.25)

    def test_parse_zero(self):
        """Test parsing zero."""
        result = parse_balance_value('0')
        self.assertEqual(result, 0.0)

    def test_parse_with_whitespace(self):
        """Test parsing number with leading/trailing whitespace."""
        result = parse_balance_value('  1000.50  ')
        self.assertEqual(result, 1000.5)

    def test_parse_empty_string_uses_default(self):
        """Test parsing empty string returns default."""
        result = parse_balance_value('')
        self.assertEqual(result, 0.0)

    def test_parse_empty_string_custom_default(self):
        """Test parsing empty string with custom default."""
        result = parse_balance_value('', default=100.0)
        self.assertEqual(result, 100.0)

    def test_parse_whitespace_only_uses_default(self):
        """Test parsing whitespace-only string returns default."""
        result = parse_balance_value('   ')
        self.assertEqual(result, 0.0)

    def test_parse_invalid_string_uses_default(self):
        """Test parsing invalid string returns default."""
        result = parse_balance_value('invalid')
        self.assertEqual(result, 0.0)

    def test_parse_invalid_string_custom_default(self):
        """Test parsing invalid string with custom default."""
        result = parse_balance_value('abc123', default=250.0)
        self.assertEqual(result, 250.0)

    def test_parse_none_value_uses_default(self):
        """Test parsing None value returns default."""
        result = parse_balance_value(None, default=50.0)
        self.assertEqual(result, 50.0)

    def test_parse_scientific_notation(self):
        """Test parsing scientific notation."""
        result = parse_balance_value('1.5e3')
        self.assertEqual(result, 1500.0)

    def test_parse_integer_string(self):
        """Test parsing integer string."""
        result = parse_balance_value('1000')
        self.assertEqual(result, 1000.0)


if __name__ == '__main__':
    unittest.main()
