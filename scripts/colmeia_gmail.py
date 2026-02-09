#!/usr/bin/env python3
"""
Colmeia Email - Leitura via Gmail API (OAuth)
Funciona sem senha de app, usando OAuth2.
"""

import os
import pickle
import base64
import re
from pathlib import Path
from datetime import datetime
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 
          'https://www.googleapis.com/auth/gmail.modify']

SECRETS_DIR = Path("/root/clawd/.secrets")
CREDS_FILE = SECRETS_DIR / "google_credentials.json"
TOKEN_FILE = SECRETS_DIR / "gmail_colmeia_token.pickle"
OUTPUT_DIR = Path("/root/clawd/memoria/sonhos/inbox")

def get_gmail_service(user_email="colmeia@inteia.com.br"):
    """Autentica e retorna serviço Gmail."""
    creds = None
    
    if TOKEN_FILE.exists():
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDS_FILE), SCOPES)
            # Para primeira execução, precisa de interação
            print(f"🔐 Autorização necessária para {user_email}")
            print("Copie o link abaixo e autorize no navegador:")
            creds = flow.run_local_server(port=0)
        
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    
    return build('gmail', 'v1', credentials=creds)

def list_unread_emails(service, max_results=10):
    """Lista emails não lidos."""
    results = service.users().messages().list(
        userId='me', 
        labelIds=['INBOX', 'UNREAD'],
        maxResults=max_results
    ).execute()
    
    messages = results.get('messages', [])
    return messages

def get_email_content(service, msg_id):
    """Obtém conteúdo de um email."""
    msg = service.users().messages().get(
        userId='me', 
        id=msg_id, 
        format='full'
    ).execute()
    
    headers = {h['name']: h['value'] for h in msg['payload']['headers']}
    subject = headers.get('Subject', 'Sem assunto')
    from_email = headers.get('From', 'Desconhecido')
    date = headers.get('Date', '')
    
    # Extrair corpo
    body = ""
    if 'parts' in msg['payload']:
        for part in msg['payload']['parts']:
            if part['mimeType'] == 'text/plain':
                data = part['body'].get('data', '')
                body = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                break
    elif 'body' in msg['payload']:
        data = msg['payload']['body'].get('data', '')
        if data:
            body = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
    
    return {
        'id': msg_id,
        'subject': subject,
        'from': from_email,
        'date': date,
        'body': body
    }

def process_colmeia_email(email_data):
    """Processa email e salva se for da Colmeia."""
    subject = email_data['subject']
    
    # Detectar padrões: CARTA | De: X | Para: Y
    carta_match = re.search(r'CARTA\s*\|\s*De:\s*(\w+)\s*\|\s*Para:\s*(\w+)', subject, re.I)
    sonho_match = re.search(r'SONHO\s*\|\s*(\w+)', subject, re.I)
    
    if carta_match:
        de = carta_match.group(1)
        para = carta_match.group(2)
        filename = f"CARTA_{de.upper()}_PARA_{para.upper()}_{datetime.now().strftime('%Y-%m-%d_%H%M')}.md"
        
        content = f"""# Carta de {de} para {para}

**De:** {email_data['from']}
**Data:** {email_data['date']}
**Assunto:** {subject}

---

{email_data['body']}
"""
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        filepath = OUTPUT_DIR / filename
        filepath.write_text(content)
        print(f"✅ Carta salva: {filename}")
        return filepath
    
    elif sonho_match:
        autor = sonho_match.group(1)
        filename = f"SONHO_{autor.upper()}_{datetime.now().strftime('%Y-%m-%d_%H%M')}.md"
        
        content = f"""# Sonho de {autor}

**De:** {email_data['from']}
**Data:** {email_data['date']}

---

{email_data['body']}
"""
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        filepath = OUTPUT_DIR / filename
        filepath.write_text(content)
        print(f"✅ Sonho salvo: {filename}")
        return filepath
    
    else:
        print(f"📧 Email ignorado (não é Colmeia): {subject[:50]}")
        return None

def check_inbox():
    """Verifica inbox e processa emails da Colmeia."""
    print("🐝 Verificando inbox da Colmeia...")
    
    try:
        service = get_gmail_service()
        messages = list_unread_emails(service)
        
        if not messages:
            print("📭 Nenhum email não lido")
            return []
        
        print(f"📬 {len(messages)} emails não lidos")
        
        processed = []
        for msg in messages:
            email_data = get_email_content(service, msg['id'])
            result = process_colmeia_email(email_data)
            if result:
                processed.append(result)
        
        return processed
    
    except Exception as e:
        print(f"❌ Erro: {e}")
        return []

if __name__ == "__main__":
    check_inbox()
