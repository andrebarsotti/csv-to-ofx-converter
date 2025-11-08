# Date Validation - Code Examples

## Quick Code Reference

### 1. Creating a DateValidator

```python
from src.csv_to_ofx_converter import DateValidator

# Create validator with date range
validator = DateValidator('2025-10-01', '2025-10-31')

# Various input formats are supported
validator = DateValidator('01/10/2025', '31/10/2025')
validator = DateValidator('2025/10/01', '2025/10/31')
```

### 2. Checking if a Date is Valid

```python
# Check if date is within range
is_valid = validator.is_within_range('2025-10-15')  # Returns: True
is_valid = validator.is_within_range('2025-09-30')  # Returns: False

# Works with different date formats
is_valid = validator.is_within_range('15/10/2025')  # Returns: True
```

### 3. Getting Date Status

```python
# Determine where the date falls
status = validator.get_date_status('2025-09-30')  # Returns: 'before'
status = validator.get_date_status('2025-10-15')  # Returns: 'within'
status = validator.get_date_status('2025-11-05')  # Returns: 'after'
```

### 4. Adjusting Out-of-Range Dates

```python
# Adjust dates to nearest boundary
adjusted = validator.adjust_date_to_boundary('2025-09-30')
# Returns: '2025-10-01' (adjusted to start date)

adjusted = validator.adjust_date_to_boundary('2025-11-05')
# Returns: '2025-10-31' (adjusted to end date)

adjusted = validator.adjust_date_to_boundary('2025-10-15')
# Returns: '2025-10-15' (already within range)
```

### 5. Error Handling

```python
# Invalid date range (start > end)
try:
    validator = DateValidator('2025-10-31', '2025-10-01')
except ValueError as e:
    print(f"Error: {e}")
    # Output: Error: Start date must be before or equal to end date

# Invalid date format
try:
    validator = DateValidator('invalid-date', '2025-10-31')
except ValueError as e:
    print(f"Error: {e}")
    # Output: Error: Unrecognized date format: invalid-date
```

### 6. Complete Conversion Example

```python
from src.csv_to_ofx_converter import CSVParser, OFXGenerator, DateValidator

# Setup
parser = CSVParser(delimiter=',', decimal_separator='.')
generator = OFXGenerator()
validator = DateValidator('2025-10-01', '2025-10-31')

# Parse CSV
headers, rows = parser.parse_file('statement.csv')

# Process transactions with validation
for row in rows:
    date = row['date']
    amount = parser.normalize_amount(row['amount'])
    description = row['description']

    # Check if date is valid
    if not validator.is_within_range(date):
        status = validator.get_date_status(date)
        print(f"Transaction date {date} is {status} the range")

        # Option 1: Adjust to boundary
        adjusted_date = validator.adjust_date_to_boundary(date)
        date = adjusted_date
        print(f"Adjusted to: {date}")

        # Option 2: Skip transaction
        # continue

    # Add transaction
    generator.add_transaction(
        date=date,
        amount=amount,
        description=description,
        transaction_type='DEBIT' if amount < 0 else 'CREDIT'
    )

# Generate OFX
generator.generate(
    output_path='output.ofx',
    account_id='12345',
    bank_name='My Bank',
    currency='BRL'
)
```

## Unit Test Examples

### Testing Date Validation

```python
import unittest
from src.csv_to_ofx_converter import DateValidator

class TestDateValidation(unittest.TestCase):

    def test_within_range(self):
        """Test date within range."""
        validator = DateValidator('2025-10-01', '2025-10-31')
        self.assertTrue(validator.is_within_range('2025-10-15'))

    def test_before_range(self):
        """Test date before range."""
        validator = DateValidator('2025-10-01', '2025-10-31')
        self.assertFalse(validator.is_within_range('2025-09-30'))
        self.assertEqual(validator.get_date_status('2025-09-30'), 'before')

    def test_after_range(self):
        """Test date after range."""
        validator = DateValidator('2025-10-01', '2025-10-31')
        self.assertFalse(validator.is_within_range('2025-11-01'))
        self.assertEqual(validator.get_date_status('2025-11-01'), 'after')

    def test_adjustment(self):
        """Test date adjustment."""
        validator = DateValidator('2025-10-01', '2025-10-31')

        # Before range → adjust to start
        self.assertEqual(
            validator.adjust_date_to_boundary('2025-09-30'),
            '2025-10-01'
        )

        # After range → adjust to end
        self.assertEqual(
            validator.adjust_date_to_boundary('2025-11-01'),
            '2025-10-31'
        )
```

## Integration with GUI

### In the ConverterGUI Class

```python
def _convert(self):
    """Convert CSV to OFX with optional date validation."""

    # Initialize date validator if enabled
    date_validator = None
    if self.enable_date_validation.get():
        try:
            date_validator = DateValidator(
                self.start_date.get(),
                self.end_date.get()
            )
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid date range: {e}")
            return

    # Process transactions
    for row_idx, row in enumerate(self.csv_data, 1):
        date = row[date_col]

        # Validate date if enabled
        if date_validator:
            if not date_validator.is_within_range(date):
                status = date_validator.get_date_status(date)

                # Show dialog and get user choice
                adjusted_date = self._handle_out_of_range_transaction(
                    row_idx, date, status, date_validator, description
                )

                if adjusted_date is None:
                    continue  # Exclude transaction
                else:
                    date = adjusted_date  # Use adjusted date

        # Add transaction to generator
        generator.add_transaction(...)
```

## Practical Scenarios

### Scenario 1: Monthly Credit Card Statement

```python
# Statement period: October 1-31, 2025
validator = DateValidator('2025-10-01', '2025-10-31')

# Check various transactions
transactions = [
    ('28/09/2025', -50.00, 'Late September'),      # Before
    ('01/10/2025', -100.50, 'October Day 1'),      # Within
    ('15/10/2025', -75.25, 'Mid October'),         # Within
    ('31/10/2025', -200.00, 'October Last Day'),   # Within
    ('02/11/2025', -30.00, 'Early November'),      # After
]

for date, amount, desc in transactions:
    if validator.is_within_range(date):
        print(f"✓ {date}: {desc} - VALID")
    else:
        status = validator.get_date_status(date)
        adjusted = validator.adjust_date_to_boundary(date)
        print(f"✗ {date}: {desc} - {status.upper()}")
        print(f"  → Suggested adjustment: {adjusted}")
```

### Scenario 2: Quarterly Report

```python
# Q4 2025: October 1 - December 31
validator = DateValidator('2025-10-01', '2025-12-31')

# Check year-end transaction
if validator.is_within_range('2025-12-31'):
    print("Year-end transaction is valid for Q4")

if not validator.is_within_range('2026-01-01'):
    print("This transaction belongs to Q1 2026")
```

### Scenario 3: Custom Billing Cycle

```python
# Billing cycle: 25th to 24th of next month
validator = DateValidator('2025-10-25', '2025-11-24')

# Transactions span two calendar months
test_dates = [
    '2025-10-24',  # Before cycle
    '2025-10-25',  # First day
    '2025-10-31',  # Still valid
    '2025-11-15',  # Still valid
    '2025-11-24',  # Last day
    '2025-11-25',  # After cycle
]

for date in test_dates:
    status = "VALID" if validator.is_within_range(date) else "OUT OF RANGE"
    print(f"{date}: {status}")
```

## Performance Tips

### Efficient Validation

```python
# BAD: Creating validator inside loop
for row in rows:
    validator = DateValidator(start, end)  # Don't do this!
    if validator.is_within_range(row['date']):
        process_row(row)

# GOOD: Create validator once
validator = DateValidator(start, end)
for row in rows:
    if validator.is_within_range(row['date']):  # Reuse validator
        process_row(row)
```

### Batch Processing

```python
# Collect out-of-range transactions first
out_of_range = []
in_range = []

for row in rows:
    if validator.is_within_range(row['date']):
        in_range.append(row)
    else:
        out_of_range.append(row)

# Process in-range transactions immediately
for row in in_range:
    generator.add_transaction(...)

# Handle out-of-range transactions separately
for row in out_of_range:
    # Handle with user input or automatic adjustment
    adjusted_date = validator.adjust_date_to_boundary(row['date'])
    row['date'] = adjusted_date
    generator.add_transaction(...)
```

## Common Patterns

### Pattern 1: Strict Validation

```python
# Exclude all out-of-range transactions
for row in rows:
    if validator.is_within_range(row['date']):
        generator.add_transaction(...)
    else:
        log(f"Excluded: {row['date']} - {row['description']}")
```

### Pattern 2: Automatic Adjustment

```python
# Adjust all out-of-range dates automatically
for row in rows:
    date = row['date']
    if not validator.is_within_range(date):
        date = validator.adjust_date_to_boundary(date)
        log(f"Adjusted: {row['date']} → {date}")

    generator.add_transaction(date=date, ...)
```

### Pattern 3: User Choice (GUI)

```python
# Let user decide for each transaction
for row in rows:
    if not validator.is_within_range(row['date']):
        choice = show_dialog(row)  # 'adjust' or 'exclude'

        if choice == 'adjust':
            row['date'] = validator.adjust_date_to_boundary(row['date'])
            generator.add_transaction(...)
        # else: skip transaction
    else:
        generator.add_transaction(...)
```

## Edge Cases

### Handling Invalid Input

```python
def safe_validate(validator, date_str):
    """Safely validate a date with error handling."""
    try:
        return validator.is_within_range(date_str)
    except ValueError as e:
        print(f"Invalid date format: {date_str} - {e}")
        return False

# Usage
if safe_validate(validator, row['date']):
    process_transaction(row)
```

### Handling Empty Dates

```python
def validate_with_empty_check(validator, date_str):
    """Validate date with empty string handling."""
    if not date_str or date_str.strip() == '':
        return False
    return validator.is_within_range(date_str)
```

### Cross-Year Validation

```python
# Fiscal year: April 2025 - March 2026
validator = DateValidator('2025-04-01', '2026-03-31')

# Test dates across year boundary
assert validator.is_within_range('2025-12-31')
assert validator.is_within_range('2026-01-01')
assert validator.is_within_range('2026-03-31')
assert not validator.is_within_range('2026-04-01')
```

## Summary

The DateValidator class provides a clean, simple API:

```python
# Initialize
validator = DateValidator(start_date, end_date)

# Check
is_valid = validator.is_within_range(date)

# Classify
status = validator.get_date_status(date)  # 'before', 'within', 'after'

# Adjust
new_date = validator.adjust_date_to_boundary(date)
```

All methods handle multiple date formats automatically and provide clear error messages.
