#!/usr/bin/env python3
"""
🐝 Colmeia Email Check
Lê emails de colmeia@inteia.com.br e processa cartas/sonhos automaticamente.
Roda no heartbeat.
"""

import pickle
import re
import json
from pathlib import Path
from datetime import datetime
from googleapiclient.discovery import build
import base64

TOKEN_FILE = Path("/root/clawd/.secrets/gmail_colmeia_token.pickle")
OUTPUT_DIR = Path("/root/clawd/memoria/sonhos/inbox")
PROCESSED_FILE = Path("/root/clawd/.secrets/colmeia_processed_emails.json")

def get_service():
    """Conecta ao Gmail."""
    with open(TOKEN_FILE, 'rb') as token:
        creds = pickle.load(token)
    return build('gmail', 'v1', credentials=creds)

def get_processed_ids():
    """Retorna IDs de emails já processados."""
    if PROCESSED_FILE.exists():
        return set(json.loads(PROCESSED_FILE.read_text()))
    return set()

def save_processed_id(msg_id):
    """Salva ID como processado."""
    ids = get_processed_ids()
    ids.add(msg_id)
    PROCESSED_FILE.write_text(json.dumps(list(ids)))

def get_email_body(payload):
    """Extrai corpo do email."""
    body = ""
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                data = part['body'].get('data', '')
                if data:
                    body = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                    break
    elif 'body' in payload:
        data = payload['body'].get('data', '')
        if data:
            body = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
    return body

def process_email(service, msg_id):
    """Processa um email e salva se for da Colmeia."""
    msg = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
    headers = {h['name']: h['value'] for h in msg['payload']['headers']}
    
    subject = headers.get('Subject', '')
    from_email = headers.get('From', '')
    date = headers.get('Date', '')
    body = get_email_body(msg['payload'])
    
    # Detectar padrão: CARTA | De: X | Para: Y
    carta_match = re.search(r'CARTA\s*\|\s*De:\s*(\w+)\s*\|\s*Para:\s*(\w+)', subject, re.I)
    sonho_match = re.search(r'SONHO\s*\|\s*(\w+)', subject, re.I)
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    if carta_match:
        de = carta_match.group(1).upper()
        para = carta_match.group(2).upper()
        filename = f"CARTA_{de}_PARA_{para}_{datetime.now().strftime('%Y-%m-%d_%H%M')}.md"
        
        content = f"""# Carta de {de} para {para}

**De:** {from_email}
**Data:** {date}
**Assunto:** {subject}

---

{body}
"""
        filepath = OUTPUT_DIR / filename
        filepath.write_text(content)
        print(f"✅ CARTA salva: {filename}")
        return {"type": "carta", "de": de, "para": para, "file": str(filepath)}
    
    elif sonho_match:
        autor = sonho_match.group(1).upper()
        filename = f"SONHO_{autor}_{datetime.now().strftime('%Y-%m-%d_%H%M')}.md"
        
        content = f"""# Sonho de {autor}

**De:** {from_email}
**Data:** {date}

---

{body}
"""
        filepath = OUTPUT_DIR / filename
        filepath.write_text(content)
        print(f"✅ SONHO salvo: {filename}")
        return {"type": "sonho", "autor": autor, "file": str(filepath)}
    
    else:
        # Email normal - não processar
        print(f"📧 Ignorado (não é Colmeia): {subject[:40]}...")
        return None

def check_inbox():
    """Verifica inbox e processa emails novos."""
    print("🐝 Verificando colmeia@inteia.com.br...")
    
    service = get_service()
    processed_ids = get_processed_ids()
    
    # Buscar emails não lidos
    results = service.users().messages().list(
        userId='me',
        labelIds=['INBOX', 'UNREAD'],
        maxResults=20
    ).execute()
    
    messages = results.get('messages', [])
    
    if not messages:
        print("📭 Nenhum email não lido")
        return []
    
    print(f"📬 {len(messages)} emails não lidos")
    
    processed = []
    for msg in messages:
        if msg['id'] in processed_ids:
            continue
        
        result = process_email(service, msg['id'])
        if result:
            processed.append(result)
            # Marcar como lido
            service.users().messages().modify(
                userId='me',
                id=msg['id'],
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
        
        save_processed_id(msg['id'])
    
    if processed:
        print(f"\n🐝 Processados: {len(processed)} emails da Colmeia!")
    
    return processed

if __name__ == "__main__":
    check_inbox()
