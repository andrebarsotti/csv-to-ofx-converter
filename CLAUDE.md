# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CSV to OFX Converter - A Python application that converts CSV files to OFX (Open Financial Exchange) format, with full support for Brazilian banking formats. Features a Tkinter-based wizard interface with 7 steps guiding users through CSV import, data preview, field mapping, balance preview, and conversion.

**Current Version**: 3.0.0 (November 2025)

**Key characteristics:**
- Pure Python 3.7+ with standard library only (no external dependencies for runtime)
- GUI application using Tkinter with DPI awareness for Windows
- Multi-step wizard interface with data preview
- Support for both standard (comma, dot) and Brazilian (semicolon, comma) CSV formats
- Context menu for transaction management with date validation
- Automatic window maximization on startup (cross-platform compatible)

## Development Commands

### Running the Application

```bash
# Run from source
python3 main.py
```

### Testing

```bash
# Run all tests (recommended - discovers all test files)
python3 -m unittest discover tests

# Run with verbose output
python3 -m unittest discover tests -v

# Run specific test modules
python3 -m unittest tests.test_csv_parser
python3 -m unittest tests.test_ofx_generator
python3 -m unittest tests.test_date_validator
python3 -m unittest tests.test_transaction_utils
python3 -m unittest tests.test_integration

# Run specific test classes
python3 -m unittest tests.test_csv_parser.TestCSVParser
python3 -m unittest tests.test_ofx_generator.TestOFXGenerator
python3 -m unittest tests.test_date_validator.TestDateValidator
python3 -m unittest tests.test_transaction_utils.TestBuildTransactionDescription
python3 -m unittest tests.test_integration.TestIntegration

# Alternative: Run using convenience script
python3 tests/run_all_tests.py
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
  transaction_utils.py     # Utility functions for transaction processing (no UI dependencies)
  constants.py             # Shared constants (NOT_MAPPED, NOT_SELECTED)
tests/
  __init__.py              # Test package initialization
  test_csv_parser.py       # CSV parser tests (8 tests)
  test_ofx_generator.py    # OFX generator tests (20 tests)
  test_date_validator.py   # Date validator tests (12 tests)
  test_transaction_utils.py # Transaction utilities tests (50 tests)
  test_integration.py      # Integration tests (5 tests)
  run_all_tests.py         # Convenience script to run all tests
```

### Key Classes and Responsibilities

**CSVParser** (`src/csv_parser.py`):
- Parses CSV files with configurable delimiter and decimal separator
- Method `parse_file()` returns tuple of (headers, rows)
- Method `normalize_amount()` converts string amounts to floats, handling Brazilian format (1.234,56) and standard format (1,234.56)
- Supports negative amounts with currency symbols in any position: `-R$ 100,00`, `R$ -100,00`
- Supports parentheses notation for negative amounts: `(R$ 100,00)` = `-100.00`
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

**TransactionUtils** (`src/transaction_utils.py`):
- Pure utility functions with no UI dependencies (fully testable)
- Function `build_transaction_description()` creates single or composite descriptions from CSV columns
- Function `determine_transaction_type()` determines DEBIT/CREDIT from column value or amount sign
- Function `extract_transaction_id()` extracts transaction ID from mapped column
- Function `calculate_balance_summary()` computes balance totals from transaction list
- Function `validate_field_mappings()` validates required field mappings
- Function `parse_balance_value()` safely parses balance strings to floats with defaults

**ConverterGUI** (`src/converter_gui.py`):
- Multi-step wizard interface (7 steps)
- Uses Tkinter ttk widgets for modern appearance
- Step 1: File selection
- Step 2: CSV format configuration (delimiter, decimal separator)
- Step 3: Data preview (Treeview showing first 100 rows)
- Step 4: OFX configuration (account ID, bank name, currency, initial balance)
- Step 5: Field mapping with composite description support (combine up to 4 columns)
- Step 6: Advanced options (value inversion, date validation with Keep/Adjust/Exclude)
- Step 7: Balance preview & confirmation (shows balance summary and transaction preview)
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

Test suite is organized into separate modules (95 tests total):

**test_csv_parser.py** (8 tests):
- CSV parsing (standard and Brazilian formats)
- Amount normalization with various edge cases including negative values with currency symbols
- Support for parentheses notation for negative amounts
- BOM handling and error cases

**test_ofx_generator.py** (20 tests):
- OFX generation and transaction formatting
- Date parsing in multiple formats
- Value inversion logic
- Transaction sorting and auto-correction
- Multiple currency support

**test_date_validator.py** (12 tests):
- Date validation (before/within/after range)
- Date adjustment to boundaries
- Edge cases (year boundaries, leap years)

**test_transaction_utils.py** (50 tests):
- Building transaction descriptions (single column and composite)
- Determining transaction types from columns or amounts
- Extracting transaction IDs from row data
- Calculating balance summaries from transaction lists
- Validating field mappings
- Parsing balance values with fallback defaults
- Tests cover edge cases, empty values, and error handling

**test_integration.py** (5 tests):
- Complete end-to-end conversion workflows
- Composite descriptions with various separators
- Value inversion in full workflow

**Test Patterns**:
- Uses `unittest` framework with test discovery
- Creates temporary files in `setUp()`, cleans in `tearDown()`
- Tests both positive cases and error conditions
- Each test class in its own file for better maintainability
- Utility functions tested independently without UI dependencies

## Common Patterns

**When adding new date formats**:
1. Add format string to `date_formats` list in both `OFXGenerator._parse_date()` and `DateValidator._parse_date_to_datetime()`
2. Add test case in `test_ofx_generator.py` or `test_date_validator.py` as appropriate

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

**When extracting functions from GUI**:
- Create pure utility functions without UI dependencies in `transaction_utils.py`
- Functions should accept all needed data as parameters (no `self` access)
- Write comprehensive unit tests for each utility function
- Update GUI code to import and use the utility functions
- Ensure all tests pass after refactoring

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
- Maintain consistency with the project's existing structure and GUI framework.

## Documentation Requirements

**IMPORTANT**: When making changes to the codebase, ALWAYS update the relevant documentation files:

1. **CLAUDE.md** - This file:
   - Update module structure if files are added/removed/renamed
   - Update test commands if test organization changes
   - Add new sections for new features or patterns
   - Keep test counts accurate

2. **README.md** (English):
   - Update usage instructions for user-facing changes
   - Update test commands if test structure changes
   - Add examples for new features
   - Keep feature list up to date

3. **README.pt-BR.md** (Portuguese):
   - Mirror all changes from README.md
   - Maintain translation consistency
   - Ensure examples are culturally appropriate

4. **Code Comments and Docstrings**:
   - Update docstrings when function signatures change
   - Keep inline comments accurate
   - Document non-obvious logic

**When adding tests**:
- Place in the appropriate test module (test_csv_parser.py, test_ofx_generator.py, etc.)
- Update test counts in documentation
- Ensure test discovery works: `python3 -m unittest discover tests`
## Release Process

**IMPORTANT**: Follow the comprehensive checklist in `RELEASE_CHECKLIST.md` for all releases.

### Pre-Release Verification

Before creating a release, ensure all of the following are complete:

1. **Code Quality & Testing**:
   - All tests passing: `python3 -m unittest discover tests -v`
   - Verify 95 tests run successfully
   - Test individual modules work correctly
   - Code follows PEP8 standards
   - No debugging code or print statements

2. **Documentation Updates**:
   - **CLAUDE.md**: Update module structure, test counts, new features
   - **README.md**: Update version, changelog, examples, last updated date
   - **README.pt-BR.md**: Mirror all changes from README.md in Portuguese
   - **RELEASE_CHECKLIST.md**: Update if release process changed
   - All code comments and docstrings are accurate

3. **Version Management**:
   - Decide version number using semantic versioning:
     - **Patch** (1.0.X): Bug fixes only
     - **Minor** (1.X.0): New features, backward compatible
     - **Major** (X.0.0): Breaking changes
   - Update version in README.md and README.pt-BR.md
   - Update changelog in both README files

4. **Functional Testing**:
   - Test with sample CSV files (both Brazilian and standard formats)
   - Test date validation feature
   - Verify OFX output in financial software
   - Test error handling
   - Test GUI on target platform if possible

5. **Build Testing**:
   - Local build succeeds: `./build.sh` (Linux/macOS) or `build.bat` (Windows)
   - Executable runs without errors
   - Executable size is reasonable (< 50MB)
   - GUI elements render correctly

### Release Steps

1. **Prepare Repository**:
   ```bash
   # Ensure everything is committed and up to date
   git status  # Should be clean
   git pull origin main
   ```

2. **Create and Push Tag**:
   ```bash
   # Create annotated tag with version
   git tag -a v1.x.x -m "Release version 1.x.x: Brief description"

   # Push tag to trigger GitHub Actions workflow
   git push origin v1.x.x
   ```

3. **Monitor Build**:
   - Go to GitHub Actions: `https://github.com/YOUR_USERNAME/csv-to-ofx-converter/actions`
   - Watch workflow execution for all platforms:
     - Ubuntu (Linux x64)
     - Windows (x64)
     - macOS (x64)
   - Verify all jobs complete successfully
   - Check for errors in logs

4. **Verify Release**:
   - Check Release page for new release
   - Verify all executables are attached:
     - `csv-to-ofx-converter-linux-x64`
     - `csv-to-ofx-converter-windows-x64.exe`
     - `csv-to-ofx-converter-macos-x64`
   - Verify checksums file is attached
   - Verify release notes are complete
   - Test download links work

5. **Post-Release Testing**:
   - Download and test each platform's executable
   - Verify SHA256 checksums match
   - Test functionality on actual system

### Rollback Procedure

If issues are discovered after release:

```bash
# Delete the release on GitHub (via web interface)

# Delete local tag
git tag -d v1.x.x

# Delete remote tag
git push origin :refs/tags/v1.x.x

# Fix issues, commit, and create new tag
git tag -a v1.x.y -m "Release version 1.x.y: Bug fixes"
git push origin v1.x.y
```

### Important Files for Releases

1. **RELEASE_CHECKLIST.md**: Complete step-by-step checklist
2. **README.md**: Version number, changelog, last updated date
3. **README.pt-BR.md**: Version number, changelog (Portuguese)
4. **CLAUDE.md**: Technical documentation updates
5. **.github/workflows/build-and-release.yml**: Automated build workflow

### Release Notes Template

Include in git tag message and GitHub release:

```markdown
Release version X.Y.Z: Brief title

Changes:
- New Feature: Description of feature
- Bug Fix: Description of fix
- Improvement: Description of improvement
- Documentation: Updates to docs

Testing:
- All 95 tests passing
- Tested on [platforms]
- Compatible with [software versions]
```

### Quick Release Reference

```bash
# 1. Run tests
python3 -m unittest discover tests -v

# 2. Update documentation (README.md, README.pt-BR.md, CLAUDE.md)

# 3. Commit changes
git add -A
git commit -m "chore: Prepare release v1.x.x"
git push origin main

# 4. Create and push tag
git tag -a v1.x.x -m "Release v1.x.x: Description"
git push origin v1.x.x

# 5. Monitor GitHub Actions and verify release
```

**Remember**: Always consult `RELEASE_CHECKLIST.md` for the complete and detailed release process.
