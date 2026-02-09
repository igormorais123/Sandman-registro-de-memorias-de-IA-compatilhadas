#!/usr/bin/env python3
"""
Google OAuth com redirect localhost — funciona em WSL.
Abre um servidor temporário na porta 8085 pra capturar o código.
"""

import os
import sys
import json
import pickle
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/drive.readonly',
]

SECRETS_DIR = Path("/root/clawd/.secrets")
CREDENTIALS_FILE = SECRETS_DIR / "google_credentials.json"
TOKEN_FILE = SECRETS_DIR / "google_token.pickle"
PORT = 8085

auth_code = None
server_done = threading.Event()


class AuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        query = parse_qs(urlparse(self.path).query)
        
        if 'code' in query:
            auth_code = query['code'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(b"""
            <html><body style="font-family:sans-serif; text-align:center; padding:50px;">
            <h1>&#x2705; Autorizado!</h1>
            <p>Pode fechar esta aba e voltar pro Clawd.</p>
            </body></html>
            """)
            server_done.set()
        elif 'error' in query:
            self.send_response(400)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            error = query.get('error', ['unknown'])[0]
            self.wfile.write(f"<h1>Erro: {error}</h1>".encode())
            server_done.set()
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass  # silenciar logs


def main():
    global auth_code
    
    # Modificar credentials pra usar localhost redirect
    cred_data = json.loads(CREDENTIALS_FILE.read_text())
    key = list(cred_data.keys())[0]
    
    # Criar flow com redirect pra localhost
    flow = InstalledAppFlow.from_client_secrets_file(
        str(CREDENTIALS_FILE),
        SCOPES,
        redirect_uri=f'http://localhost:{PORT}'
    )
    
    auth_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )
    
    print(f"🔗 Abra este link no navegador do seu PC:\n")
    print(auth_url)
    print(f"\n⏳ Aguardando autorização na porta {PORT}...")
    print(f"   (O navegador vai redirecionar pra localhost:{PORT} automaticamente)")
    
    # Iniciar servidor
    server = HTTPServer(('0.0.0.0', PORT), AuthHandler)
    server.timeout = 300  # 5 min timeout
    
    # Esperar o callback
    while not server_done.is_set():
        server.handle_request()
    
    server.server_close()
    
    if not auth_code:
        print("❌ Não recebi o código de autorização.")
        sys.exit(1)
    
    print(f"\n✅ Código recebido! Trocando por token...")
    
    # Trocar código por token
    flow.fetch_token(code=auth_code)
    creds = flow.credentials
    
    # Salvar token
    with open(TOKEN_FILE, 'wb') as token:
        pickle.dump(creds, token)
    
    print(f"✅ Token salvo com sucesso!")
    print(f"   Scopes: {creds.scopes}")
    print(f"   Válido: {creds.valid}")
    print(f"   Refresh token: {'Sim' if creds.refresh_token else 'Não'}")
    
    # Teste rápido
    from googleapiclient.discovery import build
    service = build('drive', 'v3', credentials=creds)
    about = service.about().get(fields="user").execute()
    print(f"   Conta: {about['user']['emailAddress']}")
    print(f"\n🎉 Pronto! Agora posso acessar seu Google Drive.")


if __name__ == '__main__':
    main()
