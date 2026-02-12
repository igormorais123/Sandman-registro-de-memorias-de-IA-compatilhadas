#!/usr/bin/env python3
"""
Colmeia v6 - Gerador de Relatorio de Aceite
Preenche automaticamente o RELATORIO_ACEITE.md com dados do soak test.

Uso:
  python gerar_relatorio_aceite.py              # ultimos 7 dias
  python gerar_relatorio_aceite.py --dias 7     # especificar dias
  python gerar_relatorio_aceite.py --preview    # so mostra, nao salva
"""

import argparse
import json
import sys
import io
import re
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

if sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
LOGS_DIR = REPO_ROOT / "operacional" / "logs"
RELATORIO_PATH = REPO_ROOT / "operacional" / "RELATORIO_ACEITE.md"


def carregar_logs(dias=7):
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
    total = len(entradas)
    por_agente = defaultdict(list)
    por_dia = defaultdict(list)

    for e in entradas:
        por_agente[e["agente"]].append(e)
        dia = e["timestamp"][:10]
        por_dia[dia].append(e)

    sucessos = sum(1 for e in entradas if e.get("resultado") != "ERRO")
    taxa = round((sucessos / total * 100), 1) if total else 0
    duracoes = [e["duracao_ms"] for e in entradas if "duracao_ms" in e]
    duracao_media = round(sum(duracoes) / len(duracoes), 1) if duracoes else 0
    erros = sum(1 for e in entradas if e.get("resultado") == "ERRO")

    agentes = {}
    for ag, logs in sorted(por_agente.items()):
        a_total = len(logs)
        a_suc = sum(1 for e in logs if e.get("resultado") != "ERRO")
        a_trab = sum(1 for e in logs if str(e.get("resultado", "")).startswith("TRABALHO"))
        agentes[ag] = {
            "total": a_total,
            "taxa": round((a_suc / a_total * 100), 1) if a_total else 0,
            "trabalho": a_trab,
            "idle": a_total - a_trab,
        }

    dias_stats = {}
    for dia, logs in sorted(por_dia.items()):
        d_total = len(logs)
        d_suc = sum(1 for e in logs if e.get("resultado") != "ERRO")
        dias_stats[dia] = {
            "ciclos": d_total,
            "taxa": round((d_suc / d_total * 100), 1) if d_total else 0,
            "agentes": len(set(e.get("agente") for e in logs)),
        }

    return {
        "total": total,
        "taxa": taxa,
        "duracao_media": duracao_media,
        "erros": erros,
        "dias_com_dados": len(por_dia),
        "agentes_ativos": len(por_agente),
        "agentes": agentes,
        "dias": dias_stats,
        "meta_atingida": taxa >= 90,
    }


def calcular_custos_estimados(kpis, dias):
    # Assuncoes conservadoras para referencia de API (nao custo real observado)
    idle_tokens = 500
    trabalho_tokens = 2000
    preco_ref = 0.00012

    total_idle = sum(v["idle"] for v in kpis["agentes"].values())
    sonnet_work = 0
    opus_work = 0

    for nome, stats in kpis["agentes"].items():
        n = nome.lower()
        if n in ("nexo", "sandman"):
            sonnet_work += stats["trabalho"]
        elif n in ("onir", "helena"):
            opus_work += stats["trabalho"]

    haiku_tokens_total = total_idle * idle_tokens
    sonnet_tokens_total = sonnet_work * trabalho_tokens
    opus_tokens_total = opus_work * trabalho_tokens
    total_tokens = haiku_tokens_total + sonnet_tokens_total + opus_tokens_total

    divisor = max(dias, 1)
    haiku_tokens_dia = haiku_tokens_total / divisor
    sonnet_tokens_dia = sonnet_tokens_total / divisor
    opus_tokens_dia = opus_tokens_total / divisor
    total_tokens_dia = total_tokens / divisor

    return {
        "haiku_tokens_dia": round(haiku_tokens_dia),
        "sonnet_tokens_dia": round(sonnet_tokens_dia),
        "opus_tokens_dia": round(opus_tokens_dia),
        "total_tokens_dia": round(total_tokens_dia),
        "haiku_custo_dia": haiku_tokens_dia * preco_ref,
        "sonnet_custo_dia": sonnet_tokens_dia * preco_ref,
        "opus_custo_dia": opus_tokens_dia * preco_ref,
        "total_custo_dia": total_tokens_dia * preco_ref,
    }


def gerar_tabela_kpis(kpis, dias):
    meta_tag = "ATINGIDA" if kpis["meta_atingida"] else "NAO_ATINGIDA"
    return "\n".join([
        f"| Taxa de sucesso global | >= 90% | {kpis['taxa']}% | {meta_tag} |",
        f"| Ciclos totais ({dias} dias) | >= 1.300 | {kpis['total']} | {'OK' if kpis['total'] >= 1300 else 'BAIXO'} |",
        f"| Agentes ativos | 4/4 | {kpis['agentes_ativos']}/4 | {'OK' if kpis['agentes_ativos'] >= 4 else 'BAIXO'} |",
        "| Missed runs (scheduler) | 0 | - | verificar Task Scheduler |",
        f"| Duracao media ciclo | < 500ms | {kpis['duracao_media']}ms | {'OK' if kpis['duracao_media'] < 500 else 'ALTO'} |",
        f"| Erros criticos | 0 | {kpis['erros']} | {'OK' if kpis['erros'] == 0 else 'ATENCAO'} |",
        f"| Dias com cobertura | 7/7 | {kpis['dias_com_dados']}/7 | {'OK' if kpis['dias_com_dados'] >= 7 else 'INCOMPLETO'} |",
    ])


def gerar_tabela_agentes(kpis):
    linhas = []
    for nome, stats in kpis["agentes"].items():
        linhas.append(f"| {nome.upper()} | {stats['total']} | {stats['taxa']}% | {stats['trabalho']} | {stats['idle']} |")
    return "\n".join(linhas)


def gerar_tabela_dias(kpis):
    linhas = []
    for i, (dia, stats) in enumerate(kpis["dias"].items(), 1):
        linhas.append(f"| {i} | {dia} | {stats['ciclos']} | {stats['taxa']}% | {stats['agentes']}/4 |")
    return "\n".join(linhas)


def gerar_tabela_custos(kpis, dias):
    c = calcular_custos_estimados(kpis, dias)
    return "\n".join([
        f"| Haiku 4.5 (triagem) | {c['haiku_tokens_dia']:,} tokens | R$ {c['haiku_custo_dia']:.2f}/dia |",
        f"| Sonnet 4.5 (NEXO/Sandman) | {c['sonnet_tokens_dia']:,} tokens | R$ {c['sonnet_custo_dia']:.2f}/dia |",
        f"| Opus 4.6 (ONIR/Helena) | {c['opus_tokens_dia']:,} tokens | R$ {c['opus_custo_dia']:.2f}/dia |",
        f"| **Total execucao/dia** | {c['total_tokens_dia']:,} tokens | **R$ {c['total_custo_dia']:.2f}/dia** |",
    ])


def preencher_relatorio(kpis, dias):
    if not RELATORIO_PATH.exists():
        print(f"ERRO: {RELATORIO_PATH} nao encontrado")
        sys.exit(1)

    conteudo = RELATORIO_PATH.read_text(encoding="utf-8")
    hoje = datetime.now().strftime("%Y-%m-%d")

    # Status
    if dias >= 7:
        status = f"**Status:** PREENCHIDO (dados do soak test inseridos em {hoje})"
    else:
        status = f"**Status:** RASCUNHO ATIVO (atualizacao parcial automatica em {hoje}, janela {dias} dia[s])"
    conteudo = re.sub(r"\*\*Status:\*\*.*", status, conteudo, count=1)

    # KPIs tabela
    kpi_body = gerar_tabela_kpis(kpis, dias)
    conteudo = re.sub(
        r"(\| Metrica \| Meta \| Resultado \| Status \|\n\|[-| ]+\|\n)(.*?)(\n### Detalhamento por Agente)",
        r"\1" + kpi_body + r"\3",
        conteudo,
        flags=re.S,
        count=1,
    )

    # Agentes tabela
    ag_body = gerar_tabela_agentes(kpis)
    conteudo = re.sub(
        r"(\| Agente \| Ciclos \| Taxa \| Trabalho \| Idle \|\n\|[-| ]+\|\n)(.*?)(\n### Historico Diario)",
        r"\1" + ag_body + r"\3",
        conteudo,
        flags=re.S,
        count=1,
    )

    # Dias tabela
    dias_body = gerar_tabela_dias(kpis)
    conteudo = re.sub(
        r"(\| Dia \| Data \| Ciclos \| Taxa \| Agentes \|\n\|[-| ]+\|\n)(.*?)(\n---)",
        r"\1" + dias_body + r"\3",
        conteudo,
        flags=re.S,
        count=1,
    )

    # Custos por modelo
    custo_body = gerar_tabela_custos(kpis, dias)
    conteudo = re.sub(
        r"(\| Modelo \| Uso \| Custo estimado/dia \|\n\|[-| ]+\|\n)(.*?)(\n### Recomendacao P033)",
        r"\1" + custo_body + r"\3",
        conteudo,
        flags=re.S,
        count=1,
    )

    return conteudo


def main():
    parser = argparse.ArgumentParser(description="Gerar relatorio de aceite")
    parser.add_argument("--dias", type=int, default=7)
    parser.add_argument("--preview", action="store_true", help="Apenas mostra, nao salva")
    args = parser.parse_args()

    entradas = carregar_logs(args.dias)
    if not entradas:
        print(f"Nenhum log encontrado nos ultimos {args.dias} dias.")
        sys.exit(1)

    kpis = calcular_kpis(entradas)
    conteudo = preencher_relatorio(kpis, args.dias)

    if args.preview:
        print(conteudo)
    else:
        RELATORIO_PATH.write_text(conteudo, encoding="utf-8")
        print(f"Relatorio atualizado: {RELATORIO_PATH}")
        print(f"Taxa de sucesso: {kpis['taxa']}%")
        print(f"Meta {'ATINGIDA' if kpis['meta_atingida'] else 'NAO ATINGIDA'}")


if __name__ == "__main__":
    main()
