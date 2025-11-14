#!/bin/bash
# Verify Codespaces setup is working correctly

set -e

echo "========================================="
echo "Codespaces Setup Verification"
echo "========================================="
echo ""

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

success() {
    echo -e "${GREEN}✓${NC} $1"
}

error() {
    echo -e "${RED}✗${NC} $1"
}

warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Check Python version
echo "Checking Python installation..."
if python3 --version > /dev/null 2>&1; then
    VERSION=$(python3 --version)
    success "Python installed: $VERSION"
else
    error "Python not found"
    exit 1
fi

# Check Tkinter
echo ""
echo "Checking Tkinter..."
if python3 -c "import tkinter" 2>/dev/null; then
    TK_VERSION=$(python3 -c "import tkinter; print(tkinter.TkVersion)")
    success "Tkinter available: version $TK_VERSION"
else
    error "Tkinter not available"
    exit 1
fi

# Check PyInstaller
echo ""
echo "Checking PyInstaller..."
if pip show pyinstaller > /dev/null 2>&1; then
    PYINSTALLER_VERSION=$(pip show pyinstaller | grep Version | cut -d' ' -f2)
    success "PyInstaller installed: $PYINSTALLER_VERSION"
else
    warning "PyInstaller not installed (run: pip install pyinstaller)"
fi

# Check GUI services
echo ""
echo "Checking GUI services..."
if pgrep Xvfb > /dev/null; then
    success "Xvfb is running"
else
    warning "Xvfb not running (run: start-gui.sh)"
fi

if pgrep x11vnc > /dev/null; then
    success "x11vnc is running"
else
    warning "x11vnc not running (run: start-gui.sh)"
fi

if pgrep websockify > /dev/null; then
    success "noVNC is running"
else
    warning "noVNC not running (run: start-gui.sh)"
fi

# Check DISPLAY variable
echo ""
echo "Checking environment..."
if [ -n "$DISPLAY" ]; then
    success "DISPLAY set to: $DISPLAY"
else
    warning "DISPLAY not set"
fi

if [ -n "$PYTHONPATH" ]; then
    success "PYTHONPATH set to: $PYTHONPATH"
else
    warning "PYTHONPATH not set"
fi

# Check project structure
echo ""
echo "Checking project structure..."
if [ -f "main.py" ]; then
    success "main.py found"
else
    error "main.py not found"
fi

if [ -d "src" ]; then
    success "src/ directory found"
else
    error "src/ directory not found"
fi

if [ -d "tests" ]; then
    success "tests/ directory found"
else
    error "tests/ directory not found"
fi

# Count test files
TEST_COUNT=$(find tests -name "test_*.py" | wc -l)
if [ "$TEST_COUNT" -gt 0 ]; then
    success "Found $TEST_COUNT test modules"
else
    error "No test files found"
fi

# Run quick import test
echo ""
echo "Checking Python imports..."
if python3 -c "from src.csv_parser import CSVParser" 2>/dev/null; then
    success "CSVParser imports correctly"
else
    error "CSVParser import failed"
fi

if python3 -c "from src.ofx_generator import OFXGenerator" 2>/dev/null; then
    success "OFXGenerator imports correctly"
else
    error "OFXGenerator import failed"
fi

if python3 -c "from src.converter_gui import ConverterGUI" 2>/dev/null; then
    success "ConverterGUI imports correctly"
else
    error "ConverterGUI import failed"
fi

# Run quick test
echo ""
echo "Running quick test..."
if python3 -m unittest tests.test_csv_parser.TestCSVParser.test_parse_standard_csv 2>/dev/null; then
    success "Sample test passed"
else
    error "Sample test failed"
fi

# Check development tools
echo ""
echo "Checking development tools..."
if command -v flake8 > /dev/null 2>&1; then
    success "flake8 available"
else
    warning "flake8 not installed"
fi

if command -v black > /dev/null 2>&1; then
    success "black available"
else
    warning "black not installed"
fi

# Summary
echo ""
echo "========================================="
echo "Verification Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "  1. Start GUI services: start-gui.sh"
echo "  2. Run full test suite: python3 -m unittest discover tests -v"
echo "  3. Launch application: python3 main.py"
echo ""
