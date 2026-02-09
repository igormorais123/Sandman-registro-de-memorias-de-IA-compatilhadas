#!/usr/bin/env python3
"""
🔐 Cofre de Senhas do Igor
Criptografia AES-256 com senha mestre
"""
import json
import base64
import hashlib
import getpass
import sys
import os
from pathlib import Path
from datetime import datetime

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
except ImportError:
    print("Instalando cryptography...")
    os.system("pip install cryptography -q")
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

VAULT_DIR = Path(__file__).parent
VAULT_FILE = VAULT_DIR / "secrets.vault"
SALT_FILE = VAULT_DIR / ".salt"

def get_salt():
    """Gera ou recupera o salt único do cofre."""
    if SALT_FILE.exists():
        return SALT_FILE.read_bytes()
    salt = os.urandom(16)
    SALT_FILE.write_bytes(salt)
    os.chmod(SALT_FILE, 0o600)
    return salt

def derive_key(master_password: str) -> bytes:
    """Deriva chave AES-256 da senha mestre."""
    salt = get_salt()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
    return key

def encrypt(data: dict, master_password: str) -> bytes:
    """Criptografa dados com a senha mestre."""
    key = derive_key(master_password)
    f = Fernet(key)
    return f.encrypt(json.dumps(data, ensure_ascii=False).encode())

def decrypt(encrypted_data: bytes, master_password: str) -> dict:
    """Descriptografa dados com a senha mestre."""
    key = derive_key(master_password)
    f = Fernet(key)
    return json.loads(f.decrypt(encrypted_data).decode())

def load_vault(master_password: str) -> dict:
    """Carrega o cofre."""
    if not VAULT_FILE.exists():
        return {"entries": {}, "created": datetime.now().isoformat()}
    try:
        encrypted = VAULT_FILE.read_bytes()
        return decrypt(encrypted, master_password)
    except Exception:
        raise ValueError("❌ Senha mestre incorreta!")

def save_vault(data: dict, master_password: str):
    """Salva o cofre."""
    encrypted = encrypt(data, master_password)
    VAULT_FILE.write_bytes(encrypted)
    os.chmod(VAULT_FILE, 0o600)

def add_entry(vault: dict, name: str, username: str, password: str, url: str = "", notes: str = ""):
    """Adiciona uma entrada."""
    vault["entries"][name] = {
        "username": username,
        "password": password,
        "url": url,
        "notes": notes,
        "created": datetime.now().isoformat(),
        "updated": datetime.now().isoformat()
    }

def list_entries(vault: dict):
    """Lista todas as entradas (sem mostrar senhas)."""
    if not vault["entries"]:
        print("📭 Cofre vazio")
        return
    print("\n🔐 Entradas no cofre:\n")
    for i, (name, entry) in enumerate(vault["entries"].items(), 1):
        print(f"  {i}. {name}")
        print(f"     👤 {entry['username']}")
        if entry.get('url'):
            print(f"     🔗 {entry['url']}")
        print()

def get_entry(vault: dict, name: str) -> dict:
    """Recupera uma entrada."""
    if name not in vault["entries"]:
        raise KeyError(f"❌ '{name}' não encontrado")
    return vault["entries"][name]

def delete_entry(vault: dict, name: str):
    """Remove uma entrada."""
    if name in vault["entries"]:
        del vault["entries"][name]

def interactive():
    """Modo interativo."""
    print("\n🔐 COFRE DE SENHAS DO IGOR")
    print("=" * 40)
    
    master = getpass.getpass("Senha mestre: ")
    
    try:
        vault = load_vault(master)
        print("✅ Cofre aberto!\n")
    except ValueError as e:
        print(e)
        return
    except Exception:
        # Cofre novo
        print("📦 Criando novo cofre...")
        vault = {"entries": {}, "created": datetime.now().isoformat()}
    
    while True:
        print("\n[1] Listar  [2] Adicionar  [3] Ver  [4] Deletar  [5] Sair")
        choice = input("> ").strip()
        
        if choice == "1":
            list_entries(vault)
        
        elif choice == "2":
            name = input("Nome do serviço: ").strip()
            username = input("Usuário/Email: ").strip()
            password = getpass.getpass("Senha: ")
            url = input("URL (opcional): ").strip()
            notes = input("Notas (opcional): ").strip()
            add_entry(vault, name, username, password, url, notes)
            save_vault(vault, master)
            print(f"✅ '{name}' adicionado!")
        
        elif choice == "3":
            name = input("Nome do serviço: ").strip()
            try:
                entry = get_entry(vault, name)
                print(f"\n📋 {name}")
                print(f"   👤 Usuário: {entry['username']}")
                print(f"   🔑 Senha: {entry['password']}")
                if entry.get('url'):
                    print(f"   🔗 URL: {entry['url']}")
                if entry.get('notes'):
                    print(f"   📝 Notas: {entry['notes']}")
            except KeyError as e:
                print(e)
        
        elif choice == "4":
            name = input("Nome do serviço: ").strip()
            confirm = input(f"Deletar '{name}'? (s/n): ").strip().lower()
            if confirm == "s":
                delete_entry(vault, name)
                save_vault(vault, master)
                print(f"🗑️ '{name}' deletado!")
        
        elif choice == "5":
            print("👋 Cofre fechado!")
            break

# API para uso programático (pelo Clawd)
class Vault:
    def __init__(self, master_password: str):
        self.master = master_password
        self.data = load_vault(master_password)
    
    def get(self, name: str) -> dict:
        return get_entry(self.data, name)
    
    def add(self, name: str, username: str, password: str, url: str = "", notes: str = ""):
        add_entry(self.data, name, username, password, url, notes)
        save_vault(self.data, self.master)
    
    def delete(self, name: str):
        delete_entry(self.data, name)
        save_vault(self.data, self.master)
    
    def list(self) -> list:
        return list(self.data["entries"].keys())

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "list" and len(sys.argv) == 3:
            master = sys.argv[2]
            vault = load_vault(master)
            for name in vault["entries"]:
                print(name)
        elif cmd == "get" and len(sys.argv) == 4:
            master, name = sys.argv[2], sys.argv[3]
            vault = load_vault(master)
            entry = vault["entries"].get(name, {})
            print(json.dumps(entry))
    else:
        interactive()
