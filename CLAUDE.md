# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Quick Navigation

**Essential Guides:**
- 🏗️ [Architecture Details](docs/CLAUDE-ARCHITECTURE.md) - Module structure, classes, data flow
- 🧪 [Testing Strategy](docs/CLAUDE-TESTING.md) - 499 tests, patterns, test organization
- 🚀 [Release Process](docs/CLAUDE-RELEASE.md) - Complete release checklist and procedures
- 🔧 [Common Patterns](docs/CLAUDE-PATTERNS.md) - Recipes for frequent development tasks

**Quick Jumps:**
- [Development Commands](#development-commands) - Run, test, build
- [Environment Requirements](#environment-requirements) - Python versions, dependencies, OS support
- [Core Principles](#core-principles) - Key development guidelines
- [Troubleshooting](#troubleshooting) - Common issues and solutions

---

## Project Overview

CSV to OFX Converter - A Python application that converts CSV files to OFX (Open Financial Exchange) format, with full support for Brazilian banking formats. Features a Tkinter-based wizard interface with 7 steps guiding users through CSV import, data preview, field mapping, balance preview, and conversion.

**Current Version**: 3.2.0 (January 2026)

**Key Characteristics:**
- Pure Python 3.7+ with standard library only (no external dependencies for runtime)
- GUI application using Tkinter with DPI awareness for Windows
- Multi-step wizard interface with data preview
- Support for both standard (comma, dot) and Brazilian (semicolon, comma) CSV formats
- Context menu for transaction management with date validation
- Automatic window maximization on startup (cross-platform compatible)
- Deterministic transaction IDs using UUID v5 (consistent FITIDs on regeneration)

**Project Structure:**
```
csv-to-ofx-converter/
├── main.py                      # Entry point
├── src/                         # Source code
│   ├── csv_to_ofx_converter.py  # Main module
│   ├── csv_parser.py            # CSV parsing
│   ├── ofx_generator.py         # OFX generation
│   ├── date_validator.py        # Date validation
│   ├── converter_gui.py         # GUI orchestrator (750 lines)
│   ├── transaction_utils.py     # Transaction utilities
│   ├── gui_utils.py             # GUI utilities
│   ├── gui_balance_manager.py   # Balance calculations
│   ├── gui_conversion_handler.py # Conversion orchestration
│   ├── gui_transaction_manager.py # Transaction operations
│   ├── gui_wizard_step.py       # Base class for wizard steps
│   ├── constants.py             # Shared constants
│   └── gui_steps/               # 7 wizard step implementations
│       ├── file_selection_step.py
│       ├── csv_format_step.py
│       ├── data_preview_step.py
│       ├── ofx_config_step.py
│       ├── field_mapping_step.py
│       ├── advanced_options_step.py
│       └── balance_preview_step.py
├── tests/                       # 499 tests total
│   ├── test_csv_parser.py       # 8 tests
│   ├── test_ofx_generator.py    # 21 tests
│   ├── test_date_validator.py   # 12 tests
│   ├── test_transaction_utils.py # 68 tests
│   ├── test_gui_utils.py        # 63 tests
│   ├── test_gui_integration.py  # 15 tests
│   ├── test_gui_balance_manager.py # 14 tests
│   ├── test_gui_conversion_handler.py # 23 tests
│   ├── test_gui_transaction_manager.py # 26 tests
│   ├── test_gui_wizard_step.py  # 32 tests
│   ├── test_integration.py      # 11 tests
│   └── test_gui_steps/          # 206 tests (7 step test files)
├── docs/                        # Documentation
│   ├── CLAUDE-ARCHITECTURE.md   # Architecture details
│   ├── CLAUDE-TESTING.md        # Testing strategy
│   ├── CLAUDE-RELEASE.md        # Release process
│   └── CLAUDE-PATTERNS.md       # Common patterns
└── examples/                    # Sample CSV files
```

---

## Environment Requirements

**Python Version**: 3.7+ (tested on 3.7, 3.8, 3.9, 3.10, 3.11)

**Runtime Dependencies**: None (pure Python standard library)

**Development Dependencies**:
- PyInstaller (building executables only)
- unittest (included in standard library)

**Operating System Support**:
- ✅ Linux (Ubuntu 20.04+, Debian 10+, Fedora 34+)
- ✅ macOS (10.14 Mojave and later)
- ✅ Windows (10, 11)

**GUI Requirements**:
- Tkinter (included in most Python distributions)
- Display server for GUI tests (use `xvfb-run` for headless CI environments)

**Recommended Development Environment**:
- Python 3.8+ for best compatibility
- Git for version control
- GitHub CLI (`gh`) for release management
- Code editor with Python support (VS Code, PyCharm, etc.)

---

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

# Alternative: Run using convenience script
python3 tests/run_all_tests.py
```

See [Testing Strategy](docs/CLAUDE-TESTING.md) for comprehensive testing documentation.

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

---

## Core Principles

1. **Pure Python Standard Library**: No external runtime dependencies. PyInstaller is dev-only.

2. **Modular Architecture**: Separate concerns into focused modules. Use companion classes for complex subsystems (BalanceManager, ConversionHandler, TransactionManager).

3. **Testability First**: Write tests for all business logic. Use dependency injection to enable testing without GUI dependencies.

4. **Brazilian Format Support**: First-class support for Brazilian banking CSV formats (semicolon delimiter, comma decimal separator).

5. **User-Friendly GUI**: Multi-step wizard with clear validation and helpful error messages at each step.

6. **Comprehensive Testing**: 499 tests covering all modules. GUI tests use mocks to avoid display server dependencies.

7. **CI/CD Integration**: Automated builds for Linux/macOS/Windows. SonarCloud quality analysis on every push.

8. **Documentation Sync**: Always update CLAUDE.md, README.md, and README.pt-BR.md when making changes.

---

## Coding Style

- Follow PEP8 guidelines
- Use descriptive variable and function names
- Keep code modular and maintainable
- Separate classes into different files
- Maintain consistency with existing structure and GUI framework
- Document non-obvious logic with inline comments
- Update docstrings when function signatures change

---

## Troubleshooting

### GUI Tests Failing in CI

**Problem**: `_tkinter.TclError: couldn't connect to display`

**Solution**: Use `xvfb-run` for headless environments or skip GUI tests in CI. Already configured in `.github/workflows/sonar.yml`:
```bash
# Run tests without GUI tests in CI
xvfb-run -a python3 -m unittest discover tests -v
```

### PyInstaller Build Fails

**Problem**: `ModuleNotFoundError` in built executable

**Solution**:
1. Verify all modules listed in `csv_to_ofx_converter.spec` under `hiddenimports`
2. Check that data files are included in `datas` array
3. Run `pyinstaller --clean csv_to_ofx_converter.spec` to rebuild from scratch

### OFX File Not Accepted by Bank Software

**Problem**: Bank software rejects generated OFX file

**Solution**:
1. Verify OFX 1.0.2 SGML format compatibility with target software
2. Check that account ID format matches bank requirements
3. Ensure dates are in YYYYMMDD format
4. Verify transaction types (DEBIT/CREDIT) are correct
5. Check that amounts don't have currency symbols in OFX output

### Date Validation Not Working

**Problem**: Dates not validating correctly or transactions marked as out-of-range

**Solution**:
1. Check date format matches patterns in `DateValidator._parse_date_to_datetime()` (see CLAUDE-ARCHITECTURE.md)
2. Supported formats: YYYY-MM-DD, DD/MM/YYYY, MM/DD/YYYY, YYYYMMDD
3. Ensure statement start/end dates are valid and in correct order
4. Verify transaction dates fall within expected range

### Brazilian CSV Format Not Detected

**Problem**: Amounts parsed incorrectly from Brazilian CSVs (e.g., 1.234,56 becomes wrong value)

**Solution**:
1. Verify semicolon delimiter selected in Step 2 (CSV Format)
2. Verify comma decimal separator selected in Step 2
3. Check that CSV file uses consistent formatting
4. Brazilian format example: `01/10/2025;100,50;Compra` (semicolon delimiter, comma decimal)
5. See `CSVParser.normalize_amount()` in CLAUDE-ARCHITECTURE.md for parsing logic

### Tkinter Not Found

**Problem**: `ModuleNotFoundError: No module named '_tkinter'`

**Solution**:
- **Ubuntu/Debian**: `sudo apt-get install python3-tk`
- **macOS**: Tkinter included with Python from python.org installer
- **Windows**: Tkinter included with standard Python installation

### Tests Running Slowly

**Problem**: Test suite takes too long to complete

**Solution**:
1. Run specific test modules instead of entire suite
2. Skip GUI integration tests during development: `python3 -m unittest discover tests -k "not gui_integration"`
3. Use test discovery with pattern: `python3 -m unittest discover tests -p "test_csv*.py"`

---

## Important Implementation Details

### Deterministic Transaction IDs (FITID)

When no ID column is mapped in Step 5, the system generates deterministic FITIDs using UUID v5 based on transaction data. This ensures the same transaction always receives the same FITID.

**Namespace:** `NAMESPACE_CSV_TO_OFX` in `transaction_utils.py`

**Input Data:**
- Transaction date (normalized to YYYYMMDD)
- Transaction amount (normalized to 2 decimals)
- Transaction memo (normalized: stripped, lowercase, max 255 chars)
- Account ID (optional, empty string for v1)
- Disambiguation (optional, empty string for v1)

**Benefits:**
- Same transaction → same FITID on every export
- Enables reliable reconciliation in financial software
- Supports partial file regeneration without duplicates
- Maintains backward compatibility (explicit IDs still honored)

**Implementation:**
- `generate_deterministic_fitid()` in `transaction_utils.py`
- Used by `OFXGenerator.add_transaction()` when `transaction_id=None`

---

## Documentation Requirements

**IMPORTANT**: When making changes to the codebase, ALWAYS update relevant documentation:

1. **CLAUDE.md** (this file):
   - Update project overview if major features added
   - Keep environment requirements current
   - Add new troubleshooting entries as needed

2. **docs/CLAUDE-*.md** files:
   - Update architecture docs when adding/removing modules
   - Update testing docs when adding test modules
   - Update patterns docs when establishing new patterns
   - Update release docs if release process changes

3. **README.md** (English):
   - Update usage instructions for user-facing changes
   - Add examples for new features
   - Keep feature list up to date
   - Update version number for releases

4. **README.pt-BR.md** (Portuguese):
   - Mirror all changes from README.md
   - Maintain translation consistency
   - Ensure examples are culturally appropriate

5. **Code Comments and Docstrings**:
   - Update docstrings when function signatures change
   - Keep inline comments accurate
   - Document non-obvious logic

---

## Key Resources

- **Architecture**: [docs/CLAUDE-ARCHITECTURE.md](docs/CLAUDE-ARCHITECTURE.md) - Detailed module structure, class responsibilities, data flow
- **Testing**: [docs/CLAUDE-TESTING.md](docs/CLAUDE-TESTING.md) - Complete testing strategy, 499 tests, test patterns
- **Release**: [docs/CLAUDE-RELEASE.md](docs/CLAUDE-RELEASE.md) - Step-by-step release process, CI/CD verification
- **Patterns**: [docs/CLAUDE-PATTERNS.md](docs/CLAUDE-PATTERNS.md) - Common development tasks, recipes, best practices

- **Release Checklist**: [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md) - Comprehensive release verification checklist
- **User Documentation**: [README.md](README.md) (English), [README.pt-BR.md](README.pt-BR.md) (Portuguese)
- **Sample Data**: [examples/](examples/) - Sample CSV files for testing

---

## Quick Reference

**Run App**: `python3 main.py`

**Run Tests**: `python3 -m unittest discover tests`

**Build**: `./build.sh` (Linux/macOS) or `build.bat` (Windows)

**Release**: See [docs/CLAUDE-RELEASE.md](docs/CLAUDE-RELEASE.md)

**Need Help?**
- 🏗️ Understanding code structure? → [CLAUDE-ARCHITECTURE.md](docs/CLAUDE-ARCHITECTURE.md)
- 🧪 Writing tests? → [CLAUDE-TESTING.md](docs/CLAUDE-TESTING.md)
- 🚀 Creating release? → [CLAUDE-RELEASE.md](docs/CLAUDE-RELEASE.md)
- 🔧 Common tasks? → [CLAUDE-PATTERNS.md](docs/CLAUDE-PATTERNS.md)
