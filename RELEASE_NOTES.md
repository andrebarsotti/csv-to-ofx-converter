# Release Notes - Version 2.0.3

## CSV to OFX Converter - Code Quality and Refactoring Release

**Release Date**: November 9, 2025

### Overview

Version 2.0.3 focuses on code quality improvements, refactoring for better maintainability, and integration with SonarCloud for continuous code quality monitoring. This release maintains all the features from version 2.0.2 while significantly improving the codebase organization and addressing security concerns.

### What's New

#### Code Quality Improvements
- **SonarCloud Integration**: Added continuous code quality monitoring
  - Automated code analysis on every push
  - Code coverage tracking and reporting
  - Security vulnerability scanning
  - Code smell detection and resolution

#### Major Refactoring
- **Modular Architecture**: Split the monolithic `csv_to_ofx_converter.py` into specialized modules:
  - `csv_parser.py` (113 lines): Handles all CSV file parsing and format detection
  - `ofx_generator.py` (247 lines): Manages OFX file generation and formatting
  - `date_validator.py` (139 lines): Contains date validation logic and dialogs
  - `converter_gui.py` (1180 lines): Complete GUI implementation
  - `constants.py` (12 lines): Shared constants across modules
  - `__init__.py` (29 lines): Package initialization and exports

- **Better Code Organization**:
  - Added comprehensive docstrings to all modules and classes
  - Implemented type hints throughout the codebase
  - Improved error handling and logging
  - Reduced code duplication

### Bug Fixes
- Resolved import errors that could occur in certain environments
- Fixed Unicode character issues in comments and strings (replaced with ASCII)
- Corrected executable names in the GitHub Actions release workflow
- Improved success message formatting for better readability

### Cleanup
- Removed outdated implementation summaries that were no longer relevant
- Removed Claude settings from version control (.gitignore updated)
- Cleaned up redundant and commented-out code
- Improved overall code clarity

### Security
- Fixed potential security vulnerabilities identified by SonarCloud
- Improved input validation and error handling
- Better separation of concerns reduces attack surface

### Testing
- All 39 unit tests passing
- Added code coverage analysis
- Maintained 100% backward compatibility

### What's Changed (Technical Details)

**File Structure Changes:**
```
Before (v2.0.2):
- src/csv_to_ofx_converter.py (1523 lines)

After (v2.0.3):
- src/__init__.py (29 lines)
- src/constants.py (12 lines)
- src/csv_parser.py (113 lines)
- src/ofx_generator.py (247 lines)
- src/date_validator.py (139 lines)
- src/converter_gui.py (1180 lines)
```

**New Configuration Files:**
- `sonar-project.properties`: SonarCloud configuration
- `.github/workflows/sonar.yml`: SonarQube analysis workflow
- `CHANGELOG.md`: Detailed changelog (English)
- `CHANGELOG_pt-BR.md`: Detailed changelog (Portuguese)

### No Breaking Changes
- All features from v2.0.2 are fully preserved
- Same user interface and functionality
- Same command-line usage
- Same file formats and compatibility

### Download

#### Executables (No Python Required)

**Windows:**
```
csv-to-ofx-converter-windows-x64.exe
```
Double-click to run. If Windows shows a security warning, click "More info" then "Run anyway".

**macOS:**
```bash
chmod +x csv-to-ofx-converter-macos-x64
./csv-to-ofx-converter-macos-x64
```
If macOS blocks it: System Preferences > Security & Privacy > Allow

**Linux:**
```bash
chmod +x csv-to-ofx-converter-linux-x64
./csv-to-ofx-converter-linux-x64
```

### Verification

You can verify the integrity of downloaded files using the provided SHA256 checksums:

```bash
# Linux/macOS
sha256sum csv-to-ofx-converter-linux-x64

# Windows (PowerShell)
Get-FileHash csv-to-ofx-converter-windows-x64.exe -Algorithm SHA256
```

Compare the output with the checksums in `checksums.txt`.

### System Requirements

- **For Executables**: No additional requirements
  - Windows 10 or later (64-bit)
  - macOS 10.13 or later (64-bit)
  - Linux with glibc 2.17 or later (64-bit)

- **For Source Code**:
  - Python 3.7 or higher
  - Tkinter (usually included with Python)
  - No external dependencies required

### Getting Started

1. Download the appropriate executable for your platform
2. Make it executable (macOS/Linux only)
3. Run the application
4. Follow the step-by-step wizard to convert your CSV files

For detailed instructions, see the [README](README.md) or [README.pt-BR](README.pt-BR.md).

### Support

- **Issues**: Report bugs at https://github.com/andrebarsotti/conversor-csv-ofx/issues
- **Documentation**: See README.md for complete documentation
- **Questions**: Open a discussion on GitHub

### Coming Next

Future releases may include:
- Additional bank format presets
- Import templates for common banks
- Enhanced transaction categorization
- Multi-file batch processing

### Contributors

**Author**: André Claudinei Barsotti Salvadeo (with AI Assistance)

### License

MIT License - See LICENSE file for details

---

**Full Changelog**: https://github.com/andrebarsotti/conversor-csv-ofx/compare/v2.0.2...v2.0.3
