#!/bin/bash
# Post-create script for GitHub Codespaces
# This script runs after the container is created

set -e

echo "========================================="
echo "CSV to OFX Converter - Post-Create Setup"
echo "========================================="
echo ""

# Create log directory
echo "Creating log directory..."
mkdir -p logs

# Set Python path
echo "Configuring Python environment..."
export PYTHONPATH="/workspaces/csv-to-ofx-converter/src:$PYTHONPATH"

# Verify Python installation
echo ""
echo "Python version:"
python3 --version

# Verify Tkinter installation
echo ""
echo "Verifying Tkinter installation..."
python3 -c "import tkinter; print('Tkinter version:', tkinter.TkVersion)" || {
    echo "WARNING: Tkinter verification failed!"
}

# Install/upgrade development dependencies from requirements-dev.txt
echo ""
echo "Installing development dependencies..."
if [ -f "requirements-dev.txt" ]; then
    echo "Installing from requirements-dev.txt..."
    pip install -q --upgrade -r requirements-dev.txt
    echo "Development dependencies installed successfully!"
else
    echo "WARNING: requirements-dev.txt not found, installing PyInstaller manually..."
    pip show pyinstaller > /dev/null 2>&1 || {
        echo "Installing PyInstaller..."
        pip install pyinstaller
    }
fi

# Verify key packages
echo ""
echo "Verifying installed packages..."
pip show pyinstaller >/dev/null 2>&1 && echo "✓ PyInstaller installed" || echo "✗ PyInstaller missing"
pip show black >/dev/null 2>&1 && echo "✓ Black installed" || echo "✗ Black missing"
pip show flake8 >/dev/null 2>&1 && echo "✓ Flake8 installed" || echo "✗ Flake8 missing"

# Install Claude Code CLI
echo ""
echo "Installing Claude Code CLI..."
if [ -f "/tmp/install-claude.sh" ]; then
    bash /tmp/install-claude.sh 2>&1 | grep -v "^$" || true
    rm /tmp/install-claude.sh 2>/dev/null || true
    echo "Claude Code CLI installation completed!"
else
    echo "Installing Claude Code CLI from web..."
    curl -fsSL https://claude.ai/install.sh | bash || {
        echo "WARNING: Claude Code installation failed. You can install it manually later."
    }
fi

# Verify Claude Code installation
echo ""
echo "Verifying Claude Code installation..."
if command -v claude >/dev/null 2>&1; then
    echo "✓ Claude Code installed successfully"
    claude --version 2>/dev/null || echo "  Version info unavailable"
else
    echo "✗ Claude Code not found in PATH"
    echo "  You may need to restart your terminal or run: source ~/.bashrc"
fi

# Run tests to verify everything works
echo ""
echo "Running test suite..."
python3 -m unittest discover tests -v || {
    echo "WARNING: Some tests failed. Please review."
}

# Create sample data directory if it doesn't exist
echo ""
echo "Creating sample data directory..."
mkdir -p sample_data

# Make build scripts executable
echo ""
echo "Setting executable permissions on build scripts..."
chmod +x build.sh 2>/dev/null || true

# Display helpful information
echo ""
echo "========================================="
echo "Setup Complete!"
echo "========================================="
echo ""
echo "Quick Start Commands:"
echo "  Run application:     python3 main.py"
echo "  Run tests:           python3 -m unittest discover tests -v"
echo "  Build executable:    ./build.sh"
echo "  Start GUI services:  start-gui.sh"
echo "  Use Claude Code:     claude"
echo ""
echo "Claude Code Commands:"
echo "  Start Claude:        claude"
echo "  Check installation:  claude --version"
echo "  Update Claude:       claude update"
echo "  Diagnostics:         claude doctor"
echo "  Note: First run will prompt for authentication"
echo ""
echo "To use the GUI in Codespaces:"
echo "  1. Run: start-gui.sh"
echo "  2. Click on the 'Ports' tab in VS Code"
echo "  3. Open the forwarded port 6080 in your browser"
echo "  4. Enter VNC password: codespaces"
echo "  5. Run: python3 main.py"
echo ""
echo "Project Information:"
echo "  - 95 tests available in tests/ directory"
echo "  - Pure Python 3.7+ with no runtime dependencies"
echo "  - GUI application using Tkinter"
echo "  - Multi-step wizard interface (7 steps)"
echo ""
echo "Documentation:"
echo "  - README.md (English)"
echo "  - README.pt-BR.md (Portuguese)"
echo "  - CLAUDE.md (Developer guide)"
echo ""
echo "Happy coding!"
echo "========================================="
