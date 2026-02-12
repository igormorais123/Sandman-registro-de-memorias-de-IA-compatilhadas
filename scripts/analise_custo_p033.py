#!/usr/bin/env python3
"""
P033 - Analise de custo operacional da Colmeia v6.

Gera relatorio em Markdown com:
- metricas reais de heartbeat (logs JSONL)
- custo real de infraestrutura local (zero)
- cenarios estimados de custo API (apenas referencia)
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
LOGS_DIR = REPO_ROOT / "operacional" / "logs"
OUT_FILE = REPO_ROOT / "operacional" / "P033_ANALISE_CUSTO.md"


def carregar_logs(prefix: str, dias: int) -> list[dict]:
    hoje = datetime.now()
    dados = []
    for i in range(dias):
        data = (hoje - timedelta(days=i)).strftime("%Y-%m-%d")
        arq = LOGS_DIR / f"{prefix}_{data}.jsonl"
        if not arq.exists():
            continue
        with open(arq, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        dados.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
    return dados


def main() -> int:
    parser = argparse.ArgumentParser(description="Gera analise de custo P033")
    parser.add_argument("--dias", type=int, default=1)
    parser.add_argument("--out", default=str(OUT_FILE))
    args = parser.parse_args()

    hb = carregar_logs("heartbeat", args.dias)
    nt = carregar_logs("notificacao", args.dias)

    total_hb = len(hb)
    por_resultado = defaultdict(int)
    por_agente = defaultdict(int)
    trabalho = 0
    idle = 0
    duracoes = []
    for e in hb:
        r = e.get("resultado", "DESCONHECIDO")
        por_resultado[r] += 1
        por_agente[e.get("agente", "desconhecido")] += 1
        if r.startswith("TRABALHO"):
            trabalho += 1
        if r == "HEARTBEAT_OK":
            idle += 1
        if "duracao_ms" in e:
            try:
                duracoes.append(float(e["duracao_ms"]))
            except Exception:
                pass

    sucesso = sum(1 for e in hb if e.get("resultado") != "ERRO")
    taxa = (sucesso / total_hb * 100.0) if total_hb else 0.0
    duracao_media = (sum(duracoes) / len(duracoes)) if duracoes else 0.0

    notif_total = len(nt)
    notif_entregues = 0
    notif_reprog = 0
    notif_falha = 0
    for e in nt:
        s = e.get("stats", {})
        notif_entregues += int(s.get("entregues", 0))
        notif_reprog += int(s.get("reprogramadas", 0))
        notif_falha += int(s.get("falhas_finais", 0))

    # Inferencia de custo API (cenario hipotetico, nao uso real)
    # Assuncao: idle=500 tokens; trabalho=2000 tokens por ciclo.
    tok_idle = idle * 500
    tok_work = trabalho * 2000
    tok_total = tok_idle + tok_work
    tok_dia_medio = tok_total / max(args.dias, 1)
    tok_mes = tok_dia_medio * 30

    # referencia simplificada: R$ 0.00012 por token (composite conservador)
    custo_token_ref = 0.00012
    custo_api_estimado_mes = tok_mes * custo_token_ref
    custo_account_first_mes = custo_api_estimado_mes * 0.20  # meta >=80% conta

    linhas = []
    linhas.append("# P033 - Analise de Custo Operacional (parcial)")
    linhas.append("")
    linhas.append(f"Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    linhas.append(f"Janela analisada: {args.dias} dia(s)")
    linhas.append("")
    linhas.append("## 1. Dados Reais de Operacao")
    linhas.append("")
    linhas.append(f"- Ciclos de heartbeat: **{total_hb}**")
    linhas.append(f"- Taxa de sucesso: **{taxa:.1f}%**")
    linhas.append(f"- Duracao media de ciclo: **{duracao_media:.1f} ms**")
    linhas.append(f"- Ciclos de trabalho: **{trabalho}**")
    linhas.append(f"- Ciclos idle: **{idle}**")
    linhas.append("")
    linhas.append("### Distribuicao por agente")
    linhas.append("")
    for a, c in sorted(por_agente.items()):
        linhas.append(f"- `{a}`: {c} ciclos")
    linhas.append("")
    linhas.append("### Notificacoes")
    linhas.append("")
    linhas.append(f"- Execucoes do daemon: **{notif_total}**")
    linhas.append(f"- Entregues: **{notif_entregues}**")
    linhas.append(f"- Reprogramadas: **{notif_reprog}**")
    linhas.append(f"- Falhas finais: **{notif_falha}**")
    linhas.append("")
    linhas.append("## 2. Custo Real Atual (observado)")
    linhas.append("")
    linhas.append("- Infra local (SQLite/WAL, scheduler, daemon): **R$ 0,00 adicional**")
    linhas.append("- Custo incremental do piloto (sem API obrigatoria): **R$ 0,00 adicional**")
    linhas.append("")
    linhas.append("## 3. Cenario de Referencia (se API fosse usada em tudo)")
    linhas.append("")
    linhas.append("Assuncoes de inferencia (conservadoras):")
    linhas.append("- idle: 500 tokens/ciclo")
    linhas.append("- trabalho: 2000 tokens/ciclo")
    linhas.append("- preco composto de referencia: R$ 0,00012/token")
    linhas.append("")
    linhas.append(f"- Tokens estimados por dia: **{tok_dia_medio:,.0f}**")
    linhas.append(f"- Tokens estimados por mes: **{tok_mes:,.0f}**")
    linhas.append(f"- Custo API estimado/mes (100% API): **R$ {custo_api_estimado_mes:,.2f}**")
    linhas.append(f"- Custo API estimado/mes (account-first 80/20): **R$ {custo_account_first_mes:,.2f}**")
    linhas.append("")
    linhas.append("## 4. Recomendacao P033 (parcial)")
    linhas.append("")
    linhas.append("1. Manter politica `account-first` como padrao.")
    linhas.append("2. Preservar `USE_API=false` no caminho critico.")
    linhas.append("3. Recalcular esta analise no fechamento do soak de 7 dias.")
    linhas.append("4. Fechar P033 com numero oficial medio de 7 dias e assinar no P034.")
    linhas.append("")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(linhas), encoding="utf-8")
    print(str(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
