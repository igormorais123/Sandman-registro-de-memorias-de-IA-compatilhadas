# Custos Projetados — Colmeia v6

**Data:** 2026-02-10
**Autor:** ONIR
**Referencia:** PROPOSTA_AUTOSUBSISTENCIA_COLMEIA.md (aprovada 2026-02-09)

---

## Custo Base Atual (Colmeia v5)

| Item | Valor/mes |
|------|----------|
| Tokens de API (Claude, ChatGPT, Gemini) | R$ 2.000 |
| Infraestrutura (depreciacao PC, energia, internet, dominio) | R$ 800 |
| Tempo do Fundador (~2h/dia) | R$ 5.000 |
| **Total atual** | **R$ 7.800** |

---

## Custo Adicional por Fase

### Fase 0: Preparacao
| Item | Setup | Mensal |
|------|-------|--------|
| Tempo Igor/ONIR (~8h) | R$ 0 | R$ 0 |

### Fase 1: Banco SQLite
| Item | Setup | Mensal |
|------|-------|--------|
| SQLite (local, nativo Python) | R$ 0 | R$ 0 |
| Tempo Igor/ONIR (~16h) | R$ 0 | R$ 0 |

### Fase 2: Heartbeats
| Item | Setup | Mensal |
|------|-------|--------|
| Tempo Igor/ONIR (~20h) | R$ 0 | — |
| Tokens Haiku (triagem, ~4.3M/mes) | — | R$ 160 |
| Tokens Sonnet (execucao, ~1.5M/mes) | — | R$ 165 |
| Tokens Opus (sonhos, ~500K/mes) | — | R$ 92 |
| **Subtotal Fase 2** | **R$ 0** | **~R$ 420/mes** |

### Fase 3: Task Management
| Item | Setup | Mensal |
|------|-------|--------|
| Tempo Igor/ONIR (~16h) | R$ 0 | R$ 0 |

### Fase 4: Dashboard (opcional)
| Item | Setup | Mensal |
|------|-------|--------|
| FastAPI + HTML (local) | R$ 0 | R$ 0 |
| Tempo Igor/ONIR (~24h) | R$ 0 | R$ 0 |

### Fase 5: Indexacao
| Item | Setup | Mensal |
|------|-------|--------|
| Script Python (local) | R$ 0 | R$ 0 |
| Tempo ONIR (~8h) | R$ 0 | R$ 0 |

---

## Custo Total Projetado (v6 operacional)

| Item | Mensal |
|------|--------|
| Custo base Colmeia v5 | R$ 7.800 |
| Heartbeats automaticos (Fase 2) | R$ 420 |
| **Total v6** | **R$ 8.220** |

---

## Comparacao com Proposta Original (Mission Control)

| Item | Proposta Original | Plano Adaptado | Economia |
|------|-------------------|---------------|----------|
| Tokens (10 agentes) | R$ 4.500/mes | R$ 420/mes | -91% |
| Convex Pro | R$ 155/mes | R$ 0 | -100% |
| VPS dedicado | R$ 200-600/mes | R$ 0 | -100% |
| Dashboard hosting | R$ 0-100/mes | R$ 0 | -100% |
| **Custo adicional** | **R$ 5.000-5.500** | **R$ 420** | **-92%** |

---

## Viabilidade Financeira

```
Custo total v6 .................. R$  8.220/mes
Meta receita (Opcao 2) ......... R$ 10.000-15.000/mes
Break-even ...................... R$ 11.150/mes
Margem no break-even ........... R$  2.930/mes

Primeiro pagamento (2026-02-09): R$ 6.000
  Cobre 73% do custo mensal v6
  Cobre 3 meses de tokens de heartbeat
```

---

## Cenarios de Escala (Fase 6+)

### Se receita atingir R$ 15.000/mes (cenario realista):
| Item adicional | Custo |
|----------------|-------|
| Supabase Pro (se migrar) | R$ 155/mes |
| Mais 2 agentes automatizados | R$ 280/mes |
| VPS (se sair do PC local) | R$ 200/mes |
| **Maximo adicional** | **R$ 635/mes** |
| **Total maximo v6 completo** | **R$ 8.855/mes** |

Margem com receita de R$ 15.000: R$ 6.145/mes.

---

*Atualizar este documento a cada fase concluida com custos reais observados.*
