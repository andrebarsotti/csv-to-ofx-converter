# Dependency Management Guide

## Overview

This project follows a minimal dependency philosophy:
- **Runtime:** Uses only Python standard library (no external dependencies)
- **Development:** Uses industry-standard tools for building, testing, and code quality

## Requirements Files

### requirements.txt
Contains runtime dependencies (currently empty - project uses only standard library).

```bash
# No runtime dependencies needed
# Application uses only Python standard library
```

### requirements-dev.txt
Contains development tools and dependencies:

```bash
# Install development dependencies
pip install -r requirements-dev.txt
```

**Included packages:**
- `pyinstaller` - Build standalone executables
- `flake8` - Code linting (PEP8 compliance)
- `black` - Code formatting
- `pylint` - Code analysis
- `mypy` - Static type checking

## Installation in Codespaces

### Automatic Installation

When you create or rebuild a Codespace:

1. **During build** - Dockerfile installs `requirements-dev.txt`
2. **After creation** - `post-create.sh` verifies and upgrades packages

No manual action required!

### Manual Installation

If you need to reinstall or update dependencies:

```bash
# Install/upgrade development dependencies
pip install --upgrade -r requirements-dev.txt

# Install specific package
pip install package-name

# Verify installation
pip list
pip show package-name
```

## Adding New Dependencies

### Adding Runtime Dependencies

If you need to add an external library (not recommended, but possible):

1. **Add to requirements.txt:**
   ```bash
   echo "package-name>=1.0.0" >> requirements.txt
   ```

2. **Install locally:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Update documentation:**
   - Update [CLAUDE.md](../CLAUDE.md) - note the new dependency
   - Update [README.md](../README.md) - installation instructions
   - Update [README.pt-BR.md](../README.pt-BR.md) - Portuguese version

4. **Update build configuration:**
   - Check `csv_to_ofx_converter.spec` - ensure PyInstaller includes it
   - Test build: `./build.sh`

5. **Commit changes:**
   ```bash
   git add requirements.txt
   git commit -m "feat: Add [package-name] dependency"
   ```

### Adding Development Dependencies

For linters, formatters, or development tools:

1. **Add to requirements-dev.txt:**
   ```bash
   echo "package-name>=1.0.0" >> requirements-dev.txt
   ```

2. **Install locally:**
   ```bash
   pip install -r requirements-dev.txt
   ```

3. **Update Codespaces config (optional):**
   - Rebuild container to include in base image
   - Or let `post-create.sh` install it automatically

4. **Commit changes:**
   ```bash
   git add requirements-dev.txt
   git commit -m "chore: Add [package-name] dev dependency"
   ```

## Version Pinning

### Philosophy

- **Minimum versions** (`>=`) for flexibility
- **Exact versions** (`==`) only when necessary for compatibility
- **Compatible versions** (`~=`) for minor updates

### Examples

```bash
# Minimum version (recommended for dev tools)
black>=22.10.0

# Exact version (use when needed)
pyinstaller==6.3.0

# Compatible release (major.minor)
mypy~=0.991  # allows 0.991, 0.992, but not 1.0
```

### Updating Versions

```bash
# Show outdated packages
pip list --outdated

# Update specific package
pip install --upgrade package-name

# Update all dev dependencies
pip install --upgrade -r requirements-dev.txt

# Freeze current versions (for documentation)
pip freeze > requirements-frozen.txt
```

## Verification

### Check Installed Packages

```bash
# List all packages
pip list

# Show specific package info
pip show pyinstaller

# Check package location
pip show -f black
```

### Verify Dependencies

Run the verification script:

```bash
.devcontainer/verify-setup.sh
```

This checks:
- ✓ Python version
- ✓ Tkinter availability
- ✓ PyInstaller installation
- ✓ Development tools (black, flake8)

## Troubleshooting

### Package Not Found

```bash
# Update pip
pip install --upgrade pip

# Clear cache and reinstall
pip cache purge
pip install --no-cache-dir -r requirements-dev.txt
```

### Version Conflicts

```bash
# Check dependency tree
pip show package-name

# Force reinstall
pip install --force-reinstall package-name

# Use specific version
pip install package-name==1.2.3
```

### Import Errors

```bash
# Verify package is installed
pip show package-name

# Check Python path
echo $PYTHONPATH
python3 -c "import sys; print(sys.path)"

# Test import
python3 -c "import package_name; print(package_name.__version__)"
```

## Best Practices

### 1. Keep Runtime Dependencies Minimal
- Use standard library when possible
- Avoid external dependencies for core functionality
- Consider vendoring small utilities instead

### 2. Use Virtual Environments Locally
```bash
# Create virtual environment
python3 -m venv venv

# Activate
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate.bat  # Windows

# Install dependencies
pip install -r requirements-dev.txt
```

### 3. Test Before Committing
```bash
# Run tests
python3 -m unittest discover tests -v

# Build executable
./build.sh

# Test executable
./dist/csv-to-ofx-converter
```

### 4. Document Changes
- Update CHANGELOG if adding major dependencies
- Update documentation files
- Add comments in requirements files

### 5. Security Updates
```bash
# Check for security vulnerabilities
pip install safety
safety check

# Update vulnerable packages
pip install --upgrade package-name
```

## Codespaces-Specific Notes

### Persistence

- Packages installed via Dockerfile persist in container image
- Packages installed via `post-create.sh` are reinstalled each time
- Packages installed manually may be lost on rebuild

### Rebuilding Container

To apply Dockerfile changes:

1. Open Command Palette: `Ctrl+Shift+P` (Linux/Windows) or `Cmd+Shift+P` (macOS)
2. Select: `Codespaces: Rebuild Container`
3. Wait for rebuild and automatic setup

### Pre-built Containers

For faster startup, consider:
- Adding common packages to Dockerfile
- Using devcontainer prebuilds
- Caching pip packages

## References

- [Python Packaging Guide](https://packaging.python.org/)
- [pip Documentation](https://pip.pypa.io/)
- [Requirements File Format](https://pip.pypa.io/en/stable/reference/requirements-file-format/)
- [PyInstaller Manual](https://pyinstaller.readthedocs.io/)
- [PEP 440 - Version Specifiers](https://www.python.org/dev/peps/pep-0440/)

---

**Questions?** Check [CLAUDE.md](../CLAUDE.md) or create an issue on GitHub.
