# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CSV to OFX Converter - A Python application that converts CSV files to OFX (Open Financial Exchange) format, with full support for Brazilian banking formats. Features a Tkinter-based wizard interface with 6 steps guiding users through CSV import, data preview, field mapping, and conversion.

**Key characteristics:**
- Pure Python 3.7+ with standard library only (no external dependencies for runtime)
- GUI application using Tkinter
- Multi-step wizard interface with data preview
- Support for both standard (comma, dot) and Brazilian (semicolon, comma) CSV formats

## Development Commands

### Running the Application

```bash
# Run from source
python3 main.py
```

### Testing

```bash
# Run all tests
python3 -m unittest tests.test_converter

# Run with verbose output
python3 -m unittest tests.test_converter -v

# Run specific test classes
python3 -m unittest tests.test_converter.TestCSVParser
python3 -m unittest tests.test_converter.TestOFXGenerator
python3 -m unittest tests.test_converter.TestDateValidator
```

### Building Executables

```bash
# Install build dependency (PyInstaller)
pip install pyinstaller

# Build (Linux/macOS)
./build.sh

# Build (Windows)
build.bat

# Builds are controlled by csv_to_ofx_converter.spec
# Output goes to dist/ directory
```

## Code Architecture

### Module Structure

The codebase is organized into separate modules under `src/`:

```
main.py                    # Entry point, imports from src
src/
  csv_to_ofx_converter.py  # Main module, initializes logging and exports all classes
  csv_parser.py            # CSVParser class - handles CSV file parsing
  ofx_generator.py         # OFXGenerator class - generates OFX files
  date_validator.py        # DateValidator class - validates transaction dates
  converter_gui.py         # ConverterGUI class - Tkinter wizard interface
  constants.py             # Shared constants (NOT_MAPPED, NOT_SELECTED)
tests/
  test_converter.py        # Comprehensive test suite (39+ tests)
```

### Key Classes and Responsibilities

**CSVParser** (`src/csv_parser.py`):
- Parses CSV files with configurable delimiter and decimal separator
- Method `parse_file()` returns tuple of (headers, rows)
- Method `normalize_amount()` converts string amounts to floats, handling Brazilian format (1.234,56) and standard format (1,234.56)
- Handles UTF-8 and BOM encoding

**OFXGenerator** (`src/ofx_generator.py`):
- Generates OFX 1.0.2 format (SGML, not XML)
- Initialized with optional `invert_values` flag to swap debits/credits
- Method `add_transaction()` queues transactions
- Method `generate()` produces final OFX file with credit card statement format (CREDITCARDMSGSRSV1)
- Automatically infers transaction type from amount sign
- Generates UUID for transaction IDs if not provided
- Limits description to 255 characters per OFX spec

**DateValidator** (`src/date_validator.py`):
- Validates transaction dates against statement period (start_date to end_date)
- Method `is_within_range()` checks if date is valid
- Method `get_date_status()` returns 'before', 'within', or 'after'
- Method `adjust_date_to_boundary()` moves out-of-range dates to nearest boundary
- Supports multiple date formats (YYYY-MM-DD, DD/MM/YYYY, etc.)

**ConverterGUI** (`src/converter_gui.py`):
- Multi-step wizard interface (6 steps)
- Uses Tkinter ttk widgets for modern appearance
- Step 1: File selection
- Step 2: CSV format configuration (delimiter, decimal separator)
- Step 3: Data preview (Treeview showing first 100 rows)
- Step 4: OFX configuration (account ID, bank name, currency)
- Step 5: Field mapping with composite description support (combine up to 4 columns)
- Step 6: Advanced options (value inversion, date validation with Keep/Adjust/Exclude)
- Logs conversion progress to GUI text widget

### Data Flow

```
CSV File → CSVParser.parse_file()
  → Preview in GUI (Step 3)
  → User maps columns (Step 5)
  → OFXGenerator.add_transaction() (with optional DateValidator)
  → OFXGenerator.generate()
  → OFX File
```

### Important Implementation Details

**Value Inversion**: When enabled, OFXGenerator multiplies all amounts by -1 and swaps DEBIT↔CREDIT types. This is handled in `add_transaction()` before type-based sign adjustments.

**Composite Descriptions**: GUI allows combining up to 4 columns with separator (space, dash, comma, pipe). The combined string is passed as the `description` parameter to `add_transaction()`.

**Date Validation Dialog**: When a transaction falls outside the statement period, GUI displays a dialog with three options:
- Keep original date (use as-is)
- Adjust to boundary (move to start_date or end_date)
- Exclude transaction (skip it entirely)

**OFX Format**: Generates credit card statement format (CREDITCARDMSGSRSV1) with:
- Header: OFX version, SGML format
- Sign-on message with bank info
- Statement with account details
- Transaction list (BANKTRANLIST)
- Each transaction has: type, date, amount, UUID, memo

### Logging

Application logs to both:
- File: `csv_to_ofx_converter.log` (INFO level)
- Console: stdout (INFO level)

Logger is configured in `src/csv_to_ofx_converter.py` main module.

## Build System

**PyInstaller Configuration** (`csv_to_ofx_converter.spec`):
- Entry point: `main.py`
- Bundles README.md, README.pt-BR.md, LICENSE
- Console mode: False (GUI app, no terminal window)
- Single-file executable with UPX compression
- Output name: `csv-to-ofx-converter`

**GitHub Actions** (`.github/workflows/`):
- `build-and-release.yml`: Multi-platform builds (Linux, macOS, Windows) with matrix strategy
- `sonar.yml`: SonarCloud code quality analysis

## Testing Strategy

Test suite covers:
- CSV parsing (standard and Brazilian formats)
- Amount normalization with various edge cases
- Date parsing in multiple formats
- OFX generation and transaction formatting
- Value inversion logic
- Date validation (before/within/after range)
- Composite descriptions
- Error handling (missing files, invalid data)
- Integration tests for full conversion workflow

**Test Patterns**:
- Uses `unittest` framework
- Creates temporary files in `setUp()`, cleans in `tearDown()`
- Tests both positive cases and error conditions

## Common Patterns

**When adding new date formats**:
1. Add format string to `date_formats` list in both `OFXGenerator._parse_date()` and `DateValidator._parse_date_to_datetime()`
2. Add test case in `test_converter.py`

**When modifying GUI steps**:
- GUI step methods are named `_create_step_1()`, `_create_step_2()`, etc.
- Navigation handled by `_next_step()` and `_previous_step()`
- Step visibility controlled by `_show_step(step_number)`
- Validation happens in `_next_step()` before allowing progression

**When adding new OFX fields**:
- Modify `add_transaction()` signature in `OFXGenerator`
- Update transaction dictionary in `add_transaction()`
- Add field to OFX template in `generate()`
- Update GUI field mapping UI (Step 5)
- Add tests for new field

## Important Notes

- **No External Dependencies**: Application uses only Python standard library for runtime. PyInstaller is dev-only dependency for building executables.
- **Brazilian Format**: Semicolon delimiter, comma decimal separator. Examples: `01/10/2025;100,50;Compra`
- **OFX Version**: Generates OFX 1.0.2 SGML format (not the newer XML format). Uses CREDITCARDMSGSRSV1 message type.
- **Encoding**: All CSV files read as UTF-8 with BOM handling
- **Account Type**: Currently only supports credit card statements. Does not support checking/savings accounts (BANKMSGSRSV1) or investment accounts.
- **GUI Design**: Wizard follows step-by-step pattern with clear Back/Next navigation. Each step validates before allowing progression.

## Coding Style

- Follow PEP8 guidelines.
- Use descriptive variable and function names.
- Keep the code modular and easy to maintain.
- Separate classes in diferent files.
- Maintain consistency with the project’s existing structure and GUI framework.