"""
GUI Transaction Manager Module
===============================
Handles transaction operations and context menu management for the GUI.

This module extracts transaction management functionality from ConverterGUI
to improve maintainability and testability.

Author: Generated for Brazilian banking compatibility
License: MIT
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional, Tuple, Set, Dict
import logging

from .date_validator import DateValidator

logger = logging.getLogger(__name__)


class TransactionManager:
    """
    Manages transaction operations for the GUI.

    This class handles:
    - Context menu display and operations for transactions
    - Transaction deletion and restoration
    - Date action decisions (keep/adjust/exclude)
    - Dialog management for out-of-range transactions
    """

    def __init__(self, parent_gui):
        """
        Initialize the transaction manager.

        Args:
            parent_gui: ConverterGUI instance for callbacks and data access
        """
        self.parent = parent_gui
        self._context_menu = None

    def show_context_menu(
        self,
        event,
        tree_widget: ttk.Treeview,
        transaction_tree_items: Dict[int, str],
        deleted_transactions: Set[int],
        date_action_decisions: Dict[int, str]
    ):
        """
        Show context menu for transaction operations.

        Args:
            event: Right-click event containing mouse position
            tree_widget: Treeview widget containing transactions
            transaction_tree_items: Map of row_idx -> tree item ID
            deleted_transactions: Set of deleted row indices
            date_action_decisions: Map of row_idx -> date action
        """
        # Close any existing menu
        self._close_existing_context_menu()

        # Check if any items are selected
        selected = tree_widget.selection()

        # Create context menu
        self._context_menu = tk.Menu(self.parent.root, tearoff=0)
        menu_has_items = False

        # Find the row index and date status for selected item
        selected_row_idx, date_status = self._get_selected_row_info(
            selected, transaction_tree_items
        )

        # Add date action options first if there's a date issue
        has_date_actions = False
        if selected_row_idx is not None and date_status in ('before', 'after'):
            current_action = date_action_decisions.get(
                selected_row_idx, 'adjust'
            )
            # Build date action menu items
            self._add_date_action_menu_items(
                self._context_menu,
                selected_row_idx,
                current_action
            )
            menu_has_items = True
            has_date_actions = True

        # Add delete/restore options
        self._add_delete_restore_menu_items(
            self._context_menu,
            selected,
            has_date_actions,
            deleted_transactions
        )
        if deleted_transactions:
            menu_has_items = True

        if menu_has_items:
            self._context_menu.post(event.x_root, event.y_root)
            # Bind to close menu when clicking elsewhere
            self._context_menu.bind(
                "<FocusOut>", lambda e: self._context_menu.unpost()
            )
            self.parent.root.bind(
                "<Button-1>", self._close_context_menu, add="+"
            )

    def _close_existing_context_menu(self):
        """Close any existing context menu."""
        if self._context_menu:
            try:
                self._context_menu.unpost()
                self._context_menu.destroy()
            except Exception as e:
                logger.debug("Error closing existing context menu: %s", e)

    def _close_context_menu(self, event=None):
        """Close context menu if it exists."""
        if self._context_menu:
            try:
                self._context_menu.unpost()
            except Exception as e:
                logger.debug("Error unposting context menu: %s", e)

    def _get_selected_row_info(
        self,
        selected,
        transaction_tree_items: Dict[int, str]
    ) -> Tuple[Optional[int], Optional[str]]:
        """
        Get row index and date status for selected transaction.

        Args:
            selected: Selection from treeview
            transaction_tree_items: Map of row_idx -> tree item ID

        Returns:
            Tuple of (row_idx, date_status) or (None, None) if not found
        """
        if len(selected) != 1:
            return None, None

        item_id = selected[0]

        # Find the row_idx for this tree item
        for row_idx, tree_item_id in transaction_tree_items.items():
            if tree_item_id == item_id:
                # Get the transaction data to check date status
                date_status = self._get_date_status_for_row(row_idx)
                return row_idx, date_status

        return None, None

    def _get_date_status_for_row(self, row_idx: int) -> str:
        """
        Get date status for a specific row.

        Args:
            row_idx: Row index to check

        Returns:
            Date status string ('before', 'after', 'valid')
        """
        cached_balance = getattr(self.parent, '_cached_balance_info', None)
        return self.parent.balance_manager.get_date_status_for_transaction(
            row_idx, cached_balance
        )

    def _add_date_action_menu_items(
        self,
        menu: tk.Menu,
        row_idx: int,
        current_action: str
    ):
        """
        Add date-related actions to a context menu for a specific row.

        Args:
            menu: Menu to add items to
            row_idx: Row index of transaction
            current_action: Currently selected action
        """
        # Get label texts from balance manager
        labels = self.parent.balance_manager.get_date_action_label_texts(
            current_action
        )

        menu.add_command(label="📅 Date Actions", state='disabled')
        menu.add_separator()
        menu.add_command(
            label=labels['keep'],
            command=lambda: self._set_date_action_and_close(row_idx, 'keep')
        )
        menu.add_command(
            label=labels['adjust'],
            command=lambda: self._set_date_action_and_close(
                row_idx, 'adjust'
            )
        )
        menu.add_command(
            label=labels['exclude'],
            command=lambda: self._set_date_action_and_close(
                row_idx, 'exclude'
            )
        )
        menu.add_separator()

    def _add_delete_restore_menu_items(
        self,
        menu: tk.Menu,
        selected,
        has_date_actions: bool,
        deleted_transactions: Set[int]
    ):
        """
        Add delete/restore menu items depending on selection and state.

        Args:
            menu: Menu to add items to
            selected: Selected items from treeview
            has_date_actions: Whether date actions are shown
            deleted_transactions: Set of deleted row indices
        """
        if selected and not has_date_actions:
            delete_count = len(selected)
            plural = 's' if delete_count > 1 else ''
            menu.add_command(
                label=f"Delete Selected ({delete_count} transaction{plural})",
                command=lambda: self._delete_selected_and_close_menu()
            )
        if deleted_transactions:
            deleted_count = len(deleted_transactions)
            plural = 's' if deleted_count > 1 else ''
            menu.add_command(
                label=(
                    f"Restore All Deleted ({deleted_count} "
                    f"transaction{plural})"
                ),
                command=lambda: self._restore_all_and_close_menu()
            )

    def _set_date_action_and_close(self, row_idx: int, action: str):
        """
        Set date action for a specific transaction and close menu.

        Args:
            row_idx: Row index of the transaction
            action: Date action to apply ('keep', 'adjust', 'exclude')
        """
        self.parent.date_action_decisions[row_idx] = action
        self.parent._log(
            f"Date action set to '{action}' for transaction at "
            f"row {row_idx}"
        )
        self._close_context_menu()

        # If action is 'exclude', also mark as deleted and remove from tree
        if action == 'exclude':
            self.parent.deleted_transactions.add(row_idx)
            # Remove the transaction from the tree view
            tree_item_id = self.parent.transaction_tree_items.get(row_idx)
            if tree_item_id:
                self.parent.balance_preview_tree.delete(tree_item_id)
            # Recalculate balances without recreating the entire step
            self.parent._recalculate_balance_preview()

    def _delete_selected_and_close_menu(self):
        """Delete selected transactions and close menu."""
        self.delete_selected_transactions(
            self.parent.balance_preview_tree,
            self.parent.transaction_tree_items,
            self.parent.deleted_transactions
        )
        self._close_context_menu()

    def _restore_all_and_close_menu(self):
        """Restore all transactions and close menu."""
        self.restore_all_transactions(
            self.parent.deleted_transactions
        )
        self._close_context_menu()

    def delete_selected_transactions(
        self,
        tree_widget: ttk.Treeview,
        transaction_tree_items: Dict[int, str],
        deleted_transactions: Set[int]
    ):
        """
        Delete selected transactions from preview and mark for exclusion.

        Removes selected items from tree, adds their row indices to deleted
        set, and triggers balance recalculation.

        Args:
            tree_widget: Treeview widget containing transactions
            transaction_tree_items: Map of row_idx -> tree item ID
            deleted_transactions: Set of deleted row indices
        """
        selected = tree_widget.selection()

        if not selected:
            return

        # Find row indices for selected items
        deleted_count = 0
        for item_id in selected:
            # Find the row_idx for this tree item
            for row_idx, tree_item_id in transaction_tree_items.items():
                if tree_item_id == item_id:
                    # Mark as deleted
                    deleted_transactions.add(row_idx)
                    # Remove from tree
                    tree_widget.delete(item_id)
                    deleted_count += 1
                    break

        if deleted_count > 0:
            plural = 's' if deleted_count > 1 else ''
            self.parent._log(
                f"Deleted {deleted_count} transaction{plural} from preview"
            )
            # Recalculate balances
            self.parent._recalculate_balance_preview()

    def restore_all_transactions(
        self,
        deleted_transactions: Set[int]
    ):
        """
        Restore all deleted transactions.

        Clears the deleted set and refreshes the preview to show all
        transactions.

        Args:
            deleted_transactions: Set of deleted row indices to clear
        """
        if not deleted_transactions:
            return

        count = len(deleted_transactions)
        deleted_transactions.clear()
        self.parent._log(
            f"Restored {count} deleted transaction{'s' if count > 1 else ''}"
        )

        # Refresh the entire preview step to rebuild the tree
        self.parent._show_step(self.parent.current_step)

    def show_out_of_range_dialog(
        self,
        row_idx: int,
        date_str: str,
        status: str,
        validator: DateValidator,
        description: str
    ) -> Tuple[Optional[str], str]:
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
        dialog = tk.Toplevel(self.parent.root)
        dialog.title("Out-of-Range Transaction Detected")
        dialog.geometry("650x350")
        dialog.transient(self.parent.root)
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

        ttk.Label(
            details_frame,
            text="Transaction Date:",
            font=('Arial', 10, 'bold')
        ).grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Label(details_frame, text=date_str).grid(
            row=0, column=1, sticky=tk.W, padx=10, pady=2
        )

        ttk.Label(
            details_frame,
            text="Description:",
            font=('Arial', 10, 'bold')
        ).grid(row=1, column=0, sticky=tk.W, pady=2)
        desc_text = description[:50] + (
            '...' if len(description) > 50 else ''
        )
        ttk.Label(details_frame, text=desc_text).grid(
            row=1, column=1, sticky=tk.W, padx=10, pady=2
        )

        ttk.Label(
            details_frame,
            text="Valid Range:",
            font=('Arial', 10, 'bold')
        ).grid(row=2, column=0, sticky=tk.W, pady=2)
        start_str = validator.start_date.strftime('%Y-%m-%d')
        end_str = validator.end_date.strftime('%Y-%m-%d')
        range_text = f"{start_str} to {end_str}"
        ttk.Label(details_frame, text=range_text).grid(
            row=2, column=1, sticky=tk.W, padx=10, pady=2
        )

        if status == 'before':
            status_text = "This transaction occurs BEFORE the start date"
        else:
            status_text = "This transaction occurs AFTER the end date"

        ttk.Label(
            details_frame,
            text="Status:",
            font=('Arial', 10, 'bold')
        ).grid(row=3, column=0, sticky=tk.W, pady=2)
        ttk.Label(
            details_frame,
            text=status_text,
            foreground='orange'
        ).grid(row=3, column=1, sticky=tk.W, padx=10, pady=2)

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

        # Keep button
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
            text=(
                "- Keep: Use the original date as-is\n"
                "- Adjust: Change to the nearest valid date\n"
                "- Exclude: Remove this transaction from the OFX file"
            ),
            font=('Arial', 8),
            foreground='gray',
            justify=tk.LEFT
        )
        explanation.pack(pady=10)

        # Wait for dialog to close
        dialog.wait_window()

        return result['date'], result['action']
