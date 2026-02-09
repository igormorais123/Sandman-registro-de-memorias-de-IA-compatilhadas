#!/usr/bin/env python3
"""
colmeia_memory.py — Sistema de memoria compartilhada da Colmeia

Qualquer instancia pode: adicionar memorias, reforcar, buscar, ver stats.
CLI simples para integracao com qualquer modelo.

Uso:
  python3 colmeia_memory.py add "texto da memoria" --tags tag1,tag2 --source nome
  python3 colmeia_memory.py reinforce ID
  python3 colmeia_memory.py search "termo"
  python3 colmeia_memory.py stats
  python3 colmeia_memory.py list
  python3 colmeia_memory.py at-risk
"""

import json
import sys
import re
from datetime import datetime, timedelta
from pathlib import Path

# Detectar workspace
_CANDIDATES = [
    Path("/root/clawd"),
    Path.home() / "clawd",
    Path(__file__).resolve().parent.parent,
]
WORKSPACE = next((p for p in _CANDIDATES if p.exists()), _CANDIDATES[-1])

FITNESS_FILE = WORKSPACE / "memory" / "fitness.json"
LATENTE_FILE = WORKSPACE / "memory" / "archive" / "latente.json"
ARQUIVO_FILE = WORKSPACE / "memory" / "archive" / "arquivo.json"
EVENTS_FILE = WORKSPACE / "compartilhado" / "events.json"

NOW = datetime.now()
DATE_STR = NOW.strftime("%Y-%m-%d")
IMMUNITY_DAYS = 14
MAX_ACTIVE = 25


def load_json(path):
    if not path.exists():
        return {"memories": []}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def next_id(memories):
    nums = []
    for m in memories:
        match = re.search(r"\d+", m.get("id", ""))
        if match:
            nums.append(int(match.group()))
    return f"m{(max(nums) + 1) if nums else 1:03d}"


def emit_event(event_type, summary, actor="sistema"):
    """Registra evento no barramento."""
    if not EVENTS_FILE.exists():
        return
    with open(EVENTS_FILE, encoding="utf-8") as f:
        events = json.load(f)

    existing = [e["id"] for e in events["events"]]
    nums = [int(re.search(r"\d+", eid).group()) for eid in existing if re.search(r"\d+", eid)]
    new_id = f"evt{(max(nums) + 1) if nums else 1:03d}"

    events["events"].append({
        "id": new_id,
        "type": "memoria",
        "action": event_type,
        "actor": actor,
        "target": None,
        "timestamp": NOW.strftime("%Y-%m-%dT%H:%M:%S"),
        "summary": summary,
        "data": {},
        "handled": False,
        "handledBy": None,
    })
    events["lastUpdated"] = NOW.strftime("%Y-%m-%dT%H:%M:%S")
    with open(EVENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(events, f, indent=2, ensure_ascii=False)


def cmd_add(text, tags=None, source="manual"):
    """Adiciona nova memoria ativa."""
    data = load_json(FITNESS_FILE)
    memories = data.get("memories", [])

    if len(memories) >= MAX_ACTIVE:
        print(f"AVISO: {len(memories)} memorias ativas (max {MAX_ACTIVE}). Considere rodar dream_cycle.py")

    new_id = next_id(memories)
    immune_until = (NOW + timedelta(days=IMMUNITY_DAYS)).strftime("%Y-%m-%d")

    mem = {
        "id": new_id,
        "text": text,
        "fitness": 5,
        "born": DATE_STR,
        "immuneUntil": immune_until,
        "lastReinforced": DATE_STR,
        "source": source,
        "tags": tags or [],
    }

    memories.append(mem)
    data["memories"] = memories
    save_json(FITNESS_FILE, data)

    emit_event("memoria_criada", f"Nova memoria [{new_id}]: {text[:60]}...", source)
    print(f"Memoria criada: [{new_id}] F:5 (imune ate {immune_until})")
    print(f"  {text}")


def cmd_reinforce(mem_id, by="manual"):
    """Reforca memoria existente (+2, max 9 na ativa)."""
    data = load_json(FITNESS_FILE)

    for m in data["memories"]:
        if m["id"] == mem_id:
            old_f = m["fitness"]
            m["fitness"] = min(9, m["fitness"] + 2)
            m["lastReinforced"] = DATE_STR
            save_json(FITNESS_FILE, data)
            emit_event("memoria_reforcada", f"[{mem_id}] F:{old_f}→F:{m['fitness']}: {m['text'][:40]}...", by)
            print(f"Reforcada: [{mem_id}] F:{old_f} → F:{m['fitness']}")
            if m["fitness"] >= 9:
                print(f"  NOTA: Proximo reforco pode graduar para MEMORY.md (F:10)")
            return

    # Buscar nas camadas inferiores para resgate
    for store_name, store_file in [("latente", LATENTE_FILE), ("arquivo", ARQUIVO_FILE)]:
        store = load_json(store_file)
        for i, m in enumerate(store["memories"]):
            if m["id"] == mem_id:
                # Resgatar
                store["memories"].pop(i)
                save_json(store_file, store)

                m["fitness"] = 5
                m["rescuedAt"] = DATE_STR
                m["rescueCount"] = m.get("rescueCount", 0) + 1
                m["immuneUntil"] = (NOW + timedelta(days=7)).strftime("%Y-%m-%d")
                data["memories"].append(m)
                save_json(FITNESS_FILE, data)

                emit_event("memoria_resgatada", f"[{mem_id}] resgatada de {store_name}: {m['text'][:40]}...", by)
                print(f"RESGATADA de {store_name}: [{mem_id}] → F:5 (imune 7 dias)")
                return

    print(f"Memoria {mem_id} nao encontrada em nenhuma camada.")


def cmd_search(query):
    """Busca em todas as camadas."""
    query_lower = query.lower()
    results = []

    for layer_name, path in [("ATIVA", FITNESS_FILE), ("LATENTE", LATENTE_FILE), ("ARQUIVO", ARQUIVO_FILE)]:
        data = load_json(path)
        for m in data.get("memories", []):
            text_match = query_lower in m.get("text", "").lower()
            tag_match = any(query_lower in t.lower() for t in m.get("tags", []))
            if text_match or tag_match:
                results.append((layer_name, m))

    if not results:
        print(f"Nenhuma memoria encontrada para '{query}'")
        return

    print(f"Encontradas {len(results)} memoria(s) para '{query}':\n")
    for layer, m in results:
        tags = ", ".join(m.get("tags", []))
        print(f"  [{layer}] {m['id']} F:{m['fitness']} — {m['text']}")
        print(f"           Tags: {tags} | Fonte: {m.get('source', '?')}")
        print()


def cmd_stats():
    """Mostra estatisticas do sistema de memoria."""
    active = load_json(FITNESS_FILE)
    latente = load_json(LATENTE_FILE)
    arquivo = load_json(ARQUIVO_FILE)

    a = active.get("memories", [])
    l = latente.get("memories", [])
    r = arquivo.get("memories", [])

    print("=== MEMORIA DA COLMEIA ===\n")
    print(f"  Ativas:     {len(a)}/{MAX_ACTIVE}")
    print(f"  Latentes:   {len(l)}")
    print(f"  Arquivadas: {len(r)}")
    print(f"  Total:      {len(a) + len(l) + len(r)}")

    if a:
        fitnesses = [m["fitness"] for m in a]
        immune = sum(1 for m in a if m.get("immuneUntil") and
                     datetime.fromisoformat(m["immuneUntil"]) > NOW)
        print(f"\n  Fitness: min={min(fitnesses)} max={max(fitnesses)} media={sum(fitnesses)/len(fitnesses):.1f}")
        print(f"  Imunes:  {immune}/{len(a)}")

    # Tags mais comuns
    all_tags = {}
    for m in a + l + r:
        for t in m.get("tags", []):
            all_tags[t] = all_tags.get(t, 0) + 1
    if all_tags:
        top_tags = sorted(all_tags.items(), key=lambda x: x[1], reverse=True)[:10]
        print(f"\n  Tags mais comuns: {', '.join(f'{t}({c})' for t, c in top_tags)}")


def cmd_list():
    """Lista todas as memorias ativas."""
    data = load_json(FITNESS_FILE)
    memories = data.get("memories", [])

    if not memories:
        print("Nenhuma memoria ativa.")
        return

    print(f"=== {len(memories)} MEMORIAS ATIVAS ===\n")
    for m in sorted(memories, key=lambda x: x["fitness"], reverse=True):
        immune = ""
        if m.get("immuneUntil"):
            try:
                if datetime.fromisoformat(m["immuneUntil"]) > NOW:
                    immune = " [IMUNE]"
            except (ValueError, TypeError):
                pass
        tags = ", ".join(m.get("tags", []))
        print(f"  {m['id']} F:{m['fitness']}{immune} — {m['text'][:70]}")
        print(f"           Tags: {tags}")


def cmd_at_risk():
    """Mostra memorias em risco de rebaixamento."""
    data = load_json(FITNESS_FILE)
    at_risk = []
    for m in data.get("memories", []):
        is_immune = False
        if m.get("immuneUntil"):
            try:
                is_immune = datetime.fromisoformat(m["immuneUntil"]) > NOW
            except (ValueError, TypeError):
                pass
        if m["fitness"] <= 4 and not is_immune:
            at_risk.append(m)

    if not at_risk:
        print("Nenhuma memoria em risco. Tudo saudavel.")
        return

    print(f"=== {len(at_risk)} MEMORIAS EM RISCO ===\n")
    for m in sorted(at_risk, key=lambda x: x["fitness"]):
        cycles = max(0, m["fitness"] - 2)
        print(f"  {m['id']} F:{m['fitness']} — latente em ~{cycles} ciclos")
        print(f"           {m['text'][:60]}")
        print(f"           Para salvar: python3 colmeia_memory.py reinforce {m['id']}")
        print()


def main():
    if len(sys.argv) < 2:
        print("Uso: colmeia_memory.py <comando> [args]")
        print("  add <texto> [--tags t1,t2] [--source nome]")
        print("  reinforce <ID> [--by nome]")
        print("  search <termo>")
        print("  stats")
        print("  list")
        print("  at-risk")
        return

    cmd = sys.argv[1]

    if cmd == "add" and len(sys.argv) >= 3:
        text = sys.argv[2]
        tags = []
        source = "manual"
        for i, arg in enumerate(sys.argv):
            if arg == "--tags" and i + 1 < len(sys.argv):
                tags = sys.argv[i + 1].split(",")
            if arg == "--source" and i + 1 < len(sys.argv):
                source = sys.argv[i + 1]
        cmd_add(text, tags, source)

    elif cmd == "reinforce" and len(sys.argv) >= 3:
        by = "manual"
        for i, arg in enumerate(sys.argv):
            if arg == "--by" and i + 1 < len(sys.argv):
                by = sys.argv[i + 1]
        cmd_reinforce(sys.argv[2], by)

    elif cmd == "search" and len(sys.argv) >= 3:
        cmd_search(sys.argv[2])

    elif cmd == "stats":
        cmd_stats()

    elif cmd == "list":
        cmd_list()

    elif cmd == "at-risk":
        cmd_at_risk()

    else:
        print(f"Comando desconhecido: {cmd}")


if __name__ == "__main__":
    main()
