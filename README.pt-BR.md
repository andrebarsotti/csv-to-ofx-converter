# Conversor de CSV para OFX - Edição Aprimorada

> 🇺🇸 **[Read in English](README.md)**

Uma aplicação Python completa que converte arquivos CSV (Comma-Separated Values) para o formato OFX (Open Financial Exchange), com suporte total para formatos bancários brasileiros. **Versão 3.2.0** apresenta uma interface completamente redesenhada em formato de assistente com recursos avançados incluindo gerenciamento de saldos e visualização prévia.

## ⚠️ Aviso Importante

**Esta aplicação foi desenvolvida com assistência de Inteligência Artificial (IA).**

- O código foi gerado e revisado com o auxílio de modelos de IA
- Embora tenha sido testado extensivamente, recomenda-se validação adicional para uso em produção
- **Sempre mantenha backups dos seus arquivos CSV originais**
- Revise os arquivos OFX gerados antes de importá-los em seu software financeiro
- Use por sua conta e risco - teste completamente antes de uso em dados importantes
- Contribuições e melhorias da comunidade são bem-vindas

## ✨ Novidades na Versão 2.1

**Funcionalidades de Gerenciamento de Saldos:**

1. **💰 Saldo Inicial**: Especifique o saldo inicial para seu extrato (opcional)
2. **📊 Visualização de Saldos**: Nova Etapa 7 mostrando resumo completo de saldos antes da exportação
3. **🔢 Saldo Manual/Automático**: Alterne entre cálculo automático e manual do saldo final
4. **📱 Layout Responsivo**: Janela agora redimensionável com melhor utilização do espaço

**Funcionalidades Principais Anteriores (Versão 2.0):**

1. **🎯 Interface em Assistente Passo a Passo**: Processo guiado em múltiplas etapas com indicadores de progresso claros
2. **👀 Visualização de Dados CSV**: Veja seus dados em uma tabela antes de converter
3. **🔄 Inversão de Valores**: Troque facilmente débitos e créditos quando necessário
4. **📝 Descrições Compostas**: Combine múltiplas colunas para criar descrições de transações
5. **✅ Tratamento Aprimorado de Datas**: Mantenha, ajuste ou exclua transações fora do intervalo

## Funcionalidades

### Funcionalidades Principais
- **Interface em Assistente Passo a Passo**: Processo guiado intuitivo em 7 etapas com acompanhamento visual de progresso
- **Visualização de Dados CSV**: Visualize dados importados em formato tabular antes da conversão
- **Suporte Flexível a CSV**:
  - Formato padrão (delimitador vírgula, separador decimal ponto)
  - Formato brasileiro (delimitador ponto-e-vírgula, separador decimal vírgula)
  - Arquivos delimitados por tabulação
- **Mapeamento Inteligente de Colunas**: Mapeie qualquer coluna CSV para campos OFX
- **Descrições Compostas**: Combine até 4 colunas para criar descrições ricas de transações
- **IDs de Transação Determinísticos**: As mesmas transações recebem IDs idênticos em exportações repetidas, permitindo reconciliação confiável ao regerar arquivos
- **Inversão de Valores**: Opção para inverter todos os valores de transação (trocar débitos e créditos)
- **Detecção Automática de Tipo**: Infere débito/crédito pelo sinal do valor
- **Múltiplos Formatos de Data**: Suporta vários formatos de data (DD/MM/AAAA, AAAA-MM-DD, etc.)
- **Múltiplas Moedas**: Suporte para BRL, USD, EUR, GBP

### Funcionalidades Avançadas
- **Validação de Data**: Valide transações contra o período da fatura do cartão de crédito com três opções:
  - **Manter**: Use a data original como está
  - **Ajustar**: Mova para o limite válido mais próximo (data inicial ou final)
  - **Excluir**: Remova a transação da saída
- **Tratamento de Erros**: Tratamento elegante de erros com log detalhado
- **Testes Abrangentes**: Suite completa de testes unitários incluída

## Requisitos

- Python 3.7 ou superior
- Tkinter (geralmente incluído com Python)

Nenhuma dependência externa necessária! Todas as bibliotecas usadas fazem parte da biblioteca padrão do Python.

## Instalação

### Opção 1: Baixar Executável Pré-compilado (Recomendado)

**Não requer instalação do Python!**

1. Acesse a [página de Releases](https://github.com/YOUR_USERNAME/conversor-csv-ofx/releases)
2. Baixe a versão mais recente para seu sistema operacional:
   - **Windows**: `csv-to-ofx-converter-windows-x64.exe`
   - **macOS**: `csv-to-ofx-converter-macos-x64`
   - **Linux**: `csv-to-ofx-converter-linux-x64`
3. Siga as instruções específicas da plataforma nas notas de lançamento

#### Windows
- Baixe e clique duas vezes no arquivo `.exe`
- Se o Windows mostrar um aviso de segurança, clique em "Mais informações" e depois "Executar assim mesmo"

#### macOS
```bash
chmod +x csv-to-ofx-converter-macos-x64
./csv-to-ofx-converter-macos-x64
```
- Se o macOS bloquear: Preferências do Sistema > Segurança e Privacidade > Permitir

#### Linux
```bash
chmod +x csv-to-ofx-converter-linux-x64
./csv-to-ofx-converter-linux-x64
```

### Opção 2: Executar do Código Fonte

**Requer Python 3.7+**

1. **Clone ou baixe este repositório**:
```bash
git clone https://github.com/YOUR_USERNAME/conversor-csv-ofx.git
cd conversor-csv-ofx
```

2. **Verifique a instalação do Python**:
```bash
python3 --version
```

3. **Execute a aplicação**:
```bash
python3 main.py
```

### Opção 3: Compilar do Código Fonte

**Para desenvolvedores que desejam criar seu próprio executável**

1. **Instale o PyInstaller**:
```bash
pip install pyinstaller
```

2. **Compile o executável**:

   **Linux/macOS**:
   ```bash
   ./build.sh
   ```

   **Windows**:
   ```cmd
   build.bat
   ```

3. **Encontre o executável no diretório `dist/`**

## Uso

### Executando a Aplicação

**Método 1 - Aplicação com Interface Gráfica**:
```bash
python3 src/csv_to_ofx_converter.py
```

Isso abrirá a **Interface Aprimorada em Assistente** que guia você através de um processo de 7 etapas:

1. **Seleção de Arquivo** - Selecione seu arquivo CSV
2. **Formato CSV** - Configure delimitador e separador decimal
3. **Visualização de Dados** - Veja seus dados em uma tabela (até 100 linhas)
4. **Configuração OFX** - Defina detalhes da conta, moeda e saldo inicial
5. **Mapeamento de Campos** - Mapeie colunas e configure descrições compostas
6. **Opções Avançadas** - Inversão de valores e validação de data
7. **Visualização de Saldos** - Revise saldos e transações antes da exportação

### Guia Passo a Passo do Assistente

#### Etapa 1: Seleção de Arquivo
Clique no botão "Browse..." para selecionar seu arquivo CSV. O arquivo deve ter uma linha de cabeçalho com nomes de colunas.

#### Etapa 2: Configurar Formato CSV

Escolha o formato que corresponde ao seu arquivo CSV:

**Formato Padrão** (internacional):
- Delimitador: Vírgula (,)
- Decimal: Ponto (.)
- Exemplo: `2025-10-22,100.50,Purchase`

**Formato Brasileiro**:
- Delimitador: Ponto-e-vírgula (;)
- Decimal: Vírgula (,)
- Exemplo: `22/10/2025;100,50;Compra`

**Formato Tabulação**:
- Delimitador: Tab
- Decimal: Ponto (.) ou Vírgula (,)

Clique em "Próximo" para continuar.

#### Etapa 3: Visualização de Dados

**Novo na Versão 2.0!**

Visualize seus dados CSV em um formato de tabela fácil de ler. Esta etapa permite que você:
- Verifique se o arquivo foi analisado corretamente
- Confirme se os nomes das colunas correspondem às suas expectativas
- Revise dados de amostra antes da conversão
- Use o botão "Recarregar Dados" se precisar alterar configurações de formato

A visualização mostra até 100 linhas para performance. Clique em "Próximo" para continuar.

#### Etapa 4: Configuração OFX

Configure as definições do arquivo de saída:

- **ID da Conta**: Seu identificador de conta (ex: número da conta) - *Opcional* (padrão: "UNKNOWN")
- **Nome do Banco**: Nome da sua instituição financeira (padrão: "CSV Import")
- **Moeda**: Escolha entre:
  - BRL (Real Brasileiro)
  - USD (Dólar Americano)
  - EUR (Euro)
  - GBP (Libra Esterlina)
- **Saldo Inicial**: Saldo inicial do seu extrato - *Opcional* (padrão: 0,00)
  - Suporta valores positivos e negativos
  - Usado para calcular o saldo final automaticamente

Clique em "Próximo" para prosseguir ao mapeamento de campos.

#### Etapa 5: Mapeamento de Campos

Mapeie suas colunas CSV para os campos de transação OFX:

| Campo OFX | Obrigatório | Descrição |
|-----------|-------------|-----------|
| Date | Sim | Data da transação |
| Amount | Sim | Valor da transação (positivo ou negativo) |
| Description | Não* | Descrição da transação |
| Type | Não | Tipo de transação: DEBIT ou CREDIT |
| ID | Não | Identificador único da transação |

**\*Nota**: Description é obrigatória, mas você pode usar um mapeamento de coluna única OU o recurso de descrição composta (veja abaixo).

##### Recurso de Descrição Composta

**Novo na Versão 2.0!**

Combine múltiplas colunas CSV para criar descrições ricas de transações:

1. Selecione até 4 colunas para combinar
2. Escolha um separador:
   - Espaço: `Coluna1 Coluna2 Coluna3`
   - Traço (−): `Coluna1 - Coluna2 - Coluna3`
   - Vírgula (,): `Coluna1, Coluna2, Coluna3`
   - Barra (|): `Coluna1 | Coluna2 | Coluna3`

**Exemplo**:
Se seu CSV tem colunas `categoria`, `estabelecimento` e `observacoes`:
- Coluna 1: `categoria`
- Coluna 2: `estabelecimento`
- Coluna 3: `observacoes`
- Separador: Traço (-)
- Resultado: `Alimentação - Restaurante ABC - Almoço de negócios`

Isso é útil para criar descrições detalhadas a partir de múltiplos campos de dados, especialmente comum em exportações bancárias que separam informações de transação em várias colunas.

Clique em "Próximo" para prosseguir às opções avançadas.

#### Etapa 6: Opções Avançadas

Configure recursos avançados opcionais:

##### Inversão de Valores

**Novo na Versão 2.0!**

Marque a caixa "Inverter todos os valores de transação" se:
- Seu CSV mostra débitos como positivos e créditos como negativos (ou vice-versa)
- Você precisa inverter o sinal de todos os valores

Isso multiplicará todos os valores de transação por -1 e trocará os tipos DEBIT/CREDIT.

**Exemplo**: Um CSV com `100,50` (positivo) que deveria ser um débito se tornará `-100,50` (DEBIT).

##### Validação de Data de Transação

**Aprimorado na Versão 2.0!**

Para faturas de cartão de crédito, valide que as transações estão dentro do período da fatura:

1. Marque "Habilitar validação de data para período da fatura do cartão de crédito"
2. Insira a **Data Inicial** (ex: `2025-10-01` ou `01/10/2025`)
3. Insira a **Data Final** (ex: `2025-10-31` ou `31/10/2025`)

Quando habilitado, para cada transação fora do intervalo de datas, você verá um diálogo com **três opções**:

- **Manter data original**: Use a data como está, mesmo estando fora do intervalo
- **Ajustar para limite**: Mova a data para o limite válido mais próximo (data inicial ou final)
- **Excluir transação**: Remova a transação do arquivo OFX

**Benefícios**:
- Garante precisão do período da fatura
- Ajuda a identificar transações mal posicionadas
- Mantém consistência cronológica
- Fornece controle total sobre casos limítrofes

**Exemplo de Diálogo**:
```
Transação #5 está fora do intervalo!
Data da Transação: 02/11/2025
Descrição: Restaurante ABC
Intervalo Válido: 2025-10-01 a 2025-10-31
Status: Esta transação ocorre APÓS a data final

Como você gostaria de lidar com esta transação?
[Manter data original] [Ajustar para data final] [Excluir esta transação]
```

Uma vez configurado, clique em **"Próximo"** para prosseguir à etapa de visualização de saldos.

#### Etapa 7: Visualização de Saldos e Confirmação

**Novo na Versão 2.1.0!**

Antes de gerar o arquivo OFX, revise um resumo completo de saldos e visualização de transações:

##### Resumo de Saldos

A seção de resumo de saldos exibe:

- **Saldo Inicial**: O saldo inicial que você especificou na Etapa 4 (padrão: 0,00)
- **Total de Créditos**: Soma de todas as transações positivas (exibido em verde)
- **Total de Débitos**: Soma de todas as transações negativas (exibido em vermelho)
- **Saldo Final**: Saldo final calculado ou inserido manualmente (exibido em azul)
- **Contagem de Transações**: Número total de transações a serem exportadas

**Importante**: Todos os cálculos respeitam automaticamente a configuração de inversão de valores da Etapa 6.

##### Modos de Saldo Final

Você pode escolher entre dois modos para o saldo final:

**Modo Auto-Cálculo (Padrão)**:
- Calcula automaticamente: Saldo Inicial + Soma de todas as transações
- Campo de saldo final desabilitado (somente leitura)
- Garante precisão matemática

**Modo Entrada Manual**:
- Insira seu próprio valor de saldo final
- Útil quando você precisa corresponder a um saldo de extrato específico
- Ative desmarcando "Calcular saldo final automaticamente"

##### Visualização de Transações

Visualize as primeiras 20 transações em uma tabela rolável mostrando:
- Número da transação
- Data
- Tipo (DEBIT/CREDIT)
- Valor
- Descrição

Esta visualização ajuda você a verificar:
- Formatos de data estão corretos
- Tipos de transação estão atribuídos corretamente
- Valores têm sinais corretos
- Descrições estão formatadas como esperado
- Inversão de valores está funcionando corretamente (se habilitada)

##### Finalizando

Após revisar o resumo de saldos e a visualização de transações:
- Clique em **"Converter para OFX"** para gerar o arquivo OFX final
- Um diálogo de salvar arquivo aparecerá para escolher o local de saída
- O log exibirá estatísticas de conversão e confirmará o sucesso

### Navegação

- **Botão Voltar**: Vá para a etapa anterior
- **Botão Próximo**: Prossiga para a próxima etapa (valida a etapa atual)
- **Botão Converter para OFX**: Aparece na última etapa
- **Botão Limpar Tudo**: Redefine todo o formulário e retorna à Etapa 1
- **Indicador de progresso**: Mostra a etapa atual e etapas concluídas

## Exemplos de Formato CSV

### Exemplo 1: Formato Padrão
```csv
date,amount,description,type
2025-10-01,-100.50,Grocery Store,DEBIT
2025-10-02,-50.25,Gas Station,DEBIT
2025-10-03,1000.00,Salary,CREDIT
```

### Exemplo 2: Formato Brasileiro
```csv
data;valor;descricao;tipo
01/10/2025;-100,50;Supermercado;DEBIT
02/10/2025;-50,25;Posto de Gasolina;DEBIT
03/10/2025;1.000,00;Salário;CREDIT
```

### Exemplo 3: Formato de Descrição Composta
```csv
date,category,merchant,notes,amount
2025-10-01,Alimentação,Restaurante ABC,Almoço de negócios,-75.50
2025-10-02,Transporte,Uber,Viagem para aeroporto,-25.00
2025-10-03,Salário,Empresa XYZ,Pagamento mensal,3000.00
```

**Mapeamento para Exemplo 3**:
- Date → `date`
- Amount → `amount`
- Descrição Composta:
  - Coluna 1: `category`
  - Coluna 2: `merchant`
  - Coluna 3: `notes`
  - Separador: Traço (-)
- Resultado: `Alimentação - Restaurante ABC - Almoço de negócios`

### Exemplo 4: Formato Mínimo (Sem Coluna de Tipo)
```csv
date,amount,description
2025-10-01,-100.50,Grocery Store
2025-10-02,-50.25,Gas Station
2025-10-03,1000.00,Salary
```

### Exemplo 5: Formato de Exportação do Nubank
```csv
date,category,title,amount
01/10/2025,alimentação,Supermercado ABC,-100,50
02/10/2025,transporte,Uber,-25,00
05/10/2025,outros,Pagamento recebido,1.500,00
```

**Mapeamento de Colunas para Nubank**:
- Date → `date`
- Amount → `amount`
- Opção A: Description → `title`
- Opção B: Descrição Composta:
  - Coluna 1: `category`
  - Coluna 2: `title`
  - Separador: Traço (-)

### Exemplo 6: Usando Inversão de Valores

**CSV com valores invertidos:**
```csv
date,amount,description
2025-10-01,100.50,Despesa (deveria ser negativa)
2025-10-02,50.25,Despesa (deveria ser negativa)
2025-10-03,-1000.00,Receita (deveria ser positiva)
```

Habilite "Inverter todos os valores de transação" para corrigir os sinais:
- `100,50` se torna `-100,50` (DEBIT)
- `50,25` se torna `-50,25` (DEBIT)
- `-1000,00` se torna `1000,00` (CREDIT)

### Exemplo 7: Usando Validação de Data

**CSV com datas mistas:**
```csv
date,amount,description
28/09/2025,-50.00,Transação antes do período
01/10/2025,-100.50,Transação válida 1
15/10/2025,-75.25,Transação válida 2
31/10/2025,-200.00,Transação válida 3
02/11/2025,-30.00,Transação após o período
```

**Com Validação de Data habilitada (Início: 01/10/2025, Fim: 31/10/2025):**
- Transação de 28/09/2025: Escolha Manter / Ajustar para 01/10/2025 / Excluir
- Transações de 01/10/2025 a 31/10/2025: Processadas normalmente
- Transação de 02/11/2025: Escolha Manter / Ajustar para 31/10/2025 / Excluir

## Formatos de Data Suportados

O conversor reconhece automaticamente estes formatos de data:

- `AAAA-MM-DD` (2025-10-22)
- `DD/MM/AAAA` (22/10/2025)
- `MM/DD/AAAA` (10/22/2025)
- `AAAA/MM/DD` (2025/10/22)
- `DD-MM-AAAA` (22-10-2025)
- `DD.MM.AAAA` (22.10.2025)
- `AAAAMMDD` (20251022)

## Formato de Saída OFX

O arquivo OFX gerado segue a especificação OFX 1.0.2 (formato SGML) e inclui:

- **Cabeçalho**: Versão OFX, codificação, informações de charset
- **Mensagem de Sign-on**: Informações do banco e timestamp do servidor
- **Extrato**: Detalhes da conta e lista de transações
- **Transações**: Cada transação com:
  - Tipo (DEBIT/CREDIT)
  - Data (formato OFX: AAAAMMDD000000)
  - Valor (com sinal apropriado)
  - ID único (UUID)
  - Descrição/memo
- **Saldo**: Saldo final da conta

### Exemplo de Saída OFX
```xml
OFXHEADER:100
DATA:OFXSGML
VERSION:102
...
<OFX>
  <SIGNONMSGSRSV1>
    <SONRS>
      ...
      <FI>
        <ORG>CSV Import</ORG>
      </FI>
    </SONRS>
  </SIGNONMSGSRSV1>
  <CREDITCARDMSGSRSV1>
    <CCSTMTTRNRS>
      ...
      <CCSTMTRS>
        <CURDEF>BRL</CURDEF>
        ...
        <BANKTRANLIST>
          <STMTTRN>
            <TRNTYPE>DEBIT</TRNTYPE>
            <DTPOSTED>20251001000000[-3:BRT]</DTPOSTED>
            <TRNAMT>-100.50</TRNAMT>
            <FITID>uuid-here</FITID>
            <MEMO>Purchase description</MEMO>
          </STMTTRN>
          ...
        </BANKTRANLIST>
      </CCSTMTRS>
    </CCSTMTTRNRS>
  </CREDITCARDMSGSRSV1>
</OFX>
```

## Executando os Testes

O projeto inclui testes unitários abrangentes (94 testes) organizados em módulos separados:
- **test_csv_parser.py**: Análise de CSV com diferentes formatos e normalização de valores (8 testes)
- **test_ofx_generator.py**: Geração de OFX, inversão de valores e manipulação de transações (21 testes)
- **test_date_validator.py**: Validação de data e tratamento de limites (12 testes)
- **test_transaction_utils.py**: Funções utilitárias de transação (68 testes)
- **test_integration.py**: Fluxos completos de ponta a ponta e descrições compostas (11 testes)

### Executar todos os testes (recomendado):
```bash
python3 -m unittest discover tests
```

### Executar com saída detalhada:
```bash
python3 -m unittest discover tests -v
```

### Executar módulo de teste específico:
```bash
python3 -m unittest tests.test_csv_parser
python3 -m unittest tests.test_ofx_generator
python3 -m unittest tests.test_date_validator
python3 -m unittest tests.test_integration
```

### Executar classe de teste específica:
```bash
python3 -m unittest tests.test_csv_parser.TestCSVParser
python3 -m unittest tests.test_ofx_generator.TestOFXGenerator
python3 -m unittest tests.test_date_validator.TestDateValidator
python3 -m unittest tests.test_integration.TestIntegration
```

### Alternativa - executar usando script de conveniência:
```bash
python3 tests/run_all_tests.py
```

### Saída esperada:
```
test_add_credit_transaction (tests.test_ofx_generator.TestOFXGenerator) ... ok
test_add_transaction (tests.test_ofx_generator.TestOFXGenerator) ... ok
test_brazilian_csv_parsing (tests.test_csv_parser.TestCSVParser) ... ok
test_date_validator_initialization (tests.test_date_validator.TestDateValidator) ... ok
test_is_within_range (tests.test_date_validator.TestDateValidator) ... ok
...
----------------------------------------------------------------------
Ran 44 tests in 0.XXXs

OK
```

## Log

A aplicação gera logs detalhados em `csv_to_ofx_converter.log`:

```
2025-11-08 12:34:56 - __main__ - INFO - GUI initialized with wizard interface
2025-11-08 12:35:01 - __main__ - INFO - Parsed CSV: 150 rows, 4 columns
2025-11-08 12:35:05 - __main__ - INFO - Value inversion enabled - all amounts will be inverted
2025-11-08 12:35:10 - __main__ - INFO - OFX file generated: output.ofx (148 transactions)
```

## Solução de Problemas

### Problema: "CSV file has no headers"
**Solução**: Certifique-se de que seu arquivo CSV tem uma linha de cabeçalho com nomes de colunas.

### Problema: "Invalid amount format"
**Solução**: Verifique se a configuração do separador decimal corresponde ao formato do seu CSV.

### Problema: "Unrecognized date format"
**Solução**: Verifique se o formato da sua data é um dos formatos suportados. Você pode precisar reformatar suas datas no CSV.

### Problema: GUI não aparece
**Solução**: Certifique-se de que o Tkinter está instalado:
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# macOS (geralmente incluído)
# Windows (geralmente incluído)
```

### Problema: Caracteres aparecem corrompidos (problemas de codificação)
**Solução**: A aplicação usa codificação UTF-8. Certifique-se de que seu arquivo CSV está salvo em formato UTF-8.

### Problema: Visualização mostra dados incorretos
**Solução**: Volte à Etapa 2 e verifique as configurações de delimitador e separador decimal. Use o botão "Recarregar Dados" após alterar as configurações.

## Arquitetura

### Estrutura do Código

```
csv_to_ofx_converter.py
├── CSVParser          # Manipula análise de arquivo CSV
│   ├── parse_file()          # Analisa CSV e extrai dados
│   └── normalize_amount()    # Converte valores para float
│
├── OFXGenerator       # Gera arquivos OFX
│   ├── __init__(invert_values)   # Inicializa com opção de inversão
│   ├── add_transaction()     # Adiciona transação à fila
│   ├── _parse_date()         # Analisa e formata datas
│   └── generate()            # Cria arquivo OFX
│
├── DateValidator      # Valida datas de transação
│   ├── is_within_range()     # Verifica se a data é válida
│   ├── get_date_status()     # Determina antes/dentro/depois
│   └── adjust_date_to_boundary()  # Ajusta datas fora do intervalo
│
└── ConverterGUI       # Interface Tkinter em estilo de assistente
    ├── _create_widgets()     # Constrói interface do assistente
    ├── _show_step()          # Exibe etapa específica
    ├── _create_step_*()      # Cria UI de cada etapa
    ├── _load_csv_data()      # Carrega e analisa CSV
    ├── _populate_preview()   # Preenche tabela de visualização
    ├── _convert()            # Realiza conversão
    ├── _handle_out_of_range_transaction()  # Trata problemas de data
    └── _log()                # Exibe mensagens de log
```

### Fluxo do Assistente

```
Etapa 1: Seleção de Arquivo
    ↓
Etapa 2: Configuração de Formato CSV
    ↓
Etapa 3: Visualização de Dados (NOVO!)
    ↓ (CSV carregado automaticamente)
Etapa 4: Configuração OFX + Saldo Inicial
    ↓
Etapa 5: Mapeamento de Campos + Descrição Composta (NOVO!)
    ↓
Etapa 6: Opções Avançadas (Inversão de Valores + Validação de Data)
    ↓
Etapa 7: Visualização de Saldos e Confirmação (NOVO na v2.1!)
    ↓
Processo de Conversão
    ↓
Arquivo OFX Gerado
```

### Fluxo de Dados

```
Arquivo CSV → CSVParser → Exibição de Visualização → Mapeamento de Campos → Opções Avançadas → OFXGenerator → Arquivo OFX
    ↓            ↓            ↓                         ↓                    ↓                    ↓
  Cabeçalhos   Linhas    Treeview               Mapeamento do Usuário    Inversão de Valores  Transações
               Dados     (Etapa 3)              Descrição Composta       Validação de Data    Formatação
                                                                         (Manter/Ajustar/Excluir)
```

## Melhores Práticas

1. **Sempre revise seus dados CSV na visualização** (Etapa 3) antes da conversão
2. **Teste com um arquivo CSV pequeno** primeiro para verificar se os mapeamentos estão corretos
3. **Mantenha backups** dos seus arquivos CSV originais
4. **Use descrições compostas** quando tiver múltiplas colunas relacionadas para combinar
5. **Use inversão de valores** se seus valores tiverem o sinal errado em vez de editar manualmente o CSV
6. **Verifique os arquivos OFX** no seu software financeiro antes de importar grandes conjuntos de dados
7. **Use formatos de data consistentes** dentro de um único arquivo CSV
8. **Verifique os logs** se a conversão falhar ou produzir resultados inesperados
9. **Use validação de data** para garantir precisão do período da fatura para cartões de crédito

## Compatibilidade

### Testado Com
- Python 3.7, 3.8, 3.9, 3.10, 3.11
- Windows 10/11
- Ubuntu 20.04/22.04
- macOS 11+

### Compatibilidade com Software Financeiro
Os arquivos OFX gerados são compatíveis com:
- GnuCash
- Microsoft Money
- Quicken
- QuickBooks
- HomeBank
- KMyMoney
- A maioria dos softwares de contabilidade que suportam OFX 1.0.2

## Limitações

- Comprimento máximo de descrição: 255 caracteres (especificação OFX)
- Suporta formato de extrato de cartão de crédito (CREDITCARDMSGSRSV1)
- Não suporta contas de investimento ou transações complexas
- Uma conta por arquivo
- Visualização limitada às primeiras 100 linhas para performance

## Melhorias Futuras

Possíveis aprimoramentos para versões futuras:

1. **Suporte a Conta Bancária**: Adicionar suporte para contas corrente/poupança (BANKMSGSRSV1)
2. **Múltiplas Contas**: Suportar múltiplas contas em um único arquivo OFX
3. **Templates**: Salvar e carregar templates de mapeamento de colunas
4. **Processamento em Lote**: Converter múltiplos arquivos CSV de uma vez
5. **Auto-Detecção de CSV**: Detectar automaticamente formato CSV e formatos de data
6. **Categorias de Transação**: Suportar campos de categoria/classe OFX
7. **Contas de Investimento**: Suporte para ações, títulos e transações de investimento
8. **Suporte OFX 2.x**: Adicionar suporte para formato XML OFX mais recente
9. **Formatos de Data Personalizados**: Permitir que usuários especifiquem formatos de data personalizados
10. **Interface de Linha de Comando**: Adicionar CLI para scripts e automação
11. **Deduplicação de Transações**: Detectar e tratar transações duplicadas
12. **Transações Divididas**: Suporte para transações divididas/categorizadas
13. **Suporte Multi-idioma**: Internacionalização (i18n)
14. **Suporte a Excel**: Importação direta de arquivos .xlsx/.xls
15. **Ajuste de Data em Lote**: Opção para ajustar todas as datas fora do intervalo de uma vez sem diálogos

## Contribuindo

Contribuições são bem-vindas! Sinta-se livre para enviar pull requests ou abrir issues para bugs e solicitações de recursos.

## Licença

Licença MIT

Copyright (c) 2025 André Claudinei Barsotti Salvadeo

Veja o arquivo [LICENSE](LICENSE) para detalhes.

É concedida permissão, gratuitamente, a qualquer pessoa que obtenha uma cópia deste software e dos arquivos de documentação associados (o "Software"), para lidar com o Software sem restrição, incluindo, sem limitação, os direitos de usar, copiar, modificar, mesclar, publicar, distribuir, sublicenciar e/ou vender cópias do Software, e permitir que as pessoas a quem o Software é fornecido o façam, sob as seguintes condições:

O aviso de copyright acima e este aviso de permissão devem ser incluídos em todas as cópias ou partes substanciais do Software.

O SOFTWARE É FORNECIDO "COMO ESTÁ", SEM GARANTIA DE QUALQUER TIPO, EXPRESSA OU IMPLÍCITA, INCLUINDO, MAS NÃO SE LIMITANDO ÀS GARANTIAS DE COMERCIALIZAÇÃO, ADEQUAÇÃO A UM DETERMINADO FIM E NÃO VIOLAÇÃO. EM NENHUM CASO OS AUTORES OU DETENTORES DOS DIREITOS AUTORAIS SERÃO RESPONSÁVEIS POR QUALQUER RECLAMAÇÃO, DANOS OU OUTRA RESPONSABILIDADE, SEJA EM AÇÃO DE CONTRATO, ATO ILÍCITO OU DE OUTRA FORMA, DECORRENTE DE, FORA DE OU EM CONEXÃO COM O SOFTWARE OU O USO OU OUTRAS NEGOCIAÇÕES NO SOFTWARE.

## Créditos

**Autor**: André Claudinei Barsotti Salvadeo

Desenvolvido com análise do formato de exportação OFX do Nubank para garantir compatibilidade com padrões bancários brasileiros.

**Nota**: Este projeto foi desenvolvido com assistência de IA. Embora funcional e testado, recomenda-se revisão e validação adequadas antes de uso em ambientes de produção.

## Suporte

Para problemas, questões ou sugestões:
1. Verifique a seção Solução de Problemas
2. Revise o arquivo de log (`csv_to_ofx_converter.log`)
3. Execute a suite de testes para verificar a instalação
4. Abra uma issue com informações detalhadas sobre seu problema

---

**Versão**: 3.2.0 - Edição Aprimorada
**Última Atualização**: Janeiro de 2026
**Autor**: André Claudinei Barsotti Salvadeo (com Assistência de IA)
**Licença**: MIT

## Histórico de Mudanças

### Versão 3.2.0 (Janeiro de 2026) - Nova Funcionalidade

**Nova Funcionalidade**: IDs de Transação Determinísticos (FITIDs)

Quando nenhuma coluna de ID é mapeada na Etapa 5 (Mapeamento de Campos), o sistema agora gera **FITIDs determinísticos** usando UUID v5 baseado nos dados da transação. Isso garante que a mesma transação sempre receba o mesmo FITID em múltiplas exportações.

**Principais Benefícios**:
1. **IDs Consistentes**: Mesmos dados de transação → mesmo FITID todas as vezes
2. **Reconciliação Confiável**: Softwares financeiros podem identificar corretamente transações duplicadas ao regerar arquivos
3. **Regeneração Parcial de Arquivos**: Exporte subconjuntos de transações sem criar entradas duplicadas
4. **Compatível com Versões Anteriores**: Colunas de ID explícitas ainda são respeitadas quando mapeadas

**Implementação Técnica**:
- Usa UUID v5 com namespace dedicado: `NAMESPACE_CSV_TO_OFX`
- Dados de entrada: data da transação (AAAAMMDD), valor (normalizado para 2 casas decimais), memo (normalizado), ID da conta
- Implementado em `transaction_utils.generate_deterministic_fitid()`
- Usado por `OFXGenerator.add_transaction()` quando `transaction_id=None`

**Impacto**: Melhora significativamente a experiência do usuário ao regerar arquivos OFX ou exportar múltiplos períodos, eliminando problemas de transações duplicadas em softwares financeiros.

**Notas de Atualização**: Atualização direta da v3.1.x. Sem alterações que quebrem compatibilidade. Toda funcionalidade existente preservada. Usuários com colunas de ID mapeadas não verão mudanças no comportamento.

**Suite de Testes**: Todos os 499 testes passando (26 novos testes adicionados para geração de FITID determinístico, incluindo testes de integração).

### Versão 3.1.3 (Janeiro de 2026) - Correção de Bug

**Correções de Bug**: Robustez aprimorada na validação de data nas Opções Avançadas (Etapa 6)

1. **Validação de Data Final**: Corrigido problema onde a data final poderia ser definida antes da data inicial
   - **Problema**: A validação de intervalo de datas verificava apenas o formato, mas permitia datas finais anteriores às datas iniciais
   - **Correção**: Adicionada verificação de comparação para garantir que data final >= data inicial
   - **Testes**: Adicionados 21 novos casos de teste em test_gui_utils.py

2. **Datas Calendáricas Impossíveis**: Corrigido tratamento de datas impossíveis como 31/02/2025
   - **Problema**: validate_date_format() verificava apenas intervalos gerais (dia<=31, mês<=12), permitindo datas impossíveis que causavam erro ValueError no datetime.strptime()
   - **Correção**: Envolvida a análise de data em try/except para retornar mensagens de erro claras ao invés de lançar exceções
   - **Testes**: Adicionados 14 novos casos de teste para cenários de datas impossíveis

**Impacto**: Melhora a confiabilidade do recurso de validação de data, prevenindo intervalos de datas inválidos e tratando graciosamente datas calendáricas impossíveis.

**Notas de Atualização**: Atualização direta da v3.1.2. Sem alterações que quebrem compatibilidade. Recomendado para todos os usuários que utilizam o recurso de validação de data.

**Suite de Testes**: Todos os 473 testes passando (5 novos testes adicionados para essas correções).

### Versão 3.1.2 (Dezembro de 2025) - Correção de Bug

**Correção de Bug**: Corrigido problema crítico com o comportamento do menu de contexto para transações fora do intervalo
- **Problema**: O menu de contexto (clique direito) não aparecia para transações marcadas como fora do intervalo quando a informação de validação de data não estava devidamente armazenada em cache
- **Causa Raiz**: Em casos raros, o cache de visualização de saldo não estava sendo compartilhado corretamente com o gerenciador de transações
- **Correção**: Melhorada a sincronização do cache em `BalancePreviewStep` para garantir que as informações de validação de data estejam sempre disponíveis
- **Testes**: Todos os 468 testes passam, verificando que a correção funciona corretamente

**Impacto**: Confiabilidade aprimorada da funcionalidade do menu de contexto na etapa de visualização de saldo.

**Notas de Atualização**: Atualização direta de v3.1.1. Sem mudanças incompatíveis. Recomendado para todos os usuários.

### Versão 3.1.1 (Dezembro de 2025) - Correção de Bug

**Correção de Bug**: Corrigido menu de contexto que não aparecia para transações fora do intervalo na etapa de visualização de saldo
- **Problema**: Menu de contexto (clique direito) não estava aparecendo para transações marcadas como fora do intervalo na etapa de visualização de saldo
- **Causa Raiz**: `_cached_balance_info` contendo informações de validação de data não estava sendo compartilhado com a GUI pai, impedindo o TransactionManager de acessá-lo
- **Correção**: Modificado `BalancePreviewStep` para compartilhar o cache com o pai em dois locais:
  - Linha 114: Após cálculo inicial de saldo em `_create_ui()`
  - Linha 450: Após recálculo em `_recalculate_balance()`
- **Testes**: Todos os 468 testes passam, incluindo validação específica em:
  - 29 testes em test_balance_preview_step.py
  - 26 testes em test_gui_transaction_manager.py

**Impacto**: Usuários agora podem acessar corretamente o menu de contexto para todas as transações na etapa de visualização de saldo, incluindo aquelas com problemas de validação de data.

**Notas de Atualização**: Atualização direta de v3.1.0. Sem mudanças incompatíveis.

### Versão 3.1.0 (Novembro de 2025) - Lançamento de Refatoração Arquitetural

**Grande Refatoração: Extração de Etapas do Assistente**

- **Melhoria de Arquitetura**: Refatoração completa da implementação do assistente GUI
  - Extraídas todas as 7 etapas do assistente em classes de etapas separadas e reutilizáveis
  - Criada classe base abstrata WizardStep para ciclo de vida padronizado das etapas
  - Reduzido converter_gui.py de 1.400 linhas para 750 linhas (redução de 46%)
  - Melhorada manutenibilidade e testabilidade do código

- **Novas Classes de Etapas** (todas no pacote `src/gui_steps/`):
  - FileSelectionStep (Etapa 1): Seleção de arquivo com validação
  - CSVFormatStep (Etapa 2): Configuração de formato CSV
  - DataPreviewStep (Etapa 3): Visualização prévia de dados com Treeview
  - OFXConfigStep (Etapa 4): Configuração OFX
  - FieldMappingStep (Etapa 5): Mapeamento de campos com descrições compostas
  - AdvancedOptionsStep (Etapa 6): Opções avançadas e validação de datas
  - BalancePreviewStep (Etapa 7): Visualização prévia de saldo e gerenciamento de transações

- **Testes**: Suíte de testes abrangente expandida para 468 testes
  - Adicionados 206 novos testes de etapas GUI
  - Todos os testes passando com zero regressões
  - Mantida 100% de compatibilidade retroativa

- **Qualidade de Código**:
  - Arquitetura Grau A (aprovada para produção)
  - 100% de conformidade PEP8
  - Modularidade e extensibilidade aprimoradas
  - Melhor separação de responsabilidades

- **Benefícios**:
  - Mais fácil de manter e estender funcionalidades do assistente
  - Cada etapa testável independentemente
  - Organização e legibilidade do código melhoradas
  - Fundação para futuras melhorias do assistente

**Importante**: Este é um lançamento de refatoração sem mudanças visíveis ao usuário. Toda funcionalidade permanece idêntica à v3.0.x.

**Notas de Atualização**: Atualização direta de qualquer versão 3.0.x. Sem mudanças incompatíveis.

### Versão 3.0.1 (Novembro de 2025) - Melhorias de Qualidade de Código e Segurança

- **Correção de Segurança**: Substituída validação regex por métodos de string mais seguros
  - Eliminada vulnerabilidade potencial de backtracking catastrófico na validação de entrada numérica
  - Substituído padrão regex `r'^-?\d*\.?\d*$'` por operações eficientes de string
  - Atende à regra de segurança SonarQube python:S5852 (prevenção de DoS)
  - Mantém comportamento idêntico de validação com desempenho melhorado

- **Qualidade de Código**: Reduzida complexidade cognitiva na lógica do menu de contexto
  - Refatorado `_show_transaction_context_menu()` para melhor manutenibilidade
  - Extraída lógica aninhada complexa para métodos auxiliares separados
  - Adicionados `_close_existing_context_menu()`, `_get_selected_row_info()` e `_get_date_status_for_row()`
  - Atende à regra SonarQube python:S3776 (complexidade cognitiva)
  - Melhorada testabilidade do código e separação de responsabilidades

- **Qualidade de Código**: Melhorado tratamento de exceções e logging
  - Substituídas cláusulas `except:` genéricas por tipos específicos de exceção
  - Adicionado logging apropriado de erros em converter_gui.py
  - Melhores mensagens de erro para debugging e troubleshooting

- **Documentação**: Atualizada informação de cobertura de testes
  - Suíte de testes agora inclui 94 testes abrangentes (antes eram 44)
  - Todos os testes passando com cobertura melhorada

### Versão 3.0.0 (Novembro de 2025) - Melhorias Importantes de Usabilidade e Fluxo de Trabalho

- **Melhoria Importante**: Visualização e Gerenciamento de Saldos Aprimorados (Etapa 7)
  - **Saldo Inicial Relocado**: Movido da Etapa 4 para Etapa 7 para melhor fluxo de trabalho
  - **Recálculo de Saldo em Tempo Real**: Recalcula automaticamente o saldo final quando o saldo inicial muda
  - **Visualizar Todas as Transações**: Preview agora mostra TODAS as transações (ilimitado), não apenas as primeiras 20
  - **Lista de Transações Ordenável**: Transações sempre exibidas em ordem cronológica (mais antiga para mais nova)
  - **Gerenciamento Interativo de Transações**: Excluir qualquer transação diretamente do preview
  - **Resumo de Saldos Aprimorado**: Visualização mais clara de saldo inicial, créditos, débitos e saldo final

- **Melhoria Importante**: Fluxo de Trabalho de Validação de Data Proativa
  - **Ações de Data Baseadas no Preview**: Lidar com datas fora do intervalo na Etapa 7 preview em vez de durante a conversão
  - **Menu de Contexto para Ações de Data**: Clique com botão direito em transações para escolher Manter/Ajustar/Excluir
  - **Padrões Inteligentes**: Transações antes da data inicial automaticamente padronizam para "Ajustar ao limite"
  - **Indicadores Visuais**: Marcação clara de transações com problemas de data no preview
  - **Sem Interrupções**: Processo de conversão suave sem prompts de diálogo
  - **Controle Total**: Revisar e decidir todas as ações de data antes de exportar

- **Melhoria Importante**: Exclusão Interativa de Transações
  - **Excluir do Preview**: Excluir qualquer transação via menu de contexto na Etapa 7
  - **Feedback Visual**: Transações excluídas removidas imediatamente da visualização
  - **Atualizações de Saldo**: Recálculo automático de totais após exclusões
  - **Opção de Restaurar**: Capacidade de restaurar transações excluídas antes da exportação final
  - **Exportação Limpa**: Apenas transações selecionadas incluídas no arquivo OFX final

- **Melhoria**: Validação de Entrada Aprimorada
  - **Campos Somente Numéricos**: Campos de saldo (inicial, final manual) aceitam apenas números durante a digitação
  - **Validação em Tempo Real**: Caracteres inválidos rejeitados imediatamente, não após submissão
  - **Aplicação de Formato de Data**: Campos de data (intervalo de validação) aceitam apenas formato DD/MM/AAAA
  - **Auto-formatação**: Inserção automática de barras em campos de data conforme você digita
  - **Inteligência de Cursor**: Posicionamento adequado do cursor durante auto-formatação
  - **Amigável ao Usuário**: Não é necessário corrigir erros de formatação após entrada

- **Correção de Bug**: Auto-formatação de entrada de datas funciona corretamente
  - Corrigido problema crítico onde digitar datas exigia inserir dígitos duas vezes após as barras
  - Formatação de data completamente reescrita com rastreamento adequado da posição do cursor
  - Agora formata corretamente DD/MM/AAAA sem confusão (ex: "12/10" não se torna mais "12/01")

- **Correção de Bug**: Botões de navegação mantêm posição correta
  - Corrigido bug de reposicionamento de botões que ocorria após Etapa 7 ou ao usar Limpar Tudo
  - Botões agora aparecem consistentemente na ordem: Voltar → Avançar/Converter → Limpar Tudo

- **Correção de Bug**: Melhorias no menu de contexto
  - Removidas opções duplicadas de exclusão (não mais "Excluir" + "Deletar Selecionados")
  - Menu fecha adequadamente ao clicar fora
  - Melhor feedback visual para seleções

- **Nova Funcionalidade**: Suporte a DPI Awareness no Windows
  - Configuração automática de DPI awareness para displays Windows de alta resolução
  - Suporta DPI por monitor (Windows 8.1+) e DPI de sistema (Windows 7/8.0)
  - Previne texto borrado em telas de alto DPI (escala 125%, 150%, 200%)
  - Garante maximização correta da janela em monitores 4K
  - Sem impacto em sistemas Linux/macOS (seguro multiplataforma)

- **Testes**: Todos os 94 testes passando
  - Cobertura abrangente de testes para todas as funcionalidades
  - Compatibilidade multiplataforma verificada
  - Nenhuma regressão introduzida

**Importante**: Esta versão importante melhora significativamente o fluxo de trabalho do usuário com validação proativa de datas, preview ilimitado de transações e melhor gerenciamento de saldos. Atualização altamente recomendada.

### Versão 2.1.2 (Novembro de 2025) - Versão de Qualidade de Código

- **Qualidade de Código**: Corrigidos problemas de qualidade de código do SonarQube no converter_gui
  - Melhor organização e manutenibilidade do código
  - Melhor separação de responsabilidades
  - Padrões aprimorados de tratamento de erros
- **Refatoração**: Extraídas utilitários de transação para módulo separado
  - Criado novo módulo `transaction_utils.py` com funções utilitárias puras
  - Funções sem dependências de UI, tornando-as totalmente testáveis
  - Melhor modularidade e reusabilidade do código
  - Adicionada cobertura abrangente de testes para utilitários
- **Testes**: Melhor organização da suíte de testes
  - Adicionado `test_transaction_utils.py` com 68 testes abrangentes
  - Total de testes agora em 94 (anteriormente documentado como 44)
  - Todos os testes passando com cobertura melhorada
  - Melhor estrutura e manutenibilidade dos testes
- **Documentação**: Atualizada documentação para refletir arquitetura atual
  - Contagens de testes e referências de comandos precisas
  - Descrições de estrutura de módulos atualizadas

### Versão 2.1.1 (Novembro de 2025) - Correção de Bug

- **Correção de Bug**: Corrigido análise de valores negativos com símbolos de moeda
  - Agora trata corretamente formatos como `-R$ 2.105,00` (negativo antes da moeda)
  - Suporta negativo depois da moeda: `R$ -2.105,00`
  - Adicionado suporte para notação com parênteses: `(R$ 100,50)` = `-100.50`
  - Funciona com formatos brasileiro (vírgula decimal) e padrão (ponto decimal)
- **Testes**: Adicionados 10 novos casos de teste para formatos de valores negativos
  - Testes para negativo com símbolos de moeda em várias posições
  - Testes para notação com parênteses (comum em contabilidade)
  - Todos os 44 testes passando
- **Melhoria**: Mensagens de erro aprimoradas para análise de valores

### Versão 2.1.0 (Novembro de 2025) - Funcionalidades de Gerenciamento de Saldos

- **Nova Funcionalidade**: Suporte a Saldo Inicial
  - Adicionar campo opcional de saldo inicial na Configuração OFX (Etapa 4)
  - Padrão 0,00 se não fornecido
  - Suporta valores positivos e negativos
  - Incluído na saída OFX (seção AVAILBAL)
- **Nova Funcionalidade**: Tela de Visualização de Saldos (Etapa 7)
  - Resumo completo de saldos antes da exportação:
    - Saldo Inicial
    - Total de Créditos (exibido em verde)
    - Total de Débitos (exibido em vermelho)
    - Saldo Final Calculado (exibido em azul)
    - Contagem de Transações
  - Visualização das primeiras 20 transações em tabela rolável
  - Todos os cálculos respeitam configuração de inversão de valores
- **Nova Funcionalidade**: Alternância de Saldo Final Manual/Automático
  - Modo automático (padrão): Calcula saldo final automaticamente
  - Modo manual: Permite entrada de saldo final personalizado
  - Atualizações de UI em tempo real ao alternar modos
  - Campo de entrada adequadamente desabilitado/habilitado baseado no modo
- **Melhoria**: Layout Responsivo
  - Janela agora redimensionável com tamanho mínimo de 900x700
  - Espaçamento otimizado para melhor utilização do espaço
  - Visualização de transações expande verticalmente com a janela
  - Resumo de saldos permanece compacto
- **Técnico**: Saída OFX Aprimorada
  - Ambos saldos inicial e final incluídos no OFX gerado
  - Saldo final na seção LEDGERBAL
  - Saldo inicial na seção AVAILBAL
  - Cálculo automático: saldo_inicial + soma(transações)
- **Testes**: 44 testes passando (6 novos testes para funcionalidades de saldo)
  - test_initial_balance_in_ofx_output
  - test_auto_calculated_final_balance
  - test_manual_final_balance
  - test_zero_initial_balance_default
  - test_negative_initial_balance
- 100% de compatibilidade retroativa mantida
- Todas as funcionalidades anteriores totalmente funcionais

### Versão 2.0.3 (Novembro de 2025) - Qualidade de Código e Refatoração

- **Qualidade de Código**: Integrado SonarCloud para monitoramento contínuo da qualidade do código
  - Adicionado workflow do SonarQube para análise automática de código
  - Configurado teste de cobertura de código
  - Resolvidos múltiplos problemas de qualidade de código identificados pelo SonarCloud
  - Corrigidas potenciais vulnerabilidades de segurança
- **Refatoração**: Grande reorganização do código para melhor manutenibilidade
  - Dividido código monolítico em módulos separados:
    - `csv_parser.py`: Funcionalidade de análise de CSV
    - `ofx_generator.py`: Geração de arquivos OFX
    - `date_validator.py`: Lógica de validação de data
    - `converter_gui.py`: Implementação da GUI
    - `constants.py`: Constantes compartilhadas
  - Adicionadas docstrings abrangentes de módulos e anotações de tipo
  - Melhorado tratamento de erros e logging
- **Correções de Bug**:
  - Resolvidos erros de importação e problemas com caracteres Unicode
  - Corrigidos nomes de executáveis no workflow de release (artefatos agora corretamente achatados)
  - Melhorada formatação da mensagem de sucesso na conclusão da conversão
- **Limpeza**:
  - Removidos resumos de implementação desatualizados
  - Removidas configurações do Claude do controle de versão
  - Limpeza de código redundante e comentado
- Todos os testes passando
- Melhor organização e manutenibilidade do código
- Sem mudanças funcionais - mesmas funcionalidades da v2.0.1

### Versão 2.0.1 (Novembro de 2025) - Correção de Bug
- **Correção de Bug**: Restaurado ID da Conta como campo opcional
  - ID da Conta foi incorretamente marcado como obrigatório na v2.0.0
  - Agora opcional com valor padrão "UNKNOWN" (mesmo que v1.1.0)
  - Atualizado texto de ajuda da UI e documentação
  - Compatibilidade retroativa totalmente restaurada
- Todos os 44 testes passando
- Sem mudanças incompatíveis - todas as funcionalidades da v2.0.0 mantidas

### Versão 2.0.0 (Novembro de 2025) - Edição Aprimorada
- **Grande Atualização**: Redesign completo da UI com interface em assistente passo a passo
  - Processo guiado em 7 etapas com indicadores visuais de progresso
  - Navegação clara com botões Voltar/Próximo
  - Validação de etapa antes de prosseguir
- **Nova Funcionalidade**: Visualização de Dados CSV
  - Visualize dados importados em formato tabular (widget Treeview)
  - Visualização de até 100 linhas antes da conversão
  - Botão de recarregar dados para alterações de formato
- **Nova Funcionalidade**: Descrições Compostas
  - Combine até 4 colunas CSV em descrições de transações
  - Escolha de separadores: Espaço, Traço, Vírgula, Barra
  - Perfeito para CSVs com informações de transação divididas
- **Nova Funcionalidade**: Inversão de Valores
  - Opção para inverter todos os valores de transação
  - Troca automaticamente tipos DEBIT/CREDIT
  - Útil para CSVs com convenções de sinal invertidas
- **Funcionalidade Aprimorada**: Validação de Data com Opção "Manter"
  - Adicionada "Manter data original" como terceira opção
  - Agora oferece: Manter / Ajustar / Excluir
  - Melhor rastreamento de estatísticas (datas fora do intervalo mantidas)
- **Melhorias na UI**:
  - Janela maior (1000x850) para melhor visibilidade
  - Layout e espaçamento melhorados
  - Melhores mensagens de erro e validação
  - Exibição de log de atividades aprimorada
  - Descrições claras de etapas e texto de ajuda
- **Documentação**: Reescrita completa do README com:
  - Instruções detalhadas das etapas do assistente
  - Exemplos de novos recursos
  - Diagramas atualizados
  - Guia de melhores práticas

### Versão 1.1.0 (Novembro de 2025)
- **Nova Funcionalidade**: Validação de data de fatura de cartão de crédito
  - Adicionada validação opcional de intervalo de data para transações
  - Diálogo interativo para lidar com transações fora do intervalo
  - Opções para ajustar datas para limites ou excluir transações
  - Cobertura abrangente de testes para validação de data
- GUI aprimorada com controles de validação de data
- Relatório de estatísticas melhorado (transações ajustadas/excluídas)
- Documentação atualizada com exemplos e melhores práticas

### Versão 1.0.0 (Novembro de 2025)
- Lançamento inicial
- Conversão de CSV para OFX com GUI
- Suporte para formatos CSV brasileiro e padrão
- Mapeamento flexível de colunas
- Suporte a múltiplas moedas
