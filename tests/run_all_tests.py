#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run All Tests - CSV to OFX Converter
=====================================
Convenience script to run all tests in the test suite.

This file provides backwards compatibility with the original test_converter.py
by importing all test classes and providing the run_tests() function.

Individual test classes have been split into separate modules:
- test_csv_parser.py: Tests for CSV parsing (8 tests)
- test_ofx_generator.py: Tests for OFX generation (20 tests)
- test_date_validator.py: Tests for date validation (11 tests)
- test_integration.py: Integration tests for complete workflows (5 tests)

Usage:
- python3 tests/run_all_tests.py (runs using the run_tests() function)
- python3 -m unittest discover tests (discovers and runs all test files)

Note: This file is named run_all_tests.py (not test_*.py) to avoid
being discovered twice by unittest discovery.
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
