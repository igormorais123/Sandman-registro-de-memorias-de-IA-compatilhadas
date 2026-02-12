# Mermaid Padrao Colmeia

## Objetivo

Padronizar mapas de navegacao documental com Mermaid para leitura rapida por humano e IA.

## Regras

1. Usar `flowchart TD` para mapas estruturais.
2. Usar `flowchart LR` para fluxo de navegacao.
3. Nomear cada diagrama com escopo claro (`Mapa Global`, `Mapa da Pasta X`).
4. Usar subgraphs por dominio quando houver mais de 8 nos.
5. Evitar excesso de texto por no.

## Estrutura recomendada

1. Um mapa global por repositorio.
2. Um mapa local (`00_MAPA_GPS.md`) por pasta critica.
3. Um indice completo de arquivos para rastreabilidade.

## Check de qualidade

1. Todos os caminhos de arquivo existem.
2. Nao usar caminhos com `\`, padrao `/`.
3. Rotas rapidas devem incluir links para os arquivos mais acionados.

