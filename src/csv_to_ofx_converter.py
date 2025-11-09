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

# Export all classes for backward compatibility
__all__ = ['CSVParser', 'OFXGenerator', 'DateValidator', 'ConverterGUI', 'NOT_MAPPED', 'NOT_SELECTED']

logger = logging.getLogger(__name__)


def main():
    """Main entry point for the application."""
    root = tk.Tk()
    ConverterGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
