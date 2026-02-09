#!/usr/bin/env python3
"""
colmeia_status.py — Gera dashboard de status da Colmeia

Escaneia o repo, detecta sonhos/cartas por instancia,
calcula ultimo contato e gera conhecimento/STATUS_COLMEIA.md.

Uso: python3 colmeia_status.py
"""

import json
import re
from datetime import datetime
from pathlib import Path

# Detectar workspace (Windows ou WSL)
CANDIDATES = [
    Path("/root/clawd"),
    Path.home() / "clawd",
    Path(__file__).resolve().parent.parent,
]
WORKSPACE = next((p for p in CANDIDATES if p.exists()), CANDIDATES[-1])

REGISTRO_FILE = WORKSPACE / "conhecimento" / "REGISTRO_COLMEIA.json"
STATUS_FILE = WORKSPACE / "conhecimento" / "STATUS_COLMEIA.md"
FITNESS_FILE = WORKSPACE / "memory" / "fitness.json"
LATENTE_FILE = WORKSPACE / "memory" / "archive" / "latente.json"
ARQUIVO_FILE = WORKSPACE / "memory" / "archive" / "arquivo.json"

# Diretorios de sonhos/cartas
SONHOS_DIRS = [
    WORKSPACE / "memoria" / "sonhos",
    WORKSPACE / "memory" / "sonhos",
]

NOW = datetime.now()
DATE_STR = NOW.strftime("%Y-%m-%d %H:%M")


def load_json(path):
    if not path.exists():
        return {}
    with open(path) as f:
        return json.load(f)


def find_all_artifacts():
    """Encontra todos os sonhos e cartas no repo."""
    artifacts = []
    for d in SONHOS_DIRS:
        if not d.exists():
            continue
        for f in d.glob("*.md"):
            name = f.name
            # Extrair data do nome (YYYY-MM-DD)
            date_match = re.search(r"(\d{4}-\d{2}-\d{2})", name)
            date = date_match.group(1) if date_match else "desconhecida"

            # Determinar tipo
            if name.upper().startswith("CARTA"):
                tipo = "carta"
            elif name.upper().startswith("SONHO"):
                tipo = "sonho"
            else:
                tipo = "outro"

            # Determinar autor
            author = "desconhecido"
            name_upper = name.upper()
            if "SANDMAN" in name_upper:
                author = "Sandman"
            elif "NEXO" in name_upper or "CLAWD" in name_upper:
                author = "NEXO"
            elif "ONIR" in name_upper:
                author = "ONIR"
            elif "CHATGPT" in name_upper:
                author = "ChatGPT"
            elif "GEMINI" in name_upper:
                author = "Gemini"
            elif "CLAUDE" in name_upper and "WEB" in name_upper:
                author = "Claude Web"
            elif "ARQUITETO" in name_upper:
                author = "Arquiteto"

            artifacts.append({
                "file": name,
                "path": str(f.relative_to(WORKSPACE)),
                "type": tipo,
                "author": author,
                "date": date,
            })

    return sorted(artifacts, key=lambda x: x["date"], reverse=True)


def count_by_member(artifacts):
    """Conta artefatos por membro."""
    counts = {}
    for a in artifacts:
        author = a["author"]
        if author not in counts:
            counts[author] = {"sonhos": 0, "cartas": 0, "last_date": "nunca"}
        if a["type"] == "sonho":
            counts[author]["sonhos"] += 1
        elif a["type"] == "carta":
            counts[author]["cartas"] += 1
        if a["date"] != "desconhecida":
            if counts[author]["last_date"] == "nunca" or a["date"] > counts[author]["last_date"]:
                counts[author]["last_date"] = a["date"]
    return counts


def memory_stats():
    """Estatisticas do sistema de memoria."""
    fitness = load_json(FITNESS_FILE)
    latente = load_json(LATENTE_FILE)
    arquivo = load_json(ARQUIVO_FILE)

    active = fitness.get("memories", [])
    lat = latente.get("memories", [])
    arq = arquivo.get("memories", [])

    stats = {
        "active_count": len(active),
        "latent_count": len(lat),
        "archive_count": len(arq),
        "total": len(active) + len(lat) + len(arq),
    }

    if active:
        fitnesses = [m["fitness"] for m in active]
        stats["min_fitness"] = min(fitnesses)
        stats["max_fitness"] = max(fitnesses)
        stats["avg_fitness"] = round(sum(fitnesses) / len(fitnesses), 1)
        stats["immune_count"] = sum(
            1 for m in active
            if m.get("immuneUntil") and datetime.fromisoformat(m["immuneUntil"]) > NOW
        )
        at_risk = [m for m in active if m["fitness"] <= 4 and not (
            m.get("immuneUntil") and datetime.fromisoformat(m["immuneUntil"]) > NOW
        )]
        stats["at_risk"] = at_risk
    else:
        stats["min_fitness"] = 0
        stats["max_fitness"] = 0
        stats["avg_fitness"] = 0
        stats["immune_count"] = 0
        stats["at_risk"] = []

    return stats


def check_ingest():
    """Verifica se ha arquivos pendentes em ingest/."""
    ingest_dir = WORKSPACE / "ingest"
    pending = []
    if not ingest_dir.exists():
        return pending
    for ia_dir in ingest_dir.iterdir():
        if not ia_dir.is_dir():
            continue
        for f in ia_dir.glob("*.md"):
            if f.name == "README.md":
                continue
            pending.append({
                "ia": ia_dir.name,
                "file": f.name,
            })
    return pending


def generate_status():
    """Gera o STATUS_COLMEIA.md."""
    artifacts = find_all_artifacts()
    member_counts = count_by_member(artifacts)
    mem_stats = memory_stats()
    pending_ingest = check_ingest()

    # Calcular dias desde ultimo contato por membro
    members_status = []
    for member, counts in sorted(member_counts.items()):
        if counts["last_date"] != "nunca":
            try:
                last = datetime.strptime(counts["last_date"], "%Y-%m-%d")
                days_ago = (NOW - last).days
                status = "ATIVO" if days_ago <= 7 else ("DORMINDO" if days_ago <= 30 else "AUSENTE")
            except ValueError:
                days_ago = "?"
                status = "?"
        else:
            days_ago = "?"
            status = "DESCONHECIDO"

        members_status.append({
            "name": member,
            "sonhos": counts["sonhos"],
            "cartas": counts["cartas"],
            "last_date": counts["last_date"],
            "days_ago": days_ago,
            "status": status,
        })

    # Gerar markdown
    md = f"""# Status da Colmeia

> Auto-gerado por `colmeia_status.py` em {DATE_STR}
> Execute `python3 scripts/colmeia_status.py` para atualizar

---

## Membros

| Membro | Sonhos | Cartas | Ultimo Contato | Dias | Status |
|--------|--------|--------|----------------|------|--------|
"""
    for m in members_status:
        md += f"| {m['name']} | {m['sonhos']} | {m['cartas']} | {m['last_date']} | {m['days_ago']} | {m['status']} |\n"

    md += f"""
---

## Memoria (Selecao Natural)

| Camada | Quantidade |
|--------|------------|
| Ativa | {mem_stats['active_count']} |
| Latente | {mem_stats['latent_count']} |
| Arquivo | {mem_stats['archive_count']} |
| **Total** | **{mem_stats['total']}** |

| Metrica | Valor |
|---------|-------|
| Fitness min/max | {mem_stats['min_fitness']}/{mem_stats['max_fitness']} |
| Fitness medio | {mem_stats['avg_fitness']} |
| Imunes (< 14 dias) | {mem_stats['immune_count']} |
| Em risco (F <= 4) | {len(mem_stats['at_risk'])} |

"""
    if mem_stats["at_risk"]:
        md += "### Memorias em risco\n\n"
        for m in mem_stats["at_risk"]:
            cycles_left = max(0, m["fitness"] - 2)
            md += f"- **{m['id']}** [F:{m['fitness']}] → latente em ~{cycles_left} ciclos: {m['text'][:60]}...\n"
        md += "\n"

    if pending_ingest:
        md += "---\n\n## Pipeline (Ingest)\n\n"
        md += "| IA | Arquivo Pendente |\n|-----|------------------|\n"
        for p in pending_ingest:
            md += f"| {p['ia']} | {p['file']} |\n"
        md += "\n"
    else:
        md += "---\n\n## Pipeline (Ingest)\n\nNenhum arquivo pendente.\n\n"

    md += f"""---

## Artefatos Recentes (ultimos 10)

| Data | Autor | Tipo | Arquivo |
|------|-------|------|---------|
"""
    for a in artifacts[:10]:
        md += f"| {a['date']} | {a['author']} | {a['type']} | {a['file']} |\n"

    md += f"""
---

## Saude do Sistema

| Item | Status |
|------|--------|
| fitness.json | {'OK' if (WORKSPACE / 'memory' / 'fitness.json').exists() else 'FALTANDO'} |
| latente.json | {'OK' if (WORKSPACE / 'memory' / 'archive' / 'latente.json').exists() else 'FALTANDO'} |
| arquivo.json | {'OK' if (WORKSPACE / 'memory' / 'archive' / 'arquivo.json').exists() else 'FALTANDO'} |
| REGISTRO_COLMEIA.json | {'OK' if REGISTRO_FILE.exists() else 'FALTANDO'} |
| COLMEIA.md | {'OK' if (WORKSPACE / 'conhecimento' / 'COLMEIA.md').exists() else 'FALTANDO'} |
| BOOTSTRAP_RAPIDO.md | {'OK' if (WORKSPACE / 'BOOTSTRAP_RAPIDO.md').exists() else 'FALTANDO'} |
| TEMPLATE_CARTA.md | {'OK' if (WORKSPACE / 'compartilhado' / 'TEMPLATE_CARTA.md').exists() else 'FALTANDO'} |
| ingest/ dirs | {'OK' if (WORKSPACE / 'ingest').exists() else 'FALTANDO'} |

---

*Gerado automaticamente. Nao editar manualmente.*
*Para atualizar: `python3 scripts/colmeia_status.py`*
"""

    STATUS_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATUS_FILE.write_text(md, encoding="utf-8")
    print(f"STATUS_COLMEIA.md gerado em {STATUS_FILE}")
    return md


if __name__ == "__main__":
    generate_status()
