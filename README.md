# CSV to OFX Converter

> 🇧🇷 **[Leia em Português (pt-BR)](README.pt-BR.md)**

A complete Python application that converts CSV (Comma-Separated Values) files into OFX (Open Financial Exchange) format, with full support for Brazilian banking formats.

## ⚠️ Important Notice

**This application was developed with Artificial Intelligence (AI) assistance.**

- The code was generated and reviewed with the help of AI models
- While extensively tested, additional validation is recommended for production use
- **Always maintain backups of your original CSV files**
- Review generated OFX files before importing them into your financial software
- Use at your own risk - test thoroughly before using with important data
- Community contributions and improvements are welcome

## Features

- **Intuitive GUI**: User-friendly Tkinter-based interface
- **Flexible CSV Support**:
  - Standard format (comma delimiter, dot decimal separator)
  - Brazilian format (semicolon delimiter, comma decimal separator)
  - Tab-delimited files
- **Smart Column Mapping**: Map any CSV column to OFX fields
- **Automatic Type Detection**: Infers debit/credit from amount sign
- **Multiple Date Formats**: Supports various date formats (DD/MM/YYYY, YYYY-MM-DD, etc.)
- **Multiple Currencies**: BRL, USD, EUR, GBP support
- **Date Validation**: Validate transactions against credit card statement period with options to adjust or exclude out-of-range transactions
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
python3 src/csv_to_ofx_converter.py
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
python3 csv_to_ofx_converter.py
```

This will launch the graphical interface where you can:
1. Select your CSV file
2. Configure CSV format (delimiter and decimal separator)
3. Set OFX configuration (account ID, bank name, currency)
4. Map CSV columns to OFX fields
5. Convert and save the OFX file

### Step-by-Step Guide

#### 1. Select CSV File
Click the "Browse..." button to select your CSV file.

#### 2. Configure CSV Format

**Standard Format** (international):
- Delimiter: Comma (,)
- Decimal: Dot (.)
- Example: `2025-10-22,100.50,Purchase`

**Brazilian Format**:
- Delimiter: Semicolon (;)
- Decimal: Comma (,)
- Example: `22/10/2025;100,50;Compra`

#### 3. Set OFX Configuration

- **Account ID**: Your account identifier (e.g., account number)
- **Bank Name**: Name of your financial institution
- **Currency**: BRL (Brazilian Real), USD, EUR, or GBP

#### 3b. Enable Date Validation (Optional)

For credit card statements, you can validate that all transactions fall within the statement period:

1. **Check the box**: "Enable date validation for credit card statement period"
2. **Set Start Date**: Enter the first day of your statement period (e.g., `2025-10-01` or `01/10/2025`)
3. **Set End Date**: Enter the last day of your statement period (e.g., `2025-10-31` or `31/10/2025`)

When enabled, the converter will:
- Check each transaction date against the specified range
- For transactions outside the range, prompt you to choose:
  - **Adjust to boundary**: Move the date to the nearest valid boundary (start or end date)
  - **Exclude transaction**: Remove the transaction from the output

This is useful for ensuring statement consistency and handling transactions that may appear in the CSV but don't belong to the current statement period.

#### 4. Load CSV

Click "Load CSV" to parse the file. The application will display all available columns.

#### 5. Map Columns

Map your CSV columns to OFX fields:

| OFX Field | Required | Description | Example CSV Column |
|-----------|----------|-------------|--------------------|
| Date | Yes | Transaction date | `data`, `date`, `Data` |
| Amount | Yes | Transaction amount | `valor`, `amount`, `Valor` |
| Description | Yes | Transaction description | `descricao`, `description`, `memo` |
| Type | No | Transaction type (DEBIT/CREDIT) | `tipo`, `type` |
| ID | No | Unique transaction identifier | `id`, `transaction_id` |

**Note**: If Type is not mapped, it will be inferred from the amount sign (negative = DEBIT, positive = CREDIT).

#### 6. Convert

Click "Convert to OFX" to generate the OFX file. Choose where to save it.

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

### Example 3: Minimal Format (Without Type Column)
```csv
date,amount,description
2025-10-01,-100.50,Grocery Store
2025-10-02,-50.25,Gas Station
2025-10-03,1000.00,Salary
```

### Example 4: Nubank Export Format
```csv
date,category,title,amount
01/10/2025,alimentação,Supermercado ABC,-100,50
02/10/2025,transporte,Uber,-25,00
05/10/2025,outros,Pagamento recebido,1.500,00
```

**Column Mapping for Nubank**:
- Date → `date`
- Amount → `amount`
- Description → `title` (or combine `category` + `title`)
- Type → Not mapped (auto-detected)

### Example 5: Using Date Validation

When you have transactions that might fall outside your statement period:

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
- Transaction from 28/09/2025: You'll be prompted to adjust to 01/10/2025 or exclude
- Transactions from 01/10/2025 to 31/10/2025: Processed normally
- Transaction from 02/11/2025: You'll be prompted to adjust to 31/10/2025 or exclude

**Benefits:**
- Ensures statement period accuracy
- Helps identify misplaced transactions
- Maintains chronological consistency
- Provides control over boundary cases

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
- Date validation and boundary handling
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
Ran 33 tests in 0.XXXs

OK
```

## Logging

The application generates detailed logs in `csv_to_ofx_converter.log`:

```
2025-11-08 12:34:56 - __main__ - INFO - CSVParser initialized: delimiter=',', decimal='.'
2025-11-08 12:35:01 - __main__ - INFO - Parsed CSV: 150 rows, 4 columns
2025-11-08 12:35:10 - __main__ - INFO - OFX file generated: output.ofx (150 transactions)
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

## Architecture

### Code Structure

```
csv_to_ofx_converter.py
├── CSVParser          # Handles CSV file parsing
│   ├── parse_file()          # Parse CSV and extract data
│   └── normalize_amount()    # Convert amounts to float
│
├── OFXGenerator       # Generates OFX files
│   ├── add_transaction()     # Add transaction to queue
│   ├── _parse_date()         # Parse and format dates
│   └── generate()            # Create OFX file
│
├── DateValidator      # Validates transaction dates
│   ├── is_within_range()     # Check if date is valid
│   ├── get_date_status()     # Determine before/within/after
│   └── adjust_date_to_boundary()  # Adjust out-of-range dates
│
└── ConverterGUI       # Tkinter GUI interface
    ├── _create_widgets()     # Build UI components
    ├── _load_csv()           # Load and parse CSV
    ├── _convert()            # Perform conversion
    ├── _handle_out_of_range_transaction()  # Handle date issues
    └── _log()                # Display log messages
```

### Data Flow

```
CSV File → CSVParser → Field Mapping → Date Validation → OFXGenerator → OFX File
    ↓                        ↓              ↓                  ↓
  Headers              GUI Mapping     DateValidator      Transactions
  Rows                 User Input      (Optional)         Formatting
                                       User Decision
```

**Date Validation Flow** (when enabled):
```
Transaction Date → DateValidator.is_within_range()
                        ↓
                   [Within Range?]
                    ↙         ↘
                  Yes          No
                   ↓            ↓
            Add to OFX    Show Dialog
                              ↓
                      [User Choice]
                       ↙         ↘
                  Adjust        Exclude
                    ↓              ↓
              Adjust Date     Skip Transaction
                    ↓
               Add to OFX
```

## Best Practices

1. **Always review your CSV data** before conversion to ensure data quality
2. **Test with a small CSV file** first to verify mappings are correct
3. **Keep backups** of your original CSV files
4. **Verify OFX files** in your financial software before importing large datasets
5. **Use consistent date formats** within a single CSV file
6. **Check logs** if conversion fails or produces unexpected results

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
9. **Preview Mode**: Preview OFX output before saving
10. **Custom Date Formats**: Allow users to specify custom date formats
11. **Command-Line Interface**: Add CLI for scripting and automation
12. **Transaction Deduplication**: Detect and handle duplicate transactions
13. **Split Transactions**: Support for split/categorized transactions
14. **Multi-language Support**: Internationalization (i18n)
15. **Excel Support**: Direct import from .xlsx/.xls files
16. **Bulk Date Adjustment**: Option to adjust all out-of-range dates at once

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

**Version**: 1.1.0
**Last Updated**: November 2025
**Author**: André Claudinei Barsotti Salvadeo (with AI Assistance)
**License**: MIT

## Changelog

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
