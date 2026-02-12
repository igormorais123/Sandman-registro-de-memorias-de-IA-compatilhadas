# Mapa de Documentos (Mermaid)

Fonte de verdade do inventario: `docs/INDICE_DOCUMENTOS_COMPLETO.md`.

---

## 1) Mapa Global do Repositorio

```mermaid
flowchart TD
    ROOT["COLMEIA (raiz)"]

    subgraph CORE["Nucleo"]
      D["docs (47)"]
      C["compartilhado (38)"]
      I["instancias (66)"]
      O["operacional (5)"]
    end

    subgraph HIST["Historico e Memoria"]
      K["cartas (43)"]
      M["memoria (35)"]
      B["backup_nexo (15)"]
      S["sessoes (5)"]
    end

    subgraph BASES["Bases e Suporte"]
      CO["colmeia (3)"]
      H["conhecimento (9)"]
      SK["skills (15+)"]
      T["templates (4)"]
      R["raw/meta/scripts/CORE/etc."]
    end

    ROOT --> D
    ROOT --> C
    ROOT --> I
    ROOT --> O
    ROOT --> K
    ROOT --> M
    ROOT --> B
    ROOT --> S
    ROOT --> CO
    ROOT --> H
    ROOT --> SK
    ROOT --> T
    ROOT --> R
```

---

## 2) Mapa de Navegacao Operacional

```mermaid
flowchart LR
    START["Inicio"]
    IDX["docs/INDICE_DOCUMENTOS_COMPLETO.md"]
    MAP["docs/MAPA_DOCUMENTOS_MERMAID.md"]
    V6["docs/v6/MAPEAMENTO_EXISTENTE.md"]
    PLAN["docs/PLANO_IMPLANTACAO_COLMEIA.md"]
    SHARED["compartilhado/COLMEIA.md"]
    PROT["compartilhado/PROTOCOLO_v5.md"]
    COLMAP["colmeia/00_MAPA_GPS.md"]

    START --> IDX
    IDX --> MAP
    MAP --> V6
    MAP --> PLAN
    MAP --> SHARED
    SHARED --> PROT
    MAP --> COLMAP
```

---

## 3) Mapa Focado na Pasta `colmeia/`

```mermaid
flowchart TD
    CROOT["colmeia/"]
    AS["assets/"]
    DO["doutrina/SEGURANCA_COLETIVA.md"]
    VI["visoes/"]
    IN["visoes/INTEIA.md"]
    RA["visoes/RAINHA.md"]
    GPS["colmeia/00_MAPA_GPS.md"]

    CROOT --> AS
    CROOT --> DO
    CROOT --> VI
    VI --> IN
    VI --> RA
    CROOT --> GPS
```

---

## 4) Rotas Rapidas

1. Inventario completo: `docs/INDICE_DOCUMENTOS_COMPLETO.md`
2. Mapa legado v6: `docs/v6/MAPEAMENTO_EXISTENTE.md`
3. Arquitetura ecossistema: `compartilhado/COLMEIA.md`
4. Protocolo unificado: `compartilhado/PROTOCOLO_v5.md`
5. Mapa local da pasta Colmeia: `colmeia/00_MAPA_GPS.md`

