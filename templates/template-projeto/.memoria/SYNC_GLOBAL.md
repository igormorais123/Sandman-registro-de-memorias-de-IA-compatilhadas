# 🔄 Configuração de Sincronização Global

> Controla o que este projeto compartilha com a memória global

---

## Identificação do Projeto

```yaml
projeto_id: [GERAR_UUID_OU_NOME_UNICO]
nome_display: [Nome Legível do Projeto]
caminho_absoluto: [/caminho/completo/do/projeto]
data_registro_global: [YYYY-MM-DD]
tecnologias_principais: [lista, de, tecnologias]
dominio: [área de negócio ou tipo de projeto]
```

---

## Regras de Sincronização

### Exportar para Global (upload)

```yaml
exportar:
  padroes_codigo: true
  solucoes_problemas: true
  antipadroes: true
  prompts_efetivos: true
  decisoes_arquiteturais: parcial  # só as genéricas
  configuracoes: false  # muito específicas deste projeto

filtros_exportacao:
  - excluir_tag: "local-only"
  - excluir_tag: "sensivel"
  - excluir_tag: "especifico-dominio"
  - requer_tag: "consolidado"
  - requer_validacao: 2  # deve ter sido útil ao menos 2 vezes
```

### Importar do Global (download)

```yaml
importar:
  conhecimento_universal: true
  padroes_codigo:
    linguagens: [javascript, typescript, python]  # ajustar conforme projeto
  prompts_efetivos: true
  antipadroes: true
  ferramentas:
    categorias: [mcp, sdk, vscode]

filtros_importacao:
  - relevancia_minima: media
  - excluir_tecnologias: []  # tecnologias não usadas neste projeto
```

---

## Histórico de Sincronizações

| Data | Direção | Itens | Detalhes | Status |
|------|---------|-------|----------|--------|
<!-- HIST_SYNC -->

---

## Candidatos Pendentes para Exportação

> Itens identificados durante o trabalho que podem ser úteis globalmente

| Item | Origem | Tipo | Motivo Sugerido | Exportar? |
|------|--------|------|-----------------|-----------|
<!-- PENDENTES_EXPORT -->

---

## Conhecimento Importado Ativo

> Itens trazidos da memória global que estão em uso neste projeto

| Item | Origem Global | Data Import | Aplicado? | Útil? |
|------|---------------|-------------|-----------|-------|
<!-- IMPORTADOS -->

---

## Contribuições deste Projeto para o Global

> Registro histórico do que este projeto contribuiu

| Data | Tipo | Descrição | Arquivo Global |
|------|------|-----------|----------------|
<!-- CONTRIBUICOES -->

---

## Configurações Avançadas

### Sincronização Automática

```yaml
auto_sync:
  habilitado: false  # mudar para true se desejar
  frequencia: "apos_sono"  # ou "diaria", "semanal"
  apenas_exportar: false
  apenas_importar: false
```

### Notificações

```yaml
notificar:
  novos_padroes_globais: true
  novos_antipadroes: true
  conflitos: true
```
