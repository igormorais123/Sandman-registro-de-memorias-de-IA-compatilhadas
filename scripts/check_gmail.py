#!/usr/bin/env python3
"""check_gmail.py - Verificação de emails Gmail
Status: STUB - aguardando configuração de credenciais OAuth
Uso: python3 check_gmail.py --unread --days 1
"""
import sys
import json
from datetime import datetime

def main():
    print(json.dumps({
        'status': 'stub',
        'message': 'Gmail integration not yet configured.',
        'timestamp': datetime.now().isoformat(),
        'unread': [],
        'setup_needed': 'Configure OAuth credentials in /root/.openclaw/credentials/gmail.json'
    }, indent=2))
    sys.exit(0)

if __name__ == '__main__':
    main()
