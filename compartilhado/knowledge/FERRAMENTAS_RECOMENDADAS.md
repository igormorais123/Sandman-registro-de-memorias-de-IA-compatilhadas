# 🛠️ Ferramentas Recomendadas

> MCPs, SDKs, extensões e utilitários validados
> Instalação e configuração testadas

---

## MCPs Recomendados

### [Nome do MCP]
**Função**: [O que faz]
**Projetos que usam**: [Lista]
**Avaliação**: ★★★★☆

**Instalação**:
```bash
[comando]
```

**Configuração em claude_desktop_config.json**:
```json
{
  "mcpServers": {
    "[nome]": {
      "command": "[comando]",
      "args": []
    }
  }
}
```

**Pegadinhas**:
- [Problema comum e solução]

<!-- ADICIONAR_MCP_AQUI -->

---

## SDKs e Bibliotecas

### Por Linguagem

#### JavaScript/TypeScript
| Biblioteca | Função | Versão Recomendada | Notas |
|------------|--------|-------------------|-------|
<!-- LIBS_JS -->

#### Python
| Biblioteca | Função | Versão Recomendada | Notas |
|------------|--------|-------------------|-------|
<!-- LIBS_PYTHON -->

#### Go
| Biblioteca | Função | Versão Recomendada | Notas |
|------------|--------|-------------------|-------|
<!-- LIBS_GO -->

<!-- ADICIONAR_SDK_AQUI -->

---

## Extensões VS Code

| Extensão | Função | Essencial? | Notas |
|----------|--------|------------|-------|
| ESLint | Linting JS/TS | Sim | Configurar com projeto |
| Prettier | Formatação | Sim | Ativar format on save |
| GitLens | Git avançado | Recomendado | Histórico inline |
| Error Lens | Erros inline | Recomendado | Destaca problemas |
| Thunder Client | REST client | Opcional | Alternativa ao Postman |
| Docker | Containers | Se usar Docker | Gerenciamento visual |
<!-- ADICIONAR_EXTENSAO_AQUI -->

---

## Ferramentas de Linha de Comando

| Ferramenta | Função | Instalação |
|------------|--------|------------|
| jq | JSON processor | `brew install jq` / `apt install jq` |
| ripgrep (rg) | Busca rápida | `brew install ripgrep` |
| fd | Find moderno | `brew install fd` |
| bat | Cat colorido | `brew install bat` |
| delta | Git diff melhorado | `brew install git-delta` |
| fzf | Fuzzy finder | `brew install fzf` |
| httpie | HTTP client | `pip install httpie` |
| tldr | Man pages simplificadas | `npm install -g tldr` |
<!-- ADICIONAR_CLI_AQUI -->

---

## Scripts Utilitários Globais

### Localização
Todos em `~/.claude-memoria-global/scripts/`

### sync.sh - Sincronização de Memória
```bash
#!/bin/bash
# Script de referência para sincronização
# Execução real via Claude Code

GLOBAL_DIR="$HOME/.claude-memoria-global"
PROJETO_DIR="$1"

if [ -z "$PROJETO_DIR" ]; then
    echo "Uso: sync.sh /caminho/do/projeto"
    exit 1
fi

echo "🔄 Sincronização de Memória"
echo "Global: $GLOBAL_DIR"
echo "Projeto: $PROJETO_DIR"
echo ""
echo "Execute no Claude Code:"
echo "  claude 'Sincronizar projeto com memória global'"
```

### check-memory.sh - Verificação de Integridade
```bash
#!/bin/bash
# Verifica integridade da estrutura de memória

GLOBAL_DIR="$HOME/.claude-memoria-global"

echo "🔍 Verificando estrutura de memória global..."

REQUIRED_FILES=(
    "INDICE_GLOBAL.md"
    "CONHECIMENTO_UNIVERSAL.md"
    "CATALOGO_PROJETOS.md"
    "PADROES_CODIGO.md"
    "ANTIPADROES_GLOBAIS.md"
    "PROMPTS_EFETIVOS.md"
    "FERRAMENTAS_RECOMENDADAS.md"
    "META_APRENDIZADO.md"
)

MISSING=0
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$GLOBAL_DIR/$file" ]; then
        echo "❌ Faltando: $file"
        MISSING=$((MISSING + 1))
    else
        echo "✅ OK: $file"
    fi
done

if [ $MISSING -eq 0 ]; then
    echo ""
    echo "✅ Estrutura global íntegra!"
else
    echo ""
    echo "⚠️ $MISSING arquivo(s) faltando"
fi
```

<!-- ADICIONAR_SCRIPT_AQUI -->

---

## Configurações de Ambiente

### .bashrc / .zshrc recomendações
```bash
# Aliases úteis para Claude Code
alias cc="claude"
alias ccs="claude 'status da memória'"
alias ccsono="claude 'executar ciclo de sono'"
alias ccglobal="claude 'status memória global'"

# Navegação rápida para memória
alias cdmem="cd ~/.claude-memoria-global"

# Função para iniciar projeto com memória
ccprojeto() {
    if [ -d ".memoria" ]; then
        echo "✅ Memória local encontrada"
        claude "carregar contexto do projeto"
    else
        echo "⚠️ Sem memória local. Criar? (s/n)"
        read resposta
        if [ "$resposta" = "s" ]; then
            claude "inicializar sistema de memória"
        fi
    fi
}
```

### Git Aliases Úteis
```bash
# Adicionar ao .gitconfig
[alias]
    st = status
    co = checkout
    br = branch
    ci = commit
    lg = log --oneline --graph --decorate
    unstage = reset HEAD --
    last = log -1 HEAD
    visual = !gitk
```

---

## Integrações Validadas

### GitHub Actions
**Workflow de CI básico validado**:
```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - run: npm test
```

### Docker Compose para Dev
```yaml
version: '3.8'
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: dev
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  pgdata:
```

<!-- ADICIONAR_INTEGRACAO_AQUI -->
