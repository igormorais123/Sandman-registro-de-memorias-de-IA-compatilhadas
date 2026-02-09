#!/usr/bin/env python3
"""
Smart Credit Monitor - Monitora créditos e muda modelo automaticamente
Roda via cron ou pode ser chamado manualmente
"""

import json
import os
import sys
import time
import subprocess
from datetime import datetime
from pathlib import Path

# Configurações
CONFIG_PATH = Path("/root/.clawdbot/clawdbot.json")
STATE_PATH = Path("/root/clawd/scripts/credit-monitor/state.json")
LOG_PATH = Path("/root/clawd/logs/credit-monitor.log")

# Modelos em ordem de prioridade (melhor → pior)
FALLBACK_ORDER = [
    "anthropic/claude-sonnet-4",    # 1. Claude (premium)
    "openai/gpt-4o",                # 2. OpenAI (premium)
    "google/gemini-2.5-flash",      # 3. Gemini (médio)
    "opencode/gpt-5-nano",          # 4. Gratuito
    "opencode/glm-4.7-free",        # 5. Gratuito
    "opencode/kimi-k2.5-free"       # 6. Gratuito
]

PREMIUM_MODELS = ["anthropic/claude-opus-4-5", "anthropic/claude-sonnet-4", "openai/gpt-4o"]
FREE_MODELS = ["opencode/gpt-5-nano", "opencode/glm-4.7-free", "opencode/kimi-k2.5-free"]
CHEAP_MODELS = ["google/gemini-2.5-flash"]

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_PATH, "a") as f:
        f.write(line + "\n")

def load_state():
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text())
    return {"mode": "normal", "switched_at": None, "last_check": None}

def save_state(state):
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2))

def test_anthropic():
    """Testa se a API da Anthropic está funcionando"""
    import urllib.request
    import urllib.error
    
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    
    if not api_key:
        # Tentar ler da config
        try:
            config = json.loads(CONFIG_PATH.read_text())
            api_key = config.get("env", {}).get("vars", {}).get("ANTHROPIC_API_KEY", "")
        except:
            pass
    
    if not api_key:
        log("WARN: Anthropic API key não encontrada")
        return True  # Assume OK se não tem key
    
    # Requisição mínima de teste
    data = json.dumps({
        "model": "claude-3-5-haiku-20241022",
        "max_tokens": 1,
        "messages": [{"role": "user", "content": "1"}]
    }).encode()
    
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=data,
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
    )
    
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            log(f"Anthropic OK: HTTP {resp.status}")
            return True
    except urllib.error.HTTPError as e:
        log(f"Anthropic ERROR: HTTP {e.code}")
        body = e.read().decode()
        
        # Verificar se é erro de créditos
        if e.code in [402, 429] or "credit" in body.lower() or "quota" in body.lower() or "billing" in body.lower():
            log("Detectado: Problema de créditos/quota")
            return False
        
        # Outros erros (ex: rate limit temporário) - assume OK
        return True
    except Exception as e:
        log(f"Anthropic EXCEPTION: {e}")
        return True  # Erro de rede, assume OK

def get_current_config():
    """Lê a config atual do Clawdbot"""
    return json.loads(CONFIG_PATH.read_text())

def switch_to_fallback():
    """Muda para modelos gratuitos quando Claude falhar"""
    log("Ativando modo fallback...")
    
    config = get_current_config()
    
    # Mudar fallbacks: pular Anthropic, começar com GPT-5.2 Codex
    config["agents"]["defaults"]["model"]["fallbacks"] = [
        "opencode/gpt-5.2-codex",       # Premium OpenAI
        "google/gemini-2.5-flash",      # Médio
        "opencode/gpt-5-nano",          # Gratuitos
        "opencode/glm-4.7-free",
        "opencode/kimi-k2.5-free"
    ]
    
    # Salvar config
    CONFIG_PATH.write_text(json.dumps(config, indent=2))
    
    # Reiniciar gateway
    try:
        subprocess.run(["pkill", "-USR1", "-f", "clawdbot"], timeout=5)
    except:
        pass
    
    log("Fallback ativado!")
    
    state = load_state()
    state["mode"] = "fallback"
    state["switched_at"] = datetime.now().isoformat()
    save_state(state)

def restore_premium():
    """Restaura modelos premium"""
    log("Restaurando modelos premium...")
    
    config = get_current_config()
    
    # Restaurar ordem: Opus 4.5 → GPT-5.2 Codex → Gemini → Gratuitos
    config["agents"]["defaults"]["model"]["fallbacks"] = [
        "anthropic/claude-opus-4-5",
        "opencode/gpt-5.2-codex",
        "google/gemini-2.5-flash",
        "opencode/gpt-5-nano",
        "opencode/glm-4.7-free",
        "opencode/kimi-k2.5-free"
    ]
    
    # Remover override de modelo se existir
    if "name" in config["agents"]["defaults"]["model"]:
        del config["agents"]["defaults"]["model"]["name"]
    
    CONFIG_PATH.write_text(json.dumps(config, indent=2))
    
    try:
        subprocess.run(["pkill", "-USR1", "-f", "clawdbot"], timeout=5)
    except:
        pass
    
    log("Premium restaurado!")
    
    state = load_state()
    state["mode"] = "normal"
    state["switched_at"] = None
    save_state(state)

def send_alert(message):
    """Envia alerta via WhatsApp"""
    log(f"Alerta: {message}")
    try:
        subprocess.run(
            ["clawdbot", "send", "--channel", "whatsapp", "--to", "+5561981157120", message],
            timeout=30,
            capture_output=True
        )
    except Exception as e:
        log(f"Erro ao enviar alerta: {e}")

def main():
    log("=== Smart Credit Monitor ===")
    
    state = load_state()
    current_mode = state.get("mode", "normal")
    
    # Testar Anthropic
    anthropic_ok = test_anthropic()
    
    if anthropic_ok:
        if current_mode == "fallback":
            log("Anthropic voltou! Restaurando premium...")
            restore_premium()
            send_alert("✅ Créditos Anthropic OK! Voltei pro Claude.")
        else:
            log("Status: Normal (Anthropic OK)")
    else:
        if current_mode != "fallback":
            log("Anthropic com problema! Ativando fallback...")
            switch_to_fallback()
            send_alert("⚠️ Créditos Anthropic esgotados! Mudei pra modelo gratuito automaticamente.")
        else:
            log("Status: Fallback (aguardando créditos)")
    
    state["last_check"] = datetime.now().isoformat()
    save_state(state)
    
    log("=== Check completo ===")

if __name__ == "__main__":
    main()
