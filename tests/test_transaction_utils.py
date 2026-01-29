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
    parse_balance_value,
    generate_deterministic_fitid
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


class TestGenerateDeterministicFitid(unittest.TestCase):
    """Test cases for generate_deterministic_fitid function."""

    def test_generate_deterministic_fitid_basic(self):
        """Test basic deterministic FITID generation."""
        fitid = generate_deterministic_fitid(
            date="20260115",
            amount=-100.50,
            memo="Restaurant Purchase"
        )

        # Verify valid UUID format
        self.assertIsInstance(fitid, str)
        self.assertEqual(len(fitid), 36)  # UUID format: 8-4-4-4-12
        self.assertIn('-', fitid)
        # Verify UUID v5 format (version 5, variant 1)
        parts = fitid.split('-')
        self.assertEqual(len(parts), 5)

    def test_generate_deterministic_fitid_deterministic(self):
        """Test that same inputs always produce same output."""
        # Generate FITID twice with identical inputs
        fitid1 = generate_deterministic_fitid(
            date="20260115",
            amount=-100.50,
            memo="Restaurant Purchase"
        )
        fitid2 = generate_deterministic_fitid(
            date="20260115",
            amount=-100.50,
            memo="Restaurant Purchase"
        )

        # Must be identical
        self.assertEqual(fitid1, fitid2)

    def test_generate_deterministic_fitid_different_dates(self):
        """Test that different dates produce different IDs."""
        fitid1 = generate_deterministic_fitid(
            date="20260115",
            amount=-100.50,
            memo="Purchase"
        )
        fitid2 = generate_deterministic_fitid(
            date="20260116",
            amount=-100.50,
            memo="Purchase"
        )

        # Different dates should produce different IDs
        self.assertNotEqual(fitid1, fitid2)

    def test_generate_deterministic_fitid_different_amounts(self):
        """Test that different amounts produce different IDs."""
        fitid1 = generate_deterministic_fitid(
            date="20260115",
            amount=-100.50,
            memo="Purchase"
        )
        fitid2 = generate_deterministic_fitid(
            date="20260115",
            amount=-200.50,
            memo="Purchase"
        )

        # Different amounts should produce different IDs
        self.assertNotEqual(fitid1, fitid2)

    def test_generate_deterministic_fitid_different_memos(self):
        """Test that different memos produce different IDs."""
        fitid1 = generate_deterministic_fitid(
            date="20260115",
            amount=-100.50,
            memo="Restaurant"
        )
        fitid2 = generate_deterministic_fitid(
            date="20260115",
            amount=-100.50,
            memo="Store"
        )

        # Different memos should produce different IDs
        self.assertNotEqual(fitid1, fitid2)

    def test_generate_deterministic_fitid_ofx_date_normalization(self):
        """Test that OFX format dates are normalized correctly."""
        # Pass OFX format date
        fitid1 = generate_deterministic_fitid(
            date="20260115000000[-3:BRT]",
            amount=-100.50,
            memo="Purchase"
        )

        # Pass simple date format
        fitid2 = generate_deterministic_fitid(
            date="20260115",
            amount=-100.50,
            memo="Purchase"
        )

        # Must be identical (date normalization works)
        self.assertEqual(fitid1, fitid2)

    def test_generate_deterministic_fitid_amount_normalization(self):
        """Test that amounts are normalized to 2 decimal places."""
        # Same amount with different decimal places
        fitid1 = generate_deterministic_fitid(
            date="20260115",
            amount=-100.50,
            memo="Purchase"
        )
        fitid2 = generate_deterministic_fitid(
            date="20260115",
            amount=-100.55,
            memo="Purchase"
        )
        fitid3 = generate_deterministic_fitid(
            date="20260115",
            amount=-100.5,
            memo="Purchase"
        )

        # fitid1 and fitid2 should differ (different amounts)
        self.assertNotEqual(fitid1, fitid2)
        # fitid1 and fitid3 should be same (normalized to -100.50)
        self.assertEqual(fitid1, fitid3)

    def test_generate_deterministic_fitid_memo_normalization(self):
        """Test that memos are normalized (stripped, lowercase)."""
        # Memo with whitespace and mixed case
        fitid1 = generate_deterministic_fitid(
            date="20260115",
            amount=-100.50,
            memo="  Purchase  "
        )
        fitid2 = generate_deterministic_fitid(
            date="20260115",
            amount=-100.50,
            memo="PURCHASE"
        )
        fitid3 = generate_deterministic_fitid(
            date="20260115",
            amount=-100.50,
            memo="purchase"
        )

        # All should be identical (normalized to "purchase")
        self.assertEqual(fitid1, fitid2)
        self.assertEqual(fitid2, fitid3)

    def test_generate_deterministic_fitid_memo_truncation(self):
        """Test that memos longer than 255 characters are truncated."""
        # Memo exactly 255 characters with 'a'
        memo_255_a = "a" * 255
        # Memo with 256 characters but different at position 254 (to show truncation effect)
        memo_256_ab = "a" * 254 + "b" + "a"  # 256 chars, differs at position 254
        # Memo with 300 characters
        memo_300_a = "a" * 300

        fitid_255_a = generate_deterministic_fitid(
            date="20260115",
            amount=-100.50,
            memo=memo_255_a
        )
        fitid_256_ab = generate_deterministic_fitid(
            date="20260115",
            amount=-100.50,
            memo=memo_256_ab
        )
        fitid_300_a = generate_deterministic_fitid(
            date="20260115",
            amount=-100.50,
            memo=memo_300_a
        )

        # fitid_255_a and fitid_256_ab should differ (difference at position 254)
        self.assertNotEqual(fitid_255_a, fitid_256_ab)
        # fitid_300_a should be identical to fitid_255_a (all truncated to 255 a's)
        self.assertEqual(fitid_255_a, fitid_300_a)

    def test_generate_deterministic_fitid_with_account_id(self):
        """Test that different account_ids produce different IDs."""
        # Without account_id
        fitid1 = generate_deterministic_fitid(
            date="20260115",
            amount=-100.50,
            memo="Purchase"
        )

        # With account_id
        fitid2 = generate_deterministic_fitid(
            date="20260115",
            amount=-100.50,
            memo="Purchase",
            account_id="ACC001"
        )

        # Different account_ids should produce different IDs
        self.assertNotEqual(fitid1, fitid2)

        # Same account_id should produce same ID
        fitid3 = generate_deterministic_fitid(
            date="20260115",
            amount=-100.50,
            memo="Purchase",
            account_id="ACC001"
        )
        self.assertEqual(fitid2, fitid3)

    def test_generate_deterministic_fitid_with_disambiguation(self):
        """Test that different disambiguation values produce different IDs."""
        # Without disambiguation
        fitid1 = generate_deterministic_fitid(
            date="20260115",
            amount=-100.50,
            memo="Purchase"
        )

        # With disambiguation
        fitid2 = generate_deterministic_fitid(
            date="20260115",
            amount=-100.50,
            memo="Purchase",
            disambiguation="1"
        )

        # Different disambiguation should produce different IDs
        self.assertNotEqual(fitid1, fitid2)

        # Same disambiguation should produce same ID
        fitid3 = generate_deterministic_fitid(
            date="20260115",
            amount=-100.50,
            memo="Purchase",
            disambiguation="1"
        )
        self.assertEqual(fitid2, fitid3)

    def test_generate_deterministic_fitid_empty_fields(self):
        """Test handling of empty fields."""
        # Test with empty memo
        fitid1 = generate_deterministic_fitid(
            date="20260115",
            amount=-100.50,
            memo=""
        )
        self.assertIsInstance(fitid1, str)
        self.assertEqual(len(fitid1), 36)

        # Test with empty account_id and disambiguation (defaults)
        fitid2 = generate_deterministic_fitid(
            date="20260115",
            amount=-100.50,
            memo="Purchase",
            account_id="",
            disambiguation=""
        )
        self.assertIsInstance(fitid2, str)
        self.assertEqual(len(fitid2), 36)

    def test_generate_deterministic_fitid_positive_amount(self):
        """Test FITID generation with positive amount."""
        fitid = generate_deterministic_fitid(
            date="20260115",
            amount=100.50,
            memo="Deposit"
        )

        self.assertIsInstance(fitid, str)
        self.assertEqual(len(fitid), 36)

    def test_generate_deterministic_fitid_zero_amount(self):
        """Test FITID generation with zero amount."""
        fitid = generate_deterministic_fitid(
            date="20260115",
            amount=0.0,
            memo="Adjustment"
        )

        self.assertIsInstance(fitid, str)
        self.assertEqual(len(fitid), 36)

    def test_generate_deterministic_fitid_large_amount(self):
        """Test FITID generation with large amount."""
        fitid = generate_deterministic_fitid(
            date="20260115",
            amount=-999999.99,
            memo="Large payment"
        )

        self.assertIsInstance(fitid, str)
        self.assertEqual(len(fitid), 36)

    def test_generate_deterministic_fitid_special_characters_in_memo(self):
        """Test FITID generation with special characters in memo."""
        # Memo with special characters
        fitid1 = generate_deterministic_fitid(
            date="20260115",
            amount=-100.50,
            memo="Purchase @ Store & Co."
        )

        # Verify function handles without errors
        self.assertIsInstance(fitid1, str)
        self.assertEqual(len(fitid1), 36)
        # Verify valid UUID format
        parts = fitid1.split('-')
        self.assertEqual(len(parts), 5)

        # Memo with unicode characters
        fitid2 = generate_deterministic_fitid(
            date="20260115",
            amount=-100.50,
            memo="Café • Restaurant"
        )

        # Verify function handles unicode without errors
        self.assertIsInstance(fitid2, str)
        self.assertEqual(len(fitid2), 36)
        parts = fitid2.split('-')
        self.assertEqual(len(parts), 5)

        # Verify different special characters produce different IDs
        self.assertNotEqual(fitid1, fitid2)

        # Test more complex unicode
        fitid3 = generate_deterministic_fitid(
            date="20260115",
            amount=-100.50,
            memo="Açúcar € Café 日本語"
        )
        self.assertIsInstance(fitid3, str)
        self.assertEqual(len(fitid3), 36)

    def test_generate_deterministic_fitid_extreme_amounts(self):
        """Test FITID generation with extreme amounts."""
        # Very large amount
        fitid_large = generate_deterministic_fitid(
            date="20260115",
            amount=999999999.99,
            memo="Large transaction"
        )
        self.assertIsInstance(fitid_large, str)
        self.assertEqual(len(fitid_large), 36)

        # Very small amount
        fitid_small = generate_deterministic_fitid(
            date="20260115",
            amount=0.01,
            memo="Small transaction"
        )
        self.assertIsInstance(fitid_small, str)
        self.assertEqual(len(fitid_small), 36)

        # Zero amount
        fitid_zero = generate_deterministic_fitid(
            date="20260115",
            amount=0.00,
            memo="Zero transaction"
        )
        self.assertIsInstance(fitid_zero, str)
        self.assertEqual(len(fitid_zero), 36)

        # Negative large amount
        fitid_neg = generate_deterministic_fitid(
            date="20260115",
            amount=-999999999.99,
            memo="Large negative"
        )
        self.assertIsInstance(fitid_neg, str)
        self.assertEqual(len(fitid_neg), 36)

        # Verify all produce different IDs
        all_fitids = [fitid_large, fitid_small, fitid_zero, fitid_neg]
        self.assertEqual(len(set(all_fitids)), 4, "All extreme amounts should produce unique IDs")

    def test_generate_deterministic_fitid_date_formats(self):
        """Test FITID generation with various OFX date formats."""
        # Various OFX date formats
        fitid1 = generate_deterministic_fitid(
            date="20260115000000[-3:BRT]",
            amount=-100.50,
            memo="Purchase"
        )
        self.assertIsInstance(fitid1, str)
        self.assertEqual(len(fitid1), 36)

        fitid2 = generate_deterministic_fitid(
            date="20260115000000",
            amount=-100.50,
            memo="Purchase"
        )
        self.assertIsInstance(fitid2, str)
        self.assertEqual(len(fitid2), 36)

        fitid3 = generate_deterministic_fitid(
            date="20260115",
            amount=-100.50,
            memo="Purchase"
        )
        self.assertIsInstance(fitid3, str)
        self.assertEqual(len(fitid3), 36)

        # All three should extract YYYYMMDD correctly and produce same ID
        self.assertEqual(fitid1, fitid2, "OFX format with timezone should match without timezone")
        self.assertEqual(fitid2, fitid3, "OFX format with time should match date-only format")
        self.assertEqual(fitid1, fitid3, "All date formats should normalize to same ID")


if __name__ == '__main__':
    unittest.main()
