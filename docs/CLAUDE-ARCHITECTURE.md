# Architecture Details

This document provides comprehensive architecture information for the CSV to OFX Converter application.

## Module Structure

The codebase is organized into separate modules under `src/`:

```
main.py                    # Entry point, imports from src
src/
  csv_to_ofx_converter.py  # Main module, initializes logging and exports all classes
  csv_parser.py            # CSVParser class - handles CSV file parsing
  ofx_generator.py         # OFXGenerator class - generates OFX files
  date_validator.py        # DateValidator class - validates transaction dates
  converter_gui.py         # ConverterGUI class - Tkinter wizard orchestrator (750 lines)
  transaction_utils.py     # Utility functions for transaction processing (no UI dependencies)
  gui_utils.py             # GUI utility functions (pure functions, no Tkinter dependencies)
  gui_balance_manager.py   # BalanceManager class - balance calculations and preview
  gui_conversion_handler.py # ConversionHandler class - CSV to OFX conversion orchestration
  gui_transaction_manager.py # TransactionManager class - transaction operations and context menus
  gui_wizard_step.py       # WizardStep base class - abstract base for wizard steps (~355 lines)
  constants.py             # Shared constants (NOT_MAPPED, NOT_SELECTED)
  gui_steps/               # Wizard step implementations package (Phase D complete - all 7 steps)
    __init__.py            # Package initialization, exports all step classes
    file_selection_step.py # FileSelectionStep - Step 1: File selection (174 lines, 7 tests)
    csv_format_step.py     # CSVFormatStep - Step 2: CSV format config (197 lines, 31 tests)
    data_preview_step.py   # DataPreviewStep - Step 3: Data preview (285 lines, 31 tests)
    ofx_config_step.py     # OFXConfigStep - Step 4: OFX configuration (271 lines, 40 tests)
    field_mapping_step.py  # FieldMappingStep - Step 5: Field mapping (390 lines, 38 tests)
    advanced_options_step.py # AdvancedOptionsStep - Step 6: Advanced options (354 lines, 30 tests)
    balance_preview_step.py # BalancePreviewStep - Step 7: Balance preview (641 lines, 29 tests)
```

---

## Key Classes and Responsibilities

### CSVParser (`src/csv_parser.py`)

**Purpose**: Parses CSV files with configurable delimiter and decimal separator.

**Key Methods**:
- `parse_file()` - Returns tuple of (headers, rows)
- `normalize_amount()` - Converts string amounts to floats

**Features**:
- Handles Brazilian format (1.234,56) and standard format (1,234.56)
- Supports negative amounts with currency symbols in any position:
  - `-R$ 100,00` → -100.00
  - `R$ -100,00` → -100.00
- Supports parentheses notation for negative amounts:
  - `(R$ 100,00)` → -100.00
- Handles UTF-8 and BOM encoding

**Usage Example**:
```python
from src.csv_parser import CSVParser

parser = CSVParser(delimiter=';', decimal_separator=',')
headers, rows = parser.parse_file('transactions.csv')
```

---

### OFXGenerator (`src/ofx_generator.py`)

**Purpose**: Generates OFX 1.0.2 format (SGML, not XML).

**Key Methods**:
- `add_transaction()` - Queues transactions
- `generate()` - Produces final OFX file

**Features**:
- Initialized with optional `invert_values` flag to swap debits/credits
- Credit card statement format (CREDITCARDMSGSRSV1)
- Automatically infers transaction type from amount sign
- Generates UUID for transaction IDs if not provided
- Limits description to 255 characters per OFX spec

**Usage Example**:
```python
from src.ofx_generator import OFXGenerator

generator = OFXGenerator(
    bank_name="MyBank",
    account_id="1234567890",
    currency="BRL",
    invert_values=False
)

generator.add_transaction(
    date="2025-01-15",
    amount=-50.00,
    description="Restaurant",
    transaction_type="DEBIT"
)

ofx_content = generator.generate(
    start_date="2025-01-01",
    end_date="2025-01-31"
)
```

---

### DateValidator (`src/date_validator.py`)

**Purpose**: Validates transaction dates against statement period.

**Key Methods**:
- `is_within_range()` - Checks if date is valid
- `get_date_status()` - Returns 'before', 'within', or 'after'
- `adjust_date_to_boundary()` - Moves out-of-range dates to nearest boundary

**Supported Date Formats**:
- YYYY-MM-DD (ISO format)
- DD/MM/YYYY (Brazilian/European format)
- MM/DD/YYYY (US format)
- YYYYMMDD (compact format)

**Usage Example**:
```python
from src.date_validator import DateValidator

validator = DateValidator(
    start_date="2025-01-01",
    end_date="2025-01-31"
)

if validator.is_within_range("2025-01-15"):
    print("Date is valid")

status = validator.get_date_status("2025-02-05")  # Returns 'after'
adjusted = validator.adjust_date_to_boundary("2025-02-05")  # Returns '2025-01-31'
```

---

### TransactionUtils (`src/transaction_utils.py`)

**Purpose**: Pure utility functions with no UI dependencies (fully testable).

**Key Functions**:
- `build_transaction_description()` - Creates single or composite descriptions from CSV columns
- `determine_transaction_type()` - Determines DEBIT/CREDIT from column value or amount sign
- `extract_transaction_id()` - Extracts transaction ID from mapped column
- `calculate_balance_summary()` - Computes balance totals from transaction list
- `validate_field_mappings()` - Validates required field mappings
- `parse_balance_value()` - Safely parses balance strings to floats with defaults

**Usage Example**:
```python
from src.transaction_utils import build_transaction_description, determine_transaction_type

# Build composite description
description = build_transaction_description(
    row={"col1": "Restaurant", "col2": "Downtown", "col3": "Lunch"},
    description_columns=[0, 1, 2],
    separator=" - ",
    headers=["col1", "col2", "col3"]
)
# Returns: "Restaurant - Downtown - Lunch"

# Determine transaction type
tx_type = determine_transaction_type(
    row={"type": "debit"},
    type_column_index=0,
    headers=["type"],
    amount=-50.00
)
# Returns: "DEBIT"
```

---

### GUIUtils (`src/gui_utils.py`)

**Purpose**: Pure utility functions with no Tkinter dependencies (fully testable).

**Categories**:
- File validation
- Field mapping validation
- Date formatting
- Numeric validation
- Balance calculations
- Statistics formatting

**Total Functions**: 16 functions organized into 8 sections

**Usage**: Used by ConverterGUI and BalanceManager for business logic that doesn't require direct GUI access.

---

### BalanceManager (`src/gui_balance_manager.py`)

**Purpose**: Companion class for ConverterGUI using dependency injection pattern. Handles all balance calculations and preview generation.

**Key Methods**:
- `calculate_balance_preview()` - Returns BalancePreviewData dataclass with calculation results
- `format_balance_labels()` - Formats balance information for display
- `validate_balance_input()` - Validates initial balance input

**Design Pattern**:
- No direct Tkinter dependencies (independently testable)
- Returns data structures instead of manipulating widgets
- ConverterGUI creates instance: `self.balance_manager = BalanceManager(self)`

**Usage Example**:
```python
from src.gui_balance_manager import BalanceManager

manager = BalanceManager(parent_gui)
preview_data = manager.calculate_balance_preview(
    transactions=transactions,
    initial_balance=1000.00,
    currency="BRL"
)

# preview_data contains:
# - initial_balance
# - total_debits
# - total_credits
# - final_balance
# - transaction_count
# - formatted_labels (dict)
```

---

### ConversionHandler (`src/gui_conversion_handler.py`)

**Purpose**: Companion class for ConverterGUI using dependency injection pattern. Orchestrates CSV to OFX conversion workflow.

**Key Methods**:
- `convert()` - Main conversion method, returns (success: bool, message: str, stats: dict)
- `_process_csv_rows()` - Processes CSV rows into transactions
- `_validate_and_adjust_date()` - Validates dates and handles out-of-range cases
- `_generate_ofx_file()` - Generates final OFX file

**Design Pattern**:
- Uses ConversionConfig dataclass to bundle 19 conversion parameters
- No direct widget manipulation (independently testable)
- Returns tuple for success/failure reporting

**Usage Example**:
```python
from src.gui_conversion_handler import ConversionHandler, ConversionConfig

handler = ConversionHandler(parent_gui)
config = ConversionConfig(
    csv_file="transactions.csv",
    ofx_file="output.ofx",
    field_mappings={"date": 0, "amount": 1, "description": 2},
    # ... 16 more parameters
)

success, message, stats = handler.convert(config)
if success:
    print(f"Converted {stats['total']} transactions")
```

---

### TransactionManager (`src/gui_transaction_manager.py`)

**Purpose**: Companion class for ConverterGUI using dependency injection pattern. Manages transaction operations and context menu for balance preview.

**Key Methods**:
- `show_context_menu()` - Shows context menu with date actions for selected transaction
- `delete_selected_transactions()` - Deletes selected transactions from preview
- `restore_all_transactions()` - Restores all deleted transactions
- `show_out_of_range_dialog()` - Displays dialog for out-of-range transaction decisions

**Date Actions**:
- Keep original date (use as-is)
- Adjust to boundary (move to start_date or end_date)
- Exclude transaction (skip it entirely)

**Usage Example**:
```python
from src.gui_transaction_manager import TransactionManager

manager = TransactionManager(parent_gui)

# Show context menu for transaction at row 5
manager.show_context_menu(event, tree_widget, row_index=5)

# Delete selected transactions
deleted_count = manager.delete_selected_transactions(tree_widget)

# Restore all transactions
manager.restore_all_transactions(tree_widget)
```

---

### WizardStep (`src/gui_wizard_step.py`)

**Purpose**: Abstract base class for wizard step implementations. Provides lifecycle management and enforces structure.

**Lifecycle Methods**:
- `create()` - Creates UI widgets (calls abstract `_build_ui()`)
- `show()` - Shows step widgets
- `hide()` - Hides step widgets
- `destroy()` - Destroys step widgets
- `validate()` - Validates step data (calls `_collect_data()` and `_validate_data()`)

**Abstract Methods** (must be implemented by subclasses):
- `_build_ui()` - Build the step's UI
- `_collect_data()` - Collect data from widgets
- `_validate_data()` - Validate collected data

**Helper Methods**:
- `get_parent_data(key)` - Safely get data from parent GUI
- `set_parent_data(key, value)` - Safely set data in parent GUI
- `log(message)` - Log message to parent's logger

**Data Classes**:
- `StepConfig` - Configuration for step (title, description, step_number)
- `StepData` - Result from validation (is_valid, message, data_dict)

**Usage Example**:
```python
from src.gui_wizard_step import WizardStep, StepConfig, StepData

class MyStep(WizardStep):
    def _build_ui(self):
        # Create widgets
        self.label = ttk.Label(self.container, text="My Step")
        self.label.pack()

    def _collect_data(self):
        # Collect data from widgets
        return {"field1": "value1"}

    def _validate_data(self, data):
        # Validate collected data
        if not data.get("field1"):
            return StepData(False, "Field1 is required", {})
        return StepData(True, "", data)

# Usage
config = StepConfig("My Step", "Step description", 1)
step = MyStep(parent_gui, container_frame, config)
step.create()
step.show()

# Later, validate
result = step.validate()
if result.is_valid:
    print("Step is valid")
```

---

### ConverterGUI (`src/converter_gui.py`)

**Purpose**: Multi-step wizard orchestrator (7 steps). Reduced from 1,400+ lines to 750 lines in Phase D refactoring.

**Responsibilities**:
- Orchestrates UI workflow
- Manages wizard step navigation
- Delegates business logic to companion classes
- Coordinates data flow between steps

**Companion Classes**:
- `BalanceManager` - Balance calculations
- `ConversionHandler` - CSV to OFX conversion
- `TransactionManager` - Transaction operations

**Wizard Steps** (all extracted to `gui_steps/` package):
1. `FileSelectionStep` - File selection
2. `CSVFormatStep` - CSV format configuration (delimiter, decimal separator)
3. `DataPreviewStep` - Data preview (Treeview showing first 100 rows)
4. `OFXConfigStep` - OFX configuration (account ID, bank name, currency, initial balance)
5. `FieldMappingStep` - Field mapping with composite description support (combine up to 4 columns)
6. `AdvancedOptionsStep` - Advanced options (value inversion, date validation with Keep/Adjust/Exclude)
7. `BalancePreviewStep` - Balance preview & confirmation (shows balance summary and transaction preview)

**Design Pattern**:
- Uses Tkinter ttk widgets for modern appearance
- Step-by-step validation before progression
- Back/Next navigation
- Clear separation between UI and business logic

---

## Data Flow

```
CSV File → CSVParser.parse_file()
  ↓
  Preview in GUI (Step 3: DataPreviewStep)
  ↓
  User maps columns (Step 5: FieldMappingStep)
  ↓
  OFXGenerator.add_transaction() (with optional DateValidator)
  ↓
  OFXGenerator.generate()
  ↓
  OFX File
```

**Detailed Flow**:

1. **File Selection** (Step 1):
   - User selects CSV file
   - File path stored in `self.csv_file`

2. **CSV Format Configuration** (Step 2):
   - User selects delimiter (comma, semicolon, tab, pipe)
   - User selects decimal separator (dot, comma)
   - CSV parsed with selected format

3. **Data Preview** (Step 3):
   - CSV parsed using CSVParser
   - First 100 rows displayed in Treeview
   - Headers extracted for field mapping

4. **OFX Configuration** (Step 4):
   - User enters account ID, bank name
   - User selects currency (BRL, USD, EUR, etc.)
   - User enters initial balance

5. **Field Mapping** (Step 5):
   - User maps CSV columns to OFX fields (date, amount, description, type, ID)
   - User can create composite descriptions (up to 4 columns)
   - User selects separator for composite descriptions

6. **Advanced Options** (Step 6):
   - User enables/disables value inversion
   - User configures date validation (statement start/end dates)
   - User selects date action for out-of-range transactions (Keep/Adjust/Exclude)

7. **Balance Preview & Conversion** (Step 7):
   - BalanceManager calculates balance preview
   - User reviews transaction list and balance summary
   - User can delete unwanted transactions
   - User can restore deleted transactions
   - User clicks "Convert" to generate OFX file
   - ConversionHandler orchestrates conversion
   - OFX file saved to disk

---

## Important Implementation Details

### Value Inversion

When enabled, OFXGenerator multiplies all amounts by -1 and swaps DEBIT↔CREDIT types. This is handled in `add_transaction()` before type-based sign adjustments.

**Use Case**: Some banks record transactions with opposite signs (debits as positive, credits as negative). Value inversion corrects this.

**Implementation** (`ofx_generator.py:add_transaction()`):
```python
if self.invert_values:
    amount = -amount
    if transaction_type == "DEBIT":
        transaction_type = "CREDIT"
    elif transaction_type == "CREDIT":
        transaction_type = "DEBIT"
```

---

### Composite Descriptions

GUI allows combining up to 4 columns with a separator (space, dash, comma, pipe). The combined string is passed as the `description` parameter to `add_transaction()`.

**Example**:
- Columns: ["Merchant", "Location", "Category"]
- Separator: " - "
- Result: "Restaurant - Downtown - Food"

**Implementation** (`transaction_utils.py:build_transaction_description()`):
```python
def build_transaction_description(row, description_columns, separator, headers):
    parts = []
    for col_index in description_columns:
        if 0 <= col_index < len(row):
            value = row.get(headers[col_index], "").strip()
            if value:
                parts.append(value)
    return separator.join(parts) if parts else "N/A"
```

---

### Date Validation Dialog

When a transaction falls outside the statement period, GUI displays a dialog with three options:

1. **Keep original date** (use as-is) - Transaction included with original date
2. **Adjust to boundary** (move to start_date or end_date) - Date adjusted to nearest boundary
3. **Exclude transaction** (skip it entirely) - Transaction not included in OFX file

**Implementation Flow**:
1. DateValidator checks if date is within range
2. If outside range, TransactionManager.show_out_of_range_dialog() displays decision dialog
3. User selects action
4. ConversionHandler processes transaction based on user's choice

---

### OFX Format

Generates credit card statement format (CREDITCARDMSGSRSV1) with:

**Header**:
- OFX version: 102
- SGML format (not XML)
- Data encoding: UTF-8
- Character set: 1252

**Sign-on Message**:
- Bank name
- Organization ID (FID)
- Language: ENG

**Statement**:
- Account ID
- Currency
- Statement start/end dates
- Initial balance (optional)

**Transaction List (BANKTRANLIST)**:
- Start date (DTSTART)
- End date (DTEND)
- Individual transactions (STMTTRN):
  - Type (TRNTYPE): DEBIT or CREDIT
  - Date (DTPOSTED): YYYYMMDD format
  - Amount (TRNAMT): Negative for debits, positive for credits
  - Transaction ID (FITID): UUID if not provided
  - Description (MEMO): Max 255 characters

**Example OFX Output**:
```
OFXHEADER:100
DATA:OFXSGML
VERSION:102
SECURITY:NONE
ENCODING:UTF-8
CHARSET:1252
COMPRESSION:NONE
OLDFILEUID:NONE
NEWFILEUID:NONE

<OFX>
<SIGNONMSGSRSV1>
<SONRS>
<STATUS>
<CODE>0</CODE>
<SEVERITY>INFO</SEVERITY>
</STATUS>
<DTSERVER>20250115120000</DTSERVER>
<LANGUAGE>ENG</LANGUAGE>
</SONRS>
</SIGNONMSGSRSV1>
<CREDITCARDMSGSRSV1>
<CCSTMTTRNRS>
<TRNUID>1</TRNUID>
<STATUS>
<CODE>0</CODE>
<SEVERITY>INFO</SEVERITY>
</STATUS>
<CCSTMTRS>
<CURDEF>BRL</CURDEF>
<CCACCTFROM>
<ACCTID>1234567890</ACCTID>
</CCACCTFROM>
<BANKTRANLIST>
<DTSTART>20250101</DTSTART>
<DTEND>20250131</DTEND>
<STMTTRN>
<TRNTYPE>DEBIT</TRNTYPE>
<DTPOSTED>20250115</DTPOSTED>
<TRNAMT>-50.00</TRNAMT>
<FITID>abc123</FITID>
<MEMO>Restaurant - Downtown</MEMO>
</STMTTRN>
</BANKTRANLIST>
<LEDGERBAL>
<BALAMT>950.00</BALAMT>
<DTASOF>20250131</DTASOF>
</LEDGERBAL>
</CCSTMTRS>
</CCSTMTTRNRS>
</CREDITCARDMSGSRSV1>
</OFX>
```

---

### Logging

Application logs to both:
- **File**: `csv_to_ofx_converter.log` (INFO level)
- **Console**: stdout (INFO level)

Logger is configured in `src/csv_to_ofx_converter.py` main module.

**Log Format**:
```
2025-01-15 12:00:00,123 - INFO - CSVParser: Parsed 150 rows from file
2025-01-15 12:00:01,456 - INFO - OFXGenerator: Added 150 transactions
2025-01-15 12:00:02,789 - INFO - OFXGenerator: Generated OFX file successfully
```

**Usage in Code**:
```python
import logging
logger = logging.getLogger(__name__)

logger.info("Operation successful")
logger.warning("Potential issue detected")
logger.error("Operation failed")
```

---

## Build System

### PyInstaller Configuration (`csv_to_ofx_converter.spec`)

**Entry Point**: `main.py`

**Bundled Files**:
- README.md
- README.pt-BR.md
- LICENSE

**Configuration**:
- Console mode: False (GUI app, no terminal window)
- Single-file executable: Yes
- UPX compression: Yes
- Output name: `csv-to-ofx-converter`

**Platform-Specific Builds**:
- Linux: `csv-to-ofx-converter-linux-x64`
- Windows: `csv-to-ofx-converter-windows-x64.exe`
- macOS: `csv-to-ofx-converter-macos-x64`

**Build Command**:
```bash
pyinstaller csv_to_ofx_converter.spec
```

---

### GitHub Actions (`.github/workflows/`)

#### `build-and-release.yml`

**Trigger**: Push tag matching `v*.*.*` pattern

**Jobs**: Multi-platform builds (Linux, macOS, Windows) with matrix strategy

**Steps**:
1. Checkout code
2. Set up Python 3.9
3. Install dependencies (PyInstaller)
4. Build executable using PyInstaller
5. Calculate SHA256 checksum
6. Upload artifacts
7. Create GitHub release (Linux job only)
8. Upload executables and checksums to release

**Matrix**:
```yaml
matrix:
  os: [ubuntu-latest, macos-latest, windows-latest]
  include:
    - os: ubuntu-latest
      output_name: csv-to-ofx-converter-linux-x64
    - os: macos-latest
      output_name: csv-to-ofx-converter-macos-x64
    - os: windows-latest
      output_name: csv-to-ofx-converter-windows-x64.exe
```

#### `sonar.yml`

**Trigger**: Push to main branch

**Purpose**: SonarCloud code quality analysis

**Steps**:
1. Checkout code with full history
2. Set up Python 3.9
3. Install dependencies
4. Run 215 tests (excludes GUI tests requiring display server)
5. Generate coverage report using coverage.py
6. Upload coverage to SonarCloud
7. Run SonarCloud scan

**Test Execution**:
```bash
# Excludes GUI tests that require display server
python3 -m unittest discover tests -v
```

**Excluded Tests** (253 total):
- `test_gui_integration.py` (15 tests) - Skipped (requires display)
- `test_gui_wizard_step.py` (32 tests) - Not executed (Tkinter imports fail in CI)
- `test_gui_steps/*` (206 tests) - Not executed (Tkinter imports fail in CI)

**Executed Tests** (215 total):
- All non-GUI tests (94 tests)
- GUI utility tests (121 tests) - Use mocks, no Tkinter dependencies

**Coverage Configuration**:
- Measured using coverage.py
- Report format: XML for SonarCloud
- Excludes: tests/, build/, dist/

**SonarCloud Configuration** (`sonar-project.properties`):
```properties
sonar.projectKey=your-org_csv-to-ofx-converter
sonar.organization=your-org
sonar.sources=src/
sonar.tests=tests/
sonar.python.coverage.reportPaths=coverage.xml
sonar.python.version=3.7, 3.8, 3.9, 3.10, 3.11
sonar.test.exclusions=tests/**
sonar.coverage.exclusions=tests/**,**/__init__.py
```

---

## Important Notes

- **No External Dependencies**: Application uses only Python standard library for runtime. PyInstaller is dev-only dependency for building executables.

- **Brazilian Format**: Semicolon delimiter, comma decimal separator. Examples: `01/10/2025;100,50;Compra`

- **OFX Version**: Generates OFX 1.0.2 SGML format (not the newer XML format). Uses CREDITCARDMSGSRSV1 message type.

- **Encoding**: All CSV files read as UTF-8 with BOM handling.

- **Account Type**: Currently only supports credit card statements. Does not support checking/savings accounts (BANKMSGSRSV1) or investment accounts.

- **GUI Design**: Wizard follows step-by-step pattern with clear Back/Next navigation. Each step validates before allowing progression.

- **Cross-Platform**: Tested on Linux, macOS, and Windows. GUI uses Tkinter for native look and feel on each platform.
