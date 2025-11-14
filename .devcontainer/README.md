# GitHub Codespaces Configuration

This directory contains the development container configuration for GitHub Codespaces, enabling a fully configured Python development environment with GUI support for the CSV to OFX Converter application.

## What's Included

### Environment
- **Python 3.11** with full standard library
- **Tkinter** support for GUI applications
- **Virtual display** (Xvfb) for running GUI apps in the cloud
- **noVNC** for web-based GUI access

### Development Tools
- **PyInstaller** - For building standalone executables
- **Claude Code CLI** - AI-powered coding assistant
- **Flake8** - Code linting
- **Black** - Code formatting
- **Pylint** - Code analysis
- **MyPy** - Static type checking

### VS Code Extensions
- Python language support (Pylance)
- Black formatter
- Auto-docstring generator
- GitLens
- GitHub Copilot (if available)

## Quick Start

### 1. Open in Codespaces

Click the "Code" button on GitHub and select "Create codespace on main" (or your current branch).

The environment will automatically:
- Install all dependencies
- Configure Python environment
- Run the test suite
- Set up GUI services
- Display helpful information

### 2. Run the Application

#### Option A: Headless Testing (No GUI)
```bash
# Run tests without GUI
python3 -m unittest discover tests -v
```

#### Option B: With GUI (Recommended)

1. **Start GUI services:**
   ```bash
   start-gui.sh
   ```

2. **Access the web-based GUI:**
   - Click on the "Ports" tab in VS Code (bottom panel)
   - Find port 6080 (noVNC)
   - Click the globe icon to open in browser
   - Or use the forwarded URL: `https://<codespace-name>-6080.app.github.dev/vnc.html`

3. **Login to noVNC:**
   - Password: `codespaces`

4. **Run the application:**
   ```bash
   python3 main.py
   ```

5. **The Tkinter GUI will appear in the noVNC browser window**

### 3. Development Workflow

```bash
# Run all tests
python3 -m unittest discover tests -v

# Run specific test module
python3 -m unittest tests.test_csv_parser

# Format code with Black
black src/ tests/

# Check code with Flake8
flake8 src/ tests/

# Build executable (Linux)
./build.sh
```

### 4. Using Claude Code CLI

Claude Code is an AI-powered coding assistant that's pre-installed in this environment.

```bash
# Start Claude Code
claude

# Check version
claude --version

# Update Claude Code
claude update

# Run diagnostics
claude doctor
```

#### First-Time Setup

On first run, Claude Code will prompt for authentication. You have three options:

1. **Claude Console** (Default) - Requires billing at console.anthropic.com
2. **Claude App Subscription** - Use existing Pro/Max plan from claude.ai
3. **Enterprise** - Amazon Bedrock or Google Vertex AI

Follow the prompts to complete authentication.

#### Using Claude Code

Once authenticated, you can:
- Ask questions about the codebase
- Request code changes and refactoring
- Generate tests and documentation
- Debug issues
- Get explanations of complex code

Example commands:
```bash
# Start interactive session
claude

# Then type your requests, for example:
# "Explain how the CSV parser works"
# "Add error handling to the date validator"
# "Generate tests for the transaction utils"
```

## Files in This Directory

- **devcontainer.json** - Main configuration file
  - Defines container settings
  - VS Code extensions and settings
  - Port forwarding (6080 for noVNC)
  - Post-create command
  - Environment variables

- **Dockerfile** - Container image definition
  - Based on official Python 3.11 image
  - Installs Tkinter and GUI dependencies
  - Installs X11, VNC, and noVNC
  - Installs development tools (PyInstaller, linters)

- **start-gui.sh** - GUI services startup script
  - Starts Xvfb (virtual display)
  - Starts Fluxbox (window manager)
  - Starts x11vnc (VNC server)
  - Starts noVNC (web-based VNC client)

- **post-create.sh** - Automatic setup script
  - Runs after container creation
  - Installs/upgrades dependencies from requirements-dev.txt
  - Configures environment
  - Runs test suite
  - Displays helpful information

- **verify-setup.sh** - Environment verification script
  - Checks Python and Tkinter installation
  - Verifies GUI services
  - Tests project structure and imports

- **DEPENDENCIES.md** - Dependency management guide
  - How to add/update dependencies
  - Requirements file format
  - Best practices

- **.env.example** - Environment variables template
  - Display settings
  - Python configuration
  - VNC settings

## GUI Architecture

The GUI support works through the following chain:

```
Tkinter App → DISPLAY :1 → Xvfb (Virtual Display) → x11vnc (VNC Server)
→ websockify (WebSocket Proxy) → noVNC (Web Client) → Your Browser
```

This allows you to run and interact with the Tkinter GUI application directly in your web browser while the code runs in the cloud.

## Customization

### Change Python Version
Edit `Dockerfile`:
```dockerfile
FROM mcr.microsoft.com/devcontainers/python:3.10-bullseye
```

### Add VS Code Extensions
Edit `devcontainer.json`:
```json
"extensions": [
  "ms-python.python",
  "your-extension-id"
]
```

### Add System Packages
Edit `Dockerfile`:
```dockerfile
RUN apt-get update && apt-get install -y \
    your-package-name \
    && apt-get clean
```

### Add Python Packages

For development tools, edit [requirements-dev.txt](../requirements-dev.txt):
```bash
# Add to requirements-dev.txt
echo "package-name>=1.0.0" >> requirements-dev.txt

# Rebuild container or install manually
pip install -r requirements-dev.txt
```

For runtime dependencies (discouraged), edit [requirements.txt](../requirements.txt):
```bash
# Add to requirements.txt
echo "package-name>=1.0.0" >> requirements.txt

# Install
pip install -r requirements.txt
```

See [DEPENDENCIES.md](DEPENDENCIES.md) for detailed dependency management guide.

## Troubleshooting

### GUI doesn't appear
1. Ensure GUI services are running: `start-gui.sh`
2. Check port 6080 is forwarded in VS Code
3. Verify VNC password: `codespaces`
4. Check logs: `ps aux | grep vnc`

### Tests fail on container creation
This is usually temporary during initial setup. Try:
```bash
python3 -m unittest discover tests -v
```

### Build fails
Ensure PyInstaller is installed:
```bash
pip install pyinstaller
./build.sh
```

### Display errors
Set the DISPLAY variable:
```bash
export DISPLAY=:1
python3 main.py
```

## Performance Tips

1. **Close GUI when not needed** - GUI services consume resources
2. **Use headless tests** - Faster for unit testing
3. **Stop Codespace when done** - Saves compute hours

## Port Reference

- **6080** - noVNC web interface (HTTP)
- **5901** - VNC server (internal, not exposed)

## Environment Variables

The following are automatically set:

- `DISPLAY=:1` - X11 display for GUI apps
- `PYTHONPATH=/workspaces/csv-to-ofx-converter/src` - Python module path
- `PYTHONUNBUFFERED=1` - Real-time Python output

## Additional Resources

- [GitHub Codespaces Documentation](https://docs.github.com/en/codespaces)
- [Dev Container Specification](https://containers.dev/)
- [Project README](../README.md)
- [Developer Guide (CLAUDE.md)](../CLAUDE.md)
- [Release Checklist](../RELEASE_CHECKLIST.md)

## Notes

- The container runs as user `vscode` (not root)
- All changes are saved in the Codespace until deleted
- Free tier: 60 hours/month for 2-core machines
- Remember to stop or delete Codespaces when not in use

## Support

For issues with:
- **Codespaces setup**: Check GitHub Codespaces documentation
- **Application bugs**: Create issue on GitHub repository
- **Development questions**: See CLAUDE.md for project architecture

---

**Happy coding in the cloud!**
