#!/usr/bin/env python3
"""
Fechamento automatico de P032/P033/P034.

Executa:
1) verificar_heartbeats.py --dias 7
2) analise_custo_p033.py --dias 7
3) gerar_relatorio_aceite.py --dias 7

Gera um resumo em operacional/FECHAMENTO_P032_P034_YYYY-MM-DD.md
"""

from __future__ import annotations

import subprocess
from datetime import datetime
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = REPO_ROOT / "operacional"
PYTHON = r"C:\Python314\python.exe"


def run(cmd: list[str]) -> tuple[int, str, str]:
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=str(REPO_ROOT))
    return p.returncode, p.stdout, p.stderr


def main() -> int:
    steps = [
        [PYTHON, "scripts/verificar_heartbeats.py", "--dias", "7"],
        [PYTHON, "scripts/analise_custo_p033.py", "--dias", "7"],
        [PYTHON, "scripts/gerar_relatorio_aceite.py", "--dias", "7"],
    ]

    results = []
    for cmd in steps:
        code, out, err = run(cmd)
        results.append(
            {
                "cmd": " ".join(cmd),
                "code": code,
                "stdout": out.strip(),
                "stderr": err.strip(),
            }
        )

    ok = all(r["code"] == 0 for r in results)
    now = datetime.now()
    out_file = OUT_DIR / f"FECHAMENTO_P032_P034_{now.strftime('%Y-%m-%d')}.md"
    lines = []
    lines.append("# Fechamento P032/P033/P034")
    lines.append("")
    lines.append(f"Gerado em: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"Status geral: {'OK' if ok else 'ERRO'}")
    lines.append("")
    for i, r in enumerate(results, 1):
        lines.append(f"## Etapa {i}")
        lines.append(f"Comando: `{r['cmd']}`")
        lines.append(f"Exit code: `{r['code']}`")
        if r["stdout"]:
            lines.append("")
            lines.append("Saida:")
            lines.append("```text")
            lines.append(r["stdout"])
            lines.append("```")
        if r["stderr"]:
            lines.append("")
            lines.append("Erro:")
            lines.append("```text")
            lines.append(r["stderr"])
            lines.append("```")
        lines.append("")

    lines.append("## Proxima acao")
    lines.append("1. Abrir `operacional/RELATORIO_ACEITE.md`.")
    lines.append("2. Marcar decisao GO/GO COM RESSALVAS/NO-GO.")
    lines.append("3. Preencher assinaturas.")
    lines.append("")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_file.write_text("\n".join(lines), encoding="utf-8")
    print(str(out_file))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
