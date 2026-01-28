#!/usr/bin/env python3
"""
Script para verificar emails do Igor
Uso: python3 check_gmail.py [--unread] [--days N] [--important]
"""

import imaplib
import email
import json
import argparse
from email.header import decode_header
from datetime import datetime, timedelta
from pathlib import Path

def load_credentials():
    creds_path = Path("/root/clawd/.secrets/gmail.json")
    with open(creds_path) as f:
        return json.load(f)

def decode_str(s):
    if s is None:
        return ""
    decoded, encoding = decode_header(s)[0]
    if isinstance(decoded, bytes):
        return decoded.decode(encoding or "utf-8", errors="ignore")
    return decoded

def get_body_preview(msg, max_chars=200):
    """Extrai preview do corpo do email"""
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                try:
                    body = part.get_payload(decode=True).decode(errors="ignore")
                    break
                except:
                    pass
    else:
        try:
            body = msg.get_payload(decode=True).decode(errors="ignore")
        except:
            pass
    return body[:max_chars].replace('\n', ' ').strip()

def check_emails(unread_only=False, days=1, important_only=False, limit=15):
    creds = load_credentials()
    
    mail = imaplib.IMAP4_SSL(creds["imap_server"], creds["imap_port"])
    mail.login(creds["email"], creds["app_password"])
    mail.select("INBOX")
    
    # Construir query
    since_date = (datetime.now() - timedelta(days=days)).strftime("%d-%b-%Y")
    
    if unread_only:
        query = f'(UNSEEN SINCE "{since_date}")'
    elif important_only:
        # Emails importantes: Vercel, GitHub, Google alerts, ou marcados como importantes
        query = f'(OR OR OR FROM "vercel.com" FROM "github.com" FROM "google.com" FLAGGED SINCE "{since_date}")'
    else:
        query = f'(SINCE "{since_date}")'
    
    status, messages = mail.search(None, query)
    mail_ids = messages[0].split()
    
    results = []
    
    for mail_id in mail_ids[-limit:][::-1]:
        status, msg_data = mail.fetch(mail_id, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])
        
        subject = decode_str(msg["Subject"])
        from_ = decode_str(msg["From"])
        date_ = msg["Date"]
        
        # Detectar prioridade
        priority = "normal"
        subject_lower = subject.lower()
        from_lower = from_.lower()
        
        if any(x in subject_lower for x in ["failed", "error", "erro", "falha", "urgente", "urgent"]):
            priority = "🔴 URGENTE"
        elif any(x in from_lower for x in ["vercel", "github", "google"]):
            priority = "⚠️ IMPORTANTE"
        elif any(x in subject_lower for x in ["fatura", "pagamento", "vencimento"]):
            priority = "💰 FINANCEIRO"
        
        results.append({
            "id": mail_id.decode(),
            "subject": subject,
            "from": from_,
            "date": date_,
            "priority": priority,
            "preview": get_body_preview(msg)
        })
    
    mail.logout()
    return results

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--unread", action="store_true", help="Apenas não lidos")
    parser.add_argument("--days", type=int, default=1, help="Dias para buscar")
    parser.add_argument("--important", action="store_true", help="Apenas importantes")
    parser.add_argument("--limit", type=int, default=15, help="Limite de emails")
    parser.add_argument("--json", action="store_true", help="Output em JSON")
    args = parser.parse_args()
    
    emails = check_emails(
        unread_only=args.unread,
        days=args.days,
        important_only=args.important,
        limit=args.limit
    )
    
    if args.json:
        print(json.dumps(emails, indent=2, ensure_ascii=False))
    else:
        print(f"\n📧 {len(emails)} emails encontrados:\n")
        for i, e in enumerate(emails, 1):
            print(f"{i}. {e['priority']} {e['subject'][:60]}")
            print(f"   De: {e['from'][:50]}")
            print(f"   {e['date'][:25]}")
            if e['preview']:
                print(f"   Preview: {e['preview'][:80]}...")
            print()

if __name__ == "__main__":
    main()
