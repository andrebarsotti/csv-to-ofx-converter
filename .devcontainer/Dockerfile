# Use official Python image as base
FROM mcr.microsoft.com/devcontainers/python:3.11-bullseye

# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies for Tkinter and GUI support
RUN apt-get update && apt-get install -y \
    # Python Tkinter dependencies
    python3-tk \
    tk-dev \
    # X11 and display dependencies
    xvfb \
    x11vnc \
    fluxbox \
    # noVNC for web-based GUI access
    novnc \
    websockify \
    # Build tools for PyInstaller
    build-essential \
    binutils \
    upx-ucl \
    # Additional utilities
    git \
    curl \
    wget \
    vim \
    tree \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Setup noVNC
RUN ln -s /usr/share/novnc/vnc.html /usr/share/novnc/index.html

# Create a startup script for X11 and VNC
RUN mkdir -p /usr/local/bin
COPY start-gui.sh /usr/local/bin/start-gui.sh
RUN chmod +x /usr/local/bin/start-gui.sh

# Copy requirements file and install Python development dependencies
COPY requirements-dev.txt /tmp/requirements-dev.txt
RUN pip install --no-cache-dir -r /tmp/requirements-dev.txt && \
    rm /tmp/requirements-dev.txt

# Install Claude Code CLI
# Note: Claude Code will be installed during post-create for the vscode user
# This ensures proper permissions and user-specific configuration
RUN curl -fsSL https://claude.ai/install.sh -o /tmp/install-claude.sh && \
    chmod +x /tmp/install-claude.sh

# Set display for GUI applications
ENV DISPLAY=:1

# Switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=dialog

# Set working directory
WORKDIR /workspaces/csv-to-ofx-converter

# Expose noVNC port
EXPOSE 6080
