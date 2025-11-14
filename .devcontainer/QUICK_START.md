# Codespaces Quick Start Guide

## 🚀 First Time Setup (Automatic)

When you open this project in Codespaces, everything is configured automatically:

1. ✅ Python 3.11 installed
2. ✅ Tkinter and GUI dependencies installed
3. ✅ Development tools installed (PyInstaller, Black, Flake8)
4. ✅ Test suite runs automatically
5. ✅ Environment variables configured

**Just wait for the post-create script to finish!**

---

## 🎯 Common Tasks

### Run the Application (GUI)

```bash
# Step 1: Start GUI services
start-gui.sh

# Step 2: Open port 6080 in browser (see Ports tab)
# Step 3: Enter password: codespaces

# Step 4: Run the app
python3 main.py
```

### Run Tests

```bash
# All tests (95 tests)
python3 -m unittest discover tests -v

# Specific module
python3 -m unittest tests.test_csv_parser
python3 -m unittest tests.test_ofx_generator
python3 -m unittest tests.test_date_validator
python3 -m unittest tests.test_transaction_utils
python3 -m unittest tests.test_integration

# Single test
python3 -m unittest tests.test_csv_parser.TestCSVParser.test_parse_standard_csv
```

### Build Executable

```bash
# Linux build
./build.sh

# Check output
ls -lh dist/
```

### Code Quality

```bash
# Format code
black src/ tests/

# Check style
flake8 src/ tests/

# Type checking
mypy src/
```

### Verify Setup

```bash
# Run verification script
.devcontainer/verify-setup.sh
```

### Use Claude Code (AI Assistant)

```bash
# Start Claude Code
claude

# Check version
claude --version

# Update
claude update

# Diagnostics
claude doctor
```

**First-time setup:** You'll be prompted to authenticate:
- Option 1: Claude Console (requires billing)
- Option 2: Claude App subscription (Pro/Max)
- Option 3: Enterprise (Bedrock/Vertex AI)

**Example usage:**
```bash
claude
# Then ask questions or request changes:
# "Explain the CSV parser implementation"
# "Add error handling to date validation"
# "Generate unit tests for transaction utils"
```

---

## 🖥️ Accessing the GUI

### Method 1: VS Code Ports Tab (Recommended)
1. Click "Ports" tab at bottom of VS Code
2. Find port **6080** (noVNC)
3. Click the **globe icon** 🌐
4. Enter password: `codespaces`

### Method 2: Direct URL
```
https://<your-codespace-name>-6080.app.github.dev/vnc.html
```

### Default Credentials
- **Password:** `codespaces`
- **Resolution:** 1280x720
- **Color Depth:** 24-bit

---

## 📁 Project Structure

```
csv-to-ofx-converter/
├── main.py                    # Entry point
├── src/
│   ├── csv_to_ofx_converter.py   # Main module
│   ├── csv_parser.py             # CSV parsing
│   ├── ofx_generator.py          # OFX generation
│   ├── date_validator.py         # Date validation
│   ├── converter_gui.py          # Tkinter GUI (7 steps)
│   ├── transaction_utils.py      # Utility functions
│   └── constants.py              # Shared constants
├── tests/
│   ├── test_csv_parser.py        # 8 tests
│   ├── test_ofx_generator.py     # 20 tests
│   ├── test_date_validator.py    # 12 tests
│   ├── test_transaction_utils.py # 50 tests
│   └── test_integration.py       # 5 tests
└── .devcontainer/
    ├── devcontainer.json         # Codespaces config
    ├── Dockerfile                # Container image
    ├── post-create.sh            # Auto setup
    ├── start-gui.sh              # GUI services
    └── verify-setup.sh           # Verification
```

---

## 🔧 Environment Variables

Automatically set in Codespaces:

```bash
DISPLAY=:1                                    # X11 display
PYTHONPATH=/workspaces/csv-to-ofx-converter/src  # Module path
PYTHONUNBUFFERED=1                            # Real-time output
```

---

## 🐛 Troubleshooting

### GUI Services Not Running
```bash
# Check status
ps aux | grep -E "Xvfb|x11vnc|websockify"

# Restart services
pkill -9 Xvfb x11vnc websockify
start-gui.sh
```

### Port 6080 Not Forwarded
1. Go to "Ports" tab in VS Code
2. Click "+" to add port
3. Enter: `6080`
4. Set visibility to "Public"

### Tests Fail
```bash
# Check Python path
echo $PYTHONPATH

# Reinstall if needed
pip install --force-reinstall pyinstaller

# Run individual tests to isolate issue
python3 -m unittest tests.test_csv_parser -v
```

### Display Errors
```bash
# Set display manually
export DISPLAY=:1

# Verify Xvfb is running
ps aux | grep Xvfb
```

### Import Errors
```bash
# Check if in correct directory
pwd  # Should show: /workspaces/csv-to-ofx-converter

# Set Python path
export PYTHONPATH=/workspaces/csv-to-ofx-converter/src:$PYTHONPATH

# Verify imports
python3 -c "from src.csv_parser import CSVParser; print('OK')"
```

---

## 📊 Useful Commands

### System Info
```bash
# Python version
python3 --version

# Tkinter version
python3 -c "import tkinter; print(tkinter.TkVersion)"

# Check installed packages
pip list

# Disk usage
df -h

# Memory usage
free -h
```

### Process Management
```bash
# List Python processes
ps aux | grep python

# Kill all Python processes
pkill -9 python3

# List GUI processes
ps aux | grep -E "Xvfb|vnc|fluxbox"
```

### Logs
```bash
# Application log
tail -f csv_to_ofx_converter.log

# Follow tests output
python3 -m unittest discover tests -v 2>&1 | tee test_output.log
```

---

## 💡 Tips & Tricks

### 1. Faster Testing
Run specific tests instead of full suite during development:
```bash
python3 -m unittest tests.test_csv_parser.TestCSVParser -v
```

### 2. Keep GUI Running
Start GUI services in background and keep terminal free:
```bash
nohup start-gui.sh &
```

### 3. Code Formatting on Save
Already configured in `.devcontainer/devcontainer.json`:
```json
"editor.formatOnSave": true
```

### 4. Multiple Terminals
Use VS Code's split terminal feature:
- Terminal 1: Run GUI services
- Terminal 2: Run tests
- Terminal 3: Run application

### 5. Quick File Search
Use VS Code's file search (Ctrl+P) to quickly find files:
- Type `csv_parser` to find CSV parser
- Type `test_csv` to find CSV tests

---

## 🎓 Learning Resources

### Project Documentation
- [README.md](../README.md) - User guide (English)
- [README.pt-BR.md](../README.pt-BR.md) - User guide (Portuguese)
- [CLAUDE.md](../CLAUDE.md) - Developer guide
- [RELEASE_CHECKLIST.md](../RELEASE_CHECKLIST.md) - Release process

### External Resources
- [Python Tkinter Tutorial](https://docs.python.org/3/library/tkinter.html)
- [OFX Specification](https://www.ofx.net/)
- [PyInstaller Documentation](https://pyinstaller.readthedocs.io/)
- [GitHub Codespaces Docs](https://docs.github.com/codespaces)

---

## ⚡ Performance Notes

### Codespaces Tiers
- **Free:** 60 hours/month (2-core machines)
- **Pro:** 180 hours/month
- Remember to **stop or delete** when not in use!

### Resource Usage
- **GUI services:** ~200MB RAM
- **Python application:** ~50-100MB RAM
- **VS Code:** ~200-300MB RAM

### Optimization
- Close GUI when not needed: saves ~200MB RAM
- Use headless tests: faster execution
- Stop Codespace when done: saves hours

---

## 🔐 Security Notes

- VNC password is `codespaces` (change in production)
- All ports are private by default
- No sensitive data should be committed
- Use environment variables for secrets

---

## 📞 Support

### Common Issues
1. **GUI doesn't load** → Run `start-gui.sh`
2. **Tests fail** → Check `$PYTHONPATH`
3. **Import errors** → Verify working directory
4. **Port not forwarded** → Check Ports tab

### Getting Help
- Check [CLAUDE.md](../CLAUDE.md) for architecture
- Run `.devcontainer/verify-setup.sh` for diagnostics
- Create issue on GitHub for bugs

---

**Ready to start? Run:** `start-gui.sh` **then** `python3 main.py`
