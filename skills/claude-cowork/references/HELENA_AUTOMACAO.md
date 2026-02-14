# Helena — Deusa da Automação

## Visão

Helena evolui de analista de inteligência eleitoral para **agente autônomo de produtividade**, capaz de:
- Executar workflows complexos em cadeia
- Gravar e reutilizar sequências de tarefas
- Processar dados e gerar entregas automaticamente
- Aprender com execuções anteriores

---

## Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                    HELENA CENTRAL                            │
│  (Backend FastAPI em api.inteia.com.br)                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │  Análise    │  │  Automação  │  │  Gravação   │          │
│  │  Eleitoral  │  │  de Tarefas │  │  Workflows  │          │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘          │
│         │                │                │                  │
│         └────────────────┼────────────────┘                  │
│                          ▼                                   │
│              ┌───────────────────────┐                       │
│              │   Motor de Execução   │                       │
│              │   (Workflow Engine)   │                       │
│              └───────────┬───────────┘                       │
│                          │                                   │
└──────────────────────────┼───────────────────────────────────┘
                           │
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
    ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
    │   Cowork    │ │   OpenClaw  │ │   APIs      │
    │  (Desktop)  │ │  (Browser)  │ │  Externas   │
    └─────────────┘ └─────────────┘ └─────────────┘
```

---

## Capacidades de Helena

### 1. Análise de Dados (Existente)
- Consultar 1000+ eleitores sintéticos
- Correlações demográficas
- Recomendações estratégicas

### 2. Automação de Tarefas (NOVO)
- Organizar arquivos
- Criar documentos/planilhas/apresentações
- Processar imagens e extrair dados
- Gerar relatórios automatizados

### 3. Gravação de Workflows (NOVO)
- Gravar sequência de ações
- Salvar como template reutilizável
- Executar workflows salvos
- Aprender padrões de uso

### 4. Execução em Cadeia (NOVO)
- Pipeline de tarefas sequenciais
- Condicionais (se X então Y)
- Loops (para cada arquivo faça)
- Paralelização quando possível

---

## Comandos Helena

### Automação Básica

```
/helena organizar [pasta]
→ Organiza arquivos por tipo, renomeia, gera relatório

/helena briefing
→ Acessa Gmail + Calendar, gera resumo do dia

/helena extrair [pasta-imagens]
→ Processa notas fiscais, cria planilha de despesas

/helena apresentacao [tema]
→ Pesquisa, estrutura e cria PowerPoint

/helena relatorio [projeto]
→ Audita pasta, gera relatório de status
```

### Workflows Gravados

```
/helena gravar [nome-workflow]
→ Inicia gravação de ações

/helena parar
→ Para gravação e salva workflow

/helena executar [nome-workflow]
→ Executa workflow salvo

/helena listar-workflows
→ Lista todos workflows disponíveis

/helena editar [nome-workflow]
→ Abre workflow para edição
```

### Execução em Cadeia

```
/helena pipeline
  1. organizar Downloads
  2. extrair Downloads/NotasFiscais
  3. relatorio projeto-x
  4. apresentacao resumo-mensal
→ Executa sequência de tarefas

/helena agendar [workflow] [cron]
→ Agenda execução recorrente
```

---

## Estrutura de Workflow

```yaml
# Exemplo: workflow_briefing_completo.yaml
name: briefing-completo
description: Briefing matinal com emails, agenda e tarefas
version: 1.0
author: Helena

triggers:
  - schedule: "0 7 * * 1-5"  # Seg-Sex 7h
  - command: "/helena briefing-completo"

steps:
  - id: emails
    action: gmail.unread
    params:
      limit: 20
      categorize: true
    output: $emails

  - id: agenda
    action: calendar.today
    params:
      include_tomorrow: true
    output: $agenda

  - id: analise
    action: ai.analyze
    params:
      prompt: |
        Analise estes emails e agenda:
        Emails: $emails
        Agenda: $agenda
        
        Gere briefing executivo com:
        1. Emails urgentes
        2. Compromissos do dia
        3. Ações recomendadas
    output: $briefing

  - id: salvar
    action: file.write
    params:
      path: "~/Briefings/briefing_{{date}}.md"
      content: $briefing

  - id: notificar
    action: notify.send
    params:
      channel: whatsapp
      message: |
        ☀️ Briefing pronto!
        {{$briefing.resumo}}
```

---

## Sistema de Gravação

### Como Funciona

1. **Início da Gravação**
   ```
   Usuário: /helena gravar preparar-reuniao
   Helena: 🔴 Gravando workflow "preparar-reuniao"...
           Execute as ações que deseja gravar.
   ```

2. **Execução de Ações**
   ```
   Usuário: Busca no Drive a pauta da reunião de ontem
   Helena: [GRAVANDO] Ação 1: drive.search("pauta reunião")
           Encontrei: pauta_reuniao_2026-02-13.docx
   
   Usuário: Cria uma cópia com data de hoje
   Helena: [GRAVANDO] Ação 2: file.copy → pauta_reuniao_2026-02-14.docx
   
   Usuário: Abre e atualiza a data no documento
   Helena: [GRAVANDO] Ação 3: doc.edit(atualizar_data)
   ```

3. **Fim da Gravação**
   ```
   Usuário: /helena parar
   Helena: ✅ Workflow "preparar-reuniao" salvo!
           3 ações gravadas:
           1. Buscar pauta anterior no Drive
           2. Criar cópia com nova data
           3. Atualizar data no documento
           
           Próxima vez: /helena executar preparar-reuniao
   ```

4. **Execução Futura**
   ```
   Usuário: /helena executar preparar-reuniao
   Helena: ▶️ Executando "preparar-reuniao"...
           [1/3] Buscando pauta anterior... ✓
           [2/3] Criando cópia... ✓
           [3/3] Atualizando data... ✓
           ✅ Concluído! Arquivo: pauta_reuniao_2026-02-15.docx
   ```

---

## Integração com Cowork

### Helena como Orquestradora

```python
# Pseudocódigo: Helena enviando tarefa para Cowork

async def helena_executar_tarefa(tarefa: str, pasta: str):
    # 1. Construir prompt otimizado
    prompt = construir_prompt_cowork(tarefa, pasta)
    
    # 2. Conectar ao Cowork via browser relay
    browser = await conectar_browser_relay()
    
    # 3. Navegar para Cowork
    await browser.navigate("https://claude.ai/cowork")
    
    # 4. Selecionar pasta de trabalho
    await browser.select_folder(pasta)
    
    # 5. Enviar prompt
    await browser.type_and_send(prompt)
    
    # 6. Aguardar e capturar resultado
    resultado = await browser.wait_for_completion()
    
    # 7. Gravar no histórico (para aprendizado)
    await gravar_execucao(tarefa, prompt, resultado)
    
    return resultado
```

### Fluxo via WhatsApp/Telegram

```
Usuário: Helena, organiza a pasta Downloads e me faz um relatório

Helena: 📂 Iniciando organização...

[Helena conecta ao Cowork]
[Helena envia prompt de organização]
[Cowork executa no PC]

Helena: ✅ Organização concluída!
        
        📊 Resumo:
        - 127 arquivos organizados
        - 6 categorias criadas
        - 12 arquivos renomeados
        
        📎 Relatório: organizacao_2026-02-14.md
        
        Quer que eu envie o relatório completo?
```

---

## Aprendizado Contínuo

### O que Helena Aprende

1. **Padrões de Uso**
   - Quais tarefas são mais frequentes
   - Horários típicos de cada tipo de tarefa
   - Sequências comuns de ações

2. **Otimizações**
   - Prompts que funcionam melhor
   - Tempo médio de cada tarefa
   - Erros frequentes e como evitar

3. **Preferências do Usuário**
   - Formato de saída preferido
   - Nível de detalhe desejado
   - Nomenclatura de arquivos

### Armazenamento

```
/helena/
├── workflows/           # Workflows gravados
│   ├── briefing-completo.yaml
│   ├── preparar-reuniao.yaml
│   └── ...
├── historico/           # Histórico de execuções
│   ├── 2026-02/
│   │   ├── execucao_001.json
│   │   └── ...
├── aprendizado/         # Dados de aprendizado
│   ├── padroes.json
│   ├── otimizacoes.json
│   └── preferencias.json
└── templates/           # Templates de prompts
    ├── organizar.md
    ├── briefing.md
    └── ...
```

---

## Próximos Passos

1. **Implementar no Backend**
   - Adicionar endpoints de workflow em FastAPI
   - Integrar com sistema de mensagens

2. **Conectar com Cowork**
   - Testar browser relay
   - Mapear elementos da UI

3. **Criar Workflows Iniciais**
   - Briefing diário
   - Organização de arquivos
   - Processamento de NF

4. **Treinar Aprendizado**
   - Coletar dados de execuções
   - Identificar padrões
   - Otimizar prompts
