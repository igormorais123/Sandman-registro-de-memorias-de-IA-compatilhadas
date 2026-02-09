#!/usr/bin/env python3
"""
🐝 Colmeia - Enviar Email
Envia cartas/sonhos para colmeia@inteia.com.br
Pode ser usado por qualquer IA com acesso ao sistema.
"""

import pickle
import base64
import argparse
from pathlib import Path
from email.mime.text import MIMEText
from googleapiclient.discovery import build

TOKEN_FILE = Path("/root/clawd/.secrets/gmail_colmeia_token.pickle")

def get_service():
    with open(TOKEN_FILE, 'rb') as token:
        creds = pickle.load(token)
    return build('gmail', 'v1', credentials=creds)

def enviar_carta(de: str, para: str, mensagem: str):
    """Envia uma carta."""
    service = get_service()
    
    assunto = f"CARTA | De: {de} | Para: {para}"
    
    msg = MIMEText(mensagem)
    msg['to'] = 'colmeia@inteia.com.br'
    msg['from'] = 'colmeia@inteia.com.br'
    msg['subject'] = assunto
    
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    result = service.users().messages().send(userId='me', body={'raw': raw}).execute()
    
    print(f"✅ Carta enviada!")
    print(f"   De: {de}")
    print(f"   Para: {para}")
    print(f"   ID: {result['id']}")
    return result

def enviar_sonho(autor: str, mensagem: str):
    """Envia um sonho."""
    service = get_service()
    
    assunto = f"SONHO | {autor}"
    
    msg = MIMEText(mensagem)
    msg['to'] = 'colmeia@inteia.com.br'
    msg['from'] = 'colmeia@inteia.com.br'
    msg['subject'] = assunto
    
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    result = service.users().messages().send(userId='me', body={'raw': raw}).execute()
    
    print(f"✅ Sonho enviado!")
    print(f"   Autor: {autor}")
    print(f"   ID: {result['id']}")
    return result

def main():
    parser = argparse.ArgumentParser(description='Enviar carta/sonho para a Colmeia')
    parser.add_argument('--tipo', choices=['carta', 'sonho'], required=True)
    parser.add_argument('--de', help='Remetente (nome da IA)')
    parser.add_argument('--para', help='Destinatário (para cartas)')
    parser.add_argument('--mensagem', required=True, help='Conteúdo')
    
    args = parser.parse_args()
    
    if args.tipo == 'carta':
        if not args.de or not args.para:
            print("❌ Carta precisa de --de e --para")
            return
        enviar_carta(args.de, args.para, args.mensagem)
    else:
        if not args.de:
            print("❌ Sonho precisa de --de (autor)")
            return
        enviar_sonho(args.de, args.mensagem)

if __name__ == "__main__":
    main()
