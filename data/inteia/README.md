# 📊 INTEIA — Base de Dados Completa

## Dados Extraídos: 2026-02-07 23:30

Sistema de Pesquisa Eleitoral DF 2026 — INTEIA
https://inteia.com.br

---

## 📁 Estrutura

```
/root/clawd/data/inteia/
├── README.md                 # Este arquivo
├── eleitores/
│   └── eleitores_df_completo.json    # 1000 eleitores sintéticos
├── magistrados/
│   └── magistrados_completo.json     # 164 magistrados (STF/STJ/TJDFT/TRF1)
├── consultores/
│   └── consultores_lendarios.json    # 100 consultores (digital twins)
├── candidatos/
│   └── candidatos_2026.json          # 18 candidatos
├── parlamentares/
│   └── parlamentares_df.json         # Deputados/Senadores DF
└── gestores/
    └── gestores.json                 # Gestores públicos
```

---

## 📊 Inventário

| Base | Registros | Campos | Tamanho |
|------|-----------|--------|---------|
| Eleitores | 1.000 | 32+ | 2.0 MB |
| Magistrados | 164 | 40+ | ~2 MB |
| Consultores | 100 | 50+ | ~3 MB |
| Candidatos | 18 | 30+ | ~500 KB |
| **TOTAL** | **1.282** | | **~21 MB** |

---

## 🔬 Campos Principais por Base

### Eleitores (60+ atributos)
- **Demográficos:** nome, idade, gênero, cor_raca, escolaridade, renda
- **Geográficos:** regiao_administrativa, tipo_moradia
- **Políticos:** orientacao_politica, posicao_bolsonaro, interesse_politico
- **Psicográficos:** valores, preocupacoes, medos, estilo_decisao
- **Comportamentais:** fontes_informacao, susceptibilidade_desinformacao
- **Contexto:** historia_resumida, instrucao_comportamental

### Magistrados (40+ atributos)
- **Identificação:** nome, tribunal, cargo, data_posse
- **Formação:** graduacao, pos_graduacao, cursos_internacionais
- **Perfil:** perfil_filosofico, tendencia_jurisprudencial
- **Atuação:** casos_emblematicos, atuacao_destacada

### Consultores Lendários (50+ atributos)
- **Identidade:** nome, pais_origem, ano_nascimento, ano_morte
- **Expertise:** areas_expertise, metodologias, obras_principais
- **Personalidade:** arquetipo, abordagem_consultoria
- **Estilo:** citacoes_famosas, estilo_comunicacao

### Candidatos
- **Dados:** nome, partido, cargo_pretendido, foto
- **Histórico:** cargos_anteriores, votacoes_passadas
- **Campanha:** propostas, slogan, estrategia

---

## 🛠️ Análises Disponíveis

### 1. Análise Demográfica
```python
# Distribuição por região administrativa
df.groupby('regiao_administrativa').size()

# Pirâmide etária
df['faixa_etaria'] = pd.cut(df['idade'], bins=[18,25,35,45,55,65,100])
```

### 2. Análise Política
```python
# Orientação política por região
pd.crosstab(df['regiao_administrativa'], df['orientacao_politica'], normalize='index')

# Posição Bolsonaro vs Orientação
pd.crosstab(df['orientacao_politica'], df['posicao_bolsonaro'])
```

### 3. Correlações
```python
from scipy import stats

# Renda vs Orientação
stats.pearsonr(df['renda_num'], df['orient_num'])

# Idade vs Posição Bolsonaro
stats.pearsonr(df['idade'], df['bols_num'])
```

### 4. Segmentação Eleitoral
```python
# Clusters políticos
seg_esquerda = df[df['orientacao_politica'].isin(['esquerda', 'centro_esquerda'])]
seg_direita = df[df['orientacao_politica'].isin(['direita', 'centro_direita'])]
seg_centro = df[df['orientacao_politica'] == 'centro']
```

### 5. Análise de Preocupações
```python
from collections import Counter

# Top preocupações
preocs = [p for lista in df['preocupacoes'] for p in lista]
Counter(preocs).most_common(10)
```

### 6. Simulação de Campanha
```python
# Calcular probabilidade de voto
def prob_voto(eleitor, candidato):
    prob = 0.3  # base
    if match_orientacao(eleitor, candidato):
        prob += 0.2
    if match_preocupacoes(eleitor, candidato.propostas):
        prob += 0.15
    return min(0.95, prob)
```

### 7. Análise de Magistrados
```python
# Por tribunal
mag_df.groupby('tribunal').size()

# Tendência jurisprudencial
mag_df['tendencia_jurisprudencial'].value_counts()
```

### 8. Consultoria com Digital Twins
```python
# Consultar especialista em estratégia
consultor = consultores[consultores['arquetipo'] == 'estrategista'].iloc[0]
prompt = f"Como {consultor['nome']} analisaria esta situação?"
```

---

## 🔐 Autenticação API

```bash
# Login
curl -X POST "https://inteia.com.br/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"usuario":"professorigor","senha":"professorigor"}'

# Usar token
curl "https://inteia.com.br/api/v1/eleitores" \
  -H "Authorization: Bearer <TOKEN>"
```

---

## 📈 Exemplos de Uso

### Pesquisa por Região
```bash
# Eleitores do Gama
jq '.eleitores[] | select(.regiao_administrativa == "Gama")' eleitores_df_completo.json
```

### Filtro por Perfil
```bash
# Mulheres evangélicas de centro
jq '.eleitores[] | select(.genero == "feminino" and .religiao == "evangelica" and .orientacao_politica == "centro")' eleitores_df_completo.json
```

### Estatísticas Rápidas
```bash
# Contagem por orientação
jq '[.eleitores[].orientacao_politica] | group_by(.) | map({key: .[0], count: length})' eleitores_df_completo.json
```

---

## 🚀 Scripts de Análise

Ver pasta `/root/clawd/scripts/inteia/` para:
- `analise_demografica.py`
- `simulacao_campanha.py`
- `correlacoes.py`
- `segmentacao.py`

---

## 📝 Notas

- Dados são **eleitores sintéticos** gerados por IA
- Baseados em dados demográficos reais do DF (CODEPLAN)
- Atributos psicográficos são inferidos/simulados
- Usar para **simulação e pesquisa**, não como dados reais

---

## 🔄 Atualização

Para atualizar os dados:
```bash
cd /root/clawd && python3 scripts/inteia/atualizar_dados.py
```

---

*NEXO — INTEIA Data Hub*
*Última atualização: 2026-02-07 23:30*
