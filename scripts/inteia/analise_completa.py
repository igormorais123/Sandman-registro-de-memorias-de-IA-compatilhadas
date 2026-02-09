#!/usr/bin/env python3
"""
INTEIA — Script de Análise Completa
Todas as análises possíveis com as bases de dados

Uso:
    python3 analise_completa.py [--regiao GAMA] [--output json|text]
"""

import json
import sys
import os
from collections import Counter
from typing import Dict, List, Any
import argparse

# Paths
DATA_DIR = "/root/clawd/data/inteia"
ELEITORES_FILE = f"{DATA_DIR}/eleitores/eleitores_df_completo.json"
MAGISTRADOS_FILE = f"{DATA_DIR}/magistrados/magistrados_completo.json"
CONSULTORES_FILE = f"{DATA_DIR}/consultores/consultores_lendarios.json"
CANDIDATOS_FILE = f"{DATA_DIR}/candidatos/candidatos_2026.json"


def load_data():
    """Carrega todas as bases de dados"""
    data = {}
    
    # Eleitores
    with open(ELEITORES_FILE, 'r') as f:
        data['eleitores'] = json.load(f)['eleitores']
    
    # Magistrados
    with open(MAGISTRADOS_FILE, 'r') as f:
        data['magistrados'] = json.load(f)['magistrados']
    
    # Consultores
    with open(CONSULTORES_FILE, 'r') as f:
        data['consultores'] = json.load(f)['consultores']
    
    # Candidatos
    with open(CANDIDATOS_FILE, 'r') as f:
        cand = json.load(f)
        data['candidatos'] = cand if isinstance(cand, list) else cand.get('candidatos', [])
    
    return data


def analise_demografica(eleitores: List[Dict], regiao: str = None) -> Dict:
    """Análise demográfica dos eleitores"""
    if regiao:
        eleitores = [e for e in eleitores if e.get('regiao_administrativa', '').lower() == regiao.lower()]
    
    n = len(eleitores)
    if n == 0:
        return {"erro": "Nenhum eleitor encontrado"}
    
    # Gênero
    genero = Counter(e['genero'] for e in eleitores)
    
    # Idade
    idades = [e['idade'] for e in eleitores if 'idade' in e]
    idade_media = sum(idades) / len(idades) if idades else 0
    
    # Cor/Raça
    cor_raca = Counter(e.get('cor_raca', 'N/A') for e in eleitores)
    
    # Escolaridade
    escolaridade = Counter(e.get('escolaridade', 'N/A') for e in eleitores)
    
    # Renda
    renda = Counter(e.get('renda_salarios_minimos', 'N/A') for e in eleitores)
    
    # Religião
    religiao = Counter(e.get('religiao', 'N/A') for e in eleitores)
    
    return {
        "total": n,
        "regiao": regiao or "Todas",
        "genero": dict(genero),
        "idade_media": round(idade_media, 1),
        "cor_raca": dict(cor_raca),
        "escolaridade": dict(escolaridade),
        "renda": dict(renda),
        "religiao": dict(religiao)
    }


def analise_politica(eleitores: List[Dict], regiao: str = None) -> Dict:
    """Análise do perfil político"""
    if regiao:
        eleitores = [e for e in eleitores if e.get('regiao_administrativa', '').lower() == regiao.lower()]
    
    n = len(eleitores)
    if n == 0:
        return {"erro": "Nenhum eleitor encontrado"}
    
    # Orientação política
    orientacao = Counter(e.get('orientacao_politica', 'N/A') for e in eleitores)
    
    # Posição Bolsonaro
    bolsonaro = Counter(e.get('posicao_bolsonaro', 'N/A') for e in eleitores)
    
    # Interesse político
    interesse = Counter(e.get('interesse_politico', 'N/A') for e in eleitores)
    
    # Agregações
    esquerda = sum(1 for e in eleitores if e.get('orientacao_politica') in ['esquerda', 'centro_esquerda'])
    direita = sum(1 for e in eleitores if e.get('orientacao_politica') in ['direita', 'centro_direita'])
    centro = sum(1 for e in eleitores if e.get('orientacao_politica') == 'centro')
    
    apoiadores = sum(1 for e in eleitores if e.get('posicao_bolsonaro') in ['apoiador_forte', 'apoiador_moderado'])
    criticos = sum(1 for e in eleitores if e.get('posicao_bolsonaro') in ['critico_forte', 'critico_moderado'])
    
    return {
        "total": n,
        "orientacao_politica": dict(orientacao),
        "posicao_bolsonaro": dict(bolsonaro),
        "interesse_politico": dict(interesse),
        "agregacoes": {
            "esquerda_total": esquerda,
            "direita_total": direita,
            "centro": centro,
            "bolsonaro_apoiadores": apoiadores,
            "bolsonaro_criticos": criticos
        },
        "percentuais": {
            "esquerda_pct": round(esquerda/n*100, 1),
            "direita_pct": round(direita/n*100, 1),
            "centro_pct": round(centro/n*100, 1),
            "apoiadores_pct": round(apoiadores/n*100, 1),
            "criticos_pct": round(criticos/n*100, 1)
        }
    }


def analise_preocupacoes(eleitores: List[Dict], regiao: str = None, top: int = 10) -> Dict:
    """Análise de preocupações, valores e medos"""
    if regiao:
        eleitores = [e for e in eleitores if e.get('regiao_administrativa', '').lower() == regiao.lower()]
    
    # Preocupações
    preocs = []
    for e in eleitores:
        if isinstance(e.get('preocupacoes'), list):
            preocs.extend(e['preocupacoes'])
    
    # Valores
    valores = []
    for e in eleitores:
        if isinstance(e.get('valores'), list):
            valores.extend(e['valores'])
    
    # Medos
    medos = []
    for e in eleitores:
        if isinstance(e.get('medos'), list):
            medos.extend(e['medos'])
    
    return {
        "total_eleitores": len(eleitores),
        "top_preocupacoes": dict(Counter(preocs).most_common(top)),
        "top_valores": dict(Counter(valores).most_common(top)),
        "top_medos": dict(Counter(medos).most_common(top))
    }


def analise_regioes(eleitores: List[Dict]) -> Dict:
    """Análise por região administrativa"""
    regioes = Counter(e.get('regiao_administrativa', 'N/A') for e in eleitores)
    
    resultado = {}
    for regiao, count in regioes.most_common():
        eleitores_regiao = [e for e in eleitores if e.get('regiao_administrativa') == regiao]
        
        # Orientação predominante
        orient = Counter(e.get('orientacao_politica') for e in eleitores_regiao)
        orient_dom = orient.most_common(1)[0] if orient else ('N/A', 0)
        
        # Bolsonaro predominante
        bols = Counter(e.get('posicao_bolsonaro') for e in eleitores_regiao)
        bols_dom = bols.most_common(1)[0] if bols else ('N/A', 0)
        
        resultado[regiao] = {
            "total": count,
            "orientacao_predominante": orient_dom[0],
            "posicao_bolsonaro_predominante": bols_dom[0]
        }
    
    return resultado


def analise_magistrados(magistrados: List[Dict]) -> Dict:
    """Análise dos magistrados"""
    n = len(magistrados)
    
    # Por tribunal
    tribunais = Counter(m.get('tribunal', 'N/A') for m in magistrados)
    
    # Por cargo
    cargos = Counter(m.get('cargo', 'N/A') for m in magistrados)
    
    return {
        "total": n,
        "por_tribunal": dict(tribunais),
        "por_cargo": dict(cargos)
    }


def analise_consultores(consultores: List[Dict]) -> Dict:
    """Análise dos consultores lendários"""
    n = len(consultores)
    
    # Por arquétipo
    arquetipos = Counter(c.get('arquetipo', 'N/A') for c in consultores)
    
    # Por área de expertise (flatten)
    areas = []
    for c in consultores:
        if isinstance(c.get('areas_expertise'), list):
            areas.extend(c['areas_expertise'])
    
    return {
        "total": n,
        "por_arquetipo": dict(arquetipos),
        "top_areas_expertise": dict(Counter(areas).most_common(15))
    }


def simulacao_campanha(eleitores: List[Dict], candidato: str, regiao: str = None) -> Dict:
    """Simula resultado de campanha para um candidato"""
    if regiao:
        eleitores = [e for e in eleitores if e.get('regiao_administrativa', '').lower() == regiao.lower()]
    
    n = len(eleitores)
    votos = 0
    
    # Regras simplificadas por candidato
    for e in eleitores:
        orient = e.get('orientacao_politica', '')
        bols = e.get('posicao_bolsonaro', '')
        
        if candidato.lower() == 'celina':
            # Celina: centro + direita moderada não-bolsonarista
            if orient == 'centro':
                votos += 0.7
            elif orient in ['centro_direita', 'direita'] and bols not in ['apoiador_forte']:
                votos += 0.4
            elif orient in ['centro_esquerda'] and bols in ['critico_forte', 'critico_moderado']:
                votos += 0.2
                
        elif candidato.lower() == 'grass':
            # Grass: esquerda
            if orient in ['esquerda', 'centro_esquerda']:
                votos += 0.6
            elif orient == 'centro' and bols in ['critico_forte']:
                votos += 0.3
                
        elif candidato.lower() == 'flavia':
            # Flávia: bolsonaristas
            if bols in ['apoiador_forte', 'apoiador_moderado']:
                votos += 0.7
            elif orient == 'direita':
                votos += 0.3
    
    return {
        "candidato": candidato,
        "regiao": regiao or "Todas",
        "total_eleitores": n,
        "votos_estimados": round(votos),
        "percentual": round(votos/n*100, 1) if n > 0 else 0
    }


def main():
    parser = argparse.ArgumentParser(description='INTEIA - Análise Completa')
    parser.add_argument('--regiao', type=str, help='Filtrar por região (ex: Gama)')
    parser.add_argument('--output', type=str, default='text', choices=['json', 'text'])
    parser.add_argument('--analise', type=str, default='todas', 
                        choices=['demografica', 'politica', 'preocupacoes', 'regioes', 
                                'magistrados', 'consultores', 'campanha', 'todas'])
    parser.add_argument('--candidato', type=str, help='Para simulação de campanha')
    args = parser.parse_args()
    
    # Carregar dados
    print("📥 Carregando dados...", file=sys.stderr)
    data = load_data()
    
    resultados = {}
    
    if args.analise in ['demografica', 'todas']:
        resultados['demografica'] = analise_demografica(data['eleitores'], args.regiao)
    
    if args.analise in ['politica', 'todas']:
        resultados['politica'] = analise_politica(data['eleitores'], args.regiao)
    
    if args.analise in ['preocupacoes', 'todas']:
        resultados['preocupacoes'] = analise_preocupacoes(data['eleitores'], args.regiao)
    
    if args.analise in ['regioes', 'todas']:
        resultados['regioes'] = analise_regioes(data['eleitores'])
    
    if args.analise in ['magistrados', 'todas']:
        resultados['magistrados'] = analise_magistrados(data['magistrados'])
    
    if args.analise in ['consultores', 'todas']:
        resultados['consultores'] = analise_consultores(data['consultores'])
    
    if args.analise == 'campanha' and args.candidato:
        resultados['campanha'] = simulacao_campanha(data['eleitores'], args.candidato, args.regiao)
    
    # Output
    if args.output == 'json':
        print(json.dumps(resultados, indent=2, ensure_ascii=False))
    else:
        for secao, dados in resultados.items():
            print(f"\n{'='*60}")
            print(f"📊 {secao.upper()}")
            print('='*60)
            print(json.dumps(dados, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
