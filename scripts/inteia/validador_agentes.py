#!/usr/bin/env python3
"""
INTEIA - Validador e Corretor de Agentes
Identifica e corrige incoerências nas bases de dados

Regras de validação:
1. Eleitores: história deve ser coerente com ficha (idade, escolaridade, renda, etc)
2. Magistrados: dados profissionais devem ser consistentes
3. Consultores: informações devem bater com dados reais históricos
4. Gestores: cargos e datas devem ser possíveis
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Tuple, Any
from collections import defaultdict

DATA_DIR = "/root/clawd/data/inteia"

class ValidadorAgentes:
    def __init__(self):
        self.erros = defaultdict(list)
        self.correcoes = defaultdict(list)
        self.estatisticas = defaultdict(int)
    
    def validar_eleitor(self, eleitor: Dict) -> List[Dict]:
        """Valida coerência de um eleitor"""
        erros = []
        nome = eleitor.get('nome', 'Desconhecido')
        
        # 1. Idade vs Escolaridade
        idade = eleitor.get('idade', 0)
        escolaridade = eleitor.get('escolaridade', '')
        
        if idade < 22 and 'pos' in escolaridade.lower():
            erros.append({
                'campo': 'escolaridade',
                'erro': f'Idade {idade} incompatível com pós-graduação',
                'valor_atual': escolaridade,
                'sugestao': 'medio_completo_ou_sup_incompleto'
            })
        
        if idade < 18:
            erros.append({
                'campo': 'idade',
                'erro': f'Eleitor com menos de 18 anos ({idade})',
                'valor_atual': idade,
                'sugestao': 18
            })
        
        # 2. Renda vs Ocupação
        renda = eleitor.get('renda_salarios_minimos', '')
        ocupacao = eleitor.get('ocupacao_vinculo', '')
        
        if ocupacao == 'desempregado' and renda in ['mais_de_10_ate_20', 'mais_de_20']:
            erros.append({
                'campo': 'renda_salarios_minimos',
                'erro': f'Desempregado com renda alta ({renda})',
                'valor_atual': renda,
                'sugestao': 'ate_1'
            })
        
        if ocupacao == 'estudante' and renda in ['mais_de_10_ate_20', 'mais_de_20']:
            erros.append({
                'campo': 'renda_salarios_minimos',
                'erro': f'Estudante com renda muito alta ({renda})',
                'valor_atual': renda,
                'sugestao': 'mais_de_1_ate_2'
            })
        
        # 3. Idade vs Aposentado
        if ocupacao == 'aposentado' and idade < 50:
            erros.append({
                'campo': 'ocupacao_vinculo',
                'erro': f'Aposentado muito jovem ({idade} anos)',
                'valor_atual': ocupacao,
                'sugestao': 'clt' if idade > 25 else 'estudante'
            })
        
        # 4. História vs Ficha
        historia = eleitor.get('historia_resumida', '')
        
        # Verificar menções de idade na história
        idade_mencionada = re.findall(r'(\d+)\s*anos', historia)
        for idade_str in idade_mencionada:
            idade_hist = int(idade_str)
            if abs(idade_hist - idade) > 5 and idade_hist > 10:
                erros.append({
                    'campo': 'historia_resumida',
                    'erro': f'História menciona {idade_hist} anos, ficha diz {idade}',
                    'valor_atual': f'...{idade_hist} anos...',
                    'sugestao': 'Ajustar história para refletir idade correta'
                })
        
        # Verificar gênero na história
        genero = eleitor.get('genero', '')
        if genero == 'feminino':
            if re.search(r'\bele\b|\bmarido\b.*trabalha|\bpai\b.*de\s+família', historia.lower()):
                erros.append({
                    'campo': 'historia_resumida',
                    'erro': 'História usa pronomes/termos masculinos para pessoa feminina',
                    'valor_atual': 'Termos masculinos detectados',
                    'sugestao': 'Ajustar para pronomes femininos'
                })
        elif genero == 'masculino':
            if re.search(r'\bela\b|\besposa\b.*trabalha|\bmãe\b.*de\s+família', historia.lower()):
                erros.append({
                    'campo': 'historia_resumida',
                    'erro': 'História usa pronomes/termos femininos para pessoa masculina',
                    'valor_atual': 'Termos femininos detectados',
                    'sugestao': 'Ajustar para pronomes masculinos'
                })
        
        # 5. Estado civil vs Filhos (menos restritivo)
        estado_civil = eleitor.get('estado_civil', '')
        filhos = eleitor.get('filhos', 0)
        
        # Só erro se for muito extremo
        if filhos > 6:
            erros.append({
                'campo': 'filhos',
                'erro': f'Número de filhos muito alto ({filhos})',
                'valor_atual': filhos,
                'sugestao': min(filhos, 5)
            })
        
        # 6. Orientação política vs Valores (coerência lógica)
        orientacao = eleitor.get('orientacao_politica', '')
        valores = eleitor.get('valores', [])
        
        if orientacao == 'esquerda' and 'Meritocracia' in valores and 'Igualdade' not in valores:
            erros.append({
                'campo': 'valores',
                'erro': 'Esquerda com meritocracia mas sem igualdade',
                'valor_atual': valores,
                'sugestao': 'Adicionar "Igualdade" ou "Justiça social"'
            })
        
        if orientacao == 'direita' and 'Comunismo' in valores:
            erros.append({
                'campo': 'valores',
                'erro': 'Direita com comunismo nos valores',
                'valor_atual': valores,
                'sugestao': 'Remover valor contraditório'
            })
        
        return erros
    
    def validar_magistrado(self, magistrado: Dict) -> List[Dict]:
        """Valida coerência de um magistrado"""
        erros = []
        nome = magistrado.get('nome', 'Desconhecido')
        
        # 1. Tribunal deve existir
        tribunal = magistrado.get('tribunal', '')
        tribunais_validos = ['STF', 'STJ', 'TJDFT', 'TRF1', 'TST', 'TSE', 'STM']
        if tribunal and tribunal not in tribunais_validos:
            erros.append({
                'campo': 'tribunal',
                'erro': f'Tribunal desconhecido: {tribunal}',
                'valor_atual': tribunal,
                'sugestao': 'TJDFT'
            })
        
        # 2. Cargo deve ser compatível com tribunal
        cargo = magistrado.get('cargo', '')
        if tribunal == 'STF' and cargo and 'Desembargador' in cargo:
            erros.append({
                'campo': 'cargo',
                'erro': 'STF não tem desembargadores (são Ministros)',
                'valor_atual': cargo,
                'sugestao': 'Ministro'
            })
        
        # 3. Campos obrigatórios vazios
        campos_importantes = ['graduacao', 'perfil_filosofico', 'tendencia_jurisprudencial']
        for campo in campos_importantes:
            valor = magistrado.get(campo, '')
            if not valor or valor == 'N/A' or valor == 'null':
                erros.append({
                    'campo': campo,
                    'erro': f'Campo importante vazio ou inválido',
                    'valor_atual': valor,
                    'sugestao': 'Preencher com dados pesquisados'
                })
        
        return erros
    
    def validar_consultor(self, consultor: Dict) -> List[Dict]:
        """Valida coerência de um consultor lendário"""
        erros = []
        nome = consultor.get('nome', 'Desconhecido')
        
        # 1. Datas de vida
        nascimento = consultor.get('ano_nascimento', 0)
        morte = consultor.get('ano_morte', 0)
        
        if nascimento and morte:
            idade_morte = morte - nascimento
            if idade_morte < 20:
                erros.append({
                    'campo': 'ano_morte',
                    'erro': f'Morreu muito jovem ({idade_morte} anos)',
                    'valor_atual': f'{nascimento}-{morte}',
                    'sugestao': 'Verificar datas históricas'
                })
            if idade_morte > 120:
                erros.append({
                    'campo': 'ano_morte',
                    'erro': f'Viveu tempo impossível ({idade_morte} anos)',
                    'valor_atual': f'{nascimento}-{morte}',
                    'sugestao': 'Verificar datas históricas'
                })
        
        if nascimento and nascimento > 2000:
            erros.append({
                'campo': 'ano_nascimento',
                'erro': 'Consultor lendário nasceu depois de 2000',
                'valor_atual': nascimento,
                'sugestao': 'Verificar se é figura histórica'
            })
        
        # 2. Áreas de expertise vazias
        areas = consultor.get('areas_expertise', [])
        if not areas or len(areas) == 0:
            erros.append({
                'campo': 'areas_expertise',
                'erro': 'Consultor sem áreas de expertise',
                'valor_atual': areas,
                'sugestao': 'Adicionar especialidades baseadas em biografia'
            })
        
        # 3. Biografia vazia
        bio = consultor.get('biografia_resumida', '')
        if not bio or len(bio) < 50:
            erros.append({
                'campo': 'biografia_resumida',
                'erro': 'Biografia muito curta ou vazia',
                'valor_atual': bio[:50] if bio else '',
                'sugestao': 'Expandir com informações históricas'
            })
        
        return erros
    
    def validar_todos(self) -> Dict:
        """Valida todas as bases de dados"""
        resultados = {
            'timestamp': datetime.now().isoformat(),
            'resumo': {},
            'erros_por_base': {},
            'amostras_erros': {}
        }
        
        # Eleitores
        print("📊 Validando eleitores...")
        with open(f"{DATA_DIR}/eleitores/eleitores_df_completo.json") as f:
            data = json.load(f)
            eleitores = data.get('eleitores', data) if isinstance(data, dict) else data
        
        erros_eleitores = []
        for e in eleitores:
            erros = self.validar_eleitor(e)
            if erros:
                erros_eleitores.append({
                    'nome': e.get('nome'),
                    'erros': erros
                })
        
        resultados['resumo']['eleitores'] = {
            'total': len(eleitores),
            'com_erros': len(erros_eleitores),
            'taxa_erro': round(len(erros_eleitores)/len(eleitores)*100, 1)
        }
        resultados['erros_por_base']['eleitores'] = erros_eleitores
        resultados['amostras_erros']['eleitores'] = erros_eleitores[:5]
        
        # Magistrados
        print("📊 Validando magistrados...")
        with open(f"{DATA_DIR}/magistrados/magistrados_completo.json") as f:
            data = json.load(f)
            magistrados = data.get('magistrados', [])
        
        erros_magistrados = []
        for m in magistrados:
            erros = self.validar_magistrado(m)
            if erros:
                erros_magistrados.append({
                    'nome': m.get('nome'),
                    'erros': erros
                })
        
        resultados['resumo']['magistrados'] = {
            'total': len(magistrados),
            'com_erros': len(erros_magistrados),
            'taxa_erro': round(len(erros_magistrados)/len(magistrados)*100, 1) if magistrados else 0
        }
        resultados['erros_por_base']['magistrados'] = erros_magistrados
        resultados['amostras_erros']['magistrados'] = erros_magistrados[:5]
        
        # Consultores
        print("📊 Validando consultores...")
        with open(f"{DATA_DIR}/consultores/consultores_lendarios.json") as f:
            data = json.load(f)
            consultores = data.get('consultores', [])
        
        erros_consultores = []
        for c in consultores:
            erros = self.validar_consultor(c)
            if erros:
                erros_consultores.append({
                    'nome': c.get('nome'),
                    'erros': erros
                })
        
        resultados['resumo']['consultores'] = {
            'total': len(consultores),
            'com_erros': len(erros_consultores),
            'taxa_erro': round(len(erros_consultores)/len(consultores)*100, 1) if consultores else 0
        }
        resultados['erros_por_base']['consultores'] = erros_consultores
        resultados['amostras_erros']['consultores'] = erros_consultores[:5]
        
        return resultados


def main():
    validador = ValidadorAgentes()
    resultados = validador.validar_todos()
    
    print("\n" + "="*60)
    print("📊 RELATÓRIO DE VALIDAÇÃO - INTEIA")
    print("="*60)
    
    for base, stats in resultados['resumo'].items():
        print(f"\n📁 {base.upper()}")
        print(f"   Total: {stats['total']}")
        print(f"   Com erros: {stats['com_erros']} ({stats['taxa_erro']}%)")
    
    print("\n" + "="*60)
    print("📋 AMOSTRAS DE ERROS ENCONTRADOS")
    print("="*60)
    
    for base, amostras in resultados['amostras_erros'].items():
        if amostras:
            print(f"\n--- {base.upper()} ---")
            for item in amostras[:3]:
                print(f"\n👤 {item['nome']}")
                for erro in item['erros'][:2]:
                    print(f"   ❌ {erro['campo']}: {erro['erro']}")
                    print(f"      Sugestão: {erro['sugestao']}")
    
    # Salvar relatório completo
    with open(f"{DATA_DIR}/validacao_relatorio.json", 'w') as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Relatório salvo em: {DATA_DIR}/validacao_relatorio.json")
    
    return resultados


if __name__ == '__main__':
    main()
