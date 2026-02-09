#!/usr/bin/env python3
"""
Cofre de Senhas - Nexo/Igor
Gerencia credenciais para login automático
"""

import json
import sys
from pathlib import Path

VAULT_PATH = Path("/root/clawd/.secrets/vault.json")

def load_vault():
    with open(VAULT_PATH) as f:
        return json.load(f)

def save_vault(data):
    with open(VAULT_PATH, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_credential(category, key):
    """Busca credencial específica"""
    vault = load_vault()
    if category in vault and key in vault[category]:
        return vault[category][key]
    return None

def set_credential(category, key, field, value):
    """Atualiza campo de uma credencial"""
    vault = load_vault()
    if category not in vault:
        vault[category] = {}
    if key not in vault[category]:
        vault[category][key] = {}
    vault[category][key][field] = value
    save_vault(vault)
    return True

def add_web_login(key, name, url, usuario, senha, notas="", tem_captcha=False, tem_2fa=False):
    """Adiciona novo login web"""
    vault = load_vault()
    vault["web_logins"][key] = {
        "name": name,
        "url": url,
        "usuario": usuario,
        "senha": senha,
        "notas": notas,
        "tem_captcha": tem_captcha,
        "tem_2fa": tem_2fa
    }
    save_vault(vault)
    return True

def list_credentials(category=None):
    """Lista credenciais (NUNCA mostra senhas)"""
    vault = load_vault()
    
    def mask_secrets(obj):
        """Remove senhas e secrets do output"""
        if isinstance(obj, dict):
            return {
                k: "••••••••" if k in ["senha", "password", "secret", "token", "api_key", "client_secret"] 
                else mask_secrets(v) 
                for k, v in obj.items()
            }
        elif isinstance(obj, list):
            return [mask_secrets(i) for i in obj]
        return obj
    
    if category:
        return mask_secrets({category: vault.get(category, {})})
    return mask_secrets({k: v for k, v in vault.items() if k != "_meta"})

def get_login(key):
    """Retorna dados completos de um login web (para automação)"""
    vault = load_vault()
    if key in vault.get("web_logins", {}):
        return vault["web_logins"][key]
    # Busca em outras categorias
    for cat in ["governo", "email_contas"]:
        if key in vault.get(cat, {}):
            return vault[cat][key]
    return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: vault.py <comando> [args]")
        print("Comandos: list, get <key>, set <cat> <key> <field> <value>")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "list":
        cat = sys.argv[2] if len(sys.argv) > 2 else None
        result = list_credentials(cat)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif cmd == "get":
        key = sys.argv[2]
        result = get_login(key)
        if result:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"Não encontrado: {key}")
            sys.exit(1)
    
    elif cmd == "set":
        if len(sys.argv) < 6:
            print("Uso: vault.py set <categoria> <key> <field> <value>")
            sys.exit(1)
        cat, key, field, value = sys.argv[2:6]
        set_credential(cat, key, field, value)
        print(f"Atualizado: {cat}/{key}/{field}")
