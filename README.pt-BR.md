# Conversor de CSV para OFX - Edição Aprimorada

> 🇺🇸 **[Read in English](README.md)**

Uma aplicação Python completa que converte arquivos CSV (Comma-Separated Values) para o formato OFX (Open Financial Exchange), com suporte total para formatos bancários brasileiros. **Versão 2.0** apresenta uma interface completamente redesenhada em formato de assistente com recursos avançados para melhor experiência do usuário.

## ⚠️ Aviso Importante

**Esta aplicação foi desenvolvida com assistência de Inteligência Artificial (IA).**

- O código foi gerado e revisado com o auxílio de modelos de IA
- Embora tenha sido testado extensivamente, recomenda-se validação adicional para uso em produção
- **Sempre mantenha backups dos seus arquivos CSV originais**
- Revise os arquivos OFX gerados antes de importá-los em seu software financeiro
- Use por sua conta e risco - teste completamente antes de uso em dados importantes
- Contribuições e melhorias da comunidade são bem-vindas

## ✨ Novidades na Versão 2.0

**Grandes Melhorias na Experiência do Usuário:**

1. **🎯 Interface em Assistente Passo a Passo**: Processo guiado em múltiplas etapas com indicadores de progresso claros
2. **👀 Visualização de Dados CSV**: Veja seus dados em uma tabela antes de converter
3. **🔄 Inversão de Valores**: Troque facilmente débitos e créditos quando necessário
4. **📝 Descrições Compostas**: Combine múltiplas colunas para criar descrições de transações
5. **✅ Tratamento Aprimorado de Datas**: Mantenha, ajuste ou exclua transações fora do intervalo (nova opção "Manter"!)

## Funcionalidades

### Funcionalidades Principais
- **Interface em Assistente Passo a Passo**: Processo guiado intuitivo em 6 etapas com acompanhamento visual de progresso
- **Visualização de Dados CSV**: Visualize dados importados em formato tabular antes da conversão
- **Suporte Flexível a CSV**:
  - Formato padrão (delimitador vírgula, separador decimal ponto)
  - Formato brasileiro (delimitador ponto-e-vírgula, separador decimal vírgula)
  - Arquivos delimitados por tabulação
- **Mapeamento Inteligente de Colunas**: Mapeie qualquer coluna CSV para campos OFX
- **Descrições Compostas**: Combine até 4 colunas para criar descrições ricas de transações
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

Isso abrirá a **Interface Aprimorada em Assistente** que guia você através de um processo de 6 etapas:

1. **Seleção de Arquivo** - Selecione seu arquivo CSV
2. **Formato CSV** - Configure delimitador e separador decimal
3. **Visualização de Dados** - Veja seus dados em uma tabela (até 100 linhas)
4. **Configuração OFX** - Defina detalhes da conta e moeda
5. **Mapeamento de Campos** - Mapeie colunas e configure descrições compostas
6. **Opções Avançadas** - Inversão de valores e validação de data

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

Uma vez configurado, clique em **"Converter para OFX"** para iniciar a conversão!

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

O projeto inclui testes unitários abrangentes cobrindo:
- Análise de CSV com diferentes formatos
- Normalização de valores
- Análise de datas
- Geração de OFX
- Inversão de valores
- Validação de data e tratamento de limites
- Descrições compostas
- Tratamento de erros
- Testes de integração

### Executar todos os testes:
```bash
python3 -m unittest tests.test_converter
```

### Executar com saída detalhada:
```bash
python3 -m unittest tests.test_converter -v
```

### Executar classe de teste específica:
```bash
python3 -m unittest tests.test_converter.TestCSVParser
python3 -m unittest tests.test_converter.TestOFXGenerator
python3 -m unittest tests.test_converter.TestDateValidator
```

### Saída esperada:
```
test_add_credit_transaction (tests.test_converter.TestOFXGenerator) ... ok
test_add_transaction (tests.test_converter.TestOFXGenerator) ... ok
test_brazilian_csv_parsing (tests.test_converter.TestCSVParser) ... ok
test_date_validator_initialization (tests.test_converter.TestDateValidator) ... ok
test_is_within_range (tests.test_converter.TestDateValidator) ... ok
...
----------------------------------------------------------------------
Ran 39+ tests in 0.XXXs

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
Etapa 4: Configuração OFX
    ↓
Etapa 5: Mapeamento de Campos + Descrição Composta (NOVO!)
    ↓
Etapa 6: Opções Avançadas (Inversão de Valores + Validação de Data)
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

**Versão**: 2.0.1 - Edição Aprimorada
**Última Atualização**: Novembro de 2025
**Autor**: André Claudinei Barsotti Salvadeo (com Assistência de IA)
**Licença**: MIT

## Histórico de Mudanças

### Versão 2.0.1 (Novembro de 2025) - Correção de Bug
- **Correção de Bug**: Restaurado ID da Conta como campo opcional
  - ID da Conta foi incorretamente marcado como obrigatório na v2.0.0
  - Agora opcional com valor padrão "UNKNOWN" (mesmo que v1.1.0)
  - Atualizado texto de ajuda da UI e documentação
  - Compatibilidade retroativa totalmente restaurada
- Todos os 39 testes passando
- Sem mudanças incompatíveis - todas as funcionalidades da v2.0.0 mantidas

### Versão 2.0.0 (Novembro de 2025) - Edição Aprimorada
- **Grande Atualização**: Redesign completo da UI com interface em assistente passo a passo
  - Processo guiado em 6 etapas com indicadores visuais de progresso
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
