#!/usr/bin/env python3
"""
Análise de outliers da validação C-Agentes
Identifica padrões dos eleitores que votaram NS/Indeciso vs outros candidatos
"""
import json
import re
import requests
from collections import Counter, defaultdict
from datetime import datetime

# Token da API
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyLTA1ODY4NjBhZjllNSIsIm5vbWUiOiJDQVNVTE8gVmFsaWRhY2FvIiwicGFwZWwiOiJsZWl0b3IiLCJlbWFpbCI6ImNhc3Vsb0BpbnRlaWEuY29tLmJyIiwiYXByb3ZhZG8iOmZhbHNlLCJleHAiOjE3NzA4MjU2ODYsInRpcG8iOiJhY2Nlc3MiLCJpYXQiOjE3NzA4MjIwODZ9.OJT_cEMsoGjrAkOCsTFvfEaebYN-BvaQan_GiQata-E"

def extract_vote_choice(resposta_texto):
    """Extrai a escolha de voto do texto da resposta"""
    # Buscar padrão "X-" onde X é número
    match = re.search(r'(\d+)-(\w+)', resposta_texto)
    if match:
        return match.group(1), match.group(2)
    return None, None

def classify_vote(codigo, nome):
    """Classifica o voto em categorias"""
    if codigo == "6" or nome in ["NS", "Indeciso"]:
        return "indeciso"
    elif "Celina" in nome:
        return "celina"
    else:
        return "outros"

def load_interview_data(filename):
    """Carrega dados da entrevista"""
    with open(filename, 'r') as f:
        data = json.load(f)
    return data['respostas']

def get_eleitor_profile(eleitor_id):
    """Busca perfil completo do eleitor via API"""
    try:
        headers = {"Authorization": f"Bearer {TOKEN}"}
        response = requests.get(f"https://api.inteia.com.br/api/v1/eleitores/{eleitor_id}", 
                              headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erro ao buscar perfil de {eleitor_id}: {response.status_code}")
            return None
    except Exception as e:
        print(f"Erro ao buscar perfil de {eleitor_id}: {e}")
        return None

def main():
    print("=== ANÁLISE DE OUTLIERS - VALIDAÇÃO C-AGENTES ===\n")
    
    # Carregar dados das entrevistas
    print("Carregando dados das entrevistas...")
    respostas_1 = load_interview_data('entrevista_ca38ec90.json')
    respostas_2 = load_interview_data('entrevista_4406dd5b.json')
    
    all_responses = respostas_1 + respostas_2
    print(f"Total de respostas: {len(all_responses)}")
    
    # Categorizar votos
    vote_categories = {"indeciso": [], "celina": [], "outros": []}
    vote_distribution = Counter()
    
    for resp in all_responses:
        codigo, nome = extract_vote_choice(resp['resposta_texto'])
        if codigo and nome:
            categoria = classify_vote(codigo, nome)
            vote_categories[categoria].append(resp)
            vote_distribution[f"{codigo}-{nome}"] += 1
    
    print(f"\n=== DISTRIBUIÇÃO DOS VOTOS ===")
    for voto, count in vote_distribution.most_common():
        pct = (count / len(all_responses)) * 100
        print(f"{voto}: {count} votos ({pct:.1f}%)")
    
    print(f"\n=== CATEGORIZAÇÃO ===")
    for categoria, votos in vote_categories.items():
        pct = (len(votos) / len(all_responses)) * 100
        print(f"{categoria.capitalize()}: {len(votos)} votos ({pct:.1f}%)")
    
    # Coletar IDs únicos para buscar perfis
    indecisos_ids = set([resp['eleitor_id'] for resp in vote_categories['indeciso']])
    celina_ids = set([resp['eleitor_id'] for resp in vote_categories['celina']])
    
    print(f"\n=== BUSCANDO PERFIS DOS ELEITORES ===")
    print(f"Indecisos: {len(indecisos_ids)} eleitores únicos")
    print(f"Votantes Celina: {len(celina_ids)} eleitores únicos")
    
    # Buscar perfis (limitando para evitar muitas requisições)
    perfis_indecisos = []
    perfis_celina = []
    
    print("Buscando perfis dos indecisos...")
    for i, eleitor_id in enumerate(list(indecisos_ids)[:20]):  # Limitar a 20 para teste
        perfil = get_eleitor_profile(eleitor_id)
        if perfil:
            perfis_indecisos.append(perfil)
        if i % 5 == 0:
            print(f"  Processados: {i+1}")
    
    print("Buscando perfis dos votantes da Celina...")
    for i, eleitor_id in enumerate(list(celina_ids)[:20]):  # Limitar a 20 para teste
        perfil = get_eleitor_profile(eleitor_id)
        if perfil:
            perfis_celina.append(perfil)
        if i % 5 == 0:
            print(f"  Processados: {i+1}")
    
    # Análise dos padrões
    print(f"\n=== ANÁLISE DOS PADRÕES ===")
    
    def analyze_profiles(perfis, nome_grupo):
        if not perfis:
            print(f"Nenhum perfil disponível para {nome_grupo}")
            return
        
        print(f"\n--- {nome_grupo} ({len(perfis)} perfis) ---")
        
        # Campos para analisar
        campos_interesse = ['orientacao_politica', 'faixa_etaria', 'regiao_administrativa', 
                          'posicao_bolsonaro', 'escolaridade', 'renda', 'genero']
        
        for campo in campos_interesse:
            if any(campo in perfil for perfil in perfis):
                valores = [perfil.get(campo) for perfil in perfis if perfil.get(campo)]
                if valores:
                    counter = Counter(valores)
                    print(f"\n{campo.replace('_', ' ').title()}:")
                    for valor, count in counter.most_common():
                        pct = (count / len(valores)) * 100
                        print(f"  {valor}: {count} ({pct:.1f}%)")
    
    analyze_profiles(perfis_indecisos, "INDECISOS")
    analyze_profiles(perfis_celina, "VOTANTES CELINA")
    
    # Salvar dados detalhados para análise posterior
    dados_analise = {
        'timestamp': datetime.now().isoformat(),
        'total_respostas': len(all_responses),
        'distribuicao_votos': dict(vote_distribution),
        'categorias': {k: len(v) for k, v in vote_categories.items()},
        'perfis_indecisos': perfis_indecisos,
        'perfis_celina': perfis_celina,
        'amostras_respostas': {
            'indecisos': [resp['resposta_texto'][:200] + '...' for resp in vote_categories['indeciso'][:5]],
            'celina': [resp['resposta_texto'][:200] + '...' for resp in vote_categories['celina'][:5]]
        }
    }
    
    with open('dados_analise_outliers.json', 'w', encoding='utf-8') as f:
        json.dump(dados_analise, f, ensure_ascii=False, indent=2)
    
    print(f"\n=== DADOS SALVOS ===")
    print("Arquivo: dados_analise_outliers.json")
    
    return dados_analise

if __name__ == "__main__":
    dados = main()