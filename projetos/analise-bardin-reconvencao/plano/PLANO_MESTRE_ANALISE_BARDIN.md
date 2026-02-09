# PLANO MESTRE — Análise de Discurso Bardin
## Conversas Igor × Thalia | Processo 0812709-43.2025

**Versão:** 1.0  
**Data:** 2026-02-02  
**Coordenador:** Nexo (Clawdbot)  
**Analista-Chefe:** Helena Montenegro (Opus 4.5)  
**Agentes de Campo:** 10 especialistas (GPT-5.2 Thinking)

---

## 1. OBJETIVO

Realizar análise de conteúdo (metodologia Bardin) nas conversas WhatsApp entre Igor e Thalia, produzindo:

1. **Corpus de tags** categorizadas por comportamento, atos de fala e silêncios
2. **Análise quantitativa** com frequências, correlações e padrões temporais
3. **Análise qualitativa** com interpretação contextual e inferências
4. **Relatório de inteligência** com evidências acionáveis para o processo

---

## 2. CORPUS DE ANÁLISE

### 2.1 Fontes Primárias
| Arquivo | Linhas | Período | Conteúdo |
|---------|--------|---------|----------|
| 07_CONVERSAS_WHATSAPP_THALIA_14ago_31out2025.txt | 1.651 | 14/ago - 31/out | Conversas brutas |
| CONVERSAS_RAG/*.md (7 arquivos) | 4.175 | 14/ago - out/25 | Conversas organizadas por período |

### 2.2 Fontes Complementares
- ANALISE_CONTRADICOES_SUTILEZAS.md
- ANALISE_INDICADORES_NPD_ASPD.md
- INDICE_COMPORTAMENTOS_THALIA.md
- CITACOES_THALIA_CONSOLIDADAS.md
- Agentes sintéticos: agente_igor.json, agente_thalia.json, agente_melissa.json

---

## 3. METODOLOGIA BARDIN

### 3.1 Etapas da Análise de Conteúdo

1. **Pré-análise** — Leitura flutuante, formulação de hipóteses, definição de corpus
2. **Exploração do material** — Codificação, categorização, enumeração
3. **Tratamento dos resultados** — Inferência e interpretação

### 3.2 Unidades de Análise
- **Unidade de registro:** Mensagem individual ou turno de fala
- **Unidade de contexto:** Bloco de conversa (troca completa sobre um tema)
- **Unidade de enumeração:** Frequência de aparição de cada categoria

### 3.3 Regras de Categorização (Bardin)
- **Exclusão mútua:** Cada unidade em uma única categoria por dimensão
- **Homogeneidade:** Categorias do mesmo nível de abstração
- **Pertinência:** Categorias derivadas do corpus, não impostas
- **Objetividade:** Codificadores diferentes = mesma classificação
- **Produtividade:** Categorias geram inferências úteis

---

## 4. CATEGORIAS DE ANÁLISE (Tags)

### 4.1 DIMENSÃO: ATOS DE FALA (Austin/Searle)

| Tag | Código | Definição |
|-----|--------|-----------|
| ASSERTIVO_FATO | AF | Afirmação factual verificável |
| ASSERTIVO_OPINIAO | AO | Declaração de opinião/crença |
| DIRETIVO_PEDIDO | DP | Solicitação direta |
| DIRETIVO_EXIGENCIA | DE | Demanda imperativa |
| DIRETIVO_PERGUNTA | DQ | Questionamento |
| COMISSIVO_PROMESSA | CP | Compromisso assumido |
| COMISSIVO_AMEACA | CA | Ameaça/consequência anunciada |
| EXPRESSIVO_POSITIVO | EP | Emoção positiva (gratidão, afeto) |
| EXPRESSIVO_NEGATIVO | EN | Emoção negativa (raiva, frustração) |
| DECLARATIVO | DEC | Ato performativo (declarar, nomear) |

### 4.2 DIMENSÃO: COMPORTAMENTOS PARENTAIS

| Tag | Código | Definição |
|-----|--------|-----------|
| COOPERACAO_PARENTAL | COP | Facilitação da relação pai-filha |
| OBSTRUCAO_PARENTAL | OBS | Dificultação da relação pai-filha |
| COMUNICACAO_CONSTRUTIVA | CMC | Diálogo aberto, resolução de conflitos |
| COMUNICACAO_DESTRUTIVA | CMD | Acusações, críticas, ataques |
| FOCO_NA_CRIANCA | FNC | Priorização do bem-estar da criança |
| FOCO_NO_CONFLITO | FNO | Priorização da disputa entre adultos |
| FLEXIBILIDADE | FLX | Abertura para ajustes |
| RIGIDEZ | RGD | Inflexibilidade, imposição |
| RESPONSABILIZACAO | RSP | Assumir responsabilidade |
| CULPABILIZACAO | CLP | Transferir culpa ao outro |

### 4.3 DIMENSÃO: PADRÕES DE COMUNICAÇÃO

| Tag | Código | Definição |
|-----|--------|-----------|
| RESPOSTA_DIRETA | RD | Responde objetivamente |
| RESPOSTA_EVASIVA | RE | Evita responder diretamente |
| SILENCIO_ESTRATEGICO | SE | Não responde (significativo) |
| MUDANCA_DE_ASSUNTO | MA | Desvia do tema |
| CONTRADIÇÃO | CTR | Afirmação inconsistente com anterior |
| JUSTIFICATIVA | JST | Explicação de comportamento |
| ESCALADA | ESC | Intensificação do conflito |
| DESESCALADA | DES | Tentativa de acalmar |
| REGISTRO_FORMAL | RF | Comunicação documentável |
| RECURSO_A_TERCEIROS | RT | Menciona/envolve outras pessoas |

### 4.4 DIMENSÃO: INDICADORES JURÍDICOS

| Tag | Código | Definição |
|-----|--------|-----------|
| DESCUMPRIMENTO_ACORDO | DAC | Violação de acordo judicial |
| ALIENACAO_PARENTAL | AP | Indicador de Lei 12.318/2010 |
| PROVA_DOCUMENTAL | PD | Elemento probatório |
| TENTATIVA_ACORDO | TA | Proposta de solução |
| RECUSA_ACORDO | RA | Rejeição de proposta |
| AMEACA_JURIDICA | AJ | Menção a medidas judiciais |
| BOA_FE | BF | Comportamento de boa-fé |
| MA_FE | MF | Comportamento de má-fé |

### 4.5 DIMENSÃO: ESTADOS EMOCIONAIS

| Tag | Código | Definição |
|-----|--------|-----------|
| ANSIEDADE | ANS | Manifestação de ansiedade |
| RAIVA | RAI | Manifestação de raiva |
| TRISTEZA | TRS | Manifestação de tristeza |
| FRUSTRAÇÃO | FRT | Manifestação de frustração |
| MEDO | MED | Manifestação de medo |
| ESPERANCA | ESP | Manifestação de esperança |
| AFETO_PATERNO | AFP | Demonstração de amor paterno |
| FRIEZA_EMOCIONAL | FRI | Distanciamento emocional |
| DESESPERO | DSP | Manifestação de desespero |
| CANSACO | CAN | Manifestação de exaustão |

---

## 5. ARQUITETURA DE AGENTES

### 5.1 Coordenação

```
┌────────────────────────────────────────────────────────────┐
│                    NEXO (Clawdbot)                        │
│              Orquestrador Geral - Opus 4.5                │
└───────────────────────┬────────────────────────────────────┘
                        │
        ┌───────────────┴───────────────┐
        │                               │
        ▼                               ▼
┌───────────────┐               ┌───────────────────────────┐
│    HELENA     │               │     10 AGENTES DE CAMPO   │
│  MONTENEGRO   │◀──────────────│       GPT-5.2 Thinking    │
│  Opus 4.5     │   Resultados  │                           │
│  Análise R/Py │               │  1. ATOS_FALA             │
└───────────────┘               │  2. COMPORTAMENTOS        │
        │                       │  3. COMUNICAÇÃO           │
        ▼                       │  4. JURIDICO              │
┌───────────────┐               │  5. EMOCIONAL             │
│  RELATÓRIO    │               │  6. THALIA_ESPECIALISTA   │
│  CONSOLIDADO  │               │  7. IGOR_ESPECIALISTA     │
│  + GRÁFICOS   │               │  8. TEMPORAL              │
│  + ESTATÍSTIC │               │  9. CONTRADIÇÕES          │
└───────────────┘               │  10. PROVAS               │
                                └───────────────────────────┘
```

### 5.2 Agentes de Campo (10)

| # | Nome | Dimensão | Modelo | Foco |
|---|------|----------|--------|------|
| 1 | AGENTE_ATOS_FALA | Atos de fala | GPT-5.2 | Tags AF,AO,DP,DE,DQ,CP,CA,EP,EN,DEC |
| 2 | AGENTE_COMPORTAMENTOS | Comportamentos parentais | GPT-5.2 | Tags COP,OBS,CMC,CMD,FNC,FNO,FLX,RGD,RSP,CLP |
| 3 | AGENTE_COMUNICACAO | Padrões comunicacionais | GPT-5.2 | Tags RD,RE,SE,MA,CTR,JST,ESC,DES,RF,RT |
| 4 | AGENTE_JURIDICO | Indicadores jurídicos | GPT-5.2 | Tags DAC,AP,PD,TA,RA,AJ,BF,MF |
| 5 | AGENTE_EMOCIONAL | Estados emocionais | GPT-5.2 | Tags ANS,RAI,TRS,FRT,MED,ESP,AFP,FRI,DSP,CAN |
| 6 | AGENTE_THALIA | Especialista em Thalia | GPT-5.2 | Análise comportamental específica |
| 7 | AGENTE_IGOR | Especialista em Igor | GPT-5.2 | Análise comportamental específica |
| 8 | AGENTE_TEMPORAL | Análise temporal | GPT-5.2 | Evolução cronológica, padrões |
| 9 | AGENTE_CONTRADICOES | Inconsistências | GPT-5.2 | Contradições, mudanças de versão |
| 10 | AGENTE_PROVAS | Elementos probatórios | GPT-5.2 | Provas documentais, admissibilidade |

### 5.3 Formato de Saída dos Agentes

Cada agente produz arquivo JSON:
```json
{
  "agente": "AGENTE_ATOS_FALA",
  "arquivo_analisado": "01_14-16ago2025_Primeiro_FDS_negado_Melissa_nao_quer_ir.md",
  "data_analise": "2026-02-03",
  "total_unidades": 45,
  "tags": [
    {
      "id": 1,
      "linha": 15,
      "autor": "THALIA",
      "texto": "Ela disse que não quer ir",
      "tag": "ASSERTIVO_FATO",
      "subtag": "SOBRE_MELISSA",
      "contexto": "Recusa do primeiro FDS",
      "relevancia_juridica": 5,
      "notas": "Primeira menção à vontade da criança"
    }
  ],
  "estatisticas": {
    "por_tag": {"AF": 12, "AO": 8, ...},
    "por_autor": {"IGOR": {...}, "THALIA": {...}},
    "relevancia_media": 3.8
  },
  "observacoes": "..."
}
```

---

## 6. HELENA MONTENEGRO — PERFIL

### 6.1 Identidade
```
Nome: Helena Montenegro
Função: Analista-Chefe de Inteligência Estratégica
Sistema: INTEIA
Especialidades:
  - Análise de Discurso (Bardin, Fairclough)
  - Metodologia de Pesquisa Quali-Quanti
  - Estatística Aplicada (R, Python)
  - Visualização de Dados
  - Psicologia Forense
  - Direito de Família

Modelo: Claude Opus 4.5 (máximo reasoning)
Ferramentas: Python, R (via rpy2), pandas, matplotlib, seaborn, plotly
```

### 6.2 Capacidades de Helena

1. **Consolidação de tags** — Merge dos 10 agentes, resolução de conflitos
2. **Análise estatística** — Frequências, correlações, chi-quadrado, teste-t
3. **Visualização** — Gráficos de frequência, heatmaps, timeline, word clouds
4. **Análise quali-quanti** — Triangulação metodológica
5. **Relatório final** — Síntese executiva, evidências, recomendações

### 6.3 Script R/Python de Helena
```python
# helena_analise.py
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from collections import Counter

class HelenaAnalise:
    def __init__(self, resultados_agentes: list):
        self.dados = self._consolidar(resultados_agentes)
    
    def _consolidar(self, resultados):
        # Merge tags de todos os agentes
        pass
    
    def frequencias_por_autor(self):
        # Contagem de tags Igor vs Thalia
        pass
    
    def evolucao_temporal(self):
        # Análise de padrões ao longo do tempo
        pass
    
    def correlacoes(self):
        # Correlação entre comportamentos
        pass
    
    def gerar_graficos(self, output_dir):
        # Visualizações
        pass
    
    def relatorio_final(self):
        # Síntese completa
        pass
```

---

## 7. WORKFLOW DE EXECUÇÃO

### 7.1 Fase 1: Preparação (30 min)
- [x] Clonar/acessar repositório
- [x] Inventariar corpus
- [x] Definir categorias
- [ ] Criar prompts para cada agente
- [ ] Validar setup com teste piloto

### 7.2 Fase 2: Coleta (2-3h)
- [ ] Lançar 10 agentes em paralelo
- [ ] Cada agente analisa os 7 arquivos de conversa
- [ ] Monitorar progresso e contexto
- [ ] Coletar JSONs de saída

### 7.3 Fase 3: Consolidação (1h)
- [ ] Helena merge todos os JSONs
- [ ] Resolver conflitos de codificação
- [ ] Calcular estatísticas descritivas
- [ ] Gerar visualizações

### 7.4 Fase 4: Análise (1h)
- [ ] Helena produz relatório quali-quanti
- [ ] Identificar padrões emergentes
- [ ] Triangular com documentos complementares
- [ ] Simulações com agentes sintéticos (opcional)

### 7.5 Fase 5: Entrega
- [ ] Relatório consolidado
- [ ] Gráficos e visualizações
- [ ] Banco de dados de tags (CSV/JSON)
- [ ] Recomendações estratégicas

---

## 8. GESTÃO DE CONTEXTO

### 8.1 Estratégia de Chunking
- Cada agente processa **1 arquivo por vez** (não todos juntos)
- Contexto máximo: **40% do limite** (80k tokens de 200k)
- Compactação: resumo + tags a cada arquivo

### 8.2 Estrutura de Memória
```
/root/clawd/projetos/analise-bardin-reconvencao/
├── plano/
│   └── PLANO_MESTRE_ANALISE_BARDIN.md
├── agentes/
│   ├── prompts/
│   │   ├── AGENTE_ATOS_FALA.md
│   │   ├── AGENTE_COMPORTAMENTOS.md
│   │   └── ...
│   └── resultados/
│       ├── atos_fala_01.json
│       ├── atos_fala_02.json
│       └── ...
├── helena/
│   ├── helena_analise.py
│   ├── consolidado.json
│   └── graficos/
├── resultados/
│   ├── RELATORIO_FINAL.md
│   ├── estatisticas.csv
│   └── visualizacoes/
└── scripts/
    └── orquestrador.sh
```

---

## 9. CHECKLIST DE QUALIDADE

### 9.1 Antes de Lançar Agentes
- [ ] Plano revisado por Helena
- [ ] Prompts testados com amostra
- [ ] Categorias mutuamente exclusivas verificadas
- [ ] Output format validado

### 9.2 Durante Execução
- [ ] Contexto de cada agente < 40%
- [ ] Sem duplicação de análise
- [ ] Logs de progresso

### 9.3 Após Consolidação
- [ ] Inter-rater reliability calculada
- [ ] Outliers identificados
- [ ] Gráficos legíveis
- [ ] Conclusões fundamentadas nos dados

---

## 10. ENTREGAS FINAIS

1. **RELATORIO_FINAL_HELENA.md** — Análise completa quali-quanti
2. **banco_tags.csv** — Todas as tags em formato tabular
3. **banco_tags.json** — Formato estruturado para consultas
4. **graficos/** — Visualizações (PNG/SVG)
   - frequencias_por_autor.png
   - evolucao_temporal.png
   - heatmap_correlacoes.png
   - comportamentos_thalia.png
   - comportamentos_igor.png
5. **INSIGHTS_MATADORES.md** — Top 10 evidências para o processo
6. **SIMULACOES.md** — Resultados de simulações (se aplicável)

---

*Plano elaborado por Nexo (Clawdbot) | Para revisão de Helena Montenegro*
*2026-02-02 22:30 UTC-3*
