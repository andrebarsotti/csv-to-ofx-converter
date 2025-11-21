"""
GUI Conversion Handler Module
==============================
Handles CSV to OFX conversion orchestration for the GUI.

This module extracts conversion-related functionality from ConverterGUI
to improve maintainability and testability.

Author: Generated for Brazilian banking compatibility
License: MIT
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import logging

from .csv_parser import CSVParser
from .ofx_generator import OFXGenerator
from .date_validator import DateValidator
from .constants import NOT_SELECTED
from . import transaction_utils

logger = logging.getLogger(__name__)


@dataclass
class ConversionConfig:
    """
    Configuration for conversion process.

    Attributes:
        csv_file_path: Path to CSV file
        csv_data: List of CSV row dictionaries
        field_mappings: Dictionary mapping OFX fields to CSV columns
        description_columns: List of columns for composite description
        description_separator: Separator for composite description
        delimiter: CSV delimiter
        decimal_separator: Decimal separator for amounts
        invert_values: Whether to invert transaction values
        account_id: OFX account ID
        bank_name: Bank name for OFX
        currency: Currency code (BRL, USD, etc.)
        initial_balance: Starting balance
        statement_start_date: Statement period start date (DD/MM/YYYY)
        statement_end_date: Statement period end date (DD/MM/YYYY)
        date_action: Date validation action ('keep', 'adjust', 'exclude')
        deleted_transactions: Set of row indices to exclude
        date_action_decisions: Dict mapping row index to date action
        enable_date_validation: Whether to validate dates
        final_balance: Final balance (None for auto-calculate)
    """
    csv_file_path: str
    csv_data: List[Dict[str, str]]
    field_mappings: Dict[str, str]
    description_columns: List[str]
    description_separator: str
    delimiter: str
    decimal_separator: str
    invert_values: bool
    account_id: str
    bank_name: str
    currency: str
    initial_balance: float
    statement_start_date: str
    statement_end_date: str
    date_action: str
    deleted_transactions: set
    date_action_decisions: Dict[int, str]
    enable_date_validation: bool
    final_balance: Optional[float] = None


class ConversionHandler:
    """
    Handles CSV to OFX conversion orchestration.

    This class manages:
    - Conversion workflow coordination
    - Date validation and adjustment
    - Transaction processing
    - OFX file generation
    """

    def __init__(self, parent_gui):
        """
        Initialize the conversion handler.

        Args:
            parent_gui: ConverterGUI instance for callbacks
        """
        self.parent = parent_gui

    def convert(
        self,
        config: ConversionConfig,
        output_file: str
    ) -> Tuple[bool, str, Dict]:
        """
        Convert CSV to OFX file.

        Args:
            config: ConversionConfig with all conversion parameters
            output_file: Path to save the OFX file

        Returns:
            Tuple of (success, message, stats) where:
            - success: True if conversion succeeded, False otherwise
            - message: Success or error message
            - stats: Dictionary with conversion statistics
        """
        try:
            parser, generator = self._create_parser_and_generator(config)

            date_validator = self._create_date_validator(config)
            if date_validator is False:
                return (
                    False,
                    "Invalid date range for validation",
                    {}
                )

            stats = self._process_csv_rows(
                config, parser, generator, date_validator
            )

            self._generate_ofx_file(config, generator, output_file)

            success_msg = self._format_success_message(
                output_file, stats, date_validator
            )

            return (True, success_msg, stats)

        except Exception as e:
            logger.error("Conversion failed: %s", e)
            return (False, f"Conversion failed:\n{e}", {})

    def _create_parser_and_generator(
        self,
        config: ConversionConfig
    ) -> Tuple[CSVParser, OFXGenerator]:
        """
        Create CSV parser and OFX generator.

        Args:
            config: ConversionConfig with parser/generator settings

        Returns:
            Tuple of (parser, generator)
        """
        parser = CSVParser(
            delimiter=config.delimiter,
            decimal_separator=config.decimal_separator
        )
        generator = OFXGenerator(invert_values=config.invert_values)

        return parser, generator

    def _create_date_validator(
        self,
        config: ConversionConfig
    ) -> Optional[DateValidator]:
        """
        Create date validator if enabled.

        Args:
            config: ConversionConfig with date validation settings

        Returns:
            DateValidator instance, None if disabled, or False on error
        """
        if not config.enable_date_validation:
            return None

        start_date_str = config.statement_start_date.strip()
        end_date_str = config.statement_end_date.strip()

        if not start_date_str or not end_date_str:
            return False

        try:
            validator = DateValidator(start_date_str, end_date_str)
            return validator
        except ValueError as e:
            logger.error("Invalid date range: %s", e)
            return False

    def _process_csv_rows(
        self,
        config: ConversionConfig,
        parser: CSVParser,
        generator: OFXGenerator,
        date_validator: Optional[DateValidator]
    ) -> Dict:
        """
        Process all CSV rows and add transactions to generator.

        Args:
            config: ConversionConfig with field mappings and settings
            parser: CSVParser instance
            generator: OFXGenerator instance
            date_validator: DateValidator instance or None

        Returns:
            Dictionary with conversion statistics
        """
        date_col = config.field_mappings['date']
        amount_col = config.field_mappings['amount']
        desc_col = config.field_mappings['description']
        type_col = config.field_mappings['type']
        id_col = config.field_mappings['id']
        use_composite = any(
            col != NOT_SELECTED for col in config.description_columns
        )

        stats = {
            'total_rows': len(config.csv_data),
            'processed': 0,
            'excluded': 0,
            'adjusted': 0,
            'kept_out_of_range': 0,
            'deleted': len(config.deleted_transactions)
        }

        for row_idx, row in enumerate(config.csv_data):
            # Skip deleted transactions
            if row_idx in config.deleted_transactions:
                stats['excluded'] += 1
                continue

            try:
                date = row[date_col]
                amount = parser.normalize_amount(row[amount_col])
                description = self._build_description(
                    config, row, desc_col, use_composite
                )

                date, date_stats = self._validate_and_adjust_date(
                    config, date, row_idx, description, date_validator
                )
                if date is None:
                    stats['excluded'] += 1
                    continue

                stats['adjusted'] += date_stats.get('adjusted', 0)
                stats['kept_out_of_range'] += date_stats.get(
                    'kept_out_of_range', 0
                )

                trans_type = self._get_transaction_type(
                    type_col, row, amount
                )
                trans_id = self._get_transaction_id(id_col, row)

                generator.add_transaction(
                    date=date,
                    amount=amount,
                    description=description,
                    transaction_type=trans_type,
                    transaction_id=trans_id
                )
                stats['processed'] += 1

            except Exception as e:
                logger.warning("Skipping row %d: %s", row_idx + 1, e)
                stats['excluded'] += 1

        return stats

    def _build_description(
        self,
        config: ConversionConfig,
        row: Dict[str, str],
        desc_col: str,
        use_composite: bool
    ) -> str:
        """
        Build transaction description from single or multiple columns.

        Args:
            config: ConversionConfig with description settings
            row: CSV row data
            desc_col: Description column name
            use_composite: Whether to use composite description

        Returns:
            Transaction description string
        """
        return transaction_utils.build_transaction_description(
            row=row,
            desc_col=desc_col,
            description_columns=config.description_columns,
            separator=config.description_separator,
            use_composite=use_composite
        )

    def _validate_and_adjust_date(
        self,
        config: ConversionConfig,
        date: str,
        row_idx: int,
        description: str,
        date_validator: Optional[DateValidator]
    ) -> Tuple[Optional[str], Dict]:
        """
        Validate date and adjust if necessary.

        Checks if user has made a decision via date_action_decisions.
        If yes, applies that decision. If no, applies default behavior:
        - Dates BEFORE start_date: automatically adjusted to start_date
        - Dates AFTER end_date: kept as-is with warning

        Args:
            config: ConversionConfig with date action decisions
            date: Transaction date string
            row_idx: Row index (0-based) in csv_data
            description: Transaction description
            date_validator: DateValidator instance or None

        Returns:
            Tuple of (date_string, stats_dict) where:
            - date_string: Adjusted date or None to exclude transaction
            - stats_dict: Dictionary with 'adjusted' and 'kept_out_of_range'
        """
        stats = {'adjusted': 0, 'kept_out_of_range': 0}

        if not date_validator:
            return date, stats

        if date_validator.is_within_range(date):
            return date, stats

        status = date_validator.get_date_status(date)

        # Check if user has made a decision for this transaction
        user_action = config.date_action_decisions.get(row_idx)

        if user_action:
            # Apply user's decision
            if user_action == 'exclude':
                return None, stats
            elif user_action == 'keep':
                stats['kept_out_of_range'] = 1
                return date, stats
            elif user_action == 'adjust':
                adjusted_date = date_validator.adjust_date_to_boundary(date)
                stats['adjusted'] = 1
                return adjusted_date, stats
        else:
            # Apply automatic default actions based on date status
            if status == 'before':
                # Default: adjust dates before start to start_date
                adjusted_date = date_validator.adjust_date_to_boundary(date)
                stats['adjusted'] = 1
                return adjusted_date, stats
            elif status == 'after':
                # Default: keep dates after end with warning
                stats['kept_out_of_range'] = 1
                return date, stats

        return date, stats

    def _get_transaction_type(
        self,
        type_col: str,
        row: Dict[str, str],
        amount: float
    ) -> Optional[str]:
        """
        Get transaction type from mapping or infer from amount.

        Args:
            type_col: Type column name
            row: CSV row data
            amount: Transaction amount

        Returns:
            Transaction type ('DEBIT', 'CREDIT') or None
        """
        return transaction_utils.determine_transaction_type(
            type_col, row, amount
        )

    def _get_transaction_id(
        self,
        id_col: str,
        row: Dict[str, str]
    ) -> Optional[str]:
        """
        Get transaction ID from mapping if available.

        Args:
            id_col: ID column name
            row: CSV row data

        Returns:
            Transaction ID or None
        """
        return transaction_utils.extract_transaction_id(id_col, row)

    def _generate_ofx_file(
        self,
        config: ConversionConfig,
        generator: OFXGenerator,
        output_file: str
    ):
        """
        Generate the OFX file using the generator.

        Args:
            config: ConversionConfig with OFX settings
            generator: OFXGenerator with transactions
            output_file: Path to save the OFX file
        """
        # Validate initial balance (already parsed in config)
        initial_balance = config.initial_balance

        # Use final balance from config (None for auto-calculate)
        final_balance = config.final_balance

        generator.generate(
            output_path=output_file,
            account_id=config.account_id,
            bank_name=config.bank_name,
            currency=config.currency,
            initial_balance=initial_balance,
            final_balance=final_balance
        )

    def _format_success_message(
        self,
        output_file: str,
        stats: Dict,
        date_validator: Optional[DateValidator]
    ) -> str:
        """
        Format success message with statistics.

        Args:
            output_file: Path to generated OFX file
            stats: Conversion statistics dictionary
            date_validator: DateValidator instance or None

        Returns:
            Formatted success message string
        """
        stats_lines = [
            f"Total rows in CSV: {stats['total_rows']}",
            f"Transactions processed: {stats['processed']}",
            f"Transactions excluded: {stats['excluded']}"
        ]

        if date_validator:
            if stats.get('adjusted', 0) > 0:
                stats_lines.append(
                    f"Dates adjusted to boundaries: {stats['adjusted']}"
                )
            if stats.get('kept_out_of_range', 0) > 0:
                stats_lines.append(
                    f"Out-of-range dates kept: {stats['kept_out_of_range']}"
                )

        stats_text = "\n".join(stats_lines)

        message = (
            "Conversion completed successfully!\n"
            f"\n"
            f"Output file: {output_file}\n"
            f"\n"
            f"{stats_text}"
        )

        return message

    def get_date_validation_dialog_data(
        self,
        row_idx: int,
        date_str: str,
        status: str,
        validator: DateValidator,
        description: str
    ) -> Dict:
        """
        Get data for date validation dialog display.

        Args:
            row_idx: Row index in CSV (0-based)
            date_str: Original transaction date
            status: 'before' or 'after' the valid range
            validator: DateValidator instance
            description: Transaction description

        Returns:
            Dictionary with dialog data:
            - row_idx: Row index (1-based for display)
            - date: Original date
            - description: Transaction description (truncated)
            - start_date: Validation start date
            - end_date: Validation end date
            - status: Date status
            - status_text: Human-readable status text
            - boundary: Boundary name ('start date' or 'end date')
        """
        start_str = validator.start_date.strftime('%Y-%m-%d')
        end_str = validator.end_date.strftime('%Y-%m-%d')

        if status == 'before':
            status_text = "This transaction occurs BEFORE the start date"
            boundary = "start date"
        else:
            status_text = "This transaction occurs AFTER the end date"
            boundary = "end date"

        desc_truncated = description[:50]
        if len(description) > 50:
            desc_truncated += '...'

        return {
            'row_idx': row_idx + 1,  # 1-based for display
            'date': date_str,
            'description': desc_truncated,
            'start_date': start_str,
            'end_date': end_str,
            'status': status,
            'status_text': status_text,
            'boundary': boundary
        }
