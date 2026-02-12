# 🗑️ Registro de Esquecimento

> Auditoria de memórias descartadas durante ciclos de sono
> Permite rastreabilidade e eventual recuperação

---

## Por que registrar o esquecimento?

1. **Auditoria**: Documentar decisões do sistema de memória
2. **Recuperação**: Possibilitar reversão em caso de erro
3. **Aprendizado**: Identificar padrões de obsolescência
4. **Transparência**: Manter histórico completo das transformações

---

## Memórias Descartadas

| Data | Origem | Conteúdo Resumido | Motivo do Descarte |
|------|--------|-------------------|-------------------|
<!-- INSERIR_ESQUECIMENTO_AQUI -->

---

## Categorias de Motivo

| Código | Motivo | Descrição |
|--------|--------|-----------|
| OBS | Obsolescência | Informação desatualizada por eventos posteriores |
| RED | Redundância | Duplicado de conhecimento já consolidado |
| ESP | Especificidade | Muito específico para ser reutilizável |
| ERR | Erro | Informação incorreta identificada posteriormente |
| REL | Irrelevância | Baixa probabilidade de uso futuro |
| SUB | Substituição | Substituído por conhecimento melhor |
| COM | Compactação | Mesclado em entrada mais abrangente |

---

## Estatísticas de Esquecimento

| Período | Total Esquecido | Por Categoria |
|---------|-----------------|---------------|
<!-- INSERIR_ESTATISTICAS_AQUI -->

---

## Notas de Recuperação

Se uma memória descartada for necessária novamente:

1. Localizar nesta tabela pelo resumo ou data
2. Buscar sessão de origem em `sessoes/`
3. Recuperar informação original
4. Reavaliar para possível reconsolidação

---

## Alertas

<!-- Memórias descartadas que podem ser relevantes novamente -->

| Data Descarte | Conteúdo | Condição para Recuperar |
|---------------|----------|-------------------------|
<!-- INSERIR_ALERTAS_AQUI -->
