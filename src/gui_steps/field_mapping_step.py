"""
field_mapping_step.py - Field Mapping Step (Step 5)

This module implements the field mapping step for the CSV to OFX Converter wizard.
Users can map CSV columns to OFX transaction fields and configure composite descriptions.

Classes:
    FieldMappingStep: Step 5 implementation for field mapping and composite description
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Tuple, Optional, List

from src.gui_wizard_step import WizardStep, StepConfig
from src import gui_utils
from src.constants import NOT_MAPPED, NOT_SELECTED


class FieldMappingStep(WizardStep):
    """
    Step 5: Map CSV columns to OFX transaction fields.

    This step allows users to:
    - Map CSV columns to required OFX fields (date, amount)
    - Map CSV columns to optional OFX fields (description, type, id)
    - Configure composite descriptions by combining up to 4 columns
    - Choose separator for composite descriptions (space, dash, comma, pipe)

    UI Elements:
        - Info label with mapping instructions
        - 5 field mapping comboboxes (date*, amount*, description, type, id)
        - Help text for each field
        - Composite description section with:
          - 4 column selector comboboxes
          - 4 separator radio buttons (Space, Dash, Comma, Pipe)
        - Note label about required fields

    Required Fields:
        - Date: Transaction date (marked with *)
        - Amount: Transaction amount (marked with *)
        - Description: Either single field OR composite description must be configured

    Data Collected:
        - field_mappings: Dict mapping OFX field names to CSV column names
        - description_columns: List of 4 column names for composite description
        - description_separator: Separator string for composite description

    Validation:
        - Date field must be mapped
        - Amount field must be mapped
        - Either description field OR at least one composite column must be selected

    Example:
        >>> step = FieldMappingStep(parent_gui)
        >>> container = step.create(parent_frame)
        >>> step.show()
        >>> result = step.validate()
        >>> if result.is_valid:
        ...     print(f"Field mappings: {result.data['field_mappings']}")
        ...     print(f"Composite columns: {result.data['description_columns']}")
    """

    def __init__(self, parent):
        """
        Initialize FieldMappingStep.

        Args:
            parent: Parent wizard orchestrator (ConverterGUI)
        """
        config = StepConfig(
            step_number=4,
            step_name="Field Mapping",
            step_title="Step 5: Map CSV Columns to OFX Fields"
        )
        super().__init__(parent, config)

    def _build_ui(self):
        """
        Build field mapping UI.

        Creates comboboxes for mapping CSV columns to OFX fields,
        and a composite description section for combining multiple columns.
        """
        # Info label
        ttk.Label(
            self.container,
            text="Map your CSV columns to OFX transaction fields:",
            font=('Arial', 10)
        ).grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 20))

        # Ensure CSV is loaded
        csv_headers = self.get_parent_data('csv_headers', [])
        if not csv_headers:
            ttk.Label(
                self.container,
                text="No CSV data loaded. Please go back to step 3.",
                foreground='red'
            ).grid(row=1, column=0, columnspan=3)
            return

        # Create field mapping widgets
        self._create_field_mapping_widgets(csv_headers)

        # Composite description section
        self._create_composite_description_section(csv_headers)

        # Note about required fields
        self._create_note_label()

    def _create_field_mapping_widgets(self, csv_headers: List[str]):
        """
        Create mapping widgets for OFX fields.

        Args:
            csv_headers: List of CSV column headers
        """
        # Define OFX fields with labels and help text
        ofx_fields = [
            ('date', 'Date *', 'Transaction date'),
            ('amount', 'Amount *', 'Transaction amount (positive or negative)'),
            ('description', 'Description',
             'Transaction description (or use composite below)'),
            ('type', 'Type', 'Transaction type: DEBIT or CREDIT (optional)'),
            ('id', 'ID', 'Unique transaction identifier (optional)'),
        ]

        column_options = [NOT_MAPPED] + csv_headers

        # Get or create field_mappings dictionary
        field_mappings = self.get_parent_data('field_mappings', {})
        if not isinstance(field_mappings, dict):
            field_mappings = {}
            self.set_parent_data('field_mappings', field_mappings)

        # Create mapping widgets for each field
        for idx, (field_key, field_label, field_help) in enumerate(ofx_fields, start=1):
            # Label
            ttk.Label(
                self.container,
                text=f"{field_label}:",
                font=('Arial', 10, 'bold')
            ).grid(row=idx, column=0, sticky=tk.W, padx=5, pady=5)

            # Get or create StringVar for this field
            if field_key not in field_mappings:
                field_mappings[field_key] = tk.StringVar(value=NOT_MAPPED)

            # Combobox
            combo = ttk.Combobox(
                self.container,
                textvariable=field_mappings[field_key],
                values=column_options,
                state='readonly',
                width=30
            )
            combo.grid(row=idx, column=1, sticky=tk.W, padx=5, pady=5)

            # Store widget reference
            self._widgets[f'{field_key}_combo'] = combo

            # Help text
            ttk.Label(
                self.container,
                text=field_help,
                font=('Arial', 8),
                foreground='gray'
            ).grid(row=idx, column=2, sticky=tk.W, padx=5, pady=5)

    def _create_composite_description_section(self, csv_headers: List[str]):
        """
        Create composite description section.

        Args:
            csv_headers: List of CSV column headers
        """
        # Calculate row offset (after field mappings)
        row_offset = 6  # 5 field mappings + 1 for separator

        # Horizontal separator
        ttk.Separator(
            self.container,
            orient='horizontal'
        ).grid(row=row_offset, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=20)

        # Section title
        ttk.Label(
            self.container,
            text="Composite Description (Optional)",
            font=('Arial', 11, 'bold')
        ).grid(row=row_offset + 1, column=0, columnspan=3, sticky=tk.W, pady=(0, 10))

        # Instructions
        ttk.Label(
            self.container,
            text="Combine multiple columns to create transaction descriptions:",
            font=('Arial', 9)
        ).grid(row=row_offset + 2, column=0, columnspan=3, sticky=tk.W, pady=(0, 10))

        # Create composite UI frame
        composite_frame = ttk.Frame(self.container)
        composite_frame.grid(
            row=row_offset + 3,
            column=0,
            columnspan=3,
            sticky=(tk.W, tk.E),
            pady=5
        )

        self._create_composite_description_ui(composite_frame, csv_headers)

    def _create_composite_description_ui(self, parent: ttk.Frame, csv_headers: List[str]):
        """
        Create UI for composite description configuration.

        Args:
            parent: Parent frame to contain composite description widgets
            csv_headers: List of CSV column headers
        """
        parent.columnconfigure(1, weight=1)

        column_options = [NOT_SELECTED] + csv_headers

        # Get or create description_columns list
        description_columns = self.get_parent_data('description_columns', [])
        if not isinstance(description_columns, list) or len(description_columns) != 4:
            # Create new list with 4 StringVars
            description_columns = []
            for i in range(4):
                description_columns.append(tk.StringVar(value=NOT_SELECTED))
            self.set_parent_data('description_columns', description_columns)

        # Create 4 column selectors
        for i in range(4):
            ttk.Label(
                parent,
                text=f"Column {i+1}:",
                font=('Arial', 9)
            ).grid(row=i, column=0, sticky=tk.W, padx=5, pady=3)

            combo = ttk.Combobox(
                parent,
                textvariable=description_columns[i],
                values=column_options,
                state='readonly',
                width=30
            )
            combo.grid(row=i, column=1, sticky=tk.W, padx=5, pady=3)

            # Store widget reference
            self._widgets[f'desc_col_{i}_combo'] = combo

        # Separator selection
        ttk.Label(
            parent,
            text="Separator:",
            font=('Arial', 9)
        ).grid(row=4, column=0, sticky=tk.W, padx=5, pady=3)

        # Get or create description_separator variable
        description_separator = self.get_parent_data('description_separator')
        if description_separator is None:
            description_separator = tk.StringVar(value=' ')
            self.set_parent_data('description_separator', description_separator)

        # Separator radio buttons frame
        sep_frame = ttk.Frame(parent)
        sep_frame.grid(row=4, column=1, sticky=tk.W, padx=5, pady=3)

        # Radio buttons for separators
        separators = [
            ("Space", ' '),
            ("Dash (-)", ' - '),
            ("Comma (,)", ', '),
            ("Pipe (|)", ' | ')
        ]

        for label, value in separators:
            rb = ttk.Radiobutton(
                sep_frame,
                text=label,
                variable=description_separator,
                value=value
            )
            rb.pack(side=tk.LEFT, padx=5)

            # Store widget reference
            self._widgets[f'sep_radio_{value}'] = rb

    def _create_note_label(self):
        """Create note label about required fields."""
        note_text = (
            "* Required fields\n"
            "Note: If composite description is configured, it will be used instead of "
            "the Description field mapping."
        )
        ttk.Label(
            self.container,
            text=note_text,
            font=('Arial', 8),
            foreground='gray',
            wraplength=700,
            justify=tk.LEFT
        ).grid(row=10, column=0, columnspan=3, sticky=tk.W, pady=(20, 0))

    def _configure_layout(self):
        """Configure responsive grid layout."""
        # Make column 1 expandable (for comboboxes)
        self.container.columnconfigure(1, weight=1)

        # Allow the container to expand
        self.container.grid_rowconfigure(0, weight=0)  # Info label
        self.container.grid_rowconfigure(6, weight=0)  # Separator
        self.container.grid_rowconfigure(9, weight=1)  # Composite frame

    def _collect_data(self) -> Dict[str, Any]:
        """
        Collect data from field mapping step.

        Returns:
            Dictionary containing field_mappings, description_columns,
            and description_separator
        """
        # Collect field mappings
        field_mappings = self.get_parent_data('field_mappings', {})
        field_mappings_dict = {}
        for field_key, string_var in field_mappings.items():
            if isinstance(string_var, tk.StringVar):
                field_mappings_dict[field_key] = string_var.get()
            else:
                field_mappings_dict[field_key] = str(string_var)

        # Collect description columns
        description_columns = self.get_parent_data('description_columns', [])
        description_columns_list = []
        for string_var in description_columns:
            if isinstance(string_var, tk.StringVar):
                description_columns_list.append(string_var.get())
            else:
                description_columns_list.append(str(string_var))

        # Collect description separator
        description_separator = self.get_parent_data('description_separator')
        if isinstance(description_separator, tk.StringVar):
            description_separator_str = description_separator.get()
        else:
            description_separator_str = str(description_separator) if description_separator else ' '

        return {
            'field_mappings': field_mappings_dict,
            'description_columns': description_columns_list,
            'description_separator': description_separator_str
        }

    def _validate_data(self, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Validate field mapping data.

        Ensures that required fields (date and amount) are mapped,
        and that either description field or composite description is configured.

        Args:
            data: Data collected from UI

        Returns:
            Tuple of (is_valid, error_message)
        """
        field_mappings = data.get('field_mappings', {})
        description_columns = data.get('description_columns', [])

        # Validate required fields (date and amount)
        is_valid, error_msg = gui_utils.validate_required_field_mappings(
            field_mappings,
            NOT_MAPPED
        )
        if not is_valid:
            return False, error_msg

        # Validate description mapping (either single field or composite)
        description_mapping = field_mappings.get('description', NOT_MAPPED)
        is_valid, error_msg = gui_utils.validate_description_mapping(
            description_mapping,
            description_columns,
            NOT_MAPPED,
            NOT_SELECTED
        )
        if not is_valid:
            return False, error_msg

        return True, None
