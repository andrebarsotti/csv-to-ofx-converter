# Testing Strategy

This document provides comprehensive testing information for the CSV to OFX Converter application.

## Test Suite Overview

Test suite is organized into separate modules: **499 tests total** (January 2026)

**Test Organization**:
```
tests/
├── __init__.py                      # Test package initialization
├── test_csv_parser.py               # 8 tests - CSV parsing
├── test_ofx_generator.py            # 21 tests - OFX generation
├── test_date_validator.py           # 12 tests - Date validation
├── test_transaction_utils.py        # 68 tests - Transaction utilities (includes deterministic FITID coverage)
├── test_gui_utils.py                # 63 tests - GUI utilities
├── test_gui_integration.py          # 15 tests - GUI integration
├── test_gui_balance_manager.py      # 14 tests - Balance manager
├── test_gui_conversion_handler.py   # 23 tests - Conversion handler
├── test_gui_transaction_manager.py  # 26 tests - Transaction manager
├── test_gui_wizard_step.py          # 32 tests - WizardStep base class
├── test_integration.py              # 11 tests - End-to-end integration
├── test_gui_steps/                  # 206 tests - Wizard step implementations
│   ├── __init__.py
│   ├── test_file_selection_step.py  # 24 tests
│   ├── test_csv_format_step.py      # 21 tests
│   ├── test_data_preview_step.py    # 35 tests
│   ├── test_ofx_config_step.py      # 20 tests
│   ├── test_field_mapping_step.py   # 38 tests
│   ├── test_advanced_options_step.py # 39 tests
│   └── test_balance_preview_step.py # 29 tests
└── run_all_tests.py                 # Convenience script
```

---

## Running Tests

### All Tests

```bash
# Recommended - discovers all test files
python3 -m unittest discover tests

# With verbose output
python3 -m unittest discover tests -v

# Alternative: Using convenience script
python3 tests/run_all_tests.py
```

### Specific Test Modules

```bash
# CSV parsing tests
python3 -m unittest tests.test_csv_parser

# OFX generation tests
python3 -m unittest tests.test_ofx_generator

# Date validation tests
python3 -m unittest tests.test_date_validator

# Transaction utilities tests
python3 -m unittest tests.test_transaction_utils

# GUI utilities tests
python3 -m unittest tests.test_gui_utils

# GUI integration tests (requires display server)
python3 -m unittest tests.test_gui_integration

# Balance manager tests
python3 -m unittest tests.test_gui_balance_manager

# Conversion handler tests
python3 -m unittest tests.test_gui_conversion_handler

# Transaction manager tests
python3 -m unittest tests.test_gui_transaction_manager

# WizardStep base class tests
python3 -m unittest tests.test_gui_wizard_step

# Integration tests
python3 -m unittest tests.test_integration

# Wizard step tests
python3 -m unittest tests.test_gui_steps.test_file_selection_step
python3 -m unittest tests.test_gui_steps.test_csv_format_step
python3 -m unittest tests.test_gui_steps.test_data_preview_step
python3 -m unittest tests.test_gui_steps.test_ofx_config_step
python3 -m unittest tests.test_gui_steps.test_field_mapping_step
python3 -m unittest tests.test_gui_steps.test_advanced_options_step
python3 -m unittest tests.test_gui_steps.test_balance_preview_step
```

### Specific Test Classes

```bash
# CSV parser test class
python3 -m unittest tests.test_csv_parser.TestCSVParser

# OFX generator test class
python3 -m unittest tests.test_ofx_generator.TestOFXGenerator

# Date validator test class
python3 -m unittest tests.test_date_validator.TestDateValidator

# Transaction description builder tests
python3 -m unittest tests.test_transaction_utils.TestBuildTransactionDescription

# WizardStep lifecycle tests
python3 -m unittest tests.test_gui_wizard_step.TestWizardStepLifecycle
```

### Pattern-Based Testing

```bash
# Run only CSV-related tests
python3 -m unittest discover tests -p "test_csv*.py"

# Run only OFX-related tests
python3 -m unittest discover tests -p "test_ofx*.py"

# Run only GUI utility tests (no display required)
python3 -m unittest discover tests -p "test_gui_utils*.py"

# Skip GUI integration tests during development
python3 -m unittest discover tests -k "not gui_integration"
```

---

## Test Module Details

### test_csv_parser.py (8 tests)

**Coverage**:
- CSV parsing with standard and Brazilian formats
- Amount normalization with various edge cases
- Negative values with currency symbols in any position
- Parentheses notation for negative amounts
- BOM handling
- Error cases (file not found, invalid format)

**Test Cases**:
```python
test_parse_standard_format()          # Comma delimiter, dot decimal
test_parse_brazilian_format()         # Semicolon delimiter, comma decimal
test_normalize_amount_standard()      # "1,234.56" → 1234.56
test_normalize_amount_brazilian()     # "1.234,56" → 1234.56
test_normalize_negative_with_symbol() # "-R$ 100,00" → -100.00
test_normalize_parentheses()          # "(R$ 100,00)" → -100.00
test_bom_handling()                   # UTF-8 BOM properly handled
test_file_not_found()                 # Raises appropriate exception
```

---

### test_ofx_generator.py (21 tests)

**Coverage**:
- OFX generation and transaction formatting
- Date parsing in multiple formats
- Value inversion logic
- Transaction sorting and auto-correction
- Multiple currency support
- Transaction type handling (DEBIT/CREDIT)

**Test Cases**:
```python
test_add_transaction()                # Basic transaction addition
test_generate_ofx()                   # OFX file generation
test_date_format_iso()                # YYYY-MM-DD format
test_date_format_brazilian()          # DD/MM/YYYY format
test_date_format_us()                 # MM/DD/YYYY format
test_value_inversion()                # Invert values flag
test_transaction_sorting()            # Transactions sorted by date
test_auto_correct_amounts()           # DEBIT amounts become negative
test_multiple_currencies()            # BRL, USD, EUR support
test_transaction_id_generation()      # UUID generation for missing IDs
test_description_truncation()         # Limit to 255 characters
# ... 8 more tests
```

---

### test_date_validator.py (12 tests)

**Coverage**:
- Date validation (before/within/after range)
- Date adjustment to boundaries
- Edge cases (year boundaries, leap years)
- Multiple date format parsing

**Test Cases**:
```python
test_is_within_range_valid()          # Date within range
test_is_within_range_before()         # Date before start
test_is_within_range_after()          # Date after end
test_get_date_status_before()         # Returns 'before'
test_get_date_status_within()         # Returns 'within'
test_get_date_status_after()          # Returns 'after'
test_adjust_to_start_boundary()       # Adjust date to start
test_adjust_to_end_boundary()         # Adjust date to end
test_year_boundary_handling()         # Dates across year boundaries
test_leap_year_handling()             # Feb 29 in leap years
test_invalid_date_format()            # Raises exception
test_date_format_variations()         # Multiple format support
```

---

### test_transaction_utils.py (68 tests)

**Coverage**:
- Building transaction descriptions (single column and composite)
- Determining transaction types from columns or amounts
- Extracting transaction IDs from row data
- Calculating balance summaries from transaction lists
- Validating field mappings
- Parsing balance values with fallback defaults
- Edge cases, empty values, and error handling

**Test Case Categories**:
```python
# Description building (15 tests)
test_single_column_description()
test_composite_description_two_columns()
test_composite_description_four_columns()
test_composite_with_empty_values()
test_separator_variations()
# ... 10 more

# Transaction type determination (12 tests)
test_determine_type_from_column_debit()
test_determine_type_from_column_credit()
test_determine_type_from_amount_negative()
test_determine_type_from_amount_positive()
test_type_column_case_insensitive()
# ... 7 more

# Transaction ID extraction (8 tests)
test_extract_id_from_column()
test_extract_id_missing_column()
test_extract_id_empty_value()
# ... 5 more

# Balance calculations (10 tests)
test_calculate_balance_summary()
test_balance_with_mixed_transactions()
test_balance_with_deleted_transactions()
# ... 7 more

# Field mapping validation (5 tests)
test_validate_required_fields()
test_validate_missing_date_field()
test_validate_missing_amount_field()
# ... 2 more
```

---

### test_gui_utils.py (63 tests)

**Coverage**:
- File validation
- Field mapping validation
- Date formatting
- Numeric validation
- Balance calculations
- Date parsing for sorting
- Conversion validation
- Statistics formatting
- Edge cases

**Test Case Categories**:
```python
# File validation (8 tests)
test_validate_file_exists()
test_validate_file_readable()
test_validate_file_not_empty()
# ... 5 more

# Field mapping validation (12 tests)
test_validate_required_mappings()
test_validate_date_field_mapped()
test_validate_amount_field_mapped()
# ... 9 more

# Date formatting (10 tests)
test_format_date_iso()
test_format_date_brazilian()
test_format_date_us()
# ... 7 more

# Numeric validation (8 tests)
test_validate_positive_number()
test_validate_negative_number()
test_validate_zero()
# ... 5 more

# Balance calculations (10 tests)
test_calculate_final_balance()
test_calculate_with_initial_balance()
test_calculate_with_deleted_transactions()
# ... 7 more

# Statistics formatting (10 tests)
test_format_transaction_count()
test_format_percentage()
test_format_currency_amount()
# ... 7 more
```

---

### test_gui_integration.py (15 tests)

**Coverage**:
- GUI wizard navigation
- Data loading workflows
- Field mapping workflows
- Integration between GUI components

**Note**: Skipped in CI environments without display server (requires Tkinter display connection).

**Test Cases**:
```python
test_wizard_initialization()          # GUI window creation
test_step_navigation_forward()        # Next button navigation
test_step_navigation_backward()       # Back button navigation
test_file_selection_workflow()        # File selection step
test_csv_format_configuration()       # CSV format step
test_data_preview_loading()           # Data preview step
test_ofx_configuration()              # OFX config step
test_field_mapping_workflow()         # Field mapping step
test_advanced_options_workflow()      # Advanced options step
test_balance_preview_workflow()       # Balance preview step
test_validation_before_progression()  # Step validation
test_data_persistence_across_steps()  # Data persists
test_back_button_preserves_data()     # Back navigation preserves data
test_conversion_workflow()            # End-to-end conversion
test_error_handling()                 # Error display
```

---

### test_gui_balance_manager.py (14 tests)

**Coverage**:
- Balance calculations with various transaction sets
- Preview generation with different currencies
- Balance input validation
- Date status checking
- Edge cases: empty transactions, deleted transactions, value inversion

**Test Cases**:
```python
test_calculate_balance_preview()         # Basic calculation
test_balance_with_initial_amount()       # Initial balance included
test_balance_with_deleted_transactions() # Deleted transactions excluded
test_balance_with_value_inversion()      # Inverted values
test_format_balance_labels()             # Label formatting
test_multiple_currencies()               # BRL, USD, EUR
test_empty_transaction_list()            # No transactions
test_validate_balance_input_valid()      # Valid balance input
test_validate_balance_input_invalid()    # Invalid balance input
test_date_status_checking()              # Date status determination
# ... 4 more tests
```

---

### test_gui_conversion_handler.py (23 tests)

**Coverage**:
- Conversion workflow with standard and Brazilian CSV formats
- Row processing with deleted transactions and value inversion
- Date validation scenarios (keep, adjust, exclude actions)
- Description building (single and composite columns)
- Transaction type and ID determination
- Error handling for malformed data and invalid date ranges

**Test Cases**:
```python
test_convert_standard_csv()              # Standard format conversion
test_convert_brazilian_csv()             # Brazilian format conversion
test_process_csv_rows()                  # Row processing
test_process_with_deleted_transactions() # Skip deleted rows
test_process_with_value_inversion()      # Value inversion
test_validate_date_within_range()        # Date validation
test_validate_date_keep_action()         # Keep original date
test_validate_date_adjust_action()       # Adjust to boundary
test_validate_date_exclude_action()      # Exclude transaction
test_build_single_description()          # Single column description
test_build_composite_description()       # Multi-column description
test_determine_type_from_column()        # Type from column
test_determine_type_from_amount()        # Type from amount sign
test_extract_transaction_id()            # ID extraction
test_generate_ofx_file()                 # OFX generation
test_error_handling_malformed_data()     # Malformed CSV
test_error_handling_invalid_date_range() # Invalid dates
# ... 6 more tests
```

---

### test_gui_transaction_manager.py (26 tests)

**Coverage**:
- Transaction manager initialization with parent GUI
- Context menu creation for valid and out-of-range transactions
- Transaction CRUD operations (delete single/multiple, restore all)
- Getting selected row info from Treeview
- Date status determination for transactions
- Date action handling (keep/adjust/exclude)
- Date action menu item creation based on current selection
- Out-of-range dialog display logic
- Uses mock Treeview and parent GUI to avoid display dependencies

**Test Cases**:
```python
test_manager_initialization()            # Manager creation
test_show_context_menu_valid_date()      # Context menu for valid transaction
test_show_context_menu_out_of_range()    # Context menu for out-of-range
test_delete_single_transaction()         # Delete one transaction
test_delete_multiple_transactions()      # Delete multiple transactions
test_restore_all_transactions()          # Restore deleted
test_get_selected_row_info()             # Row info extraction
test_determine_date_status()             # Date status check
test_handle_keep_date_action()           # Keep action
test_handle_adjust_date_action()         # Adjust action
test_handle_exclude_date_action()        # Exclude action
test_create_keep_date_menu_item()        # Keep menu item
test_create_adjust_date_menu_item()      # Adjust menu item
test_create_exclude_date_menu_item()     # Exclude menu item
test_show_out_of_range_dialog()          # Dialog display
# ... 11 more tests
```

---

### test_gui_wizard_step.py (32 tests)

**Coverage**:
- WizardStep base class lifecycle (create, show, hide, destroy)
- StepConfig and StepData dataclasses
- Helper methods (get_parent_data, set_parent_data, log)
- Validation orchestration
- Concrete implementation with MockWizardStep

**Test Cases**:
```python
test_step_initialization()               # Step creation
test_step_create()                       # UI creation
test_step_show()                         # Show step
test_step_hide()                         # Hide step
test_step_destroy()                      # Destroy step
test_step_validate()                     # Validation
test_get_parent_data()                   # Get data from parent
test_set_parent_data()                   # Set data in parent
test_log_message()                       # Logging
test_step_config_dataclass()             # StepConfig
test_step_data_dataclass()               # StepData
test_abstract_methods_enforcement()      # Abstract method enforcement
test_lifecycle_sequence()                # Full lifecycle
test_validation_failure()                # Validation fails
test_validation_success()                # Validation succeeds
# ... 17 more tests
```

---

### test_integration.py (11 tests)

**Coverage**:
- Complete end-to-end conversion workflows
- Composite descriptions with various separators
- Value inversion in full workflow
- Brazilian and standard CSV formats

**Test Cases**:
```python
test_end_to_end_standard_csv()          # Standard CSV → OFX
test_end_to_end_brazilian_csv()         # Brazilian CSV → OFX
test_composite_description_workflow()   # Multi-column descriptions
test_value_inversion_workflow()         # Value inversion
test_date_validation_workflow()         # Date validation integration
```

---

### test_gui_steps/ (206 tests - Phase D complete)

**Test Files**:

#### test_file_selection_step.py (24 tests)
- File selection UI creation
- Browse button functionality
- File path validation
- Data collection
- File existence validation

#### test_csv_format_step.py (31 tests)
- CSV format configuration UI
- Delimiter selection (comma, semicolon, tab, pipe)
- Decimal separator selection (dot, comma)
- Format preview generation
- Data collection
- Validation

#### test_data_preview_step.py (31 tests)
- Data preview Treeview creation
- Column display
- Row pagination (first 100 rows)
- Scrollbar functionality
- Data loading
- Header extraction

#### test_ofx_config_step.py (40 tests)
- OFX configuration UI
- Account ID entry
- Bank name entry
- Currency selection (BRL, USD, EUR, etc.)
- Initial balance entry
- Statement date entry
- Validation

#### test_field_mapping_step.py (38 tests)
- Field mapping UI
- Column selection for date, amount, description, type, ID
- Composite description configuration (up to 4 columns)
- Separator selection (space, dash, comma, pipe)
- Validation (required fields)

#### test_advanced_options_step.py (30 tests)
- Value inversion checkbox
- Date validation enable/disable
- Statement start/end date entry
- Date action selection (Keep/Adjust/Exclude)
- Date entry formatting
- Validation

#### test_balance_preview_step.py (29 tests)
- Balance calculation and display
- Transaction preview Treeview
- Transaction deletion (single and multiple)
- Transaction restoration
- Balance summary display
- Conversion button
- Data collection

---

## Test Patterns

### Standard Test Pattern

All test classes follow this pattern:

```python
import unittest
import tempfile
import os

class TestFeature(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test"""
        # Create temporary files
        self.temp_dir = tempfile.mkdtemp()
        self.csv_file = os.path.join(self.temp_dir, "test.csv")

        # Write test data
        with open(self.csv_file, 'w') as f:
            f.write("date,amount,description\n")
            f.write("2025-01-15,-50.00,Restaurant\n")

    def tearDown(self):
        """Clean up after each test"""
        # Remove temporary files
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_feature(self):
        """Test specific feature"""
        # Arrange
        expected = "expected result"

        # Act
        actual = feature_function()

        # Assert
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()
```

### GUI Test Pattern (with mocks)

GUI component tests use mocks to avoid display server dependencies:

```python
import unittest
from unittest.mock import Mock, MagicMock, patch
from tkinter import Tk, Frame
from src.gui_balance_manager import BalanceManager

class TestBalanceManager(unittest.TestCase):
    def setUp(self):
        """Set up mock parent GUI"""
        self.mock_parent = Mock()
        self.mock_parent.logger = Mock()
        self.mock_parent.data = {}
        self.manager = BalanceManager(self.mock_parent)

    def test_calculate_balance(self):
        """Test balance calculation"""
        transactions = [
            {"amount": -50.00, "deleted": False},
            {"amount": 30.00, "deleted": False}
        ]

        result = self.manager.calculate_balance_preview(
            transactions=transactions,
            initial_balance=100.00,
            currency="BRL"
        )

        self.assertEqual(result.final_balance, 80.00)
```

### Integration Test Pattern

Integration tests verify complete workflows:

```python
import unittest
import tempfile
import os
from src.csv_parser import CSVParser
from src.ofx_generator import OFXGenerator

class TestIntegration(unittest.TestCase):
    def test_csv_to_ofx_workflow(self):
        """Test complete CSV to OFX conversion"""
        # Arrange: Create test CSV
        temp_dir = tempfile.mkdtemp()
        csv_file = os.path.join(temp_dir, "test.csv")
        ofx_file = os.path.join(temp_dir, "output.ofx")

        with open(csv_file, 'w') as f:
            f.write("date,amount,description\n")
            f.write("2025-01-15,-50.00,Restaurant\n")

        # Act: Parse CSV and generate OFX
        parser = CSVParser()
        headers, rows = parser.parse_file(csv_file)

        generator = OFXGenerator("MyBank", "12345", "BRL")
        for row in rows:
            generator.add_transaction(
                date=row[0],
                amount=float(row[1]),
                description=row[2]
            )

        ofx_content = generator.generate("2025-01-01", "2025-01-31")

        with open(ofx_file, 'w') as f:
            f.write(ofx_content)

        # Assert: Verify OFX file
        self.assertTrue(os.path.exists(ofx_file))
        with open(ofx_file) as f:
            content = f.read()
            self.assertIn("OFXHEADER:100", content)
            self.assertIn("<TRNAMT>-50.00</TRNAMT>", content)

        # Cleanup
        import shutil
        shutil.rmtree(temp_dir)
```

---

## CI/CD Testing

### GitHub Actions SonarCloud Workflow

**File**: `.github/workflows/sonar.yml`

**Trigger**: Push to main branch

**Test Execution**:
```bash
# Runs 246 tests (excludes GUI tests requiring display server)
python3 -m unittest discover tests -v
```

**Excluded Tests** (253 total):
- `test_gui_integration.py` (15 tests) - Skipped via skipIf decorator (requires display)
- `test_gui_wizard_step.py` (32 tests) - Not executed (Tkinter import fails in CI)
- `test_gui_steps/*` (206 tests) - Not executed (Tkinter import fails in CI)

**Executed Tests** (246 total):
- All non-GUI tests (120 tests):
  - test_csv_parser.py (8)
  - test_ofx_generator.py (21)
  - test_date_validator.py (12)
  - test_transaction_utils.py (68)
  - test_integration.py (11)

- GUI utility tests without Tkinter dependencies (126 tests):
  - test_gui_utils.py (63)
  - test_gui_balance_manager.py (14)
  - test_gui_conversion_handler.py (23)
  - test_gui_transaction_manager.py (26)

**Coverage Report**:
- Generated using coverage.py
- Format: XML for SonarCloud
- Report path: `coverage.xml`
- Excludes: tests/, build/, dist/

**Running Coverage Locally**:
```bash
# Install coverage
pip install coverage

# Run tests with coverage
coverage run -m unittest discover tests

# Generate report
coverage report

# Generate HTML report
coverage html

# View report
open htmlcov/index.html
```

---

## Test Best Practices

### 1. Test Independence
- Each test should be independent and not rely on other tests
- Use setUp() to create fresh fixtures for each test
- Use tearDown() to clean up after each test

### 2. Descriptive Test Names
- Use descriptive test method names that explain what is being tested
- Pattern: `test_<feature>_<scenario>_<expected_result>()`
- Example: `test_normalize_amount_brazilian_format_returns_correct_float()`

### 3. AAA Pattern (Arrange, Act, Assert)
- **Arrange**: Set up test data and preconditions
- **Act**: Execute the code being tested
- **Assert**: Verify the results

### 4. Use Mocks for External Dependencies
- Mock file I/O, network requests, GUI components
- Use unittest.mock.Mock and unittest.mock.patch
- Avoid testing external dependencies, focus on your code

### 5. Test Both Success and Failure Cases
- Test happy path (valid inputs, expected behavior)
- Test edge cases (boundary values, empty inputs)
- Test error cases (invalid inputs, exceptions)

### 6. Keep Tests Focused
- Each test should test one specific behavior
- Avoid testing multiple features in one test
- If a test is complex, split it into multiple tests

### 7. Use Assertions Appropriately
- Use specific assertions (assertEqual, assertIn, assertRaises)
- Avoid assertTrue(x == y), use assertEqual(x, y)
- Include helpful assertion messages when needed

### 8. Temporary Files
- Always use tempfile module for temporary files
- Clean up temporary files in tearDown()
- Use context managers when appropriate

### 9. GUI Testing
- Use mocks to avoid display server dependencies
- Test business logic separately from UI rendering
- Use dependency injection to enable testing

### 10. Documentation
- Add docstrings to test methods explaining what is tested
- Document complex test setups
- Keep test code clean and readable

---

## Adding New Tests

When adding new functionality, follow this pattern:

1. **Create test file** (if new module):
   ```bash
   touch tests/test_new_feature.py
   ```

2. **Write test class**:
   ```python
   import unittest
   from src.new_feature import NewFeature

   class TestNewFeature(unittest.TestCase):
       def setUp(self):
           self.feature = NewFeature()

       def test_basic_functionality(self):
           result = self.feature.do_something()
           self.assertEqual(result, expected_value)
   ```

3. **Run tests**:
   ```bash
   python3 -m unittest tests.test_new_feature
   ```

4. **Update documentation**:
   - Add test count to this file (CLAUDE-TESTING.md)
   - Update total test count in CLAUDE.md
   - Update test count in README.md

5. **Verify in CI**:
   - Push to main branch
   - Check GitHub Actions SonarCloud workflow passes
   - Verify test appears in coverage report

---

## Troubleshooting Test Failures

### GUI Tests Failing Locally

**Problem**: GUI tests fail with Tkinter display errors

**Solution**:
```bash
# Use xvfb-run to provide virtual display
xvfb-run -a python3 -m unittest tests.test_gui_integration
```

### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'src'`

**Solution**:
```bash
# Run from project root, not tests/ directory
cd /path/to/csv-to-ofx-converter
python3 -m unittest discover tests
```

### Tests Pass Locally But Fail in CI

**Problem**: Tests pass on local machine but fail in GitHub Actions

**Solution**:
1. Check if test relies on local files or paths
2. Verify test doesn't require GUI display
3. Check Python version compatibility (CI uses 3.9)
4. Review CI logs for specific error messages

### Temporary Files Not Cleaned Up

**Problem**: Test failures leave temporary files

**Solution**:
```python
def tearDown(self):
    """Always clean up, even if test fails"""
    try:
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    except Exception as e:
        print(f"Cleanup failed: {e}")
```

### Tests Running Slowly

**Problem**: Test suite takes too long

**Solution**:
1. Run specific test modules during development
2. Use pattern matching to run subset of tests
3. Skip slow integration tests: `-k "not integration"`
4. Profile tests to identify slow ones

---

## Test Coverage Goals

**Current Coverage**: ~90% (excluding GUI rendering code)

**Coverage Goals**:
- Core business logic (csv_parser, ofx_generator): 100%
- Utility functions (transaction_utils, gui_utils): 100%
- Companion classes (managers, handlers): 95%
- GUI orchestration (converter_gui): 80%
- GUI steps: 85%

**Areas with Lower Coverage** (by design):
- Tkinter widget creation and rendering
- Window management and geometry
- Event loop handling
- Platform-specific GUI behavior

**Measuring Coverage**:
```bash
# Install coverage
pip install coverage

# Run with coverage
coverage run -m unittest discover tests

# Generate report
coverage report -m

# View detailed HTML report
coverage html
open htmlcov/index.html
```

---

## Quick Reference

**Run All Tests**: `python3 -m unittest discover tests`

**Run Specific Module**: `python3 -m unittest tests.test_csv_parser`

**Run With Coverage**: `coverage run -m unittest discover tests && coverage report`

**Skip GUI Tests**: `python3 -m unittest discover tests -k "not gui_integration"`

**Verbose Output**: `python3 -m unittest discover tests -v`

**Pattern Matching**: `python3 -m unittest discover tests -p "test_csv*.py"`
