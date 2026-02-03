#!/usr/bin/env python3
"""
colmeia_sync_drive.py — Sincroniza Google Drive → repo Sandman

Puxa sonhos/cartas que irmãos (Claude Web, Gemini) salvaram no Drive
e integra no repo Git. Roda via cron ou heartbeat.

Uso:
  python3 colmeia_sync_drive.py          → Sync completo
  python3 colmeia_sync_drive.py --dry    → Só mostra o que faria
"""

import os
import sys
import json
import pickle
import hashlib
from datetime import datetime
from pathlib import Path

# Tentar importar Google APIs
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
except ImportError:
    print("❌ google-api-python-client não instalado")
    sys.exit(1)

SECRETS_DIR = Path("/root/clawd/.secrets")
TOKEN_FILE = SECRETS_DIR / "google_token.pickle"
REPO_DIR = Path("/root/clawd/sandman")
SYNC_STATE_FILE = Path("/root/clawd/memory/drive_sync_state.json")
LOG_FILE = REPO_DIR / "logs"

# Pastas do Drive a monitorar (folder_id → destino no repo)
DRIVE_FOLDERS = {
    # Pasta principal claude-memoria-global
    "1jNLC2DAk566TcMdmQfR2WUUGVzRgUmCc": {
        "name": "claude-memoria-global",
        "subfolder_map": {
            "sonhos": "instancias/onir/sonhos",
            "laboratorio": "historico/claude-memoria-global/laboratorio",
            "consolidado": "historico/claude-memoria-global/consolidado",
        },
        "default_dest": "historico/claude-memoria-global",
    },
    # ONIR original
    "1Cd7EJN3UGob9kVwxTSzPpwhTJVIL9OPk": {
        "name": "onir-original",
        "default_dest": "historico/drive/onir-original",
    },
    # Gemini/Opal
    "1R_v3lolmLJQ2WBWFXOxImCHiorqcBrT8": {
        "name": "gemini-opal",
        "default_dest": "instancias/gemini/sonhos",
    },
    # Skill memória
    "1Kb8cCG1Ygawbq1FNyOA_BxslbKR50t_1": {
        "name": "skill-memoria",
        "default_dest": "skills/memoria-persistente-sono-rem",
    },
    # Guias Claude Web
    "162XlSYLcoUrTXJx-GJPuiLJ8R9qOPG-q": {
        "name": "guias-claude-web",
        "default_dest": "docs/guias-claude-web",
    },
}


def get_drive_service():
    """Obtém serviço do Drive autenticado."""
    if not TOKEN_FILE.exists():
        print("❌ Token Google não encontrado. Rode google_auth_drive.py primeiro.")
        sys.exit(1)

    with open(TOKEN_FILE, 'rb') as f:
        creds = pickle.load(f)

    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(TOKEN_FILE, 'wb') as f:
            pickle.dump(creds, f)

    return build('drive', 'v3', credentials=creds)


def load_sync_state():
    """Carrega estado do último sync."""
    if SYNC_STATE_FILE.exists():
        return json.loads(SYNC_STATE_FILE.read_text())
    return {"lastSync": None, "knownFiles": {}}


def save_sync_state(state):
    """Salva estado do sync."""
    SYNC_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    state["lastSync"] = datetime.now().isoformat()
    SYNC_STATE_FILE.write_text(json.dumps(state, indent=2))


def list_drive_files(service, folder_id, depth=0, max_depth=3):
    """Lista arquivos recursivamente."""
    if depth > max_depth:
        return []

    files = []
    results = service.files().list(
        q=f"'{folder_id}' in parents and trashed = false",
        pageSize=100,
        fields="files(id, name, mimeType, modifiedTime, size, md5Checksum)",
    ).execute()

    for item in results.get('files', []):
        if 'folder' in item.get('mimeType', ''):
            # Recursão em subpastas
            sub_files = list_drive_files(service, item['id'], depth + 1, max_depth)
            for sf in sub_files:
                sf['path'] = f"{item['name']}/{sf.get('path', sf['name'])}"
            files.extend(sub_files)
        else:
            item['path'] = item['name']
            files.append(item)

    return files


def download_file(service, file_id, mime_type):
    """Baixa conteúdo de um arquivo."""
    if 'google-apps.document' in mime_type:
        content = service.files().export(fileId=file_id, mimeType='text/plain').execute()
        return content.decode('utf-8')
    elif 'google-apps.spreadsheet' in mime_type:
        content = service.files().export(fileId=file_id, mimeType='text/csv').execute()
        return content.decode('utf-8')
    elif mime_type.startswith('text/') or mime_type in ['application/json', 'application/xml']:
        content = service.files().get_media(fileId=file_id).execute()
        return content.decode('utf-8')
    else:
        return None  # Binários são ignorados


def file_hash(content):
    """Hash do conteúdo pra detectar mudanças."""
    return hashlib.md5(content.encode()).hexdigest()


def sync_folder(service, folder_id, config, state, dry_run=False):
    """Sincroniza uma pasta do Drive pro repo."""
    name = config['name']
    default_dest = config['default_dest']
    subfolder_map = config.get('subfolder_map', {})

    print(f"\n📁 Sincronizando: {name}")
    files = list_drive_files(service, folder_id)

    new_files = 0
    updated_files = 0

    for f in files:
        file_id = f['id']
        mime = f.get('mimeType', '')
        modified = f.get('modifiedTime', '')
        path = f.get('path', f['name'])

        # Ignorar binários
        if mime.startswith('image/') or mime.startswith('video/') or mime.startswith('audio/'):
            continue
        if mime == 'application/octet-stream':
            continue

        # Determinar destino
        dest_dir = default_dest
        for sub_name, sub_dest in subfolder_map.items():
            if path.startswith(sub_name + '/'):
                dest_dir = sub_dest
                path = path[len(sub_name) + 1:]
                break

        # Garantir extensão .md pra Google Docs
        if 'google-apps.document' in mime and not path.endswith('.md'):
            path = path + '.md'

        dest_path = REPO_DIR / dest_dir / path

        # Checar se já processamos este arquivo (por ID + modified)
        known = state['knownFiles'].get(file_id, {})
        if known.get('modifiedTime') == modified:
            continue  # Sem mudanças

        # Baixar conteúdo
        content = download_file(service, file_id, mime)
        if content is None:
            continue

        # Checar se conteúdo mudou (pode ter mesmo modifiedTime diferente)
        content_hash = file_hash(content)
        if dest_path.exists():
            existing_hash = file_hash(dest_path.read_text())
            if existing_hash == content_hash:
                state['knownFiles'][file_id] = {
                    'modifiedTime': modified,
                    'hash': content_hash,
                    'dest': str(dest_path.relative_to(REPO_DIR)),
                }
                continue

        action = "NOVO" if not dest_path.exists() else "ATUALIZADO"

        if dry_run:
            print(f"  {'🆕' if action == 'NOVO' else '🔄'} [{action}] {dest_dir}/{path}")
        else:
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            dest_path.write_text(content)
            print(f"  {'🆕' if action == 'NOVO' else '🔄'} [{action}] {dest_dir}/{path}")

        state['knownFiles'][file_id] = {
            'modifiedTime': modified,
            'hash': content_hash,
            'dest': str(dest_path.relative_to(REPO_DIR)) if not dry_run else f"{dest_dir}/{path}",
        }

        if action == "NOVO":
            new_files += 1
        else:
            updated_files += 1

    return new_files, updated_files


def main():
    dry_run = '--dry' in sys.argv

    if dry_run:
        print("🔍 Modo DRY RUN — nada será alterado\n")

    service = get_drive_service()
    state = load_sync_state()

    total_new = 0
    total_updated = 0

    for folder_id, config in DRIVE_FOLDERS.items():
        try:
            new, updated = sync_folder(service, folder_id, config, state, dry_run)
            total_new += new
            total_updated += updated
        except Exception as e:
            print(f"  ❌ Erro em {config['name']}: {e}")

    if not dry_run:
        save_sync_state(state)

    print(f"\n{'='*40}")
    print(f"📊 Resultado: {total_new} novos, {total_updated} atualizados")

    if total_new > 0 or total_updated > 0:
        print("SYNC_CHANGES")
    else:
        print("SYNC_CLEAN")


if __name__ == '__main__':
    main()
