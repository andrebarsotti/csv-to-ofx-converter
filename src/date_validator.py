"""
Date Validator Module
=====================
Validator for transaction dates against a specified date range.

Validates transactions to ensure they fall within a credit card statement period,
and provides options for handling out-of-range transactions.

Author: Generated for Brazilian banking compatibility
License: MIT
"""

import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class DateValidator:
    """
    Validator for transaction dates against a specified date range.

    Validates transactions to ensure they fall within a credit card statement period,
    and provides options for handling out-of-range transactions.
    """

    def __init__(self, start_date_str: str, end_date_str: str):
        """
        Initialize date validator with start and end dates.

        Args:
            start_date_str: Start date of the statement period (various formats)
            end_date_str: End date of the statement period (various formats)

        Raises:
            ValueError: If dates cannot be parsed
        """
        self.start_date = self._parse_date_to_datetime(start_date_str)
        self.end_date = self._parse_date_to_datetime(end_date_str)

        if self.start_date > self.end_date:
            raise ValueError("Start date must be before or equal to end date")

        logger.info(f"DateValidator initialized: {self.start_date.date()} to {self.end_date.date()}")

    def _parse_date_to_datetime(self, date_str: str) -> datetime:
        """
        Parse date string to datetime object.

        Args:
            date_str: Date string in various formats

        Returns:
            datetime object

        Raises:
            ValueError: If date format is not recognized
        """
        date_formats = [
            '%Y-%m-%d',      # 2025-10-22
            '%d/%m/%Y',      # 22/10/2025
            '%m/%d/%Y',      # 10/22/2025
            '%Y/%m/%d',      # 2025/10/22
            '%d-%m-%Y',      # 22-10-2025
            '%d.%m.%Y',      # 22.10.2025
            '%Y%m%d',        # 20251022
        ]

        date_str = date_str.strip()

        for fmt in date_formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue

        raise ValueError(f"Unrecognized date format: {date_str}")

    def is_within_range(self, date_str: str) -> bool:
        """
        Check if a date is within the valid range.

        Args:
            date_str: Date string to check

        Returns:
            True if date is within range, False otherwise
        """
        try:
            date_obj = self._parse_date_to_datetime(date_str)
            return self.start_date <= date_obj <= self.end_date
        except ValueError:
            return False

    def get_date_status(self, date_str: str) -> str:
        """
        Determine if a date is before, within, or after the valid range.

        Args:
            date_str: Date string to check

        Returns:
            'within', 'before', or 'after'

        Raises:
            ValueError: If date cannot be parsed
        """
        date_obj = self._parse_date_to_datetime(date_str)

        if date_obj < self.start_date:
            return 'before'
        elif date_obj > self.end_date:
            return 'after'
        else:
            return 'within'

    def adjust_date_to_boundary(self, date_str: str) -> str:
        """
        Adjust an out-of-range date to the nearest boundary.

        Args:
            date_str: Date string to adjust

        Returns:
            Adjusted date string in YYYY-MM-DD format

        Raises:
            ValueError: If date cannot be parsed
        """
        status = self.get_date_status(date_str)

        if status == 'before':
            return self.start_date.strftime('%Y-%m-%d')
        elif status == 'after':
            return self.end_date.strftime('%Y-%m-%d')
        else:
            # Already within range
            date_obj = self._parse_date_to_datetime(date_str)
            return date_obj.strftime('%Y-%m-%d')
