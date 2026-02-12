# Governanca de Operacao - Agentes Research

## 1. Regras de seguranca

1. Nao alterar arquivos em `C:/Agentes` durante pesquisa, apenas leitura.
2. Se o ambiente bloquear acesso fora do workspace, solicitar permissao de execucao.
3. Dados sensiveis devem ser minimizados na resposta final.

## 2. Regras de qualidade

1. Separar fato, inferencia e hipotese.
2. Nunca afirmar "consenso" sem base amostral explicita.
3. Incluir trilha de fontes (arquivos e linhas quando possivel).

## 3. Regras de provider

1. Conta Pro primeiro.
2. API por excecao com justificativa.
3. Registrar em log o modo de execucao (`account` ou `api`).

## 4. Regras para Helena/Elena

1. Buscar variacoes de nome antes de concluir ausencia.
2. Se houver mais de uma Helena/Elena, desambiguar por contexto.
3. Declarar claramente qual registro foi usado.
