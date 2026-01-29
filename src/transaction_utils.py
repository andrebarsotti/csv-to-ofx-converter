"""
Transaction Utilities Module
============================
Helper functions for processing transaction data without UI dependencies.

Provides utility functions for:
- Building transaction descriptions from CSV columns
- Determining transaction types (DEBIT/CREDIT)
- Extracting transaction identifiers
- Calculating balance summaries
- Generating deterministic transaction IDs (FITIDs)

Author: Generated for Brazilian banking compatibility
License: MIT
"""

import uuid
from typing import List, Dict, Optional, Tuple
from .constants import NOT_MAPPED, NOT_SELECTED

# Application-specific namespace for deterministic FITID generation
# Uses UUID v5 to ensure reproducible transaction IDs
NAMESPACE_CSV_TO_OFX = uuid.uuid5(
    uuid.NAMESPACE_DNS,
    "csv-to-ofx-converter.local"
)


def build_transaction_description(
    row: Dict[str, str],
    desc_col: str,
    description_columns: List[str],
    separator: str,
    use_composite: bool
) -> str:
    """
    Build transaction description from single column or composite of multiple columns.

    Args:
        row: Dictionary containing row data with column values
        desc_col: Name of the description column (used if not composite)
        description_columns: List of column names to combine for composite description
        separator: String to join column values (e.g., ' ', ' - ', ', ')
        use_composite: If True, use composite description; otherwise use desc_col

    Returns:
        Transaction description string. Returns "Transaction" if composite is empty.

    Examples:
        >>> row = {'memo': 'Purchase', 'vendor': 'Store', 'category': 'Food'}
        >>> build_transaction_description(row, 'memo', ['memo', 'vendor'], ' - ', True)
        'Purchase - Store'

        >>> build_transaction_description(row, 'memo', [], ' ', False)
        'Purchase'
    """
    if use_composite:
        desc_parts = []
        for col_name in description_columns:
            if col_name != NOT_SELECTED and col_name in row:
                value = row[col_name].strip()
                if value:
                    desc_parts.append(value)
        description = separator.join(desc_parts)
        return description if description else "Transaction"

    # Use single description column
    return row.get(desc_col, "Transaction")


def determine_transaction_type(
    type_col: str,
    row: Dict[str, str],
    amount: float
) -> str:
    """
    Determine transaction type (DEBIT or CREDIT) from column value or amount sign.

    If type_col is mapped and contains a valid type (DEBIT/CREDIT), use it.
    Otherwise, infer from amount: negative = DEBIT, positive = CREDIT.

    Args:
        type_col: Name of the transaction type column (or NOT_MAPPED)
        row: Dictionary containing row data
        amount: Transaction amount (can be positive or negative)

    Returns:
        Transaction type string: 'DEBIT' or 'CREDIT'

    Examples:
        >>> determine_transaction_type('type', {'type': 'CREDIT'}, -50.0)
        'CREDIT'

        >>> determine_transaction_type(NOT_MAPPED, {}, -50.0)
        'DEBIT'

        >>> determine_transaction_type(NOT_MAPPED, {}, 100.0)
        'CREDIT'
    """
    if type_col != NOT_MAPPED and type_col in row:
        trans_type = row[type_col].upper()
        if trans_type in ['DEBIT', 'CREDIT']:
            return trans_type

    # Infer from amount sign
    return 'DEBIT' if amount < 0 else 'CREDIT'


def extract_transaction_id(
    id_col: str,
    row: Dict[str, str]
) -> Optional[str]:
    """
    Extract transaction ID from row data if column is mapped.

    Args:
        id_col: Name of the transaction ID column (or NOT_MAPPED)
        row: Dictionary containing row data

    Returns:
        Transaction ID string if found, None otherwise

    Examples:
        >>> extract_transaction_id('trans_id', {'trans_id': 'TXN123'})
        'TXN123'

        >>> extract_transaction_id(NOT_MAPPED, {'trans_id': 'TXN123'})
        None

        >>> extract_transaction_id('trans_id', {})
        None
    """
    if id_col != NOT_MAPPED and id_col in row:
        return row[id_col]
    return None


def calculate_balance_summary(
    transactions: List[Dict[str, any]],
    initial_balance: float
) -> Dict[str, float]:
    """
    Calculate balance summary from list of transactions.

    Args:
        transactions: List of transaction dictionaries with 'amount' key
        initial_balance: Starting balance before transactions

    Returns:
        Dictionary with:
        - 'initial_balance': Starting balance
        - 'total_credits': Sum of positive amounts
        - 'total_debits': Sum of absolute values of negative amounts
        - 'calculated_final_balance': initial + credits - debits
        - 'transaction_count': Number of transactions

    Examples:
        >>> transactions = [
        ...     {'amount': 100.0},
        ...     {'amount': -50.0},
        ...     {'amount': 25.0}
        ... ]
        >>> result = calculate_balance_summary(transactions, 1000.0)
        >>> result['total_credits']
        125.0
        >>> result['total_debits']
        50.0
        >>> result['calculated_final_balance']
        1075.0
    """
    total_credits = 0.0
    total_debits = 0.0

    for trans in transactions:
        amount = trans.get('amount', 0.0)
        if amount >= 0:
            total_credits += amount
        else:
            total_debits += abs(amount)

    calculated_final_balance = initial_balance + total_credits - total_debits

    return {
        'initial_balance': initial_balance,
        'total_credits': total_credits,
        'total_debits': total_debits,
        'calculated_final_balance': calculated_final_balance,
        'transaction_count': len(transactions)
    }


def validate_field_mappings(
    field_mappings: Dict[str, str],
    required_fields: List[str]
) -> Tuple[bool, Optional[str]]:
    """
    Validate that required fields are mapped (not set to NOT_MAPPED).

    Args:
        field_mappings: Dictionary of field name to column name mappings
        required_fields: List of field names that must be mapped

    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if all required fields are mapped
        - error_message: None if valid, error string if invalid

    Examples:
        >>> mappings = {'date': 'Date', 'amount': 'Amount', 'description': NOT_MAPPED}
        >>> validate_field_mappings(mappings, ['date', 'amount'])
        (True, None)

        >>> validate_field_mappings(mappings, ['date', 'amount', 'description'])
        (False, "Required field 'description' is not mapped")
    """
    for field in required_fields:
        if field not in field_mappings or field_mappings[field] == NOT_MAPPED:
            return False, f"Required field '{field}' is not mapped"

    return True, None


def parse_balance_value(balance_str: str, default: float = 0.0) -> float:
    """
    Parse balance string to float, with fallback to default value.

    Handles empty strings, whitespace, and invalid numeric formats.

    Args:
        balance_str: String representation of balance
        default: Default value to return if parsing fails

    Returns:
        Parsed float value or default if parsing fails

    Examples:
        >>> parse_balance_value('1000.50')
        1000.5

        >>> parse_balance_value('  ')
        0.0

        >>> parse_balance_value('invalid', 100.0)
        100.0
    """
    try:
        return float(balance_str.strip() or str(default))
    except (ValueError, AttributeError):
        return default


def generate_deterministic_fitid(
    date: str,
    amount: float,
    memo: str,
    account_id: str = "",
    disambiguation: str = ""
) -> str:
    """
    Generate deterministic FITID using UUID v5 based on transaction data.

    Same inputs always produce same output, enabling reliable reconciliation
    when regenerating OFX files. This ensures that if a user exports
    transactions and then exports them again (fully or partially), the
    transaction IDs remain consistent for duplicate detection.

    Args:
        date: Transaction date (any format, will be normalized to YYYYMMDD)
        amount: Transaction amount (will be formatted to 2 decimal places)
        memo: Transaction description/memo (will be normalized)
        account_id: Optional account identifier for uniqueness (default: "")
        disambiguation: Optional string to distinguish duplicate transactions (default: "")

    Returns:
        Deterministic UUID v5 string (format: 8-4-4-4-12 hex digits with hyphens)

    Examples:
        >>> fitid1 = generate_deterministic_fitid("20260115000000[-3:BRT]", -100.50, "Restaurant Purchase")
        >>> fitid2 = generate_deterministic_fitid("20260115", -100.50, "restaurant purchase")
        >>> # Same transaction data produces same ID despite format differences
        >>> len(fitid1) == 36  # UUID format length
        True

        >>> # Different amounts produce different IDs
        >>> id_a = generate_deterministic_fitid("20260115", -100.50, "Purchase")
        >>> id_b = generate_deterministic_fitid("20260115", -200.50, "Purchase")
        >>> id_a != id_b
        True
    """
    # Normalize date: Extract YYYYMMDD portion if in OFX format
    date_normalized = date.strip()
    if '000000' in date_normalized:
        # OFX format: YYYYMMDD000000[-3:BRT]
        date_normalized = date_normalized[:8]

    # Normalize amount: Format to 2 decimal places
    amount_normalized = f"{amount:.2f}"

    # Normalize memo: Strip whitespace, lowercase, limit length
    memo_normalized = memo.strip().lower()[:255]

    # Combine all components with pipe separator for clarity
    components = [
        date_normalized,
        amount_normalized,
        memo_normalized,
        account_id.strip(),
        disambiguation.strip()
    ]

    # Create deterministic string
    data_string = "|".join(components)

    # Generate UUID v5 from normalized data
    return str(uuid.uuid5(NAMESPACE_CSV_TO_OFX, data_string))
