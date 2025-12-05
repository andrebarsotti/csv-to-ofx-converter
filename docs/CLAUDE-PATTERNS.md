# Common Patterns

This document provides recipes and patterns for frequent development tasks in the CSV to OFX Converter application.

## Table of Contents

- [Adding New Date Formats](#adding-new-date-formats)
- [Modifying GUI Steps](#modifying-gui-steps)
- [Adding New OFX Fields](#adding-new-ofx-fields)
- [Extracting Functions from GUI](#extracting-functions-from-gui)
- [Companion Class Pattern](#companion-class-pattern)
- [Creating New Wizard Steps](#creating-new-wizard-steps)
- [Adding New CSV Formats](#adding-new-csv-formats)
- [Adding New Currency Support](#adding-new-currency-support)
- [Error Handling Patterns](#error-handling-patterns)
- [Testing Patterns](#testing-patterns)

---

## Adding New Date Formats

When adding support for a new date format (e.g., `DD-MM-YYYY`):

### 1. Add Format to OFXGenerator

**File**: `src/ofx_generator.py`

```python
def _parse_date(self, date_str):
    """Parse date string to datetime object"""
    date_formats = [
        "%Y-%m-%d",      # ISO format: 2025-01-15
        "%d/%m/%Y",      # Brazilian/European: 15/01/2025
        "%m/%d/%Y",      # US format: 01/15/2025
        "%Y%m%d",        # Compact: 20250115
        "%d-%m-%Y",      # NEW FORMAT: 15-01-2025
    ]

    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue

    raise ValueError(f"Invalid date format: {date_str}")
```

### 2. Add Format to DateValidator

**File**: `src/date_validator.py`

```python
def _parse_date_to_datetime(self, date_str):
    """Convert date string to datetime object"""
    date_formats = [
        "%Y-%m-%d",      # ISO format: 2025-01-15
        "%d/%m/%Y",      # Brazilian/European: 15/01/2025
        "%m/%d/%Y",      # US format: 01/15/2025
        "%Y%m%d",        # Compact: 20250115
        "%d-%m-%Y",      # NEW FORMAT: 15-01-2025
    ]

    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue

    raise ValueError(f"Unsupported date format: {date_str}")
```

### 3. Add Test Cases

**File**: `tests/test_ofx_generator.py`

```python
def test_date_format_dash_separated(self):
    """Test DD-MM-YYYY date format parsing"""
    generator = OFXGenerator("TestBank", "12345", "BRL")
    generator.add_transaction(
        date="15-01-2025",  # DD-MM-YYYY format
        amount=-50.00,
        description="Test"
    )
    ofx = generator.generate("01-01-2025", "31-01-2025")
    self.assertIn("<DTPOSTED>20250115</DTPOSTED>", ofx)
```

**File**: `tests/test_date_validator.py`

```python
def test_validate_dash_separated_format(self):
    """Test DD-MM-YYYY date format validation"""
    validator = DateValidator("01-01-2025", "31-01-2025")
    self.assertTrue(validator.is_within_range("15-01-2025"))
```

### 4. Update Documentation

**File**: `docs/CLAUDE-ARCHITECTURE.md`

Add the new format to the "Supported Date Formats" section.

---

## Modifying GUI Steps

### Existing Step Structure

GUI steps are named `_create_step_1()`, `_create_step_2()`, etc. in `src/converter_gui.py`.

### Navigation Methods

- `_next_step()` - Handles Next button click
- `_previous_step()` - Handles Back button click
- `_show_step(step_number)` - Shows specific step

### Validation Pattern

Validation happens in `_next_step()` before allowing progression:

```python
def _next_step(self):
    """Handle Next button click"""
    # Validate current step
    if self.current_step == 1:
        if not self._validate_step_1():
            messagebox.showerror("Validation Error", "Please select a file")
            return

    # Move to next step
    self.current_step += 1
    self._show_step(self.current_step)
```

### Adding Validation to Existing Step

**Example**: Add validation to Step 2 (CSV Format):

```python
def _validate_step_2(self):
    """Validate CSV format step"""
    # Ensure delimiter is selected
    if not self.delimiter_var.get():
        messagebox.showerror("Error", "Please select a delimiter")
        return False

    # Ensure decimal separator is selected
    if not self.decimal_var.get():
        messagebox.showerror("Error", "Please select a decimal separator")
        return False

    # Try parsing CSV with selected format
    try:
        parser = CSVParser(
            delimiter=self.delimiter_var.get(),
            decimal_separator=self.decimal_var.get()
        )
        headers, rows = parser.parse_file(self.csv_file)
        self.csv_headers = headers
        self.csv_rows = rows
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Failed to parse CSV: {e}")
        return False
```

**Update `_next_step()` to call validation**:

```python
def _next_step(self):
    """Handle Next button click"""
    if self.current_step == 1:
        if not self._validate_step_1():
            return
    elif self.current_step == 2:
        if not self._validate_step_2():  # NEW
            return
    # ... more steps

    self.current_step += 1
    self._show_step(self.current_step)
```

---

## Adding New OFX Fields

When adding a new field to OFX output (e.g., `REFNUM` for reference number):

### 1. Modify OFXGenerator.add_transaction()

**File**: `src/ofx_generator.py`

```python
def add_transaction(self, date, amount, description,
                   transaction_type=None, transaction_id=None,
                   reference_number=None):  # NEW PARAMETER
    """Add a transaction to the OFX file"""
    # ... existing code ...

    transaction = {
        "type": tx_type,
        "date": date_obj.strftime("%Y%m%d"),
        "amount": final_amount,
        "id": transaction_id or str(uuid.uuid4()),
        "description": description[:255],
        "reference_number": reference_number or ""  # NEW FIELD
    }

    self.transactions.append(transaction)
```

### 2. Update OFX Template in generate()

**File**: `src/ofx_generator.py`

```python
def generate(self, start_date, end_date):
    """Generate OFX file content"""
    # ... existing code ...

    for tx in sorted_transactions:
        transactions_xml += f"""
<STMTTRN>
<TRNTYPE>{tx['type']}</TRNTYPE>
<DTPOSTED>{tx['date']}</DTPOSTED>
<TRNAMT>{tx['amount']:.2f}</TRNAMT>
<FITID>{tx['id']}</FITID>
<REFNUM>{tx['reference_number']}</REFNUM>
<MEMO>{tx['description']}</MEMO>
</STMTTRN>
"""
```

### 3. Update GUI Field Mapping (Step 5)

**File**: `src/gui_steps/field_mapping_step.py`

Add new mapping option:

```python
def _build_ui(self):
    """Build field mapping UI"""
    # ... existing mappings ...

    # Reference Number mapping (NEW)
    ttk.Label(self.container, text="Reference Number:").grid(
        row=5, column=0, sticky="w", pady=5
    )
    self.refnum_combo = ttk.Combobox(
        self.container,
        values=["<Not Mapped>"] + self.get_parent_data("csv_headers", []),
        state="readonly"
    )
    self.refnum_combo.grid(row=5, column=1, sticky="ew", pady=5)
    self.refnum_combo.current(0)
```

### 4. Update Conversion Logic

**File**: `src/gui_conversion_handler.py`

Extract reference number from CSV row:

```python
def _process_csv_rows(self, config):
    """Process CSV rows into transactions"""
    for i, row in enumerate(config.csv_rows):
        # ... existing field extraction ...

        # Extract reference number (NEW)
        refnum = ""
        if config.refnum_column is not None:
            refnum = row.get(config.csv_headers[config.refnum_column], "")

        # Add transaction with new field
        generator.add_transaction(
            date=date_str,
            amount=amount,
            description=description,
            transaction_type=tx_type,
            transaction_id=tx_id,
            reference_number=refnum  # NEW
        )
```

### 5. Add Tests

**File**: `tests/test_ofx_generator.py`

```python
def test_add_transaction_with_reference_number(self):
    """Test adding transaction with reference number"""
    generator = OFXGenerator("TestBank", "12345", "BRL")
    generator.add_transaction(
        date="2025-01-15",
        amount=-50.00,
        description="Test",
        reference_number="REF123"
    )
    ofx = generator.generate("2025-01-01", "2025-01-31")
    self.assertIn("<REFNUM>REF123</REFNUM>", ofx)
```

---

## Extracting Functions from GUI

### When to Extract

Extract functions when:
- Logic is complex (>20 lines)
- Logic is reused in multiple places
- Logic has no UI dependencies
- Logic needs comprehensive testing

### Where to Extract

**For Pure Utility Functions** → `transaction_utils.py` or `gui_utils.py`
**For Complex Subsystems** → New companion class (e.g., `gui_balance_manager.py`)

### Example: Extract Balance Calculation

**Before** (in `converter_gui.py`):

```python
def _calculate_balance(self):
    """Calculate balance from transactions"""
    initial = float(self.initial_balance_var.get() or 0)
    debits = 0
    credits = 0

    for tx in self.transactions:
        if tx['deleted']:
            continue
        if tx['amount'] < 0:
            debits += abs(tx['amount'])
        else:
            credits += tx['amount']

    final = initial - debits + credits
    return {
        'initial': initial,
        'debits': debits,
        'credits': credits,
        'final': final
    }
```

**After** (create `src/transaction_utils.py`):

```python
def calculate_balance_summary(transactions, initial_balance, currency="BRL"):
    """
    Calculate balance summary from transaction list.

    Args:
        transactions: List of transaction dicts with 'amount' and 'deleted' keys
        initial_balance: Initial balance as float
        currency: Currency code (default: BRL)

    Returns:
        Dict with keys: initial, total_debits, total_credits, final, currency
    """
    debits = 0.0
    credits = 0.0

    for tx in transactions:
        if tx.get('deleted', False):
            continue

        amount = float(tx.get('amount', 0))
        if amount < 0:
            debits += abs(amount)
        else:
            credits += amount

    final_balance = initial_balance - debits + credits

    return {
        'initial': initial_balance,
        'total_debits': debits,
        'total_credits': credits,
        'final': final_balance,
        'currency': currency
    }
```

**Use in GUI** (`converter_gui.py`):

```python
from src.transaction_utils import calculate_balance_summary

def _update_balance_display(self):
    """Update balance display"""
    initial = float(self.initial_balance_var.get() or 0)
    summary = calculate_balance_summary(
        self.transactions,
        initial,
        self.currency_var.get()
    )

    self.balance_label.config(text=f"Final: {summary['final']:.2f}")
```

**Add Tests** (`tests/test_transaction_utils.py`):

```python
def test_calculate_balance_summary(self):
    """Test balance calculation"""
    transactions = [
        {'amount': -50.00, 'deleted': False},
        {'amount': 30.00, 'deleted': False},
        {'amount': -20.00, 'deleted': True}  # Should be ignored
    ]

    result = calculate_balance_summary(transactions, 100.00, "BRL")

    self.assertEqual(result['initial'], 100.00)
    self.assertEqual(result['total_debits'], 50.00)
    self.assertEqual(result['total_credits'], 30.00)
    self.assertEqual(result['final'], 80.00)
    self.assertEqual(result['currency'], "BRL")
```

---

## Companion Class Pattern

### When to Use

Use companion classes for complex subsystems that:
- Have multiple related methods
- Need significant state management
- Can be independently tested
- Don't need direct widget access

### Pattern Structure

**1. Create Companion Class**:

**File**: `src/gui_balance_manager.py`

```python
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class BalancePreviewData:
    """Data class for balance preview results"""
    initial_balance: float
    total_debits: float
    total_credits: float
    final_balance: float
    transaction_count: int
    formatted_labels: Dict[str, str]
    currency: str

class BalanceManager:
    """Companion class for balance calculations"""

    def __init__(self, parent):
        """Initialize with parent GUI"""
        self.parent = parent
        self.logger = parent.logger

    def calculate_balance_preview(self, transactions: List[Dict],
                                  initial_balance: float,
                                  currency: str) -> BalancePreviewData:
        """
        Calculate balance preview from transactions.

        Args:
            transactions: List of transaction dicts
            initial_balance: Initial balance amount
            currency: Currency code

        Returns:
            BalancePreviewData with calculations
        """
        # Perform calculations (no widget access)
        debits = sum(abs(tx['amount']) for tx in transactions
                    if not tx.get('deleted') and tx['amount'] < 0)
        credits = sum(tx['amount'] for tx in transactions
                     if not tx.get('deleted') and tx['amount'] > 0)
        final = initial_balance - debits + credits

        # Format labels
        labels = {
            'initial': f"{currency} {initial_balance:,.2f}",
            'debits': f"{currency} {debits:,.2f}",
            'credits': f"{currency} {credits:,.2f}",
            'final': f"{currency} {final:,.2f}"
        }

        # Return data structure (not widgets)
        return BalancePreviewData(
            initial_balance=initial_balance,
            total_debits=debits,
            total_credits=credits,
            final_balance=final,
            transaction_count=len([tx for tx in transactions if not tx.get('deleted')]),
            formatted_labels=labels,
            currency=currency
        )
```

**2. Initialize in ConverterGUI**:

**File**: `src/converter_gui.py`

```python
from src.gui_balance_manager import BalanceManager

class ConverterGUI:
    def __init__(self, root):
        self.root = root
        # ... other initialization ...

        # Initialize companion classes
        self.balance_manager = BalanceManager(self)
```

**3. Use in GUI Methods**:

```python
def _update_balance_preview(self):
    """Update balance preview display"""
    # Get data from companion (no widget manipulation in companion)
    preview = self.balance_manager.calculate_balance_preview(
        transactions=self.transactions,
        initial_balance=float(self.initial_balance_var.get() or 0),
        currency=self.currency_var.get()
    )

    # Update widgets in GUI (companion returned data)
    self.initial_label.config(text=preview.formatted_labels['initial'])
    self.debits_label.config(text=preview.formatted_labels['debits'])
    self.credits_label.config(text=preview.formatted_labels['credits'])
    self.final_label.config(text=preview.formatted_labels['final'])
```

**4. Test with Mock Parent**:

**File**: `tests/test_gui_balance_manager.py`

```python
import unittest
from unittest.mock import Mock
from src.gui_balance_manager import BalanceManager

class TestBalanceManager(unittest.TestCase):
    def setUp(self):
        """Set up mock parent"""
        self.mock_parent = Mock()
        self.mock_parent.logger = Mock()
        self.manager = BalanceManager(self.mock_parent)

    def test_calculate_balance_preview(self):
        """Test balance calculation"""
        transactions = [
            {'amount': -50.00, 'deleted': False},
            {'amount': 30.00, 'deleted': False}
        ]

        result = self.manager.calculate_balance_preview(
            transactions=transactions,
            initial_balance=100.00,
            currency="BRL"
        )

        self.assertEqual(result.initial_balance, 100.00)
        self.assertEqual(result.total_debits, 50.00)
        self.assertEqual(result.total_credits, 30.00)
        self.assertEqual(result.final_balance, 80.00)
        self.assertEqual(result.transaction_count, 2)
```

---

## Creating New Wizard Steps

### Step Creation Pattern

**1. Create Step Class** (extends WizardStep):

**File**: `src/gui_steps/my_new_step.py`

```python
import tkinter as tk
from tkinter import ttk
from src.gui_wizard_step import WizardStep, StepData

class MyNewStep(WizardStep):
    """New wizard step for feature X"""

    def _build_ui(self):
        """Build the step UI"""
        # Create widgets
        ttk.Label(self.container, text="My New Step").pack(pady=10)

        self.entry = ttk.Entry(self.container)
        self.entry.pack(pady=5)

    def _collect_data(self):
        """Collect data from widgets"""
        return {
            'my_field': self.entry.get()
        }

    def _validate_data(self, data):
        """Validate collected data"""
        if not data.get('my_field'):
            return StepData(False, "Field is required", {})

        return StepData(True, "", data)
```

**2. Register Step in GUI**:

**File**: `src/converter_gui.py`

```python
from src.gui_steps.my_new_step import MyNewStep

def _create_steps(self):
    """Create all wizard steps"""
    # ... existing steps ...

    # Add new step
    step_config = StepConfig(
        title="My New Step",
        description="Configure feature X",
        step_number=8
    )
    self.step_8 = MyNewStep(self, self.step_container, step_config)
    self.step_8.create()
```

**3. Update Navigation**:

```python
def _next_step(self):
    """Handle Next button"""
    # ... existing validations ...

    if self.current_step == 8:
        result = self.step_8.validate()
        if not result.is_valid:
            messagebox.showerror("Error", result.message)
            return
        # Store data
        self.data.update(result.data)

    self.current_step += 1
    self._show_step(self.current_step)
```

**4. Add Tests**:

**File**: `tests/test_gui_steps/test_my_new_step.py`

```python
import unittest
from unittest.mock import Mock
from tkinter import Tk, Frame
from src.gui_steps.my_new_step import MyNewStep
from src.gui_wizard_step import StepConfig

class TestMyNewStep(unittest.TestCase):
    def setUp(self):
        """Set up test"""
        self.root = Tk()
        self.container = Frame(self.root)
        self.mock_parent = Mock()
        self.mock_parent.data = {}

        config = StepConfig("My Step", "Description", 8)
        self.step = MyNewStep(self.mock_parent, self.container, config)

    def tearDown(self):
        """Clean up"""
        self.root.destroy()

    def test_create_ui(self):
        """Test UI creation"""
        self.step.create()
        # Assert widgets created
        self.assertIsNotNone(self.step.entry)

    def test_validate_empty_field(self):
        """Test validation with empty field"""
        self.step.create()
        result = self.step.validate()
        self.assertFalse(result.is_valid)
        self.assertEqual(result.message, "Field is required")
```

---

## Adding New CSV Formats

### Example: Add Tab-Separated Values (TSV) Support

**1. Update CSVParser**:

**File**: `src/csv_parser.py`

```python
class CSVParser:
    """CSV file parser with configurable format"""

    DELIMITER_TAB = '\t'  # NEW CONSTANT

    def __init__(self, delimiter=',', decimal_separator='.'):
        """Initialize parser with format"""
        self.delimiter = delimiter
        self.decimal_separator = decimal_separator
```

**2. Update GUI Delimiter Options**:

**File**: `src/gui_steps/csv_format_step.py`

```python
def _build_ui(self):
    """Build CSV format configuration UI"""
    # ... existing code ...

    # Delimiter options
    ttk.Radiobutton(
        self.container,
        text="Tab",
        variable=self.delimiter_var,
        value='\t'  # NEW OPTION
    ).pack(anchor='w')
```

**3. Add Tests**:

**File**: `tests/test_csv_parser.py`

```python
def test_parse_tab_separated_format(self):
    """Test TSV parsing"""
    # Create test TSV file
    tsv_content = "date\tamount\tdescription\n"
    tsv_content += "2025-01-15\t-50.00\tTest\n"

    with open(self.tsv_file, 'w') as f:
        f.write(tsv_content)

    # Parse with tab delimiter
    parser = CSVParser(delimiter='\t', decimal_separator='.')
    headers, rows = parser.parse_file(self.tsv_file)

    self.assertEqual(len(headers), 3)
    self.assertEqual(len(rows), 1)
    self.assertEqual(rows[0][headers[0]], "2025-01-15")
```

---

## Adding New Currency Support

### Example: Add JPY (Japanese Yen) Support

**1. Update Currency List**:

**File**: `src/gui_steps/ofx_config_step.py`

```python
def _build_ui(self):
    """Build OFX configuration UI"""
    # ... existing code ...

    # Currency selection
    currencies = ["BRL", "USD", "EUR", "GBP", "JPY"]  # ADD JPY
    self.currency_combo = ttk.Combobox(
        self.container,
        values=currencies,
        state="readonly"
    )
```

**2. Test Currency in OFXGenerator**:

**File**: `tests/test_ofx_generator.py`

```python
def test_japanese_yen_currency(self):
    """Test OFX generation with JPY currency"""
    generator = OFXGenerator("TestBank", "12345", "JPY")
    generator.add_transaction(
        date="2025-01-15",
        amount=-5000.00,  # 5000 yen
        description="Test"
    )
    ofx = generator.generate("2025-01-01", "2025-01-31")
    self.assertIn("<CURDEF>JPY</CURDEF>", ofx)
```

**3. Update Documentation**:

**File**: `README.md`

Add JPY to supported currencies list.

---

## Error Handling Patterns

### Try-Except Pattern

```python
def parse_csv_file(filename):
    """Parse CSV file with error handling"""
    try:
        parser = CSVParser()
        headers, rows = parser.parse_file(filename)
        return headers, rows
    except FileNotFoundError:
        logger.error(f"File not found: {filename}")
        messagebox.showerror("Error", f"File not found: {filename}")
        return None, None
    except csv.Error as e:
        logger.error(f"CSV parsing error: {e}")
        messagebox.showerror("Error", f"Invalid CSV format: {e}")
        return None, None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        messagebox.showerror("Error", f"Unexpected error: {e}")
        return None, None
```

### Validation Pattern

```python
def validate_date_range(start_date, end_date):
    """Validate date range"""
    # Check both dates provided
    if not start_date or not end_date:
        return False, "Both start and end dates are required"

    # Parse dates
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        return False, "Invalid date format (use YYYY-MM-DD)"

    # Check start before end
    if start >= end:
        return False, "Start date must be before end date"

    # Check reasonable range (e.g., max 1 year)
    if (end - start).days > 365:
        return False, "Date range cannot exceed 1 year"

    return True, ""
```

---

## Testing Patterns

### Unit Test Pattern

```python
import unittest
from src.my_module import my_function

class TestMyFunction(unittest.TestCase):
    def test_normal_case(self):
        """Test with normal input"""
        result = my_function("input")
        self.assertEqual(result, "expected")

    def test_edge_case(self):
        """Test with edge case"""
        result = my_function("")
        self.assertEqual(result, "default")

    def test_error_case(self):
        """Test error handling"""
        with self.assertRaises(ValueError):
            my_function(None)
```

### Mock Pattern

```python
from unittest.mock import Mock, patch

class TestWithMocks(unittest.TestCase):
    def test_with_mock_parent(self):
        """Test with mock parent GUI"""
        mock_parent = Mock()
        mock_parent.data = {"key": "value"}
        mock_parent.logger = Mock()

        # Use mock
        manager = MyManager(mock_parent)
        result = manager.do_something()

        # Assert mock methods called
        mock_parent.logger.info.assert_called()

    @patch('src.my_module.external_function')
    def test_with_patch(self, mock_external):
        """Test with patched external function"""
        mock_external.return_value = "mocked"

        result = my_function_that_calls_external()

        self.assertEqual(result, "expected")
        mock_external.assert_called_once()
```

### Integration Test Pattern

```python
import tempfile
import os

class TestIntegration(unittest.TestCase):
    def setUp(self):
        """Create temporary files"""
        self.temp_dir = tempfile.mkdtemp()
        self.csv_file = os.path.join(self.temp_dir, "test.csv")
        self.ofx_file = os.path.join(self.temp_dir, "output.ofx")

    def tearDown(self):
        """Clean up"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_end_to_end(self):
        """Test complete workflow"""
        # Create input
        with open(self.csv_file, 'w') as f:
            f.write("date,amount,description\n")
            f.write("2025-01-15,-50.00,Test\n")

        # Process
        # ... workflow steps ...

        # Verify output
        self.assertTrue(os.path.exists(self.ofx_file))
        with open(self.ofx_file) as f:
            content = f.read()
            self.assertIn("OFXHEADER", content)
```

---

## Quick Reference

**Add Date Format**: Update `OFXGenerator` and `DateValidator`, add tests

**Modify GUI Step**: Update validation in `_next_step()`, test workflow

**Add OFX Field**: Update `add_transaction()`, `generate()`, GUI mapping, tests

**Extract Function**: Move to `transaction_utils.py` or create companion class

**Companion Class**: Create in `src/gui_*.py`, init in ConverterGUI, return data structures

**New Wizard Step**: Extend `WizardStep`, implement abstract methods, add tests

**Add CSV Format**: Update `CSVParser`, add GUI option, add tests

**Add Currency**: Update currency list in `OFXConfigStep`, add tests

**Error Handling**: Use try-except, validate inputs, log errors, show user-friendly messages

**Testing**: Unit tests for functions, mocks for GUI dependencies, integration tests for workflows
