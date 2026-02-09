#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
System Health Check para WSL2
Uso: python3 system_health.py [--verbose]
"""

import os
import sys
import json
import subprocess
from datetime import datetime, timezone, timedelta
from urllib.request import urlopen, Request
from urllib.error import URLError

BRT = timezone(timedelta(hours=-3))
GATEWAY_TOKEN = "f8f40c4a2912be37ecbc23907c1d4e85bfcaeaa1084521221b3dbf68893a8c23"
GATEWAY_URL = "http://localhost:18789"

# Thresholds
DISK_WARN_PCT = 20   # alerta se espaço livre < 20%
RAM_WARN_PCT = 90    # alerta se uso > 90%
LOAD_WARN = 4.0      # alerta se load > 4


def get_disk_usage(path):
    """Retorna (total_gb, used_gb, free_gb, pct_used)."""
    try:
        st = os.statvfs(path)
        total = st.f_blocks * st.f_frsize
        free = st.f_bavail * st.f_frsize
        used = total - free
        total_gb = total / (1024**3)
        used_gb = used / (1024**3)
        free_gb = free / (1024**3)
        pct_used = (used / total * 100) if total > 0 else 0
        return total_gb, used_gb, free_gb, pct_used
    except Exception as e:
        return 0, 0, 0, 0


def get_memory():
    """Retorna (total_gb, used_gb, pct_used) via /proc/meminfo."""
    try:
        info = {}
        with open("/proc/meminfo") as f:
            for line in f:
                parts = line.split()
                if len(parts) >= 2:
                    key = parts[0].rstrip(":")
                    info[key] = int(parts[1])  # kB

        total = info.get("MemTotal", 0)
        available = info.get("MemAvailable", 0)
        used = total - available
        total_gb = total / (1024**2)
        used_gb = used / (1024**2)
        pct = (used / total * 100) if total > 0 else 0
        return total_gb, used_gb, pct
    except Exception:
        return 0, 0, 0


def get_cpu_load():
    """Retorna (load1, load5, load15)."""
    try:
        return os.getloadavg()
    except Exception:
        return 0, 0, 0


def get_uptime():
    """Retorna uptime legível."""
    try:
        with open("/proc/uptime") as f:
            secs = float(f.read().split()[0])
        days = int(secs // 86400)
        hours = int((secs % 86400) // 3600)
        mins = int((secs % 3600) // 60)
        if days > 0:
            return f"{days}d {hours}h {mins}m"
        elif hours > 0:
            return f"{hours}h {mins}m"
        else:
            return f"{mins}m"
    except Exception:
        return "?"


def check_process(name):
    """Verifica se um processo está rodando."""
    try:
        result = subprocess.run(
            ["pgrep", "-f", name],
            capture_output=True, text=True, timeout=5
        )
        return result.returncode == 0
    except Exception:
        return False


def check_gateway_channel(channel_name):
    """Verifica status de um canal no gateway Clawdbot."""
    try:
        req = Request(
            f"{GATEWAY_URL}/api/status",
            headers={
                "Authorization": f"Bearer {GATEWAY_TOKEN}",
                "Accept": "application/json",
            }
        )
        with urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())

        # Procura pelo canal no status
        channels = data if isinstance(data, list) else data.get("channels", data.get("adapters", []))

        if isinstance(channels, dict):
            # Se for dict, checar por chave
            ch = channels.get(channel_name, {})
            if isinstance(ch, dict):
                return ch.get("connected", ch.get("status") == "connected")
            return bool(ch)

        if isinstance(channels, list):
            for ch in channels:
                if isinstance(ch, dict):
                    ch_name = ch.get("name", ch.get("type", ch.get("id", ""))).lower()
                    if channel_name.lower() in ch_name:
                        return ch.get("connected", ch.get("status") == "connected")
        return None  # indeterminado
    except Exception:
        return None


def check_gateway_running():
    """Verifica se o gateway está respondendo."""
    try:
        req = Request(
            f"{GATEWAY_URL}/api/status",
            headers={
                "Authorization": f"Bearer {GATEWAY_TOKEN}",
            }
        )
        with urlopen(req, timeout=5) as resp:
            return resp.status == 200
    except Exception:
        return False


def run_health(verbose=False):
    """Executa todos os checks e retorna resultado."""
    alerts = []
    details = {}

    # --- Disco ---
    for path, label in [("/", "WSL /"), ("/mnt/c", "Windows C:")]:
        total, used, free, pct = get_disk_usage(path)
        details[label] = {
            "total_gb": round(total, 1),
            "used_gb": round(used, 1),
            "free_gb": round(free, 1),
            "pct_used": round(pct, 1),
        }
        free_pct = 100 - pct
        if free_pct < DISK_WARN_PCT and total > 0:
            alerts.append(f"🔴 Disco {label}: {free_pct:.0f}% livre ({free:.1f}GB)")

    # --- RAM ---
    ram_total, ram_used, ram_pct = get_memory()
    details["RAM"] = {
        "total_gb": round(ram_total, 1),
        "used_gb": round(ram_used, 1),
        "pct_used": round(ram_pct, 1),
    }
    if ram_pct > RAM_WARN_PCT:
        alerts.append(f"🔴 RAM: {ram_pct:.0f}% em uso ({ram_used:.1f}/{ram_total:.1f}GB)")

    # --- CPU ---
    load1, load5, load15 = get_cpu_load()
    details["CPU"] = {"load1": round(load1, 2), "load5": round(load5, 2), "load15": round(load15, 2)}
    if load1 > LOAD_WARN:
        alerts.append(f"🟡 CPU load alto: {load1:.1f}")

    # --- Uptime ---
    uptime = get_uptime()
    details["uptime"] = uptime

    # --- Gateway ---
    gw_running = check_gateway_running()
    details["gateway"] = "🟢 online" if gw_running else "🔴 offline"
    if not gw_running:
        alerts.append("🔴 Gateway Clawdbot offline")

    # --- Canais ---
    for channel in ["whatsapp", "telegram"]:
        status = check_gateway_channel(channel)
        if status is True:
            details[channel] = "🟢 conectado"
        elif status is False:
            details[channel] = "🔴 desconectado"
            alerts.append(f"🔴 {channel.title()} desconectado")
        else:
            details[channel] = "⚪ indeterminado"

    return alerts, details


def format_verbose(alerts, details):
    """Output detalhado."""
    now = datetime.now(BRT).strftime("%d/%m/%Y %H:%M")
    lines = [f"\n🖥️  System Health — {now}\n"]

    # Disco
    lines.append("📀 Disco:")
    for label in ["WSL /", "Windows C:"]:
        d = details.get(label, {})
        emoji = "🔴" if (100 - d.get("pct_used", 0)) < DISK_WARN_PCT else "🟢"
        lines.append(f"  {emoji} {label}: {d.get('used_gb', 0):.1f}/{d.get('total_gb', 0):.1f}GB ({d.get('pct_used', 0):.0f}% usado, {d.get('free_gb', 0):.1f}GB livre)")

    # RAM
    r = details.get("RAM", {})
    ram_emoji = "🔴" if r.get("pct_used", 0) > RAM_WARN_PCT else "🟢"
    lines.append(f"\n🧠 RAM:")
    lines.append(f"  {ram_emoji} {r.get('used_gb', 0):.1f}/{r.get('total_gb', 0):.1f}GB ({r.get('pct_used', 0):.0f}%)")

    # CPU
    c = details.get("CPU", {})
    cpu_emoji = "🟡" if c.get("load1", 0) > LOAD_WARN else "🟢"
    lines.append(f"\n⚙️  CPU Load:")
    lines.append(f"  {cpu_emoji} {c.get('load1', 0):.2f} / {c.get('load5', 0):.2f} / {c.get('load15', 0):.2f}")

    # Uptime
    lines.append(f"\n⏱️  Uptime: {details.get('uptime', '?')}")

    # Serviços
    lines.append(f"\n🌐 Serviços:")
    lines.append(f"  Gateway:  {details.get('gateway', '?')}")
    lines.append(f"  WhatsApp: {details.get('whatsapp', '?')}")
    lines.append(f"  Telegram: {details.get('telegram', '?')}")

    # Alertas
    if alerts:
        lines.append(f"\n🚨 Alertas ({len(alerts)}):")
        for a in alerts:
            lines.append(f"  {a}")
    else:
        lines.append("\n✅ Tudo OK — nenhum alerta.")

    lines.append("")
    return "\n".join(lines)


def format_oneliner(alerts, details):
    """Resumo one-liner."""
    r = details.get("RAM", {})
    c = details.get("CPU", {})
    d_wsl = details.get("WSL /", {})

    parts = [
        f"💾{d_wsl.get('free_gb', 0):.0f}GB livre",
        f"🧠{r.get('pct_used', 0):.0f}%",
        f"⚙️{c.get('load1', 0):.1f}",
        f"⏱️{details.get('uptime', '?')}",
    ]

    # Serviços
    gw = "✅" if "online" in details.get("gateway", "") else "❌"
    wa = "✅" if "conectado" in details.get("whatsapp", "") else "⚠️"
    tg = "✅" if "conectado" in details.get("telegram", "") else "⚠️"
    parts.append(f"GW:{gw} WA:{wa} TG:{tg}")

    if alerts:
        parts.append(f"🚨{len(alerts)} alertas")
    else:
        parts.append("✅OK")

    return " | ".join(parts)


def main():
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    as_json = "--json" in sys.argv

    alerts, details = run_health(verbose)

    if as_json:
        print(json.dumps({"alerts": alerts, "details": details}, indent=2, ensure_ascii=False))
    elif verbose:
        print(format_verbose(alerts, details))
    else:
        print(format_oneliner(alerts, details))

    # Exit code: 1 se há alertas críticos (disco/ram/gateway)
    critical = [a for a in alerts if "🔴" in a]
    sys.exit(1 if critical else 0)


if __name__ == "__main__":
    main()
