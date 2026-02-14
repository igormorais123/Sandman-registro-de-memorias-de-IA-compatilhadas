#!/usr/bin/env python3
"""
check_gmail.py - Verifica emails não lidos no Gmail
Versão: 2.0 (2026-02-13) - Integrado com Gmail API

Uso:
    python3 check_gmail.py --unread           # Emails não lidos
    python3 check_gmail.py --unread --limit 5 # Limitar quantidade
    python3 check_gmail.py --important        # Emails importantes não lidos
"""

import subprocess
import sys
import json
import argparse
from datetime import datetime

# Configuração - tokens fora do repo
import os
CONFIG_DIR = os.path.expanduser("~/.config/helena")
TOKEN_FILE = os.path.join(CONFIG_DIR, "tokens/gmail_token.json")
CREDENTIALS_FILE = os.path.join(CONFIG_DIR, "credentials.json")

def load_credentials():
    """Carrega client_id e client_secret do arquivo de credenciais"""
    try:
        with open(CREDENTIALS_FILE, 'r') as f:
            creds = json.load(f)
            installed = creds.get('installed', creds.get('web', {}))
            return installed.get('client_id'), installed.get('client_secret')
    except FileNotFoundError:
        print(f"❌ Credenciais não encontradas em {CREDENTIALS_FILE}")
        print("   Configure com: cp credentials.json ~/.config/helena/")
        sys.exit(1)

CLIENT_ID, CLIENT_SECRET = None, None  # Carregado em runtime

def load_token():
    """Carrega token do arquivo"""
    try:
        with open(TOKEN_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def refresh_token(token_data):
    """Renova o access token usando o refresh token"""
    import subprocess
    
    result = subprocess.run([
        'curl', '-s', '-X', 'POST', 'https://oauth2.googleapis.com/token',
        '-d', f"refresh_token={token_data['refresh_token']}",
        '-d', f"client_id={CLIENT_ID}",
        '-d', f"client_secret={CLIENT_SECRET}",
        '-d', 'grant_type=refresh_token'
    ], capture_output=True, text=True)
    
    new_token = json.loads(result.stdout)
    if 'access_token' in new_token:
        token_data['access_token'] = new_token['access_token']
        with open(TOKEN_FILE, 'w') as f:
            json.dump(token_data, f, indent=2)
        return token_data
    return None

def get_messages(access_token, query="is:unread", max_results=10):
    """Busca mensagens"""
    import urllib.parse
    
    q = urllib.parse.quote(query)
    result = subprocess.run([
        'curl', '-s',
        f"https://gmail.googleapis.com/gmail/v1/users/me/messages?maxResults={max_results}&q={q}",
        '-H', f"Authorization: Bearer {access_token}"
    ], capture_output=True, text=True)
    
    return json.loads(result.stdout)

def get_message_detail(access_token, msg_id):
    """Busca detalhes de uma mensagem"""
    result = subprocess.run([
        'curl', '-s',
        f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{msg_id}?format=metadata&metadataHeaders=From&metadataHeaders=Subject&metadataHeaders=Date",
        '-H', f"Authorization: Bearer {access_token}"
    ], capture_output=True, text=True)
    
    return json.loads(result.stdout)

def extract_headers(msg_detail):
    """Extrai headers relevantes"""
    headers = {}
    if 'payload' in msg_detail and 'headers' in msg_detail['payload']:
        for h in msg_detail['payload']['headers']:
            if h['name'] in ['From', 'Subject', 'Date']:
                headers[h['name']] = h['value']
    return headers

def main():
    global CLIENT_ID, CLIENT_SECRET
    
    parser = argparse.ArgumentParser(description='Verifica emails do Gmail')
    parser.add_argument('--unread', action='store_true', help='Mostrar não lidos')
    parser.add_argument('--important', action='store_true', help='Mostrar importantes')
    parser.add_argument('--limit', type=int, default=5, help='Limite de emails')
    args = parser.parse_args()
    
    # Carregar credenciais
    CLIENT_ID, CLIENT_SECRET = load_credentials()
    
    token_data = load_token()
    if not token_data:
        print("❌ Token não encontrado. Execute a configuração OAuth primeiro.")
        sys.exit(1)
    
    access_token = token_data['access_token']
    
    # Construir query
    query = "is:unread"
    if args.important:
        query += " is:important"
    
    # Buscar mensagens
    result = get_messages(access_token, query, args.limit)
    
    # Se erro de autenticação, tentar renovar token
    if 'error' in result:
        token_data = refresh_token(token_data)
        if token_data:
            access_token = token_data['access_token']
            result = get_messages(access_token, query, args.limit)
        else:
            print("❌ Erro ao renovar token")
            sys.exit(1)
    
    messages = result.get('messages', [])
    total = result.get('resultSizeEstimate', 0)
    
    if not messages:
        print("📧 Nenhum email não lido encontrado.")
        return
    
    print(f"📧 {total} emails não lidos (mostrando {len(messages)}):\n")
    
    for msg in messages[:args.limit]:
        detail = get_message_detail(access_token, msg['id'])
        headers = extract_headers(detail)
        
        sender = headers.get('From', 'Desconhecido')
        subject = headers.get('Subject', '(sem assunto)')
        
        # Limpar sender
        if '<' in sender:
            sender = sender.split('<')[0].strip().strip('"')
        
        # Truncar se muito longo
        if len(subject) > 50:
            subject = subject[:47] + "..."
        if len(sender) > 25:
            sender = sender[:22] + "..."
            
        print(f"  • [{sender}] {subject}")

if __name__ == '__main__':
    main()
