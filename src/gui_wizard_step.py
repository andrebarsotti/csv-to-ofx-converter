"""
gui_wizard_step.py - Base class for wizard steps

This module provides the abstract base class and supporting dataclasses
for implementing wizard steps in a multi-step GUI wizard.

Classes:
    StepConfig: Configuration dataclass for wizard step properties
    StepData: Data returned by step validation with results and error info
    WizardStep: Abstract base class for all wizard step implementations
"""

import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class StepConfig:
    """
    Configuration for a wizard step.

    This dataclass encapsulates all configuration properties for a wizard step,
    eliminating the need for hard-coded step properties.

    Attributes:
        step_number: Position in wizard (0-based index)
        step_name: Display name for the step (e.g., "File Selection")
        step_title: Full title displayed in step frame
        is_required: Whether the step can be skipped (default: True)
        can_go_back: Whether the back button should be enabled (default: True)
        show_next: Whether to show the next button (default: True)
        show_convert: Whether to show the convert button (default: False)
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
    Data returned by a step after validation.

    This dataclass provides a standardized return format for step validation,
    creating a clear contract between step and orchestrator.

    Attributes:
        is_valid: Whether step data is valid for progression to next step
        error_message: User-friendly error message if validation failed (None if valid)
        data: Dictionary containing step-specific data collected from UI
    """
    is_valid: bool
    error_message: Optional[str] = None
    data: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Initialize data dict if None was provided."""
        if self.data is None:
            self.data = {}


class WizardStep(ABC):
    """
    Abstract base class for wizard steps.

    This class provides the foundation for all wizard step implementations,
    handling common functionality like lifecycle management, parent access,
    and validation coordination.

    Subclasses must implement three abstract methods:
    - _build_ui(): Create step-specific UI elements
    - _collect_data(): Gather data from UI elements
    - _validate_data(): Validate collected data

    Lifecycle:
    1. __init__: Initialize step with parent and config
    2. create(): Build UI in parent container
    3. show(): Display step when it becomes active
    4. validate(): Collect and validate data before navigation
    5. hide(): Hide step when leaving
    6. destroy(): Cleanup resources when step is removed

    Example:
        >>> class MyStep(WizardStep):
        ...     def __init__(self, parent):
        ...         config = StepConfig(
        ...             step_number=0,
        ...             step_name="My Step",
        ...             step_title="Step 1: My Step"
        ...         )
        ...         super().__init__(parent, config)
        ...
        ...     def _build_ui(self):
        ...         # Create widgets
        ...         pass
        ...
        ...     def _collect_data(self):
        ...         return {'field': 'value'}
        ...
        ...     def _validate_data(self, data):
        ...         return True, None
    """

    def __init__(self, parent, config: StepConfig):
        """
        Initialize wizard step.

        Args:
            parent: Parent wizard orchestrator (typically ConverterGUI instance)
            config: Step configuration containing display properties and behavior
        """
        self.parent = parent
        self.config = config
        self.container: Optional[ttk.Frame] = None
        self._widgets: Dict[str, tk.Widget] = {}

    # === Lifecycle Methods ===

    def create(self, parent_container: ttk.Frame) -> ttk.Frame:
        """
        Create step UI in parent container.

        This method creates the main step frame, calls the subclass's _build_ui()
        method to populate it with widgets, and configures the layout for responsiveness.

        Args:
            parent_container: Parent container widget where step should be created

        Returns:
            The created step frame (self.container)
        """
        # Create step frame with title
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

        Subclasses must implement this method to create their widgets.
        Widget references should be stored in self._widgets for later access.

        Example:
            >>> def _build_ui(self):
            ...     self._widgets['label'] = ttk.Label(self.container, text="Hello")
            ...     self._widgets['label'].grid(row=0, column=0)
        """
        pass

    def _configure_layout(self):
        """
        Configure grid layout for responsiveness.

        Default implementation makes the first column expandable.
        Subclasses can override this for custom layout configurations.
        """
        if self.container:
            self.container.columnconfigure(0, weight=1)

    def show(self):
        """
        Show this step (called when step becomes active).

        Default implementation makes the container visible.
        Subclasses can override to perform additional actions on activation
        (e.g., loading data, refreshing display).
        """
        if self.container:
            self.container.grid()

    def hide(self):
        """
        Hide this step (called when leaving step).

        Default implementation hides the container without destroying it.
        Subclasses can override to perform cleanup actions
        (e.g., saving state, clearing temporary data).
        """
        if self.container:
            self.container.grid_remove()

    def destroy(self):
        """
        Destroy step and cleanup resources.

        This method destroys the UI container and clears all widget references.
        Called when the step is permanently removed from the wizard.
        """
        if self.container:
            self.container.destroy()
            self.container = None
        self._widgets.clear()

    # === Data Collection & Validation ===

    def validate(self) -> StepData:
        """
        Validate step data before progression.

        This method orchestrates the validation process by:
        1. Collecting data from UI elements via _collect_data()
        2. Validating the collected data via _validate_data()
        3. Returning a StepData object with results

        Returns:
            StepData object containing:
            - is_valid: True if data is valid, False otherwise
            - error_message: User-friendly error message if invalid, None if valid
            - data: Collected data dict if valid, empty dict if invalid
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

        Subclasses must implement this to extract current values from their widgets.

        Returns:
            Dictionary with step-specific data (e.g., {'csv_file': '/path/to/file.csv'})

        Example:
            >>> def _collect_data(self):
            ...     return {
            ...         'file_path': self._widgets['entry'].get(),
            ...         'option': self._widgets['checkbox_var'].get()
            ...     }
        """
        pass

    @abstractmethod
    def _validate_data(self, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Validate collected step data.

        Subclasses must implement this to validate the data collected by _collect_data().

        Args:
            data: Data dictionary returned by _collect_data()

        Returns:
            Tuple of (is_valid, error_message):
            - is_valid: True if data is valid, False otherwise
            - error_message: User-friendly error message if invalid, None if valid

        Example:
            >>> def _validate_data(self, data):
            ...     file_path = data.get('file_path', '')
            ...     if not file_path:
            ...         return False, "Please select a file"
            ...     if not os.path.exists(file_path):
            ...         return False, f"File not found: {file_path}"
            ...     return True, None
        """
        pass

    # === Helper Methods ===

    def log(self, message: str):
        """
        Log message to parent's activity log.

        This provides a safe way to log messages without directly depending
        on the parent's logging implementation.

        Args:
            message: Message to log
        """
        if hasattr(self.parent, '_log'):
            self.parent._log(message)

    def get_parent_data(self, key: str, default=None):
        """
        Safely get data from parent orchestrator.

        This method provides safe access to parent data, handling both
        regular attributes and Tkinter variable objects (StringVar, BooleanVar, etc.).

        Args:
            key: Attribute name to retrieve from parent
            default: Default value to return if key not found

        Returns:
            Value from parent attribute, or default if not found

        Example:
            >>> file_path = self.get_parent_data('csv_file')  # Gets StringVar value
            >>> headers = self.get_parent_data('csv_headers', [])  # Returns list or []
        """
        # Access through parent's public interface only
        if hasattr(self.parent, key):
            attr = getattr(self.parent, key)
            # If it's a Tkinter variable (StringVar, BooleanVar, etc.), get its value
            # Check for Tkinter Variable class to avoid calling .get() on dict/list
            if hasattr(attr, 'get') and hasattr(attr, 'set') and callable(attr.get):
                return attr.get()
            return attr
        return default

    def set_parent_data(self, key: str, value: Any):
        """
        Safely set data in parent orchestrator.

        This method provides safe write access to parent data, handling both
        regular attributes and Tkinter variable objects.

        Args:
            key: Attribute name to set in parent
            value: Value to set

        Example:
            >>> self.set_parent_data('csv_file', '/path/to/file.csv')  # Sets StringVar
            >>> self.set_parent_data('csv_headers', ['Date', 'Amount'])  # Sets list
        """
        if hasattr(self.parent, key):
            attr = getattr(self.parent, key)
            # If it's a Tkinter variable, use set() method
            if hasattr(attr, 'set'):
                attr.set(value)
            else:
                setattr(self.parent, key, value)
