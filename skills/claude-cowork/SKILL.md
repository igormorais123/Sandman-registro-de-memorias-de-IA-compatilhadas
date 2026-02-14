---
name: claude-cowork
description: Operar o Claude Cowork via browser relay para automação de tarefas no PC do usuário. Use quando precisar organizar arquivos, criar documentos/planilhas/apresentações, analisar dados, acessar Gmail/Calendar/Drive, ou executar qualquer tarefa que o Cowork suporta no Windows/Mac do usuário.
---

# Claude Cowork Control

Skill para controlar o Claude Cowork via browser relay do OpenClaw.

## Pré-requisitos

1. **Browser relay ativo** — Usuário deve anexar aba do Chrome com OpenClaw extension
2. **Claude Desktop** instalado no PC do usuário
3. **Plano Pro ou superior** no Claude

## Verificar Conexão

Antes de operar, verificar se browser relay está conectado:

```
browser action=status profile=chrome
```

Se não conectado, instruir usuário:
> Abra claude.ai no Chrome e clique no ícone do OpenClaw na barra de extensões para anexar a aba.

## Fluxo de Operação

### 1. Navegar para Cowork

```
browser action=navigate targetUrl="https://claude.ai/cowork" profile=chrome
```

### 2. Capturar Estado Atual

```
browser action=snapshot profile=chrome
```

### 3. Interagir com Interface

Usar `browser action=act` com os refs do snapshot:

```
browser action=act profile=chrome request={"kind":"click","ref":"<ref>"}
browser action=act profile=chrome request={"kind":"type","ref":"<ref>","text":"<comando>"}
```

## Comandos Comuns

### Selecionar Pasta de Trabalho

1. Snapshot para encontrar botão "Select folder"
2. Click no botão
3. Aguardar diálogo do sistema (usuário seleciona pasta)

### Enviar Prompt ao Cowork

1. Snapshot para encontrar textarea de input
2. Type o comando desejado
3. Click no botão de enviar ou press Enter

### Aguardar Conclusão

1. Snapshot periódico para verificar status
2. Verificar se há indicador de "working" ou "completed"
3. Capturar resultado quando disponível

## Prompts Úteis para Cowork

### Organização de Arquivos
```
Organiza este diretório criando subpastas por tipo de arquivo.
Renomeie arquivos com data no início (YYYY-MM-DD).
Não exclua nada, apenas mova e renomeie.
```

### Criar Planilha de Dados
```
Analise todas as imagens nesta pasta.
Extraia os dados e crie uma planilha Excel com as informações encontradas.
Organize por data decrescente.
```

### Análise de Calendário
```
Revise meu calendário desta semana.
Me mostre um resumo com total de reuniões, dias mais ocupados e janelas livres.
Sugira otimizações.
```

### Processar Emails
```
Verifique meus emails não lidos.
Categorize por urgência e me dê um resumo dos mais importantes.
```

## Conectores Disponíveis

O Cowork pode acessar via conectores nativos:

| Conector | Comando de Ativação |
|----------|---------------------|
| Gmail | "Verifique meus emails" |
| Calendar | "Mostre minha agenda" |
| Drive | "Busque no meu Drive" |
| GitHub | "Acesse meu repositório" |

## Tratamento de Erros

### Browser não conectado
```
Erro: Chrome extension relay não conectado
Ação: Pedir usuário anexar aba
```

### Cowork não disponível
```
Erro: Elemento "Cowork" não encontrado
Ação: Verificar se usuário tem plano Pro+
```

### Permissão de pasta negada
```
Erro: Usuário não autorizou acesso à pasta
Ação: Instruir usuário a clicar "Permitir"
```

## Boas Práticas

1. **Sempre fazer snapshot** antes de interagir
2. **Aguardar carregamento** — usar timeoutMs se necessário
3. **Confirmar ações destrutivas** — perguntar antes de deletar
4. **Reportar progresso** — informar usuário sobre cada etapa
5. **Capturar resultado** — fazer snapshot final e extrair output

## Limitações

- Não consegue interagir com diálogos nativos do sistema (seleção de pasta)
- Depende do usuário aprovar permissões de pasta
- Limite semanal de tokens do plano Pro
- Latência entre comandos (aguardar processamento)
