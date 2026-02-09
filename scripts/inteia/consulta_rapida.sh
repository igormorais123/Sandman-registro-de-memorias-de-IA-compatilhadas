#!/bin/bash
# INTEIA - Consultas Rápidas
# Uso: ./consulta_rapida.sh [comando] [args]

DATA_DIR="/root/clawd/data/inteia"
ELEITORES="$DATA_DIR/eleitores/eleitores_df_completo.json"
MAGISTRADOS="$DATA_DIR/magistrados/magistrados_completo.json"
CONSULTORES="$DATA_DIR/consultores/consultores_lendarios.json"
CANDIDATOS="$DATA_DIR/candidatos/candidatos_2026.json"

case "$1" in
    regioes)
        echo "📊 Eleitores por Região:"
        jq '[.eleitores[].regiao_administrativa] | group_by(.) | map({regiao: .[0], total: length}) | sort_by(-.total)' "$ELEITORES"
        ;;
    
    orientacao)
        echo "📊 Orientação Política:"
        jq '[.eleitores[].orientacao_politica] | group_by(.) | map({orientacao: .[0], total: length, pct: (length / 1000 * 100 | floor)}) | sort_by(-.total)' "$ELEITORES"
        ;;
    
    bolsonaro)
        echo "📊 Posição Bolsonaro:"
        jq '[.eleitores[].posicao_bolsonaro] | group_by(.) | map({posicao: .[0], total: length, pct: (length / 1000 * 100 | floor)}) | sort_by(-.total)' "$ELEITORES"
        ;;
    
    regiao)
        if [ -z "$2" ]; then
            echo "Uso: $0 regiao <nome_regiao>"
            exit 1
        fi
        REGIAO="$2"
        echo "📊 Eleitores de $REGIAO:"
        jq --arg r "$REGIAO" '[.eleitores[] | select(.regiao_administrativa == $r)] | {
            total: length,
            orientacao: (group_by(.orientacao_politica) | map({o: .[0].orientacao_politica, n: length})),
            bolsonaro: (group_by(.posicao_bolsonaro) | map({b: .[0].posicao_bolsonaro, n: length}))
        }' "$ELEITORES"
        ;;
    
    magistrados)
        echo "📊 Magistrados por Tribunal:"
        jq '[.magistrados[].tribunal] | group_by(.) | map({tribunal: .[0], total: length}) | sort_by(-.total)' "$MAGISTRADOS"
        ;;
    
    consultores)
        echo "📊 Consultores por Arquétipo:"
        jq '[.consultores[].arquetipo] | group_by(.) | map({arquetipo: .[0], total: length}) | sort_by(-.total)' "$CONSULTORES"
        ;;
    
    candidatos)
        echo "📊 Candidatos 2026:"
        jq '.[] | {nome, partido, cargo_pretendido}' "$CANDIDATOS" 2>/dev/null || \
        jq '.candidatos[] | {nome, partido, cargo_pretendido}' "$CANDIDATOS"
        ;;
    
    preocupacoes)
        echo "📊 Top 15 Preocupações:"
        jq '[.eleitores[].preocupacoes[]] | group_by(.) | map({preocupacao: .[0], total: length}) | sort_by(-.total) | .[0:15]' "$ELEITORES"
        ;;
    
    *)
        echo "INTEIA - Consultas Rápidas"
        echo ""
        echo "Comandos disponíveis:"
        echo "  regioes      - Eleitores por região administrativa"
        echo "  orientacao   - Distribuição de orientação política"
        echo "  bolsonaro    - Posição sobre Bolsonaro"
        echo "  regiao <X>   - Análise de região específica"
        echo "  magistrados  - Magistrados por tribunal"
        echo "  consultores  - Consultores por arquétipo"
        echo "  candidatos   - Lista de candidatos"
        echo "  preocupacoes - Top preocupações"
        ;;
esac
