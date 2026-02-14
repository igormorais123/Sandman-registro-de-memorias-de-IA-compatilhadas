# Claude Cowork — Guia Completo

> Sinopse estruturada do vídeo "Automatize seu trabalho com um agente de IA"
> Fonte: https://youtu.be/SiIczzJk6B0

---

## O QUE É O CLAUDE COWORK

O Cowork é uma **funcionalidade do Claude Desktop** que transforma o Claude em um **agente autônomo** instalado no seu computador. Diferente de um chatbot comum, ele pode:

- Ler, criar, editar e excluir arquivos
- Organizar diretórios automaticamente
- Criar planilhas, apresentações e relatórios
- Analisar imagens, notas fiscais, screenshots
- Acessar conectores externos (Gmail, Calendar, Drive, GitHub, Todoist, etc.)
- Usar plugins/skills para tarefas especializadas

**Origem:** Nasceu porque desenvolvedores que usavam o Claude Code começaram a pedir tarefas não relacionadas a código. A Anthropic percebeu a demanda e criou uma versão mais amigável para não-programadores.

---

## PRÉ-REQUISITOS

| Requisito | Detalhes |
|-----------|----------|
| **Sistema** | Windows ou macOS |
| **Plano** | Claude Pro ($20/mês) ou superior |
| **App** | Claude Desktop (baixar em claude.com/download) |

**Observação sobre limites:**
- Plano Pro tem limite semanal de uso
- Tarefas complexas com Opus 4.6 consomem mais (ex: organizar pasta = ~3% do limite)
- Para uso intensivo, considere o plano Max (~R$550/mês)

---

## PASSO A PASSO: INSTALAÇÃO

### 1. Download do Claude Desktop
```
1. Acesse: claude.com/download
2. Clique em "Download for Windows" ou "Download for Mac"
3. Execute o instalador
4. Faça login com sua conta Google/email
```

### 2. Upgrade para Plano Pro (se necessário)
```
1. Na tela inicial, clique em "Fazer Upgrade"
2. Escolha plano Pro ($20/mês) ou Max
3. Preencha dados de pagamento
4. Aguarde confirmação
```

### 3. Acessar o Cowork
```
1. Após login, olhe o menu lateral
2. Clique em "Cowork" (aparece após ter plano pago)
3. Aguarde configuração do espaço de trabalho
```

---

## PASSO A PASSO: CONFIGURAÇÃO INICIAL

### Configurar Atalhos (Opcional)
- **Ctrl+Alt+Espaço** → Abre barra rápida do Claude em qualquer lugar
- Pode habilitar ícone na barra de menu para acesso rápido

### Configurar Instruções Globais
```
1. Vá em Configurações > Cowork
2. Clique em "Editar" nas instruções globais
3. Escreva instruções que se aplicam a TODAS as sessões
   Exemplo: "Sempre responda em português brasileiro"
4. Salve
```

### Configurar Instruções por Pasta
```
1. Selecione uma pasta de trabalho
2. Crie um arquivo de instruções específicas
3. Defina comportamentos para aquele contexto
```

---

## PASSO A PASSO: USAR O COWORK

### Exemplo 1: Organizar Arquivos

```
1. Clique em "Selecionar Pasta"
2. Escolha a pasta bagunçada (ex: Downloads, Desktop)
3. Dê permissão quando solicitado ("Sempre permitir" ou "Permitir desta vez")
4. Digite o prompt:
   "Organiza esse diretório da melhor forma possível.
    Você tem liberdade para fazer o que quiser, desde que fique bom."
5. Clique em "Vamos lá"
6. Acompanhe as atividades no painel lateral
```

**O que ele faz:**
- Identifica tipos de arquivo
- Cria subpastas por categoria (Imagens, Documentos, Vídeos, etc.)
- Renomeia arquivos se necessário
- Move cada arquivo para a pasta correta

### Exemplo 2: Criar Planilha de Despesas

```
1. Selecione pasta com screenshots de notas fiscais
2. Digite:
   "Analise todas as imagens de notas fiscais nesta pasta.
    Crie uma planilha Excel com:
    - Data
    - Fornecedor
    - Valor
    - Categoria
    Ordene por data decrescente."
3. Aguarde processamento
4. Planilha será criada na pasta
```

### Exemplo 3: Planejar Semana com Calendário

```
1. Conecte o Google Calendar (ver seção Conectores)
2. Digite:
   "Revise meu calendário desta semana.
    Me mostre um resumo com:
    - Total de reuniões
    - Dias mais ocupados
    - Janelas de tempo livre
    Sugira como otimizar minha agenda."
3. Ele acessa o calendário e gera relatório
```

---

## CONECTORES (MCPs)

Conectores permitem que o Cowork acesse aplicativos externos.

### Conectores Nativos (Prontos)
| Conector | O que faz |
|----------|-----------|
| **Google Drive** | Busca e acessa arquivos no Drive |
| **Google Calendar** | Lê e gerencia eventos |
| **Gmail** | Lê e gerencia emails |
| **GitHub** | Acessa repositórios e código |

### Como Conectar
```
1. No chat, clique no ícone "+"
2. Selecione "Conectores"
3. Escolha o serviço (ex: Gmail)
4. Autorize com sua conta Google
5. Pronto! Pode pedir: "Verifique meus emails não lidos"
```

### Conectores Personalizados (MCPs)
```
1. Vá em Configurações > Conectores
2. Clique "Adicionar conector personalizado"
3. Cole a URL do MCP do serviço desejado
4. Configure autenticação se necessário
```

**Exemplos de MCPs disponíveis:**
- Todoist (gerenciador de tarefas)
- Notion
- Slack
- Qualquer serviço com API MCP

---

## SKILLS (HABILIDADES)

Skills são "pacotinhos prontos" que melhoram a capacidade do Cowork para tarefas específicas.

### Skills Nativos
| Skill | Função |
|-------|--------|
| **Documentos** | Criar/editar Word, PDF |
| **Apresentações** | Criar slides |
| **Planilhas** | Criar/analisar Excel |
| **Claude in Chrome** | Navegar na web |

### Como o Claude in Chrome Funciona
```
1. Instale a extensão "Claude in Chrome"
2. Quando pedir algo que requer web:
   - Cowork automaticamente abre o navegador
   - Acessa sites necessários
   - Extrai informações
   - Retorna para o chat com os dados
```

**Exemplo prático:**
```
Prompt: "Analise meu canal do YouTube e sugira 3 ideias de vídeos virais"

O que acontece:
1. Pede link do canal
2. Pergunta se tem acesso ao YouTube Studio
3. Pede screenshots de métricas
4. Usa Claude in Chrome para acessar o canal
5. Analisa dados de performance
6. Identifica padrões de sucesso
7. Gera documento com análise e sugestões
```

---

## BOAS PRÁTICAS

### Segurança
- **Selecione apenas pastas necessárias** — Cowork só acessa o que você permitir
- **Use "Permitir desta vez"** para tarefas sensíveis
- **Revise ações** antes de confirmar exclusões
- **Cuidado com prompt injection** — dados externos podem tentar manipular o agente

### Eficiência
- **Use modelo Sonnet** para tarefas simples (economiza limite)
- **Use modelo Opus 4.6** para tarefas complexas
- **Seja específico** no prompt para evitar retrabalho
- **Use instruções globais** para preferências recorrentes

### Prompts Eficientes
```
❌ Ruim: "Organiza isso"
✅ Bom: "Organiza este diretório criando subpastas por tipo de arquivo
        (Documentos, Imagens, Vídeos, Outros). Renomeie arquivos com
        data no início (YYYY-MM-DD). Não exclua nada."
```

---

## CASOS DE USO

### Para Criadores de Conteúdo
- Analisar métricas do YouTube/Instagram
- Gerar ideias de conteúdo baseadas em dados
- Criar roteiros e briefings
- Organizar materiais de produção

### Para Profissionais
- Criar relatórios a partir de dados
- Organizar emails e priorizar respostas
- Planejar semana com base no calendário
- Extrair dados de documentos escaneados

### Para Empresas
- Automatizar tarefas repetitivas
- Criar documentação padronizada
- Analisar planilhas de vendas/financeiro
- Gerar apresentações para reuniões

---

## COMPARAÇÃO: COWORK vs OPENCLAW

| Aspecto | Claude Cowork | OpenClaw (Clawd) |
|---------|---------------|------------------|
| **Interface** | GUI no Desktop | CLI/WhatsApp/Telegram |
| **Execução** | Local no PC | Servidor 24/7 |
| **Automação** | Manual (você inicia) | Proativa (cron jobs) |
| **Memória** | Por sessão | Persistente (arquivos) |
| **Custo** | $20-100/mês | API tokens |
| **Conectores** | MCPs nativos | Plugins customizados |

**Conclusão:** Cowork é ideal para tarefas pontuais no desktop. OpenClaw é melhor para automação contínua e proativa.

---

## RESUMO EXECUTIVO

1. **O que é:** Agente de IA instalado no seu PC que manipula arquivos e conecta com apps externos
2. **Preço:** A partir de $20/mês (plano Pro)
3. **Diferencial:** Acesso ao sistema de arquivos + conectores nativos + interface amigável
4. **Limitação:** Limite semanal de uso (considere Max para uso intensivo)
5. **Segurança:** Você controla quais pastas ele acessa

---

*Documento gerado em 2026-02-14 por Clawd 🌙*
*Fonte: Eli Rigobeli (YouTube)*
