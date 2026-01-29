## Task: Implement Deterministic FITID Generation for CSV to OFX Converter

### Background

The application converts CSV files to OFX format. Currently, when the user doesn't map an ID column from the CSV, the system generates a random UUID v4 for each transaction's FITID field. This causes a problem: **the same transaction gets different FITIDs each time the file is processed**, breaking reconciliation workflows when users generate partial files.

### Current Behavior

The FITID generation flow works as follows:

1. **User maps ID column (optional)**: In Step 5 (Field Mapping), users can map a CSV column to "ID". If mapped, `extract_transaction_id()` in `src/transaction_utils.py:100-127` extracts the value directly from the CSV row.

2. **Auto-generated ID (current problem)**: If no ID column is mapped, `transaction_id` arrives as `None` in `OFXGenerator.add_transaction()` at `src/ofx_generator.py:40-77`, which generates a random UUID v4:
   ```python
   if transaction_id is None:
       transaction_id = str(uuid.uuid4())
   ```

### Required Change

Replace the random UUID v4 generation with a **deterministic UUID v5** based on transaction data. The same transaction should always produce the same FITID, regardless of:
- How many times the file is processed
- Whether the file is complete or partial
- The order of transactions in the CSV

### Implementation Requirements

1. **Create a deterministic ID generator function** that:
   - Takes transaction fields as input (date, amount, description/memo, and optionally account info)
   - Uses `uuid.uuid5()` with a consistent namespace
   - Returns a deterministic UUID string
   - Normalizes input data before hashing (trim whitespace, consistent formatting)

2. **Define an application-specific namespace**:
   - Create a constant namespace UUID for this application
   - Example: `NAMESPACE_OFX = uuid.uuid5(uuid.NAMESPACE_DNS, "csv-to-ofx-converter.local")`

3. **Modify `OFXGenerator.add_transaction()`** to:
   - Accept the necessary transaction fields for deterministic ID generation
   - When `transaction_id` is `None`, generate a deterministic UUID using the transaction data instead of `uuid.uuid4()`

4. **Handle edge cases**:
   - Transactions on the same date with identical amounts and descriptions should still be distinguishable if possible (consider including row index or sequential counter as a disambiguation field)
   - Empty or null fields should be handled gracefully

5. **Maintain backward compatibility**:
   - If user explicitly maps an ID column, continue using that value as-is
   - Only apply deterministic generation when no ID is mapped

### Example Implementation Pattern

```python
import uuid

NAMESPACE_OFX = uuid.uuid5(uuid.NAMESPACE_DNS, "csv-to-ofx-converter.local")

def generate_deterministic_fitid(date: str, amount: str, memo: str, account: str = "", disambiguation: str = "") -> str:
    """
    Generate a deterministic FITID based on transaction data.
    Same inputs always produce the same output.
    """
    # Normalize inputs
    normalized_data = "|".join([
        str(date).strip(),
        str(amount).strip(),
        str(memo).strip().lower(),
        str(account).strip(),
        str(disambiguation).strip()
    ])
    
    return str(uuid.uuid5(NAMESPACE_OFX, normalized_data))
```

### Files to Modify

- `src/ofx_generator.py` - Main changes to `add_transaction()` method
- `src/transaction_utils.py` - Possibly add the deterministic ID generator function here
- Add appropriate tests to verify deterministic behavior

### Acceptance Criteria

- [ ] Same transaction data always produces the same FITID
- [ ] Different transactions produce different FITIDs
- [ ] Existing functionality (mapped ID column) works unchanged
- [ ] Code includes appropriate comments explaining the deterministic approach
- [ ] Edge cases (empty fields, duplicates) are handled
