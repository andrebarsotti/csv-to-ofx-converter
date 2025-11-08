#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSV to OFX Converter
====================
A complete application to convert CSV files to OFX format with GUI support.

This module provides a graphical interface for converting bank transaction CSV files
into OFX (Open Financial Exchange) format, supporting both standard and Brazilian CSV formats.

Author: Generated for Brazilian banking compatibility
License: MIT
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import csv
import os
import logging
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import uuid
import re


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('csv_to_ofx_converter.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class CSVParser:
    """
    Parser for CSV files supporting both standard and Brazilian formats.

    Attributes:
        delimiter (str): Column separator character (default: ',')
        decimal_separator (str): Decimal separator for amounts (default: '.')
    """

    def __init__(self, delimiter: str = ',', decimal_separator: str = '.'):
        """
        Initialize CSV parser with format settings.

        Args:
            delimiter: Character used to separate columns
            decimal_separator: Character used as decimal point
        """
        self.delimiter = delimiter
        self.decimal_separator = decimal_separator
        logger.info(f"CSVParser initialized: delimiter='{delimiter}', decimal='{decimal_separator}'")

    def parse_file(self, filepath: str) -> Tuple[List[str], List[Dict[str, str]]]:
        """
        Parse CSV file and return headers and rows.

        Args:
            filepath: Path to the CSV file

        Returns:
            Tuple containing list of headers and list of row dictionaries

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file is empty or malformed
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"CSV file not found: {filepath}")

        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()

            # Try with utf-8-sig to handle BOM if present
            if content.startswith('\ufeff'):
                content = content[1:]

            lines = content.splitlines()
            if not lines:
                raise ValueError("CSV file is empty")

            reader = csv.DictReader(lines, delimiter=self.delimiter)
            headers = reader.fieldnames

            if not headers:
                raise ValueError("CSV file has no headers")

            rows = list(reader)
            logger.info(f"Parsed CSV: {len(rows)} rows, {len(headers)} columns")

            return list(headers), rows

        except Exception as e:
            logger.error(f"Error parsing CSV file: {e}")
            raise

    def normalize_amount(self, amount_str: str) -> float:
        """
        Convert amount string to float, handling different decimal separators.

        Args:
            amount_str: String representation of amount

        Returns:
            Float value of amount

        Raises:
            ValueError: If amount cannot be parsed
        """
        if not amount_str:
            return 0.0

        # Remove currency symbols and spaces
        clean_str = amount_str.strip().replace('R$', '').replace('$', '').strip()

        # Handle Brazilian format: 1.234,56 -> 1234.56
        if self.decimal_separator == ',':
            clean_str = clean_str.replace('.', '').replace(',', '.')
        else:
            # Handle standard format: 1,234.56 -> 1234.56
            clean_str = clean_str.replace(',', '')

        try:
            return float(clean_str)
        except ValueError as e:
            logger.error(f"Cannot parse amount '{amount_str}': {e}")
            raise ValueError(f"Invalid amount format: {amount_str}")


class OFXGenerator:
    """
    Generator for OFX (Open Financial Exchange) files.

    OFX is a standard format for exchanging financial information between
    institutions and users.
    """

    def __init__(self):
        """Initialize OFX generator."""
        self.transactions = []
        logger.info("OFXGenerator initialized")

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
                bank_name: str = "CSV Import", currency: str = "BRL"):
        """
        Generate OFX file with all added transactions.

        Args:
            output_path: Path where OFX file will be saved
            account_id: Account identifier
            bank_name: Name of the financial institution
            currency: Currency code (default: BRL for Brazilian Real)

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

        # Calculate balance
        balance = sum(t['amount'] for t in self.transactions)

        # Generate current timestamp
        now = datetime.now()
        timestamp = f"{now.strftime('%Y%m%d%H%M%S')}[0:GMT]"

        # Build OFX content
        ofx_content = self._build_ofx_content(
            timestamp, bank_name, account_id, currency,
            start_date, end_date, balance
        )

        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(ofx_content)

        logger.info(f"OFX file generated: {output_path} ({len(self.transactions)} transactions)")

    def _build_ofx_content(self, timestamp: str, bank_name: str,
                          account_id: str, currency: str,
                          start_date: str, end_date: str, balance: float) -> str:
        """
        Build complete OFX file content.

        Args:
            timestamp: Current timestamp
            bank_name: Financial institution name
            account_id: Account identifier
            currency: Currency code
            start_date: Start date of statement
            end_date: End date of statement
            balance: Final balance

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

        # Close tags
        lines.extend([
            "</BANKTRANLIST>",
            "<LEDGERBAL>",
            f"<BALAMT>{balance:.2f}</BALAMT>",
            f"<DTASOF>{end_date}</DTASOF>",
            "</LEDGERBAL>",
            "</CCSTMTRS>",
            "</CCSTMTTRNRS>",
            "</CREDITCARDMSGSRSV1>",
            "</OFX>",
        ])

        return '\n'.join(lines)


class DateValidator:
    """
    Validator for transaction dates against a specified date range.

    Validates transactions to ensure they fall within a credit card statement period,
    and provides options for handling out-of-range transactions.
    """

    def __init__(self, start_date_str: str, end_date_str: str):
        """
        Initialize date validator with start and end dates.

        Args:
            start_date_str: Start date of the statement period (various formats)
            end_date_str: End date of the statement period (various formats)

        Raises:
            ValueError: If dates cannot be parsed
        """
        self.start_date = self._parse_date_to_datetime(start_date_str)
        self.end_date = self._parse_date_to_datetime(end_date_str)

        if self.start_date > self.end_date:
            raise ValueError("Start date must be before or equal to end date")

        logger.info(f"DateValidator initialized: {self.start_date.date()} to {self.end_date.date()}")

    def _parse_date_to_datetime(self, date_str: str) -> datetime:
        """
        Parse date string to datetime object.

        Args:
            date_str: Date string in various formats

        Returns:
            datetime object

        Raises:
            ValueError: If date format is not recognized
        """
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

        for fmt in date_formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue

        raise ValueError(f"Unrecognized date format: {date_str}")

    def is_within_range(self, date_str: str) -> bool:
        """
        Check if a date is within the valid range.

        Args:
            date_str: Date string to check

        Returns:
            True if date is within range, False otherwise
        """
        try:
            date_obj = self._parse_date_to_datetime(date_str)
            return self.start_date <= date_obj <= self.end_date
        except ValueError:
            return False

    def get_date_status(self, date_str: str) -> str:
        """
        Determine if a date is before, within, or after the valid range.

        Args:
            date_str: Date string to check

        Returns:
            'within', 'before', or 'after'

        Raises:
            ValueError: If date cannot be parsed
        """
        date_obj = self._parse_date_to_datetime(date_str)

        if date_obj < self.start_date:
            return 'before'
        elif date_obj > self.end_date:
            return 'after'
        else:
            return 'within'

    def adjust_date_to_boundary(self, date_str: str) -> str:
        """
        Adjust an out-of-range date to the nearest boundary.

        Args:
            date_str: Date string to adjust

        Returns:
            Adjusted date string in YYYY-MM-DD format

        Raises:
            ValueError: If date cannot be parsed
        """
        status = self.get_date_status(date_str)

        if status == 'before':
            return self.start_date.strftime('%Y-%m-%d')
        elif status == 'after':
            return self.end_date.strftime('%Y-%m-%d')
        else:
            # Already within range
            date_obj = self._parse_date_to_datetime(date_str)
            return date_obj.strftime('%Y-%m-%d')


class ConverterGUI:
    """
    Graphical User Interface for CSV to OFX conversion.

    Provides an intuitive interface for:
    - Loading CSV files
    - Mapping CSV columns to OFX fields
    - Configuring CSV format (delimiter, decimal separator)
    - Converting and saving OFX files
    """

    def __init__(self, root: tk.Tk):
        """
        Initialize the GUI.

        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("CSV to OFX Converter")
        self.root.geometry("900x800")

        # Variables
        self.csv_file = tk.StringVar()
        self.delimiter = tk.StringVar(value=',')
        self.decimal_separator = tk.StringVar(value='.')
        self.account_id = tk.StringVar(value='')
        self.bank_name = tk.StringVar(value='CSV Import')
        self.currency = tk.StringVar(value='BRL')
        self.start_date = tk.StringVar(value='')
        self.end_date = tk.StringVar(value='')
        self.enable_date_validation = tk.BooleanVar(value=False)

        # Data
        self.csv_headers: List[str] = []
        self.csv_data: List[Dict[str, str]] = []
        self.field_mappings: Dict[str, tk.StringVar] = {}

        # Build UI
        self._create_widgets()

        logger.info("GUI initialized")

    def _create_widgets(self):
        """Create all GUI widgets."""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)

        # Title
        title_label = ttk.Label(main_frame, text="CSV to OFX Converter",
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, pady=(0, 20))

        # File selection section
        self._create_file_section(main_frame, row=1)

        # CSV format section
        self._create_format_section(main_frame, row=2)

        # OFX configuration section
        self._create_ofx_config_section(main_frame, row=3)

        # Date validation section
        self._create_date_validation_section(main_frame, row=4)

        # Field mapping section
        self._create_mapping_section(main_frame, row=5)

        # Buttons section
        self._create_buttons_section(main_frame, row=6)

        # Log section
        self._create_log_section(main_frame, row=7)

    def _create_file_section(self, parent: ttk.Frame, row: int):
        """Create file selection section."""
        frame = ttk.LabelFrame(parent, text="1. Select CSV File", padding="10")
        frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=5)
        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text="CSV File:").grid(row=0, column=0, sticky=tk.W, padx=5)
        ttk.Entry(frame, textvariable=self.csv_file, state='readonly').grid(
            row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(frame, text="Browse...", command=self._browse_csv).grid(
            row=0, column=2, padx=5)

    def _create_format_section(self, parent: ttk.Frame, row: int):
        """Create CSV format configuration section."""
        frame = ttk.LabelFrame(parent, text="2. CSV Format", padding="10")
        frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=5)

        # Delimiter options
        ttk.Label(frame, text="Delimiter:").grid(row=0, column=0, sticky=tk.W, padx=5)
        delimiter_frame = ttk.Frame(frame)
        delimiter_frame.grid(row=0, column=1, sticky=tk.W, padx=5)

        ttk.Radiobutton(delimiter_frame, text="Comma (,)", variable=self.delimiter,
                       value=',').pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(delimiter_frame, text="Semicolon (;)", variable=self.delimiter,
                       value=';').pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(delimiter_frame, text="Tab", variable=self.delimiter,
                       value='\t').pack(side=tk.LEFT, padx=5)

        # Decimal separator options
        ttk.Label(frame, text="Decimal:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        decimal_frame = ttk.Frame(frame)
        decimal_frame.grid(row=1, column=1, sticky=tk.W, padx=5)

        ttk.Radiobutton(decimal_frame, text="Dot (.)", variable=self.decimal_separator,
                       value='.').pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(decimal_frame, text="Comma (,)", variable=self.decimal_separator,
                       value=',').pack(side=tk.LEFT, padx=5)

    def _create_ofx_config_section(self, parent: ttk.Frame, row: int):
        """Create OFX configuration section."""
        frame = ttk.LabelFrame(parent, text="3. OFX Configuration", padding="10")
        frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=5)
        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text="Account ID:").grid(row=0, column=0, sticky=tk.W, padx=5)
        ttk.Entry(frame, textvariable=self.account_id).grid(
            row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=2)

        ttk.Label(frame, text="Bank Name:").grid(row=1, column=0, sticky=tk.W, padx=5)
        ttk.Entry(frame, textvariable=self.bank_name).grid(
            row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=2)

        ttk.Label(frame, text="Currency:").grid(row=2, column=0, sticky=tk.W, padx=5)
        currency_combo = ttk.Combobox(frame, textvariable=self.currency,
                                     values=['BRL', 'USD', 'EUR', 'GBP'], state='readonly')
        currency_combo.grid(row=2, column=1, sticky=tk.W, padx=5, pady=2)

    def _create_date_validation_section(self, parent: ttk.Frame, row: int):
        """Create date validation section."""
        frame = ttk.LabelFrame(parent, text="3b. Statement Date Range (Optional)", padding="10")
        frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=5)
        frame.columnconfigure(1, weight=1)

        # Checkbox to enable date validation
        enable_check = ttk.Checkbutton(
            frame,
            text="Enable date validation for credit card statement period",
            variable=self.enable_date_validation,
            command=self._toggle_date_inputs
        )
        enable_check.grid(row=0, column=0, columnspan=3, sticky=tk.W, padx=5, pady=5)

        # Start date
        ttk.Label(frame, text="Start Date:").grid(row=1, column=0, sticky=tk.W, padx=5)
        self.start_date_entry = ttk.Entry(frame, textvariable=self.start_date, state='disabled')
        self.start_date_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=2)
        ttk.Label(frame, text="(e.g., 2025-10-01 or 01/10/2025)",
                 font=('Arial', 8), foreground='gray').grid(row=1, column=2, sticky=tk.W, padx=5)

        # End date
        ttk.Label(frame, text="End Date:").grid(row=2, column=0, sticky=tk.W, padx=5)
        self.end_date_entry = ttk.Entry(frame, textvariable=self.end_date, state='disabled')
        self.end_date_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5, pady=2)
        ttk.Label(frame, text="(e.g., 2025-10-31 or 31/10/2025)",
                 font=('Arial', 8), foreground='gray').grid(row=2, column=2, sticky=tk.W, padx=5)

    def _toggle_date_inputs(self):
        """Enable or disable date input fields based on checkbox state."""
        if self.enable_date_validation.get():
            self.start_date_entry.configure(state='normal')
            self.end_date_entry.configure(state='normal')
        else:
            self.start_date_entry.configure(state='disabled')
            self.end_date_entry.configure(state='disabled')

    def _create_mapping_section(self, parent: ttk.Frame, row: int):
        """Create field mapping section."""
        self.mapping_frame = ttk.LabelFrame(parent, text="4. Map CSV Columns to OFX Fields",
                                           padding="10")
        self.mapping_frame.grid(row=row, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        self.mapping_frame.columnconfigure(1, weight=1)
        parent.rowconfigure(row, weight=1)

        # This will be populated when CSV is loaded
        self.mapping_widgets = {}

    def _create_buttons_section(self, parent: ttk.Frame, row: int):
        """Create action buttons section."""
        frame = ttk.Frame(parent)
        frame.grid(row=row, column=0, pady=10)

        ttk.Button(frame, text="Load CSV", command=self._load_csv).pack(
            side=tk.LEFT, padx=5)
        ttk.Button(frame, text="Convert to OFX", command=self._convert).pack(
            side=tk.LEFT, padx=5)
        ttk.Button(frame, text="Clear", command=self._clear).pack(
            side=tk.LEFT, padx=5)

    def _create_log_section(self, parent: ttk.Frame, row: int):
        """Create log display section."""
        frame = ttk.LabelFrame(parent, text="Log", padding="5")
        frame.grid(row=row, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        parent.rowconfigure(row, weight=1)

        self.log_text = scrolledtext.ScrolledText(frame, height=8, state='disabled')
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    def _browse_csv(self):
        """Open file dialog to select CSV file."""
        filename = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            self.csv_file.set(filename)
            self._log(f"Selected file: {filename}")

    def _load_csv(self):
        """Load and parse CSV file."""
        if not self.csv_file.get():
            messagebox.showwarning("Warning", "Please select a CSV file first")
            return

        try:
            self._log("Loading CSV file...")

            # Create parser with selected format
            parser = CSVParser(
                delimiter=self.delimiter.get(),
                decimal_separator=self.decimal_separator.get()
            )

            # Parse file
            self.csv_headers, self.csv_data = parser.parse_file(self.csv_file.get())

            # Update mapping UI
            self._update_mapping_ui()

            self._log(f"CSV loaded successfully: {len(self.csv_data)} rows")
            messagebox.showinfo("Success", f"CSV file loaded successfully!\n"
                                         f"Rows: {len(self.csv_data)}\n"
                                         f"Columns: {len(self.csv_headers)}")

        except Exception as e:
            self._log(f"Error loading CSV: {e}")
            messagebox.showerror("Error", f"Failed to load CSV file:\n{e}")

    def _update_mapping_ui(self):
        """Update field mapping UI with CSV columns."""
        # Clear existing mappings
        for widget in self.mapping_frame.winfo_children():
            widget.destroy()

        self.field_mappings.clear()

        # Define OFX fields that need mapping
        ofx_fields = [
            ('date', 'Date', 'Transaction date'),
            ('amount', 'Amount', 'Transaction amount'),
            ('description', 'Description', 'Transaction description/memo'),
            ('type', 'Type (optional)', 'Transaction type: DEBIT or CREDIT'),
            ('id', 'ID (optional)', 'Unique transaction identifier'),
        ]

        # Add "None" option for optional fields
        column_options = ['-- Not Mapped --'] + self.csv_headers

        # Create mapping widgets
        for idx, (field_key, field_label, field_help) in enumerate(ofx_fields):
            ttk.Label(self.mapping_frame, text=f"{field_label}:").grid(
                row=idx, column=0, sticky=tk.W, padx=5, pady=3)

            var = tk.StringVar(value='-- Not Mapped --')
            self.field_mappings[field_key] = var

            combo = ttk.Combobox(self.mapping_frame, textvariable=var,
                               values=column_options, state='readonly')
            combo.grid(row=idx, column=1, sticky=(tk.W, tk.E), padx=5, pady=3)

            ttk.Label(self.mapping_frame, text=field_help, font=('Arial', 8),
                     foreground='gray').grid(row=idx, column=2, sticky=tk.W, padx=5)

        self.mapping_frame.columnconfigure(1, weight=1)

    def _handle_out_of_range_transaction(self, row_idx: int, date_str: str,
                                         status: str, validator: DateValidator,
                                         description: str) -> Optional[str]:
        """
        Show dialog to handle an out-of-range transaction.

        Args:
            row_idx: Row index in CSV (1-based)
            date_str: Original transaction date
            status: 'before' or 'after' the valid range
            validator: DateValidator instance
            description: Transaction description

        Returns:
            Adjusted date string, or None to exclude the transaction
        """
        # Create dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Out-of-Range Transaction Detected")
        dialog.geometry("600x300")
        dialog.transient(self.root)
        dialog.grab_set()

        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")

        result = {'action': None, 'date': None}

        # Main frame
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Warning message
        warning_label = ttk.Label(
            main_frame,
            text=f"Transaction #{row_idx} is out of range!",
            font=('Arial', 14, 'bold'),
            foreground='red'
        )
        warning_label.pack(pady=(0, 10))

        # Transaction details
        details_frame = ttk.Frame(main_frame)
        details_frame.pack(fill=tk.X, pady=10)

        ttk.Label(details_frame, text=f"Transaction Date:", font=('Arial', 10, 'bold')).grid(
            row=0, column=0, sticky=tk.W, pady=2)
        ttk.Label(details_frame, text=date_str).grid(row=0, column=1, sticky=tk.W, padx=10, pady=2)

        ttk.Label(details_frame, text=f"Description:", font=('Arial', 10, 'bold')).grid(
            row=1, column=0, sticky=tk.W, pady=2)
        ttk.Label(details_frame, text=description[:50] + ('...' if len(description) > 50 else '')).grid(
            row=1, column=1, sticky=tk.W, padx=10, pady=2)

        ttk.Label(details_frame, text=f"Valid Range:", font=('Arial', 10, 'bold')).grid(
            row=2, column=0, sticky=tk.W, pady=2)
        range_text = f"{validator.start_date.strftime('%Y-%m-%d')} to {validator.end_date.strftime('%Y-%m-%d')}"
        ttk.Label(details_frame, text=range_text).grid(row=2, column=1, sticky=tk.W, padx=10, pady=2)

        if status == 'before':
            status_text = f"This transaction occurs BEFORE the start date"
        else:
            status_text = f"This transaction occurs AFTER the end date"

        ttk.Label(details_frame, text=f"Status:", font=('Arial', 10, 'bold')).grid(
            row=3, column=0, sticky=tk.W, pady=2)
        ttk.Label(details_frame, text=status_text, foreground='orange').grid(
            row=3, column=1, sticky=tk.W, padx=10, pady=2)

        # Question
        question_label = ttk.Label(
            main_frame,
            text="How would you like to handle this transaction?",
            font=('Arial', 10)
        )
        question_label.pack(pady=10)

        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(pady=10)

        def adjust_date():
            adjusted_date = validator.adjust_date_to_boundary(date_str)
            result['action'] = 'adjust'
            result['date'] = adjusted_date
            dialog.destroy()

        def exclude_transaction():
            result['action'] = 'exclude'
            dialog.destroy()

        # Adjust button
        boundary = "start date" if status == 'before' else "end date"
        adjust_btn = ttk.Button(
            buttons_frame,
            text=f"Adjust to {boundary}",
            command=adjust_date
        )
        adjust_btn.pack(side=tk.LEFT, padx=5)

        # Exclude button
        exclude_btn = ttk.Button(
            buttons_frame,
            text="Exclude this transaction",
            command=exclude_transaction
        )
        exclude_btn.pack(side=tk.LEFT, padx=5)

        # Wait for dialog to close
        dialog.wait_window()

        if result['action'] == 'adjust':
            return result['date']
        else:
            return None

    def _convert(self):
        """Convert CSV to OFX."""
        if not self.csv_data:
            messagebox.showwarning("Warning", "Please load a CSV file first")
            return

        # Validate required mappings
        date_col = self.field_mappings['date'].get()
        amount_col = self.field_mappings['amount'].get()
        desc_col = self.field_mappings['description'].get()

        if date_col == '-- Not Mapped --' or amount_col == '-- Not Mapped --' \
           or desc_col == '-- Not Mapped --':
            messagebox.showwarning("Warning",
                                  "Please map at least Date, Amount, and Description fields")
            return

        # Initialize date validator if enabled
        date_validator = None
        if self.enable_date_validation.get():
            start_date_str = self.start_date.get().strip()
            end_date_str = self.end_date.get().strip()

            if not start_date_str or not end_date_str:
                messagebox.showwarning("Warning",
                                      "Please enter both start and end dates for validation")
                return

            try:
                date_validator = DateValidator(start_date_str, end_date_str)
                self._log(f"Date validation enabled: {start_date_str} to {end_date_str}")
            except ValueError as e:
                messagebox.showerror("Error", f"Invalid date range: {e}")
                return

        try:
            self._log("Converting CSV to OFX...")

            # Create parser and generator
            parser = CSVParser(
                delimiter=self.delimiter.get(),
                decimal_separator=self.decimal_separator.get()
            )
            generator = OFXGenerator()

            # Get optional field mappings
            type_col = self.field_mappings['type'].get()
            id_col = self.field_mappings['id'].get()

            # Track statistics
            total_rows = len(self.csv_data)
            processed = 0
            excluded = 0
            adjusted = 0

            # Process each row
            for row_idx, row in enumerate(self.csv_data, 1):
                try:
                    date = row[date_col]
                    amount = parser.normalize_amount(row[amount_col])
                    description = row[desc_col]

                    # Validate date if validator is enabled
                    if date_validator:
                        if not date_validator.is_within_range(date):
                            status = date_validator.get_date_status(date)
                            self._log(f"Row {row_idx}: Date {date} is out of range ({status})")

                            # Show dialog and get user choice
                            adjusted_date = self._handle_out_of_range_transaction(
                                row_idx, date, status, date_validator, description
                            )

                            if adjusted_date is None:
                                # User chose to exclude
                                self._log(f"Row {row_idx}: Transaction excluded by user")
                                excluded += 1
                                continue
                            else:
                                # User chose to adjust
                                self._log(f"Row {row_idx}: Date adjusted from {date} to {adjusted_date}")
                                date = adjusted_date
                                adjusted += 1

                    # Get transaction type if mapped
                    if type_col != '-- Not Mapped --' and type_col in row:
                        trans_type = row[type_col].upper()
                        # Validate type
                        if trans_type not in ['DEBIT', 'CREDIT']:
                            # Try to infer from amount
                            trans_type = 'DEBIT' if amount < 0 else 'CREDIT'
                    else:
                        # Infer from amount
                        trans_type = 'DEBIT' if amount < 0 else 'CREDIT'

                    # Get transaction ID if mapped
                    trans_id = None
                    if id_col != '-- Not Mapped --' and id_col in row:
                        trans_id = row[id_col]

                    generator.add_transaction(
                        date=date,
                        amount=amount,
                        description=description,
                        transaction_type=trans_type,
                        transaction_id=trans_id
                    )
                    processed += 1

                except Exception as e:
                    self._log(f"Warning: Skipping row {row_idx}: {e}")
                    excluded += 1

            # Ask for output file
            output_file = filedialog.asksaveasfilename(
                title="Save OFX File",
                defaultextension=".ofx",
                filetypes=[("OFX files", "*.ofx"), ("All files", "*.*")]
            )

            if not output_file:
                self._log("Conversion cancelled")
                return

            # Generate OFX file
            generator.generate(
                output_path=output_file,
                account_id=self.account_id.get() or "UNKNOWN",
                bank_name=self.bank_name.get(),
                currency=self.currency.get()
            )

            self._log(f"OFX file created: {output_file}")

            # Build success message with statistics
            success_msg = (f"OFX file created successfully!\n"
                          f"Location: {output_file}\n"
                          f"Total rows processed: {total_rows}\n"
                          f"Transactions included: {processed}")

            if date_validator:
                success_msg += f"\nDate-adjusted: {adjusted}\nExcluded: {excluded}"

            messagebox.showinfo("Success", success_msg)

        except Exception as e:
            self._log(f"Error during conversion: {e}")
            messagebox.showerror("Error", f"Conversion failed:\n{e}")

    def _clear(self):
        """Clear all data and reset form."""
        self.csv_file.set('')
        self.csv_headers = []
        self.csv_data = []
        self.account_id.set('')
        self.bank_name.set('CSV Import')
        self.currency.set('BRL')
        self.start_date.set('')
        self.end_date.set('')
        self.enable_date_validation.set(False)
        self._toggle_date_inputs()

        # Clear mapping UI
        for widget in self.mapping_frame.winfo_children():
            widget.destroy()

        self._log("Form cleared")

    def _log(self, message: str):
        """
        Add message to log display.

        Args:
            message: Message to display
        """
        self.log_text.configure(state='normal')
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.log_text.configure(state='disabled')

        logger.info(message)


def main():
    """Main entry point for the application."""
    root = tk.Tk()
    app = ConverterGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
