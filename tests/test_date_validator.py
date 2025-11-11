#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit Tests for DateValidator
=============================
Test cases for date validation functionality.
"""

import unittest
from src.csv_to_ofx_converter import DateValidator


class TestDateValidator(unittest.TestCase):
    """Test cases for Date Validator."""

    def test_date_validator_initialization(self):
        """Test DateValidator initialization with valid dates."""
        validator = DateValidator('2025-10-01', '2025-10-31')
        self.assertEqual(validator.start_date.year, 2025)
        self.assertEqual(validator.start_date.month, 10)
        self.assertEqual(validator.start_date.day, 1)
        self.assertEqual(validator.end_date.day, 31)

    def test_date_validator_various_formats(self):
        """Test DateValidator with various date formats."""
        # Test with different date formats
        validators = [
            DateValidator('2025-10-01', '2025-10-31'),
            DateValidator('01/10/2025', '31/10/2025'),
            DateValidator('2025/10/01', '2025/10/31'),
        ]

        for validator in validators:
            self.assertEqual(validator.start_date.day, 1)
            self.assertEqual(validator.end_date.day, 31)

    def test_invalid_date_range(self):
        """Test DateValidator with invalid date range (start > end)."""
        with self.assertRaises(ValueError) as context:
            DateValidator('2025-10-31', '2025-10-01')
        self.assertIn("Start date must be before or equal to end date", str(context.exception))

    def test_invalid_date_format(self):
        """Test DateValidator with invalid date format."""
        with self.assertRaises(ValueError):
            DateValidator('invalid-date', '2025-10-31')

        with self.assertRaises(ValueError):
            DateValidator('2025-10-01', 'invalid-date')

    def test_is_within_range(self):
        """Test checking if dates are within range."""
        validator = DateValidator('2025-10-01', '2025-10-31')

        # Dates within range
        self.assertTrue(validator.is_within_range('2025-10-01'))
        self.assertTrue(validator.is_within_range('2025-10-15'))
        self.assertTrue(validator.is_within_range('2025-10-31'))

        # Dates outside range
        self.assertFalse(validator.is_within_range('2025-09-30'))
        self.assertFalse(validator.is_within_range('2025-11-01'))
        self.assertFalse(validator.is_within_range('2024-10-15'))
        self.assertFalse(validator.is_within_range('2026-10-15'))

    def test_is_within_range_different_formats(self):
        """Test date range checking with different date formats."""
        validator = DateValidator('2025-10-01', '2025-10-31')

        # Test with different formats
        self.assertTrue(validator.is_within_range('15/10/2025'))
        self.assertTrue(validator.is_within_range('2025/10/15'))
        self.assertFalse(validator.is_within_range('30/09/2025'))

    def test_get_date_status(self):
        """Test determining date status (before, within, after)."""
        validator = DateValidator('2025-10-01', '2025-10-31')

        # Before range
        self.assertEqual(validator.get_date_status('2025-09-30'), 'before')
        self.assertEqual(validator.get_date_status('2025-09-15'), 'before')
        self.assertEqual(validator.get_date_status('2024-10-15'), 'before')

        # Within range
        self.assertEqual(validator.get_date_status('2025-10-01'), 'within')
        self.assertEqual(validator.get_date_status('2025-10-15'), 'within')
        self.assertEqual(validator.get_date_status('2025-10-31'), 'within')

        # After range
        self.assertEqual(validator.get_date_status('2025-11-01'), 'after')
        self.assertEqual(validator.get_date_status('2025-11-15'), 'after')
        self.assertEqual(validator.get_date_status('2026-10-15'), 'after')

    def test_adjust_date_to_boundary(self):
        """Test adjusting out-of-range dates to boundaries."""
        validator = DateValidator('2025-10-01', '2025-10-31')

        # Dates before range should adjust to start date
        self.assertEqual(validator.adjust_date_to_boundary('2025-09-30'), '2025-10-01')
        self.assertEqual(validator.adjust_date_to_boundary('2025-09-15'), '2025-10-01')
        self.assertEqual(validator.adjust_date_to_boundary('2024-10-15'), '2025-10-01')

        # Dates after range should adjust to end date
        self.assertEqual(validator.adjust_date_to_boundary('2025-11-01'), '2025-10-31')
        self.assertEqual(validator.adjust_date_to_boundary('2025-11-15'), '2025-10-31')
        self.assertEqual(validator.adjust_date_to_boundary('2026-10-15'), '2025-10-31')

        # Dates within range should remain unchanged (but normalized to YYYY-MM-DD)
        self.assertEqual(validator.adjust_date_to_boundary('2025-10-15'), '2025-10-15')
        self.assertEqual(validator.adjust_date_to_boundary('15/10/2025'), '2025-10-15')

    def test_boundary_dates(self):
        """Test exact boundary dates."""
        validator = DateValidator('2025-10-01', '2025-10-31')

        # Boundary dates should be within range
        self.assertTrue(validator.is_within_range('2025-10-01'))
        self.assertTrue(validator.is_within_range('2025-10-31'))
        self.assertEqual(validator.get_date_status('2025-10-01'), 'within')
        self.assertEqual(validator.get_date_status('2025-10-31'), 'within')

    def test_same_start_and_end_date(self):
        """Test validator with same start and end date."""
        validator = DateValidator('2025-10-15', '2025-10-15')

        self.assertTrue(validator.is_within_range('2025-10-15'))
        self.assertFalse(validator.is_within_range('2025-10-14'))
        self.assertFalse(validator.is_within_range('2025-10-16'))

        self.assertEqual(validator.get_date_status('2025-10-14'), 'before')
        self.assertEqual(validator.get_date_status('2025-10-15'), 'within')
        self.assertEqual(validator.get_date_status('2025-10-16'), 'after')

    def test_year_boundary(self):
        """Test validator across year boundaries."""
        validator = DateValidator('2025-12-15', '2026-01-15')

        self.assertTrue(validator.is_within_range('2025-12-31'))
        self.assertTrue(validator.is_within_range('2026-01-01'))
        self.assertTrue(validator.is_within_range('2026-01-10'))

        self.assertFalse(validator.is_within_range('2025-12-14'))
        self.assertFalse(validator.is_within_range('2026-01-16'))

    def test_leap_year_date(self):
        """Test validator with leap year date."""
        validator = DateValidator('2024-02-28', '2024-03-01')

        self.assertTrue(validator.is_within_range('2024-02-29'))  # Leap year
        self.assertEqual(validator.get_date_status('2024-02-29'), 'within')


if __name__ == '__main__':
    unittest.main()
