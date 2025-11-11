#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit Tests for OFXGenerator
============================
Test cases for OFX file generation functionality.
"""

import unittest
import os
import tempfile
from src.csv_to_ofx_converter import OFXGenerator


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

    def test_value_inversion_feature(self):
        """Test value inversion feature (NEW in v2.0)."""
        generator = OFXGenerator(invert_values=True)

        # Add a debit transaction with negative amount
        generator.add_transaction(
            date='2025-10-01',
            amount=-100.50,
            description='Purchase',
            transaction_type='DEBIT'
        )

        # With inversion: amount should be inverted to positive and type to CREDIT
        self.assertEqual(generator.transactions[0]['amount'], 100.50)
        self.assertEqual(generator.transactions[0]['type'], 'CREDIT')

        # Add a credit transaction with positive amount
        generator.add_transaction(
            date='2025-10-02',
            amount=500.00,
            description='Payment',
            transaction_type='CREDIT'
        )

        # With inversion: amount should be negative and type should be DEBIT
        self.assertEqual(generator.transactions[1]['amount'], -500.00)
        self.assertEqual(generator.transactions[1]['type'], 'DEBIT')

    def test_value_inversion_with_complete_conversion(self):
        """Test value inversion in complete OFX generation (NEW in v2.0)."""
        generator = OFXGenerator(invert_values=True)

        # Add multiple transactions
        generator.add_transaction('2025-10-01', -100, 'Expense', 'DEBIT')
        generator.add_transaction('2025-10-02', 200, 'Income', 'CREDIT')

        output_file = os.path.join(self.temp_dir, 'inverted.ofx')
        generator.generate(
            output_path=output_file,
            account_id='TEST',
            bank_name='Test Bank'
        )

        with open(output_file, 'r') as f:
            content = f.read()

        # Check inverted amounts
        self.assertIn('<TRNAMT>100.00</TRNAMT>', content)  # Was -100, now 100
        self.assertIn('<TRNAMT>-200.00</TRNAMT>', content)  # Was 200, now -200

    def test_value_inversion_disabled(self):
        """Test normal operation with inversion disabled (NEW in v2.0)."""
        generator = OFXGenerator(invert_values=False)

        generator.add_transaction(
            date='2025-10-01',
            amount=-100.50,
            description='Purchase',
            transaction_type='DEBIT'
        )

        # Without inversion: should remain unchanged
        self.assertEqual(generator.transactions[0]['amount'], -100.50)
        self.assertEqual(generator.transactions[0]['type'], 'DEBIT')

    def test_initial_balance_in_ofx_output(self):
        """Test that initial balance appears in OFX output (NEW in v3.0)."""
        self.generator.add_transaction(
            date='2025-10-01',
            amount=-100.50,
            description='Purchase',
            transaction_type='DEBIT'
        )

        output_file = os.path.join(self.temp_dir, 'initial_balance.ofx')
        self.generator.generate(
            output_path=output_file,
            account_id='TEST',
            bank_name='Test Bank',
            initial_balance=1000.00
        )

        with open(output_file, 'r') as f:
            content = f.read()

        # Check that initial balance appears in AVAILBAL section
        self.assertIn('<AVAILBAL>', content)
        self.assertIn('<BALAMT>1000.00</BALAMT>', content)

    def test_auto_calculated_final_balance(self):
        """Test automatic calculation of final balance (NEW in v3.0)."""
        self.generator.add_transaction(
            date='2025-10-01',
            amount=-100.50,
            description='Purchase',
            transaction_type='DEBIT'
        )
        self.generator.add_transaction(
            date='2025-10-02',
            amount=500.00,
            description='Deposit',
            transaction_type='CREDIT'
        )

        output_file = os.path.join(self.temp_dir, 'auto_balance.ofx')
        initial = 1000.00
        # Expected: 1000 - 100.50 + 500 = 1399.50
        self.generator.generate(
            output_path=output_file,
            account_id='TEST',
            bank_name='Test Bank',
            initial_balance=initial,
            final_balance=None  # Auto-calculate
        )

        with open(output_file, 'r') as f:
            content = f.read()

        # Check calculated final balance in LEDGERBAL
        self.assertIn('<LEDGERBAL>', content)
        # The final balance should be 1399.50
        self.assertIn('<BALAMT>1399.50</BALAMT>', content)

    def test_manual_final_balance(self):
        """Test manually specified final balance (NEW in v3.0)."""
        self.generator.add_transaction(
            date='2025-10-01',
            amount=-100.50,
            description='Purchase',
            transaction_type='DEBIT'
        )

        output_file = os.path.join(self.temp_dir, 'manual_balance.ofx')
        manual_final = 2500.00
        self.generator.generate(
            output_path=output_file,
            account_id='TEST',
            bank_name='Test Bank',
            initial_balance=1000.00,
            final_balance=manual_final
        )

        with open(output_file, 'r') as f:
            content = f.read()

        # Check manual final balance appears in output
        self.assertIn(f'<BALAMT>{manual_final:.2f}</BALAMT>', content)

    def test_zero_initial_balance_default(self):
        """Test default initial balance of 0.0 (NEW in v3.0)."""
        self.generator.add_transaction(
            date='2025-10-01',
            amount=100.00,
            description='Deposit',
            transaction_type='CREDIT'
        )

        output_file = os.path.join(self.temp_dir, 'zero_initial.ofx')
        self.generator.generate(
            output_path=output_file,
            account_id='TEST',
            bank_name='Test Bank'
            # No initial_balance specified, should default to 0.00
        )

        with open(output_file, 'r') as f:
            content = f.read()

        # Should have initial balance of 0.00
        lines = content.split('\n')
        availbal_section = []
        in_availbal = False
        for line in lines:
            if '<AVAILBAL>' in line:
                in_availbal = True
            if in_availbal:
                availbal_section.append(line)
            if '</AVAILBAL>' in line:
                break

        availbal_text = '\n'.join(availbal_section)
        self.assertIn('<BALAMT>0.00</BALAMT>', availbal_text)

    def test_negative_initial_balance(self):
        """Test handling of negative initial balance (NEW in v3.0)."""
        self.generator.add_transaction(
            date='2025-10-01',
            amount=-50.00,
            description='Fee',
            transaction_type='DEBIT'
        )

        output_file = os.path.join(self.temp_dir, 'negative_initial.ofx')
        self.generator.generate(
            output_path=output_file,
            account_id='TEST',
            bank_name='Test Bank',
            initial_balance=-100.00  # Negative starting balance
        )

        with open(output_file, 'r') as f:
            content = f.read()

        # Should handle negative initial balance
        self.assertIn('<BALAMT>-100.00</BALAMT>', content)
        # Final should be -100 - 50 = -150
        self.assertIn('<BALAMT>-150.00</BALAMT>', content)


if __name__ == '__main__':
    unittest.main()
