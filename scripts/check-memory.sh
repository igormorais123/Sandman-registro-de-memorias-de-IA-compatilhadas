#!/bin/bash
# =============================================================================
# Script de Verificação de Integridade - Memória Claude Code
# =============================================================================
# Verifica se a estrutura de memória global está íntegra
# =============================================================================

GLOBAL_DIR="$HOME/.claude-memoria-global"

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║       🔍 Verificação de Integridade - Memória Global         ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

check_directories() {
    echo -e "${YELLOW}Verificando diretórios...${NC}"

    local dirs=(
        "projetos"
        "consolidado"
        "meta"
        "scripts"
        "temp"
    )

    local missing=0
    for dir in "${dirs[@]}"; do
        if [ -d "$GLOBAL_DIR/$dir" ]; then
            echo -e "  ${GREEN}✅${NC} $dir/"
        else
            echo -e "  ${RED}❌${NC} $dir/ (faltando)"
            missing=$((missing + 1))
        fi
    done

    return $missing
}

check_files() {
    echo ""
    echo -e "${YELLOW}Verificando arquivos principais...${NC}"

    local files=(
        "INDICE_GLOBAL.md"
        "CONHECIMENTO_UNIVERSAL.md"
        "CATALOGO_PROJETOS.md"
        "PADROES_CODIGO.md"
        "ANTIPADROES_GLOBAIS.md"
        "PROMPTS_EFETIVOS.md"
        "FERRAMENTAS_RECOMENDADAS.md"
        "META_APRENDIZADO.md"
        "PROTOCOLO_SONO_GLOBAL.md"
    )

    local missing=0
    local total_size=0

    for file in "${files[@]}"; do
        if [ -f "$GLOBAL_DIR/$file" ]; then
            local size=$(wc -c < "$GLOBAL_DIR/$file" 2>/dev/null || echo "0")
            total_size=$((total_size + size))
            local size_kb=$((size / 1024))
            echo -e "  ${GREEN}✅${NC} $file (${size_kb}KB)"
        else
            echo -e "  ${RED}❌${NC} $file (faltando)"
            missing=$((missing + 1))
        fi
    done

    echo ""
    echo "  Total: $((total_size / 1024))KB"

    return $missing
}

check_scripts() {
    echo ""
    echo -e "${YELLOW}Verificando scripts...${NC}"

    local scripts=(
        "scripts/sync.sh"
        "scripts/check-memory.sh"
    )

    local missing=0
    for script in "${scripts[@]}"; do
        if [ -f "$GLOBAL_DIR/$script" ]; then
            if [ -x "$GLOBAL_DIR/$script" ]; then
                echo -e "  ${GREEN}✅${NC} $script (executável)"
            else
                echo -e "  ${YELLOW}⚠️${NC} $script (não executável)"
            fi
        else
            echo -e "  ${RED}❌${NC} $script (faltando)"
            missing=$((missing + 1))
        fi
    done

    return $missing
}

count_projects() {
    echo ""
    echo -e "${YELLOW}Contando projetos registrados...${NC}"

    local count=$(ls -1 "$GLOBAL_DIR/projetos"/*.md 2>/dev/null | wc -l)
    echo "  Projetos com arquivo dedicado: $count"

    # Contar linhas na tabela do catálogo (aproximação)
    if [ -f "$GLOBAL_DIR/CATALOGO_PROJETOS.md" ]; then
        local catalog_entries=$(grep -c "^### " "$GLOBAL_DIR/CATALOGO_PROJETOS.md" 2>/dev/null || echo "0")
        echo "  Entradas no catálogo: $catalog_entries"
    fi
}

generate_summary() {
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo ""

    local dir_missing=$1
    local file_missing=$2
    local script_missing=$3

    local total_issues=$((dir_missing + file_missing + script_missing))

    if [ $total_issues -eq 0 ]; then
        echo -e "${GREEN}✅ SISTEMA DE MEMÓRIA GLOBAL ÍNTEGRO${NC}"
        echo ""
        echo "Todos os componentes estão presentes e configurados."
    else
        echo -e "${RED}⚠️ PROBLEMAS DETECTADOS: $total_issues${NC}"
        echo ""
        echo "Detalhes:"
        [ $dir_missing -gt 0 ] && echo "  - $dir_missing diretório(s) faltando"
        [ $file_missing -gt 0 ] && echo "  - $file_missing arquivo(s) faltando"
        [ $script_missing -gt 0 ] && echo "  - $script_missing script(s) faltando"
        echo ""
        echo "Para reconstruir a estrutura, execute no Claude Code:"
        echo "  claude 'Reconstruir sistema de memória global'"
    fi
}

main() {
    print_header

    if [ ! -d "$GLOBAL_DIR" ]; then
        echo -e "${RED}❌ Memória global não encontrada em: $GLOBAL_DIR${NC}"
        echo ""
        echo "Para criar a estrutura de memória global, execute no Claude Code:"
        echo "  claude 'Inicializar sistema de memória hierárquica'"
        exit 1
    fi

    echo "Localização: $GLOBAL_DIR"
    echo ""

    check_directories
    dir_missing=$?

    check_files
    file_missing=$?

    check_scripts
    script_missing=$?

    count_projects

    generate_summary $dir_missing $file_missing $script_missing
}

main "$@"
