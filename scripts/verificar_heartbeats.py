#!/usr/bin/env python3
"""
Colmeia v6 — Verificador de Saude dos Heartbeats
Analisa logs JSONL e calcula KPIs do sistema.

Uso:
  python verificar_heartbeats.py              # ultimas 24h
  python verificar_heartbeats.py --dias 7     # ultimos 7 dias
  python verificar_heartbeats.py --json       # saida JSON
"""

import argparse
import json
import sys
import io
import os
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

if sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

LOGS_DIR = Path(__file__).parent.parent / "operacional" / "logs"


def carregar_logs(dias=1):
    """Carrega logs JSONL dos ultimos N dias."""
    entradas = []
    hoje = datetime.now()

    for i in range(dias):
        data = (hoje - timedelta(days=i)).strftime("%Y-%m-%d")
        log_file = LOGS_DIR / f"heartbeat_{data}.jsonl"

        if log_file.exists():
            with open(log_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        entradas.append(json.loads(line))

    return entradas


def calcular_kpis(entradas):
    """Calcula KPIs a partir dos logs."""
    if not entradas:
        return None

    total = len(entradas)
    por_agente = defaultdict(list)
    por_resultado = defaultdict(int)

    for e in entradas:
        por_agente[e["agente"]].append(e)
        por_resultado[e["resultado"]] += 1

    # Taxa de sucesso (qualquer resultado que nao seja erro)
    sucessos = sum(1 for e in entradas if e["resultado"] != "ERRO")
    taxa_sucesso = (sucessos / total) * 100 if total > 0 else 0

    # Duracao media
    duracoes = [e["duracao_ms"] for e in entradas if "duracao_ms" in e]
    duracao_media = sum(duracoes) / len(duracoes) if duracoes else 0

    # Trabalho vs idle
    trabalho = sum(1 for e in entradas if e["resultado"].startswith("TRABALHO"))
    idle = sum(1 for e in entradas if e["resultado"] == "HEARTBEAT_OK")

    # Por agente
    agentes_stats = {}
    for agente, logs in por_agente.items():
        a_total = len(logs)
        a_sucessos = sum(1 for e in logs if e["resultado"] != "ERRO")
        a_trabalho = sum(1 for e in logs if e["resultado"].startswith("TRABALHO"))
        agentes_stats[agente] = {
            "total": a_total,
            "sucesso": a_sucessos,
            "taxa_sucesso": (a_sucessos / a_total * 100) if a_total > 0 else 0,
            "trabalho": a_trabalho,
            "idle": a_total - a_trabalho,
        }

    # Timestamps
    timestamps = [e["timestamp"] for e in entradas]
    primeiro = min(timestamps) if timestamps else None
    ultimo = max(timestamps) if timestamps else None

    return {
        "periodo": {"primeiro": primeiro, "ultimo": ultimo},
        "total_ciclos": total,
        "taxa_sucesso": round(taxa_sucesso, 1),
        "duracao_media_ms": round(duracao_media, 1),
        "por_resultado": dict(por_resultado),
        "trabalho_vs_idle": {"trabalho": trabalho, "idle": idle},
        "por_agente": agentes_stats,
        "meta_atingida": taxa_sucesso >= 90,
    }


def imprimir_relatorio(kpis):
    """Imprime relatorio formatado."""
    print(f"\n  === RELATORIO DE SAUDE — Colmeia v6 ===")
    print(f"  Periodo: {kpis['periodo']['primeiro']} a {kpis['periodo']['ultimo']}")
    print(f"  " + "=" * 50)

    meta_icon = "ATINGIDA" if kpis["meta_atingida"] else "NAO ATINGIDA"
    print(f"\n  KPI Principal: Taxa de Sucesso = {kpis['taxa_sucesso']}% (meta: >=90%) [{meta_icon}]")
    print(f"  Total de ciclos: {kpis['total_ciclos']}")
    print(f"  Duracao media: {kpis['duracao_media_ms']}ms")

    print(f"\n  Resultados:")
    for resultado, count in kpis["por_resultado"].items():
        pct = (count / kpis["total_ciclos"]) * 100
        print(f"    {resultado:25s}: {count:4d} ({pct:.1f}%)")

    print(f"\n  Trabalho vs Idle:")
    t = kpis["trabalho_vs_idle"]
    print(f"    Trabalho: {t['trabalho']} ciclos")
    print(f"    Idle:     {t['idle']} ciclos")

    print(f"\n  Por Agente:")
    print(f"  {'Agente':12s} | {'Total':>6s} | {'Sucesso':>8s} | {'Taxa':>6s} | {'Trabalho':>9s}")
    print(f"  {'-'*12}-+-{'-'*6}-+-{'-'*8}-+-{'-'*6}-+-{'-'*9}")
    for agente, stats in kpis["por_agente"].items():
        print(f"  {agente:12s} | {stats['total']:6d} | {stats['sucesso']:8d} | {stats['taxa_sucesso']:5.1f}% | {stats['trabalho']:9d}")

    print()


def main():
    parser = argparse.ArgumentParser(description="Colmeia v6 — Verificador de Heartbeats")
    parser.add_argument("--dias", type=int, default=1, help="Quantidade de dias para analisar (default: 1)")
    parser.add_argument("--json", action="store_true", help="Saida em JSON")
    args = parser.parse_args()

    entradas = carregar_logs(args.dias)

    if not entradas:
        print(f"  Nenhum log encontrado nos ultimos {args.dias} dia(s).")
        print(f"  Diretorio de logs: {LOGS_DIR}")
        sys.exit(0)

    kpis = calcular_kpis(entradas)

    if args.json:
        print(json.dumps(kpis, ensure_ascii=False, indent=2))
    else:
        imprimir_relatorio(kpis)


if __name__ == "__main__":
    main()
