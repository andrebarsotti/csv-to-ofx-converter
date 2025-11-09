"""
Converter GUI Module
===================
Graphical User Interface for CSV to OFX conversion with step-by-step wizard.

Provides an intuitive multi-step interface for:
- Loading CSV files
- Previewing CSV data
- Mapping CSV columns to OFX fields
- Creating composite descriptions
- Configuring CSV format (delimiter, decimal separator)
- Converting and saving OFX files

Author: Generated for Brazilian banking compatibility
License: MIT
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import logging
from datetime import datetime
from typing import List, Dict, Tuple, Optional

from .constants import NOT_MAPPED, NOT_SELECTED
from .csv_parser import CSVParser
from .ofx_generator import OFXGenerator
from .date_validator import DateValidator

logger = logging.getLogger(__name__)
class ConverterGUI:
    """
    Graphical User Interface for CSV to OFX conversion with step-by-step wizard.

    Provides an intuitive multi-step interface for:
    - Loading CSV files
    - Previewing CSV data
    - Mapping CSV columns to OFX fields
    - Creating composite descriptions
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
        self.root.title("CSV to OFX Converter - Enhanced Edition")
        self.root.geometry("1000x850")

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
        self.invert_values = tk.BooleanVar(value=False)

        # Composite description variables
        self.description_columns = []  # List of selected column variables
        self.description_separator = tk.StringVar(value=' ')

        # Data
        self.csv_headers: List[str] = []
        self.csv_data: List[Dict[str, str]] = []
        self.field_mappings: Dict[str, tk.StringVar] = {}

        # Wizard steps
        self.current_step = 0
        self.steps = [
            "File Selection",
            "CSV Format",
            "Data Preview",
            "OFX Configuration",
            "Field Mapping",
            "Advanced Options"
        ]

        # Build UI
        self._create_widgets()

        logger.info("GUI initialized with wizard interface")

    def _create_widgets(self):
        """Create all GUI widgets."""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)

        # Title
        title_label = ttk.Label(main_frame, text="CSV to OFX Converter - Enhanced Edition",
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, pady=(0, 10))

        # Progress indicator
        self._create_progress_indicator(main_frame, row=1)

        # Step container
        self.step_container = ttk.Frame(main_frame)
        self.step_container.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        self.step_container.columnconfigure(0, weight=1)
        self.step_container.rowconfigure(0, weight=1)

        # Navigation buttons
        self._create_navigation_buttons(main_frame, row=3)

        # Log section
        self._create_log_section(main_frame, row=4)

        # Show first step
        self._show_step(0)

    def _create_progress_indicator(self, parent: ttk.Frame, row: int):
        """Create progress indicator showing current step."""
        self.progress_frame = ttk.Frame(parent)
        self.progress_frame.grid(row=row, column=0, pady=10)

        self.step_labels = []
        for idx, step_name in enumerate(self.steps):
            # Step number/indicator
            indicator = ttk.Label(
                self.progress_frame,
                text=str(idx + 1),
                width=3,
                font=('Arial', 10, 'bold'),
                relief='solid',
                borderwidth=1,
                padding=5
            )
            indicator.grid(row=0, column=idx * 2, padx=2)

            # Step name
            label = ttk.Label(
                self.progress_frame,
                text=step_name,
                font=('Arial', 8)
            )
            label.grid(row=1, column=idx * 2, padx=2)

            self.step_labels.append((indicator, label))

            # Arrow (except after last step)
            if idx < len(self.steps) - 1:
                arrow = ttk.Label(self.progress_frame, text=">", font=('Arial', 12))
                arrow.grid(row=0, column=idx * 2 + 1, padx=5)

    def _update_progress_indicator(self):
        """Update progress indicator to highlight current step."""
        for idx, (indicator, label) in enumerate(self.step_labels):
            if idx == self.current_step:
                indicator.configure(background='#4CAF50', foreground='white')
                label.configure(font=('Arial', 8, 'bold'))
            elif idx < self.current_step:
                indicator.configure(background='#E0E0E0')
                label.configure(font=('Arial', 8))
            else:
                indicator.configure(background='white')
                label.configure(font=('Arial', 8))

    def _create_navigation_buttons(self, parent: ttk.Frame, row: int):
        """Create navigation buttons."""
        nav_frame = ttk.Frame(parent)
        nav_frame.grid(row=row, column=0, pady=10)

        self.back_btn = ttk.Button(nav_frame, text="< Back", command=self._go_back)
        self.back_btn.pack(side=tk.LEFT, padx=5)

        self.next_btn = ttk.Button(nav_frame, text="Next >", command=self._go_next)
        self.next_btn.pack(side=tk.LEFT, padx=5)

        self.convert_btn = ttk.Button(nav_frame, text="Convert to OFX", command=self._convert)
        self.convert_btn.pack(side=tk.LEFT, padx=5)
        self.convert_btn.pack_forget()  # Hidden initially

        ttk.Button(nav_frame, text="Clear All", command=self._clear).pack(side=tk.LEFT, padx=5)

    def _create_log_section(self, parent: ttk.Frame, row: int):
        """Create log display section."""
        frame = ttk.LabelFrame(parent, text="Activity Log", padding="5")
        frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=5)
        frame.columnconfigure(0, weight=1)

        self.log_text = scrolledtext.ScrolledText(frame, height=6, state='disabled')
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E))

    def _show_step(self, step_num: int):
        """Show the specified step."""
        # Clear current step container
        for widget in self.step_container.winfo_children():
            widget.destroy()

        # Update current step
        self.current_step = step_num
        self._update_progress_indicator()

        # Create step content
        if step_num == 0:
            self._create_step_file_selection()
        elif step_num == 1:
            self._create_step_csv_format()
        elif step_num == 2:
            self._create_step_data_preview()
        elif step_num == 3:
            self._create_step_ofx_config()
        elif step_num == 4:
            self._create_step_field_mapping()
        elif step_num == 5:
            self._create_step_advanced_options()

        # Update navigation buttons
        self._update_navigation_buttons()

    def _update_navigation_buttons(self):
        """Update navigation button states."""
        # Back button
        if self.current_step == 0:
            self.back_btn.configure(state='disabled')
        else:
            self.back_btn.configure(state='normal')

        # Next button and Convert button
        if self.current_step < len(self.steps) - 1:
            self.next_btn.pack(side=tk.LEFT, padx=5)
            self.convert_btn.pack_forget()
        else:
            self.next_btn.pack_forget()
            self.convert_btn.pack(side=tk.LEFT, padx=5)

    def _go_back(self):
        """Go to previous step."""
        if self.current_step > 0:
            self._show_step(self.current_step - 1)

    def _go_next(self):
        """Go to next step."""
        # Validate current step before proceeding
        if not self._validate_current_step():
            return

        if self.current_step < len(self.steps) - 1:
            self._show_step(self.current_step + 1)

    def _validate_current_step(self) -> bool:
        """Validate current step before proceeding."""
        validators = {
            0: self._validate_file_selection,
            2: self._validate_data_preview,
            4: self._validate_field_mapping,
        }

        validator = validators.get(self.current_step)
        if validator:
            return validator()
        return True

    def _validate_file_selection(self) -> bool:
        """Validate file selection step."""
        if not self.csv_file.get():
            messagebox.showwarning("Required", "Please select a CSV file")
            return False
        return True

    def _validate_data_preview(self) -> bool:
        """Validate data preview step."""
        if not self.csv_data:
            try:
                self._load_csv_data()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load CSV:\n{e}")
                return False
        return True

    def _validate_field_mapping(self) -> bool:
        """Validate field mapping step."""
        if not self._validate_required_fields():
            return False
        if not self._validate_description_mapping():
            return False
        return True

    def _validate_required_fields(self) -> bool:
        """Validate required date and amount fields."""
        date_col = self.field_mappings.get('date')
        amount_col = self.field_mappings.get('amount')

        if not date_col or date_col.get() == NOT_MAPPED:
            messagebox.showwarning("Required", "Please map the Date field")
            return False
        if not amount_col or amount_col.get() == NOT_MAPPED:
            messagebox.showwarning("Required", "Please map the Amount field")
            return False
        return True

    def _validate_description_mapping(self) -> bool:
        """Validate description field or composite description."""
        desc_col = self.field_mappings.get('description')
        if not desc_col or desc_col.get() == NOT_MAPPED:
            if not any(var.get() != NOT_SELECTED for var in self.description_columns):
                messagebox.showwarning("Required",
                    "Please map the Description field or configure composite description")
                return False
        return True

    # ==================== STEP 1: FILE SELECTION ====================

    def _create_step_file_selection(self):
        """Create file selection step."""
        frame = ttk.LabelFrame(self.step_container, text="Step 1: Select CSV File", padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=20, pady=20)
        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text="Select a CSV file to convert to OFX format:",
                 font=('Arial', 10)).grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 20))

        ttk.Label(frame, text="CSV File:", font=('Arial', 10, 'bold')).grid(
            row=1, column=0, sticky=tk.W, padx=5, pady=10)

        ttk.Entry(frame, textvariable=self.csv_file, state='readonly', width=50).grid(
            row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=10)

        ttk.Button(frame, text="Browse...", command=self._browse_csv).grid(
            row=1, column=2, padx=5, pady=10)

        # Info text
        info_text = ("Select a CSV file containing your bank transactions.\n"
                    "The file should have a header row with column names.\n"
                    "Supported formats: CSV with comma, semicolon, or tab delimiters.")
        ttk.Label(frame, text=info_text, font=('Arial', 9), foreground='gray',
                 wraplength=600, justify=tk.LEFT).grid(
            row=2, column=0, columnspan=3, sticky=tk.W, pady=20)

    def _browse_csv(self):
        """Open file dialog to select CSV file."""
        filename = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            self.csv_file.set(filename)
            self._log(f"Selected file: {filename}")

    # ==================== STEP 2: CSV FORMAT ====================

    def _create_step_csv_format(self):
        """Create CSV format configuration step."""
        frame = ttk.LabelFrame(self.step_container, text="Step 2: Configure CSV Format", padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=20, pady=20)

        ttk.Label(frame, text="Select the format of your CSV file:",
                 font=('Arial', 10)).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 20))

        # Delimiter options
        ttk.Label(frame, text="Column Delimiter:", font=('Arial', 10, 'bold')).grid(
            row=1, column=0, sticky=tk.W, pady=10)

        delimiter_frame = ttk.Frame(frame)
        delimiter_frame.grid(row=1, column=1, sticky=tk.W, padx=20, pady=10)

        ttk.Radiobutton(delimiter_frame, text="Comma (,) - Standard format",
                       variable=self.delimiter, value=',').pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(delimiter_frame, text="Semicolon (;) - Common in Brazilian exports",
                       variable=self.delimiter, value=';').pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(delimiter_frame, text="Tab - Tab-separated values",
                       variable=self.delimiter, value='\t').pack(anchor=tk.W, pady=2)

        # Decimal separator options
        ttk.Label(frame, text="Decimal Separator:", font=('Arial', 10, 'bold')).grid(
            row=2, column=0, sticky=tk.W, pady=10)

        decimal_frame = ttk.Frame(frame)
        decimal_frame.grid(row=2, column=1, sticky=tk.W, padx=20, pady=10)

        ttk.Radiobutton(decimal_frame, text="Dot (.) - Standard format (e.g., 100.50)",
                       variable=self.decimal_separator, value='.').pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(decimal_frame, text="Comma (,) - Brazilian format (e.g., 100,50)",
                       variable=self.decimal_separator, value=',').pack(anchor=tk.W, pady=2)

        # Info text
        info_text = ("These settings determine how the CSV file is parsed.\n"
                    "Common combinations:\n"
                    "- Standard: Comma delimiter + Dot decimal (1,234.56)\n"
                    "- Brazilian: Semicolon delimiter + Comma decimal (1.234,56)")
        ttk.Label(frame, text=info_text, font=('Arial', 9), foreground='gray',
                 wraplength=600, justify=tk.LEFT).grid(
            row=3, column=0, columnspan=2, sticky=tk.W, pady=20)

    # ==================== STEP 3: DATA PREVIEW ====================

    def _create_step_data_preview(self):
        """Create data preview step."""
        frame = ttk.LabelFrame(self.step_container, text="Step 3: Preview CSV Data", padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=20, pady=20)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)

        # Info label
        info_frame = ttk.Frame(frame)
        info_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        info_frame.columnconfigure(1, weight=1)

        ttk.Label(info_frame, text="Preview of your CSV data:",
                 font=('Arial', 10)).grid(row=0, column=0, sticky=tk.W)

        # Load button
        ttk.Button(info_frame, text="Reload Data",
                  command=lambda: self._load_csv_data(force_reload=True)).grid(
            row=0, column=1, sticky=tk.E, padx=5)

        # Create treeview for data preview
        tree_frame = ttk.Frame(frame)
        tree_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)

        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")

        self.preview_tree = ttk.Treeview(tree_frame,
                                         yscrollcommand=vsb.set,
                                         xscrollcommand=hsb.set)
        vsb.configure(command=self.preview_tree.yview)
        hsb.configure(command=self.preview_tree.xview)

        self.preview_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        vsb.grid(row=0, column=1, sticky=(tk.N, tk.S))
        hsb.grid(row=1, column=0, sticky=(tk.W, tk.E))

        # Stats label
        self.preview_stats_label = ttk.Label(frame, text="", font=('Arial', 9))
        self.preview_stats_label.grid(row=2, column=0, sticky=tk.W, pady=(10, 0))

        # Load data if not already loaded
        if not self.csv_data:
            try:
                self._load_csv_data()
            except Exception as e:
                self._log(f"Error loading CSV: {e}")
        else:
            self._populate_preview()

    def _load_csv_data(self, force_reload: bool = False):
        """Load CSV data."""
        if self.csv_data and not force_reload:
            return

        if not self.csv_file.get():
            raise ValueError("No CSV file selected")

        self._log("Loading CSV data...")

        # Create parser with selected format
        parser = CSVParser(
            delimiter=self.delimiter.get(),
            decimal_separator=self.decimal_separator.get()
        )

        # Parse file
        self.csv_headers, self.csv_data = parser.parse_file(self.csv_file.get())

        self._log(f"CSV loaded: {len(self.csv_data)} rows, {len(self.csv_headers)} columns")

        # Update preview if on preview step
        if self.current_step == 2:
            self._populate_preview()

    def _populate_preview(self):
        """Populate the preview treeview with CSV data."""
        # Clear existing items
        for item in self.preview_tree.get_children():
            self.preview_tree.delete(item)

        if not self.csv_data:
            return

        # Configure columns
        self.preview_tree['columns'] = self.csv_headers
        self.preview_tree['show'] = 'headings'

        # Set column headings and widths
        for col in self.csv_headers:
            self.preview_tree.heading(col, text=col)
            self.preview_tree.column(col, width=120, anchor=tk.W)

        # Add data rows (limit to first 100 for performance)
        max_rows = min(100, len(self.csv_data))
        for row in self.csv_data[:max_rows]:
            values = [row.get(col, '') for col in self.csv_headers]
            self.preview_tree.insert('', tk.END, values=values)

        # Update stats
        stats_text = f"Showing {max_rows} of {len(self.csv_data)} rows"
        if len(self.csv_data) > max_rows:
            stats_text += f" (limited to first {max_rows} for preview)"
        self.preview_stats_label.configure(text=stats_text)

    # ==================== STEP 4: OFX CONFIGURATION ====================

    def _create_step_ofx_config(self):
        """Create OFX configuration step."""
        frame = ttk.LabelFrame(self.step_container, text="Step 4: OFX Configuration", padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=20, pady=20)
        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text="Configure the OFX output file settings:",
                 font=('Arial', 10)).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 20))

        # Account ID
        ttk.Label(frame, text="Account ID:", font=('Arial', 10, 'bold')).grid(
            row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.account_id, width=40).grid(
            row=1, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Label(frame, text="(Optional - Default: 'UNKNOWN')",
                 font=('Arial', 8), foreground='gray').grid(
            row=2, column=1, sticky=tk.W, padx=5)

        # Bank Name
        ttk.Label(frame, text="Bank Name:", font=('Arial', 10, 'bold')).grid(
            row=3, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.bank_name, width=40).grid(
            row=3, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Label(frame, text="(Optional - Default: 'CSV Import')",
                 font=('Arial', 8), foreground='gray').grid(
            row=4, column=1, sticky=tk.W, padx=5)

        # Currency
        ttk.Label(frame, text="Currency:", font=('Arial', 10, 'bold')).grid(
            row=5, column=0, sticky=tk.W, padx=5, pady=5)
        currency_combo = ttk.Combobox(frame, textvariable=self.currency,
                                     values=['BRL', 'USD', 'EUR', 'GBP'],
                                     state='readonly', width=10)
        currency_combo.grid(row=5, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Label(frame, text="(BRL=Brazilian Real, USD=US Dollar, EUR=Euro, GBP=British Pound)",
                 font=('Arial', 8), foreground='gray').grid(
            row=6, column=1, sticky=tk.W, padx=5)

    # ==================== STEP 5: FIELD MAPPING ====================

    def _create_step_field_mapping(self):
        """Create field mapping step."""
        frame = ttk.LabelFrame(self.step_container, text="Step 5: Map CSV Columns to OFX Fields",
                              padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=20, pady=20)
        frame.columnconfigure(1, weight=1)

        # Info label
        ttk.Label(frame, text="Map your CSV columns to OFX transaction fields:",
                 font=('Arial', 10)).grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 20))

        # Ensure CSV is loaded
        if not self.csv_headers:
            ttk.Label(frame, text="No CSV data loaded. Please go back to step 3.",
                     foreground='red').grid(row=1, column=0, columnspan=3)
            return

        # Define OFX fields
        ofx_fields = [
            ('date', 'Date *', 'Transaction date'),
            ('amount', 'Amount *', 'Transaction amount (positive or negative)'),
            ('description', 'Description', 'Transaction description (or use composite below)'),
            ('type', 'Type', 'Transaction type: DEBIT or CREDIT (optional)'),
            ('id', 'ID', 'Unique transaction identifier (optional)'),
        ]

        column_options = [NOT_MAPPED] + self.csv_headers

        # Create mapping widgets
        for idx, (field_key, field_label, field_help) in enumerate(ofx_fields, start=1):
            ttk.Label(frame, text=f"{field_label}:", font=('Arial', 10, 'bold')).grid(
                row=idx, column=0, sticky=tk.W, padx=5, pady=5)

            if field_key not in self.field_mappings:
                self.field_mappings[field_key] = tk.StringVar(value=NOT_MAPPED)

            combo = ttk.Combobox(frame, textvariable=self.field_mappings[field_key],
                               values=column_options, state='readonly', width=30)
            combo.grid(row=idx, column=1, sticky=tk.W, padx=5, pady=5)

            ttk.Label(frame, text=field_help, font=('Arial', 8), foreground='gray').grid(
                row=idx, column=2, sticky=tk.W, padx=5, pady=5)

        # Composite description section
        ttk.Separator(frame, orient='horizontal').grid(
            row=len(ofx_fields) + 1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=20)

        ttk.Label(frame, text="Composite Description (Optional)",
                 font=('Arial', 11, 'bold')).grid(
            row=len(ofx_fields) + 2, column=0, columnspan=3, sticky=tk.W, pady=(0, 10))

        ttk.Label(frame, text="Combine multiple columns to create transaction descriptions:",
                 font=('Arial', 9)).grid(
            row=len(ofx_fields) + 3, column=0, columnspan=3, sticky=tk.W, pady=(0, 10))

        # Create composite description interface
        composite_frame = ttk.Frame(frame)
        composite_frame.grid(row=len(ofx_fields) + 4, column=0, columnspan=3,
                            sticky=(tk.W, tk.E), pady=5)

        self._create_composite_description_ui(composite_frame)

        # Note
        note_text = ("* Required fields\n"
                    "Note: If composite description is configured, it will be used instead of "
                    "the Description field mapping.")
        ttk.Label(frame, text=note_text, font=('Arial', 8), foreground='gray',
                 wraplength=700, justify=tk.LEFT).grid(
            row=len(ofx_fields) + 5, column=0, columnspan=3, sticky=tk.W, pady=(20, 0))

    def _create_composite_description_ui(self, parent: ttk.Frame):
        """Create UI for composite description configuration."""
        parent.columnconfigure(1, weight=1)

        # Up to 4 column selectors
        column_options = [NOT_SELECTED] + self.csv_headers

        self.description_columns = []
        for i in range(4):
            ttk.Label(parent, text=f"Column {i+1}:", font=('Arial', 9)).grid(
                row=i, column=0, sticky=tk.W, padx=5, pady=3)

            var = tk.StringVar(value=NOT_SELECTED)
            self.description_columns.append(var)

            combo = ttk.Combobox(parent, textvariable=var,
                               values=column_options, state='readonly', width=30)
            combo.grid(row=i, column=1, sticky=tk.W, padx=5, pady=3)

        # Separator
        ttk.Label(parent, text="Separator:", font=('Arial', 9)).grid(
            row=4, column=0, sticky=tk.W, padx=5, pady=3)

        sep_frame = ttk.Frame(parent)
        sep_frame.grid(row=4, column=1, sticky=tk.W, padx=5, pady=3)

        ttk.Radiobutton(sep_frame, text="Space", variable=self.description_separator,
                       value=' ').pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(sep_frame, text="Dash (-)", variable=self.description_separator,
                       value=' - ').pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(sep_frame, text="Comma (,)", variable=self.description_separator,
                       value=', ').pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(sep_frame, text="Pipe (|)", variable=self.description_separator,
                       value=' | ').pack(side=tk.LEFT, padx=5)

    # ==================== STEP 6: ADVANCED OPTIONS ====================

    def _create_step_advanced_options(self):
        """Create advanced options step."""
        frame = ttk.LabelFrame(self.step_container, text="Step 6: Advanced Options", padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=20, pady=20)
        frame.columnconfigure(0, weight=1)

        ttk.Label(frame, text="Configure optional advanced features:",
                 font=('Arial', 10)).grid(row=0, column=0, sticky=tk.W, pady=(0, 20))

        # Value Inversion
        inversion_frame = ttk.LabelFrame(frame, text="Value Inversion", padding="10")
        inversion_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=10)

        ttk.Checkbutton(
            inversion_frame,
            text="Invert all transaction values (swap debits and credits)",
            variable=self.invert_values
        ).pack(anchor=tk.W, pady=5)

        ttk.Label(inversion_frame,
                 text="Use this if your CSV shows debits as positive and credits as negative,\n"
                      "or vice versa. This will multiply all amounts by -1.",
                 font=('Arial', 8), foreground='gray').pack(anchor=tk.W, pady=5)

        # Date Validation
        validation_frame = ttk.LabelFrame(frame, text="Transaction Date Validation", padding="10")
        validation_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=10)
        validation_frame.columnconfigure(1, weight=1)

        ttk.Checkbutton(
            validation_frame,
            text="Enable date validation for credit card statement period",
            variable=self.enable_date_validation,
            command=self._toggle_date_inputs
        ).grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=5)

        ttk.Label(validation_frame, text="Start Date:").grid(
            row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.start_date_entry = ttk.Entry(validation_frame, textvariable=self.start_date,
                                          state='disabled', width=20)
        self.start_date_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Label(validation_frame, text="(e.g., 2025-10-01 or 01/10/2025)",
                 font=('Arial', 8), foreground='gray').grid(
            row=1, column=2, sticky=tk.W, padx=5, pady=5)

        ttk.Label(validation_frame, text="End Date:").grid(
            row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.end_date_entry = ttk.Entry(validation_frame, textvariable=self.end_date,
                                        state='disabled', width=20)
        self.end_date_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Label(validation_frame, text="(e.g., 2025-10-31 or 31/10/2025)",
                 font=('Arial', 8), foreground='gray').grid(
            row=2, column=2, sticky=tk.W, padx=5, pady=5)

        ttk.Label(validation_frame,
                 text="When enabled, transactions outside the date range will prompt you to:\n"
                      "- Keep the original date\n"
                      "- Adjust to the nearest boundary (start or end date)\n"
                      "- Exclude the transaction from the OFX file",
                 font=('Arial', 8), foreground='gray').grid(
            row=3, column=0, columnspan=3, sticky=tk.W, pady=10)

        # Ready to convert
        ttk.Label(frame, text="[OK] Configuration complete! Click 'Convert to OFX' to proceed.",
                 font=('Arial', 10, 'bold'), foreground='green').grid(
            row=3, column=0, sticky=tk.W, pady=(20, 0))

    def _toggle_date_inputs(self):
        """Enable or disable date input fields based on checkbox state."""
        if self.enable_date_validation.get():
            self.start_date_entry.configure(state='normal')
            self.end_date_entry.configure(state='normal')
        else:
            self.start_date_entry.configure(state='disabled')
            self.end_date_entry.configure(state='disabled')

    # ==================== CONVERSION ====================

    def _handle_out_of_range_transaction(self, row_idx: int, date_str: str,
                                         status: str, validator: DateValidator,
                                         description: str) -> Tuple[Optional[str], str]:
        """
        Show dialog to handle an out-of-range transaction.

        Args:
            row_idx: Row index in CSV (1-based)
            date_str: Original transaction date
            status: 'before' or 'after' the valid range
            validator: DateValidator instance
            description: Transaction description

        Returns:
            Tuple of (adjusted_date, action) where:
            - adjusted_date: New date string or None to exclude
            - action: 'keep', 'adjust', or 'exclude'
        """
        # Create dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Out-of-Range Transaction Detected")
        dialog.geometry("650x350")
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

        ttk.Label(details_frame, text="Transaction Date:", font=('Arial', 10, 'bold')).grid(
            row=0, column=0, sticky=tk.W, pady=2)
        ttk.Label(details_frame, text=date_str).grid(row=0, column=1, sticky=tk.W, padx=10, pady=2)

        ttk.Label(details_frame, text="Description:", font=('Arial', 10, 'bold')).grid(
            row=1, column=0, sticky=tk.W, pady=2)
        ttk.Label(details_frame, text=description[:50] + ('...' if len(description) > 50 else '')).grid(
            row=1, column=1, sticky=tk.W, padx=10, pady=2)

        ttk.Label(details_frame, text="Valid Range:", font=('Arial', 10, 'bold')).grid(
            row=2, column=0, sticky=tk.W, pady=2)
        range_text = f"{validator.start_date.strftime('%Y-%m-%d')} to {validator.end_date.strftime('%Y-%m-%d')}"
        ttk.Label(details_frame, text=range_text).grid(row=2, column=1, sticky=tk.W, padx=10, pady=2)

        if status == 'before':
            status_text = "This transaction occurs BEFORE the start date"
        else:
            status_text = "This transaction occurs AFTER the end date"

        ttk.Label(details_frame, text="Status:", font=('Arial', 10, 'bold')).grid(
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

        def keep_date():
            result['action'] = 'keep'
            result['date'] = date_str
            dialog.destroy()

        def adjust_date():
            adjusted_date = validator.adjust_date_to_boundary(date_str)
            result['action'] = 'adjust'
            result['date'] = adjusted_date
            dialog.destroy()

        def exclude_transaction():
            result['action'] = 'exclude'
            dialog.destroy()

        # Keep button (NEW!)
        keep_btn = ttk.Button(
            buttons_frame,
            text="Keep original date",
            command=keep_date
        )
        keep_btn.pack(side=tk.LEFT, padx=5)

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

        # Explanation
        explanation = ttk.Label(
            main_frame,
            text="- Keep: Use the original date as-is\n"
                 "- Adjust: Change to the nearest valid date\n"
                 "- Exclude: Remove this transaction from the OFX file",
            font=('Arial', 8),
            foreground='gray',
            justify=tk.LEFT
        )
        explanation.pack(pady=10)

        # Wait for dialog to close
        dialog.wait_window()

        return result['date'], result['action']

    def _convert(self):
        """Convert CSV to OFX."""
        if not self._validate_conversion_prerequisites():
            return

        date_validator = self._initialize_date_validator()
        if date_validator is False:
            return

        try:
            self._log("Converting CSV to OFX...")
            parser, generator = self._create_parser_and_generator()

            stats = self._process_csv_rows(parser, generator, date_validator)

            output_file = self._prompt_for_output_file()
            if not output_file:
                return

            self._generate_ofx_file(generator, output_file)
            self._show_conversion_success(output_file, stats, date_validator)

        except Exception as e:
            self._log(f"Error during conversion: {e}")
            messagebox.showerror("Error", f"Conversion failed:\n{e}")

    def _validate_conversion_prerequisites(self) -> bool:
        """Validate prerequisites for conversion."""
        if not self.csv_data:
            messagebox.showwarning("Warning", "Please load a CSV file first")
            return False

        date_col = self.field_mappings['date'].get()
        amount_col = self.field_mappings['amount'].get()

        if date_col == NOT_MAPPED or amount_col == NOT_MAPPED:
            messagebox.showwarning("Warning", "Please map at least Date and Amount fields")
            return False

        desc_col = self.field_mappings['description'].get()
        use_composite = any(var.get() != NOT_SELECTED for var in self.description_columns)

        if desc_col == NOT_MAPPED and not use_composite:
            messagebox.showwarning("Warning",
                                  "Please map the Description field or configure composite description")
            return False
        return True

    def _initialize_date_validator(self):
        """Initialize date validator if enabled. Returns validator or False on error."""
        if not self.enable_date_validation.get():
            return None

        start_date_str = self.start_date.get().strip()
        end_date_str = self.end_date.get().strip()

        if not start_date_str or not end_date_str:
            messagebox.showwarning("Warning",
                                  "Please enter both start and end dates for validation")
            return False

        try:
            validator = DateValidator(start_date_str, end_date_str)
            self._log(f"Date validation enabled: {start_date_str} to {end_date_str}")
            return validator
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid date range: {e}")
            return False

    def _create_parser_and_generator(self):
        """Create CSV parser and OFX generator."""
        parser = CSVParser(
            delimiter=self.delimiter.get(),
            decimal_separator=self.decimal_separator.get()
        )
        generator = OFXGenerator(invert_values=self.invert_values.get())

        if self.invert_values.get():
            self._log("Value inversion enabled - all amounts will be inverted")

        return parser, generator

    def _process_csv_rows(self, parser, generator, date_validator):
        """Process all CSV rows and return statistics."""
        date_col = self.field_mappings['date'].get()
        amount_col = self.field_mappings['amount'].get()
        desc_col = self.field_mappings['description'].get()
        type_col = self.field_mappings['type'].get()
        id_col = self.field_mappings['id'].get()
        use_composite = any(var.get() != NOT_SELECTED for var in self.description_columns)

        stats = {
            'total_rows': len(self.csv_data),
            'processed': 0,
            'excluded': 0,
            'adjusted': 0,
            'kept_out_of_range': 0
        }

        for row_idx, row in enumerate(self.csv_data, 1):
            try:
                date = row[date_col]
                amount = parser.normalize_amount(row[amount_col])
                description = self._build_description(row, desc_col, use_composite)

                date, date_stats = self._validate_and_adjust_date(
                    date, row_idx, description, date_validator
                )
                if date is None:
                    stats['excluded'] += 1
                    continue

                stats['adjusted'] += date_stats.get('adjusted', 0)
                stats['kept_out_of_range'] += date_stats.get('kept_out_of_range', 0)

                trans_type = self._get_transaction_type(type_col, row, amount)
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
                self._log(f"Warning: Skipping row {row_idx}: {e}")
                stats['excluded'] += 1

        return stats

    def _build_description(self, row, desc_col, use_composite):
        """Build transaction description from single or multiple columns."""
        if use_composite:
            desc_parts = []
            for var in self.description_columns:
                col_name = var.get()
                if col_name != NOT_SELECTED and col_name in row:
                    value = row[col_name].strip()
                    if value:
                        desc_parts.append(value)
            description = self.description_separator.get().join(desc_parts)
            return description if description else "Transaction"
        return row[desc_col]

    def _validate_and_adjust_date(self, date, row_idx, description, date_validator):
        """Validate date and adjust if necessary. Returns (date, stats_dict)."""
        stats = {'adjusted': 0, 'kept_out_of_range': 0}

        if not date_validator:
            return date, stats

        if date_validator.is_within_range(date):
            return date, stats

        status = date_validator.get_date_status(date)
        self._log(f"Row {row_idx}: Date {date} is out of range ({status})")

        adjusted_date, action = self._handle_out_of_range_transaction(
            row_idx, date, status, date_validator, description
        )

        if action == 'exclude':
            self._log(f"Row {row_idx}: Transaction excluded by user")
            return None, stats
        elif action == 'adjust':
            self._log(f"Row {row_idx}: Date adjusted from {date} to {adjusted_date}")
            stats['adjusted'] = 1
            return adjusted_date, stats
        elif action == 'keep':
            self._log(f"Row {row_idx}: Keeping original date {date}")
            stats['kept_out_of_range'] = 1
            return date, stats

        return date, stats

    def _get_transaction_type(self, type_col, row, amount):
        """Get transaction type from mapping or infer from amount."""
        if type_col != NOT_MAPPED and type_col in row:
            trans_type = row[type_col].upper()
            if trans_type in ['DEBIT', 'CREDIT']:
                return trans_type
        return 'DEBIT' if amount < 0 else 'CREDIT'

    def _get_transaction_id(self, id_col, row):
        """Get transaction ID from mapping if available."""
        if id_col != NOT_MAPPED and id_col in row:
            return row[id_col]
        return None

    def _prompt_for_output_file(self):
        """Prompt user for output file location."""
        output_file = filedialog.asksaveasfilename(
            title="Save OFX File",
            defaultextension=".ofx",
            filetypes=[("OFX files", "*.ofx"), ("All files", "*.*")]
        )
        if not output_file:
            self._log("Conversion cancelled")
        return output_file

    def _log(self, message: str):
        """
        Add a message to the activity log.

        Args:
            message: Message to log
        """
        from datetime import datetime
        self.log_text.configure(state='normal')
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)  # Scroll to the end
        self.log_text.configure(state='disabled')

    def _clear(self):
        """Clear all form data and reset to initial state."""
        # Clear all variables
        self.csv_file.set('')
        self.delimiter.set(',')
        self.decimal_separator.set('.')
        self.account_id.set('')
        self.bank_name.set('CSV Import')
        self.currency.set('BRL')
        self.start_date.set('')
        self.end_date.set('')
        self.enable_date_validation.set(False)
        self.invert_values.set(False)

        # Clear composite description
        self.description_columns.clear()
        self.description_separator.set(' ')

        # Clear data
        self.csv_headers.clear()
        self.csv_data.clear()
        self.field_mappings.clear()

        # Reset to first step
        self._show_step(0)

        # Clear log
        self.log_text.configure(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.configure(state='disabled')

        self._log("All fields cleared - ready for new conversion")
        logger.info("Form cleared and reset to initial state")

    def _generate_ofx_file(self, generator, output_file: str):
        """
        Generate the OFX file using the generator.

        Args:
            generator: OFXGenerator instance with transactions
            output_file: Path to save the OFX file
        """
        generator.generate(
            output_path=output_file,
            account_id=self.account_id.get(),
            bank_name=self.bank_name.get(),
            currency=self.currency.get()
        )
        self._log(f"OFX file saved: {output_file}")
        logger.info(f"OFX file saved: {output_file}")

    def _show_conversion_success(self, output_file: str, stats: dict, date_validator):
        """
        Show conversion success message with statistics.

        Args:
            output_file: Path to the generated OFX file
            stats: Dictionary with conversion statistics
            date_validator: DateValidator instance (or None if not used)
        """
        # Build statistics message
        msg_parts = [
            f"Conversion completed successfully!",
            f"",
            f"Output file: {output_file}",
            f"",
            f"Statistics:",
            f"  - Total rows processed: {stats['total_rows']}",
            f"  - Transactions exported: {stats['processed']}",
        ]

        if stats['excluded'] > 0:
            msg_parts.append(f"  - Transactions excluded: {stats['excluded']}")

        if date_validator and stats['adjusted'] > 0:
            msg_parts.append(f"  - Dates adjusted: {stats['adjusted']}")

        if date_validator and stats['kept_out_of_range'] > 0:
            msg_parts.append(f"  - Out-of-range dates kept: {stats['kept_out_of_range']}")

        message = "\n".join(msg_parts)
        self._log("Conversion completed successfully!")
        messagebox.showinfo("Success", message)
        logger.info(f"Conversion completed: {stats}")
