# Release Process

This document provides the complete release process for the CSV to OFX Converter application.

## Overview

**IMPORTANT**: Always follow the comprehensive checklist in `RELEASE_CHECKLIST.md` for all releases.

This document provides detailed guidance and commands for the release process. For a step-by-step checklist, see [RELEASE_CHECKLIST.md](../RELEASE_CHECKLIST.md).

---

## Semantic Versioning

We follow [Semantic Versioning 2.0.0](https://semver.org/):

**Version Format**: `MAJOR.MINOR.PATCH` (e.g., `3.1.0`)

**Version Increment Rules**:

1. **PATCH (1.0.X)**: Bug fixes only
   - Fix crashes or errors
   - Correct wrong calculations
   - Update documentation
   - No new features or breaking changes
   - Example: 3.1.0 → 3.1.1

2. **MINOR (1.X.0)**: New features, backward compatible
   - Add new features
   - Add new GUI steps
   - Add new CSV format support
   - Add new OFX fields
   - Improve performance
   - Example: 3.1.0 → 3.2.0

3. **MAJOR (X.0.0)**: Breaking changes
   - Change OFX format version
   - Remove features
   - Change API signatures
   - Require new dependencies
   - Change file formats
   - Example: 3.1.0 → 4.0.0

---

## Pre-Release Verification

Before creating a release, ensure ALL of the following are complete:

### 1. Code Quality & Testing

**Run All Tests**:
```bash
# Run all 493 tests
python3 -m unittest discover tests -v
```

**Expected Result**: All tests pass (493 tests, 0 failures, 0 errors)

**Verify Individual Test Modules**:
```bash
# Verify each module works correctly
python3 -m unittest tests.test_csv_parser
python3 -m unittest tests.test_ofx_generator
python3 -m unittest tests.test_date_validator
python3 -m unittest tests.test_transaction_utils
python3 -m unittest tests.test_gui_utils
python3 -m unittest tests.test_integration
```

**Code Quality Checks**:
```bash
# Check for PEP8 compliance (optional)
flake8 src/ --max-line-length=120

# Verify no debugging code or print statements
grep -r "print(" src/ | grep -v "#" || echo "No print statements found"
```

### 2. Documentation Updates

**Update CLAUDE.md**:
- Update version number if shown
- Add new sections for new features
- Update module structure if files added/removed
- Update test counts if test organization changed

**Update README.md** (English):
- Update version number in header
- Add changelog entry for new version
- Update feature list for new features
- Add examples for new functionality
- Update "Last Updated" date

**Update README.pt-BR.md** (Portuguese):
- Mirror ALL changes from README.md
- Translate new changelog entries
- Translate new feature descriptions
- Update "Última Atualização" date
- Ensure cultural appropriateness

**Update RELEASE_CHECKLIST.md** (if release process changed):
- Add new verification steps
- Update commands if changed
- Update expected behaviors

**Verify Code Comments and Docstrings**:
```bash
# Check that all modules have docstrings
grep -L '"""' src/*.py || echo "All files have docstrings"

# Verify function signatures match docstrings (manual review)
```

### 3. Version Management

**Decide Version Number**:
- Review changes since last release
- Apply semantic versioning rules
- Document decision in changelog

**Update Version in Files**:
```bash
# Update README.md
sed -i 's/Version: [0-9.]\+/Version: X.Y.Z/' README.md

# Update README.pt-BR.md
sed -i 's/Versão: [0-9.]\+/Versão: X.Y.Z/' README.pt-BR.md

# Update CLAUDE.md
sed -i 's/Current Version\*\*: [0-9.]\+/Current Version**: X.Y.Z/' CLAUDE.md

# Verify changes
git diff README.md README.pt-BR.md CLAUDE.md
```

**Update Changelog** (in both README files):
```markdown
## Changelog

### Version X.Y.Z (Month Year)
- **New Feature**: Description of feature
- **Bug Fix**: Description of fix
- **Improvement**: Description of improvement
- **Documentation**: Updates to documentation

### Version X.Y.Z-1 (Previous Month Year)
- Previous changes...
```

### 4. Functional Testing

**Test with Sample CSV Files**:
```bash
# Test with standard format CSV
python3 main.py
# Select examples/standard_format.csv
# Complete wizard, verify OFX output

# Test with Brazilian format CSV
python3 main.py
# Select examples/brazilian_format.csv
# Complete wizard, verify OFX output
```

**Test Date Validation Feature**:
1. Load CSV with transactions outside date range
2. Verify out-of-range dialog appears
3. Test "Keep" action
4. Test "Adjust" action
5. Test "Exclude" action

**Verify OFX Output in Financial Software**:
- Import generated OFX file into financial software (e.g., GnuCash, QuickBooks)
- Verify transactions appear correctly
- Verify amounts are correct
- Verify dates are correct
- Verify transaction types (DEBIT/CREDIT) are correct

**Test Error Handling**:
1. Test with missing file
2. Test with malformed CSV
3. Test with invalid dates
4. Test with invalid amounts
5. Verify helpful error messages displayed

### 5. Build Testing

**Test Local Build**:
```bash
# Linux/macOS
./build.sh

# Windows
build.bat

# Verify build succeeds
ls -lh dist/csv-to-ofx-converter*

# Verify executable runs without errors
./dist/csv-to-ofx-converter-*

# Verify executable size is reasonable (< 50MB)
du -h dist/csv-to-ofx-converter-*

# Test executable functionality
# Run conversion workflow with sample CSV
```

**Verify GUI Elements Render Correctly**:
1. Check window maximization on startup
2. Verify all 7 wizard steps display correctly
3. Check button alignment and spacing
4. Verify Treeview columns display properly
5. Test Back/Next navigation

---

## Release Steps

### 1. Prepare Repository

**Ensure Clean Working Directory**:
```bash
# Check git status
git status

# Expected output: "nothing to commit, working tree clean"

# If uncommitted changes exist, commit them first
git add -A
git commit -m "chore: Prepare release vX.Y.Z"
```

**Pull Latest Changes**:
```bash
# Ensure you have latest changes from remote
git pull origin main
```

**Push All Changes**:
```bash
# Push all changes before creating tag
git push origin main
```

### 2. Create and Push Tag

**Create Annotated Tag**:
```bash
# Create annotated tag with detailed message
git tag -a vX.Y.Z -m "$(cat <<'EOF'
Release version X.Y.Z: Brief Title

Changes:
- New Feature: Description
- Bug Fix: Description
- Improvement: Description
- Documentation: Updates

Testing:
- All 493 tests passing
- Tested on Linux, macOS, Windows
- Compatible with Python 3.7-3.11

Breaking Changes: (if applicable)
- Description of breaking changes

Migration Guide: (if applicable)
- Steps to upgrade from previous version
EOF
)"
```

**Verify Tag Created**:
```bash
# List recent tags
git tag -l | tail -5

# View tag details
git show vX.Y.Z
```

**Push Tag to Trigger GitHub Actions**:
```bash
# Push tag to remote (triggers build-and-release.yml workflow)
git push origin vX.Y.Z
```

### 3. Monitor Build

**Watch GitHub Actions Workflow**:
```bash
# Option 1: Use GitHub CLI to watch workflow
gh run watch

# Option 2: View specific workflow run
gh run list --workflow=build-and-release.yml --limit 5
gh run view <run-id>

# Option 3: Open in browser
# Navigate to: https://github.com/YOUR_USERNAME/csv-to-ofx-converter/actions
```

**Verify All Platform Builds**:

The workflow builds for 3 platforms in parallel:

1. **Ubuntu (Linux x64)**
   - Output: `csv-to-ofx-converter-linux-x64`
   - Expected size: ~15-20 MB

2. **Windows (x64)**
   - Output: `csv-to-ofx-converter-windows-x64.exe`
   - Expected size: ~18-25 MB

3. **macOS (x64)**
   - Output: `csv-to-ofx-converter-macos-x64`
   - Expected size: ~16-22 MB

**Check for Build Errors**:
```bash
# View build logs if any job fails
gh run view <run-id> --log
```

**Common Build Issues**:
- **PyInstaller import errors**: Check `csv_to_ofx_converter.spec` hiddenimports
- **Missing data files**: Verify datas array includes all required files
- **Platform-specific errors**: Check platform-specific build steps

### 4. Verify Release

**Check Release Page**:
```bash
# Open release page in browser
gh release view vX.Y.Z --web

# Or view in terminal
gh release view vX.Y.Z
```

**Verify All Executables Attached**:
- ✅ `csv-to-ofx-converter-linux-x64`
- ✅ `csv-to-ofx-converter-windows-x64.exe`
- ✅ `csv-to-ofx-converter-macos-x64`
- ✅ `checksums.txt` (SHA256 checksums for all executables)

**Verify Release Notes**:
- Title matches tag message
- Changelog is complete
- Breaking changes documented (if any)
- Migration guide included (if needed)

**Test Download Links**:
```bash
# Download Linux executable
gh release download vX.Y.Z --pattern '*linux*'

# Verify file downloaded
ls -lh csv-to-ofx-converter-linux-x64

# Make executable
chmod +x csv-to-ofx-converter-linux-x64

# Test it runs
./csv-to-ofx-converter-linux-x64
```

### 5. Post-Release Testing

**Download Each Platform Executable**:
```bash
# Download all assets
gh release download vX.Y.Z

# List downloaded files
ls -lh csv-to-ofx-converter-*
```

**Verify SHA256 Checksums**:
```bash
# Linux/macOS
sha256sum csv-to-ofx-converter-linux-x64
sha256sum csv-to-ofx-converter-macos-x64

# Compare with checksums.txt
cat checksums.txt

# Windows (PowerShell)
Get-FileHash csv-to-ofx-converter-windows-x64.exe -Algorithm SHA256
```

**Test Executables on Target Platforms**:

**Linux**:
```bash
chmod +x csv-to-ofx-converter-linux-x64
./csv-to-ofx-converter-linux-x64
# Complete a conversion workflow
# Verify OFX file generated correctly
```

**macOS**:
```bash
chmod +x csv-to-ofx-converter-macos-x64
./csv-to-ofx-converter-macos-x64
# May need to allow in System Preferences > Security & Privacy
# Complete a conversion workflow
# Verify OFX file generated correctly
```

**Windows**:
```cmd
csv-to-ofx-converter-windows-x64.exe
REM Complete a conversion workflow
REM Verify OFX file generated correctly
```

**Verify Functionality on Each Platform**:
1. Window opens and maximizes correctly
2. All 7 wizard steps display properly
3. CSV file can be loaded and parsed
4. OFX configuration works
5. Field mapping works
6. Balance preview displays correctly
7. OFX file is generated and valid

---

## Rollback Procedure

If critical issues are discovered after release:

### 1. Delete Release on GitHub

**Option 1: Use GitHub CLI**:
```bash
# Delete the release (keeps the tag)
gh release delete vX.Y.Z --yes
```

**Option 2: Use GitHub Web Interface**:
1. Go to Releases page
2. Click on the release
3. Click "Delete" button
4. Confirm deletion

### 2. Delete Git Tag

**Delete Local Tag**:
```bash
# Delete local tag
git tag -d vX.Y.Z
```

**Delete Remote Tag**:
```bash
# Delete remote tag
git push origin :refs/tags/vX.Y.Z

# Or use --delete flag
git push origin --delete vX.Y.Z
```

### 3. Fix Issues

**Create Fix Branch**:
```bash
# Create branch for fixes
git checkout -b hotfix/vX.Y.Z+1

# Make necessary fixes
# ...

# Commit fixes
git add -A
git commit -m "fix: Critical issue in vX.Y.Z"

# Push and create PR
git push origin hotfix/vX.Y.Z+1
```

**Merge Fixes**:
```bash
# After PR approval, merge to main
git checkout main
git pull origin main
```

### 4. Create New Release

**Create New Tag** (with incremented patch version):
```bash
# Create new tag
git tag -a vX.Y.Z+1 -m "Release version X.Y.Z+1: Bug fixes"

# Push new tag
git push origin vX.Y.Z+1
```

**Monitor New Build**:
```bash
# Watch new workflow
gh run watch
```

---

## CI/CD Workflow Verification

### Checking SonarCloud Workflow

After each push to main (before creating release):

**List Recent Workflow Runs**:
```bash
# List recent SonarCloud workflow runs
gh run list --workflow=sonar.yml --limit 3
```

**View Specific Run**:
```bash
# Get run ID from list above
gh run view <run-id>
```

**Watch Workflow in Real-Time**:
```bash
# Watch most recent workflow run
gh run watch
```

**Expected Behavior**:
- ✅ Workflow status: "completed success"
- ✅ Tests run: 215 tests (94 non-GUI + 121 GUI utility tests)
- ✅ GUI tests excluded:
  - `test_gui_integration.py` (15 tests) - skipped
  - `test_gui_wizard_step.py` (32 tests) - not executed
  - `test_gui_steps/*` (206 tests) - not executed
- ✅ Coverage report generated successfully
- ✅ SonarCloud scan completed without errors

**If Workflow Fails**:

1. **Check Logs**:
   ```bash
   # View detailed logs
   gh run view <run-id> --log
   ```

2. **Look for Test Failures**:
   - Search logs for "FAILED" or "ERROR"
   - Identify which test module failed
   - Run failed test locally: `python3 -m unittest tests.test_module`

3. **Check Tkinter Display Errors**:
   - GUI tests should NOT run in CI
   - If seeing `_tkinter.TclError: couldn't connect to display`:
     - Verify `test_gui_integration.py` has `@unittest.skipIf` decorator
     - Check `.github/workflows/sonar.yml` excludes GUI tests

4. **Verify Exclusions**:
   - Check `sonar-project.properties` for correct exclusions
   - Verify test exclusion patterns in workflow YAML

### Checking Build Workflow

For releases, verify build-and-release workflow:

**List Build Workflow Runs**:
```bash
# List recent build workflow runs
gh run list --workflow=build-and-release.yml --limit 5
```

**View Build Run**:
```bash
# View specific build run
gh run view <run-id>
```

**Expected Behavior**:
- ✅ All 3 platform jobs complete successfully
- ✅ Executables built and uploaded
- ✅ Checksums generated
- ✅ GitHub release created with all assets

---

## Important Files for Releases

### 1. RELEASE_CHECKLIST.md
Complete step-by-step verification checklist for releases.

### 2. README.md
- Version number in header
- Changelog section with release notes
- Feature list (update for new features)
- Last updated date

### 3. README.pt-BR.md
- Portuguese version of README.md
- Version number (Versão)
- Changelog (Histórico de Mudanças)
- Last updated date (Última Atualização)

### 4. CLAUDE.md (now modular)
- Root file: version number, overview
- docs/CLAUDE-ARCHITECTURE.md: architecture updates
- docs/CLAUDE-TESTING.md: test count updates
- docs/CLAUDE-PATTERNS.md: new patterns
- docs/CLAUDE-RELEASE.md: release process updates

### 5. .github/workflows/build-and-release.yml
Automated build workflow configuration.

### 6. csv_to_ofx_converter.spec
PyInstaller build specification.

---

## Release Notes Template

Include in git tag message and GitHub release:

```markdown
Release version X.Y.Z: Brief Title

## Changes

### New Features
- Feature 1: Description
- Feature 2: Description

### Bug Fixes
- Fix 1: Description
- Fix 2: Description

### Improvements
- Improvement 1: Description
- Improvement 2: Description

### Documentation
- Doc update 1: Description
- Doc update 2: Description

## Testing

- All 493 tests passing
- Tested on:
  - Linux (Ubuntu 20.04+)
  - macOS (10.14+)
  - Windows (10, 11)
- Compatible with Python 3.7-3.11

## Breaking Changes

(If applicable)
- Breaking change 1: Description
- Breaking change 2: Description

## Migration Guide

(If applicable)
Steps to upgrade from version X.Y.Z-1:
1. Step 1
2. Step 2
3. Step 3

## Installation

Download the executable for your platform:
- Linux: `csv-to-ofx-converter-linux-x64`
- macOS: `csv-to-ofx-converter-macos-x64`
- Windows: `csv-to-ofx-converter-windows-x64.exe`

Verify checksums using `checksums.txt`.

## Known Issues

(If applicable)
- Issue 1: Description and workaround
- Issue 2: Description and workaround
```

---

## Quick Release Reference

**Complete Release Workflow**:

```bash
# 1. Run all tests
python3 -m unittest discover tests -v

# 2. Update documentation
# - Edit README.md, README.pt-BR.md, CLAUDE.md
# - Update version number and changelog

# 3. Commit changes
git add -A
git commit -m "chore: Prepare release vX.Y.Z"
git push origin main

# 4. Create and push tag
git tag -a vX.Y.Z -m "Release vX.Y.Z: Description"
git push origin vX.Y.Z

# 5. Monitor GitHub Actions
gh run watch

# 6. Verify release
gh release view vX.Y.Z

# 7. Test executables
gh release download vX.Y.Z
# Test on each platform
```

**Emergency Rollback**:

```bash
# Delete release
gh release delete vX.Y.Z --yes

# Delete tags
git tag -d vX.Y.Z
git push origin :refs/tags/vX.Y.Z

# Fix issues and create new release
```

---

## Post-Release Tasks

After successful release:

### 1. Announce Release

**GitHub**:
- Release automatically appears on Releases page
- GitHub sends notifications to watchers

**Social Media** (optional):
- Announce on Twitter, LinkedIn, etc.
- Include link to release page
- Highlight key features

### 2. Update Project Board

If using GitHub Projects:
- Move completed issues to "Released" column
- Close milestone for this version
- Create milestone for next version

### 3. Monitor for Issues

**First 48 Hours**:
- Monitor GitHub Issues for bug reports
- Check for download issues
- Respond to user questions

**First Week**:
- Review analytics (download counts)
- Gather feedback from users
- Plan hotfix if critical issues found

### 4. Plan Next Release

**Create Milestone**:
```bash
# Using GitHub CLI
gh api repos/:owner/:repo/milestones -f title="vX.Y.Z+1" -f description="Next release"
```

**Organize Issues**:
- Label issues for next release
- Prioritize features and bug fixes
- Update project roadmap

---

## Versioning History

Track version history and release dates:

| Version | Date | Type | Highlights |
|---------|------|------|------------|
| 3.1.0 | Nov 2025 | Minor | Date validation, composite descriptions |
| 3.0.0 | Oct 2025 | Major | GUI wizard refactoring (Phase A-D) |
| 2.5.0 | Sep 2025 | Minor | Brazilian format support |
| 2.0.0 | Aug 2025 | Major | GUI introduction |
| 1.0.0 | Jul 2025 | Major | Initial release (CLI) |

---

## Remember

**Always consult RELEASE_CHECKLIST.md for the complete and detailed release process.**

This document provides commands and explanations. The checklist ensures nothing is missed.
