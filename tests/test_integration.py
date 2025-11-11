#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integration Tests for CSV to OFX Converter
===========================================
Test cases for the complete conversion process.
"""

import unittest
import os
import tempfile
from src.csv_to_ofx_converter import CSVParser, OFXGenerator


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

    def test_composite_description(self):
        """Test composite description feature (NEW in v2.0)."""
        # Create test CSV with multiple columns for description
        csv_content = """date,category,merchant,notes,amount
2025-10-01,Food,Restaurant ABC,Business lunch,-75.50
2025-10-02,Transport,Uber,Airport trip,-25.00
2025-10-03,Salary,Company XYZ,Monthly payment,3000.00"""

        csv_file = os.path.join(self.temp_dir, 'test_composite.csv')
        with open(csv_file, 'w') as f:
            f.write(csv_content)

        # Parse CSV
        parser = CSVParser(delimiter=',', decimal_separator='.')
        headers, rows = parser.parse_file(csv_file)

        # Generate OFX with composite descriptions
        generator = OFXGenerator()
        for row in rows:
            # Simulate composite description: combine category, merchant, and notes
            description_parts = []
            for col in ['category', 'merchant', 'notes']:
                if row[col].strip():
                    description_parts.append(row[col].strip())
            composite_description = ' - '.join(description_parts)

            generator.add_transaction(
                date=row['date'],
                amount=parser.normalize_amount(row['amount']),
                description=composite_description,
                transaction_type='DEBIT' if parser.normalize_amount(row['amount']) < 0 else 'CREDIT'
            )

        output_file = os.path.join(self.temp_dir, 'output_composite.ofx')
        generator.generate(
            output_path=output_file,
            account_id='TEST123',
            bank_name='Test Bank'
        )

        # Verify output
        with open(output_file, 'r') as f:
            content = f.read()

        # Check composite descriptions
        self.assertIn('<MEMO>Food - Restaurant ABC - Business lunch</MEMO>', content)
        self.assertIn('<MEMO>Transport - Uber - Airport trip</MEMO>', content)
        self.assertIn('<MEMO>Salary - Company XYZ - Monthly payment</MEMO>', content)

    def test_value_inversion_integration(self):
        """Test value inversion in complete workflow (NEW in v2.0)."""
        # Create test CSV with positive expenses (should be inverted)
        csv_content = """date,amount,description
2025-10-01,100.50,Expense (should be negative)
2025-10-02,50.25,Expense (should be negative)
2025-10-03,-1000.00,Income (should be positive)"""

        csv_file = os.path.join(self.temp_dir, 'test_invert.csv')
        with open(csv_file, 'w') as f:
            f.write(csv_content)

        # Parse CSV
        parser = CSVParser(delimiter=',', decimal_separator='.')
        headers, rows = parser.parse_file(csv_file)

        # Generate OFX with value inversion
        generator = OFXGenerator(invert_values=True)
        for row in rows:
            amount = parser.normalize_amount(row['amount'])
            generator.add_transaction(
                date=row['date'],
                amount=amount,
                description=row['description'],
                transaction_type='DEBIT' if amount < 0 else 'CREDIT'
            )

        output_file = os.path.join(self.temp_dir, 'output_inverted.ofx')
        generator.generate(
            output_path=output_file,
            account_id='TEST123',
            bank_name='Test Bank'
        )

        # Verify output
        with open(output_file, 'r') as f:
            content = f.read()

        # Check inverted amounts
        self.assertIn('<TRNAMT>-100.50</TRNAMT>', content)  # Was 100.50
        self.assertIn('<TRNAMT>-50.25</TRNAMT>', content)   # Was 50.25
        self.assertIn('<TRNAMT>1000.00</TRNAMT>', content)  # Was -1000.00

    def test_composite_description_with_different_separators(self):
        """Test composite descriptions with various separators (NEW in v2.0)."""
        csv_content = """date,col1,col2,col3,amount
2025-10-01,A,B,C,-100"""

        csv_file = os.path.join(self.temp_dir, 'test_sep.csv')
        with open(csv_file, 'w') as f:
            f.write(csv_content)

        parser = CSVParser(delimiter=',', decimal_separator='.')
        headers, rows = parser.parse_file(csv_file)

        # Test different separators
        separators = {
            ' ': 'A B C',
            ' - ': 'A - B - C',
            ', ': 'A, B, C',
            ' | ': 'A | B | C'
        }

        for sep, expected_desc in separators.items():
            generator = OFXGenerator()
            row = rows[0]

            description_parts = [row['col1'], row['col2'], row['col3']]
            composite_description = sep.join(description_parts)

            generator.add_transaction(
                date=row['date'],
                amount=parser.normalize_amount(row['amount']),
                description=composite_description
            )

            output_file = os.path.join(self.temp_dir, f'output_sep_{len(generator.transactions)}.ofx')
            generator.generate(output_path=output_file, account_id='TEST')

            with open(output_file, 'r') as f:
                content = f.read()

            self.assertIn(f'<MEMO>{expected_desc}</MEMO>', content)


if __name__ == '__main__':
    unittest.main()
