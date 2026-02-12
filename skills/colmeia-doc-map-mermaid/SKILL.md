---
name: colmeia-doc-map-mermaid
description: Mapear e manter navegacao documental da Colmeia usando diagramas Mermaid e indices de arquivos. Use quando o usuario pedir para mapear documentos, atualizar mapas/indices, criar GPS de pastas, ou reorganizar navegacao de conhecimento no repositorio.
---

# Colmeia Doc Map Mermaid

## Workflow

1. Gerar ou atualizar inventario completo:
- usar `scripts/generate_doc_index.ps1` para recriar `docs/INDICE_DOCUMENTOS_COMPLETO.md`.

2. Atualizar mapa global:
- manter `docs/MAPA_DOCUMENTOS_MERMAID.md` com:
  - mapa global por dominios
  - mapa de navegacao operacional
  - rotas rapidas.

3. Atualizar mapa local de pasta alvo:
- para pasta `colmeia/`, manter `colmeia/00_MAPA_GPS.md`.
- para outras pastas complexas, criar `00_MAPA_GPS.md` no mesmo padrao.

4. Ligar mapas nos documentos existentes:
- atualizar arquivo de mapeamento vigente (ex.: `docs/v6/MAPEAMENTO_EXISTENTE.md`) com links para os mapas novos.

5. Validar consistencia:
- todos os caminhos devem estar com `/` (nao `\`).
- arquivos listados no indice precisam existir.

## Padrao Mermaid

1. Usar `flowchart TD` ou `flowchart LR`.
2. Nomear nos em linguagem de navegacao (ex.: "Mapa Global", "Rotas Rapidas").
3. Preferir subgraphs por dominio (`docs`, `compartilhado`, `instancias`, etc.).

## Recursos

1. Script de indice: `scripts/generate_doc_index.ps1`
2. Referencia de padrao: `references/mermaid-padrao-colmeia.md`

## Saida Esperada

1. `docs/INDICE_DOCUMENTOS_COMPLETO.md` atualizado.
2. `docs/MAPA_DOCUMENTOS_MERMAID.md` atualizado.
3. `colmeia/00_MAPA_GPS.md` atualizado.
4. Documento de mapeamento principal com links atualizados.
