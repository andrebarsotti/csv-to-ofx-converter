# GUI Step Extraction - Task Delegation Plan

## Document Overview

**Purpose:** Break down the GUI Step Extraction Plan into specific, delegable tasks for parallel development  
**Source Plan:** `docs/plans/GUI_STEP_EXTRACTION_PLAN.md`  
**Total Timeline:** 15 working days (3 weeks)  
**Total Tasks:** 47 tasks across 5 phases  
**Agents:** feature-developer, unit-test-generator, code-quality-reviewer  

**Critical Path:**
Phase A → Phase B → Phase C → Phase D → Phase E (all sequential)

**Parallelization Opportunities:**
- Within each phase: Step implementation + test creation can run in parallel
- Code quality review can run in parallel with next phase planning

**Status:** 🟢 Phase A Complete (November 23, 2025) | 🟡 Phase B In Progress (Tasks B.1-B.2 Complete)

---

## Overall Progress

**Completion Status:** 10/47 tasks (21%)

### Phase Completion
- ✅ **Phase A (Infrastructure):** 8/8 tasks (100%) - COMPLETED November 23, 2025
- 🟡 **Phase B (Simple Steps):** 2/9 tasks (22%) - IN PROGRESS (Tasks B.1-B.2 complete)
- ⏳ **Phase C (Medium Steps):** 0/8 tasks (0%) - NOT STARTED
- ⏳ **Phase D (Complex Steps):** 0/10 tasks (0%) - NOT STARTED
- ⏳ **Phase E (Cleanup):** 0/12 tasks (0%) - NOT STARTED

### Metrics Achieved

**Phase A (Infrastructure):**
- Production Code: 388 lines (355 + 33)
- Test Code: 585 lines (32 tests)
- Total Tests: 262 (230 existing + 32 new)
- Code Quality: Grade A
- All Acceptance Criteria: Met

**Phase B Tasks B.1-B.2 (FileSelectionStep):**
- Production Code: 194 lines (file_selection_step.py)
- Test Code: 444 lines (24 tests)
- Total Tests: 286 (262 existing + 24 new)
- All tests passing
- Zero regressions

---

## Executive Summary

This document transforms the GUI Step Extraction Plan into 47 specific, actionable tasks organized across 5 phases. Each task includes:
- Specific agent assignment (feature-developer, unit-test-generator, code-quality-reviewer)
- Clear acceptance criteria
- Dependencies and sequencing
- Estimated effort and LOC
- Files to create/modify
- Testing requirements

**Key Metrics:**
- 47 tasks total
- 15 working days
- 24 feature-developer tasks (51%)
- 17 unit-test-generator tasks (36%)
- 6 code-quality-reviewer tasks (13%)
- Deliverables: 8 production files + 8 test files + updated docs
- Result: 700 line reduction in converter_gui.py (50% smaller), 170+ new tests

---

## Task Summary by Phase

| Phase | Focus | Tasks | Duration | Key Deliverables |
|-------|-------|-------|----------|------------------|
| A | Infrastructure | 8 | 5 days | Base class, package, 30+ tests |
| B | Simple Steps (1,2,4) | 9 | 3 days | 3 step classes, 45+ tests |
| C | Medium Steps (3,6) | 8 | 2 days | 2 step classes, 38+ tests |
| D | Complex Steps (5,7) | 10 | 3 days | 2 step classes, 47+ tests, orchestrator |
| E | Cleanup & Release | 12 | 2 days | Optimization, docs, v3.1.0 release |

---

## Phase A: Infrastructure (Week 1, Days 1-5) - ✅ COMPLETED

**Status:** ✅ COMPLETED November 23, 2025
**Commit:** `c4fc0d2` - "feat(phase-a): Add WizardStep base class infrastructure"
**Goal:** Establish base class, package structure, and testing infrastructure
**Success Criteria:** ✅ All met - Base class tests passing (32/32), zero regressions (262/262 tests pass), code quality A grade  

### Task A.1 - Create Base Class Infrastructure ✅ COMPLETED

**Status:** ✅ COMPLETED November 23, 2025
**Agent:** feature-developer
**Priority:** P0 (Critical - blocks all other phases)
**Duration:** 1.5 days (Actual: Completed in Phase A)
**Dependencies:** None  

**Description:**
Create the `WizardStep` abstract base class with complete lifecycle management, dataclasses for configuration and data return, and helper methods for safe parent access.

**Files to Create:**
- `/workspaces/csv-to-ofx-converter/src/gui_wizard_step.py` (~150 lines)

**Implementation Requirements:**

See docs/plans/GUI_STEP_EXTRACTION_PLAN.md sections 3-4 for complete specifications.

Key components:
1. `StepConfig` dataclass (7 fields)
2. `StepData` dataclass (3 fields with __post_init__)
3. `WizardStep` abstract base class with:
   - Lifecycle methods: create(), show(), hide(), destroy()
   - Abstract methods: _build_ui(), _collect_data(), _validate_data()
   - Helper methods: log(), get_parent_data(), set_parent_data()

**Acceptance Criteria:**
- [x] Base class compiles without errors
- [x] All abstract methods properly defined
- [x] Dataclasses have proper type hints
- [x] Docstrings follow Google/NumPy style
- [x] PEP8 compliant (verified by flake8)
- [x] No circular import issues

**Estimated LOC:** 150 lines (Actual: 355 lines - more comprehensive than planned)

---

### Task A.2 - Create Package Structure ✅ COMPLETED

**Status:** ✅ COMPLETED November 23, 2025
**Agent:** feature-developer
**Priority:** P0 (Critical)
**Duration:** 0.5 days (Actual: Completed in Phase A)
**Dependencies:** A.1

**Description:**
Create the `gui_steps/` package directory structure with proper `__init__.py` file.

**Files to Create:**
- `/workspaces/csv-to-ofx-converter/src/gui_steps/__init__.py` (~20 lines)

**Acceptance Criteria:**
- [x] Package directory exists
- [x] __init__.py is valid Python
- [x] Package can be imported
- [x] No import errors

**Estimated LOC:** 20 lines (Actual: 33 lines)

---

### Task A.3 - Create Base Class Unit Tests ✅ COMPLETED

**Status:** ✅ COMPLETED November 23, 2025
**Agent:** unit-test-generator
**Priority:** P0 (Critical)
**Duration:** 1.5 days (Actual: Completed in Phase A)
**Dependencies:** A.1

**Description:**
Create comprehensive unit tests for the `WizardStep` base class covering all lifecycle methods, dataclasses, and edge cases.

**Files to Create:**
- `/workspaces/csv-to-ofx-converter/tests/test_gui_wizard_step.py` (~250 lines)

**Test Requirements:**
- Dataclass tests (8 tests)
- Base class tests (12 tests)
- Concrete implementation tests with MockWizardStep (10 tests)
- **Total: 30+ tests**

**Acceptance Criteria:**
- [x] All 30+ tests pass (Actual: 32 tests, all passing)
- [x] Test coverage ≥ 95% for base class
- [x] Tests use proper mocking (no GUI dependencies)
- [x] Tests run in < 5 seconds (Actual: 0.746s)
- [x] Tests are independent (no shared state)

**Estimated LOC:** 250 lines (Actual: 585 lines - more comprehensive than planned)

---

### Tasks A.4 through A.8 - All Completed ✅

**Note:** Tasks A.4 through A.8 were completed as part of Phase A but are not individually detailed in this document. All tasks met their acceptance criteria:

- ✅ **Task A.4:** Test package structure
- ✅ **Task A.5:** Update main module exports (csv_to_ofx_converter.py)
- ✅ **Task A.6:** Code quality review (Grade: A, APPROVED)
- ✅ **Task A.7:** Integration testing (262/262 tests passing)
- ✅ **Task A.8:** Update documentation (CLAUDE.md)

**Phase A Summary:**
- All 8 tasks completed successfully
- 388 lines of production code added
- 585 lines of test code added (32 tests)
- Total test count: 262 (230 existing + 32 new)
- Code quality: Grade A
- Commit: `c4fc0d2`

---

## Phase B: Simple Steps (Tasks B.1 through B.9) - NOT STARTED

(Phase B tasks to be initiated next...)

---

## Summary Metrics

### Code Metrics

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| converter_gui.py | 1,400 lines | ~700 lines | -50% |
| Total Production Code | ~3,500 lines | ~4,790 lines | +1,290 lines |
| Total Test Code | ~3,861 lines | ~5,241 lines | +1,380 lines |
| Test Count | 230 tests | 400+ tests | +74% |
| Test Modules | 9 modules | 16 modules | +78% |
| Code Coverage | ~85% | 90%+ | +5%+ |

### Agent Workload Distribution

- **feature-developer:** 24 tasks (51%)
- **unit-test-generator:** 17 tasks (36%)
- **code-quality-reviewer:** 6 tasks (13%)

### Deliverables

**Production Code (8 new files):**
1. gui_wizard_step.py (150 lines)
2. gui_steps/__init__.py (30 lines)
3-9. Seven step classes (100-250 lines each)

**Test Code (8 new files):**
1. test_gui_wizard_step.py (250 lines)
2. test_gui_steps/__init__.py (10 lines)
3-9. Seven step test files (120-220 lines each)

**Total New Code:** ~2,670 lines (1,290 production + 1,380 test)

---

## Critical Success Factors

### Phase Gates

Each phase must meet these criteria before proceeding:

**Phase A Gate:**
- [ ] Base class tests passing (30+ tests)
- [ ] Total tests: 260+ (230 existing + 30 new)
- [ ] Code quality grade: A
- [ ] Zero regressions

**Phase B Gate:**
- [ ] Steps 1, 2, 4 functional
- [ ] Total tests: 305+ (260 + 45 new)
- [ ] converter_gui.py: ~1,200 lines
- [ ] Code quality grade: A
- [ ] Zero regressions

**Phase C Gate:**
- [ ] Steps 3, 6 functional
- [ ] Total tests: 343+ (305 + 38 new)
- [ ] converter_gui.py: ~1,000 lines
- [ ] Code quality grade: A
- [ ] Zero regressions

**Phase D Gate:**
- [ ] All 7 steps functional
- [ ] Total tests: 390+ (343 + 47 new)
- [ ] converter_gui.py: ~700 lines
- [ ] Code quality grade: A
- [ ] Zero regressions

**Phase E Gate (Production Release):**
- [ ] All 400+ tests passing
- [ ] converter_gui.py ≤ 750 lines
- [ ] Zero PEP8 violations
- [ ] Code quality grade: A or A+
- [ ] Documentation complete
- [ ] Sign-offs received (CQR + Tech Lead + PM)

### Risk Mitigation

1. **Breaking Changes:** Each phase independently releasable with rollback plan
2. **Performance:** Benchmarks in Phase E, lazy UI creation
3. **Testing:** Mock objects, no GUI dependencies, 90%+ coverage
4. **Timeline:** Aggressive breakdown (47 tasks), daily tracking
5. **Quality:** Code review gates at each phase

---

## Implementation Guidance

### For feature-developer

**Your 24 Tasks:**
- Phase A: Base class, package, exports, docs (4 tasks)
- Phase B: Steps 1/2/4, orchestrator update (4 tasks)
- Phase C: Steps 3/6, orchestrator update, release prep (4 tasks)
- Phase D: Steps 5/7, orchestrator finalize, docs, release prep (5 tasks)
- Phase E: Cleanup, optimization, docs, release (7 tasks)

**Quality Checklist Before Marking Complete:**
- [ ] Code compiles without errors
- [ ] PEP8 compliant (flake8 passes)
- [ ] Docstrings complete (Google/NumPy style)
- [ ] Type hints added
- [ ] No TODOs or FIXMEs
- [ ] Manual testing done
- [ ] Ready for unit tests

### For unit-test-generator

**Your 17 Tasks:**
- Phase A: Base class tests, package tests, integration (3 tasks)
- Phase B: Steps 1/2/4 tests, integration (4 tasks)
- Phase C: Steps 3/6 tests, integration (3 tasks)
- Phase D: Steps 5/7 tests, integration (4 tasks)
- Phase E: Orchestrator tests, final integration (3 tasks)

**Quality Checklist Before Marking Complete:**
- [ ] All tests pass
- [ ] Coverage ≥ 90% (run coverage tool)
- [ ] No GUI dependencies
- [ ] Tests run in < 5 seconds (per module)
- [ ] Clear test names and docstrings
- [ ] Edge cases covered
- [ ] Error scenarios covered

### For code-quality-reviewer

**Your 6 Tasks:**
- Phase A: Review base class (1 task)
- Phase B: Review simple steps (1 task)
- Phase C: Review medium steps (1 task)
- Phase D: Review complex steps (1 task)
- Phase E: Comprehensive review + final sign-off (2 tasks)

**Review Deliverables Template:**
```markdown
# Code Quality Review - Phase X

## Metrics
- PEP8 Compliance: [%]
- Test Coverage: [%]
- Lines of Code: [#]

## Findings
### Critical Issues (must fix before proceeding)
### High Priority Issues (should fix)
### Medium/Low Issues (nice to fix)

## Grade: [A+ / A / A- / B / C / D / F]

## Decision: ☐ APPROVED ☐ REJECTED
```

---

## Execution Timeline

### Week 1: Infrastructure
- Day 1-2: Base class + tests
- Day 3: Package + exports + review
- Day 4-5: Integration testing + docs

### Week 2 (Days 1-3): Simple Steps
- Day 6: Steps 1 & 2 + tests (parallel)
- Day 7: Step 4 + orchestrator update
- Day 8: Integration + review

### Week 2 (Days 4-5): Medium Steps
- Day 9: Steps 3 & 6 + tests (parallel)
- Day 10: Integration + review + release prep

### Week 3 (Days 1-3): Complex Steps
- Day 11: Steps 5 & 7 + tests (parallel)
- Day 12: Orchestrator finalize + integration
- Day 13: Review + docs + release prep

### Week 3 (Days 4-5): Cleanup & Release
- Day 14: Cleanup + optimization + final tests
- Day 15: Final review + sign-offs + v3.1.0 release

---

## Detailed Task List

**Note:** Due to length constraints, this document provides the framework and first few tasks. The complete 47 tasks follow this pattern:

**Phase A (8 tasks):**
- A.1: Create base class
- A.2: Create package
- A.3: Base class tests
- A.4: Test package structure
- A.5: Update main module exports
- A.6: Code quality review
- A.7: Integration testing
- A.8: Documentation

**Phase B (9 tasks):**
- B.1: Extract Step 1
- B.2: Step 1 tests
- B.3: Extract Step 2
- B.4: Step 2 tests
- B.5: Extract Step 4
- B.6: Step 4 tests
- B.7: Update orchestrator
- B.8: Integration testing
- B.9: Review & docs

**Phase C (8 tasks):**
- C.1: Extract Step 3
- C.2: Step 3 tests
- C.3: Extract Step 6
- C.4: Step 6 tests
- C.5: Update orchestrator
- C.6: Integration testing
- C.7: Review & docs
- C.8: Release prep

**Phase D (10 tasks):**
- D.1: Extract Step 5
- D.2: Step 5 tests
- D.3: Extract Step 7
- D.4: Step 7 tests
- D.5: Finalize orchestrator
- D.6: Integration testing
- D.7: Update package exports
- D.8: Code quality review
- D.9: Documentation
- D.10: Release prep

**Phase E (12 tasks):**
- E.1: Remove backward compatibility
- E.2: Optimize orchestrator
- E.3: Add orchestrator integration tests
- E.4: Performance testing
- E.5: Comprehensive code quality review
- E.6: Fix critical/high issues
- E.7: Update all documentation
- E.8: Final integration testing
- E.9: Create release notes
- E.10: Prepare release artifacts
- E.11: Final sign-off (GATE)
- E.12: Production release

---

## References

- **Source Plan:** /workspaces/csv-to-ofx-converter/docs/plans/GUI_STEP_EXTRACTION_PLAN.md
- **Project Docs:** /workspaces/csv-to-ofx-converter/CLAUDE.md
- **Current Codebase:** /workspaces/csv-to-ofx-converter/src/converter_gui.py (1,400 lines)
- **Test Suite:** /workspaces/csv-to-ofx-converter/tests/ (230 tests currently)

For detailed specifications of each step class, validation rules, UI requirements, and code examples, refer to sections 4-6 of the GUI Step Extraction Plan.

---

*Document Version: 1.0*  
*Created: November 22, 2025*  
*Author: Tech Lead Coordinator*  
*Status: Ready for Execution*  
*Next Action: Begin Phase A, Task A.1*
