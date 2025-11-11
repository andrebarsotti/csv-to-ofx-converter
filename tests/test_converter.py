#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit Tests for CSV to OFX Converter
====================================
Comprehensive test suite for the CSV to OFX converter application.

This file maintains backwards compatibility by importing all test classes
and providing the original run_tests() function. Individual test classes
have been split into separate modules for better maintainability:

- test_csv_parser.py: Tests for CSV parsing
- test_ofx_generator.py: Tests for OFX generation
- test_date_validator.py: Tests for date validation
- test_integration.py: Integration tests for complete workflows

You can still run tests using:
- python3 -m unittest tests.test_converter (runs all tests via this file)
- python3 -m unittest discover tests (discovers all test files)
- python3 tests/test_converter.py (runs using the run_tests() function)
"""

import unittest
import sys
import os

# Add parent directory to path when running as script
if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import test classes - works both as module and as script
try:
    from tests.test_csv_parser import TestCSVParser
    from tests.test_ofx_generator import TestOFXGenerator
    from tests.test_date_validator import TestDateValidator
    from tests.test_integration import TestIntegration
except ImportError:
    from test_csv_parser import TestCSVParser
    from test_ofx_generator import TestOFXGenerator
    from test_date_validator import TestDateValidator
    from test_integration import TestIntegration


def run_tests():
    """Run all tests and display results."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestCSVParser))
    suite.addTests(loader.loadTestsFromTestCase(TestOFXGenerator))
    suite.addTests(loader.loadTestsFromTestCase(TestDateValidator))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    exit(run_tests())
