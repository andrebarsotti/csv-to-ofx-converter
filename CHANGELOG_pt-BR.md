# Registro de Alterações

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/spec/v2.0.0.html).

## [2.0.3] - 2025-11-09

### Adicionado
- Arquivo de configuração inicial do SonarCloud para análise de qualidade de código
- Workflow do SonarQube para verificações automáticas de qualidade de código
- Configuração do Python e testes de cobertura no workflow do SonarQube
- Suporte à análise de cobertura de código
- Organização em nível de módulo com nova estrutura de pacote
- Módulo de constantes para constantes compartilhadas da aplicação
- Docstrings abrangentes de módulos e anotações de tipo

### Modificado
- Refatoração do código monolítico em módulos separados para melhor organização
  - `csv_parser.py`: Funcionalidade de análise de CSV
  - `ofx_generator.py`: Geração de arquivos OFX
  - `date_validator.py`: Lógica de validação de data
  - `converter_gui.py`: Implementação da GUI
  - `constants.py`: Constantes compartilhadas
- Atualizado workflow do GitHub Actions para melhor processo de build e release
- Melhorada configuração do SonarQube com caminhos e configurações corretos
- Atualizados nomes dos executáveis nos releases do GitHub para corresponder à saída real
- Melhorada formatação da mensagem de sucesso na conclusão da conversão
- Melhor organização e manutenibilidade do código

### Corrigido
- Resolvidos múltiplos problemas de qualidade de código identificados pelo SonarQube
- Corrigidos erros de importação e problemas com caracteres Unicode
- Corrigidos nomes de executáveis no workflow de release
- Excluídos arquivos de UI da análise de cobertura de código
- Configurado nome correto do branch para análise do SonarQube
- Melhorado tratamento de erros e logging

### Removido
- Resumos de implementação desatualizados (IMPLEMENTATION_SUMMARY.md, IMPLEMENTATION_V2.0_SUMMARY.md)
- Configurações do Claude do controle de versão
- Código redundante e comentado

### Segurança
- Corrigidas potenciais vulnerabilidades de segurança identificadas pelo SonarQube
- Melhorada qualidade de código e postura de segurança

## [2.0.2] - 2025-11-09

### Corrigido
- Corrigidos nomes de executáveis nos releases do GitHub

### Modificado
- Atualizada formatação das instruções de download de executáveis nas notas de release

## [2.0.1] - Release anterior

### Adicionado
- Recursos iniciais da versão 2.0
- GUI aprimorada com interface estilo assistente
- Suporte a descrição composta
- Recursos de validação de data

---

Para versões mais antigas, consulte o histórico do git.
