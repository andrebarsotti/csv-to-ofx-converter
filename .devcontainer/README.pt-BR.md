# Configuração do GitHub Codespaces

Este diretório contém a configuração do container de desenvolvimento para GitHub Codespaces, habilitando um ambiente Python completamente configurado com suporte a GUI para a aplicação CSV to OFX Converter.

## O Que Está Incluído

### Ambiente
- **Python 3.11** com biblioteca padrão completa
- Suporte a **Tkinter** para aplicações GUI
- **Display virtual** (Xvfb) para executar apps GUI na nuvem
- **noVNC** para acesso web à interface gráfica

### Ferramentas de Desenvolvimento
- **PyInstaller** - Para construir executáveis standalone
- **Claude Code CLI** - Assistente de codificação com IA
- **Flake8** - Linting de código
- **Black** - Formatação de código
- **Pylint** - Análise de código
- **MyPy** - Verificação estática de tipos

### Extensões do VS Code
- Suporte à linguagem Python (Pylance)
- Formatador Black
- Gerador automático de docstrings
- GitLens
- GitHub Copilot (se disponível)

## Início Rápido

### 1. Abrir no Codespaces

Clique no botão "Code" no GitHub e selecione "Create codespace on main" (ou seu branch atual).

O ambiente irá automaticamente:
- Instalar todas as dependências
- Configurar o ambiente Python
- Executar a suite de testes
- Configurar serviços GUI
- Exibir informações úteis

### 2. Executar a Aplicação

#### Opção A: Testes sem Interface (Headless)
```bash
# Executar testes sem GUI
python3 -m unittest discover tests -v
```

#### Opção B: Com Interface Gráfica (Recomendado)

1. **Iniciar serviços GUI:**
   ```bash
   start-gui.sh
   ```

2. **Acessar a GUI via web:**
   - Clique na aba "Ports" no VS Code (painel inferior)
   - Encontre a porta 6080 (noVNC)
   - Clique no ícone de globo para abrir no navegador
   - Ou use a URL redirecionada: `https://<nome-codespace>-6080.app.github.dev/vnc.html`

3. **Login no noVNC:**
   - Senha: `codespaces`

4. **Executar a aplicação:**
   ```bash
   python3 main.py
   ```

5. **A interface Tkinter aparecerá na janela do navegador noVNC**

### 3. Fluxo de Desenvolvimento

```bash
# Executar todos os testes
python3 -m unittest discover tests -v

# Executar módulo de teste específico
python3 -m unittest tests.test_csv_parser

# Formatar código com Black
black src/ tests/

# Verificar código com Flake8
flake8 src/ tests/

# Construir executável (Linux)
./build.sh
```

### 4. Usando Claude Code CLI

Claude Code é um assistente de codificação com IA que vem pré-instalado neste ambiente.

```bash
# Iniciar Claude Code
claude

# Verificar versão
claude --version

# Atualizar Claude Code
claude update

# Executar diagnósticos
claude doctor
```

#### Configuração Inicial

Na primeira execução, Claude Code solicitará autenticação. Você tem três opções:

1. **Claude Console** (Padrão) - Requer cobrança em console.anthropic.com
2. **Assinatura Claude App** - Use plano Pro/Max existente de claude.ai
3. **Enterprise** - Amazon Bedrock ou Google Vertex AI

Siga as instruções para completar a autenticação.

#### Usando Claude Code

Uma vez autenticado, você pode:
- Fazer perguntas sobre o código
- Solicitar alterações e refatorações
- Gerar testes e documentação
- Depurar problemas
- Obter explicações de código complexo

Exemplos de comandos:
```bash
# Iniciar sessão interativa
claude

# Depois digite suas solicitações, por exemplo:
# "Explique como funciona o parser CSV"
# "Adicione tratamento de erros ao validador de datas"
# "Gere testes para os utilitários de transação"
```

## Arquivos Neste Diretório

- **devcontainer.json** - Arquivo de configuração principal
  - Define configurações do container
  - Extensões e configurações do VS Code
  - Redirecionamento de portas (6080 para noVNC)
  - Comando pós-criação
  - Variáveis de ambiente

- **Dockerfile** - Definição da imagem do container
  - Baseado na imagem oficial Python 3.11
  - Instala Tkinter e dependências GUI
  - Instala X11, VNC e noVNC
  - Instala ferramentas de desenvolvimento (PyInstaller, linters)

- **start-gui.sh** - Script de inicialização dos serviços GUI
  - Inicia Xvfb (display virtual)
  - Inicia Fluxbox (gerenciador de janelas)
  - Inicia x11vnc (servidor VNC)
  - Inicia noVNC (cliente VNC baseado em web)

- **post-create.sh** - Script de configuração automática
  - Executado após criação do container
  - Instala/atualiza dependências do requirements-dev.txt
  - Configura o ambiente
  - Executa suite de testes
  - Exibe informações úteis

- **verify-setup.sh** - Script de verificação do ambiente
  - Verifica instalação do Python e Tkinter
  - Verifica serviços GUI
  - Testa estrutura do projeto e imports

- **DEPENDENCIES.md** - Guia de gerenciamento de dependências
  - Como adicionar/atualizar dependências
  - Formato dos arquivos requirements
  - Melhores práticas

- **.env.example** - Template de variáveis de ambiente
  - Configurações de display
  - Configuração Python
  - Configurações VNC

## Arquitetura da GUI

O suporte a GUI funciona através da seguinte cadeia:

```
App Tkinter → DISPLAY :1 → Xvfb (Display Virtual) → x11vnc (Servidor VNC)
→ websockify (Proxy WebSocket) → noVNC (Cliente Web) → Seu Navegador
```

Isso permite que você execute e interaja com a aplicação GUI Tkinter diretamente no seu navegador enquanto o código roda na nuvem.

## Personalização

### Alterar Versão do Python
Edite o `Dockerfile`:
```dockerfile
FROM mcr.microsoft.com/devcontainers/python:3.10-bullseye
```

### Adicionar Extensões do VS Code
Edite o `devcontainer.json`:
```json
"extensions": [
  "ms-python.python",
  "id-da-sua-extensao"
]
```

### Adicionar Pacotes do Sistema
Edite o `Dockerfile`:
```dockerfile
RUN apt-get update && apt-get install -y \
    nome-do-pacote \
    && apt-get clean
```

### Adicionar Pacotes Python

Para ferramentas de desenvolvimento, edite [requirements-dev.txt](../requirements-dev.txt):
```bash
# Adicionar ao requirements-dev.txt
echo "nome-do-pacote>=1.0.0" >> requirements-dev.txt

# Reconstruir container ou instalar manualmente
pip install -r requirements-dev.txt
```

Para dependências de runtime (não recomendado), edite [requirements.txt](../requirements.txt):
```bash
# Adicionar ao requirements.txt
echo "nome-do-pacote>=1.0.0" >> requirements.txt

# Instalar
pip install -r requirements.txt
```

Veja [DEPENDENCIES.md](DEPENDENCIES.md) para guia detalhado de gerenciamento de dependências.

## Solução de Problemas

### GUI não aparece
1. Certifique-se de que os serviços GUI estão rodando: `start-gui.sh`
2. Verifique se a porta 6080 está redirecionada no VS Code
3. Verifique a senha VNC: `codespaces`
4. Verifique os logs: `ps aux | grep vnc`

### Testes falham na criação do container
Isso geralmente é temporário durante a configuração inicial. Tente:
```bash
python3 -m unittest discover tests -v
```

### Build falha
Certifique-se de que o PyInstaller está instalado:
```bash
pip install pyinstaller
./build.sh
```

### Erros de display
Configure a variável DISPLAY:
```bash
export DISPLAY=:1
python3 main.py
```

## Dicas de Performance

1. **Feche a GUI quando não precisar** - Serviços GUI consomem recursos
2. **Use testes headless** - Mais rápido para testes unitários
3. **Pare o Codespace quando terminar** - Economiza horas de computação

## Referência de Portas

- **6080** - Interface web noVNC (HTTP)
- **5901** - Servidor VNC (interno, não exposto)

## Variáveis de Ambiente

As seguintes são configuradas automaticamente:

- `DISPLAY=:1` - Display X11 para apps GUI
- `PYTHONPATH=/workspaces/csv-to-ofx-converter/src` - Caminho dos módulos Python
- `PYTHONUNBUFFERED=1` - Saída Python em tempo real

## Recursos Adicionais

- [Documentação GitHub Codespaces](https://docs.github.com/pt/codespaces)
- [Especificação Dev Container](https://containers.dev/)
- [README do Projeto](../README.pt-BR.md)
- [Guia do Desenvolvedor (CLAUDE.md)](../CLAUDE.md)
- [Checklist de Release](../RELEASE_CHECKLIST.md)

## Notas

- O container executa como usuário `vscode` (não root)
- Todas as alterações são salvas no Codespace até ser deletado
- Tier gratuito: 60 horas/mês para máquinas de 2 cores
- Lembre-se de parar ou deletar Codespaces quando não estiver usando

## Suporte

Para problemas com:
- **Configuração do Codespaces**: Consulte a documentação do GitHub Codespaces
- **Bugs da aplicação**: Crie uma issue no repositório GitHub
- **Questões de desenvolvimento**: Veja CLAUDE.md para arquitetura do projeto

---

**Feliz codificação na nuvem!**
