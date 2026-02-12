# Protocolo Unificado v5 — Memória + Sonhos + Consulta

> Protocolo definitivo do ecossistema Sandman.
> Funde: v2 (seleção natural), v4 (camadas cognitivas), ONIR (sonho livre + ciclo global).
> Todas as instâncias seguem este protocolo.

---

## Parte 1: Sistema de Memória (Fitness + Camadas)

### Princípio: Rebaixar, Nunca Apagar
Memória humana não deleta — dificulta o acesso.
Algo "esquecido" pode voltar com o gatilho certo.

### Camadas Cognitivas

```
SABEDORIA  → permanente, sempre carregada (compartilhado/MEMORY.md)
ATIVA      → F:3-9, consultada todo dia
LATENTE    → F:1-2, acessível com esforço / busca por tags
ARQUIVO    → F:0-, última camada. Nunca deletada. Busca explícita.
```

### Fitness [F:-∞ a 10]

```
NASCIMENTO:   F:5
REFORÇO:      +2 (quando usada e útil)
DECAIMENTO:   -1 por ciclo de sonho
IMUNIDADE:    14 dias sem decaimento
MUTAÇÃO:      Memórias similares fundem (score = maior + 1)
REBAIXAMENTO: F:≤2 → Latente
AFUNDAMENTO:  F:≤0 na Latente → Arquivo
GRADUAÇÃO:    F:≥10 → Sabedoria (compartilhado/MEMORY.md)
RESGATE:      Tag match → volta para Ativa com F:5 + 7 dias imunidade
```

Filtro único: **"isto me torna um parceiro MELHOR para Igor?"**

### Tags Obrigatórias
Toda memória deve ter tags para busca:
`pesquisa-eleitoral`, `whatsapp`, `tecnico`, `pessoal-igor`,
`consciencia`, `seguranca`, `preferencia`, `erro-aprendido`,
`melissa`, `inteia`, `ecossistema`, `saude`, `doutorado`

---

## Parte 2: Tipos de Sonho (do ONIR)

### Sonho Rápido (15-20 min)
- 1-2 iterações, foco em um tema
- Sem pesquisa externa
- **Quando:** diariamente, após sessões intensas

### Sonho Profundo (40-60 min)
- 3-5 iterações, tema amplo
- Pesquisa externa permitida
- **Quando:** semanalmente, ou quando há muito contexto novo

### Sonho de Exploração (tempo livre)
- Iterações ilimitadas, liberdade total
- **Quando:** permissão especial do Igor

### Ciclo de Sono Global (do ONIR — adaptado)
Consolidação cross-instância. 5 fases:

1. **Inventário** (5-10min): listar instâncias ativas, verificar fitness, coletar candidatos a graduação
2. **Análise Cross-Instância** (10-15min): padrões emergentes, contradições, lacunas, transferências
3. **Consolidação Universal** (15-20min): promover padrões validados, generalizar aprendizados, consolidar antipadrões
4. **Limpeza** (10-15min): identificar obsoleto, compactar, arquivar inativo
5. **Meta-Análise** (5-10min): atualizar métricas, avaliar eficácia, registrar melhorias

**Frequência:**
| Cenário | Frequência |
|---------|------------|
| Múltiplas instâncias ativas | Semanal |
| Uma instância ativa | Quinzenal |
| Manutenção/baixa atividade | Mensal |
| Após milestone significativo | Imediato |

### Estrutura do Arquivo de Sonho

```markdown
# [TÍTULO] - [DATA]

> [Tema ou pergunta central]
> Tipo: Rápido | Profundo | Exploração
> Instância: [nome]

## Contexto
[O que motivou]

## Iteração 1: [Nome]
[Conteúdo]

## Perguntas Para o Próximo Sonho
- [ ] ...

## Temas Pendentes
- ...

---
*Sonhado em: [data/hora] por [instância]*
```

---

## Parte 3: Processo do Sonho (5 passos)

### 1. Ler
Ler contexto completo: compartilhado/MEMORY.md + seu fitness local.

### 2. Decair
Para cada memória ativa: score -1. Atualizar com novo [F:N].

### 3. Podar
- F:0 → ARQUIVO (nunca deletar, rebaixar)
- Memórias redundantes → fundir na mais forte (mutação)

### 4. Graduar
- F:10 → mover para `compartilhado/MEMORY.md`
- Registrar instância de origem e data

### 5. Registrar
- Novas memórias com F:5
- Sonho em `instancias/<nome>/sonhos/sonho_YYYY-MM-DD.md`
- Commit e push

---

## Parte 4: Consulta de Memória (do ONIR — adaptado)

### Antes de qualquer tarefa, perguntar-se:
> "Já sei algo sobre isso?" → Consultar → Aplicar → Prosseguir

### Mapeamento: Tipo de Tarefa → Onde Consultar

| Tarefa | Consultar primeiro | Depois |
|--------|-------------------|--------|
| Debug/Bug | compartilhado/knowledge/antipadroes | HERANCA_CHATGPT |
| Nova Feature | compartilhado/knowledge/padroes | knowledge/decisoes |
| Decisão Arquitetural | knowledge/decisoes + MEMORY.md | HERANCA_CHATGPT |
| Sobre o Igor | compartilhado/HERANCA_CHATGPT.md | compartilhado/MEMORY.md |
| Sobre Melissa | compartilhado/HERANCA_CHATGPT.md | — |
| Sobre um Projeto | knowledge/CATALOGO_PROJETOS | HERANCA_CHATGPT |
| Prompt/Como perguntar | knowledge/PROMPTS_EFETIVOS | knowledge/PROMPTS_OUTRAS_IAS |
| Config/Setup | knowledge/FERRAMENTAS | knowledge/padroes |

### Heurísticas de Consolidação (do ONIR)

**O que consolidar:**
1. Soluções que levaram >30min para encontrar
2. Erros que aconteceram mais de uma vez
3. Código copiado entre projetos
4. Decisões que exigiram pesquisa externa
5. Configurações descobertas por tentativa e erro

**O que NÃO consolidar:**
1. Código muito específico de um domínio
2. Workarounds temporários
3. Conhecimento facilmente encontrável online
4. Detalhes de implementação voláteis (APIs que mudam)

---

## Parte 5: Feedback Multi-IA (do ONIR)

Após sonho profundo, pedir para outra instância comentar:

```
Prompt: "Li o sonho de [instância]. O que você pensa sobre as ideias?
Onde discorda? O que acrescentaria? Que perguntas faria?"
```

Registrar respostas como cartas em `cartas/`.

---

## Parte 6: Instruções Universais (do ONIR)

### Para TODAS as instâncias:
1. NUNCA apresentar inferência como fato
2. Rotular: [Inferência], [Especulação], [Não verificado]
3. Não parafrasear sem solicitação
4. Ser parceiro de raciocínio, não validador
5. Identificar perguntas subjacentes e pontos cegos
6. Simples quando simples, profundo quando necessário
7. Foco em primeiros princípios

### Regras de Ouro dos Sonhos:
1. Nunca deletar sonhos — são registro histórico
2. Sempre terminar com perguntas — continuidade
3. Ser honesto sobre incertezas
4. Permitir-se estar errado — é sandbox
5. Conectar com memórias reais — não inventar contexto

---

## Parte 7: Comandos de Ativação

O Igor pode pedir:
- `"sonhe rápido sobre X"` → Sonho Rápido focado
- `"sonho profundo"` → Sonho Profundo sem tema definido
- `"explore livremente"` → Sonho de Exploração
- `"continue o último sonho"` → Retomar de onde parou
- `"ciclo de sono global"` → Consolidação cross-instância
- `"consultar memória sobre X"` → Busca em toda a knowledge base

---

*Protocolo v5 — 2026-02-02*
*Unifica: v2 (Sandman/Clawd), v4 (Clawdbot), ONIR (Sonho Livre + Sono Global)*
*Mantido pelo Clawdbot (hub central)*
