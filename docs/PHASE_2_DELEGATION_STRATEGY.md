# Phase 2 Delegation Strategy

## Executive Summary

**Status:** ✅ APPROVED for execution by Product Manager and Tech Lead

Both reviews confirm that Phase 2 and Phase 3 tasks can be successfully delegated to specialized agents:
- **feature-developer**: Handles all refactoring work
- **code-quality-reviewer**: Validates quality after each section
- **unit-test-generator**: Only needed if Phase 3 executes (new modules require tests)

---

## Recommended Approach: 3-Section Sequential

### Phase 2 Breakdown (13 hours, 2 work days)

**Section 1: Validation Methods** (~3 hours, ~100 lines)
- Replace inline validation with `gui_utils` calls
- Methods: `_validate_file_selection()`, `_validate_required_fields()`, `_validate_description_mapping()`
- Risk: LOW - Pure logic extraction
- Agent: **feature-developer**

**Section 2: Date & Numeric Operations** (~5 hours, ~230 lines)
- Replace date formatting and numeric validation
- Methods: `_format_date_entry()`, `_validate_numeric_input()`, `_parse_date_for_sorting()`
- Risk: MEDIUM - Tkinter widget state management
- Agent: **feature-developer**

**Section 3: Display & Statistics** (~3 hours, ~120 lines)
- Replace balance display and statistics formatting
- Methods: `_update_final_balance_display()`, preview stats, conversion stats
- Risk: LOW - Simple string formatting
- Agent: **feature-developer**

**Final Verification** (~2 hours)
- Comprehensive code quality review
- Metrics validation (file size, method count)
- Agent: **code-quality-reviewer**

---

## Agent Task Specifications

### Section 1: Validation Methods

**Agent:** feature-developer

**Task:**
```
Refactor validation methods in src/converter_gui.py to use gui_utils functions:
1. _validate_file_selection() → gui_utils.validate_csv_file_selection()
2. _validate_required_fields() → gui_utils.validate_required_field_mappings()
3. _validate_description_mapping() → gui_utils.validate_description_mapping()
4. _validate_conversion_prerequisites() → gui_utils.validate_conversion_prerequisites()

Constraints:
- Do NOT change method signatures (public API)
- Do NOT modify __init__ or widget creation
- Import gui_utils functions locally within methods
- Extract StringVar.get() values before passing to gui_utils

Success Criteria:
- Lines reduced by ~80-100
- All 167 tests pass
- No new pylint/flake8 warnings
```

### Section 2: Date & Numeric Operations

**Agent:** feature-developer

**Task:**
```
Refactor date and numeric methods in src/converter_gui.py:
1. _format_date_entry() → use gui_utils.format_date_string() + calculate_cursor_position_after_format()
2. _validate_numeric_input() → gui_utils.validate_numeric_input()
3. _parse_date_for_sorting() → gui_utils.parse_date_for_sorting()

Constraints:
- Keep Tkinter widget manipulation in converter_gui.py
- gui_utils only processes data, NOT UI
- Maintain exact cursor position behavior

Success Criteria:
- Date formatting: 60 lines → ~15 lines
- Numeric validation: 40 lines → ~8 lines
- Date sorting: 30 lines → ~3 lines
- Total reduction: ~180 lines
- All 167 tests pass
- Manual test: date entry formatting works correctly
```

### Section 3: Display & Statistics

**Agent:** feature-developer

**Task:**
```
Refactor display and statistics methods in src/converter_gui.py:
1. _update_final_balance_display() → gui_utils.format_balance_value()
2. Preview stats formatting → gui_utils.format_preview_stats()
3. Conversion stats formatting → gui_utils.format_conversion_stats()

Success Criteria:
- Lines reduced by ~40
- All 167 tests pass
- Manual test: balance preview displays correctly
```

### Final Verification

**Agent:** code-quality-reviewer

**Task:**
```
Comprehensive review of all Phase 2 changes:

Code Quality Checklist:
✓ All refactored methods use gui_utils correctly
✓ No duplicate logic
✓ PEP8 compliance (flake8 src/converter_gui.py)
✓ No new pylint warnings
✓ Docstrings updated

Architecture Checklist:
✓ gui_utils.py has ZERO imports from converter_gui
✓ gui_utils.py has ZERO Tkinter dependencies
✓ No circular dependencies
✓ All gui_utils functions remain pure

Testing Checklist:
✓ All 167 tests pass
✓ Manual smoke test: python3 main.py works

Metrics Checklist:
✓ File size: <1,500 lines (target: <1,000)
✓ Code complexity reduced
✓ Methods simplified

Approval Criteria:
- All checkboxes checked
- Zero regressions
- Code quality grade: A or better
```

---

## Quality Gates

**After Section 1:**
```bash
python3 -m unittest discover tests -v
# All 167 tests must pass → Proceed to Section 2
# If fails → Fix issues, re-test, then proceed
```

**After Section 2:**
```bash
python3 -m unittest discover tests -v
python3 main.py  # Manual test: date entry, numeric validation
# Both pass → Proceed to Section 3
# If fails → Fix issues, re-test, then proceed
```

**After Section 3:**
```bash
python3 -m unittest discover tests -v
python3 main.py  # Manual test: complete workflow
# Both pass → Proceed to Final Verification
# If fails → Fix issues, re-test, then proceed
```

**After Final Verification:**
```bash
wc -l src/converter_gui.py  # Verify file size
flake8 src/converter_gui.py  # Verify code quality
python3 -m unittest discover tests -v  # Verify tests
# All pass → Commit changes, update CLAUDE.md, DONE
```

---

## Phase 3 Decision Criteria

**Evaluate AFTER Phase 2 completion:**

### Objective Metrics

**File Size:**
```bash
wc -l src/converter_gui.py

IF > 1,200 lines → Phase 3 RECOMMENDED
IF ≤ 1,000 lines → Phase 3 NOT NEEDED
ELSE → Phase 3 OPTIONAL (consult user)
```

**Method Count:**
```bash
grep -c "def " src/converter_gui.py

IF > 40 methods → Phase 3 RECOMMENDED
IF ≤ 30 methods → Phase 3 NOT NEEDED
ELSE → Phase 3 OPTIONAL (acceptable)
```

**Prediction:** Phase 3 likely NOT needed
- Expected reduction: ~450 lines
- Estimated post-Phase 2: ~1,200-1,400 lines
- Close to target, acceptable complexity

### Phase 3 Scope (IF NEEDED)

**Extract ONLY ONE subsystem** (not all three):

**Option A: Conversion Handler** (~400 lines) - RECOMMENDED
- Create `src/gui_conversion_handler.py`
- Extract: `_convert()`, `_process_csv_rows()`, date validation dialog
- Requires: **unit-test-generator** to create `tests/test_gui_conversion_handler.py`

**Option B: Balance Manager** (~300 lines)
- Create `src/gui_balance_manager.py`
- Extract: `_calculate_balance_preview()`, `_recalculate_balance_preview()`

**Option C: Transaction Manager** (~200 lines)
- Create `src/gui_transaction_manager.py`
- Extract: Context menu operations, delete/restore

---

## Risk Management

### Technical Risks & Mitigations

**Risk 1: Breaking Tkinter widget state** (Section 2)
- Mitigation: Keep widget manipulation in converter_gui.py
- Pattern: gui_utils processes data → converter_gui updates UI

**Risk 2: Test failures from cumulative changes**
- Mitigation: Test after EVERY section, fix before proceeding
- Rollback: `git checkout HEAD -- src/converter_gui.py`

**Risk 3: Import circular dependencies**
- Mitigation: gui_utils NEVER imports converter_gui
- Enforcement: code-quality-reviewer verifies in final review

**Risk 4: Agent over-refactors (scope creep)**
- Mitigation: Very specific acceptance criteria per section
- Instruction: "Only replace specified methods"

---

## Execution Timeline

### 2-Day Schedule

**Day 1:**
- Morning: Section 1 (Validation) - 3 hours
  - feature-developer: Implement
  - code-quality-reviewer: Review
  - feature-developer: Fix issues (if any)
- Afternoon: Section 2 (Date & Numeric) - 5 hours
  - feature-developer: Implement
  - code-quality-reviewer: Review
  - feature-developer: Fix issues (if any)

**Day 2:**
- Morning: Section 3 (Display & Statistics) - 3 hours
  - feature-developer: Implement
  - code-quality-reviewer: Review
  - feature-developer: Fix issues (if any)
- Afternoon: Final Verification - 2 hours
  - code-quality-reviewer: Comprehensive review
  - Metrics validation
  - Documentation updates (CLAUDE.md)
  - Decision: Phase 3 needed?

**Day 3-4 (OPTIONAL):**
- Phase 3 execution (if metrics indicate it's needed)
- unit-test-generator: Create tests for extracted module
- feature-developer: Extract subsystem
- code-quality-reviewer: Final validation

---

## Success Criteria

### Phase 2 Completion

**Quantitative Goals:**
- ✓ converter_gui.py: 2,097 → <1,000 lines (stretch) or <1,500 lines (acceptable)
- ✓ Method count: 63 → <30 methods
- ✓ Tests: All 167 passing
- ✓ Regressions: Zero

**Qualitative Goals:**
- ✓ Code more readable (inline logic → named function calls)
- ✓ Methods focused on GUI orchestration (not business logic)
- ✓ Error handling consistent (utility function return values)
- ✓ Developer can understand wizard flow without implementation details

### Phase 3 Completion (if executed)

**Quantitative Goals:**
- ✓ converter_gui.py: <700 lines
- ✓ Method count: <25 methods
- ✓ Tests: 187-197 passing (20-30 new tests for extracted module)
- ✓ Regressions: Zero

---

## Approvals

✅ **Product Manager:** P1 priority, 2-day timeline approved, phased approach validated
✅ **Tech Lead:** Architecture sound, risk mitigation adequate, technical feasibility confirmed
✅ **Code Quality (Phase 1):** A+ grade, foundation solid, ready to proceed

---

## Next Steps

1. **User Decision:** Approve execution of Phase 2?
2. **If Yes:** Create git feature branch `refactor/gui-phase-2`
3. **Execute:** Section 1 → Section 2 → Section 3 → Final Verification
4. **Decide:** Phase 3 needed based on metrics
5. **Complete:** Update documentation, merge to main

---

*Document Version: 1.0*
*Last Updated: November 21, 2025*
*Status: READY FOR EXECUTION*
