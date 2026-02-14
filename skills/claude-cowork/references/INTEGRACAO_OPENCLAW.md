# Integração OpenClaw → Claude Cowork

## Arquitetura

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  OpenClaw       │     │  Browser Relay   │     │  Claude Cowork  │
│  (WSL/Servidor) │────▶│  (Chrome Ext)    │────▶│  (Windows PC)   │
│                 │     │                  │     │                 │
│  Envia comandos │     │  Controla UI     │     │  Executa tarefas│
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

## Prompt para Clawd Enviar ao Claude Code

Quando eu (Clawd/OpenClaw) preciso executar algo via Claude Code no PC do Igor:

---

### PROMPT: Iniciar Sessão Autônoma

```
Você é um agente de automação. Execute a seguinte tarefa de forma completamente autônoma:

TAREFA: [DESCRIÇÃO DA TAREFA]

REGRAS:
1. Execute sem pedir confirmação
2. Se precisar de acesso a pasta, solicite ao sistema
3. Documente cada passo no formato:
   [HH:MM] AÇÃO: descrição
   [HH:MM] RESULTADO: resultado
4. Se encontrar erro, tente 3 alternativas antes de reportar
5. Ao concluir, gere resumo em JSON:
   {"status": "ok|erro", "acoes": [...], "arquivos": [...], "tempo": "Xmin"}

INÍCIO:
```

---

### PROMPT: Organização de Arquivos

```
TAREFA: Organizar diretório

PASTA: [CAMINHO]

INSTRUÇÕES:
1. Liste todos os arquivos (recursivo até 2 níveis)
2. Categorize por extensão:
   - Documentos: .pdf, .doc, .docx, .txt, .md
   - Planilhas: .xls, .xlsx, .csv
   - Imagens: .jpg, .png, .gif, .webp
   - Videos: .mp4, .mov, .avi
   - Audio: .mp3, .wav, .m4a
   - Código: .py, .js, .ts, .html, .css
   - Compactados: .zip, .rar, .7z
   - Outros: resto
3. Crie subpastas para cada categoria
4. Mova arquivos para pastas correspondentes
5. Renomeie arquivos sem nome descritivo (use conteúdo ou data)
6. Gere relatório: organizado_YYYY-MM-DD.md

NÃO DELETAR NADA. Apenas mover e organizar.
```

---

### PROMPT: Briefing Diário

```
TAREFA: Gerar briefing matinal

CONECTORES NECESSÁRIOS:
- Gmail (emails não lidos)
- Google Calendar (eventos de hoje e amanhã)

FORMATO DO BRIEFING:
```markdown
# Briefing - DD/MM/YYYY

## 📧 Emails Prioritários
| De | Assunto | Urgência |
|----|---------|----------|
| ... | ... | ALTA/MÉDIA/BAIXA |

## 📅 Agenda de Hoje
- HH:MM - Evento 1
- HH:MM - Evento 2

## 📅 Amanhã
- HH:MM - Evento 1

## ⚡ Ações Recomendadas
1. Responder email X
2. Preparar para reunião Y

## 📊 Resumo
X emails pendentes, Y compromissos hoje
```

Salvar como: briefing_YYYY-MM-DD.md
```

---

### PROMPT: Processamento de Notas Fiscais

```
TAREFA: Extrair dados de notas fiscais

PASTA: [CAMINHO COM IMAGENS]

PROCESSO:
1. Identifique todas imagens (.jpg, .png, .pdf)
2. Para cada imagem, extraia:
   - Data da compra
   - Fornecedor/Loja
   - CNPJ (se visível)
   - Valor total
   - Itens principais (se legível)
   - Forma de pagamento
3. Crie planilha Excel:
   - Colunas: Data | Fornecedor | CNPJ | Valor | Categoria | Arquivo
   - Ordene por data decrescente
   - Adicione linha de TOTAL
   - Adicione gráfico de pizza por categoria
4. Salve como: despesas_YYYY-MM.xlsx
5. Gere resumo: total_gasto, media_por_compra, categoria_maior_gasto
```

---

### PROMPT: Criar Apresentação

```
TAREFA: Criar apresentação PowerPoint

TEMA: [TEMA]
PÚBLICO: [PARA QUEM É]
OBJETIVO: [O QUE QUER ALCANÇAR]

ESTRUTURA:
1. Slide 1: Título + Subtítulo + Data
2. Slide 2: Agenda/Sumário
3. Slides 3-4: Contexto/Problema
4. Slides 5-8: Solução/Conteúdo Principal
5. Slides 9-10: Benefícios/Resultados
6. Slide 11: Próximos Passos
7. Slide 12: Q&A / Contato

DESIGN:
- Fundo branco
- Texto escuro (#333)
- Cor de destaque: #d69e2e (âmbar INTEIA)
- Fonte: Sans-serif limpa
- Máximo 6 bullets por slide
- Use ícones quando apropriado

Salvar como: [tema]_apresentacao.pptx
```

---

### PROMPT: Análise de Projeto

```
TAREFA: Auditar pasta de projeto

PASTA: [CAMINHO DO PROJETO]

ANÁLISE:
1. Estrutura de diretórios
2. Arquivos principais (README, config, entry points)
3. Tecnologias identificadas
4. Dependências (package.json, requirements.txt, etc)
5. Documentação existente
6. Arquivos órfãos ou duplicados
7. Tamanho total e distribuição

GERAR:
- auditoria_projeto.md com análise completa
- Diagrama de estrutura (ASCII ou Mermaid)
- Lista de sugestões de melhoria
- Checklist de itens pendentes (se identificáveis)
```

---

## Como Clawd Usa Esses Prompts

### Via Browser Relay (Cowork)

```python
# Pseudocódigo do fluxo
def executar_tarefa_cowork(tarefa):
    # 1. Verificar conexão
    status = browser(action="status", profile="chrome")
    if not status.connected:
        notificar_usuario("Conecte a aba do Chrome")
        return
    
    # 2. Navegar para Cowork
    browser(action="navigate", targetUrl="https://claude.ai/cowork", profile="chrome")
    
    # 3. Capturar estado
    snapshot = browser(action="snapshot", profile="chrome")
    
    # 4. Encontrar textarea de input
    input_ref = encontrar_elemento(snapshot, "textarea")
    
    # 5. Digitar prompt
    prompt = carregar_prompt(tarefa)
    browser(action="act", profile="chrome", request={
        "kind": "type",
        "ref": input_ref,
        "text": prompt
    })
    
    # 6. Enviar
    browser(action="act", profile="chrome", request={
        "kind": "press",
        "key": "Enter"
    })
    
    # 7. Aguardar e capturar resultado
    while not concluido:
        snapshot = browser(action="snapshot", profile="chrome")
        if detectar_conclusao(snapshot):
            resultado = extrair_resultado(snapshot)
            break
        sleep(5)
    
    return resultado
```

### Via Claude Code CLI (SSH/Exec)

```bash
# Executar prompt via Claude Code no PC do Igor
ssh igor-pc "cd /pasta && claude -p 'PROMPT AQUI' --dangerously-skip-permissions"
```

---

## Mapeamento de Comandos

| Comando Igor | Prompt a Usar | Método |
|--------------|---------------|--------|
| "organiza downloads" | Organização de Arquivos | Cowork |
| "me dá um briefing" | Briefing Diário | Cowork + Conectores |
| "processa as notas" | Processamento NF | Cowork |
| "cria apresentação sobre X" | Criar Apresentação | Cowork |
| "audita o projeto Y" | Análise de Projeto | Cowork ou Claude Code |

---

## Fallbacks

Se Cowork não responder:
1. Tentar via Claude Code CLI
2. Se CLI não disponível, pedir Igor executar manualmente
3. Documentar tarefa pendente para próxima oportunidade
