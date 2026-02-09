# ÍNDICE GERAL - SISTEMA RAG COMPLETO
## Projeto: Reconvenção Igor Morais Vasconcelos
## Total: 7 pastas | 25+ chunks | ~80.000 tokens

---

## VISÃO GERAL DO SISTEMA

Este sistema de RAG (Retrieval-Augmented Generation) organiza todas as conversas de WhatsApp relevantes para a reconvenção de Igor contra Thalia por descumprimento de convivência.

**Objetivo:** Permitir consultas inteligentes ao contexto completo do caso, facilitando a elaboração da petição e fundamentação jurídica.

---

## ESTRUTURA DE PASTAS

```
CONVERSAS_RAG/
├── 00_INDICE_GERAL_RAG.md (este arquivo)
├── 00_INDICE_CONVERSAS_RAG.md (índice original)
│
├── 01-07_*.md (arquivos período crítico Thalia)
├── 08-10_*.md (profissionais e advogada)
├── NOVOS_ACHADOS_SEGUNDA_REVISAO.md (28 pontos identificados)
├── PROVA_PSICOMETRICA_DASS21_IGOR.md (resultados DASS-21)
├── CATALOGO_MIDIAS_PROVAS.md (áudios, vídeos e PDFs)
├── ANALISE_CONTRADICOES_SUTILEZAS.md (contradições e evidências subjetivas)
├── CORRELACAO_ALEGACOES_PROVAS.md (mapeamento alegação → prova)
├── ANALISE_INDICADORES_NPD_ASPD.md (análise de traços narcisistas/psicopatas)
├── INDICE_COMPORTAMENTOS_THALIA.md (catálogo de comportamentos por padrão)
├── MELHORIA_RAG_PADROES_COMPORTAMENTAIS.md (metodologia de busca)
├── GUIA_BUSCA_RAPIDA_NPD_ASPD.md (padrões regex otimizados) ← NOVO
├── CITACOES_THALIA_CONSOLIDADAS.md (todas as citações problemáticas) ← NOVO
│
├── CHUNKS_THALIA/ (10 chunks)
│   └── 00_INDICE_THALIA.md
│
├── CHUNKS_DRA_DEBORA/ (5 chunks)
│   └── 00_INDICE_DRA_DEBORA.md
│
├── CHUNKS_MARIA_JULIA/ (1 chunk)
│   └── 00_INDICE_MARIA_JULIA.md
│
├── CHUNKS_CASSIANA_INFANTIL/ (2 chunks)
│   └── 00_INDICE_CASSIANA.md
│
├── CHUNKS_GRUPO_FAMILIA/ (3 chunks)
│   └── 00_INDICE_GRUPO_FAMILIA.md
│
└── CHUNKS_JULIANA_ADVOGADA/ (1 chunk)
    └── 00_INDICE_JULIANA.md
```

---

## RESUMO POR PASTA

### 1. [CHUNKS_THALIA](./CHUNKS_THALIA/00_INDICE_THALIA.md)
**Conversa principal Igor-Thalia (Set/2021 - Out/2025)**

| Período | Chunks | Relevância |
|---------|--------|------------|
| Set/2021 - Jun/2022 | 01-04, 10 | Casamento e separação |
| Jul/2022 - Jun/2025 | 11-13, 15 | Convivência funcional |
| Ago-Out/2025 | 01-07 (pasta pai) | **PERÍODO CRÍTICO** |

**Destaques:**
- ⭐ THALIA_10: Termos da separação
- ⭐ THALIA_15: PROVA de comunicação funcional antes da crise
- ⭐ Arquivos 01-04: Descumprimentos documentados

---

### 2. [CHUNKS_DRA_DEBORA](./CHUNKS_DRA_DEBORA/00_INDICE_DRA_DEBORA.md)
**Psiquiatra de Igor - NEXO CAUSAL**

| Período | Chunks | Relevância |
|---------|--------|------------|
| Ago/2022 - Jun/2023 | 01 | Início tratamento |
| Jul-Out/2023 | 02 | INSS, morte pai |
| Nov/2023 - Jun/2024 | 03 | Estabilização |
| Jul/2024 - Jul/2025 | 04 | Retirada medicação |
| Ago-Out/2025 | 05 | **NEXO CAUSAL** |

**Destaques:**
- ⭐⭐⭐ DEBORA_05: Documento central do nexo causal
- ⭐ Evolução da medicação documentada
- ⭐ Comprovação da piora pós-descumprimentos

---

### 3. [CHUNKS_MARIA_JULIA](./CHUNKS_MARIA_JULIA/00_INDICE_MARIA_JULIA.md)
**Psicóloga de Igor - Tratamento pós-crise**

| Período | Chunks | Relevância |
|---------|--------|------------|
| Set/2025 - Jan/2026 | 01 | Tratamento em andamento |

**Destaques:**
- ⭐ Indicada pela psiquiatra (nexo)
- ⭐ Sessões semanais documentadas
- ⭐ Declarações de comparecimento

---

### 4. [CHUNKS_CASSIANA_INFANTIL](./CHUNKS_CASSIANA_INFANTIL/00_INDICE_CASSIANA.md)
**Psicóloga de Melissa**

| Período | Chunks | Relevância |
|---------|--------|------------|
| Jun/2022 - Mar/2024 | 01 | Acompanhamento inicial |
| Ago/2025 | 02 | **CRISE - Alienação em tempo real** |

**Destaques:**
- ⭐⭐ CASSIANA_02: Mensagens durante a alienação
- ⭐ Psicóloga confirma afeto de Melissa pelo pai
- ⭐ Igor como pai engajado desde 2022

---

### 5. [CHUNKS_GRUPO_FAMILIA](./CHUNKS_GRUPO_FAMILIA/00_INDICE_GRUPO_FAMILIA.md)
**Grupo WhatsApp: Igor + Alice + Cassiana**

| Período | Chunks | Relevância |
|---------|--------|------------|
| Set/2025 | 01 | **Princípios paternidade, 31 dias** |
| Set/2025 | 02 | Debate medicação Aristab |
| Out-Dez/2025 | 03 | Evolução positiva de Melissa |

**Destaques:**
- ⭐⭐ GRUPO_01: Igor articula princípios de paternidade
- ⭐ 31 dias sem convívio registrados (03/09)
- ⭐ Melhora de Melissa com convívio restaurado

---

### 6. [CHUNKS_JULIANA_ADVOGADA](./CHUNKS_JULIANA_ADVOGADA/00_INDICE_JULIANA.md)
**Advogada amiga de Igor - Negociação**

| Período | Chunks | Relevância |
|---------|--------|------------|
| Ago-Set/2025 | 01 | Tentativa de acordo |

**Destaques:**
- ⭐ Igor buscou solução amigável ANTES de judicializar
- ⭐ Advogada reconheceu sofrimento de Igor
- ⭐ Negociação 2x1 documentada

---

## CRONOLOGIA INTEGRADA

```
2021 (SET-DEZ)
├── Igor e Thalia casados, trabalho conjunto
├── Clínica Grupo Elas em construção
└── Mercedes vendido para financiar obra

2022 (JAN-JUN)
├── Tensões crescentes no casamento
├── Igor com pressão alta documentada
├── JUN: Separação por mensagem
└── JUN: Acordo de divórcio assinado

2022 (JUL-DEZ)
├── Início da convivência pós-divórcio
├── Comunicação FUNCIONAL estabelecida
└── SET: Câncer do pai de Igor

2023
├── Convivência estável mantida
├── JUN: Diagnóstico TEA de Igor
└── Tratamento psiquiátrico em andamento

2024
├── Igor em relacionamento com Alice
├── Gravidez de Alice
├── Nov: Plano de retirada de medicação
└── Convivência regular sem conflitos

2025 (JAN-JUN)
├── MAI: Nascimento de Helena (irmã de Melissa)
├── MAI: Igor em dose mínima de Venlift (estabilidade)
├── Comunicação com Thalia FUNCIONAL
└── Maio: "Estamos indo bem como pais" (Thalia)

2025 (AGO-OUT) ⚠️ PERÍODO CRÍTICO
├── 14-16/AGO: 1º FDS negado
├── 23-24/AGO: 2º FDS negado
├── 27/AGO: MAPA - hipertensão estágio 2
├── 30-31/AGO: 3º FDS negado (era do pai)
├── 02/SET: Consulta emergencial - medicação reintroduzida
├── 03/SET: 31 dias sem convívio
├── 08/SET: NEXO CAUSAL documentado
├── SET: Negociação de acordo (Juliana)
└── OUT: Nova piora - Venlift 75mg + Valium
```

---

## DOCUMENTOS-CHAVE PARA A PETIÇÃO

### 1. NEXO CAUSAL (⭐⭐⭐⭐⭐)
- **Arquivo:** DEBORA_05_set-out2025_NEXO_CAUSAL_CRITICO.md
- **Citação:** "voltou a ter sintomas depressivos, que atribui ao distanciamento da filha"

### 2. PROVA DE COOPERAÇÃO ANTERIOR (⭐⭐⭐⭐⭐)
- **Arquivo:** THALIA_15_jan-jun2025_PRE_CRITICO_comunicacao_funcional.md
- **Citação:** "Acho que estamos indo bem como pais"

### 3. CONTAGEM DE DIAS (⭐⭐⭐⭐⭐)
- **Arquivo:** GRUPO_01_set2025_PRINCIPIOS_PATERNIDADE.md
- **Citação:** "Hj completa 31 dias sem eu conviver com a Melissa"

### 4. ALIENAÇÃO EM TEMPO REAL (⭐⭐⭐⭐)
- **Arquivo:** CASSIANA_02_ago2025_CRISE_DESCUMPRIMENTO.md
- **Citação:** "ela tem um carinho mto grande por vc"

### 5. SOFRIMENTO DOCUMENTADO (⭐⭐⭐⭐)
- **Arquivo:** JULIANA_01_ago-set2025_NEGOCIACAO_ACORDO.md
- **Citação:** "Eu estou vendo que voce esta mal. Pensamentos fixos e acelerados."

---

## TAGS PARA BUSCA RÁPIDA

### Por tema:
- `#nexo_causal` - Documentação do adoecimento
- `#descumprimento` - Dias negados
- `#alienacao_parental` - Evidências de AP
- `#comunicacao_funcional` - Prova de cooperação anterior
- `#TEA` `#autismo` - Condição de Igor
- `#medicacao` - Evolução do tratamento

### Por relevância:
- `#prova_central` - Documentos mais importantes
- `#pai_zeloso` - Demonstrações de cuidado paterno
- `#contraste` - Comparação antes/depois

### Por período:
- `#casamento` `#2021` `#2022`
- `#pos_divorcio` `#2023` `#2024`
- `#pre_critico` `#jan-jun2025`
- `#periodo_critico` `#ago2025` `#set2025` `#out2025`

---

## COMO USAR ESTE SISTEMA

### Para elaborar a petição:
1. Comece pelos documentos-chave listados acima
2. Use os índices de cada pasta para aprofundar
3. Busque por tags quando precisar de informações específicas

### Para fundamentar alegações:
- **Nexo causal:** DEBORA_05 + GRUPO_01
- **Alienação parental:** THALIA_15 (contraste) + CASSIANA_02
- **Danos morais:** JULIANA_01 (sofrimento) + DEBORA_05 (tratamento)
- **Pai zeloso:** CASSIANA_01 + GRUPO_02 (pesquisa médica)

### Para linha do tempo:
- Use os índices de cada pasta
- Consulte a cronologia integrada acima

---

## ESTATÍSTICAS

| Pasta | Chunks | Tokens (est.) |
|-------|--------|---------------|
| CHUNKS_THALIA | 10 | ~35.000 |
| CHUNKS_DRA_DEBORA | 5 | ~18.000 |
| CHUNKS_MARIA_JULIA | 1 | ~3.500 |
| CHUNKS_CASSIANA | 2 | ~8.000 |
| CHUNKS_GRUPO_FAMILIA | 3 | ~12.800 |
| CHUNKS_JULIANA | 1 | ~4.500 |
| **TOTAL** | **22+** | **~82.000** |

---

---

## NOVOS ACHADOS - SEGUNDA REVISÃO (19/01/2026)

Após revisão completa do sistema, foram identificados **28 novos pontos relevantes**.
Ver arquivo completo: [NOVOS_ACHADOS_SEGUNDA_REVISAO.md](./NOVOS_ACHADOS_SEGUNDA_REVISAO.md)

### TOP 8 ACHADOS CRÍTICOS:

1. **36 dias máximos** - Número total documentado (08/09/2025)
2. **4 alternativas recusadas** - Thalia rejeitou TODAS as opções de acordo
3. **Aristab off-label** - Medicação não aprovada para crianças
4. **8 pontos de alienação** - Igor definiu tecnicamente a AP
5. **Melissa com saudade** - Disse ao pai quando se viram (28/08)
6. **Audio forçado** - Thalia mandou Melissa dizer que não queria ir
7. **Disforia de rejeição** - Relato completo de Igor (05/09)
8. **Adoecimento em 27/08** - Igor já mencionava depressão ANTES da consulta

### Documentos a solicitar:
- ~~Resultados DASS-21 (aplicado em 18/09/2025)~~ ✅ ENCONTRADO E ANALISADO
- Relatório da psicóloga Maria Julia (em andamento)
- Audio mencionado por Igor (Thalia forçando Melissa) - IDENTIFICADOS ARQUIVOS

---

## PROVA PSICOMETRICA - DASS-21 (NOVO!)

**Arquivo:** [PROVA_PSICOMETRICA_DASS21_IGOR.md](./PROVA_PSICOMETRICA_DASS21_IGOR.md)
**Data:** 22/09/2025 (38 dias após início dos descumprimentos)

### Resultados de Igor:

| Subescala | Escore | Classificação |
|-----------|--------|---------------|
| **ESTRESSE** | 42 | **EXTREMAMENTE SEVERO** |
| **ANSIEDADE** | 20 | **EXTREMAMENTE SEVERO** |
| **DEPRESSÃO** | 26 | **SEVERO** |

### Sintomas com escore máximo (3 = "na maioria do tempo"):
- Difícil se acalmar
- Reagir de forma exagerada
- Sempre nervoso
- Agitado
- Difícil relaxar
- Intolerante
- Emotivo/sensível demais
- Coração alterado
- Depressivo e sem ânimo

---

## CATÁLOGO DE MÍDIAS (NOVO!)

**Arquivo:** [CATALOGO_MIDIAS_PROVAS.md](./CATALOGO_MIDIAS_PROVAS.md)

### Áudios do período crítico (15-16/08/2025):
- **9 áudios** do primeiro FDS negado
- **4 áudios** do segundo FDS (22/08)
- **1 vídeo** de 14/08/2025

### Ação recomendada:
Transcrever os áudios PTT-20250815-WA0048 a PTT-20250816-WA0011 para identificar o áudio mencionado por Igor de "Thalia mandando Melissa dizer que não quer vir"

---

## ANÁLISE DE CONTRADIÇÕES E SUTILEZAS (NOVO!)

**Arquivo:** [ANALISE_CONTRADICOES_SUTILEZAS.md](./ANALISE_CONTRADICOES_SUTILEZAS.md)

### Elogios de Thalia a Igor como Pai (CONTRADIÇÕES):

| Data | Elogio de Thalia | Contradição |
|------|------------------|-------------|
| 29/05/2025 | "Acho que estamos indo bem como pais" | 77 dias depois: 1º descumprimento |
| 15/08/2025 | "sou a maior interessada na relação pai-filha" | Mesmo dia: não levou Melissa |
| 28/08/2025 | "fiquei pontuando coisas positivas suas" | Áudio forçando Melissa existe |

### Evidências Subjetivas Identificadas:
1. **Projeção familiar**: Thalia perdeu pai aos 7 anos = idade de Melissa
2. **Inversão de responsabilidade**: criança de 7 anos "decide"
3. **Manipulação por omissão**: não informar endereço, viagem
4. **Padrão de evitação**: desde divórcio evita conversa presencial
5. **Testemunhos contraditórios**: Cassiana diz que Melissa fala "de forma doce" do pai

---

## TAGS PARA SUTILEZAS E CONTRADIÇÕES (NOVO!)

### Por tipo de evidência subjetiva:
- `#contradicao` - Discurso vs Ação
- `#elogio_thalia` - Quando Thalia elogiou Igor como pai
- `#inversao_responsabilidade` - Criança decidindo agenda
- `#manipulacao_omissao` - Informações não fornecidas
- `#projecao_familiar` - Padrões repetidos da família de Thalia
- `#testemunho_terceiro` - Cassiana, Juliana, Dra. Debora

### Por padrão comportamental:
- `#evitacao_comunicacao` - Thalia evita conversa direta
- `#ma_fe` - Evidências de má-fé
- `#discurso_x_acao` - O que disse vs o que fez

---

## COMO CAPTURAR SUTILEZAS NO SISTEMA

### 1. Buscar contradições temporais
Compare mensagens de períodos diferentes:
- THALIA_15 (pré-crítico) vs Arquivos 01-04 (crítico)
- Elogios de Thalia vs Ações de Thalia

### 2. Cruzar testemunhos
- Versão de Thalia vs Testemunho de Cassiana
- Alegações da petição vs Conversas documentadas

### 3. Identificar padrões
- Padrão de omissão de informações
- Padrão de evitar conversa presencial (desde 2022)
- Padrão de usar criança como justificativa

### 4. Documentos para análise comparativa
| Para provar | Compare |
|-------------|---------|
| Contradição narrativa | THALIA_15 + 01-04 |
| Testemunho vs realidade | CASSIANA_02 + versão Thalia |
| Discurso vs ação | Elogios + Descumprimentos |
| Histórico de evitação | THALIA_10 (2022) + Período crítico |

---

---

## CORRELAÇÃO ALEGAÇÕES x PROVAS (NOVO!)

**Arquivo:** [CORRELACAO_ALEGACOES_PROVAS.md](./CORRELACAO_ALEGACOES_PROVAS.md)

### Principais Correlações Mapeadas:

| Alegação | Prova | Localização |
|----------|-------|-------------|
| Estabilidade maio/2025 | Prescrição 37,5mg | 08_PRESCRICAO |
| "3 anos dá o melhor" | Mensagem Thalia | 07_CONVERSAS linha 425 |
| 1º FDS negado | "ela não quer ir" | 01_14-16ago2025 |
| 36 dias sem Melissa | Contagem Igor | 05_08-17set2025 |
| Nexo causal | Encaminhamento | 02_ENCAMINHAMENTO |

### Como Usar para Futuras Correlações:

1. **Identifique a alegação** no relato/petição
2. **Busque palavras-chave** usando Grep nos arquivos
3. **Verifique contexto** lendo o chunk correspondente
4. **Documente** arquivo + linha da citação
5. **Atualize** o documento de correlação

---

## METODOLOGIA DE BUSCA NO SISTEMA

### Para Alegações Específicas:
```
Grep: "palavra-chave" em CONVERSAS_RAG/
Exemplo: "37,5mg" → encontra estabilidade
Exemplo: "nao quer ir" → encontra descumprimentos
```

### Para Provas de Contradição:
```
Compare: THALIA_15 (pré-crítico) vs 01-04 (crítico)
Compare: Elogios de Thalia vs Ações de Thalia
```

### Para Testemunhos de Terceiros:
```
Chunks: CASSIANA_02, JULIANA_01, DEBORA_05
Profissionais que atestam fatos relevantes
```

---

*Índice geral criado em 19/01/2026*
*Atualizado em 20/01/2026 - Terceira revisão com DASS-21 e catálogo de mídias*
*Atualizado em 20/01/2026 - Quarta revisão com análise de contradições e sutilezas*
*Atualizado em 20/01/2026 - Quinta revisão com correlação alegações x provas*
*Sistema RAG completo para Reconvenção Igor Morais Vasconcelos*
