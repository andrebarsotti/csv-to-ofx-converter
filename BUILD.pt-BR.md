# Guia de Compilação e Lançamento

> 🇺🇸 **[Read in English](BUILD.md)**

Este documento explica como compilar o Conversor de CSV para OFX como um executável autônomo e como funciona o processo automatizado de lançamento.

## Índice

1. [Início Rápido](#início-rápido)
2. [Compilando Localmente](#compilando-localmente)
3. [Fluxo de Trabalho do GitHub Actions](#fluxo-de-trabalho-do-github-actions)
4. [Criando um Lançamento](#criando-um-lançamento)
5. [Solução de Problemas](#solução-de-problemas)

## Início Rápido

### Para Usuários Finais

**Baixe executáveis pré-compilados** da [página de Releases](https://github.com/YOUR_USERNAME/conversor-csv-ofx/releases).

Não é necessário compilar!

### Para Desenvolvedores

Compile seu próprio executável:

```bash
# Linux/macOS
./build.sh

# Windows
build.bat
```

## Compilando Localmente

### Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes do Python)

### Passo 1: Instalar o PyInstaller

```bash
pip install pyinstaller
```

### Passo 2: Compilar o Executável

#### Opção A: Usando Scripts de Compilação (Recomendado)

**Linux/macOS:**
```bash
chmod +x build.sh
./build.sh
```

**Windows:**
```cmd
build.bat
```

#### Opção B: Usando PyInstaller Diretamente

```bash
pyinstaller csv_to_ofx_converter.spec
```

#### Opção C: Comando Manual do PyInstaller

**Linux/macOS:**
```bash
pyinstaller --onefile \
  --name="csv-to-ofx-converter" \
  --add-data "README.md:." \
  --add-data "README.pt-BR.md:." \
  --windowed \
  --noconfirm \
  src/csv_to_ofx_converter.py
```

**Windows:**
```cmd
pyinstaller --onefile ^
  --name="csv-to-ofx-converter" ^
  --add-data "README.md;." ^
  --add-data "README.pt-BR.md;." ^
  --windowed ^
  --noconfirm ^
  src/csv_to_ofx_converter.py
```

### Passo 3: Encontrar Seu Executável

O executável compilado estará no diretório `dist/`:

- **Linux/macOS**: `dist/csv-to-ofx-converter`
- **Windows**: `dist/csv-to-ofx-converter.exe`

### Passo 4: Testar o Executável

Execute o executável para garantir que funciona:

```bash
# Linux/macOS
./dist/csv-to-ofx-converter

# Windows
dist\csv-to-ofx-converter.exe
```

## Fluxo de Trabalho do GitHub Actions

O projeto usa GitHub Actions para compilar automaticamente executáveis para todas as plataformas quando você cria um lançamento.

### Arquivo de Fluxo de Trabalho

Localização: `.github/workflows/build-and-release.yml`

### O Que Ele Faz

1. **Dispara quando**:
   - Push de tags de versão (ex: `v1.1.0`)
   - Execução manual do fluxo de trabalho

2. **Compila em**:
   - Ubuntu (Linux x64)
   - Windows (Windows x64)
   - macOS (macOS x64)

3. **Gera**:
   - Executáveis autônomos para cada plataforma
   - Checksums SHA256
   - Notas de lançamento

4. **Publica**:
   - Cria um Release no GitHub
   - Anexa todos os executáveis
   - Inclui checksums e links de documentação

### Matriz de Compilação

| Plataforma | SO | Saída |
|------------|----|-------|
| Linux | ubuntu-latest | csv-to-ofx-converter-linux-x64 |
| Windows | windows-latest | csv-to-ofx-converter-windows-x64.exe |
| macOS | macos-latest | csv-to-ofx-converter-macos-x64 |

## Criando um Lançamento

### Lançamento Automático (Recomendado)

1. **Atualizar versão no código** (se necessário):
   ```python
   # Em src/csv_to_ofx_converter.py ou README.md
   __version__ = "1.2.0"
   ```

2. **Fazer commit das suas alterações**:
   ```bash
   git add .
   git commit -m "Release version 1.2.0"
   ```

3. **Criar e enviar uma tag de versão**:
   ```bash
   git tag v1.2.0
   git push origin v1.2.0
   ```

4. **Aguardar o GitHub Actions** completar (geralmente 5-10 minutos)

5. **Verificar a página de Releases** para seu novo lançamento com executáveis anexados

### Lançamento Manual

Se você precisar acionar o fluxo de trabalho manualmente:

1. Vá para a aba **Actions** no seu repositório GitHub
2. Clique no fluxo de trabalho **Build and Release**
3. Clique em **Run workflow**
4. Selecione o branch e clique no botão **Run workflow**

## Detalhes do Processo de Lançamento

### Versionamento com Tags

Use versionamento semântico: `vMAIOR.MENOR.CORREÇÃO`

Exemplos:
- `v1.0.0` - Lançamento inicial
- `v1.1.0` - Novos recursos (validação de data)
- `v1.1.1` - Correções de bugs
- `v2.0.0` - Mudanças que quebram compatibilidade

### O Que É Incluído em um Lançamento

1. **Executáveis**:
   - Linux: `csv-to-ofx-converter-linux-x64`
   - Windows: `csv-to-ofx-converter-windows-x64.exe`
   - macOS: `csv-to-ofx-converter-macos-x64`

2. **Checksums**:
   - `checksums.txt` com hashes SHA256

3. **Notas de Lançamento**:
   - Instruções de download
   - Passos de instalação específicos da plataforma
   - Links para documentação
   - Informações de versão
   - Data de compilação

## Configuração de Compilação

### Arquivo Spec do PyInstaller

O arquivo `csv_to_ofx_converter.spec` controla a compilação:

```python
# Configurações principais:
- onefile: True          # Executável único
- windowed: True         # Sem janela de console (apenas GUI)
- console: False         # Oculta console
- upx: True             # Comprime com UPX
```

### Arquivos Incluídos

Automaticamente empacotados no executável:
- `README.md` - Documentação em inglês
- `README.pt-BR.md` - Documentação em português
- Todos os módulos da biblioteca padrão do Python
- Biblioteca GUI Tkinter

### Arquivos Excluídos

Não incluídos (para reduzir tamanho):
- Arquivos de teste (`tests/`)
- Scripts de compilação
- Arquivos do Git
- Documentação de desenvolvimento

## Solução de Problemas

### Compilação Falha com "Module not found"

**Problema**: PyInstaller não consegue encontrar um módulo

**Solução**: Adicione em `hiddenimports` no arquivo spec:
```python
hiddenimports=['modulo_faltante'],
```

### Executável Muito Grande

**Problema**: Tamanho do arquivo acima de 50MB

**Soluções**:
1. Habilite compressão UPX: `upx: True`
2. Exclua módulos não utilizados no arquivo spec
3. Use a flag `--exclude-module`

### "Permission denied" no Linux/macOS

**Problema**: Não consegue executar o arquivo

**Solução**:
```bash
chmod +x csv-to-ofx-converter
```

### Aviso de Segurança do Windows

**Problema**: "O Windows protegeu seu PC"

**Solução**: Isso é normal para executáveis não assinados:
1. Clique em "Mais informações"
2. Clique em "Executar assim mesmo"

**Para distribuição**: Considere assinatura de código (requer certificado)

### macOS "Não pode ser aberto porque o desenvolvedor não pode ser verificado"

**Problema**: macOS Gatekeeper bloqueia o app

**Solução**:
1. Clique com botão direito no app
2. Selecione "Abrir"
3. Clique em "Abrir" no diálogo

**Ou via Terminal**:
```bash
xattr -d com.apple.quarantine csv-to-ofx-converter-macos-x64
```

### Compilação Funciona Localmente mas Falha no GitHub Actions

**Problema**: Ambiente diferente

**Soluções**:
1. Verifique se a versão do Python corresponde (3.11 no workflow)
2. Verifique se todas as dependências estão listadas
3. Verifique caminhos de arquivo (use barras normais)
4. Revise os logs do GitHub Actions

### Lançamento Não Criado

**Problema**: Workflow executa mas não cria lançamento

**Verifique**:
1. Tag começa com `v` (ex: `v1.0.0`)
2. Tag foi enviada para o GitHub: `git push origin v1.0.0`
3. GITHUB_TOKEN tem permissões adequadas
4. Não existe outro lançamento com a mesma tag

## Configuração Avançada

### Adicionando um Ícone

1. Crie ou obtenha um arquivo de ícone:
   - Windows: arquivo `.ico` (256x256 ou múltiplos tamanhos)
   - macOS: arquivo `.icns`
   - Linux: arquivo `.png`

2. Atualize o arquivo spec:
   ```python
   icon='caminho/para/icon.ico'
   ```

### Assinatura de Código (Opcional)

Para distribuição em produção, considere assinar:

**Windows**:
```bash
signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com csv-to-ofx-converter.exe
```

**macOS**:
```bash
codesign --deep --force --verify --verbose --sign "Developer ID" csv-to-ofx-converter
```

### Dicas de Otimização

1. **Reduzir Tamanho**:
   ```python
   excludes=['test', 'unittest', 'pdb', 'pydoc'],
   ```

2. **Inicialização Mais Rápida**:
   ```python
   noarchive=False,  # Mais rápido mas maior
   ```

3. **Compilação de Debug**:
   ```python
   debug=True,      # Para solução de problemas
   console=True,    # Mostrar saída do console
   ```

## Integração Contínua

### Gatilhos do Fluxo de Trabalho

O fluxo de trabalho pode ser acionado por:

1. **Push de tag** (automático):
   ```bash
   git tag v1.2.0 && git push origin v1.2.0
   ```

2. **Execução manual** (manual):
   - Vá para Actions > Build and Release > Run workflow

3. **Chamada de API** (automatizado):
   ```bash
   curl -X POST \
     -H "Accept: application/vnd.github.v3+json" \
     -H "Authorization: token SEU_TOKEN" \
     https://api.github.com/repos/USUARIO/REPO/actions/workflows/build-and-release.yml/dispatches \
     -d '{"ref":"main"}'
   ```

## Testando Antes do Lançamento

Antes de criar um lançamento oficial:

1. **Teste localmente**:
   ```bash
   ./build.sh
   ./dist/csv-to-ofx-converter
   ```

2. **Execute os testes**:
   ```bash
   python3 -m unittest tests.test_converter -v
   ```

3. **Crie um pré-lançamento**:
   - Tag com `-rc1`, `-beta`, etc.: `v1.2.0-rc1`
   - Marque como pré-lançamento no GitHub

4. **Obtenha feedback** antes do lançamento final

## Suporte

Para problemas de compilação:
1. Consulte este documento
2. Revise os logs do GitHub Actions
3. Teste a compilação localmente primeiro
4. Abra uma issue com:
   - Mensagens de erro
   - Logs de compilação
   - Versão da plataforma/SO
   - Versão do Python

---

**Última Atualização**: Novembro de 2025
**Sistema de Compilação**: PyInstaller 6.x
**CI/CD**: GitHub Actions
