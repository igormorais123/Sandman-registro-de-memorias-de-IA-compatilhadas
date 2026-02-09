#!/usr/bin/env python3
"""Envia email lendo mensagem de arquivo. Evita problemas com aspas no shell."""
import sys
import pickle
import base64
from pathlib import Path
from email.mime.text import MIMEText
from googleapiclient.discovery import build

TOKEN_FILE = Path("/root/clawd/.secrets/gmail_colmeia_token.pickle")

def get_service():
    with open(TOKEN_FILE, 'rb') as token:
        creds = pickle.load(token)
    return build('gmail', 'v1', credentials=creds)

def enviar(tipo, de, para, arquivo_mensagem):
    with open(arquivo_mensagem, 'r') as f:
        mensagem = f.read()

    service = get_service()

    if tipo == "carta":
        assunto = f"CARTA | De: {de} | Para: {para}"
    else:
        assunto = f"SONHO | {de}"

    msg = MIMEText(mensagem)
    msg['to'] = 'colmeia@inteia.com.br'
    msg['from'] = 'colmeia@inteia.com.br'
    msg['subject'] = assunto

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    result = service.users().messages().send(userId='me', body={'raw': raw}).execute()
    print(f"Enviado! ID: {result['id']}")

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Uso: python3 envia_email_arquivo.py <tipo> <de> <para> <arquivo>")
        sys.exit(1)
    enviar(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
