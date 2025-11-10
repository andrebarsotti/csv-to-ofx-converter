# CSV to OFX Converter - Enhanced Edition

> 🇧🇷 **[Leia em Português (pt-BR)](README.pt-BR.md)**

A complete Python application that converts CSV (Comma-Separated Values) files into OFX (Open Financial Exchange) format, with full support for Brazilian banking formats. **Version 2.0** features a completely redesigned wizard-style interface with advanced features for enhanced user experience.

## ⚠️ Important Notice

**This application was developed with Artificial Intelligence (AI) assistance.**

- The code was generated and reviewed with the help of AI models
- While extensively tested, additional validation is recommended for production use
- **Always maintain backups of your original CSV files**
- Review generated OFX files before importing them into your financial software
- Use at your own risk - test thoroughly before using with important data
- Community contributions and improvements are welcome

## ✨ What's New in Version 2.0

**Major User Experience Improvements:**

1. **🎯 Step-by-Step Wizard Interface**: Guided multi-step process with clear progress indicators
2. **👀 CSV Data Preview**: View your data in a table before converting
3. **🔄 Value Inversion**: Easily swap debits and credits if needed
4. **📝 Composite Descriptions**: Combine multiple columns to create transaction descriptions
5. **✅ Enhanced Date Handling**: Keep, adjust, or exclude out-of-range transactions (new "Keep" option!)

## Features

### Core Features
- **Step-by-Step Wizard Interface**: Intuitive 6-step guided process with visual progress tracking
- **CSV Data Preview**: View imported data in a tabular format before conversion
- **Flexible CSV Support**:
  - Standard format (comma delimiter, dot decimal separator)
  - Brazilian format (semicolon delimiter, comma decimal separator)
  - Tab-delimited files
- **Smart Column Mapping**: Map any CSV column to OFX fields
- **Composite Descriptions**: Combine up to 4 columns to create rich transaction descriptions
- **Value Inversion**: Option to invert all transaction values (swap debits and credits)
- **Automatic Type Detection**: Infers debit/credit from amount sign
- **Multiple Date Formats**: Supports various date formats (DD/MM/YYYY, YYYY-MM-DD, etc.)
- **Multiple Currencies**: BRL, USD, EUR, GBP support

### Advanced Features
- **Date Validation**: Validate transactions against credit card statement period with three options:
  - **Keep**: Use the original date as-is
  - **Adjust**: Move to the nearest valid boundary (start or end date)
  - **Exclude**: Remove the transaction from the output
- **Error Handling**: Graceful error handling with detailed logging
- **Comprehensive Testing**: Full unit test suite included

## Requirements

- Python 3.7 or higher
- Tkinter (usually included with Python)

No external dependencies required! All libraries used are part of Python's standard library.

## Installation

### Option 1: Download Pre-built Executable (Recommended)

**No Python installation required!**

1. Go to the [Releases page](https://github.com/YOUR_USERNAME/conversor-csv-ofx/releases)
2. Download the latest version for your operating system:
   - **Windows**: `csv-to-ofx-converter-windows-x64.exe`
   - **macOS**: `csv-to-ofx-converter-macos-x64`
   - **Linux**: `csv-to-ofx-converter-linux-x64`
3. Follow the platform-specific instructions in the release notes

#### Windows
- Download and double-click the `.exe` file
- If Windows shows a security warning, click "More info" then "Run anyway"

#### macOS
```bash
chmod +x csv-to-ofx-converter-macos-x64
./csv-to-ofx-converter-macos-x64
```
- If macOS blocks it: System Preferences > Security & Privacy > Allow

#### Linux
```bash
chmod +x csv-to-ofx-converter-linux-x64
./csv-to-ofx-converter-linux-x64
```

### Option 2: Run from Source

**Requires Python 3.7+**

1. **Clone or download this repository**:
```bash
git clone https://github.com/YOUR_USERNAME/conversor-csv-ofx.git
cd conversor-csv-ofx
```

2. **Verify Python installation**:
```bash
python3 --version
```

3. **Run the application**:
```bash
python3 main.py
```

### Option 3: Build from Source

**For developers who want to create their own executable**

1. **Install PyInstaller**:
```bash
pip install pyinstaller
```

2. **Build the executable**:

   **Linux/macOS**:
   ```bash
   ./build.sh
   ```

   **Windows**:
   ```cmd
   build.bat
   ```

3. **Find the executable in `dist/` directory**

## Usage

### Running the Application

**Method 1 - GUI Application**:
```bash
python3 main.py
```

This will launch the **Enhanced Wizard Interface** that guides you through a 6-step process:

1. **File Selection** - Select your CSV file
2. **CSV Format** - Configure delimiter and decimal separator
3. **Data Preview** - View your data in a table (up to 100 rows)
4. **OFX Configuration** - Set account details and currency
5. **Field Mapping** - Map columns and configure composite descriptions
6. **Advanced Options** - Value inversion and date validation

### Wizard Step-by-Step Guide

#### Step 1: File Selection
Click the "Browse..." button to select your CSV file. The file should have a header row with column names.

#### Step 2: Configure CSV Format

Choose the format that matches your CSV file:

**Standard Format** (international):
- Delimiter: Comma (,)
- Decimal: Dot (.)
- Example: `2025-10-22,100.50,Purchase`

**Brazilian Format**:
- Delimiter: Semicolon (;)
- Decimal: Comma (,)
- Example: `22/10/2025;100,50;Compra`

**Tab Format**:
- Delimiter: Tab
- Decimal: Dot (.) or Comma (,)

Click "Next" to proceed.

#### Step 3: Data Preview

**New in Version 2.0!**

View your CSV data in an easy-to-read table format. This step allows you to:
- Verify that the file was parsed correctly
- Check that column names match your expectations
- Review sample data before conversion
- Use the "Reload Data" button if you need to change format settings

The preview shows up to 100 rows for performance. Click "Next" to continue.

#### Step 4: OFX Configuration

Set up the output file settings:

- **Account ID**: Your account identifier (e.g., account number) - *Optional* (default: "UNKNOWN")
- **Bank Name**: Name of your financial institution (default: "CSV Import")
- **Currency**: Choose from:
  - BRL (Brazilian Real)
  - USD (US Dollar)
  - EUR (Euro)
  - GBP (British Pound)

Click "Next" to proceed to field mapping.

#### Step 5: Field Mapping

Map your CSV columns to OFX transaction fields:

| OFX Field | Required | Description |
|-----------|----------|-------------|
| Date | Yes | Transaction date |
| Amount | Yes | Transaction amount (positive or negative) |
| Description | No* | Transaction description |
| Type | No | Transaction type: DEBIT or CREDIT |
| ID | No | Unique transaction identifier |

**\*Note**: Description is required, but you can use either a single column mapping OR the composite description feature (see below).

##### Composite Description Feature

**New in Version 2.0!**

Combine multiple CSV columns to create rich transaction descriptions:

1. Select up to 4 columns to combine
2. Choose a separator:
   - Space: `Column1 Column2 Column3`
   - Dash: `Column1 - Column2 - Column3`
   - Comma: `Column1, Column2, Column3`
   - Pipe: `Column1 | Column2 | Column3`

**Example**:
If your CSV has columns `category`, `merchant`, and `notes`:
- Column 1: `category`
- Column 2: `merchant`
- Column 3: `notes`
- Separator: Dash (-)
- Result: `Food - Restaurant ABC - Business lunch`

This is useful for creating detailed descriptions from multiple data fields, especially common in bank exports that separate transaction information across columns.

Click "Next" to proceed to advanced options.

#### Step 6: Advanced Options

Configure optional advanced features:

##### Value Inversion

**New in Version 2.0!**

Check the box "Invert all transaction values" if:
- Your CSV shows debits as positive and credits as negative (or vice versa)
- You need to flip the sign of all amounts

This will multiply all transaction amounts by -1 and swap DEBIT/CREDIT types.

**Example**: A CSV with `100.50` (positive) that should be a debit will become `-100.50` (DEBIT).

##### Transaction Date Validation

**Enhanced in Version 2.0!**

For credit card statements, validate that transactions fall within the statement period:

1. Check "Enable date validation for credit card statement period"
2. Enter **Start Date** (e.g., `2025-10-01` or `01/10/2025`)
3. Enter **End Date** (e.g., `2025-10-31` or `31/10/2025`)

When enabled, for each transaction outside the date range, you'll see a dialog with **three options**:

- **Keep original date**: Use the date as-is, even though it's out of range
- **Adjust to boundary**: Move the date to the nearest valid boundary (start or end date)
- **Exclude transaction**: Remove the transaction from the OFX file

**Benefits**:
- Ensures statement period accuracy
- Helps identify misplaced transactions
- Maintains chronological consistency
- Provides full control over edge cases

**Example Dialog**:
```
Transaction #5 is out of range!
Transaction Date: 02/11/2025
Description: Restaurant ABC
Valid Range: 2025-10-01 to 2025-10-31
Status: This transaction occurs AFTER the end date

How would you like to handle this transaction?
[Keep original date] [Adjust to end date] [Exclude this transaction]
```

Once configured, click **"Convert to OFX"** to start the conversion!

### Navigation

- **Back button**: Go to the previous step
- **Next button**: Proceed to the next step (validates current step)
- **Convert to OFX button**: Appears on the last step
- **Clear All button**: Reset the entire form and return to Step 1
- **Progress indicator**: Shows current step and completed steps

## CSV Format Examples

### Example 1: Standard Format
```csv
date,amount,description,type
2025-10-01,-100.50,Grocery Store,DEBIT
2025-10-02,-50.25,Gas Station,DEBIT
2025-10-03,1000.00,Salary,CREDIT
```

### Example 2: Brazilian Format
```csv
data;valor;descricao;tipo
01/10/2025;-100,50;Supermercado;DEBIT
02/10/2025;-50,25;Posto de Gasolina;DEBIT
03/10/2025;1.000,00;Salário;CREDIT
```

### Example 3: Composite Description Format
```csv
date,category,merchant,notes,amount
2025-10-01,Food,Restaurant ABC,Business lunch,-75.50
2025-10-02,Transport,Uber,Airport trip,-25.00
2025-10-03,Salary,Company XYZ,Monthly payment,3000.00
```

**Mapping for Example 3**:
- Date → `date`
- Amount → `amount`
- Composite Description:
  - Column 1: `category`
  - Column 2: `merchant`
  - Column 3: `notes`
  - Separator: Dash (-)
- Result: `Food - Restaurant ABC - Business lunch`

### Example 4: Minimal Format (Without Type Column)
```csv
date,amount,description
2025-10-01,-100.50,Grocery Store
2025-10-02,-50.25,Gas Station
2025-10-03,1000.00,Salary
```

### Example 5: Nubank Export Format
```csv
date,category,title,amount
01/10/2025,alimentação,Supermercado ABC,-100,50
02/10/2025,transporte,Uber,-25,00
05/10/2025,outros,Pagamento recebido,1.500,00
```

**Column Mapping for Nubank**:
- Date → `date`
- Amount → `amount`
- Option A: Description → `title`
- Option B: Composite Description:
  - Column 1: `category`
  - Column 2: `title`
  - Separator: Dash (-)

### Example 6: Using Value Inversion

**CSV with inverted values:**
```csv
date,amount,description
2025-10-01,100.50,Expense (should be negative)
2025-10-02,50.25,Expense (should be negative)
2025-10-03,-1000.00,Income (should be positive)
```

Enable "Invert all transaction values" to fix the signs:
- `100.50` becomes `-100.50` (DEBIT)
- `50.25` becomes `-50.25` (DEBIT)
- `-1000.00` becomes `1000.00` (CREDIT)

### Example 7: Using Date Validation

**CSV with mixed dates:**
```csv
date,amount,description
28/09/2025,-50.00,Transaction before period
01/10/2025,-100.50,Valid transaction 1
15/10/2025,-75.25,Valid transaction 2
31/10/2025,-200.00,Valid transaction 3
02/11/2025,-30.00,Transaction after period
```

**With Date Validation enabled (Start: 01/10/2025, End: 31/10/2025):**
- Transaction from 28/09/2025: Choose to Keep / Adjust to 01/10/2025 / Exclude
- Transactions from 01/10/2025 to 31/10/2025: Processed normally
- Transaction from 02/11/2025: Choose to Keep / Adjust to 31/10/2025 / Exclude

## Supported Date Formats

The converter automatically recognizes these date formats:

- `YYYY-MM-DD` (2025-10-22)
- `DD/MM/YYYY` (22/10/2025)
- `MM/DD/YYYY` (10/22/2025)
- `YYYY/MM/DD` (2025/10/22)
- `DD-MM-YYYY` (22-10-2025)
- `DD.MM.YYYY` (22.10.2025)
- `YYYYMMDD` (20251022)

## OFX Output Format

The generated OFX file follows the OFX 1.0.2 specification (SGML format) and includes:

- **Header**: OFX version, encoding, charset information
- **Sign-on Message**: Bank information and server timestamp
- **Statement**: Account details and transaction list
- **Transactions**: Each transaction with:
  - Type (DEBIT/CREDIT)
  - Date (OFX format: YYYYMMDD000000)
  - Amount (with proper sign)
  - Unique ID (UUID)
  - Description/memo
- **Balance**: Final account balance

### Sample OFX Output
```xml
OFXHEADER:100
DATA:OFXSGML
VERSION:102
...
<OFX>
  <SIGNONMSGSRSV1>
    <SONRS>
      ...
      <FI>
        <ORG>CSV Import</ORG>
      </FI>
    </SONRS>
  </SIGNONMSGSRSV1>
  <CREDITCARDMSGSRSV1>
    <CCSTMTTRNRS>
      ...
      <CCSTMTRS>
        <CURDEF>BRL</CURDEF>
        ...
        <BANKTRANLIST>
          <STMTTRN>
            <TRNTYPE>DEBIT</TRNTYPE>
            <DTPOSTED>20251001000000[-3:BRT]</DTPOSTED>
            <TRNAMT>-100.50</TRNAMT>
            <FITID>uuid-here</FITID>
            <MEMO>Purchase description</MEMO>
          </STMTTRN>
          ...
        </BANKTRANLIST>
      </CCSTMTRS>
    </CCSTMTTRNRS>
  </CREDITCARDMSGSRSV1>
</OFX>
```

## Running Tests

The project includes comprehensive unit tests covering:
- CSV parsing with different formats
- Amount normalization
- Date parsing
- OFX generation
- Value inversion
- Date validation and boundary handling
- Composite descriptions
- Error handling
- Integration tests

### Run all tests:
```bash
python3 -m unittest tests.test_converter
```

### Run with verbose output:
```bash
python3 -m unittest tests.test_converter -v
```

### Run specific test class:
```bash
python3 -m unittest tests.test_converter.TestCSVParser
python3 -m unittest tests.test_converter.TestOFXGenerator
python3 -m unittest tests.test_converter.TestDateValidator
```

### Expected output:
```
test_add_credit_transaction (tests.test_converter.TestOFXGenerator) ... ok
test_add_transaction (tests.test_converter.TestOFXGenerator) ... ok
test_brazilian_csv_parsing (tests.test_converter.TestCSVParser) ... ok
test_date_validator_initialization (tests.test_converter.TestDateValidator) ... ok
test_is_within_range (tests.test_converter.TestDateValidator) ... ok
...
----------------------------------------------------------------------
Ran 33+ tests in 0.XXXs

OK
```

## Logging

The application generates detailed logs in `csv_to_ofx_converter.log`:

```
2025-11-08 12:34:56 - __main__ - INFO - GUI initialized with wizard interface
2025-11-08 12:35:01 - __main__ - INFO - Parsed CSV: 150 rows, 4 columns
2025-11-08 12:35:05 - __main__ - INFO - Value inversion enabled - all amounts will be inverted
2025-11-08 12:35:10 - __main__ - INFO - OFX file generated: output.ofx (148 transactions)
```

## Troubleshooting

### Issue: "CSV file has no headers"
**Solution**: Ensure your CSV file has a header row with column names.

### Issue: "Invalid amount format"
**Solution**: Check that your decimal separator setting matches your CSV format.

### Issue: "Unrecognized date format"
**Solution**: Verify your date format is one of the supported formats. You may need to reformat your dates in the CSV.

### Issue: GUI doesn't appear
**Solution**: Ensure Tkinter is installed:
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# macOS (usually included)
# Windows (usually included)
```

### Issue: Characters appear corrupted (encoding issues)
**Solution**: The application uses UTF-8 encoding. Ensure your CSV file is saved in UTF-8 format.

### Issue: Preview shows wrong data
**Solution**: Go back to Step 2 and verify your delimiter and decimal separator settings. Use "Reload Data" button after changing settings.

## Architecture

### Code Structure

```
csv_to_ofx_converter.py
├── CSVParser          # Handles CSV file parsing
│   ├── parse_file()          # Parse CSV and extract data
│   └── normalize_amount()    # Convert amounts to float
│
├── OFXGenerator       # Generates OFX files
│   ├── __init__(invert_values)   # Initialize with inversion option
│   ├── add_transaction()     # Add transaction to queue
│   ├── _parse_date()         # Parse and format dates
│   └── generate()            # Create OFX file
│
├── DateValidator      # Validates transaction dates
│   ├── is_within_range()     # Check if date is valid
│   ├── get_date_status()     # Determine before/within/after
│   └── adjust_date_to_boundary()  # Adjust out-of-range dates
│
└── ConverterGUI       # Wizard-style Tkinter GUI
    ├── _create_widgets()     # Build wizard interface
    ├── _show_step()          # Display specific step
    ├── _create_step_*()      # Create each step's UI
    ├── _load_csv_data()      # Load and parse CSV
    ├── _populate_preview()   # Fill data preview table
    ├── _convert()            # Perform conversion
    ├── _handle_out_of_range_transaction()  # Handle date issues
    └── _log()                # Display log messages
```

### Wizard Flow

```
Step 1: File Selection
    ↓
Step 2: CSV Format Configuration
    ↓
Step 3: Data Preview (NEW!)
    ↓ (CSV loaded automatically)
Step 4: OFX Configuration
    ↓
Step 5: Field Mapping + Composite Description (NEW!)
    ↓
Step 6: Advanced Options (Value Inversion + Date Validation)
    ↓
Conversion Process
    ↓
OFX File Generated
```

### Data Flow

```
CSV File → CSVParser → Preview Display → Field Mapping → Advanced Options → OFXGenerator → OFX File
    ↓            ↓            ↓               ↓                ↓                ↓
  Headers     Rows      Treeview      User Mapping    Value Inversion    Transactions
              Data     (Step 3)       Composite Desc   Date Validation    Formatting
                                                       (Keep/Adjust/Exclude)
```

## Best Practices

1. **Always review your CSV data in the preview** (Step 3) before conversion
2. **Test with a small CSV file** first to verify mappings are correct
3. **Keep backups** of your original CSV files
4. **Use composite descriptions** when you have multiple related columns to combine
5. **Use value inversion** if your amounts have the wrong sign instead of manually editing the CSV
6. **Verify OFX files** in your financial software before importing large datasets
7. **Use consistent date formats** within a single CSV file
8. **Check logs** if conversion fails or produces unexpected results
9. **Use date validation** to ensure statement period accuracy for credit cards

## Compatibility

### Tested With
- Python 3.7, 3.8, 3.9, 3.10, 3.11
- Windows 10/11
- Ubuntu 20.04/22.04
- macOS 11+

### Financial Software Compatibility
The generated OFX files are compatible with:
- GnuCash
- Microsoft Money
- Quicken
- QuickBooks
- HomeBank
- KMyMoney
- Most accounting software supporting OFX 1.0.2

## Limitations

- Maximum description length: 255 characters (OFX specification)
- Supports credit card statement format (CREDITCARDMSGSRSV1)
- Does not support investment accounts or complex transactions
- Single account per file
- Preview limited to first 100 rows for performance

## Future Improvements

Possible enhancements for future versions:

1. **Bank Account Support**: Add support for checking/savings accounts (BANKMSGSRSV1)
2. **Multiple Accounts**: Support multiple accounts in a single OFX file
3. **Templates**: Save and load column mapping templates
4. **Batch Processing**: Convert multiple CSV files at once
5. **CSV Auto-Detection**: Automatically detect CSV format and date formats
6. **Transaction Categories**: Support OFX category/class fields
7. **Investment Accounts**: Support for stocks, bonds, and investment transactions
8. **OFX 2.x Support**: Add support for newer OFX XML format
9. **Custom Date Formats**: Allow users to specify custom date formats
10. **Command-Line Interface**: Add CLI for scripting and automation
11. **Transaction Deduplication**: Detect and handle duplicate transactions
12. **Split Transactions**: Support for split/categorized transactions
13. **Multi-language Support**: Internationalization (i18n)
14. **Excel Support**: Direct import from .xlsx/.xls files
15. **Bulk Date Adjustment**: Option to adjust all out-of-range dates at once without dialogs

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

MIT License

Copyright (c) 2025 André Claudinei Barsotti Salvadeo

See [LICENSE](LICENSE) file for details.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Credits

**Author**: André Claudinei Barsotti Salvadeo

Developed with analysis of Nubank OFX export format to ensure compatibility with Brazilian banking standards.

**Note**: This project was developed with AI assistance. While functional and tested, proper review and validation are recommended before use in production environments.

## Support

For issues, questions, or suggestions:
1. Check the Troubleshooting section
2. Review the log file (`csv_to_ofx_converter.log`)
3. Run the test suite to verify installation
4. Open an issue with detailed information about your problem

---

**Version**: 2.0.3 - Enhanced Edition
**Last Updated**: November 2025
**Author**: André Claudinei Barsotti Salvadeo (with AI Assistance)
**License**: MIT

## Changelog

### Version 2.0.3 (November 2025) - Code Quality and Refactoring

- **Code Quality**: Integrated SonarCloud for continuous code quality monitoring
  - Added SonarQube workflow for automated code analysis
  - Configured code coverage testing
  - Addressed multiple code quality issues identified by SonarCloud
  - Fixed potential security vulnerabilities
- **Refactoring**: Major code reorganization for better maintainability
  - Split monolithic code into separate modules:
    - `csv_parser.py`: CSV parsing functionality
    - `ofx_generator.py`: OFX file generation
    - `date_validator.py`: Date validation logic
    - `converter_gui.py`: GUI implementation
    - `constants.py`: Shared constants
  - Added comprehensive module docstrings and type hints
  - Improved error handling and logging
- **Bug Fixes**:
  - Resolved import errors and Unicode character issues
  - Fixed executable names in release workflow (artifacts now properly flattened)
  - Improved success message formatting in conversion completion
- **Cleanup**:
  - Removed outdated implementation summaries
  - Removed Claude settings from version control
  - Cleaned up redundant and commented-out code
- All tests passing
- Better code organization and maintainability
- No functional changes - same features as v2.0.1

### Version 2.0.1 (November 2025) - Bugfix Release
- **Bug Fix**: Restored Account ID as optional field
  - Account ID was incorrectly marked as required in v2.0.0
  - Now optional with default value "UNKNOWN" (same as v1.1.0)
  - Updated UI help text and documentation
  - Full backward compatibility restored
- All 39 tests passing
- No breaking changes - all v2.0.0 features maintained

### Version 2.0.0 (November 2025) - Enhanced Edition
- **Major Update**: Complete UI redesign with step-by-step wizard interface
  - 6-step guided process with visual progress indicators
  - Clear navigation with Back/Next buttons
  - Step validation before proceeding
- **New Feature**: CSV Data Preview
  - View imported data in tabular format (Treeview widget)
  - Preview up to 100 rows before conversion
  - Reload data button for format changes
- **New Feature**: Composite Descriptions
  - Combine up to 4 CSV columns into transaction descriptions
  - Choice of separators: Space, Dash, Comma, Pipe
  - Perfect for CSVs with split transaction information
- **New Feature**: Value Inversion
  - Option to invert all transaction amounts
  - Automatically swaps DEBIT/CREDIT types
  - Useful for CSVs with reversed sign conventions
- **Enhanced Feature**: Date Validation with "Keep" Option
  - Added "Keep original date" as third option
  - Now offers: Keep / Adjust / Exclude
  - Better statistics tracking (kept out-of-range dates)
- **UI Improvements**:
  - Larger window (1000x850) for better visibility
  - Improved layout and spacing
  - Better error messages and validation
  - Enhanced activity log display
  - Clear step descriptions and help text
- **Documentation**: Complete rewrite of README with:
  - Detailed wizard step instructions
  - New feature examples
  - Updated screenshots and diagrams
  - Best practices guide

### Version 1.1.0 (November 2025)
- **New Feature**: Credit card statement date validation
  - Added optional date range validation for transactions
  - Interactive dialog for handling out-of-range transactions
  - Options to adjust dates to boundaries or exclude transactions
  - Comprehensive test coverage for date validation
- Enhanced GUI with date validation controls
- Improved statistics reporting (adjusted/excluded transactions)
- Updated documentation with examples and best practices

### Version 1.0.0 (November 2025)
- Initial release
- CSV to OFX conversion with GUI
- Support for Brazilian and standard CSV formats
- Flexible column mapping
- Multiple currency support
