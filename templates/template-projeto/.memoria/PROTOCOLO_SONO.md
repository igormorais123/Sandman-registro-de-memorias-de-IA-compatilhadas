# 🌙 Protocolo do Ciclo de Sono Local

> Processo de consolidação de memória para este projeto
> Executar ao final de sessões significativas ou periodicamente

---

## Comando de Ativação

```
COMANDO: Ciclo de sono
```

ou

```
COMANDO: Executar ciclo de sono
```

---

## Quando Executar

- ✅ Após completar uma feature significativa
- ✅ Ao final de um dia de trabalho intenso
- ✅ Quando resolver um bug complexo
- ✅ Antes de pausas longas no projeto
- ✅ Semanalmente em projetos ativos

---

## Fases do Ciclo

### FASE REM 1: Coleta de Fragmentos (2-3 min)

**Varrer a sessão atual procurando**:

1. Decisões tomadas (técnicas ou arquiteturais)
2. Problemas resolvidos
3. Erros cometidos e corrigidos
4. Código que funcionou bem
5. Código problemático identificado
6. Dúvidas que surgiram
7. Descobertas inesperadas

**Perguntas-guia**:
- "O que aprendi nesta sessão?"
- "Que erros cometi que não quero repetir?"
- "Que decisões tomei e por quê?"
- "O que me surpreendeu?"

---

### FASE REM 2: Processamento (3-5 min)

**Para cada fragmento coletado, avaliar**:

| Critério | Pergunta |
|----------|----------|
| Relevância | "Isso será útil no futuro?" |
| Durabilidade | "Isso continuará válido?" |
| Generalização | "Aplica-se a outras situações?" |
| Unicidade | "Já tenho isso registrado?" |

**Classificar cada item**:
- 🔴 **Descartar**: Muito específico ou temporário
- 🟡 **Memória de trabalho**: Útil a curto prazo → CONTEXTO_ATIVO.md
- 🟢 **Consolidar**: Conhecimento duradouro → MEMORIA_LONGO_PRAZO.md
- 🌐 **Candidato global**: Útil para outros projetos → marcar em SYNC_GLOBAL.md

---

### FASE REM 3: Consolidação (3-5 min)

**Executar as transferências**:

1. **Atualizar MEMORIA_LONGO_PRAZO.md**:
   - Adicionar decisões arquiteturais importantes
   - Registrar novos padrões identificados
   - Documentar soluções de problemas
   - Atualizar dependências críticas

2. **Atualizar CONTEXTO_ATIVO.md**:
   - Status atual do trabalho
   - Tarefas em andamento
   - Decisões pendentes
   - Próximos passos

3. **Atualizar APRENDIZADOS.md**:
   - Novos aprendizados
   - Erros documentados
   - Descobertas técnicas

4. **Atualizar SYNC_GLOBAL.md**:
   - Marcar candidatos para exportação
   - Verificar conhecimento importado ainda útil

---

### FASE REM 4: Limpeza (2-3 min)

**Remover**:
- Notas temporárias que já foram processadas
- Contexto obsoleto
- Debugging de problemas já resolvidos
- Tarefas completadas

**Arquivar**:
- Sessões antigas em `.memoria/sessoes/`
- Decisões substituídas (com referência à nova)

---

### FASE REM 5: Avaliação Global (1-2 min)

**Perguntar-se**:
- "Algum aprendizado de hoje é genérico para outros projetos?"
- "Alguma solução poderia ser útil universalmente?"
- "Descobri algum antipadrão que outros deveriam evitar?"
- "Algum prompt funcionou muito bem?"

**Se sim**: Adicionar a SYNC_GLOBAL.md como candidato

---

## Checklist Pós-Sono

- [ ] MEMORIA_LONGO_PRAZO.md atualizada
- [ ] CONTEXTO_ATIVO.md reflete estado real
- [ ] APRENDIZADOS.md com novos itens processados
- [ ] SYNC_GLOBAL.md com candidatos marcados (se houver)
- [ ] Arquivos temporários limpos
- [ ] Data de última consolidação atualizada

---

## Template de Registro do Sono

Adicionar a `.memoria/sono/YYYY-MM-DD.md`:

```markdown
# Ciclo de Sono - [DATA]

## Sessão(ões) Processada(s)
- [lista de sessões/período]

## Itens Consolidados
### Para Memória de Longo Prazo
1. [item]

### Para Aprendizados
1. [item]

### Candidatos para Global
1. [item]

## Itens Descartados
- [item e motivo]

## Observações
- [notas sobre o processo]

## Métricas
- Fragmentos coletados: X
- Itens consolidados: Y
- Itens descartados: Z
- Candidatos globais: W
```
