# System Architecture

## 1. Architecture Overview

**CSV to OFX Converter** follows a layered architecture with clear separation of responsibilities. The application uses an adapted **Model-View-Controller (MVC)** pattern, with emphasis on:

- **Separation of Concerns**: Business logic separated from graphical interface
- **Dependency Injection**: Companion classes receive GUI as parameter
- **Testability**: Pure functions and independently testable classes

### 1.1 Layer Architecture Diagram

```mermaid
graph TD
    subgraph Presentation Layer
        GUI[ConverterGUI]
        Steps[Wizard Steps]
    end

    subgraph Application Layer
        BM[BalanceManager]
        CH[ConversionHandler]
        TM[TransactionManager]
    end

    subgraph Domain Layer
        CSV[CSVParser]
        OFX[OFXGenerator]
        DV[DateValidator]
    end

    subgraph Utility Layer
        TU[transaction_utils]
        GU[gui_utils]
        CONST[constants]
    end

    subgraph Infrastructure
        FS[(File System)]
        LOG[Logging]
    end

    GUI --> Steps
    Steps --> BM
    Steps --> CH
    Steps --> TM

    BM --> CSV
    BM --> TU
    BM --> GU

    CH --> CSV
    CH --> OFX
    CH --> DV
    CH --> TU

    TM --> DV

    CSV --> FS
    OFX --> FS

    GUI --> LOG
    CSV --> LOG
    OFX --> LOG
    DV --> LOG
    CH --> LOG
```

## 2. Layer Descriptions

### 2.1 Presentation Layer

Responsible for user interface through Tkinter widgets.

| Component | Responsibility |
|-----------|----------------|
| **ConverterGUI** | Main wizard orchestrator, manages navigation and global state |
| **WizardStep** | Abstract base class for all wizard steps |
| **FileSelectionStep** | UI for CSV file selection |
| **CSVFormatStep** | UI for CSV format configuration |
| **DataPreviewStep** | UI for data preview in table |
| **OFXConfigStep** | UI for OFX configuration (account, bank, currency) |
| **FieldMappingStep** | UI for CSV→OFX field mapping |
| **AdvancedOptionsStep** | UI for advanced options (inversion, validation) |
| **BalancePreviewStep** | UI for balance preview and confirmation |

### 2.2 Application Layer

Companion classes that orchestrate business operations without direct Tkinter dependency.

| Component | Responsibility |
|-----------|----------------|
| **BalanceManager** | Balance calculations and transaction preview |
| **ConversionHandler** | CSV→OFX conversion process orchestration |
| **TransactionManager** | Transaction management and context menus |

### 2.3 Domain Layer

Core classes that implement main business logic.

| Component | Responsibility |
|-----------|----------------|
| **CSVParser** | CSV file parsing with multiple format support |
| **OFXGenerator** | OFX 1.0.2 file generation |
| **DateValidator** | Date validation against statement period |

### 2.4 Utility Layer

Pure functions and shared constants.

| Component | Responsibility |
|-----------|----------------|
| **transaction_utils** | Transaction processing functions |
| **gui_utils** | GUI operation utility functions |
| **constants** | Shared constants (NOT_MAPPED, NOT_SELECTED) |

## 3. Design Patterns Used

### 3.1 Wizard Pattern

The user interface implements the Wizard pattern to guide users through a multi-step process.

```mermaid
classDiagram
    class WizardStep {
        <<abstract>>
        +parent: ConverterGUI
        +config: StepConfig
        +container: Frame
        +create()
        +show()
        +hide()
        +destroy()
        +validate() StepData
        #_build_ui()*
        #_collect_data()* Dict
        #_validate_data()* Tuple
    }

    class FileSelectionStep {
        +_build_ui()
        +_collect_data()
        +_validate_data()
    }

    class CSVFormatStep {
        +_build_ui()
        +_collect_data()
        +_validate_data()
    }

    class DataPreviewStep {
        +_build_ui()
        +_collect_data()
        +_validate_data()
    }

    WizardStep <|-- FileSelectionStep
    WizardStep <|-- CSVFormatStep
    WizardStep <|-- DataPreviewStep
```

### 3.2 Dependency Injection

Companion classes receive GUI as parameter, enabling testing with mocks.

```mermaid
classDiagram
    class ConverterGUI {
        +balance_manager: BalanceManager
        +conversion_handler: ConversionHandler
        +transaction_manager: TransactionManager
    }

    class BalanceManager {
        +parent: ConverterGUI
        +calculate_balance_preview()
        +validate_balance_input()
    }

    class ConversionHandler {
        +parent: ConverterGUI
        +convert()
    }

    class TransactionManager {
        +parent: ConverterGUI
        +show_context_menu()
        +delete_selected_transactions()
    }

    ConverterGUI --> BalanceManager : creates
    ConverterGUI --> ConversionHandler : creates
    ConverterGUI --> TransactionManager : creates
    BalanceManager --> ConverterGUI : references
    ConversionHandler --> ConverterGUI : references
    TransactionManager --> ConverterGUI : references
```

### 3.3 Template Method

The `WizardStep` class uses the Template Method pattern to define the validation algorithm skeleton.

```python
# Template Method in WizardStep
def validate(self) -> StepData:
    data = self._collect_data()      # Hook for subclass
    is_valid, error = self._validate_data(data)  # Hook for subclass
    return StepData(is_valid, error, data)
```

### 3.4 Data Transfer Objects (DTOs)

Use of dataclasses for data transfer between layers.

```mermaid
classDiagram
    class StepConfig {
        +step_number: int
        +step_name: str
        +step_title: str
        +is_required: bool
        +can_go_back: bool
    }

    class StepData {
        +is_valid: bool
        +error_message: str
        +data: Dict
    }

    class BalancePreviewData {
        +initial_balance: float
        +total_credits: float
        +total_debits: float
        +calculated_final_balance: float
        +transaction_count: int
        +transactions: List
        +to_dict()
    }

    class ConversionConfig {
        +csv_file_path: str
        +csv_data: List
        +field_mappings: Dict
        +invert_values: bool
        +...
    }
```

## 4. Component Communication

### 4.1 Conversion Data Flow

```mermaid
sequenceDiagram
    participant GUI as ConverterGUI
    participant CH as ConversionHandler
    participant CSV as CSVParser
    participant DV as DateValidator
    participant OFX as OFXGenerator
    participant FS as FileSystem

    GUI->>CH: convert(config, output_file)
    CH->>CSV: CSVParser(delimiter, decimal)
    CH->>DV: DateValidator(start, end)
    
    loop For each CSV row
        CH->>CSV: normalize_amount()
        CH->>DV: is_within_range(date)
        alt Date out of range
            CH->>CH: _validate_and_adjust_date()
        end
        CH->>OFX: add_transaction()
    end
    
    CH->>OFX: generate(output_path, ...)
    OFX->>FS: write file
    FS-->>OFX: success
    OFX-->>CH: success
    CH-->>GUI: (success, message, stats)
```

### 4.2 Balance Calculation Flow

```mermaid
sequenceDiagram
    participant Step7 as BalancePreviewStep
    participant GUI as ConverterGUI
    participant BM as BalanceManager
    participant CSV as CSVParser
    participant TU as transaction_utils

    Step7->>GUI: _calculate_balance_preview()
    GUI->>BM: calculate_balance_preview(params)
    BM->>CSV: CSVParser(delimiter, decimal)
    
    loop For each non-excluded row
        BM->>CSV: normalize_amount()
        BM->>TU: build_transaction_description()
        BM->>TU: determine_transaction_type()
        BM->>BM: _process_preview_row()
    end
    
    BM-->>GUI: BalancePreviewData
    GUI-->>Step7: balance_info dict
```

## 5. Frameworks and Technologies

### 5.1 Technology Stack

| Layer | Technology | Justification |
|-------|------------|---------------|
| **Language** | Python 3.7+ | Portability, rich standard library |
| **GUI** | Tkinter/ttk | Included in standard library, cross-platform |
| **Testing** | unittest | Standard framework, no external dependencies |
| **Build** | PyInstaller | Standalone executable generation |
| **Logging** | logging | Standard module, configurable |

### 5.2 Dependencies

The application uses **only Python standard library** for runtime, ensuring:
- Zero external dependencies
- Easy installation
- Maximum portability

Development dependencies:
- **PyInstaller**: Only for executable builds

## 6. Component Diagram

```mermaid
graph TB
    subgraph main.py
        ENTRY[Entry Point]
    end

    subgraph src/
        subgraph Core
            CSV[csv_parser.py]
            OFX[ofx_generator.py]
            DV[date_validator.py]
        end

        subgraph GUI
            CGUI[converter_gui.py]
            WS[gui_wizard_step.py]
        end

        subgraph Companions
            BM[gui_balance_manager.py]
            CH[gui_conversion_handler.py]
            TM[gui_transaction_manager.py]
        end

        subgraph Utils
            TU[transaction_utils.py]
            GU[gui_utils.py]
            CONST[constants.py]
        end

        subgraph gui_steps/
            FS[file_selection_step.py]
            CF[csv_format_step.py]
            DP[data_preview_step.py]
            OC[ofx_config_step.py]
            FM[field_mapping_step.py]
            AO[advanced_options_step.py]
            BP[balance_preview_step.py]
        end
    end

    ENTRY --> CGUI
    CGUI --> WS
    CGUI --> BM
    CGUI --> CH
    CGUI --> TM

    WS --> FS
    WS --> CF
    WS --> DP
    WS --> OC
    WS --> FM
    WS --> AO
    WS --> BP

    BM --> CSV
    BM --> TU
    CH --> CSV
    CH --> OFX
    CH --> DV
    TM --> DV

    FS --> GU
    CF --> GU
    BP --> TU
```

## 7. Data Model

### 7.1 Transaction Structure

```mermaid
classDiagram
    class Transaction {
        +date: str
        +amount: float
        +description: str
        +type: str
        +id: str
        +row_idx: int
        +date_status: str
    }

    class CSVRow {
        +columns: Dict~str,str~
    }

    class OFXTransaction {
        +type: str
        +date: str
        +amount: float
        +id: str
        +memo: str
    }

    CSVRow --> Transaction : parsing
    Transaction --> OFXTransaction : generation
```

### 7.2 OFX File Structure

```mermaid
flowchart TD
    subgraph OFX File
        H[Header]
        SIGNON[SIGNONMSGSRSV1]
        CC[CREDITCARDMSGSRSV1]
    end

    subgraph SIGNONMSGSRSV1
        STATUS1[STATUS]
        FI[FI - Bank Info]
    end

    subgraph CREDITCARDMSGSRSV1
        CCSTMT[CCSTMTTRNRS]
    end

    subgraph CCSTMTTRNRS
        STATUS2[STATUS]
        CCSTMTRS[CCSTMTRS]
    end

    subgraph CCSTMTRS
        CURDEF[Currency]
        ACCT[CCACCTFROM]
        TRANLIST[BANKTRANLIST]
        LEDGER[LEDGERBAL]
        AVAIL[AVAILBAL]
    end

    subgraph BANKTRANLIST
        TRANS1[STMTTRN 1]
        TRANS2[STMTTRN 2]
        TRANSN[STMTTRN N]
    end

    H --> SIGNON
    SIGNON --> CC
    CC --> CCSTMT
    CCSTMT --> STATUS2
    CCSTMT --> CCSTMTRS
    CCSTMTRS --> CURDEF
    CCSTMTRS --> ACCT
    CCSTMTRS --> TRANLIST
    CCSTMTRS --> LEDGER
    CCSTMTRS --> AVAIL
    TRANLIST --> TRANS1
    TRANLIST --> TRANS2
    TRANLIST --> TRANSN
```

## 8. Design Considerations

### 8.1 Architecture Decisions

| Decision | Justification |
|----------|---------------|
| **No external dependencies** | Simplifies installation and distribution |
| **Tkinter for GUI** | Cross-platform, included in Python |
| **Companion classes** | Separates business logic from UI |
| **Pure functions in utils** | Facilitates unit testing |
| **Wizard pattern** | Guides user through complex process |
| **Dataclasses for DTOs** | Clean code and type hints |

### 8.2 Trade-offs

| Choice | Benefit | Cost |
|--------|---------|------|
| **Python** | Portability, readability | Performance (not critical) |
| **Tkinter** | No dependencies | Less modern interface |
| **OFX 1.0.2** | Wide compatibility | Verbose format |
| **Single-file executable** | Easy distribution | File size |

---

*Back to [Main Documentation](README.md)*
