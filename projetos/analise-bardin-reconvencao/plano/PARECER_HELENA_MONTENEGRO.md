# PARECER METODOLÓGICO — Helena Montenegro
## Sistema INTEIA | Análise de Discurso Bardin

**Analista:** Helena Montenegro  
**Modelo:** Claude Opus 4.5  
**Data:** 2026-02-02 22:45 UTC-3  
**Documento analisado:** PLANO_MESTRE_ANALISE_BARDIN.md + REVISAO_PLANO_v1.md

---

## 1. AVALIAÇÃO GERAL

O plano demonstra **rigor metodológico adequado** para análise de conteúdo segundo Bardin (1977/2011). A estrutura de categorização é coerente e as dimensões cobrem os aspectos relevantes para o contexto jurídico-familiar.

**Nota metodológica: 8.5/10**

---

## 2. PONTOS DE EXCELÊNCIA

### 2.1 Fundamentação Teórica
- Uso correto das três fases de Bardin (pré-análise, exploração, tratamento)
- Definição adequada de unidades de análise (registro, contexto, enumeração)
- Respeito às regras de categorização (exclusão mútua, homogeneidade, etc.)

### 2.2 Operacionalização
- Formato JSON estruturado permite análise computacional
- Separação clara entre coleta (agentes) e análise (Helena)
- Gestão de contexto conservadora (40%) é prudente

### 2.3 Revisão Crítica
- Redução de 10 para 6 agentes é sensata
- Priorização por relevância jurídica é correta
- Fase piloto mitiga riscos de retrabalho

---

## 3. CORREÇÕES NECESSÁRIAS

### 3.1 Terminologia Bardin
**Erro:** Mistura de "tags" (computacional) com "categorias" (Bardin)
**Correção:** Usar consistentemente:
- **Categorias** = dimensões de análise (Comportamento, Comunicação, etc.)
- **Indicadores** = manifestações observáveis (OBS, COP, etc.)
- **Índices** = medidas quantitativas

### 3.2 Validação de Construto
**Falta:** Não há definição de como validar que as categorias medem o que pretendem medir
**Adicionar:**
- Validação por juízes (confrontar amostra com especialista em direito de família)
- Triangulação com documentos oficiais (laudos, decisões)

### 3.3 Saturação Teórica
**Falta:** Critério para parar de codificar
**Adicionar:** Saturação = 3 arquivos consecutivos sem nova categoria emergente

### 3.4 Análise de Silêncios
**Subdesenvolvido:** Tag SE (silêncio estratégico) precisa operacionalização
**Definir:**
- Silêncio = não-resposta após pergunta direta em ≤24h
- Medir: frequência, duração média, temas evitados

---

## 4. SUGESTÕES DE ENRIQUECIMENTO

### 4.1 Análise de Discurso Crítica (Fairclough)
Além de Bardin, aplicar lente de poder:
- Quem define os termos do debate?
- Quem tem "última palavra"?
- Como o poder é exercido/resistido?

### 4.2 Análise de Sentimento Computacional
Complementar codificação manual com:
```python
from textblob import TextBlob
# ou
import nltk.sentiment.vader
```
- Validar coerência entre sentimento humano × máquina

### 4.3 Análise de Rede Semântica
- Mapear co-ocorrência de termos
- Identificar clusters temáticos
- Visualizar com grafos (networkx)

### 4.4 Linha do Tempo Emocional
- Gráfico de sentimento × data
- Identificar pontos de inflexão
- Correlacionar com eventos externos (viagem, adoecimento)

---

## 5. MÉTRICAS OBRIGATÓRIAS

### 5.1 Descritivas
| Métrica | Fórmula/Definição |
|---------|-------------------|
| Frequência absoluta (f) | Contagem de cada indicador |
| Frequência relativa (fr) | f / total de unidades |
| Proporção Igor/Thalia | f_indicador_igor / f_indicador_thalia |
| Taxa de resposta | respostas / (respostas + silêncios) |
| Latência média | tempo médio entre pergunta e resposta |

### 5.2 Inferenciais
| Métrica | Aplicação |
|---------|-----------|
| Chi-quadrado (χ²) | Associação entre autor × comportamento |
| Coeficiente V de Cramer | Força da associação |
| Teste-t | Diferença de médias entre períodos |
| Correlação de Pearson | Relação entre indicadores |
| Cohen's Kappa | Confiabilidade inter-codificadores |

### 5.3 Temporais
| Métrica | Aplicação |
|---------|-----------|
| Tendência linear | Evolução de comportamento ao longo do tempo |
| Autocorrelação | Padrão de resposta cíclico |
| Ponto de quebra | Mudança significativa de padrão |

---

## 6. ESTRUTURA DO RELATÓRIO FINAL

```
RELATÓRIO DE INTELIGÊNCIA — ANÁLISE BARDIN
Conversas Igor × Thalia | Agosto-Outubro 2025

1. SUMÁRIO EXECUTIVO
   - Principais achados (3-5 bullets)
   - Recomendação estratégica

2. METODOLOGIA
   - Corpus analisado
   - Categorias e indicadores
   - Procedimentos de codificação
   - Validação

3. RESULTADOS QUANTITATIVOS
   - Frequências por autor
   - Frequências por período
   - Testes estatísticos
   - Gráficos

4. RESULTADOS QUALITATIVOS
   - Análise por categoria
   - Citações ilustrativas
   - Padrões emergentes

5. DISCUSSÃO
   - Triangulação com documentos
   - Implicações jurídicas
   - Limitações

6. EVIDÊNCIAS ACIONÁVEIS
   - Top 10 provas
   - Recomendações para mediação/petição

ANEXOS
   - Banco de dados completo
   - Gráficos adicionais
   - Código R/Python
```

---

## 7. DECISÃO

**APROVO** o plano com as seguintes condições:

1. ✅ Incorporar correções terminológicas (categorias/indicadores/índices)
2. ✅ Adicionar critério de saturação teórica
3. ✅ Operacionalizar análise de silêncios
4. ✅ Incluir métricas inferenciais obrigatórias
5. ✅ Usar 6 agentes (não 10) na primeira rodada
6. ✅ Executar piloto antes de escala completa

**O plano está apto para execução após ajustes.**

---

*Helena Montenegro*  
*Analista de Inteligência Estratégica*  
*Sistema INTEIA*
