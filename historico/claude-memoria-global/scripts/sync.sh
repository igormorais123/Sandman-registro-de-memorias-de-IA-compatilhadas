#!/bin/bash
# =============================================================================
# Script de Sincronização de Memória - Claude Code
# =============================================================================
# Este script serve como ponto de entrada para sincronização.
# A execução real é feita via Claude Code que entende o contexto.
# =============================================================================

GLOBAL_DIR="$HOME/.claude-memoria-global"
PROJETO_DIR="$1"
ACTION="${2:-sync}"

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║          🔄 Sincronização de Memória Claude Code             ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_usage() {
    echo "Uso: sync.sh [caminho_projeto] [ação]"
    echo ""
    echo "Ações disponíveis:"
    echo "  sync     - Sincronização bidirecional (padrão)"
    echo "  export   - Apenas exportar para global"
    echo "  import   - Apenas importar do global"
    echo "  status   - Verificar status de sincronização"
    echo ""
    echo "Exemplos:"
    echo "  sync.sh /home/user/meu-projeto"
    echo "  sync.sh /home/user/meu-projeto export"
    echo "  sync.sh . status"
}

check_global_structure() {
    echo -e "${YELLOW}Verificando estrutura global...${NC}"

    if [ ! -d "$GLOBAL_DIR" ]; then
        echo -e "${RED}❌ Memória global não encontrada em: $GLOBAL_DIR${NC}"
        echo "Execute o comando de inicialização primeiro."
        exit 1
    fi

    local required_files=(
        "INDICE_GLOBAL.md"
        "CONHECIMENTO_UNIVERSAL.md"
        "CATALOGO_PROJETOS.md"
    )

    local missing=0
    for file in "${required_files[@]}"; do
        if [ ! -f "$GLOBAL_DIR/$file" ]; then
            echo -e "${RED}❌ Arquivo faltando: $file${NC}"
            missing=$((missing + 1))
        fi
    done

    if [ $missing -gt 0 ]; then
        echo -e "${RED}Estrutura global incompleta. Recrie a memória global.${NC}"
        exit 1
    fi

    echo -e "${GREEN}✅ Estrutura global OK${NC}"
}

check_project_structure() {
    local projeto="$1"
    echo -e "${YELLOW}Verificando estrutura do projeto...${NC}"

    if [ ! -d "$projeto/.memoria" ]; then
        echo -e "${RED}❌ Memória local não encontrada em: $projeto/.memoria${NC}"
        echo ""
        echo "Para inicializar a memória local, execute no Claude Code:"
        echo "  claude 'inicializar sistema de memória'"
        exit 1
    fi

    if [ ! -f "$projeto/.memoria/SYNC_GLOBAL.md" ]; then
        echo -e "${YELLOW}⚠️ Arquivo de sincronização não encontrado${NC}"
        echo "O projeto pode não estar registrado para sincronização global."
    fi

    echo -e "${GREEN}✅ Estrutura do projeto OK${NC}"
}

main() {
    print_header

    if [ -z "$PROJETO_DIR" ]; then
        print_usage
        exit 1
    fi

    # Resolver caminho absoluto
    if [ "$PROJETO_DIR" = "." ]; then
        PROJETO_DIR="$(pwd)"
    elif [[ "$PROJETO_DIR" != /* ]]; then
        PROJETO_DIR="$(cd "$PROJETO_DIR" 2>/dev/null && pwd)"
    fi

    echo "Global: $GLOBAL_DIR"
    echo "Projeto: $PROJETO_DIR"
    echo "Ação: $ACTION"
    echo ""

    check_global_structure
    check_project_structure "$PROJETO_DIR"

    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${GREEN}Para executar a sincronização, use o Claude Code:${NC}"
    echo ""

    case $ACTION in
        sync)
            echo "  claude 'Sincronizar projeto com memória global'"
            ;;
        export)
            echo "  claude 'Exportar conhecimento local para memória global'"
            ;;
        import)
            echo "  claude 'Importar conhecimento da memória global'"
            ;;
        status)
            echo "  claude 'Status de sincronização com memória global'"
            ;;
        *)
            echo "  claude 'Sincronizar projeto com memória global'"
            ;;
    esac

    echo ""
    echo -e "${YELLOW}Nota: A sincronização real requer contexto do Claude Code${NC}"
    echo -e "${YELLOW}      para analisar e transferir conhecimento corretamente.${NC}"
}

main "$@"
