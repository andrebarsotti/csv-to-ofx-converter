# CLI Implementation Plan - Executive Summary

## Overview

This document provides a high-level summary of the comprehensive technical implementation plan for adding a command-line interface (CLI) to the CSV to OFX Converter application.

**Full Technical Plan:** [CLI_IMPLEMENTATION_PLAN.md](CLI_IMPLEMENTATION_PLAN.md) (2,062 lines)

---

## Key Metrics

| Metric | Value |
|--------|-------|
| **MVP Effort** | 16 working days (1 developer) |
| **Complete Effort** | 25 working days (all phases) |
| **New Code (MVP)** | ~5,500 lines |
| **New Code (Complete)** | ~6,250 lines |
| **New Tests (MVP)** | 130 tests (598 total) |
| **New Tests (Complete)** | 190 tests (658 total) |
| **Test Coverage** | ~90% for CLI modules |
| **Code Reuse** | 75% (6/8 core modules) |
| **Feature Parity** | 100% (non-interactive MVP) |
| **New Dependencies** | 0 (argparse from stdlib) |
| **Phases** | 3 MVP phases + 2 optional |
| **Documentation** | ~4,000 lines (EN + PT-BR) |
| **Class Docs** | 10 new files (5 EN + 5 PT-BR) |

---

## Architecture Summary

### Entry Points

- **main.py** - GUI entry point (unchanged)
- **cli.py** - NEW CLI entry point

### New Modules (src/cli/ package)

1. **cli_parser.py** (~350 lines) - argparse wrapper, argument validation
2. **cli_wizard.py** (~600 lines) - Interactive 7-step wizard
3. **cli_converter.py** (~400 lines) - Conversion orchestrator
4. **cli_output.py** (~300 lines) - Terminal output formatting
5. **cli_utils.py** (~250 lines) - Pure utility functions

### Core Modules Reused

- CSVParser
- OFXGenerator
- DateValidator
- ConversionHandler
- transaction_utils
- BalanceManager

**Key Design Principle:** Maximize code reuse, delegate to existing core classes, maintain zero new dependencies.

---

## Implementation Phases

### Phase 1: Foundation and Non-Interactive Core (P0 - MVP)
- **Duration:** 7 days
- **Deliverables:**
  - cli_parser with ALL arguments (composite desc, value inversion, date validation)
  - cli_output, cli_converter, cli_utils, cli.py entry point
  - Complete non-interactive mode with full feature parity
- **Tests:** 130 tests
- **Acceptance:** Non-interactive CLI with ALL core features working

### Phase 2: Interactive Wizard Mode (P1 - High Priority, Not MVP)
- **Duration:** 6 days
- **Deliverables:**
  - CLIWizard class with 7 interactive steps
  - Reuses ALL Phase 1 conversion logic
- **Tests:** 45 tests
- **Acceptance:** Interactive mode with feature parity to GUI wizard

### Phase 3: Polish & Edge Cases (P2 - Optional, Not MVP)
- **Duration:** 3 days
- **Deliverables:**
  - Preview mode (--preview)
  - Dry-run mode (--dry-run)
  - Verbose/quiet modes (--verbose, --quiet)
  - Progress indicators and enhanced error messages
- **Tests:** 15 tests
- **Acceptance:** Polish features enhance usability

### Phase 4: Build and Deployment (P1 - MVP Required)
- **Duration:** 3 days
- **Deliverables:** cli.spec, updated build scripts, GitHub Actions updates
- **Tests:** Build verification
- **Acceptance:** 6 executables (3 GUI + 3 CLI) per release

### Phase 5: Documentation and Polish (P1 - MVP Required)
- **Duration:** 6 days
- **Deliverables:**
  - CLI_USAGE.md (English + Portuguese)
  - Updated CLAUDE.md, README.md, README.pt-BR.md
  - Updated docs/en/ technical documentation (README, architecture.md, overview.md)
  - 5 new class docs in docs/en/classes/ (CLIParser, CLIWizard, CLIConverter, CLIOutput, CLIUtils)
  - 5 new class docs in docs/pt-BR/classes/ (all Portuguese translations)
  - RELEASE_CHECKLIST.md and CHANGELOG for v4.0.0
- **Tests:** Documentation review
- **Acceptance:** All documentation complete, accurate, and approved

---

## Usage Examples

### Interactive Mode

```bash
csv-to-ofx-cli --interactive
```

Prompts through 7 steps:
1. File Selection
2. CSV Format
3. Data Preview
4. OFX Configuration
5. Field Mapping
6. Advanced Options
7. Balance Preview

### Non-Interactive Mode

```bash
# Simple conversion
csv-to-ofx-cli -i input.csv -o output.ofx \
  --date-column date \
  --amount-column amount \
  --description-column description

# Brazilian format with date validation
csv-to-ofx-cli -i nubank.csv -o nubank.ofx \
  --delimiter ";" --decimal-separator "," \
  --date-column data --amount-column valor \
  --description-column descricao \
  --validate-dates --start-date 2025-01-01 \
  --end-date 2025-01-31 --date-action adjust \
  --currency BRL

# Composite descriptions
csv-to-ofx-cli -i transactions.csv -o output.ofx \
  --date-column date --amount-column amount \
  --description-columns "category,merchant,notes" \
  --description-separator dash
```

---

## Test Strategy Summary

### Test Distribution

```
Total Tests: 623
├── Core Tests: 94 (15.1%)
├── GUI Utility Tests: 121 (19.4%)
├── GUI Integration Tests: 253 (40.6%) - Skipped in CI
└── CLI Tests: 155 (24.9%) - NEW, Run in CI
```

### CI/CD Execution

- **Tests Run in CI:** 370 (94 core + 121 GUI utils + 155 CLI)
- **Tests Skipped in CI:** 253 (GUI integration, require display server)
- **Total Test Suite:** 623 tests

### Coverage Targets

- cli_utils.py: 95%+
- cli_parser.py: 90%+
- cli_converter.py: 90%+
- cli_output.py: 85%+
- cli_wizard.py: 85%+

---

## Build and Deployment

### Executables per Release

**GUI Executables:**
1. csv-to-ofx-converter-linux-x64
2. csv-to-ofx-converter-windows-x64.exe
3. csv-to-ofx-converter-macos-x64

**CLI Executables:**
4. csv-to-ofx-cli-linux-x64
5. csv-to-ofx-cli-windows-x64.exe
6. csv-to-ofx-cli-macos-x64

**Plus:** SHA256SUMS.txt

### Build Scripts

- **build.sh** - Updated to build both GUI and CLI (Linux/macOS)
- **build.bat** - Updated to build both GUI and CLI (Windows)
- **csv_to_ofx_converter.spec** - GUI executable (unchanged)
- **cli.spec** - NEW CLI executable configuration

### GitHub Actions

- Updated build-and-release.yml to produce 6 executables
- Updated sonar.yml to run CLI tests (370 tests in CI)

---

## Documentation Deliverables

### New Documents

1. **CLI_USAGE.md** (~1,000 lines) - Comprehensive CLI guide (English)
2. **CLI_USAGE.pt-BR.md** (~1,000 lines) - Portuguese translation

### Updated Documents

1. **CLAUDE.md** - CLI module structure, test info, architecture
2. **README.md** - CLI Quick Start section, examples
3. **README.pt-BR.md** - Translated CLI section
4. **RELEASE_CHECKLIST.md** - Dual executable build process

---

## Risk Assessment

### Critical Risks (Mitigated)

1. **Import conflicts** - Mitigated by separate entry points (main.py vs cli.py)
2. **Breaking ConversionHandler API** - Mitigated by dependency injection, stable API
3. **CI/CD pipeline breaking** - Mitigated by incremental updates, local testing

### Medium Risks (Managed)

1. **CLI tests failing without TTY** - Mitigated by mocking stdin/stdout
2. **Cross-platform terminal differences** - Mitigated by graceful degradation
3. **Users confused by dual executables** - Mitigated by clear naming, documentation

### Low Risks (Accepted)

1. **Scope creep** - Managed by phased plan, P0/P1/P2 prioritization
2. **Timeline slippage** - Managed by daily tracking, adjustable scope

---

## Success Criteria

### Functional

- ✅ CLI accepts all arguments via command-line
- ✅ Interactive wizard prompts through all 7 steps
- ✅ CLI generates identical OFX as GUI for same inputs
- ✅ Date validation, composite descriptions, value inversion work
- ✅ Error messages are clear and actionable

### Non-Functional

- ✅ All 623 tests passing
- ✅ Zero regressions in GUI
- ✅ CLI test coverage ≥85%
- ✅ PEP8 compliance
- ✅ Documentation complete (English + Portuguese)
- ✅ Build succeeds on Linux, Windows, macOS

---

## Feature Parity Matrix

| Feature | GUI | CLI Interactive | CLI Non-Interactive |
|---------|-----|-----------------|---------------------|
| File selection | ✅ | ✅ | ✅ |
| CSV format config | ✅ | ✅ | ✅ |
| Data preview | ✅ | ✅ | ❌ |
| OFX configuration | ✅ | ✅ | ✅ |
| Field mapping | ✅ | ✅ | ✅ |
| Composite descriptions | ✅ | ✅ | ✅ |
| Value inversion | ✅ | ✅ | ✅ |
| Date validation | ✅ | ✅ | ✅ |
| Balance preview | ✅ | ✅ | ❌ |
| Transaction deletion | ✅ | ✅ | ❌ |
| Multiple currencies | ✅ | ✅ | ✅ |
| Initial balance | ✅ | ✅ | ✅ |

**Parity Score:** 13/15 features = 87%

(Non-interactive mode intentionally omits data preview, balance preview, and transaction deletion)

---

## Dependencies and Constraints

### Dependencies

- **Python:** 3.7+ (no change)
- **Standard Library Only:**
  - argparse (Python 3.2+)
  - sys, os, logging, typing
- **No New External Dependencies!**

### Constraints

1. **Zero new runtime dependencies** - Maintained
2. **Backward compatibility** - GUI unchanged, all existing imports work
3. **Cross-platform** - Linux, Windows, macOS support
4. **PEP8 compliance** - All CLI code follows project standards
5. **Test coverage** - ≥85% for all CLI modules
6. **Documentation** - English + Portuguese for all user-facing docs

---

## Next Steps

### Immediate Actions

1. **Review and approve** this implementation plan
2. **Create feature branch** `feature/cli-implementation`
3. **Set up project board** with 5 phases and tasks
4. **Assign developer(s)** to Phase 1

### Phase 1 Kickoff

1. Create `src/cli/` package structure
2. Implement `cli_utils.py` (30 tests)
3. Implement `CLIOutput` class (25 tests)
4. Implement `CLIParser` class (30 tests)
5. Create `cli.py` entry point
6. Verify all 110 Phase 1 tests passing

### Tracking

- **Daily standup** to track progress
- **Code reviews** after each module completion
- **Documentation updates** in parallel with code
- **Testing** continuously, not just at phase end

---

## References

- **Full Technical Plan:** [CLI_IMPLEMENTATION_PLAN.md](CLI_IMPLEMENTATION_PLAN.md)
- **Project Guidelines:** [CLAUDE.md](../../CLAUDE.md)
- **GUI Refactoring Reference:** [GUI_REFACTORING_PLAN.md](GUI_REFACTORING_PLAN.md)
- **Release Checklist:** [RELEASE_CHECKLIST.md](../../RELEASE_CHECKLIST.md)

---

**Document Version:** 1.0  
**Date:** December 2, 2025  
**Author:** Tech Lead Coordinator  
**Status:** READY FOR APPROVAL
