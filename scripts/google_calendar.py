#!/usr/bin/env python3
"""
google_calendar.py - Consulta eventos do Google Calendar via gcalcli
Versao: 2.1 (2026-02-13) - Secrets movidos para env vars

Uso:
    python3 google_calendar.py today      # Eventos de hoje
    python3 google_calendar.py tomorrow   # Eventos de amanha  
    python3 google_calendar.py week       # Proximos 7 dias

Requer:
    GOOGLE_CALENDAR_CLIENT_ID e GOOGLE_CALENDAR_CLIENT_SECRET em env vars
    ou em /root/.openclaw/credentials/google_calendar.json
"""

import subprocess
import sys
import os
import json
from datetime import datetime, timedelta

GCALCLI_PATH = "/root/.local/bin/gcalcli"
CREDS_FILE = "/root/.openclaw/credentials/google_calendar.json"

def load_credentials():
    """Carrega credenciais de env vars ou arquivo"""
    client_id = os.environ.get("GOOGLE_CALENDAR_CLIENT_ID")
    client_secret = os.environ.get("GOOGLE_CALENDAR_CLIENT_SECRET")
    
    if client_id and client_secret:
        return client_id, client_secret
    
    if os.path.exists(CREDS_FILE):
        with open(CREDS_FILE) as f:
            creds = json.load(f)
            return creds.get("client_id", ""), creds.get("client_secret", "")
    
    print(json.dumps({
        "status": "error",
        "message": "Google Calendar credentials not configured.",
        "setup": "Set GOOGLE_CALENDAR_CLIENT_ID and GOOGLE_CALENDAR_CLIENT_SECRET env vars, or create " + CREDS_FILE
    }, indent=2))
    sys.exit(1)

def run_gcalcli(args: list) -> str:
    """Executa gcalcli com credenciais"""
    client_id, client_secret = load_credentials()
    cmd = [
        GCALCLI_PATH,
        "--client-id", client_id,
        "--client-secret", client_secret,
        "--nocolor"
    ] + args
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return result.stdout
    except Exception as e:
        return f"Erro: {e}"

def get_agenda(start_date: str, end_date: str) -> str:
    return run_gcalcli(["agenda", start_date, end_date])

def format_output(raw: str, label: str) -> str:
    lines = raw.strip().split("\n")
    if not lines or not raw.strip():
        return f"{label}: Nenhum evento encontrado."
    
    events = []
    current_date = None
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line[0:3] in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
            current_date = line
        elif line and current_date:
            events.append(f"  - {line}")
    
    if not events:
        return f"{label}: Nenhum evento encontrado."
    return f"{label}:\n" + "\n".join(events[:10])

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 google_calendar.py [today|tomorrow|week]")
        sys.exit(1)
    
    cmd = sys.argv[1].lower()
    today = datetime.now()
    
    if cmd == "today":
        start = today.strftime("%Y-%m-%d")
        end = (today + timedelta(days=1)).strftime("%Y-%m-%d")
        label = "Hoje"
    elif cmd == "tomorrow":
        t = today + timedelta(days=1)
        start = t.strftime("%Y-%m-%d")
        end = (t + timedelta(days=1)).strftime("%Y-%m-%d")
        label = "Amanha"
    elif cmd == "week":
        start = today.strftime("%Y-%m-%d")
        end = (today + timedelta(days=7)).strftime("%Y-%m-%d")
        label = "Proximos 7 dias"
    else:
        print(f"Comando desconhecido: {cmd}")
        sys.exit(1)
    
    raw = get_agenda(start, end)
    print(format_output(raw, label))

if __name__ == "__main__":
    main()
