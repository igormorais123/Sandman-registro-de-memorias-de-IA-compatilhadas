#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Actions Monitor para igormorais123/pesquisa-eleitoral-df
Uso: python3 github_monitor.py [status|errors|watch]
"""

import sys
import json
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from datetime import datetime, timezone, timedelta

REPO = "igormorais123/pesquisa-eleitoral-df"
API_BASE = f"https://api.github.com/repos/{REPO}/actions"
BRT = timezone(timedelta(hours=-3))

STATUS_EMOJI = {
    "completed": "✅",
    "in_progress": "🔄",
    "queued": "⏳",
    "waiting": "⏳",
    "requested": "📋",
    "cancelled": "🚫",
}

CONCLUSION_EMOJI = {
    "success": "✅",
    "failure": "❌",
    "cancelled": "🚫",
    "timed_out": "⏰",
    "skipped": "⏭️",
    "action_required": "⚠️",
    "stale": "🧊",
    "neutral": "➖",
    "startup_failure": "💥",
}


def api_get(endpoint):
    """Faz GET na API do GitHub."""
    url = f"{API_BASE}/{endpoint}"
    req = Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "clawd-monitor/1.0",
    })
    try:
        with urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except HTTPError as e:
        if e.code == 403:
            print("⚠️  Rate limit da API GitHub atingido. Tente novamente em alguns minutos.")
        elif e.code == 404:
            print(f"❌ Repo não encontrado: {REPO}")
        else:
            print(f"❌ Erro HTTP {e.code}: {e.reason}")
        return None
    except URLError as e:
        print(f"❌ Erro de conexão: {e.reason}")
        return None


def format_time(iso_str):
    """Converte ISO timestamp para horário Brasília legível."""
    if not iso_str:
        return "—"
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00")).astimezone(BRT)
        return dt.strftime("%d/%m %H:%M")
    except Exception:
        return iso_str[:16]


def get_emoji(run):
    """Retorna emoji baseado no status/conclusion."""
    conclusion = run.get("conclusion")
    if conclusion:
        return CONCLUSION_EMOJI.get(conclusion, "❓")
    return STATUS_EMOJI.get(run.get("status", ""), "❓")


def cmd_status():
    """Lista últimos workflow runs."""
    data = api_get("runs?per_page=8")
    if not data:
        return

    runs = data.get("workflow_runs", [])
    if not runs:
        print("📭 Nenhum workflow run encontrado.")
        return

    print(f"\n🔧 GitHub Actions — {REPO}\n")
    print(f"{'':2}{'Status':8} {'Workflow':<30} {'Branch':<15} {'Quando':<12} {'Duração'}")
    print(f"  {'─'*80}")

    for run in runs:
        emoji = get_emoji(run)
        name = run.get("name", "?")[:28]
        branch = run.get("head_branch", "?")[:13]
        when = format_time(run.get("created_at"))

        # Calcular duração
        created = run.get("created_at")
        updated = run.get("updated_at")
        duration = "—"
        if created and updated:
            try:
                t1 = datetime.fromisoformat(created.replace("Z", "+00:00"))
                t2 = datetime.fromisoformat(updated.replace("Z", "+00:00"))
                secs = int((t2 - t1).total_seconds())
                if secs < 60:
                    duration = f"{secs}s"
                else:
                    duration = f"{secs // 60}m{secs % 60:02d}s"
            except Exception:
                pass

        conclusion = run.get("conclusion") or run.get("status", "?")
        print(f"  {emoji} {conclusion:<6} {name:<30} {branch:<15} {when:<12} {duration}")

    print()


def cmd_errors():
    """Mostra detalhes do run mais recente que falhou."""
    data = api_get("runs?status=failure&per_page=1")
    if not data:
        return

    runs = data.get("workflow_runs", [])
    if not runs:
        print("🎉 Nenhum workflow com falha encontrado!")
        return

    run = runs[0]
    run_id = run["id"]
    print(f"\n❌ Último run com falha:\n")
    print(f"  Workflow: {run.get('name')}")
    print(f"  Branch:   {run.get('head_branch')}")
    print(f"  Commit:   {run.get('head_sha', '')[:8]} — {run.get('head_commit', {}).get('message', '?')[:60]}")
    print(f"  Quando:   {format_time(run.get('created_at'))}")
    print(f"  URL:      {run.get('html_url')}")

    # Buscar jobs do run
    jobs_data = api_get(f"runs/{run_id}/jobs")
    if not jobs_data:
        return

    jobs = jobs_data.get("jobs", [])
    failed_jobs = [j for j in jobs if j.get("conclusion") == "failure"]

    if failed_jobs:
        print(f"\n  💥 Jobs com falha ({len(failed_jobs)}):\n")
        for job in failed_jobs:
            print(f"    🔸 {job.get('name')}")
            steps = job.get("steps", [])
            failed_steps = [s for s in steps if s.get("conclusion") == "failure"]
            for step in failed_steps:
                print(f"      ❌ Step: {step.get('name')}")
                print(f"         Status: {step.get('conclusion')}")
    else:
        print("\n  ⚠️  Nenhum job com falha detalhado encontrado.")

    print()


def cmd_watch():
    """Resumo one-liner do estado atual."""
    data = api_get("runs?per_page=5")
    if not data:
        print("⚠️ GitHub: sem dados")
        return

    runs = data.get("workflow_runs", [])
    if not runs:
        print("📭 GitHub: sem runs")
        return

    latest = runs[0]
    emoji = get_emoji(latest)
    name = latest.get("name", "?")
    branch = latest.get("head_branch", "?")
    conclusion = latest.get("conclusion") or latest.get("status", "?")
    when = format_time(latest.get("created_at"))

    # Contar recentes
    successes = sum(1 for r in runs if r.get("conclusion") == "success")
    failures = sum(1 for r in runs if r.get("conclusion") == "failure")

    print(f"{emoji} {name} ({branch}): {conclusion} @ {when} | Últimos 5: ✅{successes} ❌{failures}")


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 github_monitor.py [status|errors|watch]")
        print("  status  — Últimos workflow runs")
        print("  errors  — Detalhes do último run com falha")
        print("  watch   — Resumo one-liner")
        sys.exit(1)

    cmd = sys.argv[1].lower()

    if cmd == "status":
        cmd_status()
    elif cmd == "errors":
        cmd_errors()
    elif cmd == "watch":
        cmd_watch()
    else:
        print(f"❌ Comando desconhecido: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
