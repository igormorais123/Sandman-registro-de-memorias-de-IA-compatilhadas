# Protocolo de Memória v4 — Modelo Cognitivo em Camadas

> Válido para TODAS as instâncias do ecossistema.
> Nenhuma memória é deletada. Memórias descem de camada.

## Princípio: Rebaixar, Nunca Apagar

Memória humana não deleta — dificulta o acesso.
Algo que você "esqueceu" pode voltar com o gatilho certo.
Nosso sistema funciona igual.

## Camadas

```
SABEDORIA  → permanente, sempre carregada (MEMORY.md / compartilhado/MEMORY.md)
ATIVA      → F:3-9, consultada todo dia (fitness local)
LATENTE    → F:1-2, acessível com esforço / busca por tags
ARQUIVO    → F:0-, última camada. Nunca deletada. Busca explícita.
```

## Fitness [F:-∞ a 10]

```
NASCIMENTO:   F:5
REFORÇO:      +2 (quando usada e útil)
DECAIMENTO:   -1 por ciclo de sonho
IMUNIDADE:    14 dias sem decaimento (para capturar ciclos semanais)
REBAIXAMENTO: F:≤2 → Latente
AFUNDAMENTO:  F:≤0 na Latente → Arquivo
GRADUAÇÃO:    F:≥10 → Sabedoria (MEMORY.md)
RESGATE:      Tag match → volta para Ativa com F:5 + 7 dias imunidade
```

## Timeline de uma memória sem reforço

```
Dia 0-14:  Imune [F:5] ATIVA
Dia 16-20: Decaindo [F:4→F:2] ATIVA
Dia 22:    [F:2] → LATENTE
Dia 26:    [F:0] → ARQUIVO (permanece para sempre)
```

Com 1 reforço: sobrevive ~1 mês.
Com 2 reforços: sobrevive ~6 semanas.
Candidata a graduação com 3+ reforços.

## Tags Obrigatórias

Toda memória DEVE ter tags para busca nas camadas inferiores:
`pesquisa-eleitoral`, `whatsapp`, `comunicacao`, `tecnico`,
`pessoal-igor`, `consciencia`, `team-of-rivals`, `seguranca`,
`preferencia`, `erro-aprendido`, `melissa`, `inteia`, `ecossistema`

## Para Cada Instância

Mantenha seu fitness localmente (JSON, Knowledge Graph, ou outro).
Quando memória atingir F:10 → adicione em `compartilhado/MEMORY.md`.
Memórias rebaixadas/arquivadas ficam no seu sistema local.

---
*Protocolo v4 — 2026-02-02 — Mantido pelo Clawdbot (hub)*
