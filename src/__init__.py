"""
CSV to OFX Converter Package
============================
A complete application to convert CSV files to OFX format with GUI support.

This package provides classes for parsing CSV files, generating OFX files,
validating dates, and a GUI interface for the conversion process.

Author: Generated for Brazilian banking compatibility
License: MIT
Version: 2.0.0
"""

from .csv_parser import CSVParser
from .ofx_generator import OFXGenerator
from .date_validator import DateValidator
from .converter_gui import ConverterGUI
from .constants import NOT_MAPPED, NOT_SELECTED

__all__ = [
    'CSVParser',
    'OFXGenerator',
    'DateValidator',
    'ConverterGUI',
    'NOT_MAPPED',
    'NOT_SELECTED',
]

__version__ = '2.0.0'
