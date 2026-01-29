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

    def test_deterministic_fitid_consistency(self):
        """Test that same transaction data produces same FITID across multiple conversions."""
        # Create test CSV with consistent data
        csv_content = """date,amount,description
2025-10-01,-100.50,Restaurant Purchase
2025-10-02,-50.25,Gas Station
2025-10-03,1000.00,Salary Payment"""

        csv_file = os.path.join(self.temp_dir, 'test_fitid.csv')
        with open(csv_file, 'w') as f:
            f.write(csv_content)

        # Parse CSV
        parser = CSVParser(delimiter=',', decimal_separator='.')
        headers, rows = parser.parse_file(csv_file)

        # Generate OFX twice with same data
        fitids_first = []
        fitids_second = []

        for run in range(2):
            generator = OFXGenerator()
            for row in rows:
                generator.add_transaction(
                    date=row['date'],
                    amount=parser.normalize_amount(row['amount']),
                    description=row['description']
                )

            output_file = os.path.join(self.temp_dir, f'output_fitid_{run}.ofx')
            generator.generate(
                output_path=output_file,
                account_id='TEST123',
                bank_name='Test Bank'
            )

            # Extract FITIDs from generated file
            with open(output_file, 'r') as f:
                content = f.read()
                import re
                fitids = re.findall(r'<FITID>(.*?)</FITID>', content)
                if run == 0:
                    fitids_first = fitids
                else:
                    fitids_second = fitids

        # Verify FITIDs are identical across both runs
        self.assertEqual(len(fitids_first), 3, "Should have 3 transactions")
        self.assertEqual(len(fitids_second), 3, "Should have 3 transactions")
        self.assertEqual(fitids_first, fitids_second, "FITIDs should be deterministic")

        # Verify FITIDs are valid UUIDs
        import uuid
        for fitid in fitids_first:
            try:
                uuid.UUID(fitid)
            except ValueError:
                self.fail(f"Invalid UUID format: {fitid}")

    def test_deterministic_fitid_different_data(self):
        """Test that different transaction data produces different FITIDs."""
        csv_content = """date,amount,description
2025-10-01,-100.50,Purchase A
2025-10-01,-100.50,Purchase B
2025-10-01,-200.50,Purchase A
2025-10-02,-100.50,Purchase A"""

        csv_file = os.path.join(self.temp_dir, 'test_diff.csv')
        with open(csv_file, 'w') as f:
            f.write(csv_content)

        parser = CSVParser(delimiter=',', decimal_separator='.')
        headers, rows = parser.parse_file(csv_file)

        generator = OFXGenerator()
        for row in rows:
            generator.add_transaction(
                date=row['date'],
                amount=parser.normalize_amount(row['amount']),
                description=row['description']
            )

        output_file = os.path.join(self.temp_dir, 'output_different.ofx')
        generator.generate(
            output_path=output_file,
            account_id='TEST123',
            bank_name='Test Bank'
        )

        # Extract FITIDs
        with open(output_file, 'r') as f:
            content = f.read()
            import re
            fitids = re.findall(r'<FITID>(.*?)</FITID>', content)

        # Verify all FITIDs are unique (different data = different IDs)
        self.assertEqual(len(fitids), 4, "Should have 4 transactions")
        self.assertEqual(len(set(fitids)), 4, "All FITIDs should be unique")

    def test_deterministic_fitid_backward_compatibility(self):
        """Test that explicit transaction IDs are preserved (backward compatibility)."""
        csv_content = """date,amount,description,id
2025-10-01,-100.50,Purchase 1,CUSTOM-ID-001
2025-10-02,-50.25,Purchase 2,CUSTOM-ID-002
2025-10-03,1000.00,Salary,CUSTOM-ID-003"""

        csv_file = os.path.join(self.temp_dir, 'test_explicit_id.csv')
        with open(csv_file, 'w') as f:
            f.write(csv_content)

        parser = CSVParser(delimiter=',', decimal_separator='.')
        headers, rows = parser.parse_file(csv_file)

        generator = OFXGenerator()
        for row in rows:
            generator.add_transaction(
                date=row['date'],
                amount=parser.normalize_amount(row['amount']),
                description=row['description'],
                transaction_id=row['id']  # Explicit ID provided
            )

        output_file = os.path.join(self.temp_dir, 'output_explicit.ofx')
        generator.generate(
            output_path=output_file,
            account_id='TEST123',
            bank_name='Test Bank'
        )

        # Verify explicit IDs are preserved
        with open(output_file, 'r') as f:
            content = f.read()

        self.assertIn('<FITID>CUSTOM-ID-001</FITID>', content)
        self.assertIn('<FITID>CUSTOM-ID-002</FITID>', content)
        self.assertIn('<FITID>CUSTOM-ID-003</FITID>', content)

    def test_deterministic_fitid_partial_file_regeneration(self):
        """Test use case: regenerating partial CSV files produces consistent FITIDs."""
        # Simulate user exporting January 1-15, then January 1-31
        # Transactions from Jan 1-15 should have same FITIDs in both exports

        # First export: Jan 1-15
        csv_content_partial = """date,amount,description
2025-01-05,-100.50,Restaurant
2025-01-10,-50.25,Gas Station
2025-01-15,1000.00,Salary"""

        csv_file_partial = os.path.join(self.temp_dir, 'jan_1_15.csv')
        with open(csv_file_partial, 'w') as f:
            f.write(csv_content_partial)

        parser = CSVParser(delimiter=',', decimal_separator='.')
        headers, rows_partial = parser.parse_file(csv_file_partial)

        generator_partial = OFXGenerator()
        for row in rows_partial:
            generator_partial.add_transaction(
                date=row['date'],
                amount=parser.normalize_amount(row['amount']),
                description=row['description']
            )

        output_partial = os.path.join(self.temp_dir, 'jan_1_15.ofx')
        generator_partial.generate(
            output_path=output_partial,
            account_id='TEST123',
            bank_name='Test Bank'
        )

        # Extract FITIDs from partial export
        with open(output_partial, 'r') as f:
            content_partial = f.read()
            import re
            fitids_partial = re.findall(r'<FITID>(.*?)</FITID>', content_partial)

        # Second export: Jan 1-31 (includes all previous transactions plus new ones)
        csv_content_full = """date,amount,description
2025-01-05,-100.50,Restaurant
2025-01-10,-50.25,Gas Station
2025-01-15,1000.00,Salary
2025-01-20,-75.00,Shopping
2025-01-25,-125.50,Utilities"""

        csv_file_full = os.path.join(self.temp_dir, 'jan_1_31.csv')
        with open(csv_file_full, 'w') as f:
            f.write(csv_content_full)

        headers, rows_full = parser.parse_file(csv_file_full)

        generator_full = OFXGenerator()
        for row in rows_full:
            generator_full.add_transaction(
                date=row['date'],
                amount=parser.normalize_amount(row['amount']),
                description=row['description']
            )

        output_full = os.path.join(self.temp_dir, 'jan_1_31.ofx')
        generator_full.generate(
            output_path=output_full,
            account_id='TEST123',
            bank_name='Test Bank'
        )

        # Extract FITIDs from full export
        with open(output_full, 'r') as f:
            content_full = f.read()
            fitids_full = re.findall(r'<FITID>(.*?)</FITID>', content_full)

        # Verify: First 3 FITIDs should match (overlapping transactions)
        self.assertEqual(len(fitids_partial), 3, "Partial export should have 3 transactions")
        self.assertEqual(len(fitids_full), 5, "Full export should have 5 transactions")
        self.assertEqual(fitids_partial, fitids_full[:3],
                        "Overlapping transactions should have same FITIDs")

    def test_deterministic_fitid_with_value_inversion(self):
        """Test deterministic FITID generation when value inversion is enabled."""
        csv_content = """date,amount,description
2025-10-01,100.50,Expense
2025-10-02,50.25,Purchase"""

        csv_file = os.path.join(self.temp_dir, 'test_invert_fitid.csv')
        with open(csv_file, 'w') as f:
            f.write(csv_content)

        parser = CSVParser(delimiter=',', decimal_separator='.')
        headers, rows = parser.parse_file(csv_file)

        # Generate without inversion
        generator_no_invert = OFXGenerator(invert_values=False)
        for row in rows:
            generator_no_invert.add_transaction(
                date=row['date'],
                amount=parser.normalize_amount(row['amount']),
                description=row['description']
            )

        output_no_invert = os.path.join(self.temp_dir, 'no_invert.ofx')
        generator_no_invert.generate(
            output_path=output_no_invert,
            account_id='TEST123',
            bank_name='Test Bank'
        )

        # Generate with inversion
        generator_invert = OFXGenerator(invert_values=True)
        for row in rows:
            generator_invert.add_transaction(
                date=row['date'],
                amount=parser.normalize_amount(row['amount']),
                description=row['description']
            )

        output_invert = os.path.join(self.temp_dir, 'with_invert.ofx')
        generator_invert.generate(
            output_path=output_invert,
            account_id='TEST123',
            bank_name='Test Bank'
        )

        # Extract FITIDs from both files
        import re
        with open(output_no_invert, 'r') as f:
            fitids_no_invert = re.findall(r'<FITID>(.*?)</FITID>', f.read())

        with open(output_invert, 'r') as f:
            fitids_invert = re.findall(r'<FITID>(.*?)</FITID>', f.read())

        # FITIDs should be different because inverted amounts are used in FITID calculation
        self.assertEqual(len(fitids_no_invert), 2)
        self.assertEqual(len(fitids_invert), 2)
        self.assertNotEqual(fitids_no_invert[0], fitids_invert[0],
                           "FITIDs should differ when amounts are inverted")
        self.assertNotEqual(fitids_no_invert[1], fitids_invert[1],
                           "FITIDs should differ when amounts are inverted")

    def test_deterministic_fitid_brazilian_format(self):
        """Test deterministic FITID generation with Brazilian CSV format."""
        csv_content = """data;valor;descricao
01/10/2025;-100,50;Restaurante
02/10/2025;-50,25;Posto de Gasolina
03/10/2025;1.000,00;Salário"""

        csv_file = os.path.join(self.temp_dir, 'test_br_fitid.csv')
        with open(csv_file, 'w', encoding='utf-8') as f:
            f.write(csv_content)

        parser = CSVParser(delimiter=';', decimal_separator=',')
        headers, rows = parser.parse_file(csv_file)

        # Generate twice to verify determinism
        fitids_runs = []
        for run in range(2):
            generator = OFXGenerator()
            for row in rows:
                generator.add_transaction(
                    date=row['data'],
                    amount=parser.normalize_amount(row['valor']),
                    description=row['descricao']
                )

            output_file = os.path.join(self.temp_dir, f'output_br_fitid_{run}.ofx')
            generator.generate(
                output_path=output_file,
                account_id='BR123',
                bank_name='Banco Teste',
                currency='BRL'
            )

            with open(output_file, 'r') as f:
                content = f.read()
                import re
                fitids = re.findall(r'<FITID>(.*?)</FITID>', content)
                fitids_runs.append(fitids)

        # Verify FITIDs are consistent across runs
        self.assertEqual(fitids_runs[0], fitids_runs[1],
                        "Brazilian format should produce deterministic FITIDs")


if __name__ == '__main__':
    unittest.main()
