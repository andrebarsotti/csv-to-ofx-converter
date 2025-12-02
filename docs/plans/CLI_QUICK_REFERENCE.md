# CLI Implementation - Quick Reference Guide

## Document Index

1. **CLI_IMPLEMENTATION_PLAN.md** (2,062 lines, 67KB)
   - Comprehensive technical specification
   - Architecture diagrams
   - Phased implementation details
   - Module specifications
   - Test strategy
   - Build and deployment

2. **CLI_IMPLEMENTATION_SUMMARY.md** (300 lines, 9.1KB)
   - Executive summary
   - Key metrics
   - Phase overview
   - Quick examples

3. **CLI_PLAN_VALIDATION.md** (300 lines, 9.5KB)
   - Validation against CLAUDE.md
   - Compliance checks
   - Risk assessment
   - Final approval

---

## Quick Stats

| Metric | Value |
|--------|-------|
| **MVP Effort** | 16 days (1 dev) |
| **Complete Effort** | 25 days (1 dev) |
| **New Code (MVP)** | ~5,500 lines |
| **New Code (Complete)** | ~6,250 lines |
| **New Tests (MVP)** | 130 tests |
| **New Tests (Complete)** | 190 tests |
| **Test Coverage** | ~90% |
| **Code Reuse** | 75% |
| **Phases (MVP)** | 3 (Phase 1+4+5) |
| **Phases (Complete)** | 5 (all phases) |
| **New Dependencies** | 0 |
| **Documentation** | ~4,000 lines |
| **Class Docs** | 10 files (5 EN + 5 PT-BR) |
| **Feature Parity (MVP)** | 100% (non-interactive) |

---

## CLI Usage Examples

### Interactive Mode
```bash
csv-to-ofx-cli --interactive
```

### Non-Interactive Basic
```bash
csv-to-ofx-cli -i input.csv -o output.ofx \
  --date-column date \
  --amount-column amount \
  --description-column description
```

### Brazilian Format
```bash
csv-to-ofx-cli -i nubank.csv -o nubank.ofx \
  --delimiter ";" --decimal-separator "," \
  --date-column data --amount-column valor \
  --description-column descricao --currency BRL
```

### Advanced Features
```bash
csv-to-ofx-cli -i input.csv -o output.ofx \
  --date-column date --amount-column amount \
  --description-columns "category,merchant,notes" \
  --description-separator dash \
  --invert-values \
  --validate-dates --start-date 2025-01-01 \
  --end-date 2025-01-31 --date-action adjust
```

---

## Module Structure

```
src/cli/
├── __init__.py
├── cli_parser.py      (~350 lines, 30 tests)
├── cli_wizard.py      (~600 lines, 35 tests)
├── cli_converter.py   (~400 lines, 20 tests)
├── cli_output.py      (~300 lines, 25 tests)
└── cli_utils.py       (~250 lines, 30 tests)

tests/test_cli/
├── __init__.py
├── test_cli_parser.py       (30 tests)
├── test_cli_wizard.py       (35 tests)
├── test_cli_converter.py    (20 tests)
├── test_cli_output.py       (25 tests)
├── test_cli_utils.py        (30 tests)
└── test_cli_integration.py  (15 tests)
```

---

## Implementation Phases

### Phase 1: Foundation (5 days) - P0
- cli_parser with ALL args (composite desc, value inversion, date validation)
- cli_output, cli_converter, cli_utils
- Complete non-interactive mode with 100% feature parity
- 130 tests

### Phase 2: Interactive Wizard (6 days) - P1 (Not MVP)
- CLIWizard with 7 steps reusing Phase 1 logic
- 45 tests

### Phase 3: Polish & Edge Cases (3 days) - P2 (Optional)
- Preview, dry-run, verbose/quiet modes
- Progress indicators, enhanced errors
- 15 tests

### Phase 4: Build & Deploy (3 days) - P1 MVP ✨
- cli.spec, build scripts, GitHub Actions
- 6 executables (3 GUI + 3 CLI)

### Phase 5: Documentation (6 days) - P1 MVP ✨
- CLI_USAGE.md (English + Portuguese)
- Update CLAUDE.md, README.md, README.pt-BR.md
- Create 5 class docs per language (CLIParser, CLIWizard, CLIConverter, CLIOutput, CLIUtils)
- Update docs/en/ and docs/pt-BR/ (architecture, overview)

**MVP Timeline: Phase 1 + Phase 4 + Phase 5 = 16 days**

---

## Test Execution

```bash
# Run all CLI tests
python3 -m unittest discover tests/test_cli -v

# Run specific module
python3 -m unittest tests.test_cli.test_cli_parser
python3 -m unittest tests.test_cli.test_cli_wizard

# Run all tests (including CLI)
python3 -m unittest discover tests -v
# Expected: 623 tests (468 existing + 155 CLI)
```

---

## Build Commands

```bash
# Build both GUI and CLI
./build.sh              # Linux/macOS
build.bat               # Windows

# Outputs:
# - dist/csv-to-ofx-converter      (GUI)
# - dist/csv-to-ofx-cli            (CLI)
```

---

## Success Criteria Checklist

### Phase 1
- [ ] Basic conversion works
- [ ] Help and version flags work
- [ ] Required arguments validated
- [ ] 110 tests passing

### Phase 2
- [ ] Interactive wizard completes 7 steps
- [ ] Output matches GUI for same inputs
- [ ] Ctrl+C cancels gracefully
- [ ] 155 total tests passing

### Phase 3
- [ ] Composite descriptions work
- [ ] Value inversion works
- [ ] Date validation works
- [ ] Balance preview displays

### Phase 4
- [ ] Both executables build successfully
- [ ] Cross-platform builds pass
- [ ] GitHub Actions workflow succeeds
- [ ] 6 executables attached to release

### Phase 5
- [ ] CLI_USAGE.md complete and tested
- [ ] CLI_USAGE.pt-BR.md translated
- [ ] CLAUDE.md updated
- [ ] README.md includes CLI section
- [ ] All examples work

---

## Key Files to Update

### New Files
- `cli.py` (entry point)
- `src/cli/*.py` (5 modules)
- `tests/test_cli/*.py` (6 test modules)
- `cli.spec` (PyInstaller config)
- `docs/CLI_USAGE.md`
- `docs/CLI_USAGE.pt-BR.md`

### Updated Files
- `CLAUDE.md` (module structure, tests)
- `README.md` (CLI section)
- `README.pt-BR.md` (CLI section)
- `build.sh` (dual executables)
- `build.bat` (dual executables)
- `.github/workflows/build-and-release.yml`
- `.github/workflows/sonar.yml`

---

## Common Commands

```bash
# Phase 1 Development
python3 cli.py --help
python3 cli.py -i sample.csv -o output.ofx --date-column date --amount-column amount --description-column desc

# Phase 2 Development
python3 cli.py --interactive

# Testing
python3 -m unittest tests.test_cli.test_cli_parser -v
python3 -m unittest discover tests/test_cli -v

# Building
./build.sh
ls -lh dist/

# Documentation
code docs/CLI_USAGE.md
code CLAUDE.md
```

---

## Resources

- **Full Plan:** CLI_IMPLEMENTATION_PLAN.md
- **Summary:** CLI_IMPLEMENTATION_SUMMARY.md
- **Validation:** CLI_PLAN_VALIDATION.md
- **Project Guidelines:** ../../CLAUDE.md
- **GUI Refactoring Reference:** GUI_REFACTORING_PLAN.md

---

**Quick Reference Version:** 1.0  
**Last Updated:** December 2, 2025
