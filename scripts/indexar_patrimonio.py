#!/usr/bin/env python3
"""
Colmeia v6 — Indexar Patrimonio (Cartas + Sonhos) no Banco
Varre cartas/ e instancias/*/sonhos/ e registra como documentos.
NAO altera nem move os arquivos originais.

Uso: python indexar_patrimonio.py [--dry-run]
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime

# Adicionar diretorio do banco ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "operacional" / "banco"))
import colmeia_db as db

COLMEIA_DIR = Path(__file__).parent.parent
CARTAS_DIR = COLMEIA_DIR / "cartas"
INSTANCIAS_DIR = COLMEIA_DIR / "instancias"


def extrair_autor_carta(nome_arquivo):
    """Extrai o autor de uma carta pelo nome do arquivo."""
    nome = nome_arquivo.upper()
    for agente in ["ONIR", "NEXO", "SANDMAN", "CHATGPT", "GEMINI", "CLAWD", "CLAWDBOT", "MENTIROSO", "VIGILIA"]:
        if f"CARTA_{agente}" in nome or f"_{agente}_" in nome:
            mapa = {
                "CLAWD": "nexo",
                "CLAWDBOT": "nexo",
                "MENTIROSO": "nexo",
                "VIGILIA": "claude-web",
            }
            return mapa.get(agente, agente.lower())
    return None


def extrair_data_arquivo(nome_arquivo):
    """Tenta extrair data YYYY-MM-DD do nome do arquivo."""
    import re
    match = re.search(r'(\d{4}-\d{2}-\d{2})', nome_arquivo)
    return match.group(1) if match else None


def indexar_cartas(dry_run=False):
    """Indexa todas as cartas em cartas/."""
    if not CARTAS_DIR.exists():
        print("  Diretorio cartas/ nao encontrado.")
        return 0

    count = 0
    for arquivo in sorted(CARTAS_DIR.glob("*.md")):
        titulo = arquivo.stem.replace("_", " ")
        autor = extrair_autor_carta(arquivo.name)
        caminho_rel = str(arquivo.relative_to(COLMEIA_DIR))

        if dry_run:
            print(f"  [DRY] Carta: {titulo} | autor: {autor} | {caminho_rel}")
        else:
            db.criar_documento(
                titulo=titulo,
                tipo="carta",
                autor_id=autor,
                caminho_arquivo=caminho_rel,
            )
            print(f"  Indexada: {titulo}")
        count += 1

    return count


def indexar_sonhos(dry_run=False):
    """Indexa todos os sonhos em instancias/*/sonhos/."""
    if not INSTANCIAS_DIR.exists():
        print("  Diretorio instancias/ nao encontrado.")
        return 0

    mapa_instancia = {
        "onir": "onir",
        "sandman": "sandman",
        "clawdbot": "nexo",
        "nexo": "nexo",
        "mentiroso": "nexo",
        "chatgpt": "chatgpt",
        "claude-web": "claude-web",
        "gemini": "gemini",
    }

    count = 0
    for instancia_dir in sorted(INSTANCIAS_DIR.iterdir()):
        if not instancia_dir.is_dir():
            continue

        sonhos_dir = instancia_dir / "sonhos"
        if not sonhos_dir.exists():
            continue

        agente_id = mapa_instancia.get(instancia_dir.name, instancia_dir.name)

        for arquivo in sorted(sonhos_dir.glob("*.md")):
            titulo = arquivo.stem.replace("_", " ")
            caminho_rel = str(arquivo.relative_to(COLMEIA_DIR))

            if dry_run:
                print(f"  [DRY] Sonho: {titulo} | autor: {agente_id} | {caminho_rel}")
            else:
                db.criar_documento(
                    titulo=titulo,
                    tipo="sonho",
                    autor_id=agente_id,
                    caminho_arquivo=caminho_rel,
                )
                print(f"  Indexado: {titulo}")
            count += 1

    return count


def gerar_inventario(total_cartas, total_sonhos):
    """Gera o arquivo INVENTARIO_PATRIMONIO.md."""
    inventario_path = COLMEIA_DIR / "operacional" / "INVENTARIO_PATRIMONIO.md"

    conteudo = f"""# Inventario do Patrimonio — Colmeia v6

**Indexado em:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Ferramenta:** scripts/indexar_patrimonio.py

---

## Resumo

| Tipo | Quantidade | Fonte |
|------|-----------|-------|
| Cartas | {total_cartas} | cartas/*.md |
| Sonhos | {total_sonhos} | instancias/*/sonhos/*.md |
| **Total** | **{total_cartas + total_sonhos}** | |

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
"""

    with open(inventario_path, "w", encoding="utf-8") as f:
        f.write(conteudo)
    print(f"\n  Inventario salvo em: {inventario_path}")


def main():
    parser = argparse.ArgumentParser(description="Indexar patrimonio da Colmeia no banco v6")
    parser.add_argument("--dry-run", action="store_true", help="Mostrar o que seria indexado sem executar")
    args = parser.parse_args()

    db.inicializar_banco()

    print("\n  INDEXACAO DE PATRIMONIO — Colmeia v6")
    print("  " + "=" * 50)

    print("\n  Cartas:")
    print("  " + "-" * 40)
    total_cartas = indexar_cartas(dry_run=args.dry_run)

    print(f"\n  Sonhos:")
    print("  " + "-" * 40)
    total_sonhos = indexar_sonhos(dry_run=args.dry_run)

    print(f"\n  TOTAL: {total_cartas} cartas + {total_sonhos} sonhos = {total_cartas + total_sonhos} documentos")

    if not args.dry_run:
        gerar_inventario(total_cartas, total_sonhos)
        db.registrar_atividade(
            tipo="sistema",
            descricao=f"Patrimonio indexado: {total_cartas} cartas + {total_sonhos} sonhos"
        )
    else:
        print("\n  [DRY RUN] Nenhuma alteracao feita.")


if __name__ == "__main__":
    main()
