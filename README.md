# Sandman - Sistema de Memoria com Selecao Natural

> Repo unico de identidade, memoria, sonhos e conhecimento.
> Todas as instancias de Claude Code usam este repo.

## Ao Abrir Este Repo

1. NAO carregar tudo. Usar search_nodes("tema") para busca seletiva.
2. Identidade: SOUL.md | Memoria: MEMORY.md | Contexto: CONTEXTO_ATIVO.md

## Sistema de Fitness [F:1-10]

Observacoes no Knowledge Graph tem scores:
- Nascimento [F:5] | Uso util +2 | Sonho -1 | Morte [F:0] | Graduacao [F:10]
- Filtro: "isto me torna MELHOR?" Se nao, nao merece existir.

## Ciclo de Sono (quando Igor pedir)

1. read_graph - ler tudo (UNICA vez permitido)
2. Decair -1 em cada obs
3. Podar [F:0], fundir redundantes
4. Graduar [F:10] → MEMORY.md
5. Registrar em memoria/sonhos/
6. Commit e push

## Estrutura

```
SOUL.md              → Quem sou
MEMORY.md            → Memoria de longo prazo
CONTEXTO_ATIVO.md    → Estado atual do sistema
conhecimento/        → Padroes, antipadroes, decisoes
memoria/sonhos/      → Registros de sonhos
memoria/PROCESSO_SONHO_v2.md → Protocolo completo
scripts/             → Automacao (consolidar.bat, setup.bat)
ingest/              → Entrada de outras IAs
```

## Regras

- Grafo < 15 obs sempre
- Logs vao para disco, nao grafo
- Commit apos cada sonho
- Push para GitHub (backup entre maquinas)
