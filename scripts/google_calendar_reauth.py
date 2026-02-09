#!/usr/bin/env python3
"""
Google Calendar OAuth - Reautenticação manual
"""

import pickle
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/calendar']

SECRETS_DIR = Path("/root/clawd/.secrets")
CREDS_FILE = SECRETS_DIR / "google_credentials.json"
TOKEN_FILE = SECRETS_DIR / "google_token.pickle"

def main():
    print("\n🗓️ REAUTORIZAÇÃO GOOGLE CALENDAR")
    print("=" * 50)
    
    flow = InstalledAppFlow.from_client_secrets_file(
        str(CREDS_FILE), 
        SCOPES,
        redirect_uri='urn:ietf:wg:oauth:2.0:oob'
    )
    
    auth_url, _ = flow.authorization_url(
        prompt='consent',
        login_hint='igormorais123@gmail.com'
    )
    
    print("\n1. Abra esta URL no navegador:\n")
    print(auth_url)
    print("\n2. Faça login com igormorais123@gmail.com")
    print("3. Autorize o acesso ao Calendar")
    print("4. Copie o CÓDIGO que aparecer")
    print("\n" + "=" * 50)
    
    code = input("\nCole o código aqui: ").strip()
    
    flow.fetch_token(code=code)
    creds = flow.credentials
    
    with open(TOKEN_FILE, 'wb') as token:
        pickle.dump(creds, token)
    
    print(f"\n✅ Token salvo em {TOKEN_FILE}")
    
    # Testar
    print("\n📅 Testando acesso ao Calendar...")
    from googleapiclient.discovery import build
    service = build('calendar', 'v3', credentials=creds)
    
    calendars = service.calendarList().list().execute()
    print(f"✅ Acesso OK! {len(calendars.get('items', []))} calendários encontrados")

if __name__ == "__main__":
    main()
