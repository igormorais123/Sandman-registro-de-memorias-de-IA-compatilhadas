# Guia de Uso das Skills Colmeia

Este guia consolida as skills criadas para o projeto e como acionar cada uma.

---

## 1) `colmeia-doc-map-mermaid`

Quando usar:

1. Mapear documentos com Mermaid.
2. Atualizar indice completo.
3. Atualizar mapa de navegacao da pasta `colmeia/`.

Prompt de acionamento:

`Use $colmeia-doc-map-mermaid para mapear e atualizar a navegacao documental da Colmeia.`

Script util:

`powershell -ExecutionPolicy Bypass -File "skills/colmeia-doc-map-mermaid/scripts/generate_doc_index.ps1"`

Saidas principais:

1. `docs/INDICE_DOCUMENTOS_COMPLETO.md`
2. `docs/MAPA_DOCUMENTOS_MERMAID.md`
3. `colmeia/00_MAPA_GPS.md`

---

## 2) `colmeia-render-vercel-delivery`

Quando usar:

1. Implementar modulo Colmeia no backend existente.
2. Publicar frontend em `/colmeia` sem tocar a raiz.
3. Validar deploy/rollback em Render e Vercel.

Prompt de acionamento:

`Use $colmeia-render-vercel-delivery para implementar e publicar modulos da Colmeia em /colmeia.`

Contratos e referencias:

1. `docs/PLANO_IMPLANTACAO_COLMEIA.md`
2. `docs/CONTRATO_API_COLMEIA.md`
3. `docs/POLITICA_PROVIDER_ACCOUNT_FIRST.md`
4. `docs/RUNBOOK_ROLLBACK_COLMEIA.md`

---

## 3) `colmeia-agentes-research`

Quando usar:

1. Pesquisar base `C:/Agentes`.
2. Consultar Helena.
3. Fazer analise quantitativa e qualitativa por segmento.
4. Produzir respostas consultivas para a Colmeia.

Prompt de acionamento:

`Use $colmeia-agentes-research para pesquisar agentes simulados em C:/Agentes e gerar analises quanti/quali.`

Scripts uteis:

1. Inventario da base:

`powershell -ExecutionPolicy Bypass -File "skills/colmeia-agentes-research/scripts/index_agentes.ps1" -Root "C:\Agentes" -OutFile "docs/TESTE_INVENTARIO_C_AGENTES.md"`

2. Busca geral:

`powershell -ExecutionPolicy Bypass -File "skills/colmeia-agentes-research/scripts/query_agentes.ps1" -Root "C:\Agentes" -Pattern "Helena" -MaxResults 50`

3. Busca por palavra exata:

`powershell -ExecutionPolicy Bypass -File "skills/colmeia-agentes-research/scripts/query_agentes.ps1" -Root "C:\Agentes" -Pattern "Helena" -ExactWord -MaxResults 50`

Referencias da skill:

1. `skills/colmeia-agentes-research/references/modelo_entrega_pesquisa.md`
2. `skills/colmeia-agentes-research/references/governanca_operacao.md`

---

## 4) Regra de Operacao Global

1. Conta Pro primeiro.
2. API por excecao com justificativa.
3. Toda mudanca em producao deve respeitar rollback pronto antes do deploy.
