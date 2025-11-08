# Conversor de CSV para OFX

> 🇺🇸 **[Read in English](README.md)**

Uma aplicação Python completa que converte arquivos CSV (Comma-Separated Values) para o formato OFX (Open Financial Exchange), com suporte total para formatos bancários brasileiros.

## ⚠️ Aviso Importante

**Esta aplicação foi desenvolvida com assistência de Inteligência Artificial (IA).**

- O código foi gerado e revisado com o auxílio de modelos de IA
- Embora tenha sido testado extensivamente, recomenda-se validação adicional para uso em produção
- **Sempre mantenha backups dos seus arquivos CSV originais**
- Revise os arquivos OFX gerados antes de importá-los em seu software financeiro
- Use por sua conta e risco - teste completamente antes de uso em dados importantes
- Contribuições e melhorias da comunidade são bem-vindas

## Funcionalidades

- **Interface Gráfica Intuitiva**: Interface amigável baseada em Tkinter
- **Suporte Flexível a CSV**:
  - Formato padrão (delimitador vírgula, separador decimal ponto)
  - Formato brasileiro (delimitador ponto-e-vírgula, separador decimal vírgula)
  - Arquivos delimitados por tabulação
- **Mapeamento Inteligente de Colunas**: Mapeie qualquer coluna CSV para campos OFX
- **Detecção Automática de Tipo**: Infere débito/crédito pelo sinal do valor
- **Múltiplos Formatos de Data**: Suporta vários formatos de data (DD/MM/AAAA, AAAA-MM-DD, etc.)
- **Múltiplas Moedas**: Suporte para BRL, USD, EUR, GBP
- **Validação de Data**: Valide transações contra o período da fatura do cartão de crédito com opções para ajustar ou excluir transações fora do intervalo
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
python3 src/csv_to_ofx_converter.py
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

Isso abrirá a interface gráfica onde você pode:
1. Selecionar seu arquivo CSV
2. Configurar o formato CSV (delimitador e separador decimal)
3. Definir a configuração OFX (ID da conta, nome do banco, moeda)
4. Mapear colunas CSV para campos OFX
5. Converter e salvar o arquivo OFX

### Guia Passo a Passo

#### 1. Selecionar Arquivo CSV
Clique no botão "Browse..." para selecionar seu arquivo CSV.

#### 2. Configurar Formato CSV

**Formato Padrão** (internacional):
- Delimitador: Vírgula (,)
- Decimal: Ponto (.)
- Exemplo: `2025-10-22,100.50,Purchase`

**Formato Brasileiro**:
- Delimitador: Ponto-e-vírgula (;)
- Decimal: Vírgula (,)
- Exemplo: `22/10/2025;100,50;Compra`

#### 3. Definir Configuração OFX

- **ID da Conta**: Seu identificador de conta (ex: número da conta)
- **Nome do Banco**: Nome da sua instituição financeira
- **Moeda**: BRL (Real Brasileiro), USD, EUR ou GBP

#### 3b. Habilitar Validação de Data (Opcional)

Para faturas de cartão de crédito, você pode validar que todas as transações estão dentro do período da fatura:

1. **Marque a caixa**: "Habilitar validação de data para período da fatura do cartão de crédito"
2. **Defina a Data Inicial**: Insira o primeiro dia do seu período de fatura (ex: `2025-10-01` ou `01/10/2025`)
3. **Defina a Data Final**: Insira o último dia do seu período de fatura (ex: `2025-10-31` ou `31/10/2025`)

Quando habilitado, o conversor irá:
- Verificar cada data de transação contra o intervalo especificado
- Para transações fora do intervalo, solicitar que você escolha:
  - **Ajustar para limite**: Move a data para o limite válido mais próximo (data inicial ou final)
  - **Excluir transação**: Remove a transação da saída

Isso é útil para garantir consistência da fatura e lidar com transações que podem aparecer no CSV mas não pertencem ao período atual da fatura.

#### 4. Carregar CSV

Clique em "Load CSV" para analisar o arquivo. A aplicação exibirá todas as colunas disponíveis.

#### 5. Mapear Colunas

Mapeie suas colunas CSV para campos OFX:

| Campo OFX | Obrigatório | Descrição | Exemplo de Coluna CSV |
|-----------|-------------|-----------|------------------------|
| Date | Sim | Data da transação | `data`, `date`, `Data` |
| Amount | Sim | Valor da transação | `valor`, `amount`, `Valor` |
| Description | Sim | Descrição da transação | `descricao`, `description`, `memo` |
| Type | Não | Tipo de transação (DEBIT/CREDIT) | `tipo`, `type` |
| ID | Não | Identificador único da transação | `id`, `transaction_id` |

**Nota**: Se Type não for mapeado, será inferido pelo sinal do valor (negativo = DEBIT, positivo = CREDIT).

#### 6. Converter

Clique em "Convert to OFX" para gerar o arquivo OFX. Escolha onde salvá-lo.

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

### Exemplo 3: Formato Mínimo (Sem Coluna de Tipo)
```csv
date,amount,description
2025-10-01,-100.50,Grocery Store
2025-10-02,-50.25,Gas Station
2025-10-03,1000.00,Salary
```

### Exemplo 4: Formato de Exportação do Nubank
```csv
date,category,title,amount
01/10/2025,alimentação,Supermercado ABC,-100,50
02/10/2025,transporte,Uber,-25,00
05/10/2025,outros,Pagamento recebido,1.500,00
```

**Mapeamento de Colunas para Nubank**:
- Date → `date`
- Amount → `amount`
- Description → `title` (ou combine `category` + `title`)
- Type → Não mapeado (auto-detectado)

### Exemplo 5: Usando Validação de Data

Quando você tem transações que podem estar fora do período da sua fatura:

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
- Transação de 28/09/2025: Você será solicitado a ajustar para 01/10/2025 ou excluir
- Transações de 01/10/2025 a 31/10/2025: Processadas normalmente
- Transação de 02/11/2025: Você será solicitado a ajustar para 31/10/2025 ou excluir

**Benefícios:**
- Garante precisão do período da fatura
- Ajuda a identificar transações mal posicionadas
- Mantém consistência cronológica
- Fornece controle sobre casos limítrofes

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
- Validação de data e tratamento de limites
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
Ran 33 tests in 0.XXXs

OK
```

## Log

A aplicação gera logs detalhados em `csv_to_ofx_converter.log`:

```
2025-11-08 12:34:56 - __main__ - INFO - CSVParser initialized: delimiter=',', decimal='.'
2025-11-08 12:35:01 - __main__ - INFO - Parsed CSV: 150 rows, 4 columns
2025-11-08 12:35:10 - __main__ - INFO - OFX file generated: output.ofx (150 transactions)
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

## Arquitetura

### Estrutura do Código

```
csv_to_ofx_converter.py
├── CSVParser          # Manipula análise de arquivo CSV
│   ├── parse_file()          # Analisa CSV e extrai dados
│   └── normalize_amount()    # Converte valores para float
│
├── OFXGenerator       # Gera arquivos OFX
│   ├── add_transaction()     # Adiciona transação à fila
│   ├── _parse_date()         # Analisa e formata datas
│   └── generate()            # Cria arquivo OFX
│
├── DateValidator      # Valida datas de transação
│   ├── is_within_range()     # Verifica se a data é válida
│   ├── get_date_status()     # Determina antes/dentro/depois
│   └── adjust_date_to_boundary()  # Ajusta datas fora do intervalo
│
└── ConverterGUI       # Interface Tkinter GUI
    ├── _create_widgets()     # Constrói componentes UI
    ├── _load_csv()           # Carrega e analisa CSV
    ├── _convert()            # Realiza conversão
    ├── _handle_out_of_range_transaction()  # Trata problemas de data
    └── _log()                # Exibe mensagens de log
```

### Fluxo de Dados

```
Arquivo CSV → CSVParser → Mapeamento de Campos → Validação de Data → OFXGenerator → Arquivo OFX
    ↓                        ↓                      ↓                      ↓
  Cabeçalhos          Mapeamento GUI           DateValidator          Transações
  Linhas              Entrada do Usuário       (Opcional)             Formatação
                                               Decisão do Usuário
```

**Fluxo de Validação de Data** (quando habilitado):
```
Data da Transação → DateValidator.is_within_range()
                        ↓
                   [Dentro do Intervalo?]
                    ↙         ↘
                  Sim          Não
                   ↓            ↓
            Adicionar ao OFX    Mostrar Diálogo
                              ↓
                      [Escolha do Usuário]
                       ↙         ↘
                  Ajustar        Excluir
                    ↓              ↓
              Ajustar Data     Pular Transação
                    ↓
               Adicionar ao OFX
```

## Melhores Práticas

1. **Sempre revise seus dados CSV** antes da conversão para garantir qualidade dos dados
2. **Teste com um arquivo CSV pequeno** primeiro para verificar se os mapeamentos estão corretos
3. **Mantenha backups** dos seus arquivos CSV originais
4. **Verifique os arquivos OFX** no seu software financeiro antes de importar grandes conjuntos de dados
5. **Use formatos de data consistentes** dentro de um único arquivo CSV
6. **Verifique os logs** se a conversão falhar ou produzir resultados inesperados

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
9. **Modo de Visualização**: Visualizar saída OFX antes de salvar
10. **Formatos de Data Personalizados**: Permitir que usuários especifiquem formatos de data personalizados
11. **Interface de Linha de Comando**: Adicionar CLI para scripts e automação
12. **Deduplicação de Transações**: Detectar e tratar transações duplicadas
13. **Transações Divididas**: Suporte para transações divididas/categorizadas
14. **Suporte Multi-idioma**: Internacionalização (i18n)
15. **Suporte a Excel**: Importação direta de arquivos .xlsx/.xls
16. **Ajuste de Data em Lote**: Opção para ajustar todas as datas fora do intervalo de uma vez

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

## Documentação Adicional

Para mais informações, consulte:
- **DATE_VALIDATION_GUIDE.md** - Guia detalhado sobre validação de data
- **CODE_EXAMPLES.md** - Exemplos de código e padrões de uso
- **IMPLEMENTATION_SUMMARY.md** - Detalhes técnicos da implementação

---

**Versão**: 1.1.0
**Última Atualização**: Novembro de 2025
**Autor**: André Claudinei Barsotti Salvadeo (com Assistência de IA)
**Licença**: MIT

## Histórico de Mudanças

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
