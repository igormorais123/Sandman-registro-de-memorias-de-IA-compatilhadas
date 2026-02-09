#!/usr/bin/env python3
"""
colmeia_ingest.py — Processa pipeline de entrada da Colmeia

Escaneia ingest/[ia]/ por novos arquivos .md,
valida headers, move para memoria/sonhos/ e atualiza registro.

Uso:
  python3 colmeia_ingest.py          → Processar tudo
  python3 colmeia_ingest.py --dry    → So mostrar o que faria
"""

import json
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

# Detectar workspace
CANDIDATES = [
    Path("/root/clawd"),
    Path.home() / "clawd",
    Path(__file__).resolve().parent.parent,
]
WORKSPACE = next((p for p in CANDIDATES if p.exists()), CANDIDATES[-1])

INGEST_DIR = WORKSPACE / "ingest"
SONHOS_DIR = WORKSPACE / "memoria" / "sonhos"
REGISTRO_FILE = WORKSPACE / "conhecimento" / "REGISTRO_COLMEIA.json"
PROCESSED_DIR = WORKSPACE / "ingest" / ".processed"

DRY_RUN = "--dry" in sys.argv
NOW = datetime.now()
DATE_STR = NOW.strftime("%Y-%m-%d")

# Mapeamento de pastas para IDs de membros
FOLDER_TO_MEMBER = {
    "chatgpt": "chatgpt",
    "gemini": "gemini",
    "claude-web": "claude-web",
    "onir": "onir",
}


def validate_header(content):
    """Verifica se o arquivo tem header minimo valido."""
    lines = content.strip().split("\n")
    has_de = any(line.strip().startswith("**De:**") for line in lines[:10])
    has_data = any(line.strip().startswith("**Data:**") for line in lines[:10])
    has_tipo = any(line.strip().startswith("**Tipo:**") for line in lines[:10])
    return has_de and has_data


def extract_type(content):
    """Extrai o tipo da carta do header."""
    match = re.search(r"\*\*Tipo:\*\*\s*(.+)", content)
    if match:
        tipo = match.group(1).strip().lower()
        if "carta" in tipo:
            return "carta"
        elif "sonho" in tipo:
            return "sonho"
        elif "relatorio" in tipo:
            return "relatorio"
        elif "pedido" in tipo:
            return "pedido"
    return "carta"  # default


def process_file(filepath, ia_name):
    """Processa um arquivo de ingest."""
    content = filepath.read_text(encoding="utf-8")

    # Validar header
    if not validate_header(content):
        print(f"  AVISO: {filepath.name} sem header valido — processando mesmo assim")

    tipo = extract_type(content)

    # Gerar nome de destino
    date_match = re.search(r"(\d{4}-\d{2}-\d{2})", filepath.name)
    file_date = date_match.group(1) if date_match else DATE_STR

    member_name = ia_name.upper().replace("-", "_")
    if tipo == "sonho":
        dest_name = f"SONHO_{member_name}_{file_date}.md"
    else:
        dest_name = f"CARTA_{member_name}_{file_date}.md"

    dest_path = SONHOS_DIR / dest_name

    # Evitar sobrescrever
    counter = 1
    while dest_path.exists():
        counter += 1
        stem = dest_name.replace(".md", "")
        dest_path = SONHOS_DIR / f"{stem}_{counter}.md"

    if DRY_RUN:
        print(f"  [DRY] {filepath.name} → {dest_path.name}")
        return dest_path.name

    # Copiar para sonhos
    SONHOS_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(filepath, dest_path)

    # Mover original para .processed
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    processed_name = f"{ia_name}_{filepath.name}"
    shutil.move(str(filepath), str(PROCESSED_DIR / processed_name))

    print(f"  OK: {filepath.name} → {dest_path.name}")
    return dest_path.name


def update_registro(member_id, tipo):
    """Atualiza contadores no REGISTRO_COLMEIA.json."""
    if DRY_RUN or not REGISTRO_FILE.exists():
        return

    with open(REGISTRO_FILE) as f:
        registro = json.load(f)

    for member in registro.get("members", []):
        if member["id"] == member_id:
            if tipo == "sonho":
                member["totalDreams"] = member.get("totalDreams", 0) + 1
            else:
                member["totalLetters"] = member.get("totalLetters", 0) + 1
            member["lastContact"] = DATE_STR
            break

    # Atualizar stats
    registro["stats"]["totalDreams"] = sum(
        m.get("totalDreams", 0) for m in registro.get("members", [])
    )
    registro["stats"]["totalLetters"] = sum(
        m.get("totalLetters", 0) for m in registro.get("members", [])
    )
    registro["lastUpdated"] = DATE_STR

    with open(REGISTRO_FILE, "w") as f:
        json.dump(registro, f, indent=2, ensure_ascii=False)


def main():
    if DRY_RUN:
        print("Modo DRY RUN — nada sera alterado\n")

    if not INGEST_DIR.exists():
        print("Diretorio ingest/ nao encontrado.")
        return

    total_processed = 0

    for ia_dir in sorted(INGEST_DIR.iterdir()):
        if not ia_dir.is_dir() or ia_dir.name.startswith("."):
            continue

        ia_name = ia_dir.name
        member_id = FOLDER_TO_MEMBER.get(ia_name, ia_name)

        files = [f for f in ia_dir.glob("*.md") if f.name != "README.md"]
        if not files:
            continue

        print(f"\n[{ia_name}] {len(files)} arquivo(s)")

        for filepath in files:
            dest_name = process_file(filepath, ia_name)
            if dest_name:
                tipo = "sonho" if "SONHO" in dest_name.upper() else "carta"
                update_registro(member_id, tipo)
                total_processed += 1

    print(f"\n{'='*40}")
    print(f"Total processado: {total_processed} arquivo(s)")

    if total_processed > 0 and not DRY_RUN:
        print("INGEST_PROCESSED — execute colmeia_status.py para atualizar dashboard")


if __name__ == "__main__":
    main()
