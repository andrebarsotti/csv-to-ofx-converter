# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.3] - 2025-11-09

### Added
- Initial SonarCloud configuration file for code quality analysis
- SonarQube workflow for automated code quality checks
- Python setup and coverage testing to SonarQube workflow
- Code coverage analysis support
- Module-level organization with new package structure
- Constants module for shared application constants
- Comprehensive module docstrings and type hints

### Changed
- Refactored monolithic code into separate modules for better organization
  - `csv_parser.py`: CSV parsing functionality
  - `ofx_generator.py`: OFX file generation
  - `date_validator.py`: Date validation logic
  - `converter_gui.py`: GUI implementation
  - `constants.py`: Shared constants
- Updated GitHub Actions workflow for better build and release process
- Improved SonarQube configuration with correct paths and settings
- Updated executable names in GitHub releases to match actual output
- Enhanced success message formatting in conversion completion
- Better code organization and maintainability

### Fixed
- Addressed multiple SonarQube code quality issues
- Resolved import errors and Unicode character issues
- Fixed executable names in release workflow
- Excluded UI files from code coverage analysis
- Configured correct branch name for SonarQube analysis
- Improved error handling and logging

### Removed
- Outdated implementation summaries (IMPLEMENTATION_SUMMARY.md, IMPLEMENTATION_V2.0_SUMMARY.md)
- Claude settings from version control
- Redundant and commented-out code

### Security
- Fixed potential security vulnerabilities identified by SonarQube
- Improved code quality and security posture

## [2.0.2] - 2025-11-09

### Fixed
- Fixed executable names in GitHub releases

### Changed
- Updated formatting for executable download instructions in release notes

## [2.0.1] - Previous release

### Added
- Initial version 2.0 features
- Enhanced GUI with wizard-style interface
- Composite description support
- Date validation features

---

For older versions, please see the git history.
