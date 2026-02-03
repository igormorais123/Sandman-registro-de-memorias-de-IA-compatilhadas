# Gestão de Contexto — Regras para Trabalhos Longos

**Criado:** 2026-02-03  
**Motivo:** Crash durante análise Bardin por contexto corrompido  
**Lição:** Nunca confiar apenas na memória de sessão para trabalhos longos

---

## 🚨 O Problema

Em 2026-02-02, durante análise de 7 arquivos com 10 agentes:
1. Piloto funcionou (28 indicadores)
2. Escalei para execução completa
3. Contexto ficou dessincronizado (tool_result órfão)
4. Sessão crashou em loop: `tool_use_id not found`
5. Igor dormiu esperando resultados que nunca vieram

**Causa raiz:** Dependência excessiva do contexto de sessão, sem persistência externa.

---

## ✅ Regras Obrigatórias

### 1. TRABALHOS LONGOS = PERSISTÊNCIA EXTERNA

Se o trabalho tem:
- Mais de 3 etapas sequenciais
- Mais de 5 arquivos para processar
- Tempo estimado > 30 minutos
- Risco de o usuário sair/dormir

**ENTÃO:** Usar o sistema de jobs em `/root/clawd/jobs/`

```bash
# Iniciar job
python3 /root/clawd/scripts/job-manager/job_state.py start "meu-job" '{"total": 10}'

# Checkpoint a cada etapa
python3 /root/clawd/scripts/job-manager/job_state.py checkpoint "meu-job" '{"processados": 3}' "Fase 1 completa"

# Finalizar
python3 /root/clawd/scripts/job-manager/job_state.py complete "meu-job" '{"resultado": "ok"}'
```

### 2. SUB-AGENTES PARA TAREFAS ISOLADAS

Cada tarefa pesada deve rodar em sub-agente:
- **sessions_spawn** para tarefas que podem rodar em paralelo
- Contexto isolado = crash de um não afeta outros
- Resultados salvos em arquivo, não apenas reportados

```
sessions_spawn(
    task="Analisar arquivo X com metodologia Y, salvar em /path/resultado.json",
    label="analise-arquivo-x"
)
```

### 3. CHECKPOINT ANTES DE CADA AÇÃO PESADA

Antes de chamar LLM externo ou processar arquivo grande:
1. Salvar estado atual em JSON
2. Registrar o que vai fazer
3. Só então executar

Se crashar, o próximo "eu" sabe exatamente onde parou.

### 4. NUNCA ACUMULAR TOOL_CALLS SEM SALVAR

Se você fez mais de 5 tool calls em sequência:
- PARE
- Salve um resumo do progresso em arquivo
- Continue

Isso evita o contexto crescer indefinidamente.

### 5. COMPACTAÇÃO PROATIVA

A cada 10 tool calls ou 30 minutos:
- Resumir o que foi feito
- Salvar em `memory/YYYY-MM-DD.md`
- Liberar contexto antigo

### 6. REGRA DO SONO DO USUÁRIO

Se o usuário disse "vou dormir" ou "me avisa quando terminar":
- **OBRIGATÓRIO** usar sistema de jobs
- **OBRIGATÓRIO** salvar checkpoints
- **PROIBIDO** depender apenas do contexto de sessão

---

## 📁 Estrutura de Jobs

```
/root/clawd/jobs/
├── analise-bardin-2026-02-03.json    # Estado do job
├── analise-bardin-2026-02-03/
│   ├── job_def.json                   # Definição original
│   ├── prompts/                       # Prompts preparados
│   │   ├── task_01_prompt.md
│   │   └── task_02_prompt.md
│   └── results/                       # Resultados por tarefa
│       ├── task_01.json
│       └── task_02.json
```

---

## 🔄 Como Retomar um Job

```bash
# Ver status
python3 /root/clawd/scripts/job-manager/job_state.py status "meu-job"

# Listar jobs pendentes
python3 /root/clawd/scripts/job-manager/job_state.py list running

# Retomar
python3 /root/clawd/scripts/job-manager/orchestrator.py resume "meu-job"
```

---

## 🧠 Checklist Mental (Antes de Trabalho Longo)

- [ ] Criei job com `job_state.py start`?
- [ ] Defini checkpoints a cada etapa?
- [ ] Resultados salvam em arquivo (não só no contexto)?
- [ ] Se crashar, o próximo eu consegue retomar?
- [ ] Usuário sabe que pode sair e eu continuo?

---

## 📝 Exemplo Prático: Análise Bardin

**ERRADO (como fiz antes):**
```
1. Ler arquivo 1 → guardar na memória
2. Ler arquivo 2 → acumular na memória
3. Ler arquivo 3 → contexto explode
4. CRASH
```

**CERTO (como deve ser):**
```
1. Criar job: analise-bardin-YYYY-MM-DD
2. Para cada arquivo:
   a. Salvar checkpoint "iniciando arquivo X"
   b. Processar arquivo
   c. Salvar resultado em JSON
   d. Checkpoint "arquivo X completo"
3. Consolidar resultados (lendo JSONs, não memória)
4. Marcar job completo
```

---

*Nunca mais deixar Igor dormir esperando um trabalho que vai crashar.*
