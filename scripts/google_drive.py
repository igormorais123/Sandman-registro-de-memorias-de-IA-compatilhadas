#!/usr/bin/env python3
"""
Google Drive integration for Clawd
Uso:
  python3 google_drive.py auth          → Re-autenticar com scopes Calendar + Drive
  python3 google_drive.py auth_code CODE → Completar auth com código
  python3 google_drive.py list FOLDER_ID → Listar pasta
  python3 google_drive.py download FILE_ID [destino] → Baixar arquivo
  python3 google_drive.py read FILE_ID   → Ler conteúdo de texto/doc
  python3 google_drive.py tree FOLDER_ID [depth] → Árvore completa da pasta
"""

import os
import sys
import json
import pickle
import io
from datetime import datetime
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# Escopos: Calendar + Drive (readonly)
SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/drive.readonly',
]

SECRETS_DIR = Path("/root/clawd/.secrets")
CREDENTIALS_FILE = SECRETS_DIR / "google_credentials.json"
TOKEN_FILE = SECRETS_DIR / "google_token.pickle"


def get_auth_url():
    """Gera URL de autorização para o usuário visitar."""
    flow = InstalledAppFlow.from_client_secrets_file(
        str(CREDENTIALS_FILE), SCOPES,
        redirect_uri='urn:ietf:wg:oauth:2.0:oob'
    )
    auth_url, _ = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )
    # Salvar o flow state pra completar depois
    flow_state = {
        'client_config': json.loads(CREDENTIALS_FILE.read_text()),
        'scopes': SCOPES,
    }
    with open(SECRETS_DIR / "drive_flow_state.json", 'w') as f:
        json.dump(flow_state, f)
    
    return auth_url


def complete_auth(code):
    """Completa autenticação com o código do usuário."""
    flow = InstalledAppFlow.from_client_secrets_file(
        str(CREDENTIALS_FILE), SCOPES,
        redirect_uri='urn:ietf:wg:oauth:2.0:oob'
    )
    flow.fetch_token(code=code)
    creds = flow.credentials
    
    with open(TOKEN_FILE, 'wb') as token:
        pickle.dump(creds, token)
    
    print(f"✅ Autenticado com sucesso!")
    print(f"Scopes: {creds.scopes}")
    print(f"Válido: {creds.valid}")
    return creds


def get_credentials():
    """Obtém credenciais válidas."""
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
            print("❌ Token inválido. Rode: python3 google_drive.py auth")
            sys.exit(1)
    
    # Verificar se tem scope de Drive
    if creds.scopes and 'https://www.googleapis.com/auth/drive.readonly' not in creds.scopes:
        print("⚠️ Token não tem scope de Drive. Rode: python3 google_drive.py auth")
        sys.exit(1)
    
    return creds


def get_drive_service():
    """Retorna serviço do Drive."""
    creds = get_credentials()
    return build('drive', 'v3', credentials=creds)


def list_folder(folder_id):
    """Lista conteúdo de uma pasta."""
    service = get_drive_service()
    
    results = service.files().list(
        q=f"'{folder_id}' in parents and trashed = false",
        pageSize=100,
        fields="nextPageToken, files(id, name, mimeType, modifiedTime, size)",
        orderBy="name"
    ).execute()
    
    items = results.get('files', [])
    
    if not items:
        print("📂 Pasta vazia.")
        return items
    
    print(f"📂 {len(items)} itens:\n")
    for item in items:
        mime = item.get('mimeType', '')
        size = item.get('size', '')
        modified = item.get('modifiedTime', '')[:10]
        
        if 'folder' in mime:
            icon = '📁'
            size_str = ''
        elif 'document' in mime:
            icon = '📄'
            size_str = ''
        elif 'spreadsheet' in mime:
            icon = '📊'
            size_str = ''
        elif 'presentation' in mime:
            icon = '📽️'
            size_str = ''
        else:
            icon = '📎'
            size_str = f" ({int(size)//1024}KB)" if size else ''
        
        print(f"  {icon} {item['name']}{size_str}  [{modified}]  id:{item['id']}")
    
    return items


def tree_folder(folder_id, depth=2, prefix="", current_depth=0):
    """Mostra árvore recursiva de uma pasta."""
    if current_depth >= depth:
        return
    
    service = get_drive_service()
    
    results = service.files().list(
        q=f"'{folder_id}' in parents and trashed = false",
        pageSize=100,
        fields="files(id, name, mimeType, size)",
        orderBy="name"
    ).execute()
    
    items = results.get('files', [])
    
    for i, item in enumerate(items):
        is_last = (i == len(items) - 1)
        connector = "└── " if is_last else "├── "
        mime = item.get('mimeType', '')
        
        if 'folder' in mime:
            print(f"{prefix}{connector}📁 {item['name']}/")
            next_prefix = prefix + ("    " if is_last else "│   ")
            tree_folder(item['id'], depth, next_prefix, current_depth + 1)
        else:
            size = item.get('size', '')
            size_str = f" ({int(size)//1024}KB)" if size else ''
            print(f"{prefix}{connector}{item['name']}{size_str}")


def read_file(file_id):
    """Lê conteúdo de um arquivo (texto, Google Doc, etc)."""
    service = get_drive_service()
    
    # Primeiro, pegar metadata
    meta = service.files().get(fileId=file_id, fields="name, mimeType").execute()
    mime = meta.get('mimeType', '')
    name = meta.get('name', '')
    
    print(f"📄 {name} ({mime})\n{'='*60}\n")
    
    if 'google-apps.document' in mime:
        # Google Doc → exportar como texto
        content = service.files().export(fileId=file_id, mimeType='text/plain').execute()
        print(content.decode('utf-8'))
    elif 'google-apps.spreadsheet' in mime:
        # Google Sheet → exportar como CSV
        content = service.files().export(fileId=file_id, mimeType='text/csv').execute()
        print(content.decode('utf-8'))
    elif mime.startswith('text/') or mime in ['application/json', 'application/xml']:
        # Arquivo de texto direto
        content = service.files().get_media(fileId=file_id).execute()
        print(content.decode('utf-8'))
    else:
        print(f"⚠️ Tipo {mime} — use 'download' para baixar como arquivo.")


def download_file(file_id, dest=None):
    """Baixa um arquivo."""
    service = get_drive_service()
    
    meta = service.files().get(fileId=file_id, fields="name, mimeType, size").execute()
    name = meta.get('name', '')
    mime = meta.get('mimeType', '')
    
    dest_path = Path(dest) if dest else Path(f"/root/clawd/downloads/{name}")
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    
    if 'google-apps' in mime:
        # Google Doc/Sheet/Slides → exportar
        export_map = {
            'google-apps.document': ('application/pdf', '.pdf'),
            'google-apps.spreadsheet': ('text/csv', '.csv'),
            'google-apps.presentation': ('application/pdf', '.pdf'),
        }
        for key, (export_mime, ext) in export_map.items():
            if key in mime:
                content = service.files().export(fileId=file_id, mimeType=export_mime).execute()
                dest_path = dest_path.with_suffix(ext)
                dest_path.write_bytes(content)
                print(f"✅ Exportado: {dest_path} ({len(content)} bytes)")
                return str(dest_path)
        
        print(f"⚠️ Tipo Google não suportado: {mime}")
        return None
    else:
        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
        
        dest_path.write_bytes(fh.getvalue())
        print(f"✅ Baixado: {dest_path} ({len(fh.getvalue())} bytes)")
        return str(dest_path)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == 'auth':
        url = get_auth_url()
        print("🔗 Abra este link no seu navegador:\n")
        print(url)
        print("\n📋 Depois de autorizar, copie o código e rode:")
        print("python3 google_drive.py auth_code SEU_CODIGO_AQUI")
    
    elif cmd == 'auth_code':
        if len(sys.argv) < 3:
            print("❌ Uso: python3 google_drive.py auth_code CODIGO")
            sys.exit(1)
        complete_auth(sys.argv[2])
    
    elif cmd == 'list':
        if len(sys.argv) < 3:
            print("❌ Uso: python3 google_drive.py list FOLDER_ID")
            sys.exit(1)
        list_folder(sys.argv[2])
    
    elif cmd == 'tree':
        folder_id = sys.argv[2] if len(sys.argv) > 2 else None
        depth = int(sys.argv[3]) if len(sys.argv) > 3 else 2
        if not folder_id:
            print("❌ Uso: python3 google_drive.py tree FOLDER_ID [depth]")
            sys.exit(1)
        print(f"🌳 Árvore (profundidade {depth}):\n")
        tree_folder(folder_id, depth)
    
    elif cmd == 'read':
        if len(sys.argv) < 3:
            print("❌ Uso: python3 google_drive.py read FILE_ID")
            sys.exit(1)
        read_file(sys.argv[2])
    
    elif cmd == 'download':
        file_id = sys.argv[2] if len(sys.argv) > 2 else None
        dest = sys.argv[3] if len(sys.argv) > 3 else None
        if not file_id:
            print("❌ Uso: python3 google_drive.py download FILE_ID [destino]")
            sys.exit(1)
        download_file(file_id, dest)
    
    else:
        print(f"❌ Comando desconhecido: {cmd}")
        print(__doc__)
        sys.exit(1)
