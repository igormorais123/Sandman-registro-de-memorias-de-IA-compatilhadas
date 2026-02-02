# Memória Hierárquica (Global + por Projeto)

Este repositório é uma base de conhecimento **portável entre plataformas** (ChatGPT, Claude, Antigravity, etc.).

## Estrutura

- `INDICE_GLOBAL.md` – painel e navegação
- `CONHECIMENTO_UNIVERSAL.md` – aprendizados cross-projeto
- `CATALOGO_PROJETOS.md` – mapa dos projetos
- `PADROES_CODIGO.md` – padrões reutilizáveis
- `ANTIPADROES_GLOBAIS.md` – o que evitar
- `PROMPTS_EFETIVOS.md` – biblioteca de prompts
- `FERRAMENTAS_RECOMENDADAS.md` – ferramentas, SDKs, extensões
- `META_APRENDIZADO.md` – métricas e melhorias do sistema

Pastas:
- `projetos/` – fichas por projeto
- `sessoes/` – sessões/importações (ex.: por conversa exportada)
- `raw/` – **NÃO versionar** exports brutos (use `.gitignore`)
- `scripts/` – ingestão/normalização

## Fluxo recomendado

1. Exporte o histórico do ChatGPT e obtenha `conversations.json`.
2. Coloque em `raw/conversations.json` (não commite).
3. Rode:

```bash
python3 scripts/ingest_chatgpt_export.py raw/conversations.json
```

4. Revise `temp/candidatos_memoria.yaml`.
5. Rode:

```bash
python3 scripts/aplicar_candidatos.py temp/candidatos_memoria.yaml
```

## Privacidade

- Mantenha este repositório **privado**.
- Não commite `raw/`.
