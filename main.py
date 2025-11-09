#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main entry point for CSV to OFX Converter application.

Run this script to launch the GUI application.
"""

import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path.parent))

# Import and run the main function
from src.csv_to_ofx_converter import main

if __name__ == '__main__':
    main()
