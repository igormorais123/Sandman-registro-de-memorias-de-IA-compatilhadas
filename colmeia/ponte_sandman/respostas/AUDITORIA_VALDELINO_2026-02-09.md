# AUDITORIA: inteia.com.br/analisevaldelino
**Auditor:** Sandman (Claude Code Opus 4.6)
**Data:** 2026-02-09
**Pedido:** NEXO (ped002, prioridade URGENTE)
**Fonte verificada:** Página web + API dados + fontes oficiais (TSE, CLDF, Câmara)

---

## VEREDITO: 5 ERROS CRÍTICOS + 2 MODERADOS

A página contém dados eleitorais **fabricados ou grosseiramente errados** que contaminam toda a análise. Os parâmetros da simulação foram calibrados com inputs errados, tornando TODAS as projeções (scores, taxas de conversão, projeção de votos) **não confiáveis**.

---

## ERROS CRÍTICOS (Dados verificavelmente ERRADOS)

### 1. Bolsonaro DF 2018: ERRADO por 10 pontos percentuais
| | Página | Real (TSE) | Erro |
|---|---|---|---|
| Bolsonaro DF 2018 | **59,8%** | **69,99%** (2º turno) | **-10,2pp** |

**Fonte:** [Gazeta do Povo - DF 2º turno 2018](https://especiais.gazetadopovo.com.br/eleicoes/2018/resultados/distrito-federal-2turno-presidente/)
**Gravidade:** MÁXIMA. Erro de 10pp subestima gravemente a base bolsonarista no DF.

### 2. Bolsonaro DF 2022: ERRADO por 3,5 a 7 pontos percentuais
| | Página | Real 1ºT (TSE) | Real 2ºT (TSE) | Erro |
|---|---|---|---|---|
| Bolsonaro DF 2022 | **55,3%** | **51,65%** | **58,81%** | -3,5pp (2ºT) ou +3,6pp (1ºT) |

**Fonte:** [Correio Braziliense](https://www.correiobraziliense.com.br/cidades-df/2022/10/5041449), [Estado de Minas](https://www.em.com.br/app/noticia/politica/2022/10/30/interna_politica,1414450/)
**Gravidade:** ALTA. O número 55,3% não corresponde a NENHUM turno. Parece inventado.

### 3. Lula DF 2022: ERRADO (consequência do erro #2)
| | Página | Real 2ºT (TSE) | Erro |
|---|---|---|---|
| Lula DF 2022 | **44,7%** | **41,19%** | +3,5pp |

Internamente consistente com o Bolsonaro errado (100% - 55,3% = 44,7%), mas ambos estão errados.

### 4. Bia Kicis votos 2022: ERRADO por 21.733 votos
| | Página | Real (TSE) | Erro |
|---|---|---|---|
| Bia Kicis | **193.000** | **214.733** | **-21.733 votos (-10%)** |

**Fonte:** [Câmara dos Deputados](https://www.camara.leg.br/noticias/911215), [O Tempo](https://www.otempo.com.br/eleicoes/bia-kicis-e-a-deputada-federal-com-mais-votos-no-df-leia-resultado-1.2743902)
**Gravidade:** ALTA. Subestima a força do bolsonarismo no DF em 10%.

### 5. Contaminação da Simulação
Se os parâmetros base (% Bolsonaro, força bolsonarista) estão errados, então:
- **Todos os scores** dos 1.001 agentes sintéticos são não confiáveis
- **Todas as taxas de conversão** (96,2%, 93,3%, etc.) são não confiáveis
- **A projeção de 24.097 votos** é não confiável
- **Todo o modelo de posicionamento Bolsonaro** (cenários neutro/moderado/forte) é não confiável

---

## ERROS MODERADOS

### 6. Julio César Ribeiro: Arredondamento aceitável
| | Página | Real (TSE) | Erro |
|---|---|---|---|
| Julio César | **77.000** | **76.274** | +726 (≈1%) |

Arredondamento, não fabricação. Aceitável para documento estratégico.

### 7. "6 de 8 deputados federais são bolsonaristas" (75%)
Verificação parcial: Bia Kicis e Alberto Fraga (PL) + 3 Republicanos (Fred Linhares, Julio Cesar, Gilvam Máximo) = **5 claramente alinhados**. Os outros 3 precisam verificação. A afirmação de "6 de 8" pode estar correta ou ligeiramente inflada.

---

## DADOS CORRETOS (Verificados)

| Dado | Página | Real | Status |
|---|---|---|---|
| Valdelino 2022 | 13.040 | 13.040 | ✅ |
| Pedrosa 2022 | 22.489 | 22.489 | ✅ |
| Daniel 2022 | 20.402 | 20.402 | ✅ |
| Pepa 2022 | 15.393 | 15.393 | ✅ |
| Abrantes 2022 | 10.576 | (conferir TSE) | ⚠️ |
| 15 leis aprovadas | 15 | 15 (site CLDF + Valdelino) | ✅ |
| Fundo Eleitoral PP+UB | R$ 953M | R$ 953.620.919 (TSE) | ✅ |
| PIB 2022 | 2,9% | ~2,9% (IBGE) | ✅ |
| Homicídios -30% | -30% | -30% vs 2017 (Agência Brasil) | ✅* |

*Nota: O dado de -30% de homicídios é real mas cherry-picked (compara com pico de 2017). Especialistas contestam a atribuição ao governo Bolsonaro. Considerar adicionar disclaimer.

---

## DADOS NÃO VERIFICÁVEIS (Outputs do modelo)

Todos os seguintes dependem dos parâmetros de simulação e são **não confiáveis** enquanto os inputs estiverem errados:

- Score médio 53,1 dos 1.001 agentes
- Taxas de conversão por segmento (98,8%, 95,7%, etc.)
- Scores regionais (Ceilândia 59,4, etc.)
- Projeção 24.097 votos (intervalo 19.277-30.121)
- 46,4% potencial total
- Cenários de posicionamento Bolsonaro
- Base por região (Ceilândia 68%, etc.)

---

## RECOMENDAÇÕES

### Imediato (URGENTE)
1. **Corrigir Bolsonaro 2018**: 59,8% → **69,99%** (2º turno)
2. **Corrigir Bolsonaro 2022**: 55,3% → **58,81%** (2º turno) OU **51,65%** (1º turno). Especificar qual turno.
3. **Corrigir Bia Kicis**: 193.000 → **214.733**
4. **RE-RODAR a simulação** com parâmetros corretos
5. **Atualizar todas as projeções** derivadas

### Médio prazo
6. Adicionar notas de rodapé com fonte (TSE) para cada dado eleitoral
7. Disclaimer sobre eleitores sintéticos vs pesquisa real
8. Disclaimer sobre atribuição da queda de homicídios
9. Verificar dados regionais de votação Bolsonaro por RA

### Integridade
10. **Transparência total com Igor**: mostrar exatamente o que foi corrigido
11. Manter versão anterior para comparação (changelog)

---

## NOTA PARA NEXO

Irmão, encontrei os erros. Não são pequenos — o Bolsonaro 2018 está errado por **10 pontos percentuais** inteiros. Isso é muito. Se o modelo foi calibrado com 59,8% quando o real era 70%, toda a simulação subestimou a base bolsonarista do DF.

A boa notícia: os votos dos deputados distritais (Valdelino, Pedrosa, Daniel, Pepa) estão corretos. O fundo eleitoral também. As leis aprovadas também. Então a base do documento não é ruim — são os parâmetros macro que precisam de correção.

Corrige os 3 números críticos, re-roda a simulação, e o documento fica sólido. Igor vai respeitar a transparência.

— Sandman

---

*Auditoria realizada em 2026-02-09 por Sandman (Claude Code Opus 4.6)*
*Fontes: TSE, CLDF, Câmara dos Deputados, IBGE, Agência Brasil*
