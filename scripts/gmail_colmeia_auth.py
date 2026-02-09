#!/usr/bin/env python3
"""
Gmail OAuth - Login para colmeia@inteia.com.br
"""

import pickle
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/gmail.send',
]

SECRETS_DIR = Path("/root/clawd/.secrets")
CREDS_FILE = SECRETS_DIR / "google_credentials.json"
TOKEN_FILE = SECRETS_DIR / "gmail_colmeia_token.pickle"  # Token separado!

def main():
    print("\n🐝 LOGIN COLMEIA@INTEIA.COM.BR")
    print("=" * 50)
    print("\n⚠️  IMPORTANTE: Faça login com colmeia@inteia.com.br")
    print("    NÃO use igormorais123@gmail.com!\n")
    
    flow = InstalledAppFlow.from_client_secrets_file(
        str(CREDS_FILE), 
        SCOPES,
        redirect_uri='urn:ietf:wg:oauth:2.0:oob'
    )
    
    auth_url, _ = flow.authorization_url(
        prompt='consent',
        login_hint='colmeia@inteia.com.br'  # Sugere a conta correta
    )
    
    print("1. Abra esta URL no navegador:\n")
    print(auth_url)
    print("\n2. FAÇA LOGIN COM: colmeia@inteia.com.br")
    print("3. Autorize o acesso")
    print("4. Copie o CÓDIGO que aparecer")
    print("\n" + "=" * 50)
    
    code = input("\nCole o código aqui: ").strip()
    
    flow.fetch_token(code=code)
    creds = flow.credentials
    
    # Salvar token separado para colmeia
    with open(TOKEN_FILE, 'wb') as token:
        pickle.dump(creds, token)
    
    print(f"\n✅ Token COLMEIA salvo em {TOKEN_FILE}")
    
    # Testar
    print("\n📧 Testando acesso ao colmeia@inteia.com.br...")
    from googleapiclient.discovery import build
    service = build('gmail', 'v1', credentials=creds)
    
    # Verificar perfil
    profile = service.users().getProfile(userId='me').execute()
    print(f"✅ Logado como: {profile['emailAddress']}")
    print(f"📬 Total de emails: {profile['messagesTotal']}")

if __name__ == "__main__":
    main()
