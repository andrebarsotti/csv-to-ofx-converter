"""
ofx_config_step.py - OFX Configuration Step (Step 4)

This module implements the OFX configuration step for the CSV to OFX Converter wizard.
Users configure account ID, bank name, and currency for the OFX output file.

Classes:
    OFXConfigStep: Step 4 implementation for OFX configuration
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Tuple, Optional

from src.gui_wizard_step import WizardStep, StepConfig


class OFXConfigStep(WizardStep):
    """
    Step 4: Configure OFX output file settings.

    This step allows users to configure the OFX output file by specifying:
    - Account ID (optional, defaults to 'UNKNOWN')
    - Bank name (optional, defaults to 'CSV Import')
    - Currency (BRL, USD, EUR, or GBP)

    All fields have default values, so this step is always valid.

    UI Elements:
        - Description label explaining the step purpose
        - Account ID entry with label and help text
        - Bank name entry with label and help text
        - Currency combobox with label and help text
        - Information text about default values

    Data Collected:
        - account_id: Account identifier (str)
        - bank_name: Bank or institution name (str)
        - currency: Currency code (str: 'BRL', 'USD', 'EUR', or 'GBP')

    Validation:
        - Always valid since defaults are always provided by parent

    Example:
        >>> step = OFXConfigStep(parent_gui)
        >>> container = step.create(parent_frame)
        >>> step.show()
        >>> result = step.validate()
        >>> print(f"Account: {result.data['account_id']}")
        >>> print(f"Bank: {result.data['bank_name']}")
        >>> print(f"Currency: {result.data['currency']}")
    """

    def __init__(self, parent):
        """
        Initialize OFX configuration step.

        Args:
            parent: Parent wizard orchestrator (ConverterGUI instance)
        """
        config = StepConfig(
            step_number=3,
            step_name="OFX Configuration",
            step_title="Step 4: OFX Configuration"
        )
        super().__init__(parent, config)

    def _build_ui(self):
        """
        Build OFX configuration UI elements.

        Creates and arranges the following widgets:
        - Description label at the top
        - Account ID section with label, entry, and help text
        - Bank name section with label, entry, and help text
        - Currency section with label, combobox, and help text

        All widgets are arranged using grid layout for proper alignment.
        Entry widgets and combobox are bound to parent's StringVars.
        """
        # Description label
        ttk.Label(
            self.container,
            text="Configure the OFX output file settings:",
            font=('Arial', 10)
        ).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 20))

        # Account ID section
        ttk.Label(
            self.container,
            text="Account ID:",
            font=('Arial', 10, 'bold')
        ).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)

        self._widgets['account_id_entry'] = ttk.Entry(
            self.container,
            textvariable=self.parent.account_id,
            width=40
        )
        self._widgets['account_id_entry'].grid(
            row=1, column=1, sticky=tk.W, padx=5, pady=5
        )

        ttk.Label(
            self.container,
            text="(Optional - Default: 'UNKNOWN')",
            font=('Arial', 8),
            foreground='gray'
        ).grid(row=2, column=1, sticky=tk.W, padx=5)

        # Bank Name section
        ttk.Label(
            self.container,
            text="Bank Name:",
            font=('Arial', 10, 'bold')
        ).grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)

        self._widgets['bank_name_entry'] = ttk.Entry(
            self.container,
            textvariable=self.parent.bank_name,
            width=40
        )
        self._widgets['bank_name_entry'].grid(
            row=3, column=1, sticky=tk.W, padx=5, pady=5
        )

        ttk.Label(
            self.container,
            text="(Optional - Default: 'CSV Import')",
            font=('Arial', 8),
            foreground='gray'
        ).grid(row=4, column=1, sticky=tk.W, padx=5)

        # Currency section
        ttk.Label(
            self.container,
            text="Currency:",
            font=('Arial', 10, 'bold')
        ).grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)

        self._widgets['currency_combo'] = ttk.Combobox(
            self.container,
            textvariable=self.parent.currency,
            values=['BRL', 'USD', 'EUR', 'GBP'],
            state='readonly',
            width=10
        )
        self._widgets['currency_combo'].grid(
            row=5, column=1, sticky=tk.W, padx=5, pady=5
        )

        ttk.Label(
            self.container,
            text="(BRL=Brazilian Real, USD=US Dollar, EUR=Euro, GBP=British Pound)",
            font=('Arial', 8),
            foreground='gray'
        ).grid(row=6, column=1, sticky=tk.W, padx=5)

    def _configure_layout(self):
        """
        Configure responsive grid layout.

        Makes the second column (containing entry widgets and combobox) expandable
        to ensure proper spacing, while keeping the first column (labels) fixed width.
        """
        if self.container:
            self.container.columnconfigure(0, weight=0)  # Label column fixed
            self.container.columnconfigure(1, weight=1)  # Input column expandable

    def _collect_data(self) -> Dict[str, Any]:
        """
        Collect OFX configuration data from UI.

        Retrieves the current values of the account_id, bank_name, and currency
        StringVars from the parent.

        Returns:
            Dictionary containing:
                - account_id: Account identifier (str)
                - bank_name: Bank or institution name (str)
                - currency: Currency code (str: 'BRL', 'USD', 'EUR', or 'GBP')

        Example:
            >>> data = step._collect_data()
            >>> print(data)
            {'account_id': '1234567890', 'bank_name': 'My Bank', 'currency': 'BRL'}
        """
        return {
            'account_id': self.parent.account_id.get(),
            'bank_name': self.parent.bank_name.get(),
            'currency': self.parent.currency.get()
        }

    def _validate_data(self, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Validate OFX configuration data.

        This step always returns valid because the parent provides default values
        for all fields (account_id defaults to 'UNKNOWN', bank_name defaults to
        'CSV Import', currency defaults to 'BRL'). The entry widgets and combobox
        ensure valid selections are always present.

        Args:
            data: Data dictionary from _collect_data() containing 'account_id',
                  'bank_name', and 'currency' keys

        Returns:
            Tuple of (is_valid, error_message):
                - is_valid: Always True (defaults are always valid)
                - error_message: Always None (no validation errors possible)

        Example:
            >>> data = {'account_id': '1234', 'bank_name': 'Bank', 'currency': 'USD'}
            >>> is_valid, error = step._validate_data(data)
            >>> assert is_valid is True
            >>> assert error is None
        """
        # Always valid - defaults are always provided by parent
        return True, None
