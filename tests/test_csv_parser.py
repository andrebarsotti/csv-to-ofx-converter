#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit Tests for CSVParser
=========================
Test cases for CSV parsing functionality.
"""

import unittest
import os
import tempfile
from src.csv_to_ofx_converter import CSVParser


class TestCSVParser(unittest.TestCase):
    """Test cases for CSV Parser."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test files."""
        for file in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, file))
        os.rmdir(self.temp_dir)

    def test_standard_csv_parsing(self):
        """Test parsing standard CSV format (comma-separated, dot decimal)."""
        csv_content = """date,amount,description
2025-10-01,100.50,Purchase 1
2025-10-02,-50.25,Refund 1
2025-10-03,200.00,Purchase 2"""

        csv_file = os.path.join(self.temp_dir, 'test.csv')
        with open(csv_file, 'w') as f:
            f.write(csv_content)

        parser = CSVParser(delimiter=',', decimal_separator='.')
        headers, rows = parser.parse_file(csv_file)

        self.assertEqual(headers, ['date', 'amount', 'description'])
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0]['date'], '2025-10-01')
        self.assertEqual(rows[0]['amount'], '100.50')

    def test_brazilian_csv_parsing(self):
        """Test parsing Brazilian CSV format (semicolon-separated, comma decimal)."""
        csv_content = """data;valor;descricao
01/10/2025;100,50;Compra 1
02/10/2025;-50,25;Reembolso 1
03/10/2025;200,00;Compra 2"""

        csv_file = os.path.join(self.temp_dir, 'test_br.csv')
        with open(csv_file, 'w', encoding='utf-8') as f:
            f.write(csv_content)

        parser = CSVParser(delimiter=';', decimal_separator=',')
        headers, rows = parser.parse_file(csv_file)

        self.assertEqual(headers, ['data', 'valor', 'descricao'])
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0]['data'], '01/10/2025')

    def test_normalize_amount_standard_format(self):
        """Test amount normalization for standard format."""
        parser = CSVParser(delimiter=',', decimal_separator='.')

        self.assertEqual(parser.normalize_amount('100.50'), 100.50)
        self.assertEqual(parser.normalize_amount('-50.25'), -50.25)
        self.assertEqual(parser.normalize_amount('1,234.56'), 1234.56)
        self.assertEqual(parser.normalize_amount('R$ 100.50'), 100.50)
        self.assertEqual(parser.normalize_amount('$100.50'), 100.50)

    def test_normalize_amount_brazilian_format(self):
        """Test amount normalization for Brazilian format."""
        parser = CSVParser(delimiter=';', decimal_separator=',')

        self.assertEqual(parser.normalize_amount('100,50'), 100.50)
        self.assertEqual(parser.normalize_amount('-50,25'), -50.25)
        self.assertEqual(parser.normalize_amount('1.234,56'), 1234.56)
        self.assertEqual(parser.normalize_amount('R$ 1.234,56'), 1234.56)

    def test_normalize_amount_edge_cases(self):
        """Test amount normalization edge cases."""
        parser = CSVParser()

        self.assertEqual(parser.normalize_amount(''), 0.0)
        self.assertEqual(parser.normalize_amount('0'), 0.0)
        self.assertEqual(parser.normalize_amount('0.00'), 0.0)

        with self.assertRaises(ValueError):
            parser.normalize_amount('invalid')

        with self.assertRaises(ValueError):
            parser.normalize_amount('abc123')

    def test_empty_csv_file(self):
        """Test handling of empty CSV file."""
        csv_file = os.path.join(self.temp_dir, 'empty.csv')
        with open(csv_file, 'w') as f:
            f.write('')

        parser = CSVParser()
        with self.assertRaises(ValueError):
            parser.parse_file(csv_file)

    def test_nonexistent_file(self):
        """Test handling of non-existent file."""
        parser = CSVParser()
        with self.assertRaises(FileNotFoundError):
            parser.parse_file('/nonexistent/file.csv')

    def test_csv_with_bom(self):
        """Test parsing CSV file with BOM (Byte Order Mark)."""
        csv_content = "\ufeffdate,amount,description\n2025-10-01,100.50,Purchase"
        csv_file = os.path.join(self.temp_dir, 'test_bom.csv')
        with open(csv_file, 'w', encoding='utf-8') as f:
            f.write(csv_content)

        parser = CSVParser()
        headers, rows = parser.parse_file(csv_file)

        self.assertEqual(headers[0], 'date')  # BOM should be removed


if __name__ == '__main__':
    unittest.main()
