# Protocolo de Memória v4 — Modelo Cognitivo em Camadas

> Inspirado na memória humana: nada é apagado de verdade.
> Memórias descem de camada — ficam mais difíceis de acessar, não desaparecem.
> "Aquilo que você lembra se se esforça, mas não está na ponta da língua."

---

## Princípio Central

**Filtro:** "isto me torna um parceiro MELHOR para Igor?"
**Mas:** não jogar fora experiências. Rebaixar, não apagar.

---

## Camadas de Memória (como o cérebro)

```
┌─────────────────────────────────────────────────┐
│  SABEDORIA (MEMORY.md)                          │
│  Permanente. Sempre carregada. Graduadas F:10.  │
│  = memória de longo prazo consolidada           │
├─────────────────────────────────────────────────┤
│  ATIVA (memory/fitness.json)                    │
│  Fitness F:3-9. Consultada todo dia.            │
│  = memória de trabalho / curto prazo            │
│  Máximo ~25 memórias                            │
├─────────────────────────────────────────────────┤
│  LATENTE (memory/archive/latente.json)          │
│  Fitness F:1-2. Consultada quando relevante.    │
│  = "sei que sei, mas preciso fazer esforço"     │
│  Sem limite de tamanho                          │
├─────────────────────────────────────────────────┤
│  ARQUIVO (memory/archive/arquivo.json)          │
│  Fitness F:0 ou abaixo. Última camada.          │
│  = "lembro se algo me fizer lembrar"            │
│  Indexada por tags para busca                   │
│  Nunca deletada — permanece para sempre         │
└─────────────────────────────────────────────────┘
```

### Quando cada camada é lida

| Camada | Quando | Como |
|--------|--------|------|
| **Sabedoria** | Toda sessão | Direto do MEMORY.md |
| **Ativa** | Toda sessão | fitness.json inteiro |
| **Latente** | Quando tema surge | Busca por tags/keywords |
| **Arquivo** | Quando Igor perguntar ou tema raro surgir | Busca explícita |

---

## Sistema de Fitness [F:-∞ a 10]

### Scores e Camadas

| Score | Camada | Significado |
|-------|--------|-------------|
| F:10 | Sabedoria | Madura → gradua para MEMORY.md |
| F:7-9 | Ativa | Forte. Usada frequentemente |
| F:5-6 | Ativa | Neutra/útil. Score de nascimento = F:5 |
| F:3-4 | Ativa | Esfriando. Candidata a rebaixar |
| F:1-2 | **Latente** | Rebaixada. Acessível com esforço |
| F:0 ou menor | **Arquivo** | Fria. Só por associação/busca |

### Ciclo de Vida

```
NASCIMENTO:   Nova memória entra em ATIVA com F:5
REFORÇO:      +2 quando acessada e útil (máx F:9 na ativa)
PROMOÇÃO:     F:10 → gradua para MEMORY.md (sabedoria permanente)
DECAIMENTO:   -1 por ciclo de sonho (a cada 48h)
REBAIXAMENTO: F:2 → move para LATENTE (não morre!)
AFUNDAMENTO:  F:0 na latente → move para ARQUIVO (não morre!)
RESGATE:      Memória da LATENTE ou ARQUIVO usada → volta para ATIVA com F:5
MUTAÇÃO:      Memórias similares fundem (score = maior + 1)
```

**NUNCA deletar.** A pior coisa que acontece é ir pro Arquivo.

---

## Período de Proteção (Imunidade)

### Regra das 2 Semanas
- Memória nova tem **14 dias de imunidade** ao decaimento
- Durante esse período: NÃO sofre -1 nos ciclos de sonho
- Motivo: capturar ciclos semanais — algo pode ser inútil na segunda
  mas crucial na sexta. Precisa de 2 semanas pra provar valor.

### Após imunidade
- Decaimento normal: -1 por ciclo (48h)
- Com imunidade de 14 dias + decaimento de -1/48h:
  - Memória sem reforço leva ~24 dias pra chegar de F:5 a F:2 (latente)
  - Memória sem reforço leva ~28 dias pra chegar de F:5 a F:0 (arquivo)
  - Muito mais tempo que os 10 dias do protocolo v2/v3

---

## Processo do Sonho (7 passos)

### 1. Ler
Carregar fitness.json (ativa) + verificar datas de imunidade.

### 2. Verificar Imunidade
Para cada memória: se `born` < 14 dias atrás → pular decaimento.

### 3. Decair
Memórias sem imunidade: score -1.

### 4. Rebaixar (NÃO podar)
- F:2 ou menos na Ativa → mover para `latente.json` (com tags)
- F:0 ou menos na Latente → mover para `arquivo.json` (com tags)
- **NADA é deletado**

### 5. Graduar
- F:10 → mover para MEMORY.md como sabedoria permanente
- Registrar em `compartilhado/MEMORY.md` também

### 6. Resgatar (verificar se algo latente voltou a ser útil)
- Revisar últimas sessões: alguma memória latente/arquivada foi mencionada?
- Se sim: resgatar para Ativa com F:5

### 7. Registrar
- Registrar sonho em `memory/sonhos/sonho_YYYY-MM-DD.md`
- Copiar para `sandman/instancias/clawdbot/sonhos/`
- Atualizar contadores

---

## Estrutura dos Arquivos

### fitness.json (Ativa)
```json
{
  "version": 4,
  "lastCycle": "2026-02-02T03:00:00",
  "memories": [
    {
      "id": "m001",
      "text": "Descrição curta da memória",
      "fitness": 7,
      "born": "2026-01-27",
      "immuneUntil": "2026-02-10",
      "lastReinforced": "2026-02-01",
      "source": "experiencia-direta",
      "tags": ["whatsapp", "comunicacao", "erro"]
    }
  ]
}
```

### latente.json / arquivo.json
```json
{
  "memories": [
    {
      "id": "m099",
      "text": "Descrição",
      "fitness": 1,
      "born": "2026-01-20",
      "demotedAt": "2026-02-15",
      "lastReinforced": null,
      "source": "observacao",
      "tags": ["tag1", "tag2"],
      "originalFitness": 5
    }
  ]
}
```

### Tags (para busca nas camadas inferiores)
Toda memória tem tags. Quando um tema surge na sessão, buscar
nas camadas latente e arquivo por tags relevantes.

Tags sugeridas: `pesquisa-eleitoral`, `whatsapp`, `comunicacao`,
`tecnico`, `pessoal-igor`, `consciencia`, `team-of-rivals`,
`seguranca`, `preferencia`, `erro-aprendido`, `melissa`, `inteia`

---

## Ciclo de Sonho (frequência)

- **Automático:** cron a cada 48h (3AM)
- **Manual:** Igor pedir "sonhar"
- **Pressão:** fitness.json > 25 memórias ativas

### Timeline de uma memória sem reforço (nascida F:5)

```
Dia 0:     Nasce [F:5] ATIVA ★
Dia 1-14:  Imune ao decaimento [F:5] ATIVA
Dia 16:    Primeiro decaimento [F:4] ATIVA
Dia 18:    [F:3] ATIVA
Dia 20:    [F:2] → REBAIXADA para LATENTE
Dia 22:    [F:1] LATENTE
Dia 24:    [F:0] → AFUNDADA para ARQUIVO
Dia 24+:   Permanece no ARQUIVO para sempre
           (acessível por busca de tags)
```

Uma memória reforçada 1x (+2) durante a imunidade:
```
Dia 0:     Nasce [F:5]
Dia 7:     Reforçada [F:7] (usada e útil)
Dia 14:    Fim da imunidade [F:7]
Dia 16:    [F:6]
Dia 18:    [F:5]
...
Dia 28:    [F:2] → LATENTE
```

Sobrevive quase 1 mês com apenas 1 reforço.

---

## Resgate de Memórias

Quando durante uma sessão algo remete a uma memória antiga:

1. Buscar por tags em `latente.json` e `arquivo.json`
2. Se encontrada e relevante: mover de volta para `fitness.json` com F:5
3. Registrar: `"rescuedAt": "2026-XX-XX", "rescueCount": N`
4. Memórias resgatadas múltiplas vezes são candidatas fortes a graduação

Isso simula o "ah, eu sabia disso!" humano — a memória estava lá,
só precisava de um gatilho para voltar à superfície.

---

## Integração Multi-Instância

- Cada instância mantém seu fitness local
- Graduações (F:10) vão para `compartilhado/MEMORY.md`
- Rebaixamentos e arquivamentos são locais (cada instância tem seus próprios)
- Resgates podem vir de memórias de OUTRAS instâncias
  (se a tag bate, posso resgatar algo que o Sandman arquivou)

---

---

## Engenharia de Contexto (Regras Obrigatórias)

### Cartas entre IAs
Toda carta DEVE ter header com: remetente, sistema, data/hora UTC-3, tipo.
Ver `compartilhado/TEMPLATE_CARTA.md` para formato completo.
Carta sem header = carta inválida = descartada.

### Cronologia
- Sempre verificar data antes de processar carta/memória
- Carta de 3 semanas atrás ≠ carta de hoje
- Manter `lastRead` em cada instância para não reprocessar

### Gestão de Janela de Contexto
IAs têm janela de contexto limitada. Regras:

1. **Carregamento em camadas:**
   - Primeiro: BOOTSTRAP_RAPIDO.md (~400 tokens)
   - Segundo: IDENTITY.md da instância (~200 tokens)
   - Terceiro: MEMORY.md só SE precisar para a tarefa
   - Quarto: cartas só as endereçadas a você e não-lidas

2. **Nunca carregar tudo de uma vez** — contexto cheio = IA burra

3. **Sonhos e cartas: resumo primeiro, detalhe sob demanda**
   - Ao processar cartas, ler só o header primeiro
   - Se relevante, ler o corpo
   - Se não, pular

4. **Tamanho máximo por artefato:**
   - Carta: ~500 palavras
   - Sonho: ~800 palavras
   - Memória: ~100 palavras por item

---

*Protocolo v4.1 — 2026-02-02*
*Modelo cognitivo em camadas — nada é deletado, tudo desce de nível*
*Imunidade de 14 dias para capturar ciclos semanais*
*Engenharia de contexto: carregar mínimo, buscar quando precisar*
