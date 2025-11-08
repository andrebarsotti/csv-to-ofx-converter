#!/bin/bash
# Build script for CSV to OFX Converter
# This script builds a standalone executable using PyInstaller

set -e  # Exit on error

echo "======================================"
echo "CSV to OFX Converter - Build Script"
echo "======================================"
echo ""

# Check if PyInstaller is installed
if ! command -v pyinstaller &> /dev/null; then
    echo "❌ PyInstaller not found. Installing..."
    pip install pyinstaller
fi

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build dist *.spec.bak

# Build the application
echo "🔨 Building standalone executable..."
pyinstaller csv_to_ofx_converter.spec

# Check if build was successful
if [ -f "dist/csv-to-ofx-converter" ] || [ -f "dist/csv-to-ofx-converter.exe" ]; then
    echo ""
    echo "✅ Build successful!"
    echo ""
    echo "Executable location:"
    ls -lh dist/
    echo ""
    echo "To run the application:"
    if [ -f "dist/csv-to-ofx-converter" ]; then
        echo "  ./dist/csv-to-ofx-converter"
    else
        echo "  dist\\csv-to-ofx-converter.exe"
    fi
else
    echo ""
    echo "❌ Build failed. Check the output above for errors."
    exit 1
fi

echo ""
echo "======================================"
echo "Build complete!"
echo "======================================"
