#!/usr/bin/env python3
"""
Script para corrigir as bases de dados INTEIA
- Eleitores: corrigir idade, história, renda, escolaridade, valores
- Magistrados: enriquecer com dados pesquisados
"""

import json
import re
from datetime import datetime

# Carregar dados
with open('/root/clawd/data/inteia/eleitores/eleitores_df_completo.json', 'r', encoding='utf-8') as f:
    dados_eleitores = json.load(f)

with open('/root/clawd/data/inteia/validacao_relatorio.json', 'r', encoding='utf-8') as f:
    relatorio = json.load(f)

# Criar índice de eleitores por nome
eleitores_por_nome = {e['nome']: e for e in dados_eleitores['eleitores']}

# Contadores de correções
correcoes = {
    'idade_menor_18': [],
    'historia_idade': [],
    'escolaridade': [],
    'renda': [],
    'valores': []
}

# Processar cada erro de eleitor
for erro_eleitor in relatorio['erros_por_base']['eleitores']:
    nome = erro_eleitor['nome']
    if nome not in eleitores_por_nome:
        print(f"AVISO: Eleitor não encontrado: {nome}")
        continue
    
    eleitor = eleitores_por_nome[nome]
    
    for erro in erro_eleitor['erros']:
        campo = erro['campo']
        
        # Corrigir idade < 18
        if campo == 'idade' and 'menos de 18' in erro['erro']:
            idade_antiga = eleitor['idade']
            eleitor['idade'] = 18
            correcoes['idade_menor_18'].append({
                'nome': nome,
                'de': idade_antiga,
                'para': 18
            })
            
            # Também corrigir história se menciona a idade antiga
            if 'historia_resumida' in eleitor:
                historia = eleitor['historia_resumida']
                # Atualizar referência de voto facultativo para obrigatório
                if eleitor.get('voto_facultativo'):
                    eleitor['voto_facultativo'] = False
        
        # Corrigir história que menciona idade errada
        elif campo == 'historia_resumida':
            match = re.search(r'menciona (\d+) anos, ficha diz (\d+)', erro['erro'])
            if match:
                idade_errada = match.group(1)
                idade_certa = match.group(2)
                historia_antiga = eleitor['historia_resumida']
                # Substituir a menção de idade
                nova_historia = re.sub(
                    rf'\b{idade_errada}\b\s*anos',
                    f'{idade_certa} anos',
                    historia_antiga
                )
                eleitor['historia_resumida'] = nova_historia
                correcoes['historia_idade'].append({
                    'nome': nome,
                    'idade_mencionada': idade_errada,
                    'idade_correta': idade_certa
                })
        
        # Corrigir escolaridade incompatível
        elif campo == 'escolaridade':
            eleitor['escolaridade'] = erro['sugestao']
            correcoes['escolaridade'].append({
                'nome': nome,
                'de': erro['valor_atual'],
                'para': erro['sugestao']
            })
        
        # Corrigir renda incompatível
        elif campo == 'renda_salarios_minimos':
            eleitor['renda_salarios_minimos'] = erro['sugestao']
            correcoes['renda'].append({
                'nome': nome,
                'de': erro['valor_atual'],
                'para': erro['sugestao']
            })
        
        # Corrigir valores (esquerda com meritocracia sem igualdade)
        elif campo == 'valores':
            valores = eleitor.get('valores', [])
            if 'Meritocracia' in valores and 'Igualdade' not in valores and 'Justiça social' not in valores:
                # Adicionar Igualdade mantendo no máximo 5 valores
                if len(valores) < 5:
                    valores.append('Igualdade')
                else:
                    # Substituir Meritocracia por Igualdade (mantém coerência com esquerda)
                    idx = valores.index('Meritocracia')
                    valores[idx] = 'Igualdade'
                eleitor['valores'] = valores
                correcoes['valores'].append({
                    'nome': nome,
                    'acao': 'Substituído Meritocracia por Igualdade'
                })

# Salvar eleitores corrigidos
with open('/root/clawd/data/inteia/eleitores/eleitores_df_corrigido.json', 'w', encoding='utf-8') as f:
    json.dump(dados_eleitores, f, ensure_ascii=False, indent=2)

# Imprimir resumo
print("=" * 60)
print("RESUMO DE CORREÇÕES - ELEITORES")
print("=" * 60)
print(f"Idades < 18 corrigidas: {len(correcoes['idade_menor_18'])}")
print(f"Histórias com idade errada: {len(correcoes['historia_idade'])}")
print(f"Escolaridades incompatíveis: {len(correcoes['escolaridade'])}")
print(f"Rendas incompatíveis: {len(correcoes['renda'])}")
print(f"Valores incoerentes: {len(correcoes['valores'])}")
print(f"\nTotal de correções: {sum(len(v) for v in correcoes.values())}")
print(f"\nArquivo salvo: eleitores_df_corrigido.json")

# Salvar log de correções
log_correcoes = {
    'timestamp': datetime.now().isoformat(),
    'correcoes': correcoes,
    'totais': {k: len(v) for k, v in correcoes.items()},
    'total_geral': sum(len(v) for v in correcoes.values())
}

with open('/root/clawd/data/inteia/log_correcoes_eleitores.json', 'w', encoding='utf-8') as f:
    json.dump(log_correcoes, f, ensure_ascii=False, indent=2)

print("\nLog salvo: log_correcoes_eleitores.json")
