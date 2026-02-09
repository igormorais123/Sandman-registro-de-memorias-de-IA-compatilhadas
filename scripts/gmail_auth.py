#!/usr/bin/env python3
"""
Gmail OAuth - Autenticação para leitura de emails
Executa uma vez para gerar o token.
"""

import os
import pickle
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Scopes necessários (Gmail readonly)
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/gmail.labels'
]

SECRETS_DIR = Path("/root/clawd/.secrets")
CREDS_FILE = SECRETS_DIR / "google_credentials.json"
TOKEN_FILE = SECRETS_DIR / "gmail_token.pickle"

def main():
    creds = None
    
    # Verificar token existente
    if TOKEN_FILE.exists():
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
        print(f"Token existente encontrado")
        print(f"Válido: {creds.valid}")
        print(f"Scopes: {creds.scopes}")
    
    # Se não tem credenciais válidas, fazer novo fluxo
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Renovando token expirado...")
            creds.refresh(Request())
        else:
            print("\n🔐 AUTORIZAÇÃO NECESSÁRIA")
            print("=" * 50)
            print("1. Vai abrir uma janela no navegador")
            print("2. Faça login com igormorais123@gmail.com")
            print("3. Autorize o acesso ao Gmail")
            print("=" * 50)
            
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDS_FILE), 
                SCOPES
            )
            creds = flow.run_local_server(port=8080)
        
        # Salvar token
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
        print(f"\n✅ Token salvo em {TOKEN_FILE}")
    
    # Testar
    print("\n📧 Testando acesso ao Gmail...")
    from googleapiclient.discovery import build
    service = build('gmail', 'v1', credentials=creds)
    
    # Listar labels para confirmar
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])
    print(f"✅ Conexão OK! {len(labels)} labels encontrados")
    
    # Contar emails não lidos
    results = service.users().messages().list(
        userId='me', 
        labelIds=['INBOX', 'UNREAD'],
        maxResults=5
    ).execute()
    messages = results.get('messages', [])
    print(f"📬 {len(messages)} emails não lidos na inbox")

if __name__ == "__main__":
    main()
