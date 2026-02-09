# GUIA DE BUSCA RÁPIDA - INDICADORES NPD/ASPD
## Padrões de Regex Otimizados para Análise Comportamental
## Data: 20/01/2026

---

## OBJETIVO

Este documento fornece padrões de busca prontos para identificar rapidamente indicadores de Transtorno de Personalidade Narcisista (NPD) e traços Antissociais (ASPD) nas conversas.

---

## 1. PADRÕES DE BUSCA POR CATEGORIA

### 1.1 GASLIGHTING (Negação da Realidade)
```regex
jamais|nunca fiz|nao fiz|infundad|mentira|inventando|nao disse|nao foi assim
```
**O que encontra**: Negações de comportamento documentado

---

### 1.2 FALTA DE EMPATIA
```regex
ferias|descanso|tranquil|paz|nao quero falar|nao te atinge|nao me afeta
```
**O que encontra**: Priorização de si enquanto outro sofre

---

### 1.3 INVERSÃO VÍTIMA-AGRESSOR
```regex
delegacia|ameac|agressiv|importunar|assustando|me sujeitar
```
**O que encontra**: Thalia se posicionando como vítima sendo agressora

---

### 1.4 MANIPULAÇÃO
```regex
ela.*decidir|ela.*quer|nao tenho como|forcada|resistencia
```
**O que encontra**: Uso da criança como escudo

---

### 1.5 CONTROLE POR OMISSÃO
```regex
endereco|data.*viagem|nao.*informou|nao.*avisou|sem falar comigo
```
**O que encontra**: Informações sonegadas

---

### 1.6 AUSÊNCIA DE REMORSO
```regex
desculp|sinto muito|perdao|lamento|reconheco
```
**O que encontra**: AUSÊNCIA destas palavras em mensagens de Thalia = indicador

---

### 1.7 PROJEÇÃO
```regex
vc.*é|voce.*esta|vc.*tem|seu.*problema|sua.*culpa
```
**O que encontra**: Thalia acusando Igor do que ela faz

---

### 1.8 AUTOLESÃO/DANO A MELISSA
```regex
autolez|machuc|bate|agride|se apertar|cort
```
**O que encontra**: Indicadores de que Melissa se machuca por causa de Thalia

---

## 2. BUSCAS COMBINADAS PODEROSAS

### 2.1 Contradição Discurso x Ação
```regex
Thalia:.*(interesse|melhor|bem).*(pai|relacao|melissa)
```
Depois compare com datas de descumprimento (15/08, 22/08, 30/08)

---

### 2.2 Frieza Durante Sofrimento de Igor
```regex
Thalia:.*(tranquil|ferias|descanso|paz)
```
Compare com datas de adoecimento de Igor (02/09, 08/09, 14/10)

---

### 2.3 Ameaças de Thalia
```regex
Thalia:.*(delegacia|advogada|processo|vou parar)
```

---

## 3. ARQUIVOS PRIORITÁRIOS POR TIPO DE BUSCA

| Tipo de Busca | Arquivos Prioritários |
|---------------|----------------------|
| Gaslighting | 03_23-31ago2025, 04_01-07set2025 |
| Falta de empatia | 04_01-07set2025 (viagem Jeri) |
| Inversão vítima | 04_01-07set2025 (delegacia) |
| Manipulação | 01_14-16ago2025, 03_23-31ago2025 |
| Autolesão Melissa | 07_CONVERSAS_WHATSAPP (linha 1511) |
| Histórico | THALIA_10 (divórcio 2022) |

---

## 4. CITAÇÕES-CHAVE PRONTAS PARA COPIAR

### 4.1 GASLIGHTING
> "Jamais pressionei a melissa para NÃO ir para a sua casa ou a ter qualquer reação de resistência a vc e sua família. Jamais."
> -- Thalia, 29/08/2025 (03_23-31ago2025, linha 99)

**CONTRADIÇÃO**: Áudio mostra ela forçando Melissa.

---

### 4.2 FALTA DE EMPATIA
> "Nestes dias fora eu não quero falar disso. São minhas ferias e meus dias com ela de descanso e quero priorizar isso."
> -- Thalia, 01/09/2025 (04_01-07set2025, linha 50)

**CONTEXTO**: Igor voltou da psiquiatra com nova medicação.

---

### 4.3 INVERSÃO VÍTIMA-AGRESSOR
> "Se continuar a me importunar e ameaçar com essas mensagens agressivas, quem vai à delegacia da mulher sou eu."
> -- Thalia, 04/09/2025 (04_01-07set2025, linha 116)

**CONTEXTO**: Thalia é quem descumpriu acordo, mas ameaça Igor.

---

### 4.4 MANIPULAÇÃO COM CRIANÇA
> "não fui eu quem coloquei resistência em levá-la para a sua casa. Foi ela quem não quis ir"
> -- Thalia, 29/08/2025 (03_23-31ago2025, linha 101)

**REALIDADE**: Criança de 7 anos não decide agenda judicial.

---

### 4.5 AUTOLESÃO POR CAUSA DE THALIA ⭐⭐⭐⭐⭐
> "A melissa se autolezionou e eu tenho o depoimento da psicologa dela. Pq VC THALIA falou algo para melidsa que ela nao gostou. Ela nunca fez isso comigo."
> -- Igor, 09/10/2025 (07_CONVERSAS_WHATSAPP, linha 1511)

**RELEVÂNCIA MÁXIMA**: Prova de dano a Melissa causado por Thalia.

---

### 4.6 CONTRADIÇÃO DISCURSO x AÇÃO
> "Acho que estamos indo bem como pais."
> -- Thalia, 29/05/2025

**77 DIAS DEPOIS**: Iniciou descumprimentos sistemáticos.

---

### 4.7 FRIEZA EMOCIONAL
> "O seu é frio e so pensa em si. Isso nao te atinge."
> -- Igor, 28/09/2025 (07_CONVERSAS, linha 1194)

**CONTEXTO**: Igor identificou traço narcisista.

---

## 5. FLUXO DE TRABALHO OTIMIZADO

### Passo 1: Identificar Categoria
Qual tipo de indicador NPD/ASPD você procura?
- Gaslighting → Seção 1.1
- Falta de empatia → Seção 1.2
- Inversão → Seção 1.3
- etc.

### Passo 2: Usar Regex Pronto
Copie o padrão da seção correspondente.

### Passo 3: Buscar nos Arquivos Prioritários
Use a tabela da Seção 3.

### Passo 4: Citar com Fonte
Use o formato: `"Citação" -- Autor, Data (Arquivo, linha X)`

---

## 6. TAGS

`#guia_busca` `#NPD` `#ASPD` `#regex` `#metodologia` `#citacoes_prontas`

---

*Documento criado em 20/01/2026*
*Objetivo: Acelerar futuras buscas por indicadores comportamentais*
