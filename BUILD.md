# Build and Release Guide

> 🇧🇷 **[Leia em Português (pt-BR)](BUILD.pt-BR.md)**

This document explains how to build the CSV to OFX Converter as a standalone executable and how the automated release process works.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Building Locally](#building-locally)
3. [GitHub Actions Workflow](#github-actions-workflow)
4. [Creating a Release](#creating-a-release)
5. [Troubleshooting](#troubleshooting)

## Quick Start

### For End Users

**Download pre-built executables** from the [Releases page](https://github.com/YOUR_USERNAME/conversor-csv-ofx/releases).

No build required!

### For Developers

Build your own executable:

```bash
# Linux/macOS
./build.sh

# Windows
build.bat
```

## Building Locally

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Install PyInstaller

```bash
pip install pyinstaller
```

### Step 2: Build the Executable

#### Option A: Using Build Scripts (Recommended)

**Linux/macOS:**
```bash
chmod +x build.sh
./build.sh
```

**Windows:**
```cmd
build.bat
```

#### Option B: Using PyInstaller Directly

```bash
pyinstaller csv_to_ofx_converter.spec
```

#### Option C: Manual PyInstaller Command

**Linux/macOS:**
```bash
pyinstaller --onefile \
  --name="csv-to-ofx-converter" \
  --add-data "README.md:." \
  --add-data "README.pt-BR.md:." \
  --windowed \
  --noconfirm \
  src/csv_to_ofx_converter.py
```

**Windows:**
```cmd
pyinstaller --onefile ^
  --name="csv-to-ofx-converter" ^
  --add-data "README.md;." ^
  --add-data "README.pt-BR.md;." ^
  --windowed ^
  --noconfirm ^
  src/csv_to_ofx_converter.py
```

### Step 3: Find Your Executable

The built executable will be in the `dist/` directory:

- **Linux/macOS**: `dist/csv-to-ofx-converter`
- **Windows**: `dist/csv-to-ofx-converter.exe`

### Step 4: Test the Executable

Run the executable to ensure it works:

```bash
# Linux/macOS
./dist/csv-to-ofx-converter

# Windows
dist\csv-to-ofx-converter.exe
```

## GitHub Actions Workflow

The project uses GitHub Actions to automatically build executables for all platforms when you create a release.

### Workflow File

Location: `.github/workflows/build-and-release.yml`

### What It Does

1. **Triggers on**:
   - Push of version tags (e.g., `v1.1.0`)
   - Manual workflow dispatch

2. **Builds on**:
   - Ubuntu (Linux x64)
   - Windows (Windows x64)
   - macOS (macOS x64)

3. **Generates**:
   - Standalone executables for each platform
   - SHA256 checksums
   - Release notes

4. **Publishes**:
   - Creates a GitHub Release
   - Attaches all executables
   - Includes checksums and documentation links

### Build Matrix

| Platform | OS | Output |
|----------|----|---------|
| Linux | ubuntu-latest | csv-to-ofx-converter-linux-x64 |
| Windows | windows-latest | csv-to-ofx-converter-windows-x64.exe |
| macOS | macos-latest | csv-to-ofx-converter-macos-x64 |

## Creating a Release

### Automatic Release (Recommended)

1. **Update version in code** (if needed):
   ```python
   # In src/csv_to_ofx_converter.py or README.md
   __version__ = "1.2.0"
   ```

2. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Release version 1.2.0"
   ```

3. **Create and push a version tag**:
   ```bash
   git tag v1.2.0
   git push origin v1.2.0
   ```

4. **Wait for GitHub Actions** to complete (usually 5-10 minutes)

5. **Check the Releases page** for your new release with attached executables

### Manual Release

If you need to trigger the workflow manually:

1. Go to **Actions** tab in your GitHub repository
2. Click on **Build and Release** workflow
3. Click **Run workflow**
4. Select branch and click **Run workflow** button

## Release Process Details

### Version Tagging

Use semantic versioning: `vMAJOR.MINOR.PATCH`

Examples:
- `v1.0.0` - Initial release
- `v1.1.0` - New features (date validation)
- `v1.1.1` - Bug fixes
- `v2.0.0` - Breaking changes

### What Gets Included in a Release

1. **Executables**:
   - Linux: `csv-to-ofx-converter-linux-x64`
   - Windows: `csv-to-ofx-converter-windows-x64.exe`
   - macOS: `csv-to-ofx-converter-macos-x64`

2. **Checksums**:
   - `checksums.txt` with SHA256 hashes

3. **Release Notes**:
   - Download instructions
   - Platform-specific installation steps
   - Links to documentation
   - Version information
   - Build date

## Build Configuration

### PyInstaller Spec File

The `csv_to_ofx_converter.spec` file controls the build:

```python
# Key settings:
- onefile: True          # Single executable
- windowed: True         # No console window (GUI only)
- console: False         # Hides console
- upx: True             # Compress with UPX
```

### Included Files

Automatically bundled in the executable:
- `README.md` - English documentation
- `README.pt-BR.md` - Portuguese documentation
- All Python standard library modules
- Tkinter GUI library

### Excluded Files

Not included (to reduce size):
- Test files (`tests/`)
- Build scripts
- Git files
- Development documentation

## Troubleshooting

### Build Fails with "Module not found"

**Problem**: PyInstaller can't find a module

**Solution**: Add to `hiddenimports` in spec file:
```python
hiddenimports=['missing_module'],
```

### Executable is Too Large

**Problem**: File size over 50MB

**Solutions**:
1. Enable UPX compression: `upx: True`
2. Exclude unused modules in spec file
3. Use `--exclude-module` flag

### "Permission denied" on Linux/macOS

**Problem**: Can't execute the file

**Solution**:
```bash
chmod +x csv-to-ofx-converter
```

### Windows Security Warning

**Problem**: "Windows protected your PC"

**Solution**: This is normal for unsigned executables:
1. Click "More info"
2. Click "Run anyway"

**For distribution**: Consider code signing (requires certificate)

### macOS "Cannot be opened because developer cannot be verified"

**Problem**: macOS Gatekeeper blocks the app

**Solution**:
1. Right-click the app
2. Select "Open"
3. Click "Open" in dialog

**Or via Terminal**:
```bash
xattr -d com.apple.quarantine csv-to-ofx-converter-macos-x64
```

### Build Works Locally but Fails in GitHub Actions

**Problem**: Different environment

**Solutions**:
1. Check Python version matches (3.11 in workflow)
2. Verify all dependencies are listed
3. Check file paths (use forward slashes)
4. Review GitHub Actions logs

### Release Not Created

**Problem**: Workflow runs but no release

**Check**:
1. Tag starts with `v` (e.g., `v1.0.0`)
2. Tag is pushed to GitHub: `git push origin v1.0.0`
3. GITHUB_TOKEN has proper permissions
4. No other release with same tag exists

## Advanced Configuration

### Adding an Icon

1. Create or obtain an icon file:
   - Windows: `.ico` file (256x256 or multiple sizes)
   - macOS: `.icns` file
   - Linux: `.png` file

2. Update spec file:
   ```python
   icon='path/to/icon.ico'
   ```

### Code Signing (Optional)

For production distribution, consider signing:

**Windows**:
```bash
signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com csv-to-ofx-converter.exe
```

**macOS**:
```bash
codesign --deep --force --verify --verbose --sign "Developer ID" csv-to-ofx-converter
```

### Optimization Tips

1. **Reduce Size**:
   ```python
   excludes=['test', 'unittest', 'pdb', 'pydoc'],
   ```

2. **Faster Startup**:
   ```python
   noarchive=False,  # Faster but larger
   ```

3. **Debug Build**:
   ```python
   debug=True,      # For troubleshooting
   console=True,    # Show console output
   ```

## Continuous Integration

### Workflow Triggers

The workflow can be triggered by:

1. **Tag push** (automatic):
   ```bash
   git tag v1.2.0 && git push origin v1.2.0
   ```

2. **Manual dispatch** (manual):
   - Go to Actions > Build and Release > Run workflow

3. **API call** (automated):
   ```bash
   curl -X POST \
     -H "Accept: application/vnd.github.v3+json" \
     -H "Authorization: token YOUR_TOKEN" \
     https://api.github.com/repos/USER/REPO/actions/workflows/build-and-release.yml/dispatches \
     -d '{"ref":"main"}'
   ```

## Testing Before Release

Before creating an official release:

1. **Test locally**:
   ```bash
   ./build.sh
   ./dist/csv-to-ofx-converter
   ```

2. **Run tests**:
   ```bash
   python3 -m unittest tests.test_converter -v
   ```

3. **Create a pre-release**:
   - Tag with `-rc1`, `-beta`, etc.: `v1.2.0-rc1`
   - Mark as pre-release in GitHub

4. **Get feedback** before final release

## Support

For build issues:
1. Check this document
2. Review GitHub Actions logs
3. Test build locally first
4. Open an issue with:
   - Error messages
   - Build logs
   - Platform/OS version
   - Python version

---

**Last Updated**: November 2025
**Build System**: PyInstaller 6.x
**CI/CD**: GitHub Actions
