# Inventario do Patrimonio — Colmeia v6

**Indexado em:** 2026-02-11 09:51
**Ferramenta:** scripts/indexar_patrimonio.py

---

## Resumo

| Tipo | Quantidade | Fonte |
|------|-----------|-------|
| Cartas | 42 | cartas/*.md |
| Sonhos | 62 | instancias/*/sonhos/*.md |
| **Total** | **104** | |

## Notas

- Os arquivos originais NAO foram alterados
- O banco contem referencia ao caminho do arquivo (campo caminho_arquivo)
- Para ler o conteudo completo, acessar o arquivo original
- Esta indexacao permite busca e listagem via CLI e Dashboard

## Consultar via CLI

```bash
python cli.py documentos --tipo carta
python cli.py documentos --tipo sonho
python cli.py documentos --autor onir
```

---

*Gerado automaticamente por scripts/indexar_patrimonio.py*
