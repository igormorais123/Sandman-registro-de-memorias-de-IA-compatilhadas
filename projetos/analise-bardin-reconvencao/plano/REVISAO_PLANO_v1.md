# REVISÃO DO PLANO — Análise Crítica

**Revisor:** Nexo (auto-crítica)
**Data:** 2026-02-02

---

## PONTOS FORTES DO PLANO

1. **Metodologia sólida** — Bardin é referência em análise de conteúdo
2. **Categorização abrangente** — 50 tags cobrem múltiplas dimensões
3. **Arquitetura clara** — Separação agentes/Helena bem definida
4. **Gestão de contexto** — Limite de 40% é conservador e seguro
5. **Formato de saída padronizado** — JSON facilita consolidação

---

## PONTOS A MELHORAR

### 1. Granularidade dos Agentes
**Problema:** 10 agentes pode ser excessivo para 7 arquivos
**Solução:** Testar com 6 agentes primeiro:
- 3 por dimensão comportamental (Thalia, Igor, Dinâmica)
- 2 por tipo de análise (Atos de Fala, Jurídico)
- 1 temporal/contradições

### 2. Sobrecarga de Tags
**Problema:** 50 tags pode gerar inconsistência entre codificadores
**Solução:** 
- Fase 1: usar 20 tags essenciais
- Fase 2: expandir conforme necessidade
- Hierarquia: tags primárias (obrigatórias) + secundárias (opcionais)

### 3. Validação Cruzada
**Problema:** Sem método para resolver divergências entre agentes
**Solução:** 
- Cada mensagem crítica = 2 agentes independentes
- Discordância > 30% = revisão manual
- Inter-rater reliability mínimo: 0.7 (Cohen's Kappa)

### 4. Priorização de Arquivos
**Problema:** Tratar todos os 7 arquivos igualmente
**Solução:** Priorizar por relevância jurídica:
1. 03_23-31ago2025 (3º FDS, era do pai) — CRÍTICO
2. 04_01-07set2025 (36 dias, adoecimento) — CRÍTICO
3. 01_14-16ago2025 (1º FDS) — ALTO
4. 02_17-22ago2025 (2º FDS) — ALTO
5. Demais — MÉDIO

### 5. Output Quantitativo
**Problema:** Falta especificação de métricas exatas
**Solução:** Definir outputs obrigatórios:
- Frequência absoluta e relativa por tag
- Proporção Igor/Thalia por comportamento
- Tempo de resposta (latência)
- Taxa de resposta vs silêncio
- Evolução temporal (semana a semana)

### 6. Simulações
**Problema:** Mencionado como opcional
**Solução:** Tornar obrigatório ao menos 1 simulação:
- Mediador lê evidências → prediz reação
- Usar agente_juizo.json para validar

---

## TAGS ESSENCIAIS (20 prioritárias)

| Dimensão | Tags Prioritárias |
|----------|-------------------|
| Comportamento parental | OBS, COP, AP, FNC |
| Comunicação | RE, SE, CTR, ESC |
| Jurídico | DAC, PD, TA, MF |
| Emocional | AFP, FRI, DSP, ANS |
| Atos de fala | DE, CP, CA, EN |

---

## SEQUÊNCIA REVISADA

```
1. Preparação (20 min)
   └─ Criar prompts para 6 agentes essenciais

2. Piloto (30 min)
   └─ 1 arquivo (03_23-31ago) com 3 agentes
   └─ Validar formato de saída
   └─ Ajustar prompts se necessário

3. Execução Completa (2h)
   └─ 6 agentes × 7 arquivos = 42 análises
   └─ 7 em paralelo por vez (1 arquivo, todos agentes)

4. Consolidação Helena (45 min)
   └─ Merge JSONs
   └─ Estatísticas
   └─ Gráficos

5. Relatório Final (30 min)
   └─ Síntese quali-quanti
   └─ Top 10 evidências
   └─ Recomendações
```

---

## RECOMENDAÇÃO

Aprovar plano com as seguintes modificações:
- Reduzir de 10 para 6 agentes
- Usar 20 tags prioritárias (expandir depois)
- Adicionar fase piloto
- Tornar simulação obrigatória
- Priorizar arquivos por relevância

**Próximo passo:** Submeter a Helena Montenegro para validação metodológica.
