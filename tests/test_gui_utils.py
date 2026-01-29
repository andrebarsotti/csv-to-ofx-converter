"""
Unit tests for gui_utils module.

Tests pure utility functions extracted from ConverterGUI.
"""

import unittest
import tempfile
import os
from datetime import datetime
from src import gui_utils


class TestFileValidation(unittest.TestCase):
    """Test file validation functions."""

    def setUp(self):
        """Create temporary test file."""
        self.temp_file = tempfile.NamedTemporaryFile(
            mode='w', suffix='.csv', delete=False)
        self.temp_file.write('test data')
        self.temp_file.close()

    def tearDown(self):
        """Remove temporary file."""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    def test_validate_csv_file_selection_valid(self):
        """Test validation with valid file."""
        is_valid, error = gui_utils.validate_csv_file_selection(
            self.temp_file.name)
        self.assertTrue(is_valid)
        self.assertIsNone(error)

    def test_validate_csv_file_selection_empty_path(self):
        """Test validation with empty path."""
        is_valid, error = gui_utils.validate_csv_file_selection('')
        self.assertFalse(is_valid)
        self.assertEqual(error, "Please select a CSV file")

    def test_validate_csv_file_selection_nonexistent(self):
        """Test validation with nonexistent file."""
        is_valid, error = gui_utils.validate_csv_file_selection(
            '/nonexistent/file.csv')
        self.assertFalse(is_valid)
        self.assertIn("File not found", error)

    def test_validate_csv_file_selection_directory(self):
        """Test validation with directory instead of file."""
        temp_dir = tempfile.mkdtemp()
        try:
            is_valid, error = gui_utils.validate_csv_file_selection(temp_dir)
            self.assertFalse(is_valid)
            self.assertIn("not a file", error)
        finally:
            os.rmdir(temp_dir)


class TestFieldMappingValidation(unittest.TestCase):
    """Test field mapping validation functions."""

    def test_validate_required_field_mappings_valid(self):
        """Test validation with all required fields mapped."""
        mappings = {'date': 'Date Column', 'amount': 'Amount Column'}
        is_valid, error = gui_utils.validate_required_field_mappings(mappings)
        self.assertTrue(is_valid)
        self.assertIsNone(error)

    def test_validate_required_field_mappings_missing_date(self):
        """Test validation with missing date mapping."""
        mappings = {'date': '<Not Mapped>', 'amount': 'Amount Column'}
        is_valid, error = gui_utils.validate_required_field_mappings(mappings)
        self.assertFalse(is_valid)
        self.assertEqual(error, "Please map the Date field")

    def test_validate_required_field_mappings_missing_amount(self):
        """Test validation with missing amount mapping."""
        mappings = {'date': 'Date Column', 'amount': '<Not Mapped>'}
        is_valid, error = gui_utils.validate_required_field_mappings(mappings)
        self.assertFalse(is_valid)
        self.assertEqual(error, "Please map the Amount field")

    def test_validate_description_mapping_single_field(self):
        """Test validation with single description field mapped."""
        is_valid, error = gui_utils.validate_description_mapping(
            'Description Column', [], '<Not Mapped>', '<Not Selected>')
        self.assertTrue(is_valid)
        self.assertIsNone(error)

    def test_validate_description_mapping_composite(self):
        """Test validation with composite description configured."""
        is_valid, error = gui_utils.validate_description_mapping(
            '<Not Mapped>', ['Col1', 'Col2'], '<Not Mapped>', '<Not Selected>')
        self.assertTrue(is_valid)
        self.assertIsNone(error)

    def test_validate_description_mapping_none(self):
        """Test validation with no description configured."""
        is_valid, error = gui_utils.validate_description_mapping(
            '<Not Mapped>', ['<Not Selected>'], '<Not Mapped>', '<Not Selected>')
        self.assertFalse(is_valid)
        self.assertIn("Please map the Description field", error)


class TestDateFormatting(unittest.TestCase):
    """Test date formatting functions."""

    def test_format_date_string_empty(self):
        """Test formatting empty string."""
        result = gui_utils.format_date_string('')
        self.assertEqual(result, '')

    def test_format_date_string_partial_day(self):
        """Test formatting partial day input."""
        result = gui_utils.format_date_string('0')
        self.assertEqual(result, '0')

        result = gui_utils.format_date_string('01')
        self.assertEqual(result, '01')

    def test_format_date_string_day_month(self):
        """Test formatting day and month input."""
        result = gui_utils.format_date_string('010')
        self.assertEqual(result, '01/0')

        result = gui_utils.format_date_string('0110')
        self.assertEqual(result, '01/10')

    def test_format_date_string_full_date(self):
        """Test formatting full date input."""
        result = gui_utils.format_date_string('01102025')
        self.assertEqual(result, '01/10/2025')

    def test_format_date_string_removes_non_digits(self):
        """Test that non-digit characters are removed."""
        result = gui_utils.format_date_string('01-10-2025')
        self.assertEqual(result, '01/10/2025')

    def test_format_date_string_max_length(self):
        """Test max length limit."""
        result = gui_utils.format_date_string('0110202599999')
        self.assertEqual(result, '01/10/2025')

    def test_validate_date_format_valid(self):
        """Test validation with valid date."""
        is_valid, error = gui_utils.validate_date_format('01/10/2025')
        self.assertTrue(is_valid)
        self.assertIsNone(error)

    def test_validate_date_format_empty(self):
        """Test validation with empty date."""
        is_valid, error = gui_utils.validate_date_format('')
        self.assertFalse(is_valid)
        self.assertEqual(error, "Date cannot be empty")

    def test_validate_date_format_wrong_format(self):
        """Test validation with wrong format."""
        is_valid, error = gui_utils.validate_date_format('2025-10-01')
        self.assertFalse(is_valid)
        self.assertIn("DD/MM/YYYY format", error)

    def test_validate_date_format_invalid_day(self):
        """Test validation with invalid day."""
        is_valid, error = gui_utils.validate_date_format('32/10/2025')
        self.assertFalse(is_valid)
        self.assertIn("Day must be between", error)

    def test_validate_date_format_invalid_month(self):
        """Test validation with invalid month."""
        is_valid, error = gui_utils.validate_date_format('01/13/2025')
        self.assertFalse(is_valid)
        self.assertIn("Month must be between", error)

    def test_validate_date_format_invalid_year(self):
        """Test validation with invalid year."""
        is_valid, error = gui_utils.validate_date_format('01/10/1800')
        self.assertFalse(is_valid)
        self.assertIn("Year must be between", error)


class TestNumericValidation(unittest.TestCase):
    """Test numeric validation functions."""

    def test_validate_numeric_input_empty(self):
        """Test validation with empty string."""
        result = gui_utils.validate_numeric_input('')
        self.assertTrue(result)

    def test_validate_numeric_input_positive(self):
        """Test validation with positive number."""
        result = gui_utils.validate_numeric_input('123')
        self.assertTrue(result)

    def test_validate_numeric_input_negative(self):
        """Test validation with negative number."""
        result = gui_utils.validate_numeric_input('-123')
        self.assertTrue(result)

    def test_validate_numeric_input_decimal(self):
        """Test validation with decimal number."""
        result = gui_utils.validate_numeric_input('123.45')
        self.assertTrue(result)

    def test_validate_numeric_input_negative_decimal(self):
        """Test validation with negative decimal."""
        result = gui_utils.validate_numeric_input('-123.45')
        self.assertTrue(result)

    def test_validate_numeric_input_minus_only(self):
        """Test validation with minus sign only."""
        result = gui_utils.validate_numeric_input('-')
        self.assertTrue(result)

    def test_validate_numeric_input_multiple_decimals(self):
        """Test validation rejects multiple decimal points."""
        result = gui_utils.validate_numeric_input('123.45.67')
        self.assertFalse(result)

    def test_validate_numeric_input_letters(self):
        """Test validation rejects letters."""
        result = gui_utils.validate_numeric_input('abc')
        self.assertFalse(result)

    def test_validate_numeric_input_no_negative(self):
        """Test validation with negative not allowed."""
        result = gui_utils.validate_numeric_input('-123', allow_negative=False)
        self.assertFalse(result)

    def test_validate_numeric_input_no_decimal(self):
        """Test validation with decimal not allowed."""
        result = gui_utils.validate_numeric_input('123.45', allow_decimal=False)
        self.assertFalse(result)

    def test_parse_numeric_value_valid(self):
        """Test parsing valid numeric value."""
        result = gui_utils.parse_numeric_value('123.45')
        self.assertEqual(result, 123.45)

    def test_parse_numeric_value_negative(self):
        """Test parsing negative numeric value."""
        result = gui_utils.parse_numeric_value('-123.45')
        self.assertEqual(result, -123.45)

    def test_parse_numeric_value_empty(self):
        """Test parsing empty string returns default."""
        result = gui_utils.parse_numeric_value('', default=10.0)
        self.assertEqual(result, 10.0)

    def test_parse_numeric_value_invalid(self):
        """Test parsing invalid string returns default."""
        result = gui_utils.parse_numeric_value('abc', default=5.0)
        self.assertEqual(result, 5.0)


class TestBalanceCalculations(unittest.TestCase):
    """Test balance calculation functions."""

    def test_calculate_cursor_position_after_format(self):
        """Test cursor position calculation after formatting."""
        # Test with cursor at end
        new_pos = gui_utils.calculate_cursor_position_after_format(
            '01102025', '01/10/2025', 8)
        self.assertEqual(new_pos, 10)

        # Test with cursor in middle
        new_pos = gui_utils.calculate_cursor_position_after_format(
            '0110', '01/10', 4)
        self.assertEqual(new_pos, 5)

    def test_format_balance_value(self):
        """Test balance value formatting."""
        result = gui_utils.format_balance_value(123.456)
        self.assertEqual(result, '123.46')

        result = gui_utils.format_balance_value(123.4)
        self.assertEqual(result, '123.40')

    def test_format_balance_value_negative(self):
        """Test negative balance formatting."""
        result = gui_utils.format_balance_value(-123.456)
        self.assertEqual(result, '-123.46')

    def test_format_balance_value_custom_places(self):
        """Test balance formatting with custom decimal places."""
        result = gui_utils.format_balance_value(123.456, decimal_places=3)
        self.assertEqual(result, '123.456')


class TestDateParsingForSorting(unittest.TestCase):
    """Test date parsing for sorting."""

    def test_parse_date_for_sorting_iso(self):
        """Test parsing ISO format date."""
        result = gui_utils.parse_date_for_sorting('2025-10-01')
        self.assertEqual(result, datetime(2025, 10, 1))

    def test_parse_date_for_sorting_brazilian(self):
        """Test parsing Brazilian format date."""
        result = gui_utils.parse_date_for_sorting('01/10/2025')
        self.assertEqual(result, datetime(2025, 10, 1))

    def test_parse_date_for_sorting_us(self):
        """Test parsing US format date."""
        # Note: This will be parsed as Brazilian format (DD/MM/YYYY) first
        # since that pattern comes before US format in the function
        result = gui_utils.parse_date_for_sorting('10/01/2025')
        self.assertEqual(result, datetime(2025, 1, 10))

    def test_parse_date_for_sorting_compact(self):
        """Test parsing compact format date."""
        result = gui_utils.parse_date_for_sorting('20251001')
        self.assertEqual(result, datetime(2025, 10, 1))

    def test_parse_date_for_sorting_invalid(self):
        """Test parsing invalid date returns far future."""
        result = gui_utils.parse_date_for_sorting('invalid')
        self.assertEqual(result, datetime(9999, 12, 31))


class TestConversionValidation(unittest.TestCase):
    """Test conversion validation functions."""

    def test_validate_conversion_prerequisites_valid(self):
        """Test validation with all prerequisites met."""
        csv_data = [{'Date': '2025-01-01', 'Amount': '100'}]
        field_mappings = {'date': 'Date', 'amount': 'Amount'}
        is_valid, error = gui_utils.validate_conversion_prerequisites(
            csv_data, field_mappings)
        self.assertTrue(is_valid)
        self.assertIsNone(error)

    def test_validate_conversion_prerequisites_no_data(self):
        """Test validation with no CSV data."""
        is_valid, error = gui_utils.validate_conversion_prerequisites(
            [], {'date': 'Date', 'amount': 'Amount'})
        self.assertFalse(is_valid)
        self.assertEqual(error, "Please load a CSV file first")

    def test_validate_conversion_prerequisites_missing_mappings(self):
        """Test validation with missing field mappings."""
        csv_data = [{'Date': '2025-01-01'}]
        field_mappings = {'date': '<Not Mapped>', 'amount': '<Not Mapped>'}
        is_valid, error = gui_utils.validate_conversion_prerequisites(
            csv_data, field_mappings)
        self.assertFalse(is_valid)
        self.assertIn("Please map the Date field", error)

    def test_validate_date_range_inputs_valid(self):
        """Test validation with valid date range."""
        is_valid, error = gui_utils.validate_date_range_inputs(
            '01/10/2025', '31/10/2025')
        self.assertTrue(is_valid)
        self.assertIsNone(error)

    def test_validate_date_range_inputs_empty_start(self):
        """Test validation with empty start date."""
        is_valid, error = gui_utils.validate_date_range_inputs('', '31/10/2025')
        self.assertFalse(is_valid)
        self.assertEqual(error, "Please enter a start date")

    def test_validate_date_range_inputs_empty_end(self):
        """Test validation with empty end date."""
        is_valid, error = gui_utils.validate_date_range_inputs('01/10/2025', '')
        self.assertFalse(is_valid)
        self.assertEqual(error, "Please enter an end date")

    def test_validate_date_range_inputs_invalid_start_format(self):
        """Test validation with invalid start date format."""
        is_valid, error = gui_utils.validate_date_range_inputs(
            '2025-10-01', '31/10/2025')
        self.assertFalse(is_valid)
        self.assertIn("Invalid start date", error)

    def test_validate_date_range_inputs_invalid_end_format(self):
        """Test validation with invalid end date format."""
        is_valid, error = gui_utils.validate_date_range_inputs(
            '01/10/2025', '2025-10-31')
        self.assertFalse(is_valid)
        self.assertIn("Invalid end date", error)

    def test_validate_date_range_inputs_end_before_start(self):
        """Test validation with end date before start date."""
        is_valid, error = gui_utils.validate_date_range_inputs(
            '31/10/2025', '01/10/2025')
        self.assertFalse(is_valid)
        self.assertEqual(error, "End date must be greater than or equal to start date")

    def test_validate_date_range_inputs_same_dates(self):
        """Test validation with same start and end date."""
        is_valid, error = gui_utils.validate_date_range_inputs(
            '15/10/2025', '15/10/2025')
        self.assertTrue(is_valid)
        self.assertIsNone(error)

    def test_validate_date_range_inputs_end_before_start_different_months(self):
        """Test validation with end date in earlier month than start date."""
        is_valid, error = gui_utils.validate_date_range_inputs(
            '01/11/2025', '31/10/2025')
        self.assertFalse(is_valid)
        self.assertEqual(error, "End date must be greater than or equal to start date")

    def test_validate_date_range_inputs_impossible_start_date(self):
        """Test validation with impossible calendar start date (Feb 31)."""
        is_valid, error = gui_utils.validate_date_range_inputs(
            '31/02/2025', '31/03/2025')
        self.assertFalse(is_valid)
        self.assertIn("Invalid start date", error)

    def test_validate_date_range_inputs_impossible_end_date(self):
        """Test validation with impossible calendar end date (Feb 30)."""
        is_valid, error = gui_utils.validate_date_range_inputs(
            '01/02/2025', '30/02/2025')
        self.assertFalse(is_valid)
        self.assertIn("Invalid end date", error)


class TestStatisticsFormatting(unittest.TestCase):
    """Test statistics formatting functions."""

    def test_format_preview_stats_within_limit(self):
        """Test formatting when count is within preview limit."""
        result = gui_utils.format_preview_stats(50, 50, 100)
        self.assertEqual(result, "Showing 50 of 50 rows")

    def test_format_preview_stats_exceeds_limit(self):
        """Test formatting when count exceeds preview limit."""
        result = gui_utils.format_preview_stats(100, 200, 100)
        self.assertIn("Showing 100 of 200 rows", result)
        self.assertIn("limited to first 100", result)

    def test_format_conversion_stats_basic(self):
        """Test basic conversion stats formatting."""
        result = gui_utils.format_conversion_stats(
            total_rows=100, processed=95, excluded=5)
        self.assertIn("Total rows processed: 100", result)
        self.assertIn("Transactions exported: 95", result)
        self.assertIn("Transactions excluded: 5", result)

    def test_format_conversion_stats_with_date_validation(self):
        """Test conversion stats with date validation."""
        result = gui_utils.format_conversion_stats(
            total_rows=100,
            processed=95,
            excluded=5,
            adjusted=3,
            kept_out_of_range=2,
            has_date_validator=True
        )
        self.assertIn("Dates adjusted: 3", result)
        self.assertIn("Out-of-range dates kept: 2", result)

    def test_format_conversion_stats_no_exclusions(self):
        """Test conversion stats with no exclusions."""
        result = gui_utils.format_conversion_stats(
            total_rows=100, processed=100, excluded=0)
        self.assertNotIn("excluded", result)


if __name__ == '__main__':
    unittest.main()
