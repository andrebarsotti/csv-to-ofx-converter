"""
file_selection_step.py - File Selection Step (Step 1)

This module implements the file selection step for the CSV to OFX Converter wizard.
Users select a CSV file to convert using a file browser dialog.

Classes:
    FileSelectionStep: Step 1 implementation for CSV file selection
"""

import tkinter as tk
from tkinter import ttk, filedialog
from typing import Dict, Any, Tuple, Optional

from src.gui_wizard_step import WizardStep, StepConfig
from src import gui_utils


class FileSelectionStep(WizardStep):
    """
    Step 1: Select CSV file for conversion.

    This step allows users to select a CSV file using a file browser dialog.
    The selected file path is displayed in a read-only entry widget and validated
    before allowing progression to the next step.

    UI Elements:
        - Description label explaining the step purpose
        - File path label and read-only entry showing selected file
        - Browse button to open file dialog
        - Information text about supported formats

    Data Collected:
        - csv_file: Path to the selected CSV file

    Validation:
        - File path must not be empty
        - File must exist
        - File must be a valid file (not a directory)

    Example:
        >>> step = FileSelectionStep(parent_gui)
        >>> container = step.create(parent_frame)
        >>> step.show()
        >>> result = step.validate()
        >>> if result.is_valid:
        ...     print(f"Selected file: {result.data['csv_file']}")
    """

    def __init__(self, parent):
        """
        Initialize file selection step.

        Args:
            parent: Parent wizard orchestrator (ConverterGUI instance)
        """
        config = StepConfig(
            step_number=0,
            step_name="File Selection",
            step_title="Step 1: Select CSV File"
        )
        super().__init__(parent, config)

    def _build_ui(self):
        """
        Build file selection UI elements.

        Creates and arranges the following widgets:
        - Description label at the top
        - File path label, entry, and browse button
        - Information text at the bottom

        All widgets are arranged using grid layout for proper alignment.
        """
        # Description label
        ttk.Label(
            self.container,
            text="Select a CSV file to convert to OFX format:",
            font=('Arial', 10)
        ).grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 20))

        # File path label (bold)
        ttk.Label(
            self.container,
            text="CSV File:",
            font=('Arial', 10, 'bold')
        ).grid(row=1, column=0, sticky=tk.W, padx=5, pady=10)

        # File path entry (read-only, bound to parent's csv_file StringVar)
        self._widgets['file_entry'] = ttk.Entry(
            self.container,
            textvariable=self.parent.csv_file,
            state='readonly',
            width=50
        )
        self._widgets['file_entry'].grid(
            row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=10
        )

        # Browse button
        self._widgets['browse_button'] = ttk.Button(
            self.container,
            text="Browse...",
            command=self._browse_file
        )
        self._widgets['browse_button'].grid(row=1, column=2, padx=5, pady=10)

        # Information text (gray, wrapped)
        info_text = (
            "Select a CSV file containing your bank transactions.\n"
            "The file should have a header row with column names.\n"
            "Supported formats: CSV with comma, semicolon, or tab delimiters."
        )
        ttk.Label(
            self.container,
            text=info_text,
            font=('Arial', 9),
            foreground='gray',
            wraplength=600,
            justify=tk.LEFT
        ).grid(row=2, column=0, columnspan=3, sticky=tk.W, pady=20)

    def _configure_layout(self):
        """
        Configure responsive grid layout.

        Makes the middle column (file entry) expandable so it grows
        with the window width, while keeping the browse button fixed size.
        """
        if self.container:
            self.container.columnconfigure(1, weight=1)

    def _browse_file(self):
        """
        Open file dialog to select CSV file.

        Displays a file dialog filtered to show CSV files by default.
        If a file is selected, updates the parent's csv_file StringVar
        and logs the selection.
        """
        filename = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            self.parent.csv_file.set(filename)
            self.log(f"Selected file: {filename}")

    def _collect_data(self) -> Dict[str, Any]:
        """
        Collect file selection data from UI.

        Retrieves the current value of the csv_file StringVar from the parent.

        Returns:
            Dictionary containing:
                - csv_file: Path to selected CSV file (str)

        Example:
            >>> data = step._collect_data()
            >>> print(data)
            {'csv_file': '/path/to/transactions.csv'}
        """
        return {
            'csv_file': self.parent.csv_file.get()
        }

    def _validate_data(self, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Validate file selection data.

        Uses gui_utils.validate_csv_file_selection() to check:
        - File path is not empty
        - File exists
        - Path points to a file (not a directory)

        Args:
            data: Data dictionary from _collect_data() containing 'csv_file' key

        Returns:
            Tuple of (is_valid, error_message):
                - is_valid: True if file is valid, False otherwise
                - error_message: User-friendly error message if invalid, None if valid

        Example:
            >>> data = {'csv_file': '/path/to/file.csv'}
            >>> is_valid, error = step._validate_data(data)
            >>> if not is_valid:
            ...     print(f"Error: {error}")
        """
        csv_file = data.get('csv_file', '')
        is_valid, error_msg = gui_utils.validate_csv_file_selection(csv_file)

        return is_valid, error_msg
