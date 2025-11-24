"""
advanced_options_step.py - Advanced Options Step (Step 6)

This module implements the advanced options step for the CSV to OFX Converter wizard.
Users can configure value inversion and date validation features.

Classes:
    AdvancedOptionsStep: Step 6 implementation for advanced options configuration
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Tuple, Optional

from src.gui_wizard_step import WizardStep, StepConfig
from src import gui_utils


class AdvancedOptionsStep(WizardStep):
    """
    Step 6: Configure advanced options (value inversion and date validation).

    This step allows users to configure optional advanced features:
    - Value inversion: Swap debits and credits (multiply by -1)
    - Date validation: Validate transactions against a statement period

    UI Elements:
        - Checkbox: Invert transaction values
        - Checkbox: Enable date validation
        - Entry: Start date (DD/MM/YYYY format, enabled when validation is on)
        - Entry: End date (DD/MM/YYYY format, enabled when validation is on)
        - Help text labels for each option

    Data Collected:
        - invert_values: Boolean indicating if values should be inverted
        - enable_date_validation: Boolean indicating if date validation is enabled
        - start_date: Start date string (DD/MM/YYYY)
        - end_date: End date string (DD/MM/YYYY)

    Validation:
        - If date validation is enabled, validates date range inputs
        - If date validation is disabled, always valid

    Example:
        >>> step = AdvancedOptionsStep(parent_gui)
        >>> container = step.create(parent_frame)
        >>> step.show()
        >>> result = step.validate()
        >>> if result.is_valid:
        ...     print(f"Invert values: {result.data['invert_values']}")
    """

    def __init__(self, parent):
        """
        Initialize AdvancedOptionsStep.

        Args:
            parent: Parent wizard orchestrator (ConverterGUI)
        """
        config = StepConfig(
            step_number=5,
            step_name="Advanced Options",
            step_title="Step 6: Advanced Options"
        )
        super().__init__(parent, config)

    def _build_ui(self):
        """
        Build advanced options UI.

        Creates checkboxes for value inversion and date validation,
        date entry fields with auto-formatting, and help text.
        """
        # Main description
        ttk.Label(
            self.container,
            text="Configure optional advanced features:",
            font=('Arial', 10)
        ).grid(row=0, column=0, sticky=tk.W, pady=(0, 20))

        # Value Inversion Section
        self._create_value_inversion_section()

        # Date Validation Section
        self._create_date_validation_section()

        # Ready message
        ttk.Label(
            self.container,
            text="[OK] Configuration complete! Click 'Next' to preview balances.",
            font=('Arial', 10, 'bold'),
            foreground='green'
        ).grid(row=3, column=0, sticky=tk.W, pady=(20, 0))

    def _create_value_inversion_section(self):
        """Create the value inversion section with checkbox and help text."""
        inversion_frame = ttk.LabelFrame(
            self.container,
            text="Value Inversion",
            padding="10"
        )
        inversion_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=10)

        # Get or create invert_values variable
        invert_values_var = self.get_parent_data('invert_values')
        if invert_values_var is None:
            # Create variable if it doesn't exist
            invert_values_var = tk.BooleanVar(value=False)
            if hasattr(self.parent, 'invert_values'):
                self.parent.invert_values = invert_values_var
            else:
                # Store in parent if attribute doesn't exist
                setattr(self.parent, 'invert_values', invert_values_var)

        # Checkbox
        ttk.Checkbutton(
            inversion_frame,
            text="Invert all transaction values (swap debits and credits)",
            variable=invert_values_var
        ).pack(anchor=tk.W, pady=5)

        # Help text
        ttk.Label(
            inversion_frame,
            text="Use this if your CSV shows debits as positive and credits as negative,\n"
                 "or vice versa. This will multiply all amounts by -1.",
            font=('Arial', 8),
            foreground='gray'
        ).pack(anchor=tk.W, pady=5)

        # Store reference
        self._widgets['invert_values_var'] = invert_values_var

    def _create_date_validation_section(self):
        """Create the date validation section with checkbox and date entries."""
        validation_frame = ttk.LabelFrame(
            self.container,
            text="Transaction Date Validation",
            padding="10"
        )
        validation_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=10)
        validation_frame.columnconfigure(1, weight=1)

        # Get or create variables
        enable_date_validation_var = self._get_or_create_parent_var(
            'enable_date_validation', tk.BooleanVar, False
        )
        start_date_var = self._get_or_create_parent_var(
            'start_date', tk.StringVar, ''
        )
        end_date_var = self._get_or_create_parent_var(
            'end_date', tk.StringVar, ''
        )

        # Checkbox
        ttk.Checkbutton(
            validation_frame,
            text="Enable date validation for credit card statement period",
            variable=enable_date_validation_var,
            command=self._toggle_date_inputs
        ).grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=5)

        # Start date label and entry
        ttk.Label(
            validation_frame,
            text="Start Date:"
        ).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)

        self._widgets['start_date_entry'] = ttk.Entry(
            validation_frame,
            textvariable=start_date_var,
            state='disabled',
            width=20
        )
        self._widgets['start_date_entry'].grid(
            row=1, column=1, sticky=tk.W, padx=5, pady=5
        )

        # Bind auto-formatting for start date
        self._widgets['start_date_entry'].bind(
            '<KeyRelease>',
            lambda e: self._format_date_entry(self._widgets['start_date_entry'])
        )

        ttk.Label(
            validation_frame,
            text="(Format: DD/MM/YYYY, e.g., 01/10/2025)",
            font=('Arial', 8),
            foreground='gray'
        ).grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)

        # End date label and entry
        ttk.Label(
            validation_frame,
            text="End Date:"
        ).grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)

        self._widgets['end_date_entry'] = ttk.Entry(
            validation_frame,
            textvariable=end_date_var,
            state='disabled',
            width=20
        )
        self._widgets['end_date_entry'].grid(
            row=2, column=1, sticky=tk.W, padx=5, pady=5
        )

        # Bind auto-formatting for end date
        self._widgets['end_date_entry'].bind(
            '<KeyRelease>',
            lambda e: self._format_date_entry(self._widgets['end_date_entry'])
        )

        ttk.Label(
            validation_frame,
            text="(Format: DD/MM/YYYY, e.g., 31/10/2025)",
            font=('Arial', 8),
            foreground='gray'
        ).grid(row=2, column=2, sticky=tk.W, padx=5, pady=5)

        # Help text
        ttk.Label(
            validation_frame,
            text="When enabled, transactions outside the date range will prompt you to:\n"
                 "- Keep the original date\n"
                 "- Adjust to the nearest boundary (start or end date)\n"
                 "- Exclude the transaction from the OFX file",
            font=('Arial', 8),
            foreground='gray'
        ).grid(row=3, column=0, columnspan=3, sticky=tk.W, pady=10)

        # Store references
        self._widgets['enable_date_validation_var'] = enable_date_validation_var
        self._widgets['start_date_var'] = start_date_var
        self._widgets['end_date_var'] = end_date_var

        # Also make entries available to parent for compatibility
        if hasattr(self.parent, 'start_date_entry'):
            self.parent.start_date_entry = self._widgets['start_date_entry']
        if hasattr(self.parent, 'end_date_entry'):
            self.parent.end_date_entry = self._widgets['end_date_entry']

    def _get_or_create_parent_var(self, var_name: str, var_type, default_value):
        """
        Get or create a Tkinter variable in parent.

        Args:
            var_name: Name of the variable attribute
            var_type: Tkinter variable type (tk.BooleanVar, tk.StringVar, etc.)
            default_value: Default value if creating new variable

        Returns:
            The variable from parent or newly created variable
        """
        if hasattr(self.parent, var_name):
            return getattr(self.parent, var_name)
        else:
            # Create new variable and store in parent
            new_var = var_type(value=default_value)
            setattr(self.parent, var_name, new_var)
            return new_var

    def _toggle_date_inputs(self):
        """Enable or disable date input fields based on checkbox state."""
        enable_date_validation_var = self._widgets.get('enable_date_validation_var')
        start_date_entry = self._widgets.get('start_date_entry')
        end_date_entry = self._widgets.get('end_date_entry')

        if not enable_date_validation_var or not start_date_entry or not end_date_entry:
            return

        # Enable or disable based on checkbox value
        if enable_date_validation_var.get():
            start_date_entry.configure(state='normal')
            end_date_entry.configure(state='normal')
        else:
            start_date_entry.configure(state='disabled')
            end_date_entry.configure(state='disabled')

    def _format_date_entry(self, entry_widget):
        """
        Auto-format date input with slashes in DD/MM/YYYY format.

        Uses gui_utils for formatting and maintains cursor position.

        Args:
            entry_widget: ttk.Entry widget to format
        """
        # Get current value and cursor position
        current_value = entry_widget.get()
        cursor_pos = entry_widget.index(tk.INSERT)

        # Use gui_utils to format the date string
        formatted = gui_utils.format_date_string(current_value)

        # Only update if different
        if formatted != current_value:
            # Calculate new cursor position using gui_utils
            new_cursor_pos = gui_utils.calculate_cursor_position_after_format(
                current_value, formatted, cursor_pos
            )

            # Update entry value
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, formatted)

            # Restore cursor position
            entry_widget.icursor(new_cursor_pos)

    def show(self):
        """
        Show this step and restore date input field states.

        Ensures date entry fields are enabled/disabled based on checkbox value.
        """
        super().show()
        # Restore the correct state of date entry fields
        self._toggle_date_inputs()

    def _collect_data(self) -> Dict[str, Any]:
        """
        Collect data from advanced options step.

        Returns:
            Dictionary containing invert_values, enable_date_validation,
            start_date, and end_date
        """
        return {
            'invert_values': self.get_parent_data('invert_values', False),
            'enable_date_validation': self.get_parent_data('enable_date_validation', False),
            'start_date': self.get_parent_data('start_date', ''),
            'end_date': self.get_parent_data('end_date', '')
        }

    def _validate_data(self, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Validate advanced options data.

        If date validation is enabled, validates date range inputs.
        If date validation is disabled, always valid.

        Args:
            data: Data collected from UI

        Returns:
            Tuple of (is_valid, error_message)
        """
        enable_date_validation = data.get('enable_date_validation', False)

        # If date validation is disabled, no validation needed
        if not enable_date_validation:
            return True, None

        # If date validation is enabled, validate date range
        start_date = data.get('start_date', '')
        end_date = data.get('end_date', '')

        is_valid, error_msg = gui_utils.validate_date_range_inputs(start_date, end_date)
        return is_valid, error_msg
