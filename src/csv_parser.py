"""
CSV Parser Module
=================
Parser for CSV files supporting both standard and Brazilian formats.

Author: Generated for Brazilian banking compatibility
License: MIT
"""

import csv
import os
import logging
from typing import List, Dict, Tuple

logger = logging.getLogger(__name__)


class CSVParser:
    """
    Parser for CSV files supporting both standard and Brazilian formats.

    Attributes:
        delimiter (str): Column separator character (default: ',')
        decimal_separator (str): Decimal separator for amounts (default: '.')
    """

    def __init__(self, delimiter: str = ',', decimal_separator: str = '.'):
        """
        Initialize CSV parser with format settings.

        Args:
            delimiter: Character used to separate columns
            decimal_separator: Character used as decimal point
        """
        self.delimiter = delimiter
        self.decimal_separator = decimal_separator
        logger.info(f"CSVParser initialized: delimiter='{delimiter}', decimal='{decimal_separator}'")

    def parse_file(self, filepath: str) -> Tuple[List[str], List[Dict[str, str]]]:
        """
        Parse CSV file and return headers and rows.

        Args:
            filepath: Path to the CSV file

        Returns:
            Tuple containing list of headers and list of row dictionaries

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file is empty or malformed
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"CSV file not found: {filepath}")

        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()

            # Try with utf-8-sig to handle BOM if present
            if content.startswith('\ufeff'):
                content = content[1:]

            lines = content.splitlines()
            if not lines:
                raise ValueError("CSV file is empty")

            reader = csv.DictReader(lines, delimiter=self.delimiter)
            headers = reader.fieldnames

            if not headers:
                raise ValueError("CSV file has no headers")

            rows = list(reader)
            logger.info(f"Parsed CSV: {len(rows)} rows, {len(headers)} columns")

            return list(headers), rows

        except Exception as e:
            logger.error(f"Error parsing CSV file: {e}")
            raise

    def normalize_amount(self, amount_str: str) -> float:
        """
        Convert amount string to float, handling different decimal separators.

        Args:
            amount_str: String representation of amount

        Returns:
            Float value of amount

        Raises:
            ValueError: If amount cannot be parsed
        """
        if not amount_str:
            return 0.0

        # Remove currency symbols and spaces
        clean_str = amount_str.strip().replace('R$', '').replace('$', '').strip()

        # Handle Brazilian format: 1.234,56 -> 1234.56
        if self.decimal_separator == ',':
            clean_str = clean_str.replace('.', '').replace(',', '.')
        else:
            # Handle standard format: 1,234.56 -> 1234.56
            clean_str = clean_str.replace(',', '')

        try:
            return float(clean_str)
        except ValueError as e:
            logger.error(f"Cannot parse amount '{amount_str}': {e}")
            raise ValueError(f"Invalid amount format: {amount_str}")
