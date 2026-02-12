---
name: colmeia-agentes-research
description: Pesquisar e operar a base de agentes simulados em C:/Agentes, incluindo consultas a Helena, analises quantitativas e qualitativas, e uso dos agentes via Colmeia em inteia.com.br/colmeia. Use quando o usuario pedir pesquisa eleitoral simulada, consultoria com perfis de agentes, duvidas sobre segmentos (eleitores, parlamentares, magistrados, gestores, consultores, candidatos), ou cruzamento de insights por persona.
---

# Colmeia Agentes Research

## Objetivo

Permitir que a Colmeia use os agentes simulados como laboratorio de pesquisa e consultoria, com fluxo padronizado para:

1. descoberta da estrutura em `C:/Agentes`;
2. consulta direta de personas (incluindo Helena);
3. pesquisa quantitativa e qualitativa;
4. consolidacao de respostas para tomada de decisao.

## Regra de Provider (obrigatoria)

1. Account-first: usar tokens das contas assinadas (Claude/ChatGPT/Gemini) por padrao.
2. API-exception: usar API so quando for inevitavel (execucao server-side sem sessao de conta aberta).
3. Toda chamada em modo API deve registrar justificativa.

## Workflow Decisorio

1. Entender pergunta de negocio:
- qual publico?
- qual tipo de resposta? (quanti, quali, consultoria, duvida pontual)
- nivel de confianca esperado?

2. Descobrir base local:
- executar `scripts/index_agentes.ps1`.
- se necessario, executar `scripts/query_agentes.ps1` para tema/persona.

3. Identificar Helena:
- buscar nome `Helena` e aliases.
- registrar qual fonte foi usada para a resposta.

4. Selecionar metodo:
- Quantitativo: contagem por segmento, frequencia de temas, distribuicoes.
- Qualitativo: motivos, padroes narrativos, objecoes, linguagem dominante.
- Consultoria: recomendar acao com base em convergencia quanti+quali.

5. Consolidar entrega:
- resumo executivo;
- evidencias (arquivos/fontes pesquisadas);
- incertezas explicitas;
- recomendacao objetiva.

## Modos de Pesquisa

## 1) Pesquisa Quantitativa

Aplicar quando a pergunta envolve volume, distribuicao, ranking ou comparacao.

Checklist:

1. Definir universo (quais segmentos e quais arquivos).
2. Definir janela temporal (se existir metadata de data).
3. Definir metricas: frequencia, proporcao, tendencia, corte regional/tematico.
4. Reportar base amostral usada.

## 2) Pesquisa Qualitativa

Aplicar quando a pergunta envolve motivacao, percepcao, argumento, risco e narrativa.

Checklist:

1. Identificar categorias de sentido.
2. Extrair evidencias representativas por categoria.
3. Marcar contradicoes internas e sinais fracos.
4. Entregar sintese com implicacoes praticas.

## 3) Consulta Direta (Helena e outras personas)

Aplicar quando o usuario pedir:

1. "Consultar Helena";
2. "Perguntar para os agentes";
3. "Quero a visao dos parlamentares/magistrados/consultores/candidatos".

Procedimento:

1. Resolver identidade da persona (nome/alias/pasta).
2. Coletar historico e posicionamento recente.
3. Responder com "voz da persona" e "analise da Colmeia" separadas.
4. Informar incerteza quando faltar contexto.

## Integracao com Colmeia/INTEIA

1. Frontend alvo: `https://inteia.com.br/colmeia`
2. API alvo: `https://api.inteia.com.br/colmeia`
3. Nao alterar raiz de `https://inteia.com.br`

## Recursos da Skill

1. `scripts/index_agentes.ps1`:
- inventario de estrutura e tipos de arquivo em `C:/Agentes`.

2. `scripts/query_agentes.ps1`:
- busca por tema/persona em arquivos de texto estruturados e semiestruturados.

3. `references/modelo_entrega_pesquisa.md`:
- formato padrao de entrega para quanti/quali/consultoria.

4. `references/governanca_operacao.md`:
- limites, qualidade e trilha de auditoria.

