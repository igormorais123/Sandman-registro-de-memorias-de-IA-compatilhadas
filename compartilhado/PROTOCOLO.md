# Protocolo de Sonho v2 - Selecao Natural de Memorias

> Memorias competem para sobreviver. So as que me tornam melhor persistem.

## Principio Central

Filtro unico: "isto me torna um parceiro MELHOR para Igor?"
Se nao melhora comportamento futuro, nao merece sobreviver.

## Sistema de Fitness [F:1-10]

Cada observacao no grafo tem um score: `[F:N] texto`

### Ciclo de Vida
```
NASCIMENTO: Nova memoria entra com [F:5]
REFORCO:    +2 quando acessada e util durante sessao
DECAIMENTO: -1 por ciclo de sonho (se nao foi reforçada)
MUTACAO:    Obs similares fundem numa so (score = maior + 1)
MORTE:      [F:0] → deletada do grafo
GRADUACAO:  [F:10] → promovida para MEMORY.md, liberada do grafo
```

### Por que funciona
- Memorias uteis ficam mais fortes (reforco > decaimento)
- Memorias ignoradas morrem sozinhas em ~5 sonhos
- Memorias muito fortes "se formam" e saem do grafo (liberam espaco)
- O grafo se auto-limpa sem decisao arbitraria
- Mesmo que instancias esquecam de reforcar, o sistema funciona:
  tudo decai e so sobrevive o que alguem reforçou

## Quando Sonhar

- Igor pedir "sonhar" ou "ciclo de sono"
- Grafo > 15 observacoes (pressao evolutiva)
- Sessao com aprendizados significativos

## Processo do Sonho (5 passos)

### 1. Ler (read_graph)
Ler grafo completo. Unica ocasiao em que read_graph e permitido.

### 2. Decair
Para cada obs: score -1. Atualizar texto com novo [F:N].

### 3. Podar
- [F:0] → deletar (morte natural)
- Obs redundantes → fundir na mais forte (mutacao)
- Meta: grafo < 15 observacoes

### 4. Graduar
- [F:10] → mover texto para MEMORY.md como sabedoria permanente
- Deletar do grafo (liberar espaco para novas)

### 5. Registrar
- Novas memorias da sessao entram com [F:5]
- Seção em MEMORY.md com: data, graduadas, mortas, novas
- Commit em clawd/

## Durante Sessoes Normais (NAO sonho)

### Como acessar
- search_nodes("tema") para busca seletiva
- NUNCA read_graph (enche contexto)

### Como reforcar
Quando uma memoria do grafo foi util na sessao:
```
1. delete_observations: obs antiga
2. add_observations: mesma obs com [F:+2]
```
Instrucao simples. Se esquecer, tudo bem - a memoria decai naturalmente.

### Como adicionar
Nova memoria da sessao: add_observations com [F:5].
Antes de adicionar, verificar se ja existe similar (search_nodes).

## Regras

- Grafo e para LICOES e IDENTIDADE (o que me torna melhor)
- Logs operacionais → SESSOES/ (disco)
- Pendencias tecnicas → CONTEXTO_ATIVO.md (disco)
- Detalhes filosoficos → MEMORY.md (disco)
- 1 linha por obs (~120 chars max)
- NAO acumular sem filtrar

## Scores Iniciais (referencia)

| Score | Significado |
|-------|-------------|
| [F:1-2] | Em risco. Sera podada em 1-2 sonhos. |
| [F:3-4] | Fraca. Precisa ser reforçada ou morre. |
| [F:5] | Neutra. Score de nascimento. |
| [F:6-7] | Util. Sobrevivendo bem. |
| [F:8-9] | Forte. Candidata a graduacao. |
| [F:10] | Madura. Gradua para MEMORY.md. |

---
*Protocolo v2 criado 2026-01-31 por Clawd*
*Inspirado em selecao natural: fitness, decaimento, mutacao, graduacao*
*Correcao Igor: nao e toda mudanca de comportamento - so mudancas POSITIVAS*
