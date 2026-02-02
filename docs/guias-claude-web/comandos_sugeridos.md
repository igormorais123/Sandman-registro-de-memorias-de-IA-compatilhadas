Alguns comandos sugeridos


# Bash commands - npm run build: Build the project - npm run typecheck: Run the typechecker 


# Code style - Use ES modules (import/export) syntax, not CommonJS (require) - Destructure imports when possible (eg. import { foo } from 'bar') 


# Workflow - Be sure to typecheck when you’re done making a series of code changes - Prefer running single tests, and not the whole test suite, for performance.








Excelente! Vou te passar os comandos exatos para usar no Claude Code. Execute na sequência.
________________


Passo 1: Criar o CLAUDE.md (arquivo de contexto do projeto)
No terminal do VS Code, com o Claude Code já aberto, digite:
Crie um arquivo CLAUDE.md na raiz do projeto seguindo as melhores práticas. Esse arquivo deve conter:


1. Visão geral do projeto (sistema de tradução acadêmica Brislin)
2. Estrutura de arquivos e o que cada um faz
3. Stack tecnológica (HTML, CSS, JavaScript, API Anthropic)
4. Convenções de código que devem ser seguidas
5. Comandos úteis para desenvolvimento
6. Regras específicas: sempre usar português brasileiro, manter compatibilidade com navegadores modernos, seguir método de retrotradução de Brislin
7. Contexto acadêmico: este sistema será apresentado no IACCP 2026


Analise o index.html existente para extrair informações relevantes.


Pressione Enter e aguarde. Quando ele mostrar o arquivo, digite y para confirmar a criação.
________________


Passo 2: Fazer o Claude Code analisar e testar o sistema
Analise o arquivo index.html completamente. Identifique:


1. Bugs ou erros de lógica no JavaScript
2. Problemas de tratamento de erro nas chamadas de API
3. Falhas de usabilidade na interface
4. Código duplicado que pode ser refatorado
5. Vulnerabilidades de segurança (especialmente no manuseio da API key)


Para cada problema, explique o que está errado e proponha a correção.


________________


Passo 3: Fazer o Claude Code executar e testar
Para o Claude Code "ver" o sistema funcionando, você precisa do Live Server rodando.
Em outro terminal (clique no + no painel de terminais do VS Code):
cd C:\Users\igorm\projetos\brislin-translator
npx live-server


Agora volte ao terminal do Claude Code e digite:
O sistema está rodando em http://127.0.0.1:8080. Crie um arquivo tests/test-cases.json com casos de teste para validar:


1. Tradução de frases simples
2. Tradução de termos técnicos de psicologia
3. Tradução de escalas psicométricas (itens de questionário)
4. Tratamento de texto vazio
5. Tratamento de API key inválida


Inclua o texto original em inglês e a tradução esperada em português para cada caso.


________________


Passo 4: Aplicar melhorias incrementais
Use estes comandos um de cada vez, testando após cada mudança:
Melhoria 1 - Tratamento de erros robusto:
Melhore o tratamento de erros no JavaScript. Adicione:
- Mensagens de erro claras em português para o usuário
- Retry automático em caso de falha de rede (máximo 3 tentativas)
- Timeout de 60 segundos por requisição
- Loading spinner durante o processamento


Melhoria 2 - Modularização:
Extraia o JavaScript do index.html para arquivos separados em src/js/:
- config.js (configurações e prompts)
- api.js (chamadas à API)
- agents.js (lógica dos agentes tradutor, retrotradutor, avaliador)
- ui.js (manipulação do DOM)
- main.js (ponto de entrada)


Mantenha o index.html funcionando com imports de módulos ES6.


Melhoria 3 - Interface mais profissional:
Melhore o CSS para uma aparência mais acadêmica e profissional:
- Paleta de cores: azul escuro (#1a365d), branco, cinza claro
- Tipografia: fonte serifada para textos, sans-serif para interface
- Cards com sombra suave para cada agente
- Indicadores visuais de progresso para cada etapa
- Design responsivo para apresentação em projetor


Melhoria 4 - Exportação de resultados:
Adicione botão para exportar o relatório completo de tradução em formato que possa ser colado no Word, incluindo:
- Texto original
- Tradução final
- Retrotradução
- Score de equivalência
- Histórico de iterações
- Data e hora da tradução


________________


Passo 5: Verificar mudanças
Após cada modificação, o Claude Code vai mostrar um diff (diferença) do que mudou.
* Digite y para aceitar
* Digite n para recusar
* Digite uma pergunta para pedir explicação
O Live Server atualiza automaticamente, então olhe o navegador para ver o resultado.
________________


Comandos de manutenção úteis
O que você quer
	Comando no Claude Code
	Ver estrutura atual
	Liste todos os arquivos do projeto e descreva cada um
	Desfazer última mudança
	Desfaça a última modificação que você fez
	Explicar código
	Explique como funciona a função X no arquivo Y
	Otimizar
	Otimize o arquivo X para melhor performance
	Documentar
	Adicione comentários explicativos no arquivo X
	________________


Resumo do fluxo
┌────────────────────────────────────────┐
│ Terminal 1: Claude Code                │
│ > claude                               │
│ (você conversa e pede mudanças)        │
├────────────────────────────────────────┤
│ Terminal 2: Live Server                │
│ > npx live-server                      │
│ (roda o sistema para você testar)      │
├────────────────────────────────────────┤
│ Navegador: http://127.0.0.1:8080       │
│ (visualiza as mudanças em tempo real)  │
└────────────────────────────────────────┘


________________


Comece agora
Execute este primeiro comando no Claude Code:
Crie o arquivo CLAUDE.md com contexto completo do projeto e depois analise o index.html listando os 5 problemas mais críticos que precisam ser corrigidos primeiro.


Me conta o que ele respondeu e seguimos a partir daí.
