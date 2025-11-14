#!/bin/bash
# Start GUI services for Tkinter applications in Codespaces

echo "Starting GUI services..."

# Kill any existing processes
pkill -9 Xvfb 2>/dev/null
pkill -9 x11vnc 2>/dev/null
pkill -9 websockify 2>/dev/null
pkill -9 fluxbox 2>/dev/null

# Start Xvfb (virtual framebuffer)
echo "Starting Xvfb..."
Xvfb :1 -screen 0 1280x720x24 &
sleep 2

# Start window manager
echo "Starting Fluxbox window manager..."
DISPLAY=:1 fluxbox &
sleep 1

# Start VNC server
echo "Starting x11vnc..."
x11vnc -display :1 -forever -shared -rfbport 5901 -passwd codespaces &
sleep 2

# Start noVNC websocket proxy
echo "Starting noVNC..."
websockify --web=/usr/share/novnc/ 6080 localhost:5901 &
sleep 2

echo "GUI services started!"
echo "Access the GUI at: https://<codespace-name>-6080.app.github.dev/vnc.html"
echo "VNC Password: codespaces"
echo ""
echo "To run the application with GUI:"
echo "  python3 main.py"
