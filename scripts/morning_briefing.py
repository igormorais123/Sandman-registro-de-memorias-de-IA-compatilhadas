#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Morning Briefing — Newsletter matinal do Igor
Combina: Calendar, Gmail, GitHub CI, System Health, Clima
Uso: python3 morning_briefing.py [--short]
"""

import sys
import os
import subprocess
import json
from datetime import datetime, timezone, timedelta
from urllib.request import urlopen, Request
from urllib.error import URLError

BRT = timezone(timedelta(hours=-3))
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))


def run_script(script_name, args=None):
    """Executa um script e retorna (stdout, stderr, returncode)."""
    cmd = [sys.executable, os.path.join(SCRIPTS_DIR, script_name)]
    if args:
        cmd.extend(args)
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=30
        )
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except subprocess.TimeoutExpired:
        return "", f"⏰ Timeout ao executar {script_name}", 1
    except FileNotFoundError:
        return "", f"❌ Script não encontrado: {script_name}", 1
    except Exception as e:
        return "", f"❌ Erro: {e}", 1


def get_weather():
    """Busca clima de Brasília via wttr.in."""
    try:
        req = Request(
            "https://wttr.in/Brasilia?format=j1",
            headers={"User-Agent": "clawd-briefing/1.0"}
        )
        with urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())

        current = data.get("current_condition", [{}])[0]
        temp = current.get("temp_C", "?")
        feels = current.get("FeelsLikeC", "?")
        humidity = current.get("humidity", "?")
        desc_pt = current.get("lang_pt", [{}])
        if desc_pt and isinstance(desc_pt, list):
            desc = desc_pt[0].get("value", current.get("weatherDesc", [{}])[0].get("value", "?"))
        else:
            desc = current.get("weatherDesc", [{}])[0].get("value", "?")

        # Previsão de hoje e amanhã
        forecasts = data.get("weather", [])
        forecast_lines = []
        for fc in forecasts[:2]:
            date = fc.get("date", "?")
            max_t = fc.get("maxtempC", "?")
            min_t = fc.get("mintempC", "?")
            try:
                dt = datetime.strptime(date, "%Y-%m-%d")
                day_name = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"][dt.weekday()]
                date_fmt = f"{day_name} {dt.strftime('%d/%m')}"
            except Exception:
                date_fmt = date
            forecast_lines.append(f"  {date_fmt}: {min_t}°–{max_t}°C")

        result = f"  🌡️ Agora: {temp}°C (sensação {feels}°C), {desc}\n"
        result += f"  💧 Umidade: {humidity}%\n"
        if forecast_lines:
            result += "  📊 Previsão:\n"
            for line in forecast_lines:
                result += f"    {line}\n"

        return result.rstrip()
    except Exception as e:
        return f"  ⚠️ Não foi possível obter clima: {e}"


def get_weather_oneliner():
    """Versão curta do clima."""
    try:
        req = Request(
            "https://wttr.in/Brasilia?format=%t+%C&lang=pt",
            headers={"User-Agent": "clawd-briefing/1.0"}
        )
        with urlopen(req, timeout=10) as resp:
            return resp.read().decode().strip()
    except Exception:
        return "⚠️ clima indisponível"


def section_calendar():
    """Seção de calendário."""
    out, err, rc = run_script("google_calendar.py", ["list", "2"])
    if rc != 0 or not out:
        return "  ⚠️ Não foi possível acessar o Google Calendar\n" + (f"  {err[:100]}" if err else "")
    return out


def section_email():
    """Seção de emails."""
    out, err, rc = run_script("check_gmail.py", ["--unread", "--days", "1", "--limit", "10"])
    if rc != 0 or not out:
        return "  ⚠️ Não foi possível verificar emails\n" + (f"  {err[:100]}" if err else "")
    return out


def section_github():
    """Seção GitHub CI."""
    out, err, rc = run_script("github_monitor.py", ["watch"])
    if rc != 0 or not out:
        return "  ⚠️ Não foi possível verificar GitHub Actions\n" + (f"  {err[:100]}" if err else "")
    return out


def section_health():
    """Seção de saúde do sistema."""
    out, err, rc = run_script("system_health.py")
    if not out:
        return "  ⚠️ Não foi possível verificar saúde do sistema"
    return out


def greeting():
    """Saudação baseada na hora."""
    hour = datetime.now(BRT).hour
    if hour < 12:
        return "☀️ Bom dia"
    elif hour < 18:
        return "🌤️ Boa tarde"
    else:
        return "🌙 Boa noite"


def build_briefing(short=False):
    """Monta o briefing completo."""
    now = datetime.now(BRT)
    weekdays = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    day_name = weekdays[now.weekday()]
    date_str = now.strftime(f"{day_name}, %d/%m/%Y — %H:%M")

    lines = []
    lines.append("═" * 50)
    lines.append(f"  {greeting()}, Igor! 🧠")
    lines.append(f"  📆 {date_str}")
    lines.append("═" * 50)

    if short:
        # Versão curta one-liner
        weather = get_weather_oneliner()
        github = section_github()
        health = section_health()

        lines.append(f"\n🌤️ Brasília: {weather}")
        lines.append(f"🔧 CI: {github}")
        lines.append(f"🖥️ Sistema: {health}")
        lines.append("")
        return "\n".join(lines)

    # --- Clima ---
    lines.append(f"\n🌤️ CLIMA — Brasília\n")
    lines.append(get_weather())

    # --- Calendário ---
    lines.append(f"\n{'─' * 50}")
    lines.append(f"📅 AGENDA (próximos 2 dias)\n")
    lines.append(section_calendar())

    # --- Emails ---
    lines.append(f"\n{'─' * 50}")
    lines.append(f"📧 EMAILS NÃO LIDOS\n")
    lines.append(section_email())

    # --- GitHub ---
    lines.append(f"\n{'─' * 50}")
    lines.append(f"🔧 GITHUB CI\n")
    lines.append(f"  {section_github()}")

    # --- Sistema ---
    lines.append(f"\n{'─' * 50}")
    lines.append(f"🖥️  SISTEMA\n")
    lines.append(f"  {section_health()}")

    # --- Footer ---
    lines.append(f"\n{'═' * 50}")
    lines.append(f"  Briefing gerado por Clawd 🤖")
    lines.append(f"{'═' * 50}\n")

    return "\n".join(lines)


def main():
    short = "--short" in sys.argv or "-s" in sys.argv
    print(build_briefing(short=short))


if __name__ == "__main__":
    main()
