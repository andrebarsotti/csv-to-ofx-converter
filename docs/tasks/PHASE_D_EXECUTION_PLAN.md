# Phase D Execution Plan: Complex Steps Extraction (Steps 5 & 7)

**Status:** PLANNED - Ready for Implementation
**Phase:** D (4 of 5)
**Created:** 2025-11-24
**Last Updated:** 2025-11-24

---

## Executive Summary

Phase D extracts the two most complex wizard steps from `converter_gui.py`:
- **Step 5 (Field Mapping):** ~138 lines to extract → ~250 lines new file
- **Step 7 (Balance Preview):** ~313 lines to extract → ~400 lines new file

**Expected Impact:**
- Remove ~500 lines from converter_gui.py (1,211 → ~700 lines)
- Add ~650 lines of new step code
- Add ~730 lines of test code
- Add 47 new tests (401 → 448 total tests)

**Complexity Rating:** HIGH to VERY HIGH
- Step 5: 8/10 difficulty (most complex UI)
- Step 7: 10/10 difficulty (most data-heavy, manager integrations)

---

## Phase D Tasks Overview

### Task Breakdown (10 tasks total)

| Task | Description | Agent | Priority | Duration |
|------|-------------|-------|----------|----------|
| D.1  | Extract FieldMappingStep (Step 5) | feature-developer | P1 | 1 day |
| D.2  | Create FieldMappingStep Unit Tests | unit-test-generator | P1 | 0.5 days |
| D.3  | Extract BalancePreviewStep (Step 7) | feature-developer | P1 | 1 day |
| D.4  | Create BalancePreviewStep Unit Tests | unit-test-generator | P1 | 0.5 days |
| D.5  | Finalize Orchestrator | feature-developer | P1 | 0.5 days |
| D.6  | Integration Testing | unit-test-generator | P1 | 0.5 days |
| D.7  | Update Package Exports | feature-developer | P1 | 0.25 days |
| D.8  | Code Quality Review | code-quality-reviewer | P1 | 0.5 days |
| D.9  | Documentation | feature-developer | P1 | 0.25 days |
| D.10 | Release Prep | feature-developer | P1 | 0.25 days |

**Total Duration:** 5 days (allows for parallel work)

---

## Phase D Gate Criteria

To pass Phase D and proceed to Phase E, the following criteria **MUST** be met:

### Critical Metrics
- ✅ **All 7 steps functional** - Steps 1-7 fully integrated and working
- ✅ **Total tests: 390+** (343 from Phase C + 47 new Phase D tests minimum)
- ✅ **converter_gui.py: ~700 lines** (reduced from 1,211 lines, removing ~500+ lines)
- ✅ **Code quality grade: A** (minimum, A+ preferred)
- ✅ **Zero regressions** - All 390+ tests must pass

### Functional Requirements
- Step 5 (Field Mapping) fully functional in wizard
- Step 7 (Balance Preview) fully functional in wizard
- Field mapping validation working correctly
- Composite description configuration working
- Balance preview calculations accurate
- Transaction deletion/restoration working
- Date action decisions (keep/adjust/exclude) working

### Quality Requirements
- PEP8 compliance: 100%
- Docstring coverage: 100%
- Test coverage: ≥90% for new step classes
- No critical or high-priority code quality issues

### Integration Requirements
- All wizard navigation working (forward/backward through 7 steps)
- Data flow between steps intact
- Conversion workflow completing successfully
- SonarCloud workflow passing (215 non-GUI tests in CI)

---

## Current Project State (Pre-Phase D)

### Test Count
- **Total tests: 401** (as of Phase C completion)
  - Base tests: 230 (original)
  - Phase A: +32 tests (WizardStep base class)
  - Phase B: +65 tests (Steps 1, 2, 4)
  - Phase C: +74 tests (Steps 3, 6)

### Code Metrics
- **converter_gui.py: 1,211 lines** (current size)
- **Total methods in converter_gui.py: 36 methods**

### Helper Classes
- **BalanceManager:** 450 lines - Balance calculations
- **TransactionManager:** 528 lines - Transaction operations
- **Total helper code:** 978 lines

### Step Files (Existing)
1. FileSelectionStep: 194 lines (24 tests)
2. CSVFormatStep: 220 lines (21 tests)
3. OFXConfigStep: 219 lines (20 tests)
4. DataPreviewStep: 297 lines (35 tests)
5. AdvancedOptionsStep: 359 lines (39 tests)

**Total existing step code:** 1,289 lines (139 tests)

### SonarCloud CI Status
- Runs on every push to main
- Executes 215 non-GUI tests (excludes display-dependent tests)
- Currently passing ✅

---

## Step 5 (Field Mapping) - Technical Analysis

### Complexity Rating: HIGH (8/10)

### Current Implementation
**Location in converter_gui.py:**
- Main method: `_create_step_field_mapping()` (lines 525-596) = 72 lines
- Helper method: `_create_composite_description_ui()` (lines 597-634) = 38 lines
- **Total Step 5 code: ~110-112 lines**

**Validation Methods:**
- `_validate_field_mapping()` (lines 365-371) = 7 lines
- `_validate_required_fields()` (lines 373-381) = 9 lines
- `_validate_description_mapping()` (lines 383-392) = 10 lines
- **Total validation code: ~26 lines**

**Estimated Line Count for Extraction:**
- **Total lines to extract: ~138 lines** (UI + validation)
- **Expected new file size: ~250 lines** (with WizardStep scaffolding, docstrings)

### UI Elements (25-30 widgets)

**Field Mapping Section:**
1. **LabelFrame** - Step 5 container with title
2. **Info Label** - Instructions for user
3. **5 Field Mapping Combos** - Date, Amount, Description, Type, ID
   - Each has: Label (bold), Combobox (readonly), Help text (gray)
4. **Horizontal Separator** - Visual divider

**Composite Description Section:**
5. **Section Title** - "Composite Description (Optional)"
6. **Instructions Label** - Usage guidance
7. **4 Column Selectors** - Combobox for each column
8. **Separator Radio Buttons** - 4 options (Space, Dash, Comma, Pipe)
9. **Note Label** - Required field indicator

### Data Collection

```python
{
    'field_mappings': {
        'date': str,      # Required (CSV column name or NOT_MAPPED)
        'amount': str,    # Required
        'description': str,  # Optional (if composite used)
        'type': str,      # Optional
        'id': str         # Optional
    },
    'description_columns': [str, str, str, str],  # 4 columns (NOT_SELECTED if unused)
    'description_separator': str  # ' ', ' - ', ', ', or ' | '
}
```

### Dependencies

**Import Requirements:**
- `tkinter` / `tkinter.ttk` - UI widgets
- `gui_wizard_step.WizardStep` - Base class
- `constants` - NOT_MAPPED, NOT_SELECTED
- `gui_utils` - Validation functions

**Parent Data Access:**
- Read: `self.csv_headers` (List[str]) - for populating combobox options
- Read/Write: `self.field_mappings` (Dict[str, StringVar]) - field mapping state
- Read/Write: `self.description_columns` (List[StringVar]) - composite columns
- Read/Write: `self.description_separator` (StringVar) - separator choice

### Special Considerations

1. **Most Complex UI** - Step 5 has the most UI elements of any step
2. **Dynamic Options** - Combobox options populated from CSV headers (runtime data)
3. **Conditional Logic** - Either description OR composite description must be configured
4. **Validation Coordination** - Two validation methods working together
5. **State Preservation** - Must handle existing StringVar values correctly

### Expected Deliverables (Task D.1 & D.2)

**Production Code (D.1):**
- File: `src/gui_steps/field_mapping_step.py`
- Size: ~250 lines
- Class: `FieldMappingStep(WizardStep)`
- StepConfig: `step_number=4, step_name="Field Mapping", step_title="Step 5: Map CSV Columns to OFX Fields"`

**Test Code (D.2):**
- File: `tests/test_gui_steps/test_field_mapping_step.py`
- Size: ~350 lines
- Tests: 20-25 tests
- Coverage: Initialization, UI creation, field mapping validation, composite description logic, data collection, lifecycle

---

## Step 7 (Balance Preview) - Technical Analysis

### Complexity Rating: VERY HIGH (10/10)

### Current Implementation
**Location in converter_gui.py:**
- Main method: `_create_step_balance_preview()` (lines 637-847) = 211 lines
- Helper: `_recalculate_balance_preview()` (lines 848-883) = 36 lines
- Helper: `_calculate_balance_preview()` (lines 884-914) = 31 lines
- Helper: `_validate_numeric_input()` (lines 916-933) = 18 lines
- Helper: `_toggle_final_balance_mode()` (lines 966-978) = 13 lines
- Helper: `_update_final_balance_display()` (lines 980-983) = 4 lines
- **Total Step 7 code: ~313 lines**

**Additional Dependencies:**
- Uses `BalanceManager` (450 lines) - for calculations
- Uses `TransactionManager` (528 lines) - for context menus and deletion
- Transaction tree context menu binding
- Date validation status display (colored rows)

**Estimated Line Count for Extraction:**
- **Total lines to extract: ~313 lines** (UI + helpers)
- **Expected new file size: ~350-400 lines** (with WizardStep scaffolding)

### UI Elements (30-35 widgets)

**Balance Input Section:**
1. **LabelFrame** - Step 7 container with title
2. **Info Label** - Instructions
3. **Initial Balance Frame** - Input section
   - Label: "Starting Balance"
   - Entry: Initial balance (with numeric validation)
   - Button: "Recalculate"
   - Help text label

**Balance Summary Section:**
4. **LabelFrame** - "Balance Summary"
5. **Summary Labels:**
   - Total Credits (green)
   - Total Debits (red)
   - Calculated Final Balance (blue, bold)
6. **Horizontal Separator**
7. **Checkbox** - Auto-calculate final balance toggle
8. **Manual Balance Frame:**
   - Label: "Manual Final Balance"
   - Entry: Manual final balance (enabled/disabled)
   - Help text
9. **Transaction Count Label** - Gray text

**Transaction Preview Section:**
10. **LabelFrame** - "Transaction Preview"
11. **Treeview** - Transaction list with:
    - Columns: Date, Description, Amount, Type
    - Scrollbars: Vertical and horizontal
    - Context menu binding (right-click)
    - Row coloring: Light red (before), Light orange (after)
12. **Confirmation Label** - Green success message

### Data Collection

```python
{
    'initial_balance': float,  # User-entered starting balance
    'final_balance': float,    # Manual or auto-calculated
    'auto_calculate_final_balance': bool,  # Toggle mode
    'deleted_transactions': Set[int],  # Row indices to exclude
    'date_action_decisions': Dict[int, str]  # Row index -> 'keep'/'adjust'/'exclude'
}
```

### Dependencies

**Import Requirements:**
- `tkinter` / `tkinter.ttk` - UI widgets
- `gui_wizard_step.WizardStep` - Base class
- `gui_balance_manager.BalanceManager` - Calculations
- `gui_transaction_manager.TransactionManager` - Context menus
- `gui_utils` - Numeric validation

**Manager Class Integration:**
- `BalanceManager.calculate_balance_preview()` - Returns BalancePreviewData
- `BalanceManager.validate_balance_input()` - Numeric input validation
- `BalanceManager.format_final_balance()` - Balance formatting
- `TransactionManager.show_context_menu()` - Right-click menu
- `TransactionManager.show_out_of_range_dialog()` - Date action dialog

**Parent Data Access:**
- Read: All field mappings, CSV data, format settings, advanced options
- Read/Write: `self.initial_balance` (StringVar)
- Read/Write: `self.final_balance` (StringVar)
- Read/Write: `self.auto_calculate_final_balance` (BooleanVar)
- Read/Write: `self.deleted_transactions` (Set[int])
- Read/Write: `self.transaction_tree_items` (Dict[int, str])
- Widget references: `self.balance_preview_tree`, `self.total_credits_label`, etc.

### Special Considerations

1. **Most Data-Heavy Step** - Processes all transactions for preview
2. **Complex Integrations** - Works with BalanceManager and TransactionManager
3. **Interactive Features** - Context menu, transaction deletion, recalculation
4. **Real-time Updates** - Labels update without recreating step
5. **State Management** - Tracks deleted transactions and date decisions
6. **Visual Feedback** - Color-coded rows for date validation status
7. **Mode Toggle** - Auto vs manual final balance switching

### Expected Deliverables (Task D.3 & D.4)

**Production Code (D.3):**
- File: `src/gui_steps/balance_preview_step.py`
- Size: ~400 lines
- Class: `BalancePreviewStep(WizardStep)`
- StepConfig: `step_number=6, step_name="Balance Preview", step_title="Step 7: Review Balance and Confirm"`

**Test Code (D.4):**
- File: `tests/test_gui_steps/test_balance_preview_step.py`
- Size: ~380 lines
- Tests: 22-25 tests
- Coverage: Initialization, UI creation, balance calculations, manager integration, transaction operations, data collection, lifecycle

---

## Execution Strategy

### Approach: Sequential with Strategic Parallelization

### Stage 1: Field Mapping Step (Step 5)
**Duration:** 1.5 days | **Tasks:** D.1, D.2

**Day 1 Morning: Task D.1 - Extract FieldMappingStep**
- Agent: feature-developer
- Create `src/gui_steps/field_mapping_step.py`
- Extract UI creation logic (~110 lines)
- Extract validation logic (~26 lines)
- Add WizardStep scaffolding
- Total: ~250 lines

**Day 1 Afternoon: Task D.2 - Create Tests (Parallel)**
- Agent: unit-test-generator
- Create `tests/test_gui_steps/test_field_mapping_step.py`
- Write 20-25 tests covering all functionality
- Total: ~350 lines

**End of Day 1:** 250 lines production + 350 lines test

---

### Stage 2: Balance Preview Step (Step 7)
**Duration:** 1.5 days | **Tasks:** D.3, D.4

**Day 2 Morning: Task D.3 - Extract BalancePreviewStep**
- Agent: feature-developer
- Create `src/gui_steps/balance_preview_step.py`
- Extract UI creation logic (~211 lines)
- Extract helper methods (~102 lines)
- Integrate with BalanceManager and TransactionManager
- Add WizardStep scaffolding
- Total: ~400 lines

**Day 2 Afternoon: Task D.4 - Create Tests (Parallel)**
- Agent: unit-test-generator
- Create `tests/test_gui_steps/test_balance_preview_step.py`
- Write 22-25 tests covering all functionality
- Mock BalanceManager and TransactionManager
- Total: ~380 lines

**End of Day 2:** 400 lines production + 380 lines test

---

### Stage 3: Integration & Finalization
**Duration:** 1 day | **Tasks:** D.5, D.6, D.7

**Day 3 Morning: Tasks D.5 & D.7 (Parallel)**
- Agent: feature-developer
- **Task D.5:** Update `converter_gui.py`
  - Remove old Step 5 methods (~138 lines)
  - Remove old Step 7 methods (~313 lines)
  - Add step instances:
    ```python
    self.step_instances[4] = FieldMappingStep(self)  # Step 5
    self.step_instances[6] = BalancePreviewStep(self)  # Step 7
    ```
  - Target size: ~700 lines (from 1,211)
- **Task D.7:** Update `gui_steps/__init__.py`
  - Add imports and exports for new steps

**Day 3 Afternoon: Task D.6 - Integration Testing**
- Agent: unit-test-generator
- Run full test suite: `python3 -m unittest discover tests -v`
- Verify 448 tests passing (401 + 47 new)
- Test complete wizard flow (navigate through all 7 steps)
- Test conversion workflow end-to-end
- Verify zero regressions

**End of Day 3:** Orchestrator finalized, all tests passing

---

### Stage 4: Quality & Documentation
**Duration:** 1 day | **Tasks:** D.8, D.9, D.10

**Day 4 Morning: Task D.8 - Code Quality Review**
- Agent: code-quality-reviewer
- Review all Phase D code
- Assign grade (target: A+)
- Document any issues
- Address critical/high-priority issues

**Day 4 Afternoon: Task D.9 - Documentation (Parallel)**
- Agent: feature-developer
- Update **CLAUDE.md:**
  - Module structure (add new step files)
  - Test counts (401 → 448)
  - converter_gui.py size (1,211 → ~700)
  - Phase D completion section
- Update **GUI_STEP_EXTRACTION_PLAN.md:**
  - Mark Phase D complete
  - Add Phase D metrics
  - Update Phase D gate status
- Update **GUI_STEP_EXTRACTION_TASKS.md:**
  - Update task status (mark D.1-D.10 complete)
  - Update overall progress
  - Update Phase D gate status

**Day 5: Task D.10 - Release Prep**
- Agent: feature-developer
- Verify all Phase D gate criteria met
- Create comprehensive commit message
- Commit changes
- Push to main
- Verify SonarCloud workflow passes

**End of Day 5:** Phase D complete and verified

---

## Parallelization Opportunities

1. **D.1 + D.2:** Test writing can start as soon as FieldMappingStep interface is defined
2. **D.3 + D.4:** Test writing can start as soon as BalancePreviewStep interface is defined
3. **D.5 + D.7:** Small tasks can be done together
4. **D.8 + D.9:** Review and documentation can overlap

---

## Risk Mitigation

### Step 5 Risks

**Risk:** Complex UI with many widgets
- **Mitigation:** Break into sub-methods (`_create_field_mapping_section()`, `_create_composite_description_section()`)

**Risk:** Dynamic column options
- **Mitigation:** Mock CSV headers in tests, use `self.csv_headers` from parent

**Risk:** Validation coordination
- **Mitigation:** Test validation methods separately, test integration

### Step 7 Risks

**Risk:** Integration with BalanceManager/TransactionManager
- **Mitigation:** Use existing manager patterns, dependency injection via constructor

**Risk:** Real-time label updates
- **Mitigation:** Store label references in `_widgets` dict, update via helper methods

**Risk:** Context menu binding
- **Mitigation:** Delegate to TransactionManager, pass tree widget reference

**Risk:** State management (deleted transactions)
- **Mitigation:** Use parent's Set, don't duplicate state

### Integration Risks

**Risk:** Breaking existing wizard flow
- **Mitigation:** Run all 401 tests after each change, test navigation manually

**Risk:** SonarCloud failure
- **Mitigation:** Verify 215 non-GUI tests still pass, check for import errors

**Risk:** Performance degradation
- **Mitigation:** Maintain lazy UI creation, only build UI when step shown

---

## Critical Success Factors

1. **Follow existing patterns** - Steps 1-6 provide proven templates
2. **Maintain helper integrations** - Don't break BalanceManager/TransactionManager
3. **Test incrementally** - Run tests after each task completion
4. **Document thoroughly** - Update CLAUDE.md immediately after code changes
5. **Verify gate criteria early** - Check line counts and test counts daily

---

## Expected Final Metrics (Post-Phase D)

### Production Code
- `src/gui_steps/field_mapping_step.py`: ~250 lines
- `src/gui_steps/balance_preview_step.py`: ~400 lines
- `src/gui_steps/__init__.py`: +2 exports
- `src/converter_gui.py`: ~700 lines (reduced from 1,211)
- **Net result: ~150 new lines, converter_gui.py to ~700 lines**

### Test Code
- `tests/test_gui_steps/test_field_mapping_step.py`: ~350 lines (20-25 tests)
- `tests/test_gui_steps/test_balance_preview_step.py`: ~380 lines (22-25 tests)
- **Total new tests: 42-50 tests (estimate 47 tests per task plan)**

### Final Metrics
- **Total tests:** 448 (401 + 47)
- **converter_gui.py:** ~700 lines (from 1,211)
- **Test-to-code ratio:** Maintained at ~1.9:1
- **Code quality grade:** A+
- **SonarCloud:** 215/215 non-GUI tests passing

---

## Quick Command Reference

### Running Tests

```bash
# Run all tests
python3 -m unittest discover tests -v

# Run specific test module
python3 -m unittest tests.test_gui_steps.test_field_mapping_step -v
python3 -m unittest tests.test_gui_steps.test_balance_preview_step -v

# Run all GUI step tests
python3 -m unittest tests.test_gui_steps -v
```

### Code Quality Check

```bash
# Run flake8
flake8 src/gui_steps/field_mapping_step.py
flake8 src/gui_steps/balance_preview_step.py

# Check line counts
wc -l src/converter_gui.py
wc -l src/gui_steps/*.py
```

### Git Operations

```bash
# Check status
git status

# Create comprehensive commit
git add -A
git commit -m "feat(phase-d): Complete Phase D - Extract Steps 5 & 7 (Tasks D.1-D.10)

- Extract FieldMappingStep (Step 5) with field mapping UI
- Extract BalancePreviewStep (Step 7) with balance calculations
- Integrate steps into orchestrator
- Add 47 new tests (401 → 448 total)
- Reduce converter_gui.py by ~500 lines (1,211 → ~700)
- Code quality: Grade A+
- All 448 tests passing

Phase D Gate: PASSED"

# Push to trigger SonarCloud
git push origin main
```

### Verify SonarCloud

```bash
# Watch workflow
gh run watch

# List recent runs
gh run list --workflow=sonar.yml --limit 3

# View specific run
gh run view <run-id>
```

---

## Next Steps After Phase D

Once Phase D is complete and gate criteria are met:

**Phase E: Final Cleanup & Release**
- E.1: Remove any remaining legacy code
- E.2: Performance optimization
- E.3: Final documentation pass
- E.4: Version bump to v3.1.0
- E.5: Create release tag and GitHub release

---

## Document History

| Date | Author | Changes |
|------|--------|---------|
| 2025-11-24 | Claude Code | Initial creation - comprehensive Phase D plan |

---

**END OF PHASE D EXECUTION PLAN**
