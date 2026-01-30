"""
GUI Utility Functions Module
============================
Pure utility functions for GUI operations with no Tkinter dependencies.

This module contains testable utility functions extracted from ConverterGUI
to improve maintainability and testability.

Author: Generated for Brazilian banking compatibility
License: MIT
"""

import os
from typing import Tuple, Optional, List, Dict
from datetime import datetime

from .constants import DEFAULT_NOT_MAPPED, DATE_FORMAT_DISPLAY, DATE_FORMAT_STRPTIME


# ==================== FILE VALIDATION ====================

def validate_csv_file_selection(csv_file_path: str) -> Tuple[bool, Optional[str]]:
    """
    Validate that a CSV file has been selected and exists.

    Args:
        csv_file_path: Path to the CSV file

    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if file is valid, False otherwise
        - error_message: Error message if invalid, None if valid
    """
    if not csv_file_path or csv_file_path.strip() == '':
        return False, "Please select a CSV file"

    if not os.path.exists(csv_file_path):
        return False, f"File not found: {csv_file_path}"

    if not os.path.isfile(csv_file_path):
        return False, f"Path is not a file: {csv_file_path}"

    return True, None


# ==================== FIELD MAPPING VALIDATION ====================

def validate_required_field_mappings(
    field_mappings: Dict[str, str],
    not_mapped_value: str = DEFAULT_NOT_MAPPED
) -> Tuple[bool, Optional[str]]:
    """
    Validate that required fields (date and amount) are mapped.

    Args:
        field_mappings: Dictionary of field names to mapped column names
        not_mapped_value: The value representing an unmapped field

    Returns:
        Tuple of (is_valid, error_message)
    """
    date_mapping = field_mappings.get('date', not_mapped_value)
    amount_mapping = field_mappings.get('amount', not_mapped_value)

    if date_mapping == not_mapped_value:
        return False, "Please map the Date field"

    if amount_mapping == not_mapped_value:
        return False, "Please map the Amount field"

    return True, None


def validate_description_mapping(
    description_mapping: str,
    description_columns: List[str],
    not_mapped_value: str = DEFAULT_NOT_MAPPED,
    not_selected_value: str = "<Not Selected>"
) -> Tuple[bool, Optional[str]]:
    """
    Validate that description is mapped (either single field or composite).

    Args:
        description_mapping: Mapped column for description field
        description_columns: List of columns selected for composite description
        not_mapped_value: The value representing an unmapped field
        not_selected_value: The value representing an unselected column

    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check if single description field is mapped
    if description_mapping != not_mapped_value:
        return True, None

    # Check if any composite description columns are selected
    if any(col != not_selected_value for col in description_columns):
        return True, None

    return False, "Please map the Description field or configure composite description"


# ==================== DATE FORMATTING ====================

def format_date_string(input_string: str, max_length: int = 10) -> str:
    """
    Format a date input string by removing non-digit characters except slashes.

    Auto-formats in DD/MM/YYYY format.

    Args:
        input_string: Input string to format
        max_length: Maximum length of formatted string (default 10 for DD/MM/YYYY)

    Returns:
        Formatted date string
    """
    # Remove any non-digit, non-slash characters
    digits_only = ''.join(c for c in input_string if c.isdigit())

    # Limit to 8 digits (DDMMYYYY)
    digits_only = digits_only[:8]

    # Build formatted string based on number of digits
    # DD/MM/YYYY format
    if len(digits_only) <= 2:
        # Just day digits
        formatted = digits_only
    elif len(digits_only) <= 4:
        # Day + month digits
        formatted = digits_only[:2] + '/' + digits_only[2:]
    else:
        # Day + month + year digits
        formatted = digits_only[:2] + '/' + digits_only[2:4] + '/' + digits_only[4:]

    return formatted[:max_length]


def validate_date_format(date_string: str, expected_format: str = DATE_FORMAT_DISPLAY) -> Tuple[bool, Optional[str]]:
    """
    Validate that a date string matches the expected format.

    Args:
        date_string: Date string to validate
        expected_format: Expected date format (currently only supports DD/MM/YYYY)

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not date_string or date_string.strip() == '':
        return False, "Date cannot be empty"

    if expected_format == DATE_FORMAT_DISPLAY:
        return _validate_ddmmyyyy(date_string)

    return False, f"Unsupported date format: {expected_format}"


def _validate_ddmmyyyy(date_string: str) -> Tuple[bool, Optional[str]]:
    """
    Validate a date string in DD/MM/YYYY format.

    Args:
        date_string: Date string to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    parts = date_string.split('/')
    if len(parts) != 3:
        return False, "Date must be in DD/MM/YYYY format (e.g., 01/10/2025)"

    day, month, year = parts
    if not (day.isdigit() and month.isdigit() and year.isdigit()):
        return False, "Date parts must be numeric"

    if len(day) != 2 or len(month) != 2 or len(year) != 4:
        return False, "Date must be in DD/MM/YYYY format (e.g., 01/10/2025)"

    return _validate_date_ranges(int(day), int(month), int(year))


def _validate_date_ranges(day: int, month: int, year: int) -> Tuple[bool, Optional[str]]:
    """
    Validate day, month and year value ranges.

    Args:
        day: Day value (1-31)
        month: Month value (1-12)
        year: Year value (1900-2100)

    Returns:
        Tuple of (is_valid, error_message)
    """
    if day < 1 or day > 31:
        return False, "Day must be between 01 and 31"

    if month < 1 or month > 12:
        return False, "Month must be between 01 and 12"

    if year < 1900 or year > 2100:
        return False, "Year must be between 1900 and 2100"

    return True, None


# ==================== NUMERIC VALIDATION ====================

def validate_numeric_input(value: str, allow_negative: bool = True, allow_decimal: bool = True) -> bool:
    """
    Validate that a string contains valid numeric input.

    Args:
        value: String value to validate
        allow_negative: Whether to allow negative numbers (minus sign at start)
        allow_decimal: Whether to allow decimal point

    Returns:
        True if valid numeric input, False otherwise
    """
    if value == '':
        return True  # Empty is allowed

    # Allow minus sign only at start (if allowed)
    if allow_negative and value == '-':
        return True

    # Handle minus sign at start
    check_value = value
    if value.startswith('-'):
        if not allow_negative:
            return False
        check_value = value[1:]

    # Check for at most one decimal point (if allowed)
    if allow_decimal:
        if check_value.count('.') > 1:
            return False
        # Check that all remaining characters are digits or single decimal point
        return all(c.isdigit() or c == '.' for c in check_value)
    else:
        # No decimal allowed, only digits
        return check_value.isdigit()


def parse_numeric_value(value: str, default: float = 0.0) -> float:
    """
    Parse a numeric string value to float with fallback default.

    Args:
        value: String value to parse
        default: Default value if parsing fails

    Returns:
        Parsed float value or default
    """
    if not value or value.strip() == '':
        return default

    try:
        return float(value.strip())
    except ValueError:
        return default


# ==================== BALANCE CALCULATIONS ====================

def calculate_cursor_position_after_format(
    old_value: str,
    new_value: str,
    old_cursor_pos: int
) -> int:
    """
    Calculate new cursor position after formatting a value.

    Maintains cursor position relative to digits, not formatting characters.

    Args:
        old_value: Original value before formatting
        new_value: New value after formatting
        old_cursor_pos: Cursor position in old value

    Returns:
        New cursor position in formatted value
    """
    # Count how many digits are before the cursor in the old value
    digits_before_cursor = len(
        [c for c in old_value[:old_cursor_pos] if c.isdigit()])

    # Find the position in the new formatted string that corresponds
    # to the same number of digits
    new_cursor_pos = 0
    digit_count = 0
    for i, char in enumerate(new_value):
        if char.isdigit():
            digit_count += 1
        if digit_count >= digits_before_cursor:
            new_cursor_pos = i + 1
            break
    else:
        new_cursor_pos = len(new_value)

    return new_cursor_pos


def format_balance_value(value: float, decimal_places: int = 2) -> str:
    """
    Format a balance value to a fixed number of decimal places.

    Args:
        value: Numeric value to format
        decimal_places: Number of decimal places (default 2)

    Returns:
        Formatted string
    """
    return f"{value:.{decimal_places}f}"


# ==================== DATE PARSING FOR SORTING ====================

def parse_date_for_sorting(date_str: str) -> datetime:
    """
    Parse date string to datetime for sorting purposes.

    Supports multiple date formats and returns a datetime object for comparison.
    If date cannot be parsed, returns a far future date to push invalid dates to end.

    Args:
        date_str: Date string in various formats

    Returns:
        datetime object for sorting
    """
    date_formats = [
        '%Y-%m-%d',    # ISO format: 2025-10-01
        DATE_FORMAT_STRPTIME,  # Brazilian format: 01/10/2025
        '%m/%d/%Y',    # US format: 10/01/2025
        '%Y/%m/%d',    # Alternative ISO: 2025/10/01
        '%d-%m-%Y',    # Dash format: 01-10-2025
        '%d.%m.%Y',    # Dot format: 01.10.2025
        '%Y%m%d'       # Compact format: 20251001
    ]

    for fmt in date_formats:
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue

    # If no format matches, return far future date
    # This pushes unparseable dates to the end of the list
    return datetime(9999, 12, 31)


# ==================== CONVERSION VALIDATION ====================

def validate_conversion_prerequisites(
    csv_data: List[Dict],
    field_mappings: Dict[str, str],
    not_mapped_value: str = DEFAULT_NOT_MAPPED
) -> Tuple[bool, Optional[str]]:
    """
    Validate all prerequisites for CSV to OFX conversion.

    Args:
        csv_data: List of CSV row dictionaries
        field_mappings: Dictionary of field mappings
        not_mapped_value: Value representing unmapped field

    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check if CSV data is loaded
    if not csv_data:
        return False, "Please load a CSV file first"

    # Check required field mappings
    is_valid, error_msg = validate_required_field_mappings(
        field_mappings, not_mapped_value)
    if not is_valid:
        return False, error_msg

    return True, None


def validate_date_range_inputs(start_date: str, end_date: str) -> Tuple[bool, Optional[str]]:
    """
    Validate date range inputs for date validation feature.

    Args:
        start_date: Start date string
        end_date: End date string

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not start_date or start_date.strip() == '':
        return False, "Please enter a start date"

    if not end_date or end_date.strip() == '':
        return False, "Please enter an end date"

    # Validate format for both dates
    is_valid, error = validate_date_format(start_date, DATE_FORMAT_DISPLAY)
    if not is_valid:
        return False, f"Invalid start date: {error}"

    is_valid, error = validate_date_format(end_date, DATE_FORMAT_DISPLAY)
    if not is_valid:
        return False, f"Invalid end date: {error}"

    # Parse dates for comparison (strptime catches impossible calendar dates
    # like 31/02/2025 that pass the basic format check above)
    try:
        start_dt = datetime.strptime(start_date.strip(), DATE_FORMAT_STRPTIME)
    except ValueError:
        return False, "Invalid start date: date does not exist"

    try:
        end_dt = datetime.strptime(end_date.strip(), DATE_FORMAT_STRPTIME)
    except ValueError:
        return False, "Invalid end date: date does not exist"

    if end_dt < start_dt:
        return False, "End date must be greater than or equal to start date"

    return True, None


# ==================== STATISTICS FORMATTING ====================

def format_preview_stats(current_count: int, total_count: int, max_preview: int = 100) -> str:
    """
    Format preview statistics message.

    Args:
        current_count: Number of rows currently shown
        total_count: Total number of rows
        max_preview: Maximum rows shown in preview

    Returns:
        Formatted statistics string
    """
    stats_text = f"Showing {current_count} of {total_count} rows"
    if total_count > max_preview:
        stats_text += f" (limited to first {max_preview} for preview)"
    return stats_text


def format_conversion_stats(
    total_rows: int,
    processed: int,
    excluded: int,
    adjusted: int = 0,
    kept_out_of_range: int = 0,
    has_date_validator: bool = False
) -> str:
    """
    Format conversion statistics message.

    Args:
        total_rows: Total rows in CSV
        processed: Number of successfully processed transactions
        excluded: Number of excluded transactions
        adjusted: Number of dates adjusted (if date validation enabled)
        kept_out_of_range: Number of out-of-range dates kept (if date validation enabled)
        has_date_validator: Whether date validation was enabled

    Returns:
        Formatted statistics string
    """
    lines = [
        "Statistics:",
        f"  - Total rows processed: {total_rows}",
        f"  - Transactions exported: {processed}",
    ]

    if excluded > 0:
        lines.append(f"  - Transactions excluded: {excluded}")

    if has_date_validator and adjusted > 0:
        lines.append(f"  - Dates adjusted: {adjusted}")

    if has_date_validator and kept_out_of_range > 0:
        lines.append(f"  - Out-of-range dates kept: {kept_out_of_range}")

    return "\n".join(lines)
