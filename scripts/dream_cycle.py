#!/usr/bin/env python3
"""
dream_cycle.py — Ciclo de Sonho v4 (Modelo Cognitivo em Camadas)

Memórias NUNCA são deletadas. Descem de camada:
  ATIVA (fitness.json) → LATENTE (latente.json) → ARQUIVO (arquivo.json)

Imunidade de 14 dias para memórias novas.

Uso: python3 dream_cycle.py [--dry-run] [--rescue tag1,tag2]
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path("/root/clawd")
FITNESS_FILE = WORKSPACE / "memory" / "fitness.json"
LATENTE_FILE = WORKSPACE / "memory" / "archive" / "latente.json"
ARQUIVO_FILE = WORKSPACE / "memory" / "archive" / "arquivo.json"
MEMORY_FILE = WORKSPACE / "MEMORY.md"
SONHOS_DIR = WORKSPACE / "memory" / "sonhos"
SANDMAN_SONHOS = WORKSPACE / "sandman" / "instancias" / "clawdbot" / "sonhos"

DRY_RUN = "--dry-run" in sys.argv
NOW = datetime.now()
DATE_STR = NOW.strftime("%Y-%m-%d")
IMMUNITY_DAYS = 14
DEMOTE_THRESHOLD = 2  # F:2 ou menos → latente
ARCHIVE_THRESHOLD = 0  # F:0 ou menos na latente → arquivo


def load_json(path):
    if not path.exists():
        return {"memories": []}
    with open(path) as f:
        return json.load(f)


def save_json(path, data):
    if DRY_RUN:
        print(f"  [DRY RUN] Would save {path.name}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def is_immune(mem):
    """Check if memory is still in immunity period"""
    immune_until = mem.get("immuneUntil")
    if not immune_until:
        return False
    try:
        return datetime.fromisoformat(immune_until) > NOW
    except (ValueError, TypeError):
        return False


def days_alive(mem):
    """Days since birth"""
    try:
        born = datetime.fromisoformat(mem["born"])
        return (NOW - born).days
    except (ValueError, TypeError, KeyError):
        return 999


def decay(memories):
    """Step 3: Decay non-immune memories by -1"""
    decayed = 0
    immune = 0
    for m in memories:
        if is_immune(m):
            immune += 1
        else:
            m["fitness"] = m["fitness"] - 1
            decayed += 1
    return memories, decayed, immune


def demote_to_latent(active_memories, latente_data):
    """Step 4: Move F:<=2 from active to latent (NOT delete)"""
    staying = []
    demoted = []
    for m in active_memories:
        if m["fitness"] <= DEMOTE_THRESHOLD and not is_immune(m):
            m["demotedAt"] = DATE_STR
            m["originalFitness"] = m.get("originalFitness", 5)
            demoted.append(m)
            latente_data["memories"].append(m)
        else:
            staying.append(m)
    return staying, demoted, latente_data


def archive_from_latent(latente_data, arquivo_data):
    """Move F:<=0 from latent to archive (NOT delete)"""
    staying = []
    archived = []
    for m in latente_data["memories"]:
        # Latent memories also decay: -1 per cycle but slower (every other cycle)
        if m["fitness"] <= ARCHIVE_THRESHOLD:
            m["archivedAt"] = DATE_STR
            archived.append(m)
            arquivo_data["memories"].append(m)
        else:
            # Decay latent memories slower: -1 every other cycle
            # Use a simple toggle based on cycle count
            if m.get("_skipDecay"):
                m["_skipDecay"] = False
            else:
                m["fitness"] = m["fitness"] - 1
                m["_skipDecay"] = True
            staying.append(m)
    latente_data["memories"] = staying
    return latente_data, archived, arquivo_data


def graduate(memories):
    """Step 5: Graduate F:>=10 to MEMORY.md"""
    graduated = [m for m in memories if m["fitness"] >= 10]
    remaining = [m for m in memories if m["fitness"] < 10]
    return remaining, graduated


def append_to_memory(graduated):
    """Add graduated memories to MEMORY.md"""
    if not graduated or DRY_RUN:
        return
    section = f"\n\n### Graduações — {DATE_STR}\n\n"
    for m in graduated:
        section += f"**[GRADUADA F:10] {m['text']}**\n"
        section += f"*Nascida: {m['born']} | Fonte: {m.get('source', '?')} | "
        section += f"Tags: {', '.join(m.get('tags', []))}*\n\n"
    with open(MEMORY_FILE, "a") as f:
        f.write(section)


def rescue_by_tags(tags, latente_data, arquivo_data, active_data):
    """Rescue memories from latent/archive by tags"""
    rescued = []
    for store_name, store in [("latente", latente_data), ("arquivo", arquivo_data)]:
        remaining = []
        for m in store["memories"]:
            mem_tags = set(m.get("tags", []))
            if mem_tags & set(tags):
                m["fitness"] = 5
                m["rescuedAt"] = DATE_STR
                m["rescueCount"] = m.get("rescueCount", 0) + 1
                m["immuneUntil"] = (NOW + timedelta(days=7)).strftime("%Y-%m-%d")
                rescued.append((store_name, m))
                active_data["memories"].append(m)
            else:
                remaining.append(m)
        store["memories"] = remaining
    return rescued, active_data, latente_data, arquivo_data


def register_dream(active, demoted, archived, graduated, decayed, immune):
    """Register dream in sonhos files"""
    SONHOS_DIR.mkdir(parents=True, exist_ok=True)
    SANDMAN_SONHOS.mkdir(parents=True, exist_ok=True)

    alive = active["memories"]

    # Stats
    fitness_values = [m["fitness"] for m in alive] if alive else [0]
    immune_count = sum(1 for m in alive if is_immune(m))

    content = f"""# Sonho Clawd — {DATE_STR}

## Tipo: Ciclo automático (Protocolo v4 — Memória em Camadas)

## Resumo do Ciclo

| Métrica | Valor |
|---------|-------|
| Memórias ativas | {len(alive)} |
| Imunes (< 14 dias) | {immune_count} |
| Decaíram neste ciclo | {decayed} |
| Rebaixadas → Latente | {len(demoted)} |
| Afundadas → Arquivo | {len(archived)} |
| Graduadas → Sabedoria | {len(graduated)} |
| Fitness mín/máx | {min(fitness_values)}/{max(fitness_values)} |

"""
    if demoted:
        content += "### Rebaixadas para Latente (acessíveis com esforço)\n"
        for m in demoted:
            content += f"- {m['text'][:80]}... (F:{m['fitness']}, tags: {', '.join(m.get('tags', []))})\n"
        content += "\n"

    if archived:
        content += "### Afundadas para Arquivo (acessíveis por busca)\n"
        for m in archived:
            content += f"- {m['text'][:80]}... (tags: {', '.join(m.get('tags', []))})\n"
        content += "\n"

    if graduated:
        content += "### Graduadas → MEMORY.md (sabedoria permanente)\n"
        for m in graduated:
            content += f"- **{m['text']}** (F:10, nascida {m['born']})\n"
        content += "\n"

    # Previsões
    content += "### Previsões\n"
    at_risk = [m for m in alive if m["fitness"] <= 4 and not is_immune(m)]
    if at_risk:
        for m in sorted(at_risk, key=lambda x: x["fitness"]):
            cycles_left = max(0, m["fitness"] - DEMOTE_THRESHOLD)
            content += f"- {m['id']} [F:{m['fitness']}] → latente em ~{cycles_left} ciclo(s): {m['text'][:60]}...\n"
    else:
        content += "- Nenhuma memória em risco imediato\n"

    content += f"""
---
*Ciclo automático — Protocolo v4 (Memória em Camadas)*
*Nenhuma memória é deletada. Rebaixar > apagar.*
"""

    filename = f"sonho_clawd_{DATE_STR}.md"
    if not DRY_RUN:
        (SONHOS_DIR / filename).write_text(content)
        try:
            (SANDMAN_SONHOS / filename).write_text(content)
        except Exception:
            pass  # sandman dir might not exist
    return content


def main():
    print(f"🌙 Ciclo de Sonho v4 — {DATE_STR}")
    print(f"{'[DRY RUN] ' if DRY_RUN else ''}Modelo Cognitivo em Camadas\n")

    # Check for rescue mode
    rescue_tags = None
    for arg in sys.argv:
        if arg.startswith("--rescue"):
            idx = sys.argv.index(arg)
            if idx + 1 < len(sys.argv):
                rescue_tags = sys.argv[idx + 1].split(",")

    # Step 1: Load all layers
    active = load_json(FITNESS_FILE)
    latente = load_json(LATENTE_FILE)
    arquivo = load_json(ARQUIVO_FILE)

    total_active = len(active["memories"])
    total_latente = len(latente["memories"])
    total_arquivo = len(arquivo["memories"])
    print(f"📖 Carregado: {total_active} ativas, {total_latente} latentes, {total_arquivo} arquivadas")

    # Optional: Rescue by tags
    if rescue_tags:
        rescued, active, latente, arquivo = rescue_by_tags(rescue_tags, latente, arquivo, active)
        if rescued:
            print(f"🔄 Resgatadas {len(rescued)} memórias por tags {rescue_tags}:")
            for src, m in rescued:
                print(f"   [{src}] → ativa: {m['text'][:60]}...")
        else:
            print(f"🔍 Nenhuma memória encontrada para tags {rescue_tags}")

    # Step 2+3: Decay (with immunity check)
    active["memories"], decayed, immune = decay(active["memories"])
    print(f"📉 Decaimento: {decayed} decaíram, {immune} imunes (< 14 dias)")

    # Step 4: Demote to latent
    active["memories"], demoted, latente = demote_to_latent(active["memories"], latente)
    if demoted:
        print(f"⬇️  {len(demoted)} rebaixada(s) para Latente:")
        for m in demoted:
            print(f"   - {m['text'][:60]}...")

    # Archive from latent
    latente, archived, arquivo = archive_from_latent(latente, arquivo)
    if archived:
        print(f"📦 {len(archived)} afundada(s) para Arquivo:")
        for m in archived:
            print(f"   - {m['text'][:60]}...")

    # Step 5: Graduate
    active["memories"], graduated = graduate(active["memories"])
    if graduated:
        print(f"🎓 {len(graduated)} graduada(s) → MEMORY.md:")
        for m in graduated:
            print(f"   - {m['text'][:60]}...")
        append_to_memory(graduated)

    # Update metadata
    active["version"] = 4
    active["lastCycle"] = NOW.isoformat()
    try:
        next_cycle = NOW + timedelta(hours=48)
        active["nextCycle"] = next_cycle.isoformat()
    except Exception:
        pass

    # Step 7: Register dream
    register_dream(active, demoted, archived, graduated, decayed, immune)

    # Save all layers
    save_json(FITNESS_FILE, active)
    save_json(LATENTE_FILE, latente)
    save_json(ARQUIVO_FILE, arquivo)

    # Summary
    print(f"\n✅ Ciclo completo:")
    print(f"   Ativas: {len(active['memories'])}")
    print(f"   Latentes: {len(latente['memories'])}")
    print(f"   Arquivadas: {len(arquivo['memories'])}")
    print(f"   Graduadas: {len(graduated)}")
    print(f"   ⚡ Nenhuma memória perdida — apenas reorganizada")
    return 0


if __name__ == "__main__":
    sys.exit(main())
