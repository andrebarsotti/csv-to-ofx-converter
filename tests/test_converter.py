#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit Tests for CSV to OFX Converter
====================================
Comprehensive test suite for the CSV to OFX converter application.

Tests cover:
- CSV parsing with different formats
- Amount normalization
- Date parsing
- OFX generation
- Error handling
"""

import unittest
import os
import tempfile
from datetime import datetime
from src.csv_to_ofx_converter import CSVParser, OFXGenerator, DateValidator


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


class TestOFXGenerator(unittest.TestCase):
    """Test cases for OFX Generator."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.generator = OFXGenerator()

    def tearDown(self):
        """Clean up test files."""
        for file in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, file))
        os.rmdir(self.temp_dir)

    def test_add_transaction(self):
        """Test adding transactions."""
        self.generator.add_transaction(
            date='2025-10-01',
            amount=-100.50,
            description='Test Purchase',
            transaction_type='DEBIT'
        )

        self.assertEqual(len(self.generator.transactions), 1)
        self.assertEqual(self.generator.transactions[0]['type'], 'DEBIT')
        self.assertEqual(self.generator.transactions[0]['amount'], -100.50)
        self.assertEqual(self.generator.transactions[0]['memo'], 'Test Purchase')

    def test_add_credit_transaction(self):
        """Test adding credit transaction."""
        self.generator.add_transaction(
            date='2025-10-01',
            amount=1000.00,
            description='Salary',
            transaction_type='CREDIT'
        )

        self.assertEqual(self.generator.transactions[0]['type'], 'CREDIT')
        self.assertEqual(self.generator.transactions[0]['amount'], 1000.00)

    def test_date_parsing_formats(self):
        """Test various date format parsing."""
        test_dates = [
            ('2025-10-22', '20251022000000[-3:BRT]'),
            ('22/10/2025', '20251022000000[-3:BRT]'),
            ('10/22/2025', '20251022000000[-3:BRT]'),
            ('2025/10/22', '20251022000000[-3:BRT]'),
            ('22-10-2025', '20251022000000[-3:BRT]'),
            ('22.10.2025', '20251022000000[-3:BRT]'),
            ('20251022', '20251022000000[-3:BRT]'),
        ]

        for date_str, expected_ofx_date in test_dates:
            parsed = self.generator._parse_date(date_str)
            self.assertEqual(parsed, expected_ofx_date,
                           f"Failed to parse {date_str}")

    def test_invalid_date_format(self):
        """Test handling of invalid date format."""
        with self.assertRaises(ValueError):
            self.generator._parse_date('invalid-date')

        with self.assertRaises(ValueError):
            self.generator._parse_date('32/13/2025')

    def test_generate_ofx_file(self):
        """Test OFX file generation."""
        self.generator.add_transaction(
            date='2025-10-01',
            amount=-100.50,
            description='Purchase 1',
            transaction_type='DEBIT'
        )
        self.generator.add_transaction(
            date='2025-10-02',
            amount=-50.25,
            description='Purchase 2',
            transaction_type='DEBIT'
        )
        self.generator.add_transaction(
            date='2025-10-03',
            amount=1000.00,
            description='Salary',
            transaction_type='CREDIT'
        )

        output_file = os.path.join(self.temp_dir, 'test.ofx')
        self.generator.generate(
            output_path=output_file,
            account_id='TEST123',
            bank_name='Test Bank',
            currency='BRL'
        )

        # Verify file was created
        self.assertTrue(os.path.exists(output_file))

        # Read and verify content
        with open(output_file, 'r') as f:
            content = f.read()

        # Check header
        self.assertIn('OFXHEADER:100', content)
        self.assertIn('VERSION:102', content)

        # Check bank info
        self.assertIn('<ORG>Test Bank</ORG>', content)
        self.assertIn('<ACCTID>TEST123</ACCTID>', content)
        self.assertIn('<CURDEF>BRL</CURDEF>', content)

        # Check transactions
        self.assertIn('<TRNAMT>-100.50</TRNAMT>', content)
        self.assertIn('<TRNAMT>-50.25</TRNAMT>', content)
        self.assertIn('<TRNAMT>1000.00</TRNAMT>', content)
        self.assertIn('<MEMO>Purchase 1</MEMO>', content)
        self.assertIn('<MEMO>Purchase 2</MEMO>', content)
        self.assertIn('<MEMO>Salary</MEMO>', content)

        # Check balance
        expected_balance = -100.50 - 50.25 + 1000.00
        self.assertIn(f'<BALAMT>{expected_balance:.2f}</BALAMT>', content)

    def test_generate_without_transactions(self):
        """Test OFX generation without transactions."""
        output_file = os.path.join(self.temp_dir, 'empty.ofx')

        with self.assertRaises(ValueError):
            self.generator.generate(output_path=output_file)

    def test_transaction_sorting_by_date(self):
        """Test that transactions are sorted by date."""
        self.generator.add_transaction('2025-10-03', -100, 'Third')
        self.generator.add_transaction('2025-10-01', -200, 'First')
        self.generator.add_transaction('2025-10-02', -150, 'Second')

        output_file = os.path.join(self.temp_dir, 'sorted.ofx')
        self.generator.generate(output_path=output_file, account_id='TEST')

        # Verify transactions are sorted
        dates = [t['date'] for t in self.generator.transactions]
        self.assertEqual(dates, sorted(dates))

    def test_auto_correct_transaction_type_amount(self):
        """Test automatic correction of amount sign based on transaction type."""
        # Debit with positive amount should become negative
        self.generator.add_transaction(
            date='2025-10-01',
            amount=100.50,
            description='Debit with positive amount',
            transaction_type='DEBIT'
        )
        self.assertEqual(self.generator.transactions[0]['amount'], -100.50)

        # Credit with negative amount should become positive
        self.generator.add_transaction(
            date='2025-10-02',
            amount=-200.00,
            description='Credit with negative amount',
            transaction_type='CREDIT'
        )
        self.assertEqual(self.generator.transactions[1]['amount'], 200.00)

    def test_transaction_id_generation(self):
        """Test automatic transaction ID generation."""
        self.generator.add_transaction(
            date='2025-10-01',
            amount=-100,
            description='Test'
        )

        # Should have auto-generated UUID
        trans_id = self.generator.transactions[0]['id']
        self.assertIsNotNone(trans_id)
        self.assertEqual(len(trans_id), 36)  # UUID length

    def test_long_description_truncation(self):
        """Test that long descriptions are truncated."""
        long_description = 'A' * 300  # 300 characters

        self.generator.add_transaction(
            date='2025-10-01',
            amount=-100,
            description=long_description
        )

        # Should be truncated to 255 characters
        self.assertEqual(len(self.generator.transactions[0]['memo']), 255)

    def test_multiple_currency_support(self):
        """Test OFX generation with different currencies."""
        currencies = ['BRL', 'USD', 'EUR', 'GBP']

        for currency in currencies:
            generator = OFXGenerator()
            generator.add_transaction('2025-10-01', -100, 'Test')

            output_file = os.path.join(self.temp_dir, f'test_{currency}.ofx')
            generator.generate(
                output_path=output_file,
                account_id='TEST',
                currency=currency
            )

            with open(output_file, 'r') as f:
                content = f.read()

            self.assertIn(f'<CURDEF>{currency}</CURDEF>', content)


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


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete conversion process."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test files."""
        for file in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, file))
        os.rmdir(self.temp_dir)

    def test_complete_conversion_standard_format(self):
        """Test complete conversion from CSV to OFX (standard format)."""
        # Create test CSV
        csv_content = """date,amount,description,type
2025-10-01,-100.50,Purchase 1,DEBIT
2025-10-02,-50.25,Purchase 2,DEBIT
2025-10-03,1000.00,Salary,CREDIT"""

        csv_file = os.path.join(self.temp_dir, 'test.csv')
        with open(csv_file, 'w') as f:
            f.write(csv_content)

        # Parse CSV
        parser = CSVParser(delimiter=',', decimal_separator='.')
        headers, rows = parser.parse_file(csv_file)

        # Generate OFX
        generator = OFXGenerator()
        for row in rows:
            generator.add_transaction(
                date=row['date'],
                amount=parser.normalize_amount(row['amount']),
                description=row['description'],
                transaction_type=row['type']
            )

        output_file = os.path.join(self.temp_dir, 'output.ofx')
        generator.generate(
            output_path=output_file,
            account_id='TEST123',
            bank_name='Test Bank'
        )

        # Verify output
        self.assertTrue(os.path.exists(output_file))

        with open(output_file, 'r') as f:
            content = f.read()

        self.assertIn('<ACCTID>TEST123</ACCTID>', content)
        self.assertIn('<MEMO>Purchase 1</MEMO>', content)
        self.assertIn('<MEMO>Purchase 2</MEMO>', content)
        self.assertIn('<MEMO>Salary</MEMO>', content)

    def test_complete_conversion_brazilian_format(self):
        """Test complete conversion from CSV to OFX (Brazilian format)."""
        # Create test CSV
        csv_content = """data;valor;descricao;tipo
01/10/2025;-100,50;Compra 1;DEBIT
02/10/2025;-50,25;Compra 2;DEBIT
03/10/2025;1.000,00;Salário;CREDIT"""

        csv_file = os.path.join(self.temp_dir, 'test_br.csv')
        with open(csv_file, 'w', encoding='utf-8') as f:
            f.write(csv_content)

        # Parse CSV
        parser = CSVParser(delimiter=';', decimal_separator=',')
        headers, rows = parser.parse_file(csv_file)

        # Generate OFX
        generator = OFXGenerator()
        for row in rows:
            generator.add_transaction(
                date=row['data'],
                amount=parser.normalize_amount(row['valor']),
                description=row['descricao'],
                transaction_type=row['tipo']
            )

        output_file = os.path.join(self.temp_dir, 'output_br.ofx')
        generator.generate(
            output_path=output_file,
            account_id='BR123',
            bank_name='Banco Teste',
            currency='BRL'
        )

        # Verify output
        self.assertTrue(os.path.exists(output_file))

        with open(output_file, 'r') as f:
            content = f.read()

        self.assertIn('<CURDEF>BRL</CURDEF>', content)
        self.assertIn('<MEMO>Compra 1</MEMO>', content)
        self.assertIn('<TRNAMT>-100.50</TRNAMT>', content)
        self.assertIn('<TRNAMT>1000.00</TRNAMT>', content)


def run_tests():
    """Run all tests and display results."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestCSVParser))
    suite.addTests(loader.loadTestsFromTestCase(TestOFXGenerator))
    suite.addTests(loader.loadTestsFromTestCase(TestDateValidator))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    exit(run_tests())
