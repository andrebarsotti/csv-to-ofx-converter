"""
OFX Generator Module
===================
Generator for OFX (Open Financial Exchange) files.

OFX is a standard format for exchanging financial information between
institutions and users.

Author: Generated for Brazilian banking compatibility
License: MIT
"""

import logging
import uuid
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)


class OFXGenerator:
    """
    Generator for OFX (Open Financial Exchange) files.

    OFX is a standard format for exchanging financial information between
    institutions and users.
    """

    def __init__(self, invert_values: bool = False):
        """
        Initialize OFX generator.

        Args:
            invert_values: If True, invert all transaction amounts (debit <-> credit)
        """
        self.transactions = []
        self.invert_values = invert_values
        logger.info(f"OFXGenerator initialized (invert_values={invert_values})")

    def add_transaction(self, date: str, amount: float, description: str,
                       transaction_type: str = 'DEBIT', transaction_id: Optional[str] = None):
        """
        Add a transaction to the OFX file.

        Args:
            date: Transaction date (various formats accepted)
            amount: Transaction amount (negative for debits)
            description: Transaction description/memo
            transaction_type: Type of transaction (DEBIT or CREDIT)
            transaction_id: Unique transaction ID (UUID generated if not provided)
        """
        parsed_date = self._parse_date(date)
        if transaction_id is None:
            transaction_id = str(uuid.uuid4())

        # Apply value inversion if enabled
        if self.invert_values:
            amount = -amount
            # Swap transaction type
            transaction_type = 'CREDIT' if transaction_type == 'DEBIT' else 'DEBIT'

        # Ensure amount sign matches transaction type
        if transaction_type == 'DEBIT' and amount > 0:
            amount = -amount
        elif transaction_type == 'CREDIT' and amount < 0:
            amount = abs(amount)

        transaction = {
            'type': transaction_type,
            'date': parsed_date,
            'amount': amount,
            'id': transaction_id,
            'memo': description[:255]  # Limit description length
        }

        self.transactions.append(transaction)
        logger.debug(f"Transaction added: {transaction}")

    def _parse_date(self, date_str: str) -> str:
        """
        Parse various date formats and convert to OFX format (YYYYMMDD000000).

        Args:
            date_str: Date string in various formats

        Returns:
            Date in OFX format: YYYYMMDD000000[-3:BRT]

        Raises:
            ValueError: If date format is not recognized
        """
        # Common date formats
        date_formats = [
            '%Y-%m-%d',      # 2025-10-22
            '%d/%m/%Y',      # 22/10/2025
            '%m/%d/%Y',      # 10/22/2025
            '%Y/%m/%d',      # 2025/10/22
            '%d-%m-%Y',      # 22-10-2025
            '%d.%m.%Y',      # 22.10.2025
            '%Y%m%d',        # 20251022
        ]

        date_str = date_str.strip()
        parsed_date = None

        for fmt in date_formats:
            try:
                parsed_date = datetime.strptime(date_str, fmt)
                break
            except ValueError:
                continue

        if parsed_date is None:
            raise ValueError(f"Unrecognized date format: {date_str}")

        # Format: YYYYMMDD000000[-3:BRT]
        return f"{parsed_date.strftime('%Y%m%d')}000000[-3:BRT]"

    def generate(self, output_path: str, account_id: str = "UNKNOWN",
                bank_name: str = "CSV Import", currency: str = "BRL",
                initial_balance: float = 0.0, final_balance: Optional[float] = None):
        """
        Generate OFX file with all added transactions.

        Args:
            output_path: Path where OFX file will be saved
            account_id: Account identifier
            bank_name: Name of the financial institution
            currency: Currency code (default: BRL for Brazilian Real)
            initial_balance: Starting balance (default: 0.0)
            final_balance: Ending balance (if None, will be calculated from transactions)

        Raises:
            ValueError: If no transactions have been added
        """
        if not self.transactions:
            raise ValueError("No transactions to export")

        # Sort transactions by date
        self.transactions.sort(key=lambda x: x['date'])

        # Get date range
        start_date = self.transactions[0]['date']
        end_date = self.transactions[-1]['date']

        # Calculate or use provided final balance
        if final_balance is None:
            transaction_total = sum(t['amount'] for t in self.transactions)
            final_balance = initial_balance + transaction_total

        # Generate current timestamp
        now = datetime.now()
        timestamp = f"{now.strftime('%Y%m%d%H%M%S')}[0:GMT]"

        # Build OFX content
        ofx_content = self._build_ofx_content(
            timestamp, bank_name, account_id, currency,
            start_date, end_date, initial_balance, final_balance
        )

        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(ofx_content)

        logger.info(f"OFX file generated: {output_path} ({len(self.transactions)} transactions, "
                   f"initial={initial_balance:.2f}, final={final_balance:.2f})")

    def _build_ofx_content(self, timestamp: str, bank_name: str,
                          account_id: str, currency: str,
                          start_date: str, end_date: str,
                          initial_balance: float, final_balance: float) -> str:
        """
        Build complete OFX file content.

        Args:
            timestamp: Current timestamp
            bank_name: Financial institution name
            account_id: Account identifier
            currency: Currency code
            start_date: Start date of statement
            end_date: End date of statement
            initial_balance: Starting balance
            final_balance: Ending balance

        Returns:
            Complete OFX file content as string
        """
        lines = [
            "OFXHEADER:100",
            "DATA:OFXSGML",
            "VERSION:102",
            "SECURITY:NONE",
            "ENCODING:USASCII",
            "CHARSET:1252",
            "COMPRESSION:NONE",
            "OLDFILEUID:NONE",
            "NEWFILEUID:NONE",
            "<OFX>",
            "<SIGNONMSGSRSV1>",
            "<SONRS>",
            "<STATUS>",
            "<CODE>0</CODE>",
            "<SEVERITY>INFO</SEVERITY>",
            "</STATUS>",
            f"<DTSERVER>{timestamp}</DTSERVER>",
            "<LANGUAGE>POR</LANGUAGE>",
            "<FI>",
            f"<ORG>{bank_name}</ORG>",
            "<FID>0</FID>",
            "</FI>",
            "</SONRS>",
            "</SIGNONMSGSRSV1>",
            "<CREDITCARDMSGSRSV1>",
            "<CCSTMTTRNRS>",
            "<TRNUID>1001</TRNUID>",
            "<STATUS>",
            "<CODE>0</CODE>",
            "<SEVERITY>INFO</SEVERITY>",
            "</STATUS>",
            "<CCSTMTRS>",
            f"<CURDEF>{currency}</CURDEF>",
            "<CCACCTFROM>",
            f"<ACCTID>{account_id}</ACCTID>",
            "</CCACCTFROM>",
            "<BANKTRANLIST>",
            f"<DTSTART>{start_date}</DTSTART>",
            f"<DTEND>{end_date}</DTEND>",
        ]

        # Add all transactions
        for transaction in self.transactions:
            lines.extend([
                "<STMTTRN>",
                f"<TRNTYPE>{transaction['type']}</TRNTYPE>",
                f"<DTPOSTED>{transaction['date']}</DTPOSTED>",
                f"<TRNAMT>{transaction['amount']:.2f}</TRNAMT>",
                f"<FITID>{transaction['id']}</FITID>",
                f"<MEMO>{transaction['memo']}</MEMO>",
                "</STMTTRN>",
            ])

        # Close tags and add balance information
        lines.extend([
            "</BANKTRANLIST>",
            "<LEDGERBAL>",
            f"<BALAMT>{final_balance:.2f}</BALAMT>",
            f"<DTASOF>{end_date}</DTASOF>",
            "</LEDGERBAL>",
            "<AVAILBAL>",
            f"<BALAMT>{initial_balance:.2f}</BALAMT>",
            f"<DTASOF>{start_date}</DTASOF>",
            "</AVAILBAL>",
            "</CCSTMTRS>",
            "</CCSTMTTRNRS>",
            "</CREDITCARDMSGSRSV1>",
            "</OFX>",
        ])

        return '\n'.join(lines)
