#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSV to OFX Converter
====================
A complete application to convert CSV files to OFX format with GUI support.

This module provides a graphical interface for converting bank transaction CSV files
into OFX (Open Financial Exchange) format, supporting both standard and Brazilian CSV formats.

Features:
- Multi-step wizard interface
- CSV data preview
- Flexible column mapping
- Composite descriptions from multiple columns
- Value inversion option
- Transaction date validation with Keep/Adjust/Exclude options

Author: Generated for Brazilian banking compatibility
License: MIT
Version: 2.0.0
"""

import tkinter as tk
import logging
import ctypes
import platform

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('csv_to_ofx_converter.log'),
        logging.StreamHandler()
    ]
)

# Import classes from separate modules
from .csv_parser import CSVParser
from .ofx_generator import OFXGenerator
from .date_validator import DateValidator
from .converter_gui import ConverterGUI
from .constants import NOT_MAPPED, NOT_SELECTED
from . import gui_utils
from .gui_balance_manager import BalanceManager

# Export all classes for backward compatibility
__all__ = [
    'CSVParser',
    'OFXGenerator',
    'DateValidator',
    'ConverterGUI',
    'NOT_MAPPED',
    'NOT_SELECTED',
    'gui_utils',
    'BalanceManager'
]

logger = logging.getLogger(__name__)


def configure_dpi_awareness():
    """
    Configure DPI awareness for Windows high DPI displays.

    This prevents blurry text and incorrect window sizing on Windows systems
    with DPI scaling (125%, 150%, 200%, etc.) and ensures proper maximization
    on high-resolution monitors.

    Must be called before creating the Tk() window.

    Platform support:
    - Windows 8.1+: Per-monitor DPI aware (recommended)
    - Windows 7/8.0: System DPI aware (fallback)
    - Other platforms: No-op (not needed)
    """
    if platform.system() == 'Windows':
        try:
            # Windows 8.1+ (per-monitor DPI aware)
            # This allows the app to handle different DPI settings on multiple monitors
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
            logger.info("DPI awareness configured: Per-monitor DPI aware (Windows 8.1+)")
        except Exception as e:
            try:
                # Windows 7/8.0 (system DPI aware)
                # Fallback for older Windows versions
                ctypes.windll.user32.SetProcessDPIAware()
                logger.info("DPI awareness configured: System DPI aware (Windows 7/8.0)")
            except Exception as e2:
                # DPI awareness not available or already set
                logger.warning(f"Could not configure DPI awareness: {e}, {e2}")


def main():
    """Main entry point for the application."""
    # Configure DPI awareness before creating Tk window (Windows only)
    configure_dpi_awareness()

    root = tk.Tk()
    ConverterGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
