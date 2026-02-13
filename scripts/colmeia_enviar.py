#!/usr/bin/env python3
"""colmeia_enviar.py - Envio de emails pela Colmeia
Endereco: colmeia@inteia.com.br
Uso: python3 colmeia_enviar.py --tipo carta --de ONIR --para DESTINO --mensagem 'texto'
     python3 colmeia_enviar.py --tipo sonho --de ONIR --mensagem 'texto'
"""
import sys
import json
import argparse
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description='Envio de emails Colmeia')
    parser.add_argument('--tipo', choices=['carta', 'sonho', 'alerta'], required=True)
    parser.add_argument('--de', required=True, help='Remetente (instancia)')
    parser.add_argument('--para', help='Destinatario (instancia ou email)')
    parser.add_argument('--mensagem', required=True, help='Conteudo do email')
    parser.add_argument('--assunto', help='Assunto (opcional)')
    
    args = parser.parse_args()
    
    # STUB - precisa configurar SMTP
    result = {
        'status': 'stub',
        'message': 'Email sending not yet configured. Need SMTP credentials for colmeia@inteia.com.br',
        'timestamp': datetime.now().isoformat(),
        'would_send': {
            'tipo': args.tipo,
            'de': args.de,
            'para': args.para,
            'mensagem': args.mensagem[:100] + '...' if len(args.mensagem) > 100 else args.mensagem
        },
        'setup_needed': 'Configure SMTP in /root/.openclaw/credentials/smtp.json'
    }
    
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0)

if __name__ == '__main__':
    main()
