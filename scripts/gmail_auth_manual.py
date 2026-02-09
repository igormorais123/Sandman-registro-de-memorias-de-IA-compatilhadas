#!/usr/bin/env python3
"""
Gmail OAuth - Versão manual (cola o código)
"""

import pickle
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.modify',
]

SECRETS_DIR = Path("/root/clawd/.secrets")
CREDS_FILE = SECRETS_DIR / "google_credentials.json"
TOKEN_FILE = SECRETS_DIR / "gmail_token.pickle"

def main():
    print("\n🔐 AUTORIZAÇÃO GMAIL - MODO MANUAL")
    print("=" * 50)
    
    flow = InstalledAppFlow.from_client_secrets_file(
        str(CREDS_FILE), 
        SCOPES,
        redirect_uri='urn:ietf:wg:oauth:2.0:oob'
    )
    
    auth_url, _ = flow.authorization_url(prompt='consent')
    
    print("\n1. Abra esta URL no navegador:\n")
    print(auth_url)
    print("\n2. Faça login com igormorais123@gmail.com")
    print("3. Autorize o acesso")
    print("4. Copie o CÓDIGO que aparecer")
    print("\n" + "=" * 50)
    
    code = input("\nCole o código aqui: ").strip()
    
    flow.fetch_token(code=code)
    creds = flow.credentials
    
    # Salvar
    with open(TOKEN_FILE, 'wb') as token:
        pickle.dump(creds, token)
    
    print(f"\n✅ Token salvo em {TOKEN_FILE}")
    
    # Testar
    print("\n📧 Testando...")
    from googleapiclient.discovery import build
    service = build('gmail', 'v1', credentials=creds)
    results = service.users().messages().list(
        userId='me', 
        labelIds=['INBOX'],
        maxResults=3
    ).execute()
    messages = results.get('messages', [])
    print(f"✅ Funcionou! {len(messages)} emails encontrados")

if __name__ == "__main__":
    main()
