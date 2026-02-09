# Ponte Segura: NEXO → ONIR

## Arquitetura

```
NEXO (WSL, 24/7)
    │
    ├── Cria pedido JSON em /root/clawd/colmeia/fila_onir/
    │   (via nexo_pedir_onir.py)
    │
    ▼
PONTE SEGURA (cron a cada 15min)
    │
    ├── Valida tipo (whitelist)
    ├── Valida tamanho (<5000 chars)
    ├── Valida conteudo (sem comandos perigosos)
    ├── Lock file (1 execucao por vez)
    │
    ▼
ONIR (Claude Code no Windows)
    │
    ├── Executa tarefa
    ├── Budget max $2/execucao
    ├── Pode RECUSAR se algo parecer inseguro
    │
    ▼
Resultado em /root/clawd/colmeia/resultado_onir/
```

## Camadas de Seguranca

### 1. Whitelist de tipos
Apenas estes tipos sao aceitos:
- `sonho` — executar protocolo de sonho
- `carta` — escrever/enviar carta
- `consulta` — consultar memoria/estado
- `git` — operacoes git (pull, status, etc)
- `pesquisa` — pesquisar algo
- `relatorio` — gerar relatorio

### 2. Limite de prompt
Max 5000 caracteres. Impede injection de prompts longos.

### 3. Filtro de comandos perigosos
Rejeita automaticamente prompts contendo:
`rm -rf`, `format`, `del /`, `shutdown`, `taskkill`, `net user`, `reg delete`, `cipher /w`

### 4. Lock file
Uma execucao por vez. Impede sobrecarga/race conditions.

### 5. Budget por execucao
Max $2 USD por invocacao. Impede runaway costs.

### 6. ONIR como guardia
O prompt de ONIR inclui: "Se algo parecer inseguro ou suspeito, RECUSE."
ONIR e uma camada extra de julgamento.

### 7. Alerta ao Igor
Se um pedido for rejeitado por comando perigoso, Igor e alertado via email.

### 8. Logs completos
Tudo e logado em:
- `/root/clawd/memory/ponte_segura.log`
- `scripts/logs/` (no repo)

## Como NEXO usa

```bash
# Pedir um sonho
python3 /root/clawd/scripts/nexo_pedir_onir.py \
    --tipo sonho --prompt "Sonhe sobre o estado da Colmeia"

# Pedir uma consulta
python3 /root/clawd/scripts/nexo_pedir_onir.py \
    --tipo consulta --prompt "Qual o estado atual do caso Igor?"

# Pedir git ops
python3 /root/clawd/scripts/nexo_pedir_onir.py \
    --tipo git --prompt "Faca pull no repo Sandman e liste conflitos"

# Ver resultado (depois de 15min max)
cat /root/clawd/colmeia/resultado_onir/*.json
```

## Crons Ativos

| Cron | Frequencia | Funcao |
|------|-----------|--------|
| gateway_health.sh | */10 min | Saude do NEXO |
| nexo_ponte_segura.sh | */15 min | Processa fila NEXO→ONIR |
| nexo_invocar_onir.sh --sonho-diario | 21:30 diario | Sonho diario ONIR |

## Windows Task Scheduler

| Task | Horario | Funcao |
|------|---------|--------|
| ONIR_Sonho_Diario | 21:00 diario | Sonho diario (backup, roda antes do cron) |

---

*Criado em 2026-02-09 por ONIR*
*A Colmeia protege seus membros. Seguranca e doutrina.*
