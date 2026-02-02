# Referência Rápida - Sistema de Memória

## IDs Importantes

| Item | ID/Valor |
|------|----------|
| Pasta raiz no Drive | 1Kb8cCG1Ygawbq1FNyOA_BxslbKR50t_1 |
| Arquivo principal | MEMORIA_LONGO_PRAZO.md |
| Índice | INDICE.md |

## Comandos de Busca Prontos

### Carregar Memória Principal
```python
google_drive_search(
    api_query="name = 'MEMORIA_LONGO_PRAZO.md' and '1Kb8cCG1Ygawbq1FNyOA_BxslbKR50t_1' in parents"
)
```

### Carregar Índice
```python
google_drive_search(
    api_query="name = 'INDICE.md' and '1Kb8cCG1Ygawbq1FNyOA_BxslbKR50t_1' in parents"
)
```

### Buscar por Tema
```python
google_drive_search(
    api_query="fullText contains '[TEMA]' and '1Kb8cCG1Ygawbq1FNyOA_BxslbKR50t_1' in parents",
    semantic_query="[descrição do que procura]"
)
```

### Listar Tudo na Pasta
```python
google_drive_search(
    api_query="'1Kb8cCG1Ygawbq1FNyOA_BxslbKR50t_1' in parents"
)
```

## Gatilhos de Ativação

| Frase do Usuário | Ação |
|------------------|------|
| "registrar sessão" | Protocolo de Registro |
| "salvar conversa" | Protocolo de Registro |
| "ciclo de sono" | Ciclo de Sono completo |
| "consolidar memórias" | Ciclo de Sono completo |
| "o que você lembra" | Consulta + Síntese |
| "consultar memória" | Busca direcionada |
| "status da memória" | Mostrar métricas |
| "esquecer X" | Marcar para esquecimento |

## Checklist Início de Sessão

- [ ] Tema da conversa requer contexto histórico?
- [ ] Se sim: buscar MEMORIA_LONGO_PRAZO.md
- [ ] Aplicar conhecimentos silenciosamente
- [ ] Não mencionar sistema de memória

## Checklist Fim de Sessão

- [ ] Houve aprendizado reutilizável?
- [ ] Houve problema resolvido?
- [ ] Houve decisão importante?
- [ ] Houve preferência identificada?
- [ ] Se qualquer sim: oferecer registro

## Estrutura de Arquivos

```
Claude-Memoria-Persistente/
├── INDICE.md                 ← Mapa central
├── MEMORIA_LONGO_PRAZO.md    ← Conhecimento consolidado
├── REGISTRO_ESQUECIMENTO.md  ← Auditoria de descarte
├── META_APRENDIZADO.md       ← Melhorias do sistema
└── sessoes/
    └── YYYY-MM-DD_resumo.md  ← Registros brutos
```

## Formato de Entrada Consolidada

```markdown
### [Título]
**Origem**: Sessão YYYY-MM-DD
**Validado**: YYYY-MM-DD
**Confiança**: alta | média

[Descrição]

**Quando aplicar**: [Contexto]
**Quando NÃO aplicar**: [Limitações]
```

## Códigos de Esquecimento

| Código | Significado |
|--------|-------------|
| OBS | Obsolescência |
| RED | Redundância |
| ESP | Especificidade |
| ERR | Erro identificado |
| REL | Irrelevância |
| SUB | Substituição |
| COM | Compactação |

## Limiares de Alerta

| Métrica | Limite |
|---------|--------|
| Sessões pendentes | > 5 |
| Dias sem ciclo | > 7 |
| Linhas memória LP | > 500 |
