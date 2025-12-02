# TransactionManager

## 1. General Information

| Attribute | Value |
|-----------|-------|
| **Module** | `src/gui_transaction_manager.py` |
| **Type** | Companion Class |
| **Responsibility** | Transaction management and context menus |

## 2. Description

The `TransactionManager` class is a companion class that manages transaction operations, including deletion, restoration, and date actions. It also manages context menus for the transaction preview.

### 2.1 Main Responsibility

- Display context menus for transactions
- Manage transaction deletion and restoration
- Handle date action decisions
- Display dialogs for out-of-range transactions

## 3. Main Methods

### 3.1 `show_context_menu(event, tree_widget, ...)`

Displays context menu for transaction operations.

### 3.2 `delete_selected_transactions(tree, items, deleted)`

Deletes selected transactions from preview.

### 3.3 `restore_all_transactions(deleted)`

Restores all deleted transactions.

### 3.4 `show_out_of_range_dialog(...) -> Tuple[str, str]`

Displays dialog to handle out-of-range transaction.

## 4. Dependency Diagram

```mermaid
classDiagram
    class TransactionManager {
        +parent: ConverterGUI
        -_context_menu: Menu
        +show_context_menu()
        +delete_selected_transactions()
        +restore_all_transactions()
        +show_out_of_range_dialog()
        -_close_context_menu()
        -_get_selected_row_info()
    }

    class DateValidator {
        +get_date_status()
        +adjust_date_to_boundary()
    }

    class BalanceManager {
        +get_date_status_for_transaction()
        +get_date_action_label_texts()
    }

    TransactionManager --> DateValidator
    TransactionManager --> BalanceManager
    TransactionManager ..> tkinter
```

## 5. Context Menu

```mermaid
flowchart TD
    A[Right Click] --> B{Transaction selected?}
    B -->|No| C[Empty menu]
    B -->|Yes| D{Date out of range?}
    
    D -->|Yes| E[Date Actions]
    E --> E1[Keep Original]
    E --> E2[Adjust to Boundary]
    E --> E3[Exclude]
    
    D -->|No| F[Standard Actions]
    F --> F1[Delete Selected]
    
    G{Deleted transactions exist?}
    G -->|Yes| H[Restore All]
```

## 6. Usage Example

```python
from src.gui_transaction_manager import TransactionManager

# Create with parent GUI
manager = TransactionManager(parent_gui)

# Show context menu
def on_right_click(event):
    manager.show_context_menu(
        event,
        tree_widget,
        transaction_tree_items,
        deleted_transactions,
        date_action_decisions
    )

# Delete selected transactions
manager.delete_selected_transactions(
    tree_widget,
    transaction_tree_items,
    deleted_transactions
)

# Restore all
manager.restore_all_transactions(deleted_transactions)
```

## 7. Design Patterns

| Pattern | Application |
|---------|-------------|
| **Companion Class** | Extracts transaction logic |
| **Command** | Menu actions as commands |
| **Dependency Injection** | Receives parent in constructor |

## 8. Related Tests

- `tests/test_gui_transaction_manager.py` - 26 tests

---

*Back to [Main Documentation](../README.md)*
