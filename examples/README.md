# Example CSV Files

This directory contains sample CSV files to help you understand the formats supported by the converter.

## Files

### 1. example_standard.csv
**Format**: Standard international format
- **Delimiter**: Comma (,)
- **Decimal**: Dot (.)
- **Date Format**: YYYY-MM-DD
- **Columns**: date, amount, description, type

**Use Case**: English-speaking countries, international banking exports

**Column Mapping**:
- Date → date
- Amount → amount
- Description → description
- Type → type

---

### 2. example_brazilian.csv
**Format**: Brazilian format
- **Delimiter**: Semicolon (;)
- **Decimal**: Comma (,)
- **Date Format**: DD/MM/YYYY
- **Columns**: data, valor, descricao, tipo

**Use Case**: Brazilian banking exports, Portuguese language systems

**Column Mapping**:
- Date → data
- Amount → valor
- Description → descricao
- Type → tipo

---

### 3. example_minimal.csv
**Format**: Minimal required fields
- **Delimiter**: Comma (,)
- **Decimal**: Dot (.)
- **Date Format**: YYYY-MM-DD
- **Columns**: date, amount, description (no type column)

**Use Case**: Simple exports, when transaction type should be auto-detected

**Column Mapping**:
- Date → date
- Amount → amount
- Description → description
- Type → Not mapped (auto-detected from amount sign)

**Note**: Negative amounts become DEBIT, positive amounts become CREDIT

---

### 4. example_nubank_style.csv
**Format**: Nubank-style export
- **Delimiter**: Comma (,)
- **Decimal**: Comma (,)
- **Date Format**: DD/MM/YYYY
- **Columns**: date, category, title, amount

**Use Case**: Nubank credit card exports

**Column Mapping**:
- Date → date
- Amount → amount
- Description → title (or combine category + title)
- Type → Not mapped (auto-detected)

**Note**: This format uses comma as decimal separator but comma as delimiter, so the amount field appears as multiple columns (e.g., `-100,50` appears as `-100` and `50`). You may need to pre-process this file or combine columns.

---

## How to Use These Examples

### Quick Start

1. **Launch the application**:
   ```bash
   python3 ../csv_to_ofx_converter.py
   ```

2. **Load an example file**:
   - Click "Browse..." and select one of these example files
   - Choose the appropriate CSV format settings
   - Click "Load CSV"

3. **Map the columns**:
   - The examples above show the correct mapping for each file
   - Map required fields: Date, Amount, Description
   - Optionally map Type and ID

4. **Configure OFX settings**:
   - Set your account ID (e.g., "EXAMPLE-001")
   - Set bank name (e.g., "Example Bank")
   - Set currency (BRL for Brazilian examples)

5. **Convert**:
   - Click "Convert to OFX"
   - Save the output file

### Testing Different Formats

**For Standard Format** (example_standard.csv):
```
CSV Format:
  Delimiter: Comma (,)
  Decimal: Dot (.)

Column Mapping:
  Date → date
  Amount → amount
  Description → description
  Type → type
```

**For Brazilian Format** (example_brazilian.csv):
```
CSV Format:
  Delimiter: Semicolon (;)
  Decimal: Comma (,)

Column Mapping:
  Date → data
  Amount → valor
  Description → descricao
  Type → tipo
```

## Creating Your Own CSV Files

### Template Structure

```csv
column1,column2,column3,...
value1,value2,value3,...
value1,value2,value3,...
```

### Required Information

You must have at least these three pieces of information:
1. **Date** - When the transaction occurred
2. **Amount** - How much (use negative for debits, positive for credits)
3. **Description** - What the transaction was for

### Tips

1. **Always include a header row** with column names
2. **Use consistent date formats** within a single file
3. **Be consistent with negative signs** (- for debits)
4. **Avoid special characters** in descriptions when possible
5. **Test with a small file first** before processing large datasets

## Common Issues

### Issue: Amount parsing errors with Brazilian format

If you have amounts like `-100,50` in a comma-delimited file, the CSV parser may interpret this as two separate columns.

**Solution**: Use semicolon (;) as delimiter for Brazilian format.

### Issue: Date not recognized

**Solution**: Ensure your dates match one of the supported formats:
- YYYY-MM-DD
- DD/MM/YYYY
- MM/DD/YYYY
- YYYY/MM/DD
- DD-MM-YYYY
- DD.MM.YYYY
- YYYYMMDD

### Issue: Transactions appear with wrong sign

**Solution**:
- Ensure debits are negative (e.g., `-100.50`)
- Ensure credits are positive (e.g., `1000.00`)
- Or map the Type column correctly

## Advanced Examples

### Combining Columns for Description

Some exports have separate category and description columns. You may need to pre-process your CSV to combine them:

**Original**:
```csv
date,category,description,amount
2025-10-01,Food,Supermarket,-100.50
```

**Combined**:
```csv
date,amount,description
2025-10-01,-100.50,Food - Supermarket
```

You can use a spreadsheet program or text editor to combine columns before importing.

### Handling Multiple Date Formats

If your CSV has dates in different formats, standardize them first using a spreadsheet program:

1. Open in Excel/LibreOffice Calc
2. Select the date column
3. Format → Cells → Date
4. Choose a standard format (e.g., YYYY-MM-DD)
5. Save as CSV

---

**Need Help?** Check the main README.md file in the parent directory for detailed documentation.
