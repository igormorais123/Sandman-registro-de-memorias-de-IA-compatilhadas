# 📋 Templates Administrativos

Templates prontos para copiar e usar. Substitua os campos em [BRACKETS] pelos seus dados.

---

## 1. Email de Cobrança

### 📄 Template

```
Assunto: Cobrança - Fatura [NÚMERO] vencida em [DATA_VENCIMENTO]

Prezado(a) [NOME_CLIENTE],

Verificamos que a fatura nº [NÚMERO], no valor de R$ [VALOR], com vencimento em [DATA_VENCIMENTO], encontra-se em aberto em nossos registros.

Caso o pagamento já tenha sido efetuado, por gentileza desconsidere este aviso e nos envie o comprovante para baixa em nosso sistema.

Se houver alguma pendência ou dúvida sobre a cobrança, estamos à disposição para esclarecimentos.

**Dados para pagamento:**
- PIX: [CHAVE_PIX]
- Banco: [BANCO] | Ag: [AGENCIA] | CC: [CONTA]

Aguardamos retorno até [DATA_LIMITE].

Atenciosamente,
[SEU_NOME]
[EMPRESA]
[TELEFONE]
```

### 🤖 Prompt para Claude Personalizar

```
Preciso de um email de cobrança para:
- Cliente: [nome do cliente]
- Valor: R$ [valor]
- Vencimento original: [data]
- Dias em atraso: [número]
- Tom desejado: [amigável/firme/formal]

Adapte o template mantendo profissionalismo mas com o tom solicitado.
Se for 1ª cobrança, seja mais suave. Se for 3ª+, seja mais firme.
```

---

## 2. Ata de Reunião

### 📄 Template

```markdown
# ATA DE REUNIÃO

**Data:** [DATA]
**Horário:** [HORA_INÍCIO] às [HORA_FIM]
**Local/Plataforma:** [LOCAL_OU_LINK]

## Participantes
- [NOME_1] - [CARGO/FUNÇÃO]
- [NOME_2] - [CARGO/FUNÇÃO]
- [NOME_3] - [CARGO/FUNÇÃO]

## Pauta
1. [ITEM_PAUTA_1]
2. [ITEM_PAUTA_2]
3. [ITEM_PAUTA_3]

## Discussões e Deliberações

### [ITEM_PAUTA_1]
**Discussão:** [RESUMO_DO_QUE_FOI_DISCUTIDO]
**Decisão:** [O_QUE_FICOU_DECIDIDO]

### [ITEM_PAUTA_2]
**Discussão:** [RESUMO_DO_QUE_FOI_DISCUTIDO]
**Decisão:** [O_QUE_FICOU_DECIDIDO]

## Ações Definidas

| Ação | Responsável | Prazo |
|------|-------------|-------|
| [TAREFA_1] | [NOME] | [DATA] |
| [TAREFA_2] | [NOME] | [DATA] |
| [TAREFA_3] | [NOME] | [DATA] |

## Próxima Reunião
**Data:** [DATA_PRÓXIMA]
**Pauta prevista:** [TEMA]

---
*Ata elaborada por [NOME_REDATOR]*
```

### 🤖 Prompt para Claude Gerar

```
Transcrição/anotações da reunião:
"""
[Cole aqui suas anotações brutas, áudio transcrito ou pontos soltos]
"""

Gere uma ata formal de reunião com:
- Participantes identificados
- Pauta organizada
- Decisões destacadas
- Tabela de ações com responsáveis e prazos
- Data da próxima reunião se mencionada

Formato: markdown limpo e profissional.
```

---

## 3. Relatório Mensal

### 📄 Template

```markdown
# RELATÓRIO MENSAL - [MÊS/ANO]

**Período:** [DATA_INÍCIO] a [DATA_FIM]
**Elaborado por:** [NOME]
**Setor/Projeto:** [ÁREA]

---

## 📊 Resumo Executivo

[2-3 parágrafos resumindo os principais resultados, conquistas e desafios do mês]

---

## 🎯 Metas vs Realizado

| Meta | Previsto | Realizado | % | Status |
|------|----------|-----------|---|--------|
| [META_1] | [VALOR] | [VALOR] | [%] | ✅/⚠️/❌ |
| [META_2] | [VALOR] | [VALOR] | [%] | ✅/⚠️/❌ |
| [META_3] | [VALOR] | [VALOR] | [%] | ✅/⚠️/❌ |

---

## ✅ Principais Realizações

1. **[REALIZAÇÃO_1]**
   - Descrição: [DETALHES]
   - Impacto: [RESULTADO]

2. **[REALIZAÇÃO_2]**
   - Descrição: [DETALHES]
   - Impacto: [RESULTADO]

---

## ⚠️ Desafios e Obstáculos

1. **[DESAFIO_1]**
   - Causa: [MOTIVO]
   - Ação tomada: [SOLUÇÃO]
   - Status: [RESOLVIDO/EM_ANDAMENTO]

---

## 📈 Indicadores-Chave (KPIs)

- **[KPI_1]:** [VALOR] ([↑/↓][%] vs mês anterior)
- **[KPI_2]:** [VALOR] ([↑/↓][%] vs mês anterior)
- **[KPI_3]:** [VALOR] ([↑/↓][%] vs mês anterior)

---

## 📅 Previsão Próximo Mês

1. [ATIVIDADE_PLANEJADA_1]
2. [ATIVIDADE_PLANEJADA_2]
3. [ATIVIDADE_PLANEJADA_3]

---

## 💰 Resumo Financeiro (se aplicável)

| Item | Orçado | Realizado | Variação |
|------|--------|-----------|----------|
| [CATEGORIA_1] | R$ [X] | R$ [Y] | [Z]% |
| [CATEGORIA_2] | R$ [X] | R$ [Y] | [Z]% |
| **TOTAL** | R$ [X] | R$ [Y] | [Z]% |

---

*Relatório gerado em [DATA]*
```

### 🤖 Prompt para Claude Gerar

```
Dados do mês para o relatório:
- Período: [mês/ano]
- Área/Projeto: [nome]

Metas e resultados:
[liste as metas e o que foi alcançado]

Principais acontecimentos:
[liste os destaques positivos e negativos]

Números/métricas:
[inclua dados quantitativos disponíveis]

Gere um relatório mensal completo, profissional e visualmente organizado.
Destaque conquistas, seja honesto sobre desafios, e inclua próximos passos.
```

---

## 4. Planilha de Despesas

### 📄 Template (formato CSV/tabela)

```markdown
# CONTROLE DE DESPESAS - [MÊS/ANO]

## Despesas Detalhadas

| Data | Descrição | Categoria | Forma Pgto | Valor | Comprovante |
|------|-----------|-----------|------------|-------|-------------|
| [DD/MM] | [DESCRIÇÃO] | [CATEGORIA] | [PIX/CARTÃO/BOLETO] | R$ [X] | [SIM/NÃO] |
| [DD/MM] | [DESCRIÇÃO] | [CATEGORIA] | [PIX/CARTÃO/BOLETO] | R$ [X] | [SIM/NÃO] |

## Categorias

- 🏢 **Fixas:** Aluguel, internet, telefone, software
- 📦 **Operacionais:** Material, suprimentos, manutenção
- 👥 **Pessoal:** Salários, benefícios, freelancers
- 📢 **Marketing:** Ads, material promocional
- 🚗 **Transporte:** Combustível, uber, estacionamento
- 🍽️ **Alimentação:** Refeições de trabalho
- 📚 **Capacitação:** Cursos, livros, eventos
- 💼 **Diversos:** Outros

## Resumo por Categoria

| Categoria | Total | % do Total |
|-----------|-------|------------|
| Fixas | R$ [X] | [%] |
| Operacionais | R$ [X] | [%] |
| Pessoal | R$ [X] | [%] |
| **TOTAL GERAL** | **R$ [X]** | 100% |

## Observações
[NOTAS_IMPORTANTES]
```

### 🤖 Prompt para Claude Organizar

```
Minhas despesas do mês (dados brutos):
"""
[Cole aqui extratos, anotações, lista de gastos]
"""

Organize em uma planilha de controle com:
1. Tabela detalhada (data, descrição, categoria, valor)
2. Categorização automática dos gastos
3. Resumo por categoria
4. Total geral
5. Observações sobre padrões de gasto

Identifique também:
- Maiores gastos do mês
- Gastos que parecem fora do padrão
- Sugestões de economia (se houver)
```

---

## 5. Controle de Prazos

### 📄 Template

```markdown
# 📅 CONTROLE DE PRAZOS - [PERÍODO]

Atualizado em: [DATA_ATUALIZAÇÃO]

## ⏰ Urgentes (próximos 7 dias)

| Prazo | Tarefa | Responsável | Status | Prioridade |
|-------|--------|-------------|--------|------------|
| [DATA] | [TAREFA] | [NOME] | 🔴 Pendente | ALTA |
| [DATA] | [TAREFA] | [NOME] | 🟡 Em andamento | ALTA |

## 📆 Próximas 2 Semanas

| Prazo | Tarefa | Responsável | Status | Prioridade |
|-------|--------|-------------|--------|------------|
| [DATA] | [TAREFA] | [NOME] | [STATUS] | MÉDIA |

## 📅 Este Mês

| Prazo | Tarefa | Responsável | Status | Prioridade |
|-------|--------|-------------|--------|------------|
| [DATA] | [TAREFA] | [NOME] | [STATUS] | BAIXA |

## ✅ Concluídos Recentemente

| Prazo Original | Tarefa | Concluído em | Observação |
|----------------|--------|--------------|------------|
| [DATA] | [TAREFA] | [DATA] | [NOTA] |

---

## Legenda de Status
- 🔴 **Pendente** - Não iniciado
- 🟡 **Em andamento** - Trabalhando
- 🟢 **Concluído** - Finalizado
- ⚫ **Atrasado** - Passou do prazo
- ⚪ **Cancelado** - Não será feito

## Próximos Prazos Críticos
1. **[DATA]** - [DESCRIÇÃO_CURTA]
2. **[DATA]** - [DESCRIÇÃO_CURTA]
3. **[DATA]** - [DESCRIÇÃO_CURTA]
```

### 🤖 Prompt para Claude Gerenciar

```
Minhas tarefas e prazos atuais:
"""
[Liste todas suas tarefas, projetos e datas]
"""

Data de hoje: [data atual]

Monte um controle de prazos organizado por:
1. Urgência (próximos 7 dias destacados)
2. Prioridade (alta/média/baixa)
3. Status visual (emojis)

Inclua:
- Alertas para o que está atrasado ou quase vencendo
- Sugestão de ordem de execução
- Próximos 3 prazos críticos em destaque
```

---

## 💡 Dicas de Uso

1. **Copie o template** completo
2. **Substitua os [BRACKETS]** pelos seus dados
3. **Use o prompt** para Claude personalizar ou gerar do zero
4. **Salve em sua pasta** de documentos para reutilizar

---

*Templates criados para uso com Claude | Atualize conforme sua necessidade*
