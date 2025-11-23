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
from .date_validator import DateValidator
from .transaction_utils import parse_balance_value
from . import gui_utils
from .gui_balance_manager import BalanceManager
from .gui_conversion_handler import ConversionHandler, ConversionConfig
from .gui_transaction_manager import TransactionManager
from .gui_steps import FileSelectionStep, CSVFormatStep, OFXConfigStep

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
        self.root.minsize(900, 700)  # Set minimum window size
        # Allow window resizing
        self.root.resizable(True, True)

        # Start maximized (cross-platform compatible)
        try:
            # Try Windows/macOS method
            self.root.state('zoomed')
        except Exception as e:
            # Fallback to Linux method
            logger.debug("Couldn't maximize window using state(): %s", e)
            try:
                self.root.attributes('-zoomed', True)
            except Exception as e2:
                # If both fail, just maximize using geometry
                logger.debug(
                    "Couldn't maximize window using attributes(): %s", e2)
                self.root.update_idletasks()
                screen_width = self.root.winfo_screenwidth()
                screen_height = self.root.winfo_screenheight()
                self.root.geometry(f"{screen_width}x{screen_height}+0+0")

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
        self.initial_balance = tk.StringVar(value='0.00')
        self.final_balance = tk.StringVar(value='0.00')
        self.auto_calculate_final_balance = tk.BooleanVar(value=True)

        # Composite description variables
        self.description_columns = []  # List of selected column variables
        self.description_separator = tk.StringVar(value=' ')

        # Data
        self.csv_headers: List[str] = []
        self.csv_data: List[Dict[str, str]] = []
        self.field_mappings: Dict[str, tk.StringVar] = {}

        # Transaction management (for preview deletion feature)
        self.deleted_transactions = set()  # Set of row indices to exclude
        self.transaction_tree_items = {}  # Map row_index -> tree item ID

        # Date validation management (for preview date action feature)
        # Map row_index -> action ('adjust', 'keep', 'exclude')
        self.date_action_decisions = {}

        # Wizard steps
        self.current_step = 0
        self.steps = [
            "File Selection",
            "CSV Format",
            "Data Preview",
            "OFX Configuration",
            "Field Mapping",
            "Advanced Options",
            "Balance Preview"
        ]

        # Initialize balance manager
        self.balance_manager = BalanceManager(self)

        # Initialize conversion handler
        self.conversion_handler = ConversionHandler(self)

        # Initialize transaction manager
        self.transaction_manager = TransactionManager(self)

        # Initialize new wizard steps (Phase B - Steps 1, 2, 4)
        self.step_instances = {}
        self.step_instances[0] = FileSelectionStep(self)
        self.step_instances[1] = CSVFormatStep(self)
        self.step_instances[3] = OFXConfigStep(self)  # Step 4 is index 3

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
        self.step_container.grid(row=2, column=0, sticky=(
            tk.W, tk.E, tk.N, tk.S), pady=10)
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
                arrow = ttk.Label(self.progress_frame,
                                  text=">", font=('Arial', 12))
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

        self.back_btn = ttk.Button(
            nav_frame, text="< Back", command=self._go_back)
        self.back_btn.pack(side=tk.LEFT, padx=5)

        self.next_btn = ttk.Button(
            nav_frame, text="Next >", command=self._go_next)
        self.next_btn.pack(side=tk.LEFT, padx=5)

        self.convert_btn = ttk.Button(
            nav_frame, text="Convert to OFX", command=self._convert)
        self.convert_btn.pack(side=tk.LEFT, padx=5)
        self.convert_btn.pack_forget()  # Hidden initially

        self.clear_btn = ttk.Button(
            nav_frame, text="Clear All", command=self._clear)
        self.clear_btn.pack(side=tk.LEFT, padx=5)

    def _create_log_section(self, parent: ttk.Frame, row: int):
        """Create log display section."""
        frame = ttk.LabelFrame(parent, text="Activity Log", padding="2")
        frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=2)
        frame.columnconfigure(0, weight=1)

        self.log_text = scrolledtext.ScrolledText(
            frame, height=3, state='disabled', wrap=tk.WORD)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E))

    def _show_step(self, step_num: int):
        """Show the specified step."""
        # Update current step
        self.current_step = step_num
        self._update_progress_indicator()

        # Check if we have a new step instance for this step
        if step_num in self.step_instances:
            # Use new step class pattern
            step = self.step_instances[step_num]

            # Clear current step container (destroy widgets)
            for widget in self.step_container.winfo_children():
                widget.destroy()

            # Always create fresh UI (step container was destroyed above)
            step.create(self.step_container)
        else:
            # Use old step method pattern (Steps 3, 5, 6, 7)
            # Clear current step container
            for widget in self.step_container.winfo_children():
                widget.destroy()

            # Create step content using old methods
            if step_num == 2:
                self._create_step_data_preview()
            elif step_num == 4:
                self._create_step_field_mapping()
            elif step_num == 5:
                self._create_step_advanced_options()
            elif step_num == 6:
                self._create_step_balance_preview()

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
        # Always maintain correct order: Back, Next/Convert, Clear All
        if self.current_step < len(self.steps) - 1:
            self.convert_btn.pack_forget()
            self.next_btn.pack(side=tk.LEFT, padx=5, before=self.clear_btn)
        else:
            self.next_btn.pack_forget()
            self.convert_btn.pack(side=tk.LEFT, padx=5, before=self.clear_btn)

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
        # Check if we have a new step instance for this step
        if self.current_step in self.step_instances:
            # Use new step validation
            step = self.step_instances[self.current_step]
            step_data = step.validate()

            if not step_data.is_valid:
                messagebox.showwarning("Validation Error", step_data.error_message)
                return False
            return True

        # Use old validation methods for steps not yet migrated
        validators = {
            2: self._validate_data_preview,
            4: self._validate_field_mapping,
        }

        validator = validators.get(self.current_step)
        if validator:
            return validator()
        return True

    def _validate_file_selection(self) -> bool:
        """Validate file selection step."""
        csv_file = self.csv_file.get()
        is_valid, error_msg = gui_utils.validate_csv_file_selection(csv_file)
        if not is_valid:
            messagebox.showwarning("Required", error_msg)
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
        field_mappings_dict = {k: v.get() for k, v in self.field_mappings.items()}
        is_valid, error_msg = gui_utils.validate_required_field_mappings(
            field_mappings_dict, NOT_MAPPED)
        if not is_valid:
            messagebox.showwarning("Required", error_msg)
            return False
        return True

    def _validate_description_mapping(self) -> bool:
        """Validate description field or composite description."""
        desc_mapping = self.field_mappings.get('description', tk.StringVar(value=NOT_MAPPED)).get()
        description_columns = [var.get() for var in self.description_columns]
        is_valid, error_msg = gui_utils.validate_description_mapping(
            desc_mapping, description_columns, NOT_MAPPED, NOT_SELECTED)
        if not is_valid:
            messagebox.showwarning("Required", error_msg)
            return False
        return True

    # ==================== STEP 1: FILE SELECTION ====================

    def _create_step_file_selection(self):
        """Create file selection step."""
        frame = ttk.LabelFrame(self.step_container,
                               text="Step 1: Select CSV File", padding="20")
        frame.grid(row=0, column=0, sticky=(
            tk.W, tk.E, tk.N, tk.S), padx=20, pady=20)
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
        frame = ttk.LabelFrame(
            self.step_container, text="Step 2: Configure CSV Format", padding="20")
        frame.grid(row=0, column=0, sticky=(
            tk.W, tk.E, tk.N, tk.S), padx=20, pady=20)

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
        frame = ttk.LabelFrame(self.step_container,
                               text="Step 3: Preview CSV Data", padding="20")
        frame.grid(row=0, column=0, sticky=(
            tk.W, tk.E, tk.N, tk.S), padx=20, pady=20)
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

        self.preview_tree.grid(
            row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        vsb.grid(row=0, column=1, sticky=(tk.N, tk.S))
        hsb.grid(row=1, column=0, sticky=(tk.W, tk.E))

        # Stats label
        self.preview_stats_label = ttk.Label(frame, text="", font=('Arial', 9))
        self.preview_stats_label.grid(
            row=2, column=0, sticky=tk.W, pady=(10, 0))

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
        self.csv_headers, self.csv_data = parser.parse_file(
            self.csv_file.get())

        self._log(
            f"CSV loaded: {len(self.csv_data)} rows, {len(self.csv_headers)} columns")

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
        stats_text = gui_utils.format_preview_stats(
            max_rows, len(self.csv_data), max_preview=100)
        self.preview_stats_label.configure(text=stats_text)

    # ==================== STEP 4: OFX CONFIGURATION ====================

    def _create_step_ofx_config(self):
        """Create OFX configuration step."""
        frame = ttk.LabelFrame(self.step_container,
                               text="Step 4: OFX Configuration", padding="20")
        frame.grid(row=0, column=0, sticky=(
            tk.W, tk.E, tk.N, tk.S), padx=20, pady=20)
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
        frame.grid(row=0, column=0, sticky=(
            tk.W, tk.E, tk.N, tk.S), padx=20, pady=20)
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
            ('description', 'Description',
             'Transaction description (or use composite below)'),
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

        # Preserve existing StringVar values if they exist
        if len(self.description_columns) != 4:
            self.description_columns = []
            for i in range(4):
                self.description_columns.append(
                    tk.StringVar(value=NOT_SELECTED))

        for i in range(4):
            ttk.Label(parent, text=f"Column {i+1}:", font=('Arial', 9)).grid(
                row=i, column=0, sticky=tk.W, padx=5, pady=3)

            combo = ttk.Combobox(parent, textvariable=self.description_columns[i],
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
        frame = ttk.LabelFrame(self.step_container,
                               text="Step 6: Advanced Options", padding="20")
        frame.grid(row=0, column=0, sticky=(
            tk.W, tk.E, tk.N, tk.S), padx=20, pady=20)
        frame.columnconfigure(0, weight=1)

        ttk.Label(frame, text="Configure optional advanced features:",
                  font=('Arial', 10)).grid(row=0, column=0, sticky=tk.W, pady=(0, 20))

        # Value Inversion
        inversion_frame = ttk.LabelFrame(
            frame, text="Value Inversion", padding="10")
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
        validation_frame = ttk.LabelFrame(
            frame, text="Transaction Date Validation", padding="10")
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
        self.start_date_entry.grid(
            row=1, column=1, sticky=tk.W, padx=5, pady=5)
        # Add date format validation for start_date (DD/MM/YYYY)
        self.start_date_entry.bind(
            '<KeyRelease>', lambda e: self._format_date_entry(self.start_date_entry))
        ttk.Label(validation_frame, text="(Format: DD/MM/YYYY, e.g., 01/10/2025)",
                  font=('Arial', 8), foreground='gray').grid(
            row=1, column=2, sticky=tk.W, padx=5, pady=5)

        ttk.Label(validation_frame, text="End Date:").grid(
            row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.end_date_entry = ttk.Entry(validation_frame, textvariable=self.end_date,
                                        state='disabled', width=20)
        self.end_date_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        # Add date format validation for end_date (DD/MM/YYYY)
        self.end_date_entry.bind(
            '<KeyRelease>', lambda e: self._format_date_entry(self.end_date_entry))
        ttk.Label(validation_frame, text="(Format: DD/MM/YYYY, e.g., 31/10/2025)",
                  font=('Arial', 8), foreground='gray').grid(
            row=2, column=2, sticky=tk.W, padx=5, pady=5)

        ttk.Label(validation_frame,
                  text="When enabled, transactions outside the date range will prompt you to:\n"
                  "- Keep the original date\n"
                  "- Adjust to the nearest boundary (start or end date)\n"
                  "- Exclude the transaction from the OFX file",
                  font=('Arial', 8), foreground='gray').grid(
            row=3, column=0, columnspan=3, sticky=tk.W, pady=10)

        # Ready to proceed
        ttk.Label(frame, text="[OK] Configuration complete! Click 'Next' to preview balances.",
                  font=('Arial', 10, 'bold'), foreground='green').grid(
            row=3, column=0, sticky=tk.W, pady=(20, 0))

        # Restore the correct state of date entry fields based on checkbox value
        self._toggle_date_inputs()

    def _toggle_date_inputs(self):
        """Enable or disable date input fields based on checkbox state."""
        if self.enable_date_validation.get():
            self.start_date_entry.configure(state='normal')
            self.end_date_entry.configure(state='normal')
        else:
            self.start_date_entry.configure(state='disabled')
            self.end_date_entry.configure(state='disabled')

    # ==================== STEP 7: BALANCE PREVIEW ====================

    def _create_step_balance_preview(self):
        """Create balance preview step showing transactions and calculated balances."""
        frame = ttk.LabelFrame(self.step_container, text="Step 7: Balance Preview & Confirmation",
                               padding="10")
        frame.grid(row=0, column=0, sticky=(
            tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        frame.columnconfigure(0, weight=1)
        # Make transaction preview row expandable
        frame.rowconfigure(3, weight=1)

        ttk.Label(frame, text="Review transactions and balances before exporting:",
                  font=('Arial', 10)).grid(row=0, column=0, sticky=tk.W, pady=(0, 10))

        # Calculate balance information
        try:
            balance_info = self._calculate_balance_preview()
            # Cache for context menu access
            self._cached_balance_info = balance_info
        except Exception as e:
            ttk.Label(frame, text=f"Error calculating balances: {e}",
                      foreground='red', font=('Arial', 10, 'bold')).grid(
                row=1, column=0, sticky=tk.W, pady=20)
            return

        # Initial Balance Input (moved from Step 4)
        initial_balance_frame = ttk.LabelFrame(
            frame, text="Initial Balance", padding="5")
        initial_balance_frame.grid(
            row=1, column=0, sticky=(tk.W, tk.E), pady=5)

        balance_input_frame = ttk.Frame(initial_balance_frame)
        balance_input_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(balance_input_frame, text="Starting Balance:", font=('Arial', 10, 'bold')).pack(
            side=tk.LEFT, padx=5)
        # Register numeric validation command
        vcmd_numeric = (self.root.register(
            self._validate_numeric_input), '%d', '%P')
        self.initial_balance_entry = ttk.Entry(
            balance_input_frame, textvariable=self.initial_balance,
            width=20, validate='key', validatecommand=vcmd_numeric)
        self.initial_balance_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(balance_input_frame, text="Recalculate",
                   command=self._recalculate_balance_preview).pack(side=tk.LEFT, padx=5)
        ttk.Label(balance_input_frame, text="(Enter starting balance and click Recalculate)",
                  font=('Arial', 8), foreground='gray').pack(side=tk.LEFT, padx=5)

        # Balance summary frame (compact layout)
        summary_frame = ttk.LabelFrame(
            frame, text="Balance Summary", padding="5")
        summary_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=5)
        summary_frame.columnconfigure(1, weight=1)

        # Total Credits
        credits_text = f"Total Credits (+): {balance_info['total_credits']:.2f}"
        self.total_credits_label = ttk.Label(
            summary_frame, text=credits_text,
            font=('Arial', 10), foreground='green')
        self.total_credits_label.grid(
            row=0, column=0, columnspan=2, sticky=tk.W, padx=5, pady=2)

        # Total Debits
        debits_text = f"Total Debits (-): {balance_info['total_debits']:.2f}"
        self.total_debits_label = ttk.Label(
            summary_frame, text=debits_text,
            font=('Arial', 10), foreground='red')
        self.total_debits_label.grid(
            row=1, column=0, columnspan=2, sticky=tk.W, padx=5, pady=2)

        # Calculated Final Balance
        ttk.Label(summary_frame, text="Calculated Final Balance:", font=('Arial', 10, 'bold')).grid(
            row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.calculated_balance_label = ttk.Label(
            summary_frame,
            text=f"{balance_info['calculated_final_balance']:.2f}",
            font=('Arial', 11, 'bold'),
            foreground='blue'
        )
        self.calculated_balance_label.grid(
            row=2, column=1, sticky=tk.W, padx=5, pady=2)

        ttk.Separator(summary_frame, orient='horizontal').grid(
            row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        # Final Balance Mode Selection
        mode_frame = ttk.Frame(summary_frame)
        mode_frame.grid(row=4, column=0, columnspan=2,
                        sticky=(tk.W, tk.E), pady=5)

        ttk.Checkbutton(
            mode_frame,
            text="Automatically use calculated final balance",
            variable=self.auto_calculate_final_balance,
            command=self._toggle_final_balance_mode
        ).pack(anchor=tk.W, pady=2)

        # Manual Final Balance Entry
        manual_frame = ttk.Frame(summary_frame)
        manual_frame.grid(row=5, column=0, columnspan=2,
                          sticky=(tk.W, tk.E), pady=2)

        ttk.Label(manual_frame, text="Manual Final Balance:", font=('Arial', 10, 'bold')).pack(
            side=tk.LEFT, padx=5)
        # Set initial state based on auto_calculate_final_balance value
        initial_state = 'disabled' if self.auto_calculate_final_balance.get() else 'normal'
        # Register numeric validation command
        vcmd_numeric = (self.root.register(
            self._validate_numeric_input), '%d', '%P')
        self.final_balance_entry = ttk.Entry(
            manual_frame, textvariable=self.final_balance,
            width=20, state=initial_state,
            validate='key', validatecommand=vcmd_numeric)
        self.final_balance_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(manual_frame, text="(Uncheck above to edit manually)",
                  font=('Arial', 8), foreground='gray').pack(side=tk.LEFT, padx=5)

        # Transaction count
        count_text = f"Total Transactions: {balance_info['transaction_count']}"
        self.transaction_count_label = ttk.Label(
            summary_frame, text=count_text,
            font=('Arial', 9), foreground='gray')
        self.transaction_count_label.grid(
            row=6, column=0, columnspan=2, sticky=tk.W, pady=(10, 0))

        # Transaction preview (scrollable list)
        preview_frame = ttk.LabelFrame(
            frame, text="Transaction Preview (All Transactions)", padding="5")
        preview_frame.grid(row=3, column=0, sticky=(
            tk.W, tk.E, tk.N, tk.S), pady=5)
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(0, weight=1)

        # Create treeview
        tree_container = ttk.Frame(preview_frame)
        tree_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_container.columnconfigure(0, weight=1)
        tree_container.rowconfigure(0, weight=1)

        vsb = ttk.Scrollbar(tree_container, orient="vertical")
        hsb = ttk.Scrollbar(tree_container, orient="horizontal")

        self.balance_preview_tree = ttk.Treeview(
            tree_container,
            columns=('date', 'description', 'amount', 'type'),
            show='headings',
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set
        )
        vsb.configure(command=self.balance_preview_tree.yview)
        hsb.configure(command=self.balance_preview_tree.xview)

        self.balance_preview_tree.heading('date', text='Date')
        self.balance_preview_tree.heading('description', text='Description')
        self.balance_preview_tree.heading('amount', text='Amount')
        self.balance_preview_tree.heading('type', text='Type')

        self.balance_preview_tree.column('date', width=120, anchor=tk.W)
        self.balance_preview_tree.column('description', width=300, anchor=tk.W)
        self.balance_preview_tree.column('amount', width=100, anchor=tk.E)
        self.balance_preview_tree.column('type', width=80, anchor=tk.CENTER)

        self.balance_preview_tree.grid(
            row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        vsb.grid(row=0, column=1, sticky=(tk.N, tk.S))
        hsb.grid(row=1, column=0, sticky=(tk.W, tk.E))

        # Configure tags for date validation status
        self.balance_preview_tree.tag_configure(
            'date_before', background='#ffcccc')  # Light red
        self.balance_preview_tree.tag_configure(
            'date_after', background='#ffe6cc')   # Light orange

        # Bind context menu for deleting transactions
        self.balance_preview_tree.bind(
            "<Button-3>", self._show_transaction_context_menu_wrapper)

        # Populate transaction preview
        self.transaction_tree_items.clear()  # Clear previous mappings
        for trans in balance_info['transactions']:
            # Get the original row index from transaction data
            row_idx = trans.get('row_idx')

            # Skip if no row_idx (shouldn't happen, but be safe)
            if row_idx is None:
                continue

            # Determine tag based on date status
            tags = []
            if trans.get('date_status') == 'before':
                tags.append('date_before')
            elif trans.get('date_status') == 'after':
                tags.append('date_after')

            item_id = self.balance_preview_tree.insert('', tk.END, values=(
                trans['date'],
                trans['description'][:50],
                f"{trans['amount']:.2f}",
                trans['type']
            ), tags=tags)
            # Store mapping of row_idx to tree item ID
            self.transaction_tree_items[row_idx] = item_id

        # Initialize final balance
        self._update_final_balance_display(
            balance_info['calculated_final_balance'])

        # Confirmation message
        ttk.Label(frame, text="[OK] Review complete! Click 'Convert to OFX' to generate the file.",
                  font=('Arial', 10, 'bold'), foreground='green').grid(
            row=4, column=0, sticky=tk.W, pady=(10, 0))

    def _recalculate_balance_preview(self):
        """
        Recalculate balance preview when initial balance changes.

        Called when user clicks the Recalculate button after changing initial balance.
        Updates all balance labels without recreating the entire step.
        """
        try:
            # Recalculate balance information
            balance_info = self._calculate_balance_preview()
            # Cache for context menu access
            self._cached_balance_info = balance_info

            # Update labels
            self.total_credits_label.configure(
                text=f"Total Credits (+): {balance_info['total_credits']:.2f}")
            self.total_debits_label.configure(
                text=f"Total Debits (-): {balance_info['total_debits']:.2f}")
            self.calculated_balance_label.configure(
                text=f"{balance_info['calculated_final_balance']:.2f}")
            self.transaction_count_label.configure(
                text=f"Total Transactions: {balance_info['transaction_count']}")

            # Update final balance if in automatic mode
            if self.auto_calculate_final_balance.get():
                self._update_final_balance_display(
                    balance_info['calculated_final_balance'])

            self._log(
                f"Balance recalculated with initial balance: {balance_info['initial_balance']:.2f}")

        except Exception as e:
            self._log(f"Error recalculating balance: {e}")
            messagebox.showerror(
                "Error", f"Failed to recalculate balance:\n{e}")

    def _calculate_balance_preview(self) -> Dict:
        """
        Calculate balance information for preview.

        Returns:
            Dictionary with balance calculations and transaction list
        """
        # Get field mappings as strings
        field_mappings = {k: v.get() for k, v in self.field_mappings.items()}

        # Get description columns as list of strings
        description_columns = [var.get() for var in self.description_columns]

        # Use BalanceManager to calculate preview
        balance_data = self.balance_manager.calculate_balance_preview(
            initial_balance_str=self.initial_balance.get(),
            csv_data=self.csv_data,
            field_mappings=field_mappings,
            description_columns=description_columns,
            description_separator=self.description_separator.get(),
            delimiter=self.delimiter.get(),
            decimal_separator=self.decimal_separator.get(),
            invert_values=self.invert_values.get(),
            deleted_transactions=self.deleted_transactions,
            enable_date_validation=self.enable_date_validation.get(),
            start_date_str=self.start_date.get().strip(),
            end_date_str=self.end_date.get().strip()
        )

        # Convert to dictionary for compatibility with existing code
        return balance_data.to_dict()

    def _validate_numeric_input(self, action: str, value_if_allowed: str) -> bool:
        """
        Validate numeric input for balance fields.

        Allows: digits, optional minus sign at start, optional single decimal point.
        Blocks: letters, special characters, multiple decimal points.

        Args:
            action: '1' for insert, '0' for delete
            value_if_allowed: The value the entry will have if the change is allowed

        Returns:
            True if change is allowed, False otherwise
        """
        # Delegate to balance manager
        return self.balance_manager.validate_balance_input(
            action, value_if_allowed
        )

    def _format_date_entry(self, entry_widget):
        """
        Auto-format date input with slashes in DD/MM/YYYY format.

        Removes non-digit, non-slash characters and auto-inserts slashes.
        Limits to DD/MM/YYYY format (Brazilian/European standard).
        Maintains cursor position correctly.

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
                current_value, formatted, cursor_pos)

            # Update the entry (UI manipulation stays in GUI)
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, formatted)

            # Restore cursor position
            entry_widget.icursor(new_cursor_pos)

    def _toggle_final_balance_mode(self):
        """Toggle between automatic and manual final balance mode."""
        if self.auto_calculate_final_balance.get():
            self.final_balance_entry.configure(state='disabled')
            # Update to calculated value
            try:
                balance_info = self._calculate_balance_preview()
                self._update_final_balance_display(
                    balance_info['calculated_final_balance'])
            except Exception as e:
                logger.debug("Failed to update final balance display: %s", e)
        else:
            self.final_balance_entry.configure(state='normal')

    def _update_final_balance_display(self, calculated_balance: float):
        """Update the final balance display with calculated or manual value."""
        formatted = self.balance_manager.format_final_balance(calculated_balance)
        self.final_balance.set(formatted)

    def _show_transaction_context_menu_wrapper(self, event):
        """
        Wrapper for showing transaction context menu.

        Delegates to transaction manager with necessary parameters.

        Args:
            event: Right-click event containing mouse position
        """
        self.transaction_manager.show_context_menu(
            event,
            self.balance_preview_tree,
            self.transaction_tree_items,
            self.deleted_transactions,
            self.date_action_decisions
        )

    # ==================== CONVERSION ====================

    def _handle_out_of_range_transaction(self, row_idx: int, date_str: str,
                                         status: str, validator: DateValidator,
                                         description: str) -> Tuple[Optional[str], str]:
        """
        Show dialog to handle an out-of-range transaction.

        Delegates to transaction manager for dialog display.

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
        return self.transaction_manager.show_out_of_range_dialog(
            row_idx, date_str, status, validator, description
        )

    def _convert(self):
        """Convert CSV to OFX."""
        if not self._validate_conversion_prerequisites():
            return

        try:
            self._log("Converting CSV to OFX...")

            # Prompt for output file first
            output_file = self._prompt_for_output_file()
            if not output_file:
                return

            # Create conversion config
            config = self._create_conversion_config()

            # Delegate to conversion handler
            success, message, stats = self.conversion_handler.convert(
                config, output_file
            )

            if success:
                self._log("Conversion completed successfully!")
                messagebox.showinfo("Success", message)
                logger.info("Conversion completed: %s", stats)
            else:
                self._log(f"Error during conversion: {message}")
                messagebox.showerror("Error", message)

        except Exception as e:
            self._log(f"Error during conversion: {e}")
            messagebox.showerror("Error", f"Conversion failed:\n{e}")

    def _create_conversion_config(self) -> ConversionConfig:
        """
        Create ConversionConfig from GUI state.

        Returns:
            ConversionConfig object with all conversion parameters
        """
        # Get field mappings as strings
        field_mappings_dict = {
            k: v.get() for k, v in self.field_mappings.items()
        }

        # Get description columns as list of strings
        description_columns = [var.get() for var in self.description_columns]

        # Parse initial balance
        initial_balance_str = self.initial_balance.get().strip()
        if initial_balance_str and initial_balance_str not in [
            '0', '0.0', '0.00'
        ]:
            initial_balance = parse_balance_value(
                initial_balance_str, default=0.0
            )
            if abs(initial_balance) < 1e-9:
                self._log("Warning: Invalid initial balance, using 0.00")
                initial_balance = 0.0
        else:
            initial_balance = 0.0

        # Parse final balance (if manual mode)
        final_balance = None
        if not self.auto_calculate_final_balance.get():
            final_balance_str = self.final_balance.get().strip()
            if final_balance_str:
                try:
                    final_balance = float(final_balance_str)
                    self._log(
                        f"Using manual final balance: {final_balance:.2f}"
                    )
                except ValueError:
                    self._log(
                        "Warning: Invalid final balance, "
                        "will calculate automatically"
                    )
                    final_balance = None

        return ConversionConfig(
            csv_file_path=self.csv_file.get(),
            csv_data=self.csv_data,
            field_mappings=field_mappings_dict,
            description_columns=description_columns,
            description_separator=self.description_separator.get(),
            delimiter=self.delimiter.get(),
            decimal_separator=self.decimal_separator.get(),
            invert_values=self.invert_values.get(),
            account_id=self.account_id.get(),
            bank_name=self.bank_name.get(),
            currency=self.currency.get(),
            initial_balance=initial_balance,
            statement_start_date=self.start_date.get(),
            statement_end_date=self.end_date.get(),
            date_action=self.enable_date_validation.get(),
            deleted_transactions=self.deleted_transactions,
            date_action_decisions=self.date_action_decisions,
            enable_date_validation=self.enable_date_validation.get(),
            final_balance=final_balance
        )

    def _validate_conversion_prerequisites(self) -> bool:
        """Validate prerequisites for conversion."""
        field_mappings_dict = {k: v.get() for k, v in self.field_mappings.items()}
        is_valid, error_msg = gui_utils.validate_conversion_prerequisites(
            self.csv_data, field_mappings_dict, NOT_MAPPED)
        if not is_valid:
            messagebox.showwarning("Warning", error_msg)
            return False

        desc_mapping = field_mappings_dict.get('description', NOT_MAPPED)
        description_columns = [var.get() for var in self.description_columns]
        is_valid, error_msg = gui_utils.validate_description_mapping(
            desc_mapping, description_columns, NOT_MAPPED, NOT_SELECTED)
        if not is_valid:
            messagebox.showwarning("Warning", error_msg)
            return False
        return True

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
        self.initial_balance.set('0.00')
        self.auto_calculate_final_balance.set(True)
        self.final_balance.set('0.00')

        # Clear composite description
        self.description_columns.clear()
        self.description_separator.set(' ')

        # Clear data
        self.csv_headers.clear()
        self.csv_data.clear()
        self.field_mappings.clear()

        # Clear transaction management
        self.deleted_transactions.clear()
        self.transaction_tree_items.clear()
        self.date_action_decisions.clear()

        # Reset to first step
        self._show_step(0)

        # Clear log
        self.log_text.configure(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.configure(state='disabled')

        self._log("All fields cleared - ready for new conversion")
        logger.info("Form cleared and reset to initial state")
