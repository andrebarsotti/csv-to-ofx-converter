# Project Files Reference

## 📁 Main Application
- **`src/csv_to_ofx_converter.py`** - Main application with GUI (1,068 lines)
  - CSVParser class
  - OFXGenerator class
  - DateValidator class (NEW in v1.1.0)
  - ConverterGUI class

## 🧪 Tests
- **`tests/test_converter.py`** - Comprehensive test suite (608 lines)
  - TestCSVParser (8 tests)
  - TestOFXGenerator (11 tests)
  - TestDateValidator (12 tests - NEW in v1.1.0)
  - TestIntegration (2 tests)
  - **Total: 33 tests, all passing ✅**

## 📖 Documentation

### English
- **`README.md`** - Main documentation (English) with AI disclaimer
- **`BUILD.md`** - Build and release guide (English)
- **`IMPLEMENTATION_SUMMARY.md`** - Technical implementation details
- **`CODE_EXAMPLES.md`** - Code snippets and usage patterns
- **`DATE_VALIDATION_GUIDE.md`** - User guide for date validation feature

### Portuguese (pt-BR)
- **`README.pt-BR.md`** - Complete documentation in Brazilian Portuguese with AI disclaimer
- **`BUILD.pt-BR.md`** - Build and release guide in Brazilian Portuguese

### Reference
- **`PROJECT_FILES.md`** - This file

## 🔧 Configuration
- **`requirements.txt`** - Python dependencies (none required beyond standard library)
- **`environment.yml`** - Conda environment configuration
- **`.gitignore`** - Git ignore patterns for build artifacts and temporary files
- **`LICENSE`** - MIT License file

## 🏗️ Build System
- **`csv_to_ofx_converter.spec`** - PyInstaller specification file
- **`build.sh`** - Build script for Linux/macOS
- **`build.bat`** - Build script for Windows
- **`.github/workflows/build-and-release.yml`** - GitHub Actions workflow for automated builds
- **`BUILD.md`** - Comprehensive build and release guide

## 📊 Examples
- **`examples/`** - Directory with example CSV files (if present)

## 📝 Logs
- **`csv_to_ofx_converter.log`** - Application log file (generated at runtime)

## 📦 Output
- **`*.ofx`** - Generated OFX files (created by user during conversion)

## 🔑 Key Features by File

### src/csv_to_ofx_converter.py
1. **CSVParser** (lines 38-134)
   - Parses CSV files
   - Handles Brazilian and standard formats
   - Normalizes amounts

2. **OFXGenerator** (lines 136-350)
   - Generates OFX 1.0.2 format files
   - Handles multiple currencies
   - Supports credit card statements

3. **DateValidator** (lines 353-473) ⭐ NEW
   - Validates transaction dates
   - Adjusts out-of-range dates
   - Supports multiple date formats

4. **ConverterGUI** (lines 476-1068)
   - Tkinter-based graphical interface
   - Column mapping
   - Date validation controls ⭐ NEW
   - Interactive dialogs ⭐ NEW

## 📈 Project Statistics

- **Total Lines of Code**: ~1,700 lines
- **Test Coverage**: 33 unit tests
- **Documentation Pages**: 5 (English) + 1 (Portuguese)
- **Supported Date Formats**: 7
- **Supported Currencies**: 4 (BRL, USD, EUR, GBP)
- **CSV Format Support**: 3 (standard, Brazilian, tab-delimited)

## 🆕 Version 1.1.0 Changes

### New Files
- `README.pt-BR.md` - Portuguese translation
- `DATE_VALIDATION_GUIDE.md` - Date validation user guide
- `CODE_EXAMPLES.md` - Code examples and patterns
- `IMPLEMENTATION_SUMMARY.md` - Technical details
- `PROJECT_FILES.md` - This reference document

### Modified Files
- `src/csv_to_ofx_converter.py` - Added DateValidator class and date validation GUI
- `tests/test_converter.py` - Added 12 new tests for DateValidator
- `README.md` - Updated with date validation documentation + AI disclaimer

### Lines Added
- ~270 lines in main application
- ~140 lines in tests
- ~2,500 lines in documentation

## 🎯 Quick Navigation

### For Users
- Start here: [`README.md`](README.md) or [`README.pt-BR.md`](README.pt-BR.md)
- Date validation: [`DATE_VALIDATION_GUIDE.md`](DATE_VALIDATION_GUIDE.md)

### For Developers
- Code examples: [`CODE_EXAMPLES.md`](CODE_EXAMPLES.md)
- Implementation: [`IMPLEMENTATION_SUMMARY.md`](IMPLEMENTATION_SUMMARY.md)
- Tests: [`tests/test_converter.py`](tests/test_converter.py)

### For Running
- Main app: `python3 src/csv_to_ofx_converter.py`
- Tests: `python3 -m unittest tests.test_converter`

## 📋 File Sizes (Approximate)

| File | Lines | Size |
|------|-------|------|
| src/csv_to_ofx_converter.py | 1,068 | ~40 KB |
| tests/test_converter.py | 608 | ~25 KB |
| README.md | 500+ | ~30 KB |
| README.pt-BR.md | 500+ | ~35 KB |
| IMPLEMENTATION_SUMMARY.md | 400+ | ~25 KB |
| DATE_VALIDATION_GUIDE.md | 300+ | ~20 KB |
| CODE_EXAMPLES.md | 400+ | ~25 KB |

## 🚀 Getting Started

1. Read [`README.md`](README.md) or [`README.pt-BR.md`](README.pt-BR.md)
2. Run tests: `python3 -m unittest tests.test_converter`
3. Launch GUI: `python3 src/csv_to_ofx_converter.py`
4. For date validation: See [`DATE_VALIDATION_GUIDE.md`](DATE_VALIDATION_GUIDE.md)

## 📞 Support

For issues or questions:
1. Check README troubleshooting section
2. Review log file: `csv_to_ofx_converter.log`
3. Run tests to verify installation
4. Open an issue with details

---

**Project Version**: 1.1.0
**Last Updated**: November 2025
**Documentation Language**: English + Portuguese (pt-BR)
**AI Assistance**: Yes (see disclaimer in README files)
