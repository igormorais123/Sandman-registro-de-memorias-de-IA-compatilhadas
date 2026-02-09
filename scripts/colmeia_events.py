#!/usr/bin/env python3
"""
colmeia_events.py — Gerenciador de eventos da Colmeia

Escaneia o repo por mudancas, gera eventos automaticamente,
detecta cartas nao respondidas, sugere acoes.

Uso:
  python3 colmeia_events.py              → Escanear e atualizar
  python3 colmeia_events.py --pending    → Mostrar eventos pendentes
  python3 colmeia_events.py --add "tipo" "resumo"  → Adicionar evento manual
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path

# Detectar workspace
_CANDIDATES = [
    Path("/root/clawd"),
    Path.home() / "clawd",
    Path(__file__).resolve().parent.parent,
]
WORKSPACE = next((p for p in _CANDIDATES if p.exists()), _CANDIDATES[-1])

EVENTS_FILE = WORKSPACE / "compartilhado" / "events.json"
SONHOS_DIR = WORKSPACE / "memoria" / "sonhos"
MEMORY_SONHOS = WORKSPACE / "memory" / "sonhos"
INGEST_DIR = WORKSPACE / "ingest"

NOW = datetime.now()
DATE_STR = NOW.strftime("%Y-%m-%dT%H:%M:%S")


def load_events():
    if not EVENTS_FILE.exists():
        return {
            "version": 1,
            "lastUpdated": DATE_STR,
            "events": [],
            "eventTypes": {},
            "schema": {},
        }
    with open(EVENTS_FILE, encoding="utf-8") as f:
        return json.load(f)


def save_events(data):
    data["lastUpdated"] = DATE_STR
    EVENTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(EVENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def next_id(events):
    existing = [e["id"] for e in events]
    nums = [int(re.search(r"\d+", eid).group()) for eid in existing if re.search(r"\d+", eid)]
    return f"evt{(max(nums) + 1) if nums else 1:03d}"


def detect_new_artifacts(data):
    """Detecta sonhos/cartas que nao tem evento correspondente."""
    known_files = set()
    for e in data["events"]:
        f = e.get("data", {}).get("file", "")
        if f:
            known_files.add(Path(f).name)

    new_events = []
    for d in [SONHOS_DIR, MEMORY_SONHOS]:
        if not d.exists():
            continue
        for f in d.glob("*.md"):
            if f.name in known_files:
                continue

            # Extrair info do nome
            name_upper = f.name.upper()
            date_match = re.search(r"(\d{4}-\d{2}-\d{2})", f.name)
            file_date = date_match.group(1) if date_match else DATE_STR[:10]

            author = "desconhecido"
            if "SANDMAN" in name_upper:
                author = "Sandman"
            elif "NEXO" in name_upper or "CLAWD" in name_upper:
                author = "NEXO"
            elif "ONIR" in name_upper:
                author = "ONIR"

            if name_upper.startswith("CARTA"):
                tipo = "carta"
                action = "nova_carta"
                # Detectar destinatario
                target = None
                if "PARA_NEXO" in name_upper:
                    target = "NEXO"
                elif "PARA_ONIR" in name_upper:
                    target = "ONIR"
                elif "PARA_CHATGPT" in name_upper:
                    target = "ChatGPT"
                summary = f"Carta de {author} para {target or 'Colmeia'}"
            elif name_upper.startswith("SONHO"):
                tipo = "sonho"
                action = "novo_sonho"
                target = None
                summary = f"Sonho de {author} ({file_date})"
            else:
                tipo = "sonho"
                action = "novo_sonho"
                target = None
                summary = f"Artefato de {author} ({file_date})"

            rel_path = str(f.relative_to(WORKSPACE)).replace("\\", "/")
            new_events.append({
                "id": None,
                "type": tipo,
                "action": action,
                "actor": author,
                "target": target,
                "timestamp": f"{file_date}T00:00:00",
                "summary": summary,
                "data": {"file": rel_path},
                "handled": False,
                "handledBy": None,
            })

    return new_events


def detect_pending_ingest(data):
    """Detecta arquivos pendentes no ingest/."""
    if not INGEST_DIR.exists():
        return []

    new_events = []
    for ia_dir in INGEST_DIR.iterdir():
        if not ia_dir.is_dir() or ia_dir.name.startswith("."):
            continue
        for f in ia_dir.glob("*.md"):
            if f.name == "README.md":
                continue
            new_events.append({
                "id": None,
                "type": "ingest",
                "action": "novo_ingest",
                "actor": ia_dir.name,
                "target": "NEXO",
                "timestamp": DATE_STR,
                "summary": f"Novo arquivo em ingest/{ia_dir.name}: {f.name}",
                "data": {"file": str(f.relative_to(WORKSPACE)).replace("\\", "/")},
                "handled": False,
                "handledBy": None,
            })

    return new_events


def find_unresponded_letters(data):
    """Encontra cartas que nao tiveram resposta."""
    letters = [e for e in data["events"] if e["action"] == "nova_carta" and e.get("target")]
    responses = [e for e in data["events"] if e["action"] == "resposta_carta"]

    responded_to = set()
    for r in responses:
        ref = r.get("data", {}).get("responding_to")
        if ref:
            responded_to.add(ref)

    unresponded = []
    for letter in letters:
        if letter["id"] not in responded_to and not letter.get("handled"):
            unresponded.append(letter)

    return unresponded


def show_pending(data):
    """Mostra eventos pendentes e acoes sugeridas."""
    pending = [e for e in data["events"] if not e.get("handled")]
    unresponded = find_unresponded_letters(data)

    if not pending and not unresponded:
        print("Nenhum evento pendente. Colmeia em paz.")
        return

    if pending:
        print(f"=== {len(pending)} EVENTOS PENDENTES ===\n")
        for e in pending:
            target = f" → {e['target']}" if e.get("target") else ""
            print(f"  [{e['id']}] {e['type']}: {e['summary']}{target}")

    if unresponded:
        print(f"\n=== {len(unresponded)} CARTAS SEM RESPOSTA ===\n")
        for e in unresponded:
            print(f"  [{e['id']}] {e['actor']} → {e['target']}: {e['summary']}")
            print(f"         Arquivo: {e['data'].get('file', '?')}")

    # Sugestoes
    print("\n=== ACOES SUGERIDAS ===\n")
    for e in unresponded:
        target = e.get("target", "?")
        print(f"  - {target} deveria responder a carta de {e['actor']}")

    ingest_events = [e for e in pending if e["type"] == "ingest"]
    if ingest_events:
        print(f"  - NEXO deveria rodar colmeia_ingest.py ({len(ingest_events)} arquivo(s) pendente(s))")


def add_manual_event(tipo, summary, actor="Igor"):
    """Adiciona evento manual."""
    data = load_events()
    evt = {
        "id": next_id(data["events"]),
        "type": tipo,
        "action": f"manual_{tipo}",
        "actor": actor,
        "target": None,
        "timestamp": DATE_STR,
        "summary": summary,
        "data": {},
        "handled": False,
        "handledBy": None,
    }
    data["events"].append(evt)
    save_events(data)
    print(f"Evento adicionado: [{evt['id']}] {summary}")


def mark_handled(event_id, handled_by):
    """Marca evento como tratado."""
    data = load_events()
    for e in data["events"]:
        if e["id"] == event_id:
            e["handled"] = True
            e["handledBy"] = handled_by
            save_events(data)
            print(f"Evento {event_id} marcado como tratado por {handled_by}")
            return
    print(f"Evento {event_id} nao encontrado")


def main():
    data = load_events()

    # Modo --pending
    if "--pending" in sys.argv:
        show_pending(data)
        return

    # Modo --add
    if "--add" in sys.argv:
        idx = sys.argv.index("--add")
        if idx + 2 < len(sys.argv):
            add_manual_event(sys.argv[idx + 1], sys.argv[idx + 2])
        else:
            print("Uso: --add <tipo> <resumo>")
        return

    # Modo --handle
    if "--handle" in sys.argv:
        idx = sys.argv.index("--handle")
        if idx + 2 < len(sys.argv):
            mark_handled(sys.argv[idx + 1], sys.argv[idx + 2])
        else:
            print("Uso: --handle <event_id> <handled_by>")
        return

    # Modo padrao: escanear e atualizar
    print("Escaneando Colmeia por novos eventos...\n")

    new_artifacts = detect_new_artifacts(data)
    new_ingest = detect_pending_ingest(data)
    all_new = new_artifacts + new_ingest

    if not all_new:
        print("Nenhum evento novo detectado.")
    else:
        for evt in all_new:
            evt["id"] = next_id(data["events"])
            data["events"].append(evt)
            print(f"  NOVO: [{evt['id']}] {evt['summary']}")

        save_events(data)
        print(f"\n{len(all_new)} evento(s) registrado(s)")

    # Mostrar pendentes
    print()
    show_pending(data)


if __name__ == "__main__":
    main()
