"""
data_preview_step.py - Data Preview Step (Step 3)

This module implements the data preview step for the CSV to OFX Converter wizard.
Users can view the first 100 rows of their CSV data and reload the data if needed.

Classes:
    DataPreviewStep: Step 3 implementation for CSV data preview
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Tuple, Optional

from src.gui_wizard_step import WizardStep, StepConfig
from src.csv_parser import CSVParser
from src import gui_utils


class DataPreviewStep(WizardStep):
    """
    Step 3: Preview CSV data with reload functionality.

    This step loads the CSV file using the selected format (delimiter and decimal
    separator) and displays the first 100 rows in a Treeview widget for preview.
    Users can reload the data if they change the CSV format settings.

    UI Elements:
        - Info label and reload button
        - Treeview widget with vertical and horizontal scrollbars
        - Statistics label showing row count and columns

    Data Collected:
        - csv_headers: List of CSV column headers
        - csv_data: List of dictionaries containing CSV rows
        - reload_requested: Boolean indicating if user requested reload

    Validation:
        - CSV data must be loaded successfully
        - At least 1 row of data required

    Example:
        >>> step = DataPreviewStep(parent_gui)
        >>> container = step.create(parent_frame)
        >>> step.show()
        >>> result = step.validate()
        >>> if result.is_valid:
        ...     print(f"Loaded {len(result.data['csv_data'])} rows")
    """

    def __init__(self, parent):
        """
        Initialize DataPreviewStep.

        Args:
            parent: Parent wizard orchestrator (ConverterGUI)
        """
        config = StepConfig(
            step_number=2,
            step_name="Data Preview",
            step_title="Step 3: Preview CSV Data"
        )
        super().__init__(parent, config)
        self._reload_requested = False

    def _build_ui(self):
        """
        Build data preview UI.

        Creates a Treeview with scrollbars to display CSV data preview,
        a reload button, and statistics label.
        """
        # Info frame with label and reload button
        info_frame = ttk.Frame(self.container)
        info_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        info_frame.columnconfigure(1, weight=1)

        ttk.Label(
            info_frame,
            text="Preview of your CSV data:",
            font=('Arial', 10)
        ).grid(row=0, column=0, sticky=tk.W)

        # Reload button
        ttk.Button(
            info_frame,
            text="Reload Data",
            command=self._on_reload_clicked
        ).grid(row=0, column=1, sticky=tk.E, padx=5)

        # Tree frame with scrollbars
        tree_frame = ttk.Frame(self.container)
        tree_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)

        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")

        # Treeview widget
        self._widgets['preview_tree'] = ttk.Treeview(
            tree_frame,
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set
        )
        vsb.configure(command=self._widgets['preview_tree'].yview)
        hsb.configure(command=self._widgets['preview_tree'].xview)

        self._widgets['preview_tree'].grid(
            row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S)
        )
        vsb.grid(row=0, column=1, sticky=(tk.N, tk.S))
        hsb.grid(row=1, column=0, sticky=(tk.W, tk.E))

        # Statistics label
        self._widgets['stats_label'] = ttk.Label(
            self.container,
            text="",
            font=('Arial', 9)
        )
        self._widgets['stats_label'].grid(
            row=2, column=0, sticky=tk.W, pady=(10, 0)
        )

        # Make preview_tree available to parent for compatibility
        self.parent.preview_tree = self._widgets['preview_tree']
        self.parent.preview_stats_label = self._widgets['stats_label']

    def _configure_layout(self):
        """Configure responsive layout for data preview."""
        if self.container:
            self.container.columnconfigure(0, weight=1)
            self.container.rowconfigure(1, weight=1)

    def show(self):
        """
        Show this step and load CSV data if not already loaded.

        Automatically loads CSV data on first display or if reload was requested.
        """
        super().show()

        # Load data if not already loaded or if reload requested
        csv_data = self.get_parent_data('csv_data', [])
        if not csv_data or self._reload_requested:
            try:
                self._load_csv_data(force_reload=self._reload_requested)
                self._reload_requested = False
            except Exception as e:
                self.log(f"Error loading CSV: {e}")
                # Don't raise - allow user to fix and reload
        else:
            # Data already loaded, just populate preview
            self._populate_preview()

    def _on_reload_clicked(self):
        """Handle reload button click."""
        self._reload_requested = True
        try:
            self._load_csv_data(force_reload=True)
            self._reload_requested = False
            self.log("CSV data reloaded successfully")
        except Exception as e:
            self.log(f"Error reloading CSV: {e}")

    def _load_csv_data(self, force_reload: bool = False):
        """
        Load CSV data using selected format.

        Args:
            force_reload: If True, reload data even if already loaded

        Raises:
            ValueError: If no CSV file is selected
            Exception: If CSV parsing fails
        """
        # Check if already loaded and not forcing reload
        csv_data = self.get_parent_data('csv_data', [])
        if csv_data and not force_reload:
            return

        # Get CSV file path
        csv_file = self.get_parent_data('csv_file', '')
        if not csv_file:
            raise ValueError("No CSV file selected")

        self.log("Loading CSV data...")

        # Create parser with selected format
        delimiter = self.get_parent_data('delimiter', ',')
        decimal_separator = self.get_parent_data('decimal_separator', '.')

        parser = CSVParser(
            delimiter=delimiter,
            decimal_separator=decimal_separator
        )

        # Parse file
        csv_headers, csv_data = parser.parse_file(csv_file)

        # Update parent data
        self.set_parent_data('csv_headers', csv_headers)
        self.set_parent_data('csv_data', csv_data)

        # Also set directly for compatibility
        self.parent.csv_headers = csv_headers
        self.parent.csv_data = csv_data

        self.log(
            f"CSV loaded: {len(csv_data)} rows, {len(csv_headers)} columns"
        )

        # Populate preview
        self._populate_preview()

    def _populate_preview(self):
        """
        Populate the preview treeview with CSV data.

        Displays the first 100 rows for performance. Shows statistics about
        total rows and columns.
        """
        preview_tree = self._widgets.get('preview_tree')
        stats_label = self._widgets.get('stats_label')

        if not preview_tree or not stats_label:
            return

        # Clear existing items
        for item in preview_tree.get_children():
            preview_tree.delete(item)

        # Get data from parent
        csv_headers = self.get_parent_data('csv_headers', [])
        csv_data = self.get_parent_data('csv_data', [])

        if not csv_data:
            return

        # Configure columns
        preview_tree['columns'] = csv_headers
        preview_tree['show'] = 'headings'

        # Set column headings and widths
        for col in csv_headers:
            preview_tree.heading(col, text=col)
            preview_tree.column(col, width=120, anchor=tk.W)

        # Add data rows (limit to first 100 for performance)
        max_rows = min(100, len(csv_data))
        for row in csv_data[:max_rows]:
            values = [row.get(col, '') for col in csv_headers]
            preview_tree.insert('', tk.END, values=values)

        # Update statistics label
        stats_text = gui_utils.format_preview_stats(
            max_rows, len(csv_data), max_preview=100
        )
        stats_label.configure(text=stats_text)

    def _collect_data(self) -> Dict[str, Any]:
        """
        Collect data from data preview step.

        Returns:
            Dictionary containing csv_headers, csv_data, and reload flag
        """
        return {
            'csv_headers': self.get_parent_data('csv_headers', []),
            'csv_data': self.get_parent_data('csv_data', []),
            'reload_requested': self._reload_requested
        }

    def _validate_data(self, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Validate that CSV data was loaded successfully.

        Args:
            data: Data collected from UI

        Returns:
            Tuple of (is_valid, error_message)
        """
        csv_data = data.get('csv_data', [])

        if not csv_data:
            return False, (
                "No CSV data loaded. Please ensure a valid CSV file is selected "
                "and click 'Reload Data' if needed."
            )

        if len(csv_data) < 1:
            return False, "CSV file must contain at least one row of data."

        return True, None
