"""
csv_format_step.py - CSV Format Step (Step 2)

This module implements the CSV format configuration step for the CSV to OFX Converter wizard.
Users configure the delimiter and decimal separator for parsing the CSV file.

Classes:
    CSVFormatStep: Step 2 implementation for CSV format configuration
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Tuple, Optional

from src.gui_wizard_step import WizardStep, StepConfig


class CSVFormatStep(WizardStep):
    """
    Step 2: Configure CSV format (delimiter and decimal separator).

    This step allows users to configure how the CSV file will be parsed by selecting:
    - Column delimiter: comma, semicolon, or tab
    - Decimal separator: dot or comma

    The step provides common format combinations and examples to guide users.

    UI Elements:
        - Description label explaining the step purpose
        - Delimiter section with radio buttons (comma, semicolon, tab)
        - Decimal separator section with radio buttons (dot, comma)
        - Information text about format combinations

    Data Collected:
        - delimiter: Selected column delimiter (',', ';', or '\t')
        - decimal_separator: Selected decimal separator ('.' or ',')

    Validation:
        - Always valid since defaults are always provided by parent

    Example:
        >>> step = CSVFormatStep(parent_gui)
        >>> container = step.create(parent_frame)
        >>> step.show()
        >>> result = step.validate()
        >>> print(f"Delimiter: {result.data['delimiter']}")
        >>> print(f"Decimal: {result.data['decimal_separator']}")
    """

    def __init__(self, parent):
        """
        Initialize CSV format step.

        Args:
            parent: Parent wizard orchestrator (ConverterGUI instance)
        """
        config = StepConfig(
            step_number=1,
            step_name="CSV Format",
            step_title="Step 2: Configure CSV Format"
        )
        super().__init__(parent, config)

    def _build_ui(self):
        """
        Build CSV format configuration UI elements.

        Creates and arranges the following widgets:
        - Description label at the top
        - Delimiter section with label and radio buttons
        - Decimal separator section with label and radio buttons
        - Information text at the bottom

        All widgets are arranged using grid layout for proper alignment.
        Radio buttons are bound to parent's delimiter and decimal_separator StringVars.
        """
        # Description label
        ttk.Label(
            self.container,
            text="Select the format of your CSV file:",
            font=('Arial', 10)
        ).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 20))

        # Delimiter section
        ttk.Label(
            self.container,
            text="Column Delimiter:",
            font=('Arial', 10, 'bold')
        ).grid(row=1, column=0, sticky=tk.W, pady=10)

        delimiter_frame = ttk.Frame(self.container)
        delimiter_frame.grid(row=1, column=1, sticky=tk.W, padx=20, pady=10)

        # Delimiter radio buttons
        ttk.Radiobutton(
            delimiter_frame,
            text="Comma (,) - Standard format",
            variable=self.parent.delimiter,
            value=','
        ).pack(anchor=tk.W, pady=2)

        ttk.Radiobutton(
            delimiter_frame,
            text="Semicolon (;) - Common in Brazilian exports",
            variable=self.parent.delimiter,
            value=';'
        ).pack(anchor=tk.W, pady=2)

        ttk.Radiobutton(
            delimiter_frame,
            text="Tab - Tab-separated values",
            variable=self.parent.delimiter,
            value='\t'
        ).pack(anchor=tk.W, pady=2)

        # Store reference for testing
        self._widgets['delimiter_frame'] = delimiter_frame

        # Decimal separator section
        ttk.Label(
            self.container,
            text="Decimal Separator:",
            font=('Arial', 10, 'bold')
        ).grid(row=2, column=0, sticky=tk.W, pady=10)

        decimal_frame = ttk.Frame(self.container)
        decimal_frame.grid(row=2, column=1, sticky=tk.W, padx=20, pady=10)

        # Decimal separator radio buttons
        ttk.Radiobutton(
            decimal_frame,
            text="Dot (.) - Standard format (e.g., 100.50)",
            variable=self.parent.decimal_separator,
            value='.'
        ).pack(anchor=tk.W, pady=2)

        ttk.Radiobutton(
            decimal_frame,
            text="Comma (,) - Brazilian format (e.g., 100,50)",
            variable=self.parent.decimal_separator,
            value=','
        ).pack(anchor=tk.W, pady=2)

        # Store reference for testing
        self._widgets['decimal_frame'] = decimal_frame

        # Information text (gray, wrapped)
        info_text = (
            "These settings determine how the CSV file is parsed.\n"
            "Common combinations:\n"
            "- Standard: Comma delimiter + Dot decimal (1,234.56)\n"
            "- Brazilian: Semicolon delimiter + Comma decimal (1.234,56)"
        )
        ttk.Label(
            self.container,
            text=info_text,
            font=('Arial', 9),
            foreground='gray',
            wraplength=600,
            justify=tk.LEFT
        ).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=20)

    def _configure_layout(self):
        """
        Configure responsive grid layout.

        Makes both columns expandable to ensure proper spacing,
        with the second column (containing radio button frames) having more weight.
        """
        if self.container:
            self.container.columnconfigure(0, weight=0)  # Label column fixed
            self.container.columnconfigure(1, weight=1)  # Options column expandable

    def _collect_data(self) -> Dict[str, Any]:
        """
        Collect CSV format data from UI.

        Retrieves the current values of the delimiter and decimal_separator
        StringVars from the parent.

        Returns:
            Dictionary containing:
                - delimiter: Selected column delimiter (str: ',', ';', or '\t')
                - decimal_separator: Selected decimal separator (str: '.' or ',')

        Example:
            >>> data = step._collect_data()
            >>> print(data)
            {'delimiter': ';', 'decimal_separator': ','}
        """
        return {
            'delimiter': self.parent.delimiter.get(),
            'decimal_separator': self.parent.decimal_separator.get()
        }

    def _validate_data(self, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Validate CSV format data.

        This step always returns valid because the parent provides default values
        for both delimiter and decimal_separator. The radio buttons ensure a valid
        selection is always present.

        Args:
            data: Data dictionary from _collect_data() containing 'delimiter'
                  and 'decimal_separator' keys

        Returns:
            Tuple of (is_valid, error_message):
                - is_valid: Always True (defaults are always valid)
                - error_message: Always None (no validation errors possible)

        Example:
            >>> data = {'delimiter': ';', 'decimal_separator': ','}
            >>> is_valid, error = step._validate_data(data)
            >>> assert is_valid is True
            >>> assert error is None
        """
        # Always valid - defaults are always provided by parent
        return True, None
