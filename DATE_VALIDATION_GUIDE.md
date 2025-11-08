# Date Validation Feature - Quick Start Guide

## What is Date Validation?

Date validation ensures that all transactions in your CSV file fall within a specific date range (e.g., your credit card statement period). This helps maintain statement accuracy and identify transactions that might belong to a different period.

## When to Use Date Validation

Use this feature when:
- Converting credit card statement exports
- You need to ensure all transactions are within a specific billing cycle
- You want to filter transactions by date range
- You need to handle transactions that span multiple statement periods

## How to Use

### Step 1: Enable Date Validation

In the converter GUI, find the **"Statement Date Range (Optional)"** section:

1. Check the box: ☑️ **"Enable date validation for credit card statement period"**
2. The date input fields will become active

### Step 2: Enter Date Range

Enter your statement period dates:

- **Start Date**: First day of the statement (e.g., `2025-10-01`)
- **End Date**: Last day of the statement (e.g., `2025-10-31`)

**Supported formats**:
- `YYYY-MM-DD` (2025-10-01)
- `DD/MM/YYYY` (01/10/2025)
- `MM/DD/YYYY` (10/01/2025)
- `YYYY/MM/DD` (2025/10/01)
- And more...

### Step 3: Convert Your File

1. Load your CSV file (as usual)
2. Map the columns
3. Click **"Convert to OFX"**

### Step 4: Handle Out-of-Range Transactions

If a transaction date is outside your specified range, a dialog will appear with:

**Transaction Information**:
- Transaction date
- Description
- Valid date range
- Whether it's before or after the range

**Your Options**:

1. **Adjust to boundary** (recommended for most cases)
   - Moves the date to the nearest valid boundary
   - Transaction before range → adjusted to start date
   - Transaction after range → adjusted to end date
   - Transaction is included in the output

2. **Exclude transaction**
   - Removes the transaction from the output
   - Use when transaction doesn't belong to this statement

### Step 5: Review Results

After conversion, you'll see statistics:
- Total rows processed
- Transactions included
- Number of date adjustments made
- Number of transactions excluded

## Example Scenario

### Your Credit Card Statement
- **Period**: October 1-31, 2025
- **CSV export** includes some transactions from September and November

### CSV Content
```csv
date,amount,description
28/09/2025,-50.00,Late September purchase
01/10/2025,-100.50,October purchase 1
15/10/2025,-75.25,October purchase 2
31/10/2025,-200.00,October purchase 3
02/11/2025,-30.00,Early November purchase
```

### With Date Validation

**Settings**:
- Start Date: `01/10/2025`
- End Date: `31/10/2025`

**What Happens**:

1. **Transaction from 28/09/2025**:
   - ⚠️ Dialog appears: "This transaction occurs BEFORE the start date"
   - Choose: "Adjust to start date" → Date becomes 01/10/2025
   - Or choose: "Exclude transaction" → Transaction removed

2. **Transactions from 01/10 to 31/10**:
   - ✅ Processed normally (within range)

3. **Transaction from 02/11/2025**:
   - ⚠️ Dialog appears: "This transaction occurs AFTER the end date"
   - Choose: "Adjust to end date" → Date becomes 31/10/2025
   - Or choose: "Exclude transaction" → Transaction removed

### Result
Your OFX file contains only transactions from the October statement period!

## Best Practices

### DO:
✅ Use date validation for credit card statements
✅ Double-check your date range before converting
✅ Review the statistics after conversion
✅ Keep original CSV as backup
✅ Use the same date format consistently

### DON'T:
❌ Mix date formats within the same CSV
❌ Enter reversed dates (end before start)
❌ Forget to enable validation if you need it
❌ Adjust dates without understanding the impact

## Troubleshooting

### "Invalid date range" error
**Problem**: Start date is after end date
**Solution**: Swap the dates or enter them correctly

### "Unrecognized date format" error
**Problem**: Date format not supported
**Solution**: Reformat dates in your CSV to a supported format

### Dialog doesn't appear
**Problem**: Date validation not enabled
**Solution**: Check the checkbox to enable validation

### Too many dialogs
**Problem**: Many out-of-range transactions
**Solution**: Check your date range or consider using a different range

## Tips for Efficiency

1. **Check your CSV first**: Preview your CSV dates before converting
2. **Use consistent dates**: Ensure your CSV dates match your range
3. **Plan your approach**: Decide in advance whether to adjust or exclude
4. **Test with small file**: Try with a few rows first
5. **Document your choices**: Keep notes on adjustments made

## Real-World Use Cases

### Use Case 1: Credit Card Statement
**Situation**: Monthly statement from Oct 1-31
**Solution**: Enable validation, adjust boundary transactions

### Use Case 2: Quarterly Report
**Situation**: Need Q4 transactions (Oct-Dec)
**Solution**: Set range to 10/01-12/31, exclude others

### Use Case 3: Year-End Reconciliation
**Situation**: Need only current year transactions
**Solution**: Set range to 01/01-12/31, exclude previous year

### Use Case 4: Split Statement
**Situation**: Statement crosses month boundary (25th to 24th)
**Solution**: Set exact date range, adjust as needed

## Advanced Features

### Handling Leap Years
The validator correctly handles leap year dates:
```
Range: 2024-02-28 to 2024-03-01
Date: 2024-02-29 → ✅ Valid (leap year)
```

### Year Boundaries
Works across year changes:
```
Range: 2025-12-15 to 2026-01-15
Date: 2025-12-31 → ✅ Valid
Date: 2026-01-01 → ✅ Valid
```

### Same-Day Range
Support for single-day statements:
```
Range: 2025-10-15 to 2025-10-15
Only transactions from Oct 15 are valid
```

## Logging

All validation actions are logged to `csv_to_ofx_converter.log`:
```
2025-11-08 12:34:56 - Date validation enabled: 2025-10-01 to 2025-10-31
2025-11-08 12:35:01 - Row 1: Date 2025-09-30 is out of range (before)
2025-11-08 12:35:05 - Row 1: Date adjusted from 2025-09-30 to 2025-10-01
2025-11-08 12:35:10 - Row 5: Transaction excluded by user
```

## Getting Help

If you encounter issues:
1. Check this guide
2. Review the log file
3. Check README.md for more details
4. Ensure your CSV format is correct
5. Try with a test file first

## Summary

Date validation is a powerful optional feature that:
- ✅ Ensures statement period accuracy
- ✅ Gives you control over boundary transactions
- ✅ Provides clear statistics
- ✅ Integrates seamlessly into your workflow
- ✅ Is easy to use with interactive dialogs

**Remember**: Date validation is optional. If you don't need it, simply leave the checkbox unchecked and the converter works as before!
