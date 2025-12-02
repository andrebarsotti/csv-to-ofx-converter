# Arquitetura do Sistema

## 1. Visão Geral da Arquitetura

O **CSV to OFX Converter** segue uma arquitetura em camadas com separação clara de responsabilidades. A aplicação utiliza o padrão **Model-View-Controller (MVC)** adaptado, com ênfase em:

- **Separação de Concerns**: Lógica de negócio separada da interface gráfica
- **Dependency Injection**: Classes companion recebem a GUI como parâmetro
- **Testabilidade**: Funções puras e classes testáveis independentemente

### 1.1 Diagrama de Arquitetura de Camadas

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

## 2. Descrição das Camadas

### 2.1 Presentation Layer (Camada de Apresentação)

Responsável pela interface com o usuário através de widgets Tkinter.

| Componente | Responsabilidade |
|------------|------------------|
| **ConverterGUI** | Orquestrador principal do wizard, gerencia navegação e estado global |
| **WizardStep** | Classe base abstrata para todos os passos do wizard |
| **FileSelectionStep** | UI para seleção de arquivo CSV |
| **CSVFormatStep** | UI para configuração de formato CSV |
| **DataPreviewStep** | UI para prévia dos dados em tabela |
| **OFXConfigStep** | UI para configuração OFX (conta, banco, moeda) |
| **FieldMappingStep** | UI para mapeamento de campos CSV→OFX |
| **AdvancedOptionsStep** | UI para opções avançadas (inversão, validação) |
| **BalancePreviewStep** | UI para prévia de saldo e confirmação |

### 2.2 Application Layer (Camada de Aplicação)

Classes companion que orquestram operações de negócio sem dependência direta do Tkinter.

| Componente | Responsabilidade |
|------------|------------------|
| **BalanceManager** | Cálculos de saldo e prévia de transações |
| **ConversionHandler** | Orquestração do processo de conversão CSV→OFX |
| **TransactionManager** | Gestão de transações e menus de contexto |

### 2.3 Domain Layer (Camada de Domínio)

Classes core que implementam a lógica de negócio principal.

| Componente | Responsabilidade |
|------------|------------------|
| **CSVParser** | Parsing de arquivos CSV com suporte a múltiplos formatos |
| **OFXGenerator** | Geração de arquivos OFX 1.0.2 |
| **DateValidator** | Validação de datas contra período do extrato |

### 2.4 Utility Layer (Camada Utilitária)

Funções puras e constantes compartilhadas.

| Componente | Responsabilidade |
|------------|------------------|
| **transaction_utils** | Funções para processamento de transações |
| **gui_utils** | Funções utilitárias para operações GUI |
| **constants** | Constantes compartilhadas (NOT_MAPPED, NOT_SELECTED) |

## 3. Padrões de Projeto Utilizados

### 3.1 Wizard Pattern

A interface de usuário implementa o padrão Wizard para guiar o usuário através de um processo multi-etapas.

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

Classes companion recebem a GUI como parâmetro, permitindo testes com mocks.

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

A classe `WizardStep` utiliza o padrão Template Method para definir o esqueleto do algoritmo de validação.

```python
# Template Method em WizardStep
def validate(self) -> StepData:
    data = self._collect_data()      # Hook para subclasse
    is_valid, error = self._validate_data(data)  # Hook para subclasse
    return StepData(is_valid, error, data)
```

### 3.4 Data Transfer Objects (DTOs)

Uso de dataclasses para transferência de dados entre camadas.

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

## 4. Comunicação entre Componentes

### 4.1 Fluxo de Dados na Conversão

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
    
    loop Para cada linha CSV
        CH->>CSV: normalize_amount()
        CH->>DV: is_within_range(date)
        alt Data fora do período
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

### 4.2 Fluxo de Cálculo de Saldo

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
    
    loop Para cada linha não excluída
        BM->>CSV: normalize_amount()
        BM->>TU: build_transaction_description()
        BM->>TU: determine_transaction_type()
        BM->>BM: _process_preview_row()
    end
    
    BM-->>GUI: BalancePreviewData
    GUI-->>Step7: balance_info dict
```

## 5. Frameworks e Tecnologias

### 5.1 Stack Tecnológica

| Camada | Tecnologia | Justificativa |
|--------|------------|---------------|
| **Linguagem** | Python 3.7+ | Portabilidade, biblioteca padrão rica |
| **GUI** | Tkinter/ttk | Incluído na biblioteca padrão, cross-platform |
| **Testes** | unittest | Framework padrão, sem dependências externas |
| **Build** | PyInstaller | Geração de executáveis standalone |
| **Logging** | logging | Módulo padrão, configurável |

### 5.2 Dependências

A aplicação utiliza **apenas a biblioteca padrão do Python** para runtime, garantindo:
- Zero dependências externas
- Fácil instalação
- Portabilidade máxima

Dependências de desenvolvimento:
- **PyInstaller**: Apenas para build de executáveis

## 6. Diagrama de Componentes

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

## 7. Modelo de Dados

### 7.1 Estrutura de Transação

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

### 7.2 Estrutura do Arquivo OFX

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

## 8. Considerações de Design

### 8.1 Decisões de Arquitetura

| Decisão | Justificativa |
|---------|---------------|
| **Sem dependências externas** | Simplifica instalação e distribuição |
| **Tkinter para GUI** | Cross-platform, incluído no Python |
| **Classes companion** | Separa lógica de negócio de UI |
| **Funções puras em utils** | Facilita testes unitários |
| **Wizard pattern** | Guia usuário em processo complexo |
| **Dataclasses para DTOs** | Código limpo e type hints |

### 8.2 Trade-offs

| Escolha | Benefício | Custo |
|---------|-----------|-------|
| **Python** | Portabilidade, legibilidade | Performance (não crítico) |
| **Tkinter** | Sem dependências | Interface menos moderna |
| **OFX 1.0.2** | Compatibilidade ampla | Formato verboso |
| **Single-file executable** | Fácil distribuição | Tamanho do arquivo |

---

*Voltar para [Documentação Principal](README.md)*
