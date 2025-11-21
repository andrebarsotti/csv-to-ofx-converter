"""
Tests for GUI Conversion Handler Module
=========================================
Unit tests for the ConversionHandler class that handles CSV to OFX conversion
orchestration.

These tests verify conversion workflow, date validation, transaction processing,
and error handling without requiring a GUI display server.
"""

import unittest
import tempfile
import os
from src.gui_conversion_handler import ConversionHandler, ConversionConfig
from src.constants import NOT_MAPPED, NOT_SELECTED


class MockParentGUI:
    """Mock ConverterGUI for testing ConversionHandler."""

    def __init__(self):
        """Initialize mock parent GUI."""
        self.log_messages = []

    def _log_to_widget(self, message):
        """Mock logging method."""
        self.log_messages.append(message)


class TestConversionConfig(unittest.TestCase):
    """Test ConversionConfig dataclass."""

    def test_conversion_config_initialization_all_fields(self):
        """Test ConversionConfig initialization with all required fields."""
        config = ConversionConfig(
            csv_file_path='/tmp/test.csv',
            csv_data=[{'Date': '01/01/2025', 'Amount': '100.00'}],
            field_mappings={'date': 'Date', 'amount': 'Amount',
                            'description': 'Desc', 'type': NOT_MAPPED,
                            'id': NOT_MAPPED},
            description_columns=[NOT_SELECTED, NOT_SELECTED, NOT_SELECTED,
                                 NOT_SELECTED],
            description_separator=' ',
            delimiter=',',
            decimal_separator='.',
            invert_values=False,
            account_id='1234',
            bank_name='Test Bank',
            currency='BRL',
            initial_balance=1000.0,
            statement_start_date='01/01/2025',
            statement_end_date='31/01/2025',
            date_action='keep',
            deleted_transactions=set(),
            date_action_decisions={},
            enable_date_validation=False,
            final_balance=None
        )

        self.assertEqual(config.csv_file_path, '/tmp/test.csv')
        self.assertEqual(len(config.csv_data), 1)
        self.assertEqual(config.account_id, '1234')
        self.assertEqual(config.bank_name, 'Test Bank')
        self.assertEqual(config.currency, 'BRL')
        self.assertEqual(config.initial_balance, 1000.0)
        self.assertFalse(config.invert_values)
        self.assertFalse(config.enable_date_validation)
        self.assertIsNone(config.final_balance)

    def test_conversion_config_with_final_balance(self):
        """Test ConversionConfig initialization with final balance specified."""
        config = ConversionConfig(
            csv_file_path='/tmp/test.csv',
            csv_data=[],
            field_mappings={'date': 'Date', 'amount': 'Amount',
                            'description': 'Desc', 'type': NOT_MAPPED,
                            'id': NOT_MAPPED},
            description_columns=[],
            description_separator=' ',
            delimiter=',',
            decimal_separator='.',
            invert_values=False,
            account_id='1234',
            bank_name='Test Bank',
            currency='USD',
            initial_balance=1000.0,
            statement_start_date='01/01/2025',
            statement_end_date='31/01/2025',
            date_action='keep',
            deleted_transactions=set(),
            date_action_decisions={},
            enable_date_validation=False,
            final_balance=1500.0
        )

        self.assertEqual(config.final_balance, 1500.0)


class TestConversionHandler(unittest.TestCase):
    """Test ConversionHandler class."""

    def setUp(self):
        """Set up test fixtures."""
        self.parent = MockParentGUI()
        self.handler = ConversionHandler(self.parent)
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up temporary files."""
        for filename in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, filename))
        os.rmdir(self.temp_dir)

    def test_conversion_handler_initialization(self):
        """Test ConversionHandler initialization with parent GUI."""
        self.assertIsNotNone(self.handler)
        self.assertEqual(self.handler.parent, self.parent)

    def test_convert_empty_csv_data(self):
        """Test conversion with empty CSV data."""
        config = ConversionConfig(
            csv_file_path='/tmp/test.csv',
            csv_data=[],
            field_mappings={'date': 'Date', 'amount': 'Amount',
                            'description': 'Desc', 'type': NOT_MAPPED,
                            'id': NOT_MAPPED},
            description_columns=[NOT_SELECTED, NOT_SELECTED, NOT_SELECTED,
                                 NOT_SELECTED],
            description_separator=' ',
            delimiter=',',
            decimal_separator='.',
            invert_values=False,
            account_id='1234',
            bank_name='Test Bank',
            currency='BRL',
            initial_balance=1000.0,
            statement_start_date='01/01/2025',
            statement_end_date='31/01/2025',
            date_action='keep',
            deleted_transactions=set(),
            date_action_decisions={},
            enable_date_validation=False,
            final_balance=None
        )

        output_file = os.path.join(self.temp_dir, 'output.ofx')
        success, message, stats = self.handler.convert(config, output_file)

        # OFXGenerator raises ValueError when no transactions
        self.assertFalse(success)
        self.assertIn('No transactions to export', message)

    def test_convert_standard_format_transactions(self):
        """Test processing rows with standard format (comma delimiter, dot decimal)."""
        csv_data = [
            {'Date': '2025-01-01', 'Amount': '100.00', 'Desc': 'Credit'},
            {'Date': '2025-01-02', 'Amount': '-50.00', 'Desc': 'Debit'}
        ]

        config = ConversionConfig(
            csv_file_path='/tmp/test.csv',
            csv_data=csv_data,
            field_mappings={'date': 'Date', 'amount': 'Amount',
                            'description': 'Desc', 'type': NOT_MAPPED,
                            'id': NOT_MAPPED},
            description_columns=[NOT_SELECTED, NOT_SELECTED, NOT_SELECTED,
                                 NOT_SELECTED],
            description_separator=' ',
            delimiter=',',
            decimal_separator='.',
            invert_values=False,
            account_id='1234',
            bank_name='Test Bank',
            currency='USD',
            initial_balance=0.0,
            statement_start_date='01/01/2025',
            statement_end_date='31/01/2025',
            date_action='keep',
            deleted_transactions=set(),
            date_action_decisions={},
            enable_date_validation=False,
            final_balance=None
        )

        output_file = os.path.join(self.temp_dir, 'output.ofx')
        success, message, stats = self.handler.convert(config, output_file)

        self.assertTrue(success)
        self.assertEqual(stats['total_rows'], 2)
        self.assertEqual(stats['processed'], 2)
        self.assertEqual(stats['excluded'], 0)
        self.assertTrue(os.path.exists(output_file))

    def test_convert_brazilian_format_transactions(self):
        """Test processing rows with Brazilian format (semicolon delimiter, comma decimal)."""
        csv_data = [
            {'Data': '01/01/2025', 'Valor': '100,00', 'Descricao': 'Credito'},
            {'Data': '02/01/2025', 'Valor': '-50,50', 'Descricao': 'Debito'}
        ]

        config = ConversionConfig(
            csv_file_path='/tmp/test.csv',
            csv_data=csv_data,
            field_mappings={'date': 'Data', 'amount': 'Valor',
                            'description': 'Descricao', 'type': NOT_MAPPED,
                            'id': NOT_MAPPED},
            description_columns=[NOT_SELECTED, NOT_SELECTED, NOT_SELECTED,
                                 NOT_SELECTED],
            description_separator=' ',
            delimiter=';',
            decimal_separator=',',
            invert_values=False,
            account_id='1234',
            bank_name='Banco do Brasil',
            currency='BRL',
            initial_balance=1000.0,
            statement_start_date='01/01/2025',
            statement_end_date='31/01/2025',
            date_action='keep',
            deleted_transactions=set(),
            date_action_decisions={},
            enable_date_validation=False,
            final_balance=None
        )

        output_file = os.path.join(self.temp_dir, 'output.ofx')
        success, message, stats = self.handler.convert(config, output_file)

        self.assertTrue(success)
        self.assertEqual(stats['total_rows'], 2)
        self.assertEqual(stats['processed'], 2)
        self.assertEqual(stats['excluded'], 0)

    def test_convert_with_deleted_transactions(self):
        """Test processing rows with deleted transactions (should skip them)."""
        csv_data = [
            {'Date': '2025-01-01', 'Amount': '100.00', 'Desc': 'Keep'},
            {'Date': '2025-01-02', 'Amount': '-50.00', 'Desc': 'Delete'},
            {'Date': '2025-01-03', 'Amount': '25.00', 'Desc': 'Keep'}
        ]

        config = ConversionConfig(
            csv_file_path='/tmp/test.csv',
            csv_data=csv_data,
            field_mappings={'date': 'Date', 'amount': 'Amount',
                            'description': 'Desc', 'type': NOT_MAPPED,
                            'id': NOT_MAPPED},
            description_columns=[NOT_SELECTED, NOT_SELECTED, NOT_SELECTED,
                                 NOT_SELECTED],
            description_separator=' ',
            delimiter=',',
            decimal_separator='.',
            invert_values=False,
            account_id='1234',
            bank_name='Test Bank',
            currency='USD',
            initial_balance=0.0,
            statement_start_date='01/01/2025',
            statement_end_date='31/01/2025',
            date_action='keep',
            deleted_transactions={1},  # Delete second transaction
            date_action_decisions={},
            enable_date_validation=False,
            final_balance=None
        )

        output_file = os.path.join(self.temp_dir, 'output.ofx')
        success, message, stats = self.handler.convert(config, output_file)

        self.assertTrue(success)
        self.assertEqual(stats['total_rows'], 3)
        self.assertEqual(stats['processed'], 2)
        self.assertEqual(stats['excluded'], 1)
        self.assertEqual(stats['deleted'], 1)

    def test_convert_with_value_inversion(self):
        """Test processing rows with value inversion enabled."""
        csv_data = [
            {'Date': '2025-01-01', 'Amount': '100.00', 'Desc': 'Credit'},
            {'Date': '2025-01-02', 'Amount': '-50.00', 'Desc': 'Debit'}
        ]

        config = ConversionConfig(
            csv_file_path='/tmp/test.csv',
            csv_data=csv_data,
            field_mappings={'date': 'Date', 'amount': 'Amount',
                            'description': 'Desc', 'type': NOT_MAPPED,
                            'id': NOT_MAPPED},
            description_columns=[NOT_SELECTED, NOT_SELECTED, NOT_SELECTED,
                                 NOT_SELECTED],
            description_separator=' ',
            delimiter=',',
            decimal_separator='.',
            invert_values=True,  # Invert values
            account_id='1234',
            bank_name='Test Bank',
            currency='USD',
            initial_balance=0.0,
            statement_start_date='01/01/2025',
            statement_end_date='31/01/2025',
            date_action='keep',
            deleted_transactions=set(),
            date_action_decisions={},
            enable_date_validation=False,
            final_balance=None
        )

        output_file = os.path.join(self.temp_dir, 'output.ofx')
        success, message, stats = self.handler.convert(config, output_file)

        self.assertTrue(success)
        self.assertEqual(stats['total_rows'], 2)
        self.assertEqual(stats['processed'], 2)

    def test_convert_with_composite_description_space_separator(self):
        """Test processing rows with composite descriptions using space separator."""
        csv_data = [
            {'Date': '2025-01-01', 'Amount': '100.00', 'Memo': 'Purchase',
             'Vendor': 'Store', 'Category': 'Food'}
        ]

        config = ConversionConfig(
            csv_file_path='/tmp/test.csv',
            csv_data=csv_data,
            field_mappings={'date': 'Date', 'amount': 'Amount',
                            'description': 'Memo', 'type': NOT_MAPPED,
                            'id': NOT_MAPPED},
            description_columns=['Memo', 'Vendor', 'Category', NOT_SELECTED],
            description_separator=' ',
            delimiter=',',
            decimal_separator='.',
            invert_values=False,
            account_id='1234',
            bank_name='Test Bank',
            currency='USD',
            initial_balance=0.0,
            statement_start_date='01/01/2025',
            statement_end_date='31/01/2025',
            date_action='keep',
            deleted_transactions=set(),
            date_action_decisions={},
            enable_date_validation=False,
            final_balance=None
        )

        output_file = os.path.join(self.temp_dir, 'output.ofx')
        success, message, stats = self.handler.convert(config, output_file)

        self.assertTrue(success)
        self.assertEqual(stats['processed'], 1)

    def test_convert_with_composite_description_dash_separator(self):
        """Test processing rows with composite descriptions using dash separator."""
        csv_data = [
            {'Date': '2025-01-01', 'Amount': '100.00', 'Col1': 'Part1',
             'Col2': 'Part2'}
        ]

        config = ConversionConfig(
            csv_file_path='/tmp/test.csv',
            csv_data=csv_data,
            field_mappings={'date': 'Date', 'amount': 'Amount',
                            'description': 'Col1', 'type': NOT_MAPPED,
                            'id': NOT_MAPPED},
            description_columns=['Col1', 'Col2', NOT_SELECTED, NOT_SELECTED],
            description_separator=' - ',
            delimiter=',',
            decimal_separator='.',
            invert_values=False,
            account_id='1234',
            bank_name='Test Bank',
            currency='USD',
            initial_balance=0.0,
            statement_start_date='01/01/2025',
            statement_end_date='31/01/2025',
            date_action='keep',
            deleted_transactions=set(),
            date_action_decisions={},
            enable_date_validation=False,
            final_balance=None
        )

        output_file = os.path.join(self.temp_dir, 'output.ofx')
        success, message, stats = self.handler.convert(config, output_file)

        self.assertTrue(success)
        self.assertEqual(stats['processed'], 1)

    def test_date_validation_with_keep_action(self):
        """Test date validation with 'keep' action (preserve original dates)."""
        csv_data = [
            {'Date': '2024-12-15', 'Amount': '100.00', 'Desc': 'Before range'},
            {'Date': '2025-02-15', 'Amount': '50.00', 'Desc': 'After range'}
        ]

        config = ConversionConfig(
            csv_file_path='/tmp/test.csv',
            csv_data=csv_data,
            field_mappings={'date': 'Date', 'amount': 'Amount',
                            'description': 'Desc', 'type': NOT_MAPPED,
                            'id': NOT_MAPPED},
            description_columns=[NOT_SELECTED, NOT_SELECTED, NOT_SELECTED,
                                 NOT_SELECTED],
            description_separator=' ',
            delimiter=',',
            decimal_separator='.',
            invert_values=False,
            account_id='1234',
            bank_name='Test Bank',
            currency='USD',
            initial_balance=0.0,
            statement_start_date='01/01/2025',
            statement_end_date='31/01/2025',
            date_action='keep',
            deleted_transactions=set(),
            date_action_decisions={0: 'keep', 1: 'keep'},
            enable_date_validation=True,
            final_balance=None
        )

        output_file = os.path.join(self.temp_dir, 'output.ofx')
        success, message, stats = self.handler.convert(config, output_file)

        self.assertTrue(success)
        self.assertEqual(stats['processed'], 2)
        self.assertEqual(stats['adjusted'], 0)
        self.assertEqual(stats['kept_out_of_range'], 2)

    def test_date_validation_with_adjust_action(self):
        """Test date validation with 'adjust' action (move to boundaries)."""
        csv_data = [
            {'Date': '2024-12-15', 'Amount': '100.00', 'Desc': 'Before range'},
            {'Date': '2025-02-15', 'Amount': '50.00', 'Desc': 'After range'}
        ]

        config = ConversionConfig(
            csv_file_path='/tmp/test.csv',
            csv_data=csv_data,
            field_mappings={'date': 'Date', 'amount': 'Amount',
                            'description': 'Desc', 'type': NOT_MAPPED,
                            'id': NOT_MAPPED},
            description_columns=[NOT_SELECTED, NOT_SELECTED, NOT_SELECTED,
                                 NOT_SELECTED],
            description_separator=' ',
            delimiter=',',
            decimal_separator='.',
            invert_values=False,
            account_id='1234',
            bank_name='Test Bank',
            currency='USD',
            initial_balance=0.0,
            statement_start_date='01/01/2025',
            statement_end_date='31/01/2025',
            date_action='adjust',
            deleted_transactions=set(),
            date_action_decisions={0: 'adjust', 1: 'adjust'},
            enable_date_validation=True,
            final_balance=None
        )

        output_file = os.path.join(self.temp_dir, 'output.ofx')
        success, message, stats = self.handler.convert(config, output_file)

        self.assertTrue(success)
        self.assertEqual(stats['processed'], 2)
        self.assertEqual(stats['adjusted'], 2)
        self.assertEqual(stats['kept_out_of_range'], 0)

    def test_date_validation_with_exclude_action(self):
        """Test date validation with 'exclude' action (skip invalid dates)."""
        csv_data = [
            {'Date': '2024-12-15', 'Amount': '100.00', 'Desc': 'Before range'},
            {'Date': '2025-01-15', 'Amount': '75.00', 'Desc': 'Within range'},
            {'Date': '2025-02-15', 'Amount': '50.00', 'Desc': 'After range'}
        ]

        config = ConversionConfig(
            csv_file_path='/tmp/test.csv',
            csv_data=csv_data,
            field_mappings={'date': 'Date', 'amount': 'Amount',
                            'description': 'Desc', 'type': NOT_MAPPED,
                            'id': NOT_MAPPED},
            description_columns=[NOT_SELECTED, NOT_SELECTED, NOT_SELECTED,
                                 NOT_SELECTED],
            description_separator=' ',
            delimiter=',',
            decimal_separator='.',
            invert_values=False,
            account_id='1234',
            bank_name='Test Bank',
            currency='USD',
            initial_balance=0.0,
            statement_start_date='01/01/2025',
            statement_end_date='31/01/2025',
            date_action='exclude',
            deleted_transactions=set(),
            date_action_decisions={0: 'exclude', 2: 'exclude'},
            enable_date_validation=True,
            final_balance=None
        )

        output_file = os.path.join(self.temp_dir, 'output.ofx')
        success, message, stats = self.handler.convert(config, output_file)

        self.assertTrue(success)
        self.assertEqual(stats['processed'], 1)  # Only the valid date
        self.assertEqual(stats['excluded'], 2)  # Two excluded

    def test_date_validation_dates_within_range(self):
        """Test dates within range (no validation needed)."""
        csv_data = [
            {'Date': '2025-01-10', 'Amount': '100.00', 'Desc': 'Within range'},
            {'Date': '2025-01-20', 'Amount': '50.00', 'Desc': 'Within range'}
        ]

        config = ConversionConfig(
            csv_file_path='/tmp/test.csv',
            csv_data=csv_data,
            field_mappings={'date': 'Date', 'amount': 'Amount',
                            'description': 'Desc', 'type': NOT_MAPPED,
                            'id': NOT_MAPPED},
            description_columns=[NOT_SELECTED, NOT_SELECTED, NOT_SELECTED,
                                 NOT_SELECTED],
            description_separator=' ',
            delimiter=',',
            decimal_separator='.',
            invert_values=False,
            account_id='1234',
            bank_name='Test Bank',
            currency='USD',
            initial_balance=0.0,
            statement_start_date='01/01/2025',
            statement_end_date='31/01/2025',
            date_action='keep',
            deleted_transactions=set(),
            date_action_decisions={},
            enable_date_validation=True,
            final_balance=None
        )

        output_file = os.path.join(self.temp_dir, 'output.ofx')
        success, message, stats = self.handler.convert(config, output_file)

        self.assertTrue(success)
        self.assertEqual(stats['processed'], 2)
        self.assertEqual(stats['adjusted'], 0)
        self.assertEqual(stats['kept_out_of_range'], 0)

    def test_date_validation_disabled(self):
        """Test date validator creation when validation is disabled."""
        csv_data = [
            {'Date': '2024-12-15', 'Amount': '100.00', 'Desc': 'Before range'},
        ]

        config = ConversionConfig(
            csv_file_path='/tmp/test.csv',
            csv_data=csv_data,
            field_mappings={'date': 'Date', 'amount': 'Amount',
                            'description': 'Desc', 'type': NOT_MAPPED,
                            'id': NOT_MAPPED},
            description_columns=[NOT_SELECTED, NOT_SELECTED, NOT_SELECTED,
                                 NOT_SELECTED],
            description_separator=' ',
            delimiter=',',
            decimal_separator='.',
            invert_values=False,
            account_id='1234',
            bank_name='Test Bank',
            currency='USD',
            initial_balance=0.0,
            statement_start_date='01/01/2025',
            statement_end_date='31/01/2025',
            date_action='keep',
            deleted_transactions=set(),
            date_action_decisions={},
            enable_date_validation=False,  # Disabled
            final_balance=None
        )

        output_file = os.path.join(self.temp_dir, 'output.ofx')
        success, message, stats = self.handler.convert(config, output_file)

        self.assertTrue(success)
        self.assertEqual(stats['processed'], 1)
        # No date adjustment stats since validation is disabled
        self.assertEqual(stats.get('adjusted', 0), 0)

    def test_description_building_single_column(self):
        """Test building description from single column."""
        csv_data = [
            {'Date': '2025-01-01', 'Amount': '100.00', 'Desc': 'Simple description'}
        ]

        config = ConversionConfig(
            csv_file_path='/tmp/test.csv',
            csv_data=csv_data,
            field_mappings={'date': 'Date', 'amount': 'Amount',
                            'description': 'Desc', 'type': NOT_MAPPED,
                            'id': NOT_MAPPED},
            description_columns=[NOT_SELECTED, NOT_SELECTED, NOT_SELECTED,
                                 NOT_SELECTED],
            description_separator=' ',
            delimiter=',',
            decimal_separator='.',
            invert_values=False,
            account_id='1234',
            bank_name='Test Bank',
            currency='USD',
            initial_balance=0.0,
            statement_start_date='01/01/2025',
            statement_end_date='31/01/2025',
            date_action='keep',
            deleted_transactions=set(),
            date_action_decisions={},
            enable_date_validation=False,
            final_balance=None
        )

        output_file = os.path.join(self.temp_dir, 'output.ofx')
        success, message, stats = self.handler.convert(config, output_file)

        self.assertTrue(success)
        self.assertEqual(stats['processed'], 1)

    def test_description_building_empty_columns(self):
        """Test building description with empty/missing columns."""
        csv_data = [
            {'Date': '2025-01-01', 'Amount': '100.00', 'Desc': ''}
        ]

        config = ConversionConfig(
            csv_file_path='/tmp/test.csv',
            csv_data=csv_data,
            field_mappings={'date': 'Date', 'amount': 'Amount',
                            'description': 'Desc', 'type': NOT_MAPPED,
                            'id': NOT_MAPPED},
            description_columns=['Desc', NOT_SELECTED, NOT_SELECTED,
                                 NOT_SELECTED],
            description_separator=' ',
            delimiter=',',
            decimal_separator='.',
            invert_values=False,
            account_id='1234',
            bank_name='Test Bank',
            currency='USD',
            initial_balance=0.0,
            statement_start_date='01/01/2025',
            statement_end_date='31/01/2025',
            date_action='keep',
            deleted_transactions=set(),
            date_action_decisions={},
            enable_date_validation=False,
            final_balance=None
        )

        output_file = os.path.join(self.temp_dir, 'output.ofx')
        success, message, stats = self.handler.convert(config, output_file)

        self.assertTrue(success)
        self.assertEqual(stats['processed'], 1)

    def test_transaction_type_determination_from_amount_sign(self):
        """Test transaction type determination from amount sign."""
        csv_data = [
            {'Date': '2025-01-01', 'Amount': '100.00', 'Desc': 'Credit'},
            {'Date': '2025-01-02', 'Amount': '-50.00', 'Desc': 'Debit'}
        ]

        config = ConversionConfig(
            csv_file_path='/tmp/test.csv',
            csv_data=csv_data,
            field_mappings={'date': 'Date', 'amount': 'Amount',
                            'description': 'Desc', 'type': NOT_MAPPED,
                            'id': NOT_MAPPED},
            description_columns=[NOT_SELECTED, NOT_SELECTED, NOT_SELECTED,
                                 NOT_SELECTED],
            description_separator=' ',
            delimiter=',',
            decimal_separator='.',
            invert_values=False,
            account_id='1234',
            bank_name='Test Bank',
            currency='USD',
            initial_balance=0.0,
            statement_start_date='01/01/2025',
            statement_end_date='31/01/2025',
            date_action='keep',
            deleted_transactions=set(),
            date_action_decisions={},
            enable_date_validation=False,
            final_balance=None
        )

        output_file = os.path.join(self.temp_dir, 'output.ofx')
        success, message, stats = self.handler.convert(config, output_file)

        self.assertTrue(success)
        self.assertEqual(stats['processed'], 2)

    def test_transaction_id_extraction_from_mapped_column(self):
        """Test transaction ID extraction from mapped column."""
        csv_data = [
            {'Date': '2025-01-01', 'Amount': '100.00', 'Desc': 'Test',
             'TxnID': 'TXN123'}
        ]

        config = ConversionConfig(
            csv_file_path='/tmp/test.csv',
            csv_data=csv_data,
            field_mappings={'date': 'Date', 'amount': 'Amount',
                            'description': 'Desc', 'type': NOT_MAPPED,
                            'id': 'TxnID'},
            description_columns=[NOT_SELECTED, NOT_SELECTED, NOT_SELECTED,
                                 NOT_SELECTED],
            description_separator=' ',
            delimiter=',',
            decimal_separator='.',
            invert_values=False,
            account_id='1234',
            bank_name='Test Bank',
            currency='USD',
            initial_balance=0.0,
            statement_start_date='01/01/2025',
            statement_end_date='31/01/2025',
            date_action='keep',
            deleted_transactions=set(),
            date_action_decisions={},
            enable_date_validation=False,
            final_balance=None
        )

        output_file = os.path.join(self.temp_dir, 'output.ofx')
        success, message, stats = self.handler.convert(config, output_file)

        self.assertTrue(success)
        self.assertEqual(stats['processed'], 1)

    def test_error_handling_malformed_csv_data(self):
        """Test handling of malformed CSV data."""
        csv_data = [
            {'Date': '2025-01-01', 'Amount': 'invalid', 'Desc': 'Bad amount'}
        ]

        config = ConversionConfig(
            csv_file_path='/tmp/test.csv',
            csv_data=csv_data,
            field_mappings={'date': 'Date', 'amount': 'Amount',
                            'description': 'Desc', 'type': NOT_MAPPED,
                            'id': NOT_MAPPED},
            description_columns=[NOT_SELECTED, NOT_SELECTED, NOT_SELECTED,
                                 NOT_SELECTED],
            description_separator=' ',
            delimiter=',',
            decimal_separator='.',
            invert_values=False,
            account_id='1234',
            bank_name='Test Bank',
            currency='USD',
            initial_balance=0.0,
            statement_start_date='01/01/2025',
            statement_end_date='31/01/2025',
            date_action='keep',
            deleted_transactions=set(),
            date_action_decisions={},
            enable_date_validation=False,
            final_balance=None
        )

        output_file = os.path.join(self.temp_dir, 'output.ofx')
        success, message, stats = self.handler.convert(config, output_file)

        # Malformed data gets skipped, leading to no transactions
        self.assertFalse(success)
        self.assertIn('No transactions to export', message)

    def test_error_handling_invalid_date_range(self):
        """Test handling of invalid date range for validation."""
        csv_data = [
            {'Date': '2025-01-01', 'Amount': '100.00', 'Desc': 'Test'}
        ]

        config = ConversionConfig(
            csv_file_path='/tmp/test.csv',
            csv_data=csv_data,
            field_mappings={'date': 'Date', 'amount': 'Amount',
                            'description': 'Desc', 'type': NOT_MAPPED,
                            'id': NOT_MAPPED},
            description_columns=[NOT_SELECTED, NOT_SELECTED, NOT_SELECTED,
                                 NOT_SELECTED],
            description_separator=' ',
            delimiter=',',
            decimal_separator='.',
            invert_values=False,
            account_id='1234',
            bank_name='Test Bank',
            currency='USD',
            initial_balance=0.0,
            statement_start_date='invalid',
            statement_end_date='invalid',
            date_action='keep',
            deleted_transactions=set(),
            date_action_decisions={},
            enable_date_validation=True,
            final_balance=None
        )

        output_file = os.path.join(self.temp_dir, 'output.ofx')
        success, message, stats = self.handler.convert(config, output_file)

        self.assertFalse(success)
        self.assertIn('Invalid date range', message)

    def test_get_date_validation_dialog_data_before_status(self):
        """Test getting date validation dialog data for 'before' status."""
        from src.date_validator import DateValidator

        validator = DateValidator('01/01/2025', '31/01/2025')
        data = self.handler.get_date_validation_dialog_data(
            row_idx=5,
            date_str='2024-12-15',
            status='before',
            validator=validator,
            description='Test transaction description'
        )

        self.assertEqual(data['row_idx'], 6)  # 1-based
        self.assertEqual(data['date'], '2024-12-15')
        self.assertEqual(data['status'], 'before')
        self.assertIn('BEFORE', data['status_text'])
        self.assertEqual(data['boundary'], 'start date')

    def test_get_date_validation_dialog_data_after_status(self):
        """Test getting date validation dialog data for 'after' status."""
        from src.date_validator import DateValidator

        validator = DateValidator('01/01/2025', '31/01/2025')
        data = self.handler.get_date_validation_dialog_data(
            row_idx=10,
            date_str='2025-02-15',
            status='after',
            validator=validator,
            description='Long description that should be truncated' * 5
        )

        self.assertEqual(data['row_idx'], 11)  # 1-based
        self.assertEqual(data['date'], '2025-02-15')
        self.assertEqual(data['status'], 'after')
        self.assertIn('AFTER', data['status_text'])
        self.assertEqual(data['boundary'], 'end date')
        # Check description truncation
        self.assertLessEqual(len(data['description']), 53)  # 50 + '...'


if __name__ == '__main__':
    unittest.main()
