# Release Checklist

Use this checklist when preparing a new release of CSV to OFX Converter.

## Pre-Release

### 1. Code Quality

- [ ] All tests passing: `python3 -m unittest discover tests -v`
- [ ] Verify test count is correct (39 tests total)
- [ ] Code follows PEP8 standards
- [ ] No debugging code or print statements left in
- [ ] Log messages are appropriate and helpful
- [ ] All TODOs addressed or documented
- [ ] Documentation updated (CLAUDE.md, README.md, README.pt-BR.md)

### 2. Version Update

- [ ] Update version in `README.md` (line ~462)
- [ ] Update version in `README.pt-BR.md` (line ~462)
- [ ] Update changelog in both README files
- [ ] Update "Last Updated" date in documentation
- [ ] Decide version number (semantic versioning):
  - Patch (x.x.1): Bug fixes only
  - Minor (x.1.0): New features, backward compatible
  - Major (1.0.0): Breaking changes

### 3. Documentation

- [ ] README.md is up to date
- [ ] README.pt-BR.md matches English version
- [ ] All new features documented
- [ ] Examples updated if needed
- [ ] CODE_EXAMPLES.md updated if API changed
- [ ] BUILD.md reflects current build process
- [ ] AI disclaimer present and clear

### 4. Testing

- [ ] Test on sample CSV files
- [ ] Test date validation feature
- [ ] Test with Brazilian format CSV
- [ ] Test with standard format CSV
- [ ] Verify OFX output in financial software
- [ ] Test error handling
- [ ] Test GUI on target platform (if possible)

### 5. Build Testing

- [ ] Build succeeds locally:
  - [ ] Linux: `./build.sh`
  - [ ] Windows: `build.bat` (if available)
  - [ ] macOS: `./build.sh` (if available)
- [ ] Executable runs without errors
- [ ] Executable size is reasonable (< 50MB)
- [ ] All GUI elements render correctly
- [ ] File dialogs work
- [ ] CSV parsing works in executable

## Release Process

### 6. Prepare Repository

- [ ] All changes committed to main branch
- [ ] Repository is clean: `git status`
- [ ] Remote is up to date: `git pull origin main`
- [ ] Create release branch (optional): `git checkout -b release-v1.x.x`

### 7. Create Tag

```bash
# Replace x.x.x with your version
git tag -a v1.x.x -m "Release version 1.x.x"
git push origin v1.x.x
```

- [ ] Tag created with correct format: `vMAJOR.MINOR.PATCH`
- [ ] Tag pushed to GitHub
- [ ] Tag message includes brief summary

### 8. Monitor Build

- [ ] Go to GitHub Actions: `https://github.com/YOUR_USERNAME/conversor-csv-ofx/actions`
- [ ] Watch workflow execution
- [ ] All jobs complete successfully:
  - [ ] Build on Ubuntu (Linux)
  - [ ] Build on Windows
  - [ ] Build on macOS
  - [ ] Create Release
- [ ] Check for any errors in logs

### 9. Verify Release

- [ ] Release appears on Releases page
- [ ] All executables attached:
  - [ ] `csv-to-ofx-converter-linux-x64`
  - [ ] `csv-to-ofx-converter-windows-x64.exe`
  - [ ] `csv-to-ofx-converter-macos-x64`
- [ ] Checksums file attached
- [ ] Release notes are complete and accurate
- [ ] Download links work
- [ ] Version number is correct

## Post-Release

### 10. Test Downloads

- [ ] Download Linux executable
  - [ ] File downloads completely
  - [ ] SHA256 checksum matches
  - [ ] Executable runs: `./csv-to-ofx-converter-linux-x64`
- [ ] Download Windows executable (if possible)
  - [ ] File downloads completely
  - [ ] SHA256 checksum matches
  - [ ] Opens without errors
- [ ] Download macOS executable (if possible)
  - [ ] File downloads completely
  - [ ] SHA256 checksum matches
  - [ ] Runs after `chmod +x`

### 11. Documentation Update

- [ ] Update main README if needed
- [ ] Add release announcement (if applicable)
- [ ] Update any external documentation
- [ ] Post in discussions/forums if needed

### 12. Announcement

- [ ] Create release announcement (optional)
- [ ] Share on social media (optional)
- [ ] Notify users (optional)
- [ ] Update project website (optional)

### 13. Cleanup

- [ ] Delete release branch if created
- [ ] Archive old releases (keep last 3-5)
- [ ] Clean up build artifacts locally
- [ ] Update issue tracker with "Fixed in vX.X.X" tags

## Rollback Procedure

If something goes wrong:

### Delete Release (if needed)

1. Go to Releases page
2. Click on the problematic release
3. Click "Delete release"
4. Confirm deletion

### Delete Tag

```bash
# Delete local tag
git tag -d v1.x.x

# Delete remote tag
git push origin :refs/tags/v1.x.x
```

### Fix and Re-release

1. Fix the issues
2. Commit changes
3. Create new tag (same or incremented version)
4. Push and repeat process

## Common Issues

### Workflow Doesn't Trigger

**Check:**
- Tag format is correct (`v1.2.3`)
- Tag is pushed to GitHub
- Workflow file is in `.github/workflows/`
- Branch protection rules don't block tags

### Build Fails

**Check:**
- All dependencies available
- PyInstaller version compatible
- Python version matches (3.11)
- File paths are correct
- Review GitHub Actions logs

### Executables Don't Work

**Check:**
- Built for correct platform
- All required files included
- Permissions set correctly (Linux/macOS)
- Antivirus not blocking (Windows)
- Test locally first

### Release Notes Missing

**Check:**
- `RELEASE_NOTES.md` generated correctly
- Workflow completed successfully
- GitHub token has proper permissions

## Version History Template

Add to CHANGELOG section in README:

```markdown
### Version X.Y.Z (Month YYYY)
- **New Feature**: Description of feature
  - Sub-feature 1
  - Sub-feature 2
- **Bug Fix**: Description of fix
- **Improvement**: Description of improvement
- Documentation updates
```

## Testing Checklist for Each Platform

### Windows Testing
- [ ] Double-click executable opens GUI
- [ ] No console window appears
- [ ] File dialogs work
- [ ] Can browse for CSV file
- [ ] Can save OFX file
- [ ] Date validation dialog appears and works
- [ ] Log file is created

### macOS Testing
- [ ] Executable runs after chmod +x
- [ ] GUI renders correctly
- [ ] File dialogs are native
- [ ] All fonts display properly
- [ ] Keyboard shortcuts work
- [ ] Can read and write files

### Linux Testing
- [ ] Executable runs after chmod +x
- [ ] Tkinter GUI displays
- [ ] File dialogs work
- [ ] Can access file system
- [ ] Proper error messages
- [ ] No missing dependencies

## Quick Reference

### Version Naming
- `v1.0.0` - Major release
- `v1.1.0` - Minor release (new features)
- `v1.1.1` - Patch release (bug fixes)
- `v1.1.0-beta` - Pre-release
- `v1.1.0-rc1` - Release candidate

### Important Files to Update
1. `README.md` - Version, changelog, date
2. `README.pt-BR.md` - Version, changelog, date
3. Git tag - Create and push

### Build Commands
```bash
# Local build
./build.sh  # or build.bat on Windows

# Clean build
rm -rf build dist __pycache__ *.spec.bak

# Test (recommended)
python3 -m unittest discover tests -v

# Alternative test methods
python3 tests/run_all_tests.py
python3 -m unittest tests.test_csv_parser
python3 -m unittest tests.test_ofx_generator
python3 -m unittest tests.test_date_validator
python3 -m unittest tests.test_integration
```

### Git Commands
```bash
# Create tag
git tag -a v1.2.3 -m "Release 1.2.3"

# Push tag
git push origin v1.2.3

# List tags
git tag -l

# Delete tag
git tag -d v1.2.3
git push origin :refs/tags/v1.2.3
```

---

**Remember**: Always test locally before releasing! Better to catch issues early than to have to roll back a release.

**Tip**: Consider creating a beta/pre-release first for major versions to get user feedback before the final release.
