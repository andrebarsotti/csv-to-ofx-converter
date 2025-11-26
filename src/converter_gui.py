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
from .date_validator import DateValidator
from .transaction_utils import parse_balance_value
from . import gui_utils
from .gui_balance_manager import BalanceManager
from .gui_conversion_handler import ConversionHandler, ConversionConfig
from .gui_transaction_manager import TransactionManager
from .gui_steps import (
    FileSelectionStep,
    CSVFormatStep,
    DataPreviewStep,
    OFXConfigStep,
    FieldMappingStep,
    AdvancedOptionsStep,
    BalancePreviewStep
)

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

        # Initialize all wizard steps (Phase D - all 7 steps extracted)
        self.step_instances = {}
        self.step_instances[0] = FileSelectionStep(self)      # Step 1: File Selection
        self.step_instances[1] = CSVFormatStep(self)          # Step 2: CSV Format
        self.step_instances[2] = DataPreviewStep(self)        # Step 3: Data Preview
        self.step_instances[3] = OFXConfigStep(self)          # Step 4: OFX Config
        self.step_instances[4] = FieldMappingStep(self)       # Step 5: Field Mapping
        self.step_instances[5] = AdvancedOptionsStep(self)    # Step 6: Advanced Options
        self.step_instances[6] = BalancePreviewStep(self)     # Step 7: Balance Preview

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

        # Get step instance (all steps now use the new step class pattern)
        step = self.step_instances[step_num]

        # Clear current step container (destroy widgets)
        for widget in self.step_container.winfo_children():
            widget.destroy()

        # Always create fresh UI (step container was destroyed above)
        step.create(self.step_container)

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

    # ==================== HELPER METHODS (used by step classes and conversion) ====================

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
