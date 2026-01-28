#!/usr/bin/env python3
"""
Google Calendar integration for Clawd
Uso: python3 google_calendar.py [auth|list|today|add "titulo" "data hora"]
"""

import os
import sys
import json
import pickle
from datetime import datetime, timedelta
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Escopos necessários
SCOPES = ['https://www.googleapis.com/auth/calendar']

SECRETS_DIR = Path("/root/clawd/.secrets")
CREDENTIALS_FILE = SECRETS_DIR / "google_credentials.json"
TOKEN_FILE = SECRETS_DIR / "google_token.pickle"


def get_credentials():
    """Obtém ou atualiza credenciais."""
    creds = None
    
    if TOKEN_FILE.exists():
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(TOKEN_FILE, 'wb') as token:
                pickle.dump(creds, token)
        else:
            return None
    
    return creds


def authenticate():
    """Fluxo de autenticação OAuth."""
    flow = InstalledAppFlow.from_client_secrets_file(
        str(CREDENTIALS_FILE), SCOPES
    )
    
    # Gera URL de autenticação manualmente
    auth_url, _ = flow.authorization_url(access_type='offline', prompt='consent')
    
    print(f"\n🔗 Abra esta URL no navegador:\n\n{auth_url}\n")
    print("Após autorizar, você será redirecionado para uma página que não carrega.")
    print("Copie a URL COMPLETA da barra de endereço e cole aqui:\n")
    
    redirect_response = input("URL: ").strip()
    
    # Extrai o código da URL
    flow.fetch_token(authorization_response=redirect_response)
    creds = flow.credentials
    
    with open(TOKEN_FILE, 'wb') as token:
        pickle.dump(creds, token)
    
    print("\n✅ Autenticação concluída!")
    return creds


def list_events(days=7):
    """Lista eventos dos próximos N dias."""
    creds = get_credentials()
    if not creds:
        print("❌ Não autenticado. Execute: python3 google_calendar.py auth")
        return None
    
    service = build('calendar', 'v3', credentials=creds)
    
    now = datetime.utcnow().isoformat() + 'Z'
    end = (datetime.utcnow() + timedelta(days=days)).isoformat() + 'Z'
    
    events_result = service.events().list(
        calendarId='primary',
        timeMin=now,
        timeMax=end,
        maxResults=30,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])
    
    if not events:
        print(f"📅 Nenhum evento nos próximos {days} dias.")
        return []
    
    print(f"\n📅 Eventos dos próximos {days} dias:\n")
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        summary = event.get('summary', '(Sem título)')
        location = event.get('location', '')
        loc_str = f" @ {location}" if location else ""
        print(f"  • {start[:16].replace('T', ' ')} - {summary}{loc_str}")
    print()
    return events


def today_events():
    """Lista eventos de hoje."""
    creds = get_credentials()
    if not creds:
        print("❌ Não autenticado.")
        return []
    
    service = build('calendar', 'v3', credentials=creds)
    
    # Horário local (Brasília UTC-3)
    from datetime import timezone
    now = datetime.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = now.replace(hour=23, minute=59, second=59, microsecond=0)
    
    events_result = service.events().list(
        calendarId='primary',
        timeMin=today_start.isoformat() + '-03:00',
        timeMax=today_end.isoformat() + '-03:00',
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])
    
    if not events:
        print("📅 Nenhum evento hoje.")
    else:
        print("\n📅 Eventos de hoje:\n")
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            summary = event.get('summary', '(Sem título)')
            if 'T' in start:
                time_str = start[11:16]
            else:
                time_str = "Dia todo"
            print(f"  • {time_str} - {summary}")
    
    return events


def add_event(summary, start_time, duration_minutes=60):
    """Adiciona um evento."""
    creds = get_credentials()
    if not creds:
        print("❌ Não autenticado.")
        return None
    
    service = build('calendar', 'v3', credentials=creds)
    
    # Parse da data/hora
    try:
        start = datetime.strptime(start_time, "%Y-%m-%d %H:%M")
    except:
        try:
            start = datetime.strptime(start_time, "%d/%m/%Y %H:%M")
        except:
            print(f"❌ Formato de data inválido: {start_time}")
            return None
    
    end = start + timedelta(minutes=duration_minutes)
    
    event = {
        'summary': summary,
        'start': {
            'dateTime': start.isoformat(),
            'timeZone': 'America/Sao_Paulo',
        },
        'end': {
            'dateTime': end.isoformat(),
            'timeZone': 'America/Sao_Paulo',
        },
    }
    
    event = service.events().insert(calendarId='primary', body=event).execute()
    print(f"✅ Evento criado: {event.get('htmlLink')}")
    return event


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 google_calendar.py [auth|list|today|add]")
        print("  auth          - Autenticar com Google")
        print("  list [dias]   - Listar eventos (padrão: 7 dias)")
        print("  today         - Eventos de hoje")
        print('  add "titulo" "YYYY-MM-DD HH:MM" [duração_min]')
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "auth":
        authenticate()
    elif cmd == "list":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        list_events(days)
    elif cmd == "today":
        today_events()
    elif cmd == "add":
        if len(sys.argv) < 4:
            print('Uso: add "titulo" "YYYY-MM-DD HH:MM" [duração_min]')
        else:
            title = sys.argv[2]
            when = sys.argv[3]
            duration = int(sys.argv[4]) if len(sys.argv) > 4 else 60
            add_event(title, when, duration)
    else:
        print(f"Comando desconhecido: {cmd}")
