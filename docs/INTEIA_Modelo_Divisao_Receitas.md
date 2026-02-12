# INTEIA | Modelos de Divisão de Receitas
## Análise Completa para Prestação de Serviços com IA

**Data:** 29/01/2026  
**Para:** Igor Morais Vasconcelos — Presidente INTEIA  
**Documento:** BIZ-2026-001

---

## 1. MAPEAMENTO DOS STAKEHOLDERS

| Papel | Quem | O que faz |
|-------|------|-----------|
| **Indicador Externo** | Primo, contatos políticos, parceiros | Traz o cliente, marca reunião, abre a porta |
| **Vendedor/Captador** | Igor (ou futuro comercial interno) | Vai na reunião, entende a demanda, desenha o projeto, vende |
| **Operador/Dev** | Desenvolvedor contratado | Programa no Claude Code, usa ferramentas INTEIA, entrega o produto |
| **INTEIA (empresa)** | Pessoa Jurídica | Infraestrutura, tokens, hospedagem, site, marca, gestão |
| **Fundador** | Igor | Idealizou, construiu a base, detém 100% da empresa |

---

## 2. PRÁTICAS DE MERCADO

### 2.1 Taxas de Indicação (Referral Fees)
| Setor | Faixa Típica | Observações |
|-------|-------------|-------------|
| Consultoria/TI | **5% a 15%** | Sobre o valor do contrato |
| Advocacia | 10% a 25% | Regulamentado por OAB |
| Imobiliário | 20% a 35% | Comissão padrão corretagem |
| SaaS/Software | 10% a 20% | Geralmente recorrente no 1º ano |
| Governo/Licitação | 5% a 10% | Mais sensível, exige formalização |

**Padrão de mercado para TI/consultoria: 5% a 15% do valor do contrato**

### 2.2 Comissão de Vendas (Sales Commission)
| Modelo | Faixa | Quando usar |
|--------|-------|-------------|
| Comissão simples | 10% a 20% | Vendedor externo, sem salário |
| Salário + comissão | 5% a 10% | Vendedor interno com fixo |
| Tiered (escalonado) | 10-15-20% | Aumenta conforme bate metas |
| Founder selling | 15% a 25% | Fundador vendendo = captação + venda |

### 2.3 Remuneração de Desenvolvedor
| Modelo | Faixa | Observações |
|--------|-------|-------------|
| Fee fixo por projeto | 30% a 50% do contrato | Mais previsível |
| Revenue share | 20% a 40% do lucro | Mais arriscado, mais motivador |
| Hora técnica | R$ 80 a R$ 250/h | Mercado brasileiro de IA |
| Híbrido (fixo + bônus) | Base + 10-15% do lucro | Melhor retenção |

### 2.4 Overhead da Empresa
| Item | Faixa Típica |
|------|-------------|
| Impostos (Simples Nacional) | 6% a 15,5% (faixa de faturamento) |
| Custos operacionais | 10% a 20% |
| Margem da empresa | 15% a 30% |
| Total retido pela empresa | **30% a 50%** |

---

## 3. MODELOS PROPOSTOS

### 📊 MODELO A — CONSERVADOR (Empresa Forte)
*Prioriza a saúde financeira da INTEIA*

**Base: Receita Bruta do Contrato**

```
RECEITA BRUTA .................. 100%
  (-) Impostos ................. ~10% (Simples Nacional*)
  (-) Custos diretos ........... ~5%  (tokens, hospedagem, infra)
  ─────────────────────────────────
  RECEITA LÍQUIDA .............. ~85%

DISTRIBUIÇÃO DA RECEITA LÍQUIDA:
  → Indicador Externo ......... 10%
  → Vendedor/Captador ......... 15%
  → Operador/Dev .............. 30%
  → INTEIA (empresa) .......... 45%
     ├─ Reserva/reinvestimento.. 15%
     ├─ Custos adm ............ 10%
     └─ Lucro do fundador ..... 20%
```

**Exemplo: Contrato de R$ 100.000**
| Stakeholder | % Líquido | Valor |
|-------------|-----------|-------|
| Impostos | ~10% bruto | R$ 10.000 |
| Custos diretos | ~5% bruto | R$ 5.000 |
| **Indicador Externo** | 10% | **R$ 8.500** |
| **Vendedor (Igor)** | 15% | **R$ 12.750** |
| **Operador/Dev** | 30% | **R$ 25.500** |
| **INTEIA** | 45% | **R$ 38.250** |
| └ Igor (fundador) | 20% | R$ 17.000 |

**Igor total (vendedor + fundador): R$ 29.750**

---

### 📊 MODELO B — AGRESSIVO (Atrai Talentos)
*Prioriza atrair e reter operadores/devs*

```
RECEITA LÍQUIDA (pós-impostos e custos):

  → Indicador Externo ......... 10%
  → Vendedor/Captador ......... 15%
  → Operador/Dev .............. 40%
  → INTEIA (empresa) .......... 35%
     ├─ Reserva/reinvestimento.. 10%
     ├─ Custos adm ............ 10%
     └─ Lucro do fundador ..... 15%
```

**Exemplo: Contrato de R$ 100.000**
| Stakeholder | % Líquido | Valor |
|-------------|-----------|-------|
| Impostos + custos | ~15% | R$ 15.000 |
| **Indicador Externo** | 10% | **R$ 8.500** |
| **Vendedor (Igor)** | 15% | **R$ 12.750** |
| **Operador/Dev** | 40% | **R$ 34.000** |
| **INTEIA** | 35% | **R$ 29.750** |

---

### 📊 MODELO C — FLEXÍVEL (Recomendado) ⭐
*Adapta conforme quem trouxe o cliente*

```
RECEITA LÍQUIDA (pós-impostos e custos):

CENÁRIO 1 — Com indicador externo:
  → Indicador Externo ......... 10%
  → Vendedor/Captador ......... 15%
  → Operador/Dev .............. 35%
  → INTEIA (empresa) .......... 40%

CENÁRIO 2 — Igor captou sozinho (sem indicador):
  → Indicador Externo ......... 0%
  → Vendedor (Igor) ........... 20%  (+5% absorve parte da indicação)
  → Operador/Dev .............. 35%
  → INTEIA (empresa) .......... 45%  (+5% volta pra empresa)

CENÁRIO 3 — Igor captou E operou (projeto solo):
  → Igor (tudo) ............... 55%
  → INTEIA (empresa) .......... 45%

CENÁRIO 4 — Operador também vendeu (trouxe e fez):
  → Operador/Dev .............. 50%  (absorve comissão de venda)
  → INTEIA (empresa) .......... 50%
```

**Exemplo Cenário 1: Contrato BRB R$ 150.000**
| Stakeholder | % | Valor |
|-------------|---|-------|
| Impostos + custos (~15%) | — | R$ 22.500 |
| Líquido disponível | 100% | R$ 127.500 |
| **Primo (indicador)** | 10% | **R$ 12.750** |
| **Igor (vendedor)** | 15% | **R$ 19.125** |
| **Dev/Operador** | 35% | **R$ 44.625** |
| **INTEIA** | 40% | **R$ 51.000** |
| └ Igor como fundador (~20%) | — | R$ 25.500 |
| **Igor total** | — | **R$ 44.625** |

---

### 📊 MODELO D — ESCALONADO POR VALOR
*Incentiva contratos maiores*

```
INDICADOR EXTERNO:
  Até R$ 50k ............. 12%
  R$ 50k a R$ 200k ....... 10%
  Acima de R$ 200k ........ 8%

VENDEDOR/CAPTADOR:
  Até R$ 50k ............. 15%
  R$ 50k a R$ 200k ....... 15%
  Acima de R$ 200k ........ 12%

OPERADOR/DEV:
  Até R$ 50k ............. 35%
  R$ 50k a R$ 200k ....... 35%
  Acima de R$ 200k ........ 30%

INTEIA:
  Até R$ 50k ............. 38%
  R$ 50k a R$ 200k ....... 40%
  Acima de R$ 200k ........ 50%  ← margem cresce com volume
```

---

## 4. MECANISMOS DE RETENÇÃO

### Para Operadores/Devs
| Mecanismo | Descrição |
|-----------|-----------|
| **Bônus de permanência** | +2% após 6 meses, +5% após 1 ano |
| **First refusal** | Operador tem prioridade em novos projetos |
| **Equity virtual** | Phantom shares para top performers |
| **Capacitação** | Acesso a tokens/ferramentas para projetos pessoais |
| **Revenue recorrente** | Se o produto gera receita mensal, dev ganha % contínua |

### Para Indicadores
| Mecanismo | Descrição |
|-----------|-----------|
| **Recorrência** | Comissão nos primeiros 12 meses de cada cliente |
| **Escalonamento** | 10% no 1º cliente, 12% do 2º em diante |
| **Status** | Título de "Embaixador INTEIA" |
| **Exclusividade regional** | Indicador exclusivo para setor/órgão |

---

## 5. ASPECTOS TRIBUTÁRIOS E LEGAIS

### Impostos (Simples Nacional — Anexo V: TI)
| Faixa de Faturamento (12 meses) | Alíquota Efetiva |
|----------------------------------|-----------------|
| Até R$ 180.000 | 15,50% |
| R$ 180k a R$ 360k | 18,00% |
| R$ 360k a R$ 720k | 19,50% |
| R$ 720k a R$ 1,8M | 20,50% |

**⚠️ Fator R:** Se a folha de salários ≥ 28% do faturamento, cai para o Anexo III (alíquotas menores, de 6% a 14,5%). Isso é uma vantagem de pagar bem os operadores via CLT/pró-labore.

### Formalização dos Pagamentos
| Stakeholder | Como pagar | Documento |
|-------------|-----------|-----------|
| Indicador externo | NF de PJ ou contrato de comissão | Contrato de intermediação |
| Vendedor (se não for Igor) | Comissão via NF ou folha | Contrato de representação |
| Operador/Dev | NF de PJ (ideal) | Contrato de prestação de serviço |
| INTEIA | Retenção automática | Contabilidade |

### ⚠️ Cuidados com Indicação Governamental
- **NÃO** pode ser configurado como lobby ilegal
- Formalizar como "contrato de intermediação comercial"
- O indicador deve ser PJ ou autônomo com contrato
- Manter rastro documental de todas as transações
- Consultar advogado para compliance com Lei Anticorrupção (Lei 12.846/2013)

---

## 6. RECOMENDAÇÃO FINAL

### Modelo Recomendado: **C — FLEXÍVEL** ⭐

**Por quê:**
1. **Adapta-se** a diferentes cenários (com/sem indicador, projeto solo)
2. **Justo** para todos — ninguém fica sub-remunerado
3. **Retém talentos** — 35% para o dev é acima da média de mercado
4. **Sustentável** — INTEIA mantém 40% para crescer
5. **Negociável** — o desconto do indicador vira incentivo extra

### Próximos Passos
1. ✅ Escolher modelo base
2. 📋 Criar contrato-modelo para cada tipo de stakeholder
3. 💼 Consultar contador sobre enquadramento tributário ideal
4. ⚖️ Consultar advogado sobre contrato de intermediação (indicadores)
5. 📊 Criar planilha automática de cálculo de splits
6. 🤝 Testar com o primeiro projeto (BRB?)

---

## 7. SIMULADOR RÁPIDO

### Projeto BRB — Cenário Hipotético

**Contrato:** R$ 200.000 (4 meses)  
**Modelo:** C — Flexível, Cenário 1 (com indicador)

| Item | Cálculo | Valor |
|------|---------|-------|
| Receita Bruta | — | R$ 200.000 |
| Impostos (~15%) | R$ 200k × 15% | -R$ 30.000 |
| Custos diretos (tokens, infra ~5%) | R$ 200k × 5% | -R$ 10.000 |
| **Receita Líquida** | — | **R$ 160.000** |
| | | |
| **Primo (indicador) — 10%** | R$ 160k × 10% | **R$ 16.000** |
| **Igor (vendedor) — 15%** | R$ 160k × 15% | **R$ 24.000** |
| **Dev/Operador — 35%** | R$ 160k × 35% | **R$ 56.000** |
| **INTEIA — 40%** | R$ 160k × 40% | **R$ 64.000** |
| └ Reinvestimento (15%) | R$ 160k × 15% | R$ 24.000 |
| └ Custos adm (10%) | R$ 160k × 10% | R$ 16.000 |
| └ Lucro fundador (15%) | R$ 160k × 15% | R$ 24.000 |
| | | |
| **Igor total (vendedor + fundador)** | — | **R$ 48.000** |
| **Dev total (4 meses)** | R$ 14.000/mês | **R$ 56.000** |

---

**INTEIA — Inteligência Estratégica**  
Documento gerado em 29/01/2026 — Sistema Clawd  
Classificação: INTERNO
