@echo off
REM Build script for CSV to OFX Converter (Windows)
REM This script builds a standalone executable using PyInstaller

echo ======================================
echo CSV to OFX Converter - Build Script
echo ======================================
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>NUL
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
)

REM Clean previous builds
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM Build the application
echo Building standalone executable...
pyinstaller csv_to_ofx_converter.spec

REM Check if build was successful
if exist "dist\csv-to-ofx-converter.exe" (
    echo.
    echo Build successful!
    echo.
    echo Executable location:
    dir dist\csv-to-ofx-converter.exe
    echo.
    echo To run the application:
    echo   dist\csv-to-ofx-converter.exe
) else (
    echo.
    echo Build failed. Check the output above for errors.
    exit /b 1
)

echo.
echo ======================================
echo Build complete!
echo ======================================
pause
