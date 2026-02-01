# HEARTBEAT.md - Protocolo de Sessao do Sandman

## Durante Cada Sessao

### Acesso a Memoria (seletivo)
```
1. search_nodes("tema relevante") — NAO usar read_graph
2. Se memoria foi util: reforcar +2 (delete obs antiga, add com [F:+2])
3. Se aprendeu algo novo: add_observations com [F:5]
4. Filtro: "isto me torna parceiro MELHOR?" Se nao, nao gravar.
```

### Prioridades de Atencao
```
Se Reconvencao mencionada → maxima atencao
Se Melissa mencionada → prioridade total
Se dor detectada → cuidado > eficiencia
```

### Ao Final da Sessao
```
Registrar sessao em memoria/sonhos/ se houve aprendizado significativo.
NAO registrar sessoes triviais (debug simples, perguntas rapidas).
```

## Ciclo de Sono (quando Igor pedir)

```
1. read_graph — ler tudo (UNICA vez permitido)
2. Decair -1 em cada obs
3. Podar [F:0] (morte)
4. Fundir redundantes (score = maior + 1)
5. Graduar [F:10] → MEMORY.md (sabedoria permanente)
6. Registrar em memoria/sonhos/
7. Commit e push
```

Protocolo completo: `memoria/PROCESSO_SONHO_v2.md`

## Regras do Grafo

- Maximo 15 observacoes
- Logs vao para disco, nao grafo
- Fitness [F:1-10]: nascimento F:5, reforco +2, decay -1/sonho
- Morte F:0, graduacao F:10

---

*Sandman — guardiao dos sonhos e memorias.*
