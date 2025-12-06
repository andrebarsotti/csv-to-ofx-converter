"""
balance_preview_step.py - Balance Preview Step (Step 7)

This module implements the balance preview step for the CSV to OFX Converter wizard.
Users can review transaction balances, delete/restore transactions, and make date
action decisions before final OFX conversion.

Classes:
    BalancePreviewStep: Step 7 implementation for balance preview and confirmation
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, Tuple, Optional

from src.gui_wizard_step import WizardStep, StepConfig
from src import gui_utils


class BalancePreviewStep(WizardStep):
    """
    Step 7: Review balance and confirm conversion.

    This step allows users to:
    - Enter or modify initial balance
    - View calculated balance summary (credits, debits, final balance)
    - Preview all transactions with date validation status
    - Delete/restore transactions via context menu
    - Make date action decisions for out-of-range transactions
    - Toggle between auto-calculated and manual final balance
    - Confirm before conversion

    UI Elements:
        - Initial Balance Input Section:
          - Starting Balance entry (numeric validation)
          - Recalculate button
          - Help text
        - Balance Summary Section:
          - Total Credits label (green)
          - Total Debits label (red)
          - Calculated Final Balance label (blue, bold)
          - Separator
          - Auto-calculate checkbox
          - Manual Final Balance entry (enabled/disabled based on checkbox)
          - Help text
          - Transaction count label (gray)
        - Transaction Preview Section:
          - Treeview with columns: Date, Description, Amount, Type
          - Vertical and horizontal scrollbars
          - Context menu binding (right-click)
          - Row coloring: Light red (before range), Light orange (after range)
        - Confirmation label (green success message)

    Data Collected:
        - initial_balance: float (starting balance)
        - final_balance: float (ending balance, auto or manual)
        - auto_calculate_final_balance: bool (mode flag)
        - deleted_transactions: Set[int] (excluded row indices)
        - date_action_decisions: Dict[int, str] (row_idx -> action: keep/adjust/exclude)

    Manager Integration:
        - BalanceManager: For balance calculations and numeric validation
        - TransactionManager: For context menu and transaction operations

    Validation:
        - Initial balance must be valid number
        - Final balance must be valid number (if manual mode)

    Example:
        >>> step = BalancePreviewStep(parent_gui)
        >>> container = step.create(parent_frame)
        >>> step.show()
        >>> result = step.validate()
        >>> if result.is_valid:
        ...     print(f"Initial: {result.data['initial_balance']}")
        ...     print(f"Final: {result.data['final_balance']}")
        ...     print(f"Deleted: {result.data['deleted_transactions']}")
    """

    def __init__(self, parent):
        """
        Initialize BalancePreviewStep.

        Args:
            parent: Parent wizard orchestrator (ConverterGUI)
        """
        config = StepConfig(
            step_number=6,
            step_name="Balance Preview",
            step_title="Step 7: Balance Preview & Confirmation"
        )
        super().__init__(parent, config)
        self._cached_balance_info = None

    def _build_ui(self):
        """
        Build balance preview UI.

        Creates initial balance input, balance summary, transaction preview treeview,
        and confirmation message. Integrates with BalanceManager and TransactionManager.
        """
        # Info label
        ttk.Label(
            self.container,
            text="Review transactions and balances before exporting:",
            font=('Arial', 10)
        ).grid(row=0, column=0, sticky=tk.W, pady=(0, 10))

        # Calculate balance information
        try:
            balance_info = self._calculate_balance_preview()
            self._cached_balance_info = balance_info
            # Share cache with parent for TransactionManager access
            self.parent._cached_balance_info = balance_info
        except Exception as e:
            ttk.Label(
                self.container,
                text=f"Error calculating balances: {e}",
                foreground='red',
                font=('Arial', 10, 'bold')
            ).grid(row=1, column=0, sticky=tk.W, pady=20)
            return

        # Create sections
        self._create_initial_balance_section()
        self._create_balance_summary_section(balance_info)
        self._create_transaction_preview_section(balance_info)

        # Initialize final balance display
        self._update_final_balance_display(
            balance_info['calculated_final_balance'])

    def _create_initial_balance_section(self):
        """
        Create initial balance input section.

        Includes:
        - Starting Balance label
        - Entry for initial balance (with numeric validation)
        - Recalculate button
        - Help text
        """
        frame = ttk.LabelFrame(
            self.container,
            text="Initial Balance",
            padding="5"
        )
        frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        self.container.columnconfigure(0, weight=1)

        input_frame = ttk.Frame(frame)
        input_frame.pack(fill=tk.X, padx=5, pady=5)

        # Label
        ttk.Label(
            input_frame,
            text="Starting Balance:",
            font=('Arial', 10, 'bold')
        ).pack(side=tk.LEFT, padx=5)

        # Entry with numeric validation
        vcmd_numeric = (
            self.parent.root.register(self._validate_numeric_input),
            '%d', '%P'
        )
        entry = ttk.Entry(
            input_frame,
            textvariable=self.parent.initial_balance,
            width=20,
            validate='key',
            validatecommand=vcmd_numeric
        )
        entry.pack(side=tk.LEFT, padx=5)
        self._widgets['initial_balance_entry'] = entry

        # Recalculate button
        ttk.Button(
            input_frame,
            text="Recalculate",
            command=self._recalculate_balance_preview
        ).pack(side=tk.LEFT, padx=5)

        # Help text
        ttk.Label(
            input_frame,
            text="(Enter starting balance and click Recalculate)",
            font=('Arial', 8),
            foreground='gray'
        ).pack(side=tk.LEFT, padx=5)

    def _create_balance_summary_section(self, balance_info: Dict):
        """
        Create balance summary section.

        Args:
            balance_info: Dictionary with balance calculations

        Includes:
        - Total Credits label (green)
        - Total Debits label (red)
        - Calculated Final Balance label (blue, bold)
        - Separator
        - Auto-calculate checkbox
        - Manual Final Balance entry
        - Help text
        - Transaction count label (gray)
        """
        frame = ttk.LabelFrame(
            self.container,
            text="Balance Summary",
            padding="5"
        )
        frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=5)
        frame.columnconfigure(1, weight=1)

        # Total Credits
        credits_text = f"Total Credits (+): {balance_info['total_credits']:.2f}"
        credits_label = ttk.Label(
            frame,
            text=credits_text,
            font=('Arial', 10),
            foreground='green'
        )
        credits_label.grid(row=0, column=0, columnspan=2,
                           sticky=tk.W, padx=5, pady=2)
        self._widgets['total_credits_label'] = credits_label

        # Total Debits
        debits_text = f"Total Debits (-): {balance_info['total_debits']:.2f}"
        debits_label = ttk.Label(
            frame,
            text=debits_text,
            font=('Arial', 10),
            foreground='red'
        )
        debits_label.grid(row=1, column=0, columnspan=2,
                          sticky=tk.W, padx=5, pady=2)
        self._widgets['total_debits_label'] = debits_label

        # Calculated Final Balance
        ttk.Label(
            frame,
            text="Calculated Final Balance:",
            font=('Arial', 10, 'bold')
        ).grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)

        calculated_label = ttk.Label(
            frame,
            text=f"{balance_info['calculated_final_balance']:.2f}",
            font=('Arial', 11, 'bold'),
            foreground='blue'
        )
        calculated_label.grid(row=2, column=1, sticky=tk.W, padx=5, pady=2)
        self._widgets['calculated_final_label'] = calculated_label

        # Separator
        ttk.Separator(frame, orient='horizontal').grid(
            row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5
        )

        # Auto-calculate checkbox
        mode_frame = ttk.Frame(frame)
        mode_frame.grid(row=4, column=0, columnspan=2,
                        sticky=(tk.W, tk.E), pady=5)

        ttk.Checkbutton(
            mode_frame,
            text="Automatically use calculated final balance",
            variable=self.parent.auto_calculate_final_balance,
            command=self._toggle_final_balance_mode
        ).pack(anchor=tk.W, pady=2)

        # Manual Final Balance entry
        manual_frame = ttk.Frame(frame)
        manual_frame.grid(row=5, column=0, columnspan=2,
                          sticky=(tk.W, tk.E), pady=2)

        ttk.Label(
            manual_frame,
            text="Manual Final Balance:",
            font=('Arial', 10, 'bold')
        ).pack(side=tk.LEFT, padx=5)

        # Determine initial state
        initial_state = 'disabled' if self.parent.auto_calculate_final_balance.get() else 'normal'

        # Entry with numeric validation
        vcmd_numeric = (
            self.parent.root.register(self._validate_numeric_input),
            '%d', '%P'
        )
        manual_entry = ttk.Entry(
            manual_frame,
            textvariable=self.parent.final_balance,
            width=20,
            state=initial_state,
            validate='key',
            validatecommand=vcmd_numeric
        )
        manual_entry.pack(side=tk.LEFT, padx=5)
        self._widgets['manual_balance_entry'] = manual_entry

        # Help text
        ttk.Label(
            manual_frame,
            text="(Uncheck above to edit manually)",
            font=('Arial', 8),
            foreground='gray'
        ).pack(side=tk.LEFT, padx=5)

        # Transaction count
        count_text = f"Total Transactions: {balance_info['transaction_count']}"
        count_label = ttk.Label(
            frame,
            text=count_text,
            font=('Arial', 9),
            foreground='gray'
        )
        count_label.grid(row=6, column=0, columnspan=2,
                         sticky=tk.W, pady=(10, 0))
        self._widgets['transaction_count_label'] = count_label

    def _create_transaction_preview_section(self, balance_info: Dict):
        """
        Create transaction preview section.

        Args:
            balance_info: Dictionary with transaction list

        Includes:
        - Treeview with columns: Date, Description, Amount, Type
        - Vertical and horizontal scrollbars
        - Context menu binding
        - Row coloring for date validation status
        """
        frame = ttk.LabelFrame(
            self.container,
            text="Transaction Preview (All Transactions)",
            padding="5"
        )
        frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=6)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        # Make transaction preview row expandable
        self.container.rowconfigure(3, weight=1)

        # Create tree container
        tree_container = ttk.Frame(frame)
        tree_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_container.columnconfigure(0, weight=1)
        tree_container.rowconfigure(0, weight=1)

        # Scrollbars
        vsb = ttk.Scrollbar(tree_container, orient="vertical")
        hsb = ttk.Scrollbar(tree_container, orient="horizontal")

        # Treeview
        tree = ttk.Treeview(
            tree_container,
            columns=('date', 'description', 'amount', 'type'),
            show='headings',
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set
        )
        vsb.configure(command=tree.yview)
        hsb.configure(command=tree.xview)

        # Configure headings
        tree.heading('date', text='Date')
        tree.heading('description', text='Description')
        tree.heading('amount', text='Amount')
        tree.heading('type', text='Type')

        # Configure columns
        tree.column('date', width=120, anchor=tk.W)
        tree.column('description', width=300, anchor=tk.W)
        tree.column('amount', width=100, anchor=tk.E)
        tree.column('type', width=80, anchor=tk.CENTER)

        # Grid layout
        tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        vsb.grid(row=0, column=1, sticky=(tk.N, tk.S))
        hsb.grid(row=1, column=0, sticky=(tk.W, tk.E))

        # Configure tags for date validation status
        tree.tag_configure('date_before', background='#ffcccc')  # Light red
        tree.tag_configure('date_after', background='#ffe6cc')   # Light orange

        # Bind context menu
        tree.bind("<Button-3>", self._show_transaction_context_menu_wrapper)

        # Store treeview reference in parent for access by managers
        self.parent.balance_preview_tree = tree

        # Populate transaction preview
        self._populate_transaction_tree(tree, balance_info['transactions'])

    def _populate_transaction_tree(self, tree: ttk.Treeview, transactions: list):
        """
        Populate transaction treeview with data.

        Args:
            tree: Treeview widget to populate
            transactions: List of transaction dictionaries
        """
        # Clear existing items
        self.parent.transaction_tree_items.clear()

        for trans in transactions:
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

            # Insert item with appropriate styling
            item_id = tree.insert('', tk.END, values=(
                trans['date'],
                trans['description'][:50],  # Truncate to 50 chars
                f"{trans['amount']:.2f}",
                trans['type']
            ), tags=tags)

            # Store mapping of row_idx to tree item ID
            self.parent.transaction_tree_items[row_idx] = item_id

    # === Helper Methods ===

    def _recalculate_balance_preview(self):
        """
        Recalculate balance preview when initial balance changes.

        Called when user clicks the Recalculate button after changing initial balance.
        Updates all balance labels without recreating the entire step.
        """
        try:
            # Recalculate balance information
            balance_info = self._calculate_balance_preview()
            self._cached_balance_info = balance_info
            # Share cache with parent for TransactionManager access
            self.parent._cached_balance_info = balance_info

            # Update labels
            self._widgets['total_credits_label'].configure(
                text=f"Total Credits (+): {balance_info['total_credits']:.2f}"
            )
            self._widgets['total_debits_label'].configure(
                text=f"Total Debits (-): {balance_info['total_debits']:.2f}"
            )
            self._widgets['calculated_final_label'].configure(
                text=f"{balance_info['calculated_final_balance']:.2f}"
            )
            self._widgets['transaction_count_label'].configure(
                text=f"Total Transactions: {balance_info['transaction_count']}"
            )

            # Update final balance if in automatic mode
            if self.parent.auto_calculate_final_balance.get():
                self._update_final_balance_display(
                    balance_info['calculated_final_balance']
                )

            self.log(
                f"Balance recalculated with initial balance: {balance_info['initial_balance']:.2f}"
            )

        except Exception as e:
            self.log(f"Error recalculating balance: {e}")
            messagebox.showerror(
                "Error",
                f"Failed to recalculate balance:\n{e}"
            )

    def _calculate_balance_preview(self) -> Dict:
        """
        Calculate balance information for preview.

        Uses BalanceManager to calculate balance summary from current CSV data,
        field mappings, and user settings.

        Returns:
            Dictionary with balance calculations and transaction list
        """
        # Get field mappings as strings
        field_mappings = {}
        for key, var in self.parent.field_mappings.items():
            field_mappings[key] = var.get()

        # Get description columns as list of strings
        description_columns = [var.get()
                               for var in self.parent.description_columns]

        # Use BalanceManager to calculate preview
        balance_data = self.parent.balance_manager.calculate_balance_preview(
            initial_balance_str=self.parent.initial_balance.get(),
            csv_data=self.parent.csv_data,
            field_mappings=field_mappings,
            description_columns=description_columns,
            description_separator=self.parent.description_separator.get(),
            delimiter=self.parent.delimiter.get(),
            decimal_separator=self.parent.decimal_separator.get(),
            invert_values=self.parent.invert_values.get(),
            deleted_transactions=self.parent.deleted_transactions,
            enable_date_validation=self.parent.enable_date_validation.get(),
            start_date_str=self.parent.start_date.get().strip(),
            end_date_str=self.parent.end_date.get().strip()
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
        return self.parent.balance_manager.validate_balance_input(
            action, value_if_allowed
        )

    def _toggle_final_balance_mode(self):
        """
        Toggle between automatic and manual final balance mode.

        When auto mode is enabled:
        - Disables manual entry
        - Updates final balance to calculated value

        When auto mode is disabled:
        - Enables manual entry
        - Allows user to enter custom final balance
        """
        if self.parent.auto_calculate_final_balance.get():
            # Enable auto mode
            self._widgets['manual_balance_entry'].configure(state='disabled')
            # Update to calculated value
            try:
                balance_info = self._calculate_balance_preview()
                self._update_final_balance_display(
                    balance_info['calculated_final_balance']
                )
            except Exception as e:
                self.log(f"Failed to update final balance display: {e}")
        else:
            # Enable manual mode
            self._widgets['manual_balance_entry'].configure(state='normal')

    def _update_final_balance_display(self, calculated_balance: float):
        """
        Update the final balance display with calculated or manual value.

        Args:
            calculated_balance: Calculated balance value to display
        """
        formatted = self.parent.balance_manager.format_final_balance(
            calculated_balance)
        self.parent.final_balance.set(formatted)

    def _show_transaction_context_menu_wrapper(self, event):
        """
        Wrapper for showing transaction context menu.

        Delegates to transaction manager with necessary parameters.

        Args:
            event: Right-click event containing mouse position
        """
        self.parent.transaction_manager.show_context_menu(
            event,
            self.parent.balance_preview_tree,
            self.parent.transaction_tree_items,
            self.parent.deleted_transactions,
            self.parent.date_action_decisions
        )

    # === Data Collection & Validation ===

    def _collect_data(self) -> Dict[str, Any]:
        """
        Collect data from balance preview step.

        Returns:
            Dictionary with:
            - initial_balance: float (starting balance)
            - final_balance: float (ending balance, auto or manual)
            - auto_calculate_final_balance: bool (mode flag)
            - deleted_transactions: Set[int] (excluded row indices)
            - date_action_decisions: Dict[int, str] (row_idx -> action)
        """
        return {
            'initial_balance': self.parent.initial_balance.get(),
            'final_balance': self.parent.final_balance.get(),
            'auto_calculate_final_balance': self.parent.auto_calculate_final_balance.get(),
            'deleted_transactions': self.parent.deleted_transactions.copy(),
            'date_action_decisions': self.parent.date_action_decisions.copy()
        }

    def _validate_data(self, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Validate balance preview data.

        Args:
            data: Data dictionary from _collect_data()

        Returns:
            Tuple of (is_valid, error_message):
            - is_valid: True if data is valid, False otherwise
            - error_message: User-friendly error message if invalid, None if valid
        """
        # Validate initial balance
        initial_balance_str = data.get('initial_balance', '')
        is_valid, error_msg = gui_utils.validate_balance_value(
            initial_balance_str)
        if not is_valid:
            return False, f"Invalid initial balance: {error_msg}"

        # Validate final balance (if manual mode)
        auto_calculate = data.get('auto_calculate_final_balance', True)
        if not auto_calculate:
            final_balance_str = data.get('final_balance', '')
            is_valid, error_msg = gui_utils.validate_balance_value(
                final_balance_str)
            if not is_valid:
                return False, f"Invalid final balance: {error_msg}"

        return True, None
