"""
gui_steps - Wizard step implementations package

This package contains the individual wizard step classes for the CSV to OFX Converter.
Each step is a self-contained module implementing the WizardStep interface.

The wizard follows a 7-step process:
1. File Selection - Choose CSV file to convert
2. CSV Format - Configure delimiter and decimal separator
3. Data Preview - Preview loaded CSV data
4. OFX Configuration - Configure account ID, bank name, and currency
5. Field Mapping - Map CSV columns to OFX fields
6. Advanced Options - Configure value inversion and date validation
7. Balance Preview - Review balance summary and transaction preview

Each step class:
- Inherits from WizardStep base class
- Implements _build_ui(), _collect_data(), and _validate_data()
- Returns data via StepData dataclass
- Is independently testable with mock parent

Future imports will be added here as step classes are implemented.
"""

# Step classes - all 7 steps implemented (Phase D complete)
from .file_selection_step import FileSelectionStep
from .csv_format_step import CSVFormatStep
from .data_preview_step import DataPreviewStep
from .ofx_config_step import OFXConfigStep
from .field_mapping_step import FieldMappingStep
from .advanced_options_step import AdvancedOptionsStep
from .balance_preview_step import BalancePreviewStep

__all__ = [
    'FileSelectionStep',
    'CSVFormatStep',
    'DataPreviewStep',
    'OFXConfigStep',
    'FieldMappingStep',
    'AdvancedOptionsStep',
    'BalancePreviewStep',
]
