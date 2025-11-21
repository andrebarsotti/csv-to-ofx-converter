"""
GUI Balance Manager Module
===========================
Handles balance preview and transaction management for the GUI.

This module extracts balance-related functionality from ConverterGUI
to improve maintainability and testability.

Author: Generated for Brazilian banking compatibility
License: MIT
"""

from typing import Dict, List, Optional, Tuple
from .csv_parser import CSVParser
from .date_validator import DateValidator
from .constants import NOT_SELECTED, NOT_MAPPED
from . import transaction_utils
from . import gui_utils


class BalancePreviewData:
    """
    Data class representing balance preview information.

    Attributes:
        initial_balance: Starting balance
        total_credits: Sum of all credit transactions
        total_debits: Sum of all debit transactions (absolute values)
        calculated_final_balance: Computed ending balance
        transaction_count: Number of transactions
        transactions: List of transaction dictionaries
    """

    def __init__(
        self,
        initial_balance: float,
        total_credits: float,
        total_debits: float,
        calculated_final_balance: float,
        transaction_count: int,
        transactions: List[Dict]
    ):
        """Initialize balance preview data."""
        self.initial_balance = initial_balance
        self.total_credits = total_credits
        self.total_debits = total_debits
        self.calculated_final_balance = calculated_final_balance
        self.transaction_count = transaction_count
        self.transactions = transactions

    def to_dict(self) -> Dict:
        """Convert to dictionary for compatibility with existing code."""
        return {
            'initial_balance': self.initial_balance,
            'total_credits': self.total_credits,
            'total_debits': self.total_debits,
            'calculated_final_balance': self.calculated_final_balance,
            'transaction_count': self.transaction_count,
            'transactions': self.transactions
        }


class BalanceManager:
    """
    Manages balance calculations and transaction preview for the GUI.

    This class handles:
    - Calculating balance summaries from CSV data
    - Processing individual transactions for preview
    - Managing transaction deletion and date action decisions
    - Date validation for transactions
    """

    def __init__(self, parent_gui):
        """
        Initialize the balance manager.

        Args:
            parent_gui: ConverterGUI instance for callbacks and data access
        """
        self.parent = parent_gui

    def calculate_balance_preview(
        self,
        initial_balance_str: str,
        csv_data: List[Dict[str, str]],
        field_mappings: Dict[str, str],
        description_columns: List[str],
        description_separator: str,
        delimiter: str,
        decimal_separator: str,
        invert_values: bool,
        deleted_transactions: set,
        enable_date_validation: bool = False,
        start_date_str: str = '',
        end_date_str: str = ''
    ) -> BalancePreviewData:
        """
        Calculate balance information for preview.

        Args:
            initial_balance_str: Initial balance as string
            csv_data: List of CSV row dictionaries
            field_mappings: Dictionary mapping OFX fields to CSV columns
            description_columns: List of columns for composite description
            description_separator: Separator for composite description
            delimiter: CSV delimiter
            decimal_separator: Decimal separator for amounts
            invert_values: Whether to invert transaction values
            deleted_transactions: Set of row indices to exclude
            enable_date_validation: Whether to validate dates
            start_date_str: Start date for validation (DD/MM/YYYY)
            end_date_str: End date for validation (DD/MM/YYYY)

        Returns:
            BalancePreviewData object with calculated information
        """
        # Parse initial balance using utility function
        initial_balance = transaction_utils.parse_balance_value(
            initial_balance_str, default=0.0)

        # Get field mappings
        date_col = field_mappings.get('date', NOT_MAPPED)
        amount_col = field_mappings.get('amount', NOT_MAPPED)
        desc_col = field_mappings.get('description', NOT_MAPPED)
        type_col = field_mappings.get('type', NOT_MAPPED)
        use_composite = any(col != NOT_SELECTED for col in description_columns)

        # Create parser
        parser = CSVParser(
            delimiter=delimiter,
            decimal_separator=decimal_separator
        )

        # Create date validator if needed
        date_validator = None
        if enable_date_validation and start_date_str and end_date_str:
            try:
                date_validator = DateValidator(start_date_str, end_date_str)
            except Exception:
                # If validator creation fails, continue without validation
                date_validator = None

        transactions = []
        total_credits = 0.0
        total_debits = 0.0

        # Process each row
        for row_idx, row in enumerate(csv_data):
            # Skip deleted transactions
            if row_idx in deleted_transactions:
                continue

            transaction = self._process_preview_row(
                row=row,
                parser=parser,
                date_col=date_col,
                amount_col=amount_col,
                desc_col=desc_col,
                type_col=type_col,
                use_composite=use_composite,
                description_columns=description_columns,
                description_separator=description_separator,
                invert_values=invert_values,
                date_validator=date_validator
            )

            if transaction:
                # Add original row index to transaction
                transaction['row_idx'] = row_idx
                transactions.append(transaction)

                # Update totals
                if transaction['amount'] >= 0:
                    total_credits += transaction['amount']
                else:
                    total_debits += abs(transaction['amount'])

        # Sort transactions by date (oldest to newest)
        transactions.sort(
            key=lambda t: gui_utils.parse_date_for_sorting(t['date']))

        # Calculate final balance
        calculated_final_balance = initial_balance + \
            total_credits - total_debits

        return BalancePreviewData(
            initial_balance=initial_balance,
            total_credits=total_credits,
            total_debits=total_debits,
            calculated_final_balance=calculated_final_balance,
            transaction_count=len(transactions),
            transactions=transactions
        )

    def _process_preview_row(
        self,
        row: Dict[str, str],
        parser: CSVParser,
        date_col: str,
        amount_col: str,
        desc_col: str,
        type_col: str,
        use_composite: bool,
        description_columns: List[str],
        description_separator: str,
        invert_values: bool,
        date_validator: Optional[DateValidator]
    ) -> Optional[Dict]:
        """
        Process a single row for balance preview.

        Args:
            row: CSV row data
            parser: CSVParser instance
            date_col: Date column name
            amount_col: Amount column name
            desc_col: Description column name
            type_col: Type column name
            use_composite: Whether to use composite description
            description_columns: List of columns for composite description
            description_separator: Separator for composite description
            invert_values: Whether to invert values
            date_validator: DateValidator instance or None

        Returns:
            Transaction dictionary or None if processing fails
        """
        try:
            date = row[date_col]
            amount = parser.normalize_amount(row[amount_col])

            # Build description using transaction_utils
            description = transaction_utils.build_transaction_description(
                row=row,
                desc_col=desc_col,
                description_columns=description_columns,
                separator=description_separator,
                use_composite=use_composite
            )

            # Apply value inversion if enabled
            if invert_values:
                amount = -amount

            # Determine transaction type using utility function
            trans_type = transaction_utils.determine_transaction_type(
                type_col, row, amount)

            # Check date validation status if enabled
            date_status = 'valid'
            if date_validator:
                try:
                    if not date_validator.is_within_range(date):
                        date_status = date_validator.get_date_status(date)
                except Exception:
                    # If validation fails, consider date valid
                    date_status = 'valid'

            return {
                'date': date,
                'description': description,
                'amount': amount,
                'type': trans_type,
                'date_status': date_status
            }

        except Exception:
            # Return None for rows that fail processing
            return None

    def format_balance_labels(
        self,
        balance_info: BalancePreviewData
    ) -> Dict[str, str]:
        """
        Format balance information for display labels.

        Args:
            balance_info: BalancePreviewData object

        Returns:
            Dictionary with formatted label texts:
            - total_credits: Formatted credit total text
            - total_debits: Formatted debit total text
            - calculated_balance: Formatted calculated balance text
            - transaction_count: Formatted transaction count text
        """
        return {
            'total_credits': (
                f"Total Credits (+): {balance_info.total_credits:.2f}"
            ),
            'total_debits': (
                f"Total Debits (-): {balance_info.total_debits:.2f}"
            ),
            'calculated_balance': (
                f"{balance_info.calculated_final_balance:.2f}"
            ),
            'transaction_count': (
                f"Total Transactions: {balance_info.transaction_count}"
            )
        }

    def get_transaction_preview_values(
        self,
        transactions: List[Dict]
    ) -> List[Tuple[str, str, str, str, List[str]]]:
        """
        Format transactions for treeview display.

        Args:
            transactions: List of transaction dictionaries

        Returns:
            List of tuples: (date, description, amount, type, tags)
            Each tuple contains values for treeview and tags for styling
        """
        result = []
        for trans in transactions:
            # Determine tags based on date status
            tags = []
            date_status = trans.get('date_status', 'valid')
            if date_status == 'before':
                tags.append('date_before')
            elif date_status == 'after':
                tags.append('date_after')

            # Format transaction for display
            date_str = trans['date']
            desc_str = trans['description'][:50]  # Truncate for display
            amount_str = f"{trans['amount']:.2f}"
            type_str = trans['type']

            result.append((date_str, desc_str, amount_str, type_str, tags))

        return result

    def validate_balance_input(
        self,
        action: str,
        value_if_allowed: str
    ) -> bool:
        """
        Validate numeric input for balance fields.

        Allows: digits, optional minus sign at start, optional decimal point.
        Blocks: letters, special characters, multiple decimal points.

        Args:
            action: '1' for insert, '0' for delete
            value_if_allowed: The value the entry will have if allowed

        Returns:
            True if change is allowed, False otherwise
        """
        if action == '0':  # Deletion always allowed
            return True

        # Use gui_utils to validate numeric input
        return gui_utils.validate_numeric_input(
            value_if_allowed,
            allow_negative=True,
            allow_decimal=True
        )

    def format_final_balance(self, calculated_balance: float) -> str:
        """
        Format the final balance for display.

        Args:
            calculated_balance: Calculated balance value

        Returns:
            Formatted balance string
        """
        return gui_utils.format_balance_value(calculated_balance)

    def get_date_status_for_transaction(
        self,
        row_idx: int,
        cached_balance_info: Optional[Dict]
    ) -> str:
        """
        Get date status for a specific transaction.

        Args:
            row_idx: Row index to check
            cached_balance_info: Cached balance information dictionary

        Returns:
            Date status string ('before', 'after', 'valid')
        """
        if not cached_balance_info:
            return 'valid'

        for trans in cached_balance_info.get('transactions', []):
            if trans.get('row_idx') == row_idx:
                return trans.get('date_status', 'valid')

        return 'valid'

    def should_show_date_actions(
        self,
        date_status: str,
        enable_date_validation: bool
    ) -> bool:
        """
        Determine if date action menu items should be shown.

        Args:
            date_status: Date status of transaction
            enable_date_validation: Whether date validation is enabled

        Returns:
            True if date actions should be shown, False otherwise
        """
        return (enable_date_validation and
                date_status in ('before', 'after'))

    def get_date_action_label_texts(
        self,
        current_action: str = 'adjust'
    ) -> Dict[str, str]:
        """
        Get label texts for date action menu items.

        Args:
            current_action: Currently selected action ('keep', 'adjust',
                          'exclude')

        Returns:
            Dictionary with label texts for each action:
            - keep: Label for keeping original date
            - adjust: Label for adjusting to boundary
            - exclude: Label for excluding transaction
        """
        return {
            'keep': (
                f"{'✓ ' if current_action == 'keep' else ''}"
                "Keep Original Date"
            ),
            'adjust': (
                f"{'✓ ' if current_action == 'adjust' else ''}"
                "Adjust to Boundary"
            ),
            'exclude': (
                f"{'✓ ' if current_action == 'exclude' else ''}"
                "Exclude Transaction"
            )
        }
