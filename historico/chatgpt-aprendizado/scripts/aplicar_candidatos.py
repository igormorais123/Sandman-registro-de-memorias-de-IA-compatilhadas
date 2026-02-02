#!/usr/bin/env python3
"""Aplica candidatos revisados (YAML simples) aos arquivos globais.

Regras (simples e seguras):
- Você revisa manualmente `categoria` e `projeto`.
- O script só anexa em seções específicas, mantendo rastreabilidade.

Categorias aceitas: principio, padrao, antipadrao, prompt, ferramenta, meta
"""

import argparse
import json
import re
from pathlib import Path

VALID = {"principio", "padrao", "antipadrao", "prompt", "ferramenta", "meta"}


def parse_min_yaml(path: Path):
    # parser mínimo para o YAML gerado pelo ingest (lista de dicts sem aninhamento complexo)
    items = []
    cur = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip("\n")
        if not line or line.lstrip().startswith("#"):
            continue
        if line.startswith("- id:"):
            if cur:
                items.append(cur)
            cur = {"origem": {}}
            cur["id"] = line.split(":", 1)[1].strip()
            continue
        if cur is None:
            continue
        if re.match(r"\s{2}origem:\s*$", line):
            continue
        m = re.match(r"\s{2}([a-zA-Z_]+):\s*(.*)$", line)
        if m:
            k, v = m.group(1), m.group(2)
            cur[k] = json.loads(v) if v.startswith('"') or v in ("null", "true", "false") else v
            continue
        m2 = re.match(r"\s{4}([a-zA-Z_]+):\s*(.*)$", line)
        if m2:
            k, v = m2.group(1), m2.group(2)
            cur["origem"][k] = json.loads(v) if v.startswith('"') or v in ("null", "true", "false") else v
            continue
    if cur:
        items.append(cur)
    return items


def append_block(md_path: Path, heading: str, block: str):
    txt = md_path.read_text(encoding="utf-8")
    if heading not in txt:
        # se heading não existir, anexa no fim
        md_path.write_text(txt + "\n\n" + heading + "\n\n" + block, encoding="utf-8")
        return
    parts = txt.split(heading)
    before = parts[0]
    after = heading.join(parts[1:])
    # insere logo após heading
    new = before + heading + "\n\n" + block + "\n" + after.lstrip("\n")
    md_path.write_text(new, encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("candidatos_yaml", type=str)
    ap.add_argument("--root", type=str, default=".")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    items = parse_min_yaml(Path(args.candidatos_yaml))

    applied = 0

    for it in items:
        cat = (it.get("categoria") or "").strip().lower()
        if cat not in VALID:
            continue
        texto = (it.get("texto") or "").strip()
        if not texto:
            continue
        origem = it.get("origem") or {}
        evid = f"Evidência: sessão {origem.get('sessao','')}, conversation_id {origem.get('conversation_id','')}, {origem.get('timestamp','')}"

        if cat == "prompt":
            target = root / "PROMPTS_EFETIVOS.md"
            block = f"### {it.get('id')}\n\n``\n{texto}\n``\n\n- {evid}\n"
            append_block(target, "## Debugging", block)
        elif cat == "ferramenta":
            target = root / "FERRAMENTAS_RECOMENDADAS.md"
            block = f"### {it.get('id')}\n- Descrição: {texto}\n- {evid}\n"
            append_block(target, "# Ferramentas Recomendadas", block)
        elif cat == "antipadrao":
            target = root / "ANTIPADROES_GLOBAIS.md"
            block = f"### {it.get('id')}\n- {texto}\n- {evid}\n"
            append_block(target, "# Antipadrões Globais", block)
        elif cat == "padrao":
            target = root / "PADROES_CODIGO.md"
            block = f"### {it.get('id')}\n- {texto}\n- {evid}\n"
            append_block(target, "## JavaScript/TypeScript", block)
        elif cat == "principio":
            target = root / "CONHECIMENTO_UNIVERSAL.md"
            block = f"### {it.get('id')}\n- {texto}\n- {evid}\n"
            append_block(target, "## Princípios", block)
        elif cat == "meta":
            target = root / "META_APRENDIZADO.md"
            block = f"### {it.get('id')}\n- {texto}\n- {evid}\n"
            append_block(target, "## Melhorias do sistema", block)
        else:
            continue

        applied += 1

    print(f"OK: {applied} itens aplicados")


if __name__ == "__main__":
    main()
