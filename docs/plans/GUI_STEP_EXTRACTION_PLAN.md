# GUI Step Extraction Plan

## Executive Summary

This document outlines the architecture and implementation plan for extracting the 7 wizard steps from `converter_gui.py` into separate, reusable step classes. This refactoring will reduce the main GUI file from 1,400 lines to approximately 600-700 lines while establishing a clear, modular wizard step framework.

**Current State:**
- File: `src/converter_gui.py` (1,400 lines)
- 7 wizard steps embedded in monolithic class
- Step methods range from 50-200 lines each
- All step logic tightly coupled to ConverterGUI

**Target State:**
- Orchestrator: `src/converter_gui.py` (~600-700 lines)
- Base class: `src/gui_wizard_step.py` (~150 lines)
- Step classes: 7 files in `src/gui_steps/` package (~100-250 lines each)
- Total reduction: ~700 lines (50% reduction)

**Priority:** P1 (High) - Critical for maintainability and future wizard enhancements

**Timeline:** 2-3 weeks (10-15 working days)

**Status:** 🟢 Phase A Complete (November 23, 2025)

---

## Implementation Progress

### ✅ Phase A: Infrastructure (COMPLETED - November 23, 2025)

**Commit:** `c4fc0d2` - "feat(phase-a): Add WizardStep base class infrastructure"

**Deliverables:**
- ✅ `src/gui_wizard_step.py` (355 lines) - WizardStep base class
- ✅ `src/gui_steps/__init__.py` (33 lines) - Package structure
- ✅ `tests/test_gui_wizard_step.py` (585 lines, 32 tests) - Comprehensive tests
- ✅ Updated `src/csv_to_ofx_converter.py` - Module exports
- ✅ Updated `CLAUDE.md` - Documentation

**Metrics:**
- Tests: 262/262 passing (230 existing + 32 new)
- Code Quality Grade: A (APPROVED)
- PEP8 Compliance: 98%
- Docstring Coverage: 100%
- Test Coverage: 95%+

**Tasks Completed (8/8):**
1. ✅ Create base class infrastructure
2. ✅ Create package structure
3. ✅ Create base class unit tests
4. ✅ Test package structure
5. ✅ Update main module exports
6. ✅ Code quality review
7. ✅ Integration testing
8. ✅ Update documentation

### 🟡 Phase B: Simple Steps (Steps 1, 2, 4) - IN PROGRESS (4/9 tasks - 44%)

**Target:** Extract FileSelectionStep, CSVFormatStep, OFXConfigStep

**Progress (November 23, 2025):**
- ✅ Task B.1: FileSelectionStep implementation (194 lines)
- ✅ Task B.2: FileSelectionStep tests (24 tests, 444 lines)
- ✅ Task B.3: CSVFormatStep implementation (220 lines)
- ✅ Task B.4: CSVFormatStep tests (21 tests, 402 lines)
- ⏳ Task B.5-B.9: Remaining tasks (Step 4, orchestrator update, integration)

**Commits:**
- `e5c6560` - "feat(phase-b): Add FileSelectionStep wizard step (Tasks B.1-B.2)"
- `047c76d` - "feat(phase-b): Add CSVFormatStep wizard step (Tasks B.3-B.4)"

**Metrics:**
- Total Tests: 307 (262 Phase A + 24 FileSelectionStep + 21 CSVFormatStep)
- All tests passing
- Zero regressions
- SonarCloud: ✅ Passing (215 tests in CI)

### ⏳ Phase C: Medium Steps (Steps 3, 6) - NOT STARTED

**Target:** Extract DataPreviewStep, AdvancedOptionsStep

### ⏳ Phase D: Complex Steps (Steps 5, 7) - NOT STARTED

**Target:** Extract FieldMappingStep, BalancePreviewStep

### ⏳ Phase E: Cleanup & Release - NOT STARTED

**Target:** Final optimization, documentation, v3.1.0 release

---

## Table of Contents

1. [Problem Statement](#problem-statement)
2. [Architecture Overview](#architecture-overview)
3. [Base Class Design](#base-class-design)
4. [Step Class Specifications](#step-class-specifications)
5. [Orchestrator Design](#orchestrator-design)
6. [Data Flow & Communication](#data-flow--communication)
7. [Validation Strategy](#validation-strategy)
8. [Migration Strategy](#migration-strategy)
9. [Testing Strategy](#testing-strategy)
10. [Success Metrics](#success-metrics)
11. [Risk Management](#risk-management)
12. [Implementation Phases](#implementation-phases)

---

## Problem Statement

### Current Issues

**Monolithic Step Methods:**
- Each step method (`_create_step_*`) contains UI creation, validation, and business logic
- Steps range from 50-200 lines of tightly coupled code
- Difficult to test individual steps independently
- No reusability across different wizard contexts
- Changes to one step can accidentally affect others

**Tight Coupling:**
- Steps directly access `self` (ConverterGUI instance) for all data
- No clear interface between steps and orchestrator
- Steps manipulate parent's state directly (e.g., `self.csv_data`)
- Validation logic mixed with UI creation

**Scalability Limitations:**
- Adding a new wizard step requires modifying ConverterGUI
- Cannot reuse wizard steps in other applications
- Difficult to change step order or make steps conditional
- No way to skip/enable/disable steps dynamically

### User Impact

**For Developers:**
- 30+ minutes to understand a single step's logic
- High risk of introducing bugs when modifying steps
- Difficult to add new wizard features (e.g., step branching)

**For Users:**
- Potential bugs due to complex, hard-to-maintain code
- Slower feature development and bug fixes
- Cannot customize wizard flow easily

### Business Value of Solution

**Improved Maintainability:**
- Each step is self-contained and independently testable
- Clear boundaries reduce cognitive load
- New contributors can understand steps in <10 minutes

**Enhanced Extensibility:**
- Easy to add new steps (just create new step class)
- Steps can be reused in other wizard contexts
- Support for conditional steps and dynamic flows

**Better Quality:**
- Unit tests for each step class
- Validation logic separated from UI
- Easier bug isolation and fixing

---

## Architecture Overview

### Module Structure

```
src/
  converter_gui.py              # 🔄 REFACTOR: Orchestrator (600-700 lines)
  gui_wizard_step.py            # ✅ NEW: Base step class (~150 lines)
  gui_steps/                    # ✅ NEW: Step package
    __init__.py                 # Step exports
    file_selection_step.py      # Step 1 (~100 lines)
    csv_format_step.py          # Step 2 (~120 lines)
    data_preview_step.py        # Step 3 (~180 lines)
    ofx_config_step.py          # Step 4 (~140 lines)
    field_mapping_step.py       # Step 5 (~250 lines)
    advanced_options_step.py    # Step 6 (~150 lines)
    balance_preview_step.py     # Step 7 (~200 lines)

tests/
  test_gui_wizard_step.py       # ✅ NEW: Base class tests (~80 lines)
  test_gui_steps/               # ✅ NEW: Step tests package
    __init__.py
    test_file_selection_step.py    # (~100 lines)
    test_csv_format_step.py        # (~120 lines)
    test_data_preview_step.py      # (~150 lines)
    test_ofx_config_step.py        # (~100 lines)
    test_field_mapping_step.py     # (~180 lines)
    test_advanced_options_step.py  # (~120 lines)
    test_balance_preview_step.py   # (~150 lines)
```

**Total New Code:**
- Production: ~1,290 lines (base + 7 steps)
- Tests: ~1,000 lines (base tests + 7 step tests)
- Net Reduction in converter_gui.py: ~700 lines (50%)

### Class Hierarchy

```
WizardStep (abstract base class)
│
├── FileSelectionStep
├── CSVFormatStep
├── DataPreviewStep
├── OFXConfigStep
├── FieldMappingStep
├── AdvancedOptionsStep
└── BalancePreviewStep
```

### Design Principles

1. **Dependency Injection:** Steps receive parent via constructor
2. **Data Return:** Steps return data structures, don't manipulate parent directly
3. **Validation Separation:** Validation logic separated from UI creation
4. **Minimal Coupling:** Steps only access parent through defined interface
5. **Independent Testing:** Each step testable with mock parent

---

## Base Class Design

### WizardStep Abstract Base Class

```python
"""
gui_wizard_step.py - Base class for wizard steps
"""

import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass


@dataclass
class StepConfig:
    """
    Configuration for a wizard step.
    
    Attributes:
        step_number: Position in wizard (0-based)
        step_name: Display name (e.g., "File Selection")
        step_title: Full title for step frame
        is_required: Whether step can be skipped
        can_go_back: Whether back button is enabled
        show_next: Whether to show next button
        show_convert: Whether to show convert button
    """
    step_number: int
    step_name: str
    step_title: str
    is_required: bool = True
    can_go_back: bool = True
    show_next: bool = True
    show_convert: bool = False


@dataclass
class StepData:
    """
    Data returned by a step after user interaction.
    
    Attributes:
        is_valid: Whether step data is valid for progression
        error_message: Error message if not valid
        data: Dictionary with step-specific data
    """
    is_valid: bool
    error_message: Optional[str] = None
    data: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.data is None:
            self.data = {}


class WizardStep(ABC):
    """
    Abstract base class for wizard steps.
    
    Provides common functionality:
    - Step lifecycle (create, show, hide, validate)
    - Parent orchestrator access through defined interface
    - Container management
    - Configuration management
    
    Each concrete step must implement:
    - _build_ui(): Create step's UI elements
    - _collect_data(): Gather data from UI elements
    - _validate_data(): Validate collected data
    """
    
    def __init__(self, parent, config: StepConfig):
        """
        Initialize wizard step.
        
        Args:
            parent: Parent wizard orchestrator (ConverterGUI)
            config: Step configuration
        """
        self.parent = parent
        self.config = config
        self.container: Optional[ttk.Frame] = None
        self._widgets: Dict[str, tk.Widget] = {}
        
    # === Lifecycle Methods ===
    
    def create(self, parent_container: ttk.Frame) -> ttk.Frame:
        """
        Create step UI in parent container.
        
        Args:
            parent_container: Parent container widget
            
        Returns:
            Step's main frame
        """
        # Create step frame
        self.container = ttk.LabelFrame(
            parent_container,
            text=self.config.step_title,
            padding="20"
        )
        self.container.grid(
            row=0, column=0,
            sticky=(tk.W, tk.E, tk.N, tk.S),
            padx=20, pady=20
        )
        
        # Build step-specific UI
        self._build_ui()
        
        # Configure grid weights for responsiveness
        self._configure_layout()
        
        return self.container
    
    @abstractmethod
    def _build_ui(self):
        """
        Build step-specific UI elements.
        
        Subclasses must implement this to create their widgets.
        Store widget references in self._widgets for later access.
        """
        pass
    
    def _configure_layout(self):
        """
        Configure grid layout for responsiveness.
        
        Can be overridden by subclasses for custom layouts.
        """
        if self.container:
            self.container.columnconfigure(0, weight=1)
    
    def show(self):
        """
        Show this step (called when step becomes active).
        
        Can be overridden to perform actions on step activation.
        """
        if self.container:
            self.container.grid()
    
    def hide(self):
        """
        Hide this step (called when leaving step).
        
        Can be overridden to perform cleanup actions.
        """
        if self.container:
            self.container.grid_remove()
    
    def destroy(self):
        """Destroy step and cleanup resources."""
        if self.container:
            self.container.destroy()
            self.container = None
        self._widgets.clear()
    
    # === Data Collection & Validation ===
    
    def validate(self) -> StepData:
        """
        Validate step data before progression.
        
        Returns:
            StepData with validation result and collected data
        """
        # Collect data from UI
        data = self._collect_data()
        
        # Validate collected data
        is_valid, error_msg = self._validate_data(data)
        
        return StepData(
            is_valid=is_valid,
            error_message=error_msg,
            data=data if is_valid else {}
        )
    
    @abstractmethod
    def _collect_data(self) -> Dict[str, Any]:
        """
        Collect data from step's UI elements.
        
        Returns:
            Dictionary with step data
        """
        pass
    
    @abstractmethod
    def _validate_data(self, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Validate collected step data.
        
        Args:
            data: Data collected from UI
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        pass
    
    # === Helper Methods ===
    
    def log(self, message: str):
        """
        Log message to parent's activity log.
        
        Args:
            message: Message to log
        """
        if hasattr(self.parent, '_log'):
            self.parent._log(message)
    
    def get_parent_data(self, key: str, default=None):
        """
        Safely get data from parent orchestrator.
        
        Args:
            key: Data key
            default: Default value if key not found
            
        Returns:
            Value from parent or default
        """
        # Access through parent's public interface only
        if hasattr(self.parent, key):
            attr = getattr(self.parent, key)
            # If it's a tk.StringVar or similar, get its value
            if hasattr(attr, 'get'):
                return attr.get()
            return attr
        return default
    
    def set_parent_data(self, key: str, value: Any):
        """
        Safely set data in parent orchestrator.
        
        Args:
            key: Data key
            value: Value to set
        """
        if hasattr(self.parent, key):
            attr = getattr(self.parent, key)
            # If it's a tk.StringVar or similar, use set()
            if hasattr(attr, 'set'):
                attr.set(value)
            else:
                setattr(self.parent, key, value)
```

**Key Features:**

1. **StepConfig Dataclass:**
   - Encapsulates step configuration
   - Eliminates hard-coded step properties
   - Easy to modify step behavior

2. **StepData Dataclass:**
   - Standardized return format for validation
   - Contains validity flag, error message, and data
   - Clear contract between step and orchestrator

3. **Lifecycle Methods:**
   - `create()`: Initialize step UI
   - `show()`/`hide()`: Step visibility management
   - `validate()`: Pre-navigation validation
   - `destroy()`: Cleanup resources

4. **Abstract Methods:**
   - Forces subclasses to implement UI building
   - Forces subclasses to implement data collection
   - Forces subclasses to implement validation

5. **Safe Parent Access:**
   - `get_parent_data()`: Read from parent safely
   - `set_parent_data()`: Write to parent safely
   - `log()`: Logging helper
   - Minimizes direct parent coupling

---

## Step Class Specifications

### Step 1: File Selection Step

**File:** `src/gui_steps/file_selection_step.py`

**Responsibilities:**
- Display file browser button
- Show selected file path
- Validate file selection

**Data Collected:**
```python
{
    'csv_file': str  # Path to selected CSV file
}
```

**Validation Rules:**
- File path must not be empty
- File must exist
- File must be a valid file (not directory)

**UI Elements:**
- Label: "Select a CSV file to convert to OFX format"
- Entry: Read-only entry showing file path (bound to parent.csv_file)
- Button: "Browse..." (triggers file dialog)
- Label: Info text about supported formats

**Estimated Size:** ~100 lines

**Dependencies:**
- `gui_utils.validate_csv_file_selection()`
- `filedialog.askopenfilename()`

**Example Implementation:**

```python
class FileSelectionStep(WizardStep):
    """Step 1: Select CSV file for conversion."""
    
    def __init__(self, parent):
        config = StepConfig(
            step_number=0,
            step_name="File Selection",
            step_title="Step 1: Select CSV File"
        )
        super().__init__(parent, config)
    
    def _build_ui(self):
        """Build file selection UI."""
        # Description
        ttk.Label(
            self.container,
            text="Select a CSV file to convert to OFX format:",
            font=('Arial', 10)
        ).grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 20))
        
        # File path label
        ttk.Label(
            self.container,
            text="CSV File:",
            font=('Arial', 10, 'bold')
        ).grid(row=1, column=0, sticky=tk.W, padx=5, pady=10)
        
        # File path entry (bound to parent's csv_file variable)
        self._widgets['file_entry'] = ttk.Entry(
            self.container,
            textvariable=self.parent.csv_file,
            state='readonly',
            width=50
        )
        self._widgets['file_entry'].grid(
            row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=10
        )
        
        # Browse button
        self._widgets['browse_button'] = ttk.Button(
            self.container,
            text="Browse...",
            command=self._browse_file
        )
        self._widgets['browse_button'].grid(row=1, column=2, padx=5, pady=10)
        
        # Info text
        info_text = (
            "Select a CSV file containing your bank transactions.\n"
            "The file should have a header row with column names.\n"
            "Supported formats: CSV with comma, semicolon, or tab delimiters."
        )
        ttk.Label(
            self.container,
            text=info_text,
            font=('Arial', 9),
            foreground='gray',
            wraplength=600,
            justify=tk.LEFT
        ).grid(row=2, column=0, columnspan=3, sticky=tk.W, pady=20)
    
    def _browse_file(self):
        """Open file dialog to select CSV file."""
        from tkinter import filedialog
        
        filename = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            self.parent.csv_file.set(filename)
            self.log(f"Selected file: {filename}")
    
    def _configure_layout(self):
        """Configure responsive layout."""
        self.container.columnconfigure(1, weight=1)
    
    def _collect_data(self) -> Dict[str, Any]:
        """Collect file selection data."""
        return {
            'csv_file': self.parent.csv_file.get()
        }
    
    def _validate_data(self, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Validate file selection."""
        from src import gui_utils
        
        csv_file = data.get('csv_file', '')
        is_valid, error_msg = gui_utils.validate_csv_file_selection(csv_file)
        
        return is_valid, error_msg
```

---

### Step 2: CSV Format Step

**File:** `src/gui_steps/csv_format_step.py`

**Responsibilities:**
- Configure CSV delimiter (comma, semicolon, tab)
- Configure decimal separator (dot, comma)
- Provide format presets (Standard, Brazilian)

**Data Collected:**
```python
{
    'delimiter': str,        # ',', ';', or '\t'
    'decimal_separator': str # '.' or ','
}
```

**Validation Rules:**
- Always valid (has defaults)

**UI Elements:**
- Radio buttons: Delimiter options (comma, semicolon, tab)
- Radio buttons: Decimal separator options (dot, comma)
- Info text: Explanation of format combinations

**Estimated Size:** ~120 lines

**Dependencies:**
- None (pure UI)

---

### Step 3: Data Preview Step

**File:** `src/gui_steps/data_preview_step.py`

**Responsibilities:**
- Load CSV data using selected format
- Display first 100 rows in Treeview
- Show statistics (row count, column count)
- Provide reload button

**Data Collected:**
```python
{
    'csv_headers': List[str],
    'csv_data': List[Dict[str, str]],
    'reload_requested': bool
}
```

**Validation Rules:**
- CSV data must be loaded successfully
- At least 1 row of data required

**UI Elements:**
- Button: "Reload Data"
- Treeview: Data preview with scrollbars
- Label: Statistics (e.g., "Showing 100 of 500 rows")

**Estimated Size:** ~180 lines

**Dependencies:**
- `CSVParser`
- `gui_utils.format_preview_stats()`

**Special Considerations:**
- Must handle CSV parsing errors gracefully
- Performance: Limit preview to 100 rows
- Auto-loads data on first show

---

### Step 4: OFX Configuration Step

**File:** `src/gui_steps/ofx_config_step.py`

**Responsibilities:**
- Configure account ID
- Configure bank name
- Select currency

**Data Collected:**
```python
{
    'account_id': str,
    'bank_name': str,
    'currency': str  # BRL, USD, EUR, GBP
}
```

**Validation Rules:**
- Always valid (has defaults)

**UI Elements:**
- Entry: Account ID (with default hint)
- Entry: Bank name (with default hint)
- Combobox: Currency selection (BRL, USD, EUR, GBP)
- Labels: Help text for each field

**Estimated Size:** ~140 lines

**Dependencies:**
- None (pure UI)

---

### Step 5: Field Mapping Step

**File:** `src/gui_steps/field_mapping_step.py`

**Responsibilities:**
- Map CSV columns to OFX fields (date, amount, description, type, id)
- Configure composite description (up to 4 columns)
- Select description separator

**Data Collected:**
```python
{
    'field_mappings': Dict[str, str],  # OFX field -> CSV column
    'description_columns': List[str],   # Composite description columns
    'description_separator': str        # ' ', ' - ', ', ', ' | '
}
```

**Validation Rules:**
- Date field must be mapped
- Amount field must be mapped
- Description OR composite description must be configured

**UI Elements:**
- Comboboxes: Field mappings (5 fields)
- Separator: Horizontal separator
- Comboboxes: Composite description columns (4 columns)
- Radio buttons: Description separator options
- Labels: Help text and notes

**Estimated Size:** ~250 lines

**Dependencies:**
- `gui_utils.validate_required_field_mappings()`
- `gui_utils.validate_description_mapping()`
- `constants.NOT_MAPPED`, `constants.NOT_SELECTED`

**Special Considerations:**
- Most complex step UI
- Requires CSV headers from previous step
- Dynamic column options based on loaded CSV

---

### Step 6: Advanced Options Step

**File:** `src/gui_steps/advanced_options_step.py`

**Responsibilities:**
- Configure value inversion (swap debits/credits)
- Enable/disable date validation
- Configure date range (start/end dates)

**Data Collected:**
```python
{
    'invert_values': bool,
    'enable_date_validation': bool,
    'start_date': str,  # DD/MM/YYYY
    'end_date': str     # DD/MM/YYYY
}
```

**Validation Rules:**
- If date validation enabled, start_date and end_date must be valid DD/MM/YYYY
- Start date must be before end date

**UI Elements:**
- Checkbox: Invert values
- Checkbox: Enable date validation
- Entry: Start date (with auto-formatting)
- Entry: End date (with auto-formatting)
- Labels: Help text for each option

**Estimated Size:** ~150 lines

**Dependencies:**
- `gui_utils.format_date_string()`
- `gui_utils.calculate_cursor_position_after_format()`
- `gui_utils.validate_date_range_inputs()`

**Special Considerations:**
- Date entry fields toggle enabled/disabled based on checkbox
- Auto-formatting of date input (DD/MM/YYYY)

---

### Step 7: Balance Preview Step

**File:** `src/gui_steps/balance_preview_step.py`

**Responsibilities:**
- Display balance summary (credits, debits, calculated final)
- Show transaction preview in Treeview
- Handle initial balance input
- Support transaction deletion (context menu)
- Handle date action decisions (keep/adjust/exclude)

**Data Collected:**
```python
{
    'initial_balance': float,
    'final_balance': float,
    'auto_calculate_final_balance': bool,
    'deleted_transactions': Set[int],
    'date_action_decisions': Dict[int, str]
}
```

**Validation Rules:**
- Initial balance must be a valid number
- Final balance must be a valid number (if manual mode)

**UI Elements:**
- Entry: Initial balance (with validation)
- Button: Recalculate
- Labels: Balance summary (credits, debits, calculated final)
- Checkbox: Auto-calculate final balance
- Entry: Manual final balance (enabled/disabled)
- Treeview: Transaction preview with context menu
- Labels: Transaction count, confirmation message

**Estimated Size:** ~200 lines

**Dependencies:**
- `BalanceManager.calculate_balance_preview()`
- `BalanceManager.validate_balance_input()`
- `TransactionManager.show_context_menu()`
- `gui_utils.validate_numeric_input()`

**Special Considerations:**
- Most data-heavy step
- Integrates with BalanceManager and TransactionManager
- Supports transaction deletion and restoration
- Handles date validation actions

---

## Orchestrator Design

### Simplified ConverterGUI

**Responsibilities:**
- Initialize all wizard steps
- Manage step navigation (forward/backward)
- Update progress indicator
- Coordinate between steps
- Handle conversion trigger

**Removed Responsibilities:**
- Creating step UI (delegated to step classes)
- Step-specific validation (delegated to step classes)
- Step-specific data collection (delegated to step classes)

**New Structure:**

```python
class ConverterGUI:
    """
    Simplified wizard orchestrator.
    
    Manages wizard flow and coordinates between steps.
    """
    
    def __init__(self, root: tk.Tk):
        """Initialize GUI orchestrator."""
        self.root = root
        # ... existing initialization ...
        
        # Initialize step classes
        self.steps = self._create_steps()
        self.current_step_idx = 0
        
        # Build UI
        self._create_widgets()
        
        # Show first step
        self._show_step(0)
    
    def _create_steps(self) -> List[WizardStep]:
        """
        Create all wizard step instances.
        
        Returns:
            List of WizardStep instances
        """
        from .gui_steps import (
            FileSelectionStep,
            CSVFormatStep,
            DataPreviewStep,
            OFXConfigStep,
            FieldMappingStep,
            AdvancedOptionsStep,
            BalancePreviewStep
        )
        
        return [
            FileSelectionStep(self),
            CSVFormatStep(self),
            DataPreviewStep(self),
            OFXConfigStep(self),
            FieldMappingStep(self),
            AdvancedOptionsStep(self),
            BalancePreviewStep(self)
        ]
    
    def _create_widgets(self):
        """Create orchestrator UI (non-step widgets)."""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="CSV to OFX Converter - Enhanced Edition",
            font=('Arial', 16, 'bold')
        )
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Progress indicator
        self._create_progress_indicator(main_frame, row=1)
        
        # Step container
        self.step_container = ttk.Frame(main_frame)
        self.step_container.grid(
            row=2, column=0,
            sticky=(tk.W, tk.E, tk.N, tk.S),
            pady=10
        )
        self.step_container.columnconfigure(0, weight=1)
        self.step_container.rowconfigure(0, weight=1)
        
        # Navigation buttons
        self._create_navigation_buttons(main_frame, row=3)
        
        # Log section
        self._create_log_section(main_frame, row=4)
    
    def _show_step(self, step_idx: int):
        """
        Show specified wizard step.
        
        Args:
            step_idx: Index of step to show (0-based)
        """
        # Hide current step if exists
        if hasattr(self, '_current_step_widget') and self._current_step_widget:
            self._current_step_widget.hide()
        
        # Update current step index
        self.current_step_idx = step_idx
        
        # Get step instance
        step = self.steps[step_idx]
        
        # Create step UI if not already created
        if not step.container:
            step.create(self.step_container)
        
        # Show step
        step.show()
        self._current_step_widget = step
        
        # Update progress indicator
        self._update_progress_indicator()
        
        # Update navigation buttons
        self._update_navigation_buttons()
    
    def _go_next(self):
        """Navigate to next step."""
        # Validate current step
        current_step = self.steps[self.current_step_idx]
        step_data = current_step.validate()
        
        if not step_data.is_valid:
            messagebox.showwarning("Validation Error", step_data.error_message)
            return
        
        # Process step data (optional)
        self._process_step_data(step_data)
        
        # Navigate to next step
        if self.current_step_idx < len(self.steps) - 1:
            self._show_step(self.current_step_idx + 1)
    
    def _go_back(self):
        """Navigate to previous step."""
        if self.current_step_idx > 0:
            self._show_step(self.current_step_idx - 1)
    
    def _process_step_data(self, step_data: StepData):
        """
        Process data collected from step.
        
        Args:
            step_data: Data returned by step validation
        """
        # Update parent state with step data if needed
        # Most data is already bound to parent variables
        pass
    
    # ... rest of orchestrator methods ...
```

**Key Changes:**

1. **Step Management:**
   - `_create_steps()`: Initialize all step instances
   - `self.steps`: List of WizardStep instances
   - No more `if step_num == 0: ...` chains

2. **Navigation:**
   - `_show_step()`: Generic step display
   - `_go_next()`: Validates current step, then navigates
   - `_go_back()`: Simple backward navigation

3. **Simplified:**
   - No more `_create_step_1()` through `_create_step_7()` methods
   - No more step-specific validation methods
   - No more step-specific data collection

4. **Size Reduction:**
   - From 1,400 lines to ~600-700 lines
   - ~700 line reduction (50%)
   - Much easier to understand and maintain

---

## Data Flow & Communication

### Step -> Orchestrator Communication

**Method 1: Direct Variable Binding (Preferred for Simple Data)**

Steps bind directly to parent's tk.StringVar/BooleanVar:

```python
# In step:
ttk.Entry(self.container, textvariable=self.parent.csv_file)

# Parent automatically gets updated value
```

**Pros:**
- Automatic synchronization
- No explicit data passing needed
- Simple and intuitive

**Cons:**
- Tight coupling to parent's variable names
- Only works for simple types

**Method 2: StepData Return (Preferred for Complex Data)**

Steps return data via StepData on validation:

```python
# In step:
def _validate_data(self, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    return True, None

def _collect_data(self) -> Dict[str, Any]:
    return {
        'field_mappings': {...},
        'description_columns': [...]
    }

# In orchestrator:
step_data = current_step.validate()
if step_data.is_valid:
    self._process_step_data(step_data)
```

**Pros:**
- Clear data flow
- Explicit validation
- Supports complex data structures

**Cons:**
- Requires explicit data processing

**Method 3: Parent Accessor Methods (Preferred for Safety)**

Steps use safe accessor methods:

```python
# In step:
file_path = self.get_parent_data('csv_file')
self.set_parent_data('csv_file', new_path)

# In base class:
def get_parent_data(self, key: str, default=None):
    if hasattr(self.parent, key):
        attr = getattr(self.parent, key)
        if hasattr(attr, 'get'):
            return attr.get()
        return attr
    return default
```

**Pros:**
- Safe access (no AttributeError)
- Works with both variables and attributes
- Encapsulates parent structure

**Cons:**
- Slightly more verbose

### Orchestrator -> Step Communication

**Method 1: Constructor Parameters**

```python
step = FileSelectionStep(parent=self, config=custom_config)
```

**Method 2: Parent Access**

```python
# Step reads from parent
csv_headers = self.parent.csv_headers
```

**Method 3: Method Calls**

```python
# Orchestrator calls step method
step.show()
step.hide()
step_data = step.validate()
```

### Step -> Step Communication

**Rule: Steps NEVER communicate directly**

All inter-step communication goes through orchestrator:

```python
# ❌ WRONG - Direct step-to-step communication
class DataPreviewStep:
    def _build_ui(self):
        file_path = self.parent.steps[0].get_file_path()

# ✅ CORRECT - Via parent data
class DataPreviewStep:
    def _build_ui(self):
        file_path = self.get_parent_data('csv_file')
```

**Rationale:**
- Steps remain independent
- Can reorder steps without breaking dependencies
- Easier to test in isolation

---

## Validation Strategy

### Two-Level Validation

**Level 1: Step-Level Validation**

Performed by step's `_validate_data()` method:

```python
def _validate_data(self, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """Validate step-specific data."""
    csv_file = data.get('csv_file', '')
    
    if not csv_file:
        return False, "Please select a CSV file"
    
    if not os.path.exists(csv_file):
        return False, f"File not found: {csv_file}"
    
    return True, None
```

**Triggered:** When user clicks "Next" button

**Scope:** Only validates data for this specific step

**Level 2: Cross-Step Validation**

Performed by orchestrator before final conversion:

```python
def _validate_all_steps(self) -> Tuple[bool, Optional[str]]:
    """Validate data across all steps."""
    # Example: Check field mappings reference valid columns
    field_mappings = self.field_mappings
    csv_headers = self.csv_headers
    
    for field, column in field_mappings.items():
        if column not in csv_headers:
            return False, f"Invalid mapping: {column} not in CSV headers"
    
    return True, None
```

**Triggered:** When user clicks "Convert to OFX" button

**Scope:** Validates consistency across multiple steps

### Validation Helpers

Use existing `gui_utils` functions:

```python
# File validation
is_valid, error = gui_utils.validate_csv_file_selection(csv_file)

# Field mapping validation
is_valid, error = gui_utils.validate_required_field_mappings(mappings)

# Description validation
is_valid, error = gui_utils.validate_description_mapping(desc, columns)

# Date validation
is_valid, error = gui_utils.validate_date_range_inputs(start, end)
```

### Validation Error Display

**User-Friendly Messages:**

```python
# ❌ BAD - Technical error
"AttributeError: 'NoneType' object has no attribute 'get'"

# ✅ GOOD - User-friendly error
"Please select a CSV file"
```

**Specific Guidance:**

```python
# ❌ BAD - Vague error
"Invalid input"

# ✅ GOOD - Specific error
"Please map the Date field before continuing"
```

---

## Migration Strategy

### Incremental Migration Approach

**Phase A: Establish Infrastructure (Week 1)**

1. Create `gui_wizard_step.py` base class
2. Create `gui_steps/` package structure
3. Write tests for base class
4. Update `csv_to_ofx_converter.py` exports

**Deliverables:**
- `src/gui_wizard_step.py` (~150 lines)
- `src/gui_steps/__init__.py`
- `tests/test_gui_wizard_step.py` (~80 lines)

**Success Criteria:**
- Base class tests passing
- No changes to converter_gui.py yet
- Zero regressions

**Phase B: Extract Simple Steps (Week 2, Days 1-3)**

Extract steps 1, 2, and 4 (simplest steps):

1. Create `FileSelectionStep` class
2. Create `CSVFormatStep` class
3. Create `OFXConfigStep` class
4. Write tests for each step
5. Update orchestrator to use new steps
6. Remove old step methods from converter_gui.py

**Deliverables:**
- 3 new step classes (~360 lines total)
- 3 new test files (~300 lines total)
- converter_gui.py reduced by ~200 lines

**Success Criteria:**
- All 230+ tests still passing
- Steps 1, 2, 4 functional in GUI
- Application runs without errors

**Phase C: Extract Medium Steps (Week 2, Days 4-5)**

Extract steps 3 and 6 (medium complexity):

1. Create `DataPreviewStep` class
2. Create `AdvancedOptionsStep` class
3. Write tests for each step
4. Update orchestrator
5. Remove old step methods

**Deliverables:**
- 2 new step classes (~330 lines total)
- 2 new test files (~270 lines total)
- converter_gui.py reduced by ~200 more lines

**Success Criteria:**
- All 230+ tests still passing
- Steps 3, 6 functional in GUI
- CSV loading and date validation working

**Phase D: Extract Complex Steps (Week 3, Days 1-3)**

Extract steps 5 and 7 (most complex):

1. Create `FieldMappingStep` class
2. Create `BalancePreviewStep` class
3. Write tests for each step
4. Update orchestrator
5. Remove old step methods

**Deliverables:**
- 2 new step classes (~450 lines total)
- 2 new test files (~330 lines total)
- converter_gui.py reduced by ~300 more lines

**Success Criteria:**
- All 230+ tests still passing
- Steps 5, 7 functional in GUI
- Field mapping and balance preview working
- Transaction deletion working

**Phase E: Cleanup & Optimization (Week 3, Days 4-5)**

1. Remove all old step methods from converter_gui.py
2. Optimize orchestrator code
3. Update documentation
4. Code quality review
5. Performance testing

**Deliverables:**
- converter_gui.py finalized (~600-700 lines)
- Updated CLAUDE.md
- Updated README files
- Code quality report

**Success Criteria:**
- All tests passing
- converter_gui.py < 750 lines
- Zero PEP8 violations
- Documentation updated
- Production-ready

### Backward Compatibility

**Maintain Public API:**

All existing public methods remain:

```python
# These must continue to work:
gui = ConverterGUI(root)
gui._convert()
gui._clear()
```

**Preserve State Variables:**

All tk variables remain accessible:

```python
# These must remain:
self.csv_file
self.delimiter
self.decimal_separator
# ... etc
```

**Import Compatibility:**

```python
# This must continue to work:
from csv_to_ofx_converter import ConverterGUI
```

### Rollback Plan

**Per-Phase Rollback:**

Each phase is independently releasable:

1. Tag repository before each phase
2. If issues found, revert to previous tag
3. Fix issues in isolation
4. Re-apply phase with fixes

**Example:**

```bash
# Before Phase B
git tag -a "pre-phase-b" -m "Before extracting simple steps"

# If Phase B has issues
git revert <phase-b-commits>
git checkout pre-phase-b

# Fix and retry
```

---

## Testing Strategy

### Test Pyramid

**Unit Tests (70% of tests):**

Test each step class in isolation:

```python
class TestFileSelectionStep(unittest.TestCase):
    def setUp(self):
        """Create mock parent and step instance."""
        self.mock_parent = MockConverterGUI()
        self.step = FileSelectionStep(self.mock_parent)
    
    def test_create_ui(self):
        """Test UI creation."""
        container = ttk.Frame()
        self.step.create(container)
        
        self.assertIsNotNone(self.step.container)
        self.assertIn('file_entry', self.step._widgets)
        self.assertIn('browse_button', self.step._widgets)
    
    def test_validate_no_file(self):
        """Test validation with no file selected."""
        self.mock_parent.csv_file.set('')
        
        step_data = self.step.validate()
        
        self.assertFalse(step_data.is_valid)
        self.assertIsNotNone(step_data.error_message)
    
    def test_validate_valid_file(self):
        """Test validation with valid file."""
        self.mock_parent.csv_file.set('/path/to/valid.csv')
        
        with patch('os.path.exists', return_value=True):
            step_data = self.step.validate()
        
        self.assertTrue(step_data.is_valid)
        self.assertIsNone(step_data.error_message)
```

**Integration Tests (20% of tests):**

Test step interactions and orchestrator:

```python
class TestWizardFlow(unittest.TestCase):
    def test_complete_wizard_flow(self):
        """Test navigating through all steps."""
        root = tk.Tk()
        gui = ConverterGUI(root)
        
        # Step 1: Select file
        gui.csv_file.set('/path/to/test.csv')
        gui._go_next()
        
        # Step 2: Configure format
        self.assertEqual(gui.current_step_idx, 1)
        gui._go_next()
        
        # ... continue through all steps
        
        root.destroy()
```

**End-to-End Tests (10% of tests):**

Test full conversion workflow:

```python
class TestFullConversion(unittest.TestCase):
    def test_complete_conversion(self):
        """Test complete conversion workflow."""
        # Create test CSV file
        # Navigate through all steps
        # Trigger conversion
        # Verify OFX output
```

### Test Coverage Requirements

**Minimum Coverage:**
- Base class: 95% coverage
- Step classes: 90% coverage each
- Orchestrator: 85% coverage

**Critical Paths:**
- Step validation: 100% coverage
- Navigation: 100% coverage
- Data collection: 95% coverage

### Mock Objects

**MockConverterGUI:**

```python
class MockConverterGUI:
    """Mock parent for testing steps."""
    
    def __init__(self):
        self.csv_file = tk.StringVar()
        self.delimiter = tk.StringVar(value=',')
        self.decimal_separator = tk.StringVar(value='.')
        self.csv_headers = []
        self.csv_data = []
        # ... all other variables
        
        self.log_messages = []
    
    def _log(self, message: str):
        """Mock logging."""
        self.log_messages.append(message)
```

### Continuous Integration

**CI Requirements:**

1. All tests must pass before merge
2. Code coverage must not decrease
3. PEP8 compliance mandatory
4. Performance benchmarks must not regress

**GitHub Actions Workflow:**

```yaml
name: Step Extraction Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.7'
      - name: Run tests
        run: |
          python -m unittest discover tests -v
      - name: Check coverage
        run: |
          coverage run -m unittest discover tests
          coverage report --fail-under=90
```

---

## Success Metrics

### Quantitative Metrics

**File Size Reduction:**
- Target: converter_gui.py < 750 lines (from 1,400 lines)
- Reduction: ~700 lines (50%)
- Achieved: TBD

**Test Coverage:**
- Target: 90%+ coverage for all new code
- New tests: ~80 base + ~1,000 step tests = 1,080 tests
- Total tests: 230 existing + 1,080 new = 1,310 tests
- Achieved: TBD

**Code Quality:**
- Target: Zero PEP8 violations
- Target: A or A+ grade from code quality reviewer
- Achieved: TBD

**Performance:**
- Target: No regression in GUI responsiveness
- Target: Step navigation < 100ms
- Achieved: TBD

### Qualitative Metrics

**Maintainability:**
- New contributor can understand a step in < 10 minutes
- Adding a new step requires < 100 lines of code
- Bug isolation time reduced by 50%

**Extensibility:**
- Can add conditional steps without modifying orchestrator
- Can reorder steps by changing list order
- Can create alternate wizard flows by composing steps

**Testability:**
- Each step independently testable
- 100% of validation logic covered by tests
- No GUI dependencies in business logic

### Release Criteria

**Before Merging Phase E:**

✅ All 1,310+ tests passing
✅ converter_gui.py < 750 lines
✅ Zero PEP8 violations
✅ Code quality grade A or better
✅ Documentation updated (CLAUDE.md, READMEs)
✅ Performance benchmarks met
✅ Manual smoke test passed
✅ Product Manager approval
✅ Tech Lead approval

---

## Risk Management

### Identified Risks

**Risk 1: Increased Complexity**

**Severity:** Medium
**Probability:** Medium

**Description:**
Adding base class and 7 step classes increases overall code complexity compared to single-file approach.

**Mitigation:**
- Clear documentation of step lifecycle
- Comprehensive tests for each step
- Code review focus on simplicity
- Use established patterns (dependency injection, dataclasses)

**Impact if Occurs:**
- Harder for new contributors to understand
- Longer onboarding time

**Response Plan:**
- Create step development guide
- Provide step template
- Add inline documentation

---

**Risk 2: Breaking Existing Functionality**

**Severity:** High
**Probability:** Low

**Description:**
Refactoring existing working code could introduce regressions.

**Mitigation:**
- Incremental migration (one step at a time)
- Comprehensive test suite (1,310+ tests)
- Test after each phase
- Keep backward compatibility

**Impact if Occurs:**
- Users experience bugs
- Lost productivity

**Response Plan:**
- Rollback to previous phase
- Fix issues in isolation
- Re-apply with fixes

---

**Risk 3: Performance Degradation**

**Severity:** Medium
**Probability:** Low

**Description:**
Additional class instantiation and method calls could slow down GUI.

**Mitigation:**
- Lazy UI creation (create step UI only when shown)
- Performance benchmarks before/after
- Profile code if issues arise

**Impact if Occurs:**
- Slower GUI responsiveness
- Poor user experience

**Response Plan:**
- Profile and identify bottlenecks
- Optimize hot paths
- Consider caching if needed

---

**Risk 4: Import Circular Dependencies**

**Severity:** Medium
**Probability:** Low

**Description:**
Step classes import from orchestrator, orchestrator imports steps.

**Mitigation:**
- Steps only import from base class
- Orchestrator imports steps in method (lazy import)
- No step-to-step imports

**Impact if Occurs:**
- Application fails to start
- Import errors

**Response Plan:**
- Restructure imports
- Use lazy imports
- Review dependency graph

---

**Risk 5: Testing Complexity**

**Severity:** Medium
**Probability:** Medium

**Description:**
Testing Tkinter widgets is complex and environment-dependent.

**Mitigation:**
- Use mock parent objects
- Test validation logic independently
- Integration tests only for critical paths
- Skip GUI tests in CI if no display server

**Impact if Occurs:**
- Tests fail in CI
- Reduced test coverage

**Response Plan:**
- Add DISPLAY=:99 for headless testing
- Mark GUI tests as optional
- Focus on unit tests for business logic

---

## Implementation Phases

### Phase A: Infrastructure (Week 1)

**Timeline:** 5 days

**Tasks:**
1. Create `gui_wizard_step.py` base class
2. Create `gui_steps/` package
3. Write base class tests
4. Update exports in `csv_to_ofx_converter.py`

**Deliverables:**
- Base class: ~150 lines
- Tests: ~80 lines
- Package structure

**Success Criteria:**
- Base class tests passing
- Zero regressions
- Code quality: A grade

---

### Phase B: Simple Steps (Week 2, Days 1-3)

**Timeline:** 3 days

**Tasks:**
1. Extract Step 1 (File Selection)
2. Extract Step 2 (CSV Format)
3. Extract Step 4 (OFX Config)
4. Write tests for each
5. Update orchestrator
6. Remove old methods

**Deliverables:**
- 3 step classes: ~360 lines
- 3 test files: ~300 lines
- Reduced converter_gui.py: ~1,200 lines

**Success Criteria:**
- All tests passing
- Steps 1, 2, 4 functional
- Zero regressions

---

### Phase C: Medium Steps (Week 2, Days 4-5)

**Timeline:** 2 days

**Tasks:**
1. Extract Step 3 (Data Preview)
2. Extract Step 6 (Advanced Options)
3. Write tests for each
4. Update orchestrator
5. Remove old methods

**Deliverables:**
- 2 step classes: ~330 lines
- 2 test files: ~270 lines
- Reduced converter_gui.py: ~1,000 lines

**Success Criteria:**
- All tests passing
- Steps 3, 6 functional
- CSV loading working

---

### Phase D: Complex Steps (Week 3, Days 1-3)

**Timeline:** 3 days

**Tasks:**
1. Extract Step 5 (Field Mapping)
2. Extract Step 7 (Balance Preview)
3. Write tests for each
4. Update orchestrator
5. Remove old methods

**Deliverables:**
- 2 step classes: ~450 lines
- 2 test files: ~330 lines
- Reduced converter_gui.py: ~700 lines

**Success Criteria:**
- All tests passing
- Steps 5, 7 functional
- Field mapping working
- Balance preview working

---

### Phase E: Cleanup (Week 3, Days 4-5)

**Timeline:** 2 days

**Tasks:**
1. Remove all old step methods
2. Optimize orchestrator
3. Update documentation
4. Code quality review
5. Performance testing
6. Final testing

**Deliverables:**
- converter_gui.py finalized: ~600-700 lines
- Updated CLAUDE.md
- Updated README files
- Code quality report
- Performance report

**Success Criteria:**
- All 1,310+ tests passing
- converter_gui.py < 750 lines
- Zero PEP8 violations
- Documentation complete
- Production-ready

---

## Conclusion

### Summary

This plan provides a comprehensive roadmap for extracting wizard steps from `converter_gui.py` into a modular, testable architecture:

**Key Benefits:**
1. **50% Reduction** in converter_gui.py size (1,400 → 700 lines)
2. **Modular Architecture** with clear step boundaries
3. **Enhanced Testability** with 1,080+ new tests
4. **Improved Maintainability** for new contributors
5. **Better Extensibility** for future wizard enhancements

**Architecture Highlights:**
- Abstract base class with lifecycle methods
- 7 independent step classes
- Clear data flow via StepData dataclass
- Safe parent access through helper methods
- Comprehensive validation strategy

**Risk Mitigation:**
- Incremental 5-phase migration
- Extensive test coverage (1,310+ total tests)
- Backward compatibility maintained
- Rollback plan for each phase

**Timeline:**
- 3 weeks (15 working days)
- 5 phases with clear deliverables
- Independent phase releases

### Next Steps

**Immediate Actions (Product Manager):**
1. Review and approve this plan
2. Prioritize against other work
3. Allocate tech lead resources

**Tech Lead Actions:**
1. Review technical architecture
2. Validate timeline estimates
3. Assign to developer

**Developer Actions:**
1. Set up development branch
2. Begin Phase A (infrastructure)
3. Daily progress updates

### Approval

**Stakeholders:**
- Product Manager: [ ] Approved / [ ] Needs Changes
- Tech Lead: [ ] Approved / [ ] Needs Changes
- Code Quality Reviewer: [ ] Approved / [ ] Needs Changes

**Sign-off:**
- Date: ________________
- Version: 1.0

---

*Document created: November 22, 2025*
*Author: Product Manager*
*Status: Draft - Awaiting Approval*
