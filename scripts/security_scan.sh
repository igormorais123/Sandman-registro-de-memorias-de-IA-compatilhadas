#!/bin/bash
# =============================================================================
# security_scan.sh — Monitoramento de segurança contínuo
# =============================================================================
# Uso:
#   security_scan.sh              → Scan completo (portas + Shodan + senhas)
#   security_scan.sh --ports      → Só portas abertas
#   security_scan.sh --shodan     → Só Shodan
#   security_scan.sh --quick      → Scan rápido (portas expostas)
#   security_scan.sh --json       → Output JSON para automação
# =============================================================================

SECRETS_DIR="/root/clawd/.secrets"
REPORT_DIR="/root/clawd/memory/security"
mkdir -p "$REPORT_DIR"

NOW=$(date '+%Y-%m-%d %H:%M:%S')
DATE=$(date '+%Y-%m-%d')
REPORT="$REPORT_DIR/scan_$DATE.log"
PUBLIC_IP=$(curl -s --max-time 5 ifconfig.me 2>/dev/null)
ALERTS=""
JSON_MODE=false

log() { echo "[$NOW] $1" | tee -a "$REPORT"; }
alert() { ALERTS="$ALERTS\n🔴 $1"; log "ALERT: $1"; }
warn() { ALERTS="$ALERTS\n🟡 $1"; log "WARN: $1"; }
ok() { log "OK: $1"; }

# ----- PORTAS EXPOSTAS (não-localhost) -----
check_ports() {
    log "=== SCAN DE PORTAS ==="
    
    # Portas TCP escutando em todas interfaces (0.0.0.0 ou *)
    # Ignorar: localhost, DNS interno (systemd-resolved/docker), loopback
    EXPOSED=$(ss -tlnp 2>/dev/null | grep -v "127.0.0.\|::1\|\[::1\]" | grep "LISTEN" | grep -v "Local Address" | grep -v "10.255.255.254:53")
    
    if [ -n "$EXPOSED" ]; then
        while IFS= read -r line; do
            PORT=$(echo "$line" | awk '{print $4}' | rev | cut -d: -f1 | rev)
            PROC=$(echo "$line" | awk '{print $6}')
            
            # Portas conhecidas como perigosas
            case "$PORT" in
                5432) alert "PostgreSQL ($PORT) exposto externamente! $PROC" ;;
                3306) alert "MySQL ($PORT) exposto externamente! $PROC" ;;
                6379) alert "Redis ($PORT) exposto externamente! $PROC" ;;
                27017) alert "MongoDB ($PORT) exposto externamente! $PROC" ;;
                22) warn "SSH ($PORT) aberto — verificar se intencional" ;;
                80|443) warn "HTTP/S ($PORT) aberto — $PROC" ;;
                *) warn "Porta $PORT exposta externamente — $PROC" ;;
            esac
        done <<< "$EXPOSED"
    else
        ok "Nenhuma porta exposta externamente"
    fi
    
    # Docker containers com ports em 0.0.0.0
    DOCKER_EXPOSED=$(docker ps --format '{{.Ports}} {{.Names}}' 2>/dev/null | grep "0.0.0.0")
    if [ -n "$DOCKER_EXPOSED" ]; then
        alert "Docker containers com portas expostas: $DOCKER_EXPOSED"
    else
        ok "Docker containers seguros (localhost only)"
    fi
}

# ----- SHODAN -----
check_shodan() {
    log "=== SCAN SHODAN ==="
    
    if [ -z "$PUBLIC_IP" ]; then
        warn "Não consegui determinar IP público"
        return
    fi
    
    log "IP público: $PUBLIC_IP"
    
    # Buscar no Shodan via web (sem API key)
    SHODAN_RESULT=$(curl -s --max-time 15 "https://internetdb.shodan.io/$PUBLIC_IP" 2>/dev/null)
    
    if echo "$SHODAN_RESULT" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    ports = d.get('ports', [])
    vulns = d.get('vulns', [])
    cpes = d.get('cpes', [])
    hostnames = d.get('hostnames', [])
    
    if ports:
        print(f'PORTS_FOUND:{len(ports)}')
        for p in ports:
            print(f'  PORT:{p}')
    if vulns:
        print(f'VULNS_FOUND:{len(vulns)}')
        for v in vulns:
            print(f'  VULN:{v}')
    if cpes:
        print(f'CPES:{len(cpes)}')
        for c in cpes:
            print(f'  CPE:{c}')
    if hostnames:
        print(f'HOSTNAMES:{\" \".join(hostnames)}')
    if not ports and not vulns:
        print('CLEAN')
except:
    print('PARSE_ERROR')
" 2>/dev/null | tee -a "$REPORT" | grep -q "PORTS_FOUND\|VULNS_FOUND"; then
        SHODAN_PORTS=$(echo "$SHODAN_RESULT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(','.join(str(p) for p in d.get('ports',[])))" 2>/dev/null)
        alert "Shodan encontrou portas abertas no seu IP: $SHODAN_PORTS"
        
        SHODAN_VULNS=$(echo "$SHODAN_RESULT" | python3 -c "import json,sys; d=json.load(sys.stdin); v=d.get('vulns',[]); print(','.join(v)) if v else print('none')" 2>/dev/null)
        if [ "$SHODAN_VULNS" != "none" ] && [ -n "$SHODAN_VULNS" ]; then
            alert "Shodan encontrou VULNERABILIDADES: $SHODAN_VULNS"
        fi
    else
        ok "Shodan limpo — nenhuma porta/vuln indexada para $PUBLIC_IP"
    fi
}

# ----- SENHAS PADRÃO -----
check_passwords() {
    log "=== CHECK SENHAS PADRÃO ==="
    
    # PostgreSQL — testar via TCP (como atacante faria)
    PG_CONTAINER=$(docker ps -q --filter name=pesquisa-db 2>/dev/null | head -1)
    if [ -n "$PG_CONTAINER" ]; then
        DEFAULT_PASSWORDS="postgres password admin root 123456"
        WEAK_FOUND=false
        for pw in $DEFAULT_PASSWORDS; do
            if docker exec "$PG_CONTAINER" sh -c "PGPASSWORD=$pw psql -U postgres -h 127.0.0.1 -c 'SELECT 1'" 2>/dev/null | grep -q "1"; then
                alert "PostgreSQL aceita senha fraca: '$pw'"
                WEAK_FOUND=true
                break
            fi
        done
        if [ "$WEAK_FOUND" = false ]; then
            ok "PostgreSQL com senha forte (senhas padrão rejeitadas)"
        fi
    fi
}

# ----- FIREWALL -----
check_firewall() {
    log "=== CHECK FIREWALL ==="
    
    UFW_STATUS=$(/usr/sbin/ufw status 2>/dev/null | head -1)
    if echo "$UFW_STATUS" | grep -q "active"; then
        ok "Firewall (ufw) ativo"
    else
        alert "Firewall (ufw) INATIVO!"
    fi
}

# ----- HISTÓRICO DE IP -----
check_ip_change() {
    LAST_IP_FILE="$REPORT_DIR/.last_ip"
    if [ -f "$LAST_IP_FILE" ]; then
        LAST_IP=$(cat "$LAST_IP_FILE")
        if [ "$LAST_IP" != "$PUBLIC_IP" ]; then
            warn "IP público mudou: $LAST_IP → $PUBLIC_IP (re-scan Shodan recomendado)"
        fi
    fi
    echo "$PUBLIC_IP" > "$LAST_IP_FILE"
}

# ----- MAIN -----
case "${1:-}" in
    --ports)
        check_ports
        ;;
    --shodan)
        check_shodan
        ;;
    --quick)
        check_ports
        check_firewall
        ;;
    --json)
        JSON_MODE=true
        check_ports
        check_shodan
        check_firewall
        check_ip_change
        ;;
    *)
        check_ports
        check_shodan
        check_passwords
        check_firewall
        check_ip_change
        ;;
esac

# Output resumo
if [ -n "$ALERTS" ]; then
    echo ""
    echo "⚠️ ALERTAS ENCONTRADOS:"
    echo -e "$ALERTS"
    echo ""
    echo "SECURITY_ALERT"
    exit 1
else
    echo ""
    echo "✅ Nenhum problema encontrado"
    echo "SECURITY_OK"
    exit 0
fi
