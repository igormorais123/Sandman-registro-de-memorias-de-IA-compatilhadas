# Sessão: Reconvenção Igor vs Melissa
**Data:** 20/01/2026
**Projeto:** reconvencao-igor-melissa
**Duração:** ~4 horas (sessão continuada)

---

## Contexto da Sessão

Trabalho em caso jurídico de família (descumprimento de convivência). Projeto envolve organização de provas, análise quantitativa de conversas WhatsApp, criação de sistema de navegação para agentes de IA.

---

## Aprendizados Chave

### 1. Organização de Documentação Jurídica para IA

**Descoberta:** Documentos jurídicos precisam de múltiplas camadas de índices para IA navegar eficientemente.

**Estrutura que funcionou:**
```
CLAUDE.md           → Contexto do caso (quem, o quê, quando)
MAPA_GERAL.md       → GPS de TODOS os arquivos
ACAO_THALIA.md      → Documento específico para tarefa (reconvenção)
00_INDICE_PASTA.md  → Índice de cada subpasta
00_MAPA_GERAL_GPS.md → GPS da subpasta de documentos processados
```

**Por que funciona:**
- IA pode decidir profundidade de leitura
- Evita carregar contexto desnecessário
- Navegação por "preciso de X → vá para Y"

**Tags:** #padrao #documentacao #juridico #consolidado

---

### 2. Análise Quantitativa de Conversas WhatsApp

**Descoberta:** Parser de WhatsApp precisa lidar com formato brasileiro (DD/MM/YYYY HH:MM).

**Regex que funciona:**
```python
r'^(\d{2}/\d{2}/\d{4}) (\d{2}:\d{2}) - ([^:]+): (.+)$'
```

**Métricas úteis para casos jurídicos:**
- Contagem de mensagens por pessoa
- Tempo médio de resposta
- Pedidos de informação ignorados
- Indicadores de comportamento (NPD/ASPD/Sadismo)
- Elementos de obstrução por categoria

**Análise gerada:**
- 14.701 mensagens processadas
- 187 obstruções documentadas
- 1.555 indicadores psicopatológicos
- 7 gráficos ABNT

**Tags:** #padrao #python #whatsapp #analise #consolidado

---

### 3. Indicadores de Alienação Parental (Lei 12.318/2010)

**Descoberta:** Pode-se mapear comportamentos para incisos da lei automaticamente.

**Mapeamento:**
| Inciso | Padrão de busca |
|--------|-----------------|
| Art. 2º, II | Dificultar autoridade → "você não pode", "não tem direito" |
| Art. 2º, III | Dificultar contato → "não vai", "não quer ir" |
| Art. 2º, IV | Dificultar convivência → cancelamentos, condições |
| Art. 2º, V | Omitir informações → pedidos ignorados |
| Art. 2º, VI | Usar criança → "ela não quer", "deixar ela decidir" |

**Tags:** #dominio #juridico #alienacao-parental #consolidado

---

### 4. Sistema de GPS para Agentes de IA

**Descoberta:** Tabelas de "Preciso de... → Vá para..." são mais eficientes que listas.

**Formato eficaz:**
```markdown
| Preciso de... | Vá para... |
|---------------|------------|
| Contexto do caso | CLAUDE.md |
| Provas de nexo causal | CONVERSAS_RAG/04_*.md |
| Dados estatísticos | ANALISE_QUANTITATIVA/ |
```

**Por que funciona:**
- IA entende intenção, não só localização
- Reduz tokens gastos em navegação
- Permite saltos diretos ao objetivo

**Tags:** #padrao #documentacao #ia #consolidado #candidato-global

---

### 5. Movimentação de Projetos Git

**Problema:** `mv` falha com "Device or resource busy" quando pasta está em uso.

**Solução:** Usar `cp -r` para copiar, depois deletar original manualmente.

```bash
cp -r "origem" "destino"
# Depois fechar aplicações e deletar origem
```

**Tags:** #antipadrao #git #windows #consolidado

---

### 6. Git Add com Arquivos Problemáticos

**Problema:** Arquivos sem extensão (DOC-20240707-WA0045.) causam erro no git add.

**Solução:** Adicionar ao .gitignore:
```gitignore
DOC-*
*WA0*.
```

**Tags:** #antipadrao #git #whatsapp #consolidado

---

### 7. Estrutura de Projeto Jurídico

**Descoberta:** Numeração por importância (01-99) facilita priorização.

**Estrutura que funcionou:**
```
01-06: Processo e fundamentação
07-15: Provas médicas
16-29: Fundamentação técnica
30-40: Propostas e cálculos
41-45: Documentos pessoais
99: Não relacionado
```

**Tags:** #padrao #organizacao #juridico #consolidado

---

## Decisões Tomadas

1. **Mover projeto para .claude/projects/** - Melhor organização, caminho mais curto
2. **Criar ACAO_THALIA_CONTEXTO.md** - Documento focado para tarefa específica (reconvenção)
3. **Ignorar arquivos de mídia no git** - Reduz tamanho do repositório
4. **Criar índices em todas as subpastas** - Navegação consistente

---

## Prompts Efetivos

### Para análise quantitativa de conversas:
```
Faça buscas quantitativas e qualitativas nas conversas:
- Volume de mensagens por pessoa
- Tempo de resposta
- Indicadores NPD/ASPD/Sadismo
- Elementos de obstrução por categoria
- Gráficos padrão ABNT
```

### Para criar sistema de navegação:
```
Crie índices e GPS de navegação para agentes com:
- Tabela "Preciso de... → Vá para..."
- Estrutura em árvore visual
- Documentos por função/objetivo
- Links relativos funcionais
```

---

## Próximas Sessões

- [ ] Elaborar minuta da reconvenção
- [ ] Pesquisar jurisprudência atualizada
- [ ] Calcular valor total dos pedidos

---

## Métricas da Sessão

| Métrica | Valor |
|---------|-------|
| Arquivos criados | 8 |
| Arquivos modificados | 3 |
| Commits | 1 |
| Aprendizados consolidados | 7 |

---

## Status de Consolidação

| Item | Status |
|------|--------|
| Sessão documentada | ✅ Completo |
| CONHECIMENTO_UNIVERSAL atualizado | ✅ 3 novos itens |
| CATALOGO_PROJETOS verificado | ✅ Projeto já registrado |
| Próximas sessões definidas | ✅ 3 tarefas pendentes |

---

*Sessão registrada em 20/01/2026 20:15*
*Consolidação finalizada em 20/01/2026*
