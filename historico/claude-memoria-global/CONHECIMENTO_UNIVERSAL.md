# 🧬 Conhecimento Universal

> Aprendizados que transcendem projetos específicos
> Aplicáveis em qualquer contexto de desenvolvimento

---

## Princípios de Arquitetura

### Operações Críticas Devem Ser Atômicas e Reversíveis
**Origem**: Conserto-PC, sessão 2026-01-08
**Validado em**: Migração OneDrive → Google Drive
**Confiança**: Alta

Qualquer operação que modifique estado crítico do sistema (migrações, reorganizações de arquivos, alterações de configuração) deve:
1. Criar backup/snapshot antes
2. Ser executável em etapas verificáveis
3. Ter rollback definido
4. Documentar estado antes/depois

### Trabalho em Contexto Instável Requer Checkpoints Frequentes
**Origem**: Conserto-PC, múltiplas sessões
**Confiança**: Alta

Quando o ambiente é instável (PC reiniciando, internet caindo):
1. Salvar progresso a cada etapa significativa
2. Documentar em MD o que foi feito
3. Criar pontos de recuperação
4. Evitar operações longas não-interruptíveis

### Sistemas Multi-IA Requerem Hub Único de Escrita
**Origem**: Sistema-Memoria, sessão 2026-01-20
**Validado em**: Arquitetura Multi-IA
**Confiança**: Alta

Quando múltiplas IAs precisam compartilhar conhecimento:
1. Apenas UMA IA deve escrever (evita conflitos)
2. Outras IAs são consumidoras (read-only)
3. Hub central deve ser acessível por todas (Google Drive, GitHub)
4. Formato Markdown é universal entre IAs

### Custom Instructions Devem Ser Compactas (< 1500 chars)
**Origem**: Sistema-Memoria, sessão 2026-01-20
**Confiança**: Alta

Para Custom Instructions funcionarem em ChatGPT/Claude:
1. Manter cada arquivo < 1500 caracteres
2. Separar resumo (CORE/) de detalhes (sob demanda)
3. Usar referências a URLs em vez de conteúdo inline

### Eleitores/Agentes Sintéticos Requerem Validação de Consistência Interna
**Origem**: Sistema Eleitoral DF (C:\Agentes), sessão 2026-01-16
**Validado em**: Múltiplas iterações de geração
**Confiança**: Alta

Ao gerar perfis sintéticos com múltiplos atributos (~60+):
1. Validar consistência entre dados demográficos e história narrativa
2. Verificar coerência temporal (idade vs aposentadoria vs tempo de trabalho)
3. Cruzar atributos relacionados (estado civil na história vs no perfil)
4. Comparar distribuição estatística com dados reais (TSE, IBGE)

### Deploy Iterativo com Testes a Cada Commit
**Origem**: Sistema Eleitoral DF, múltiplas sessões
**Confiança**: Alta

Para evitar acúmulo de problemas:
1. Rodar lint/typecheck/test antes de cada commit
2. Fazer commits atômicos e pequenos
3. Testar localmente antes de deploy
4. Verificar ambiente de produção após cada deploy

### Credenciais/Tokens Nunca no Chat
**Origem**: Histórico Claude Code, sessão 2026-01-15
**Confiança**: Crítica

Nunca colar tokens, API keys ou senhas no chat:
1. Usar variáveis de ambiente (.env.local)
2. Configurar secrets no provedor (Vercel, Render)
3. Remover imediatamente se exposto acidentalmente
4. Regenerar token após exposição

### Documentação Jurídica para IA Requer Múltiplas Camadas de Índices
**Origem**: Reconvencao-Igor-Melissa, sessão 2026-01-20
**Validado em**: Organização de 50+ documentos legais
**Confiança**: Alta

Para IAs navegarem eficientemente em documentação jurídica volumosa:
1. CLAUDE.md → Contexto do caso (quem, o quê, quando)
2. MAPA_GERAL.md → GPS de TODOS os arquivos
3. ACAO_[NOME].md → Documento específico para tarefa
4. 00_INDICE_PASTA.md → Índice em cada subpasta
5. 00_MAPA_GPS.md → GPS da subpasta (se complexa)

Benefícios:
- IA decide profundidade de leitura
- Evita carregar contexto desnecessário
- Navegação por intenção ("preciso de X → vá para Y")

### Tabelas GPS São Mais Eficientes que Listas para Navegação de IA
**Origem**: Reconvencao-Igor-Melissa, sessão 2026-01-20
**Confiança**: Alta

Formato de tabela "Preciso de... → Vá para..." supera listas simples:
```markdown
| Preciso de... | Vá para... |
|---------------|------------|
| Contexto do caso | CLAUDE.md |
| Provas de nexo causal | CONVERSAS_RAG/04_*.md |
| Dados estatísticos | ANALISE_QUANTITATIVA/ |
```

Por que funciona:
- IA entende intenção, não só localização
- Reduz tokens gastos em navegação
- Permite saltos diretos ao objetivo

<!-- ADICIONAR_PRINCIPIO_AQUI -->

---

## Soluções Genéricas

### Diagnóstico de Rede WiFi no Windows
**Problema genérico**: Internet instável, quedas frequentes
**Solução padrão**:
```powershell
# Verificar status do adaptador
Get-NetAdapter | Select-Object Name,Status,LinkSpeed

# Verificar força do sinal
netsh wlan show interfaces

# Desabilitar economia de energia do adaptador
# Via Gerenciador de Dispositivos > Propriedades > Gerenciamento de Energia
# Desmarcar "Permitir que o computador desligue este dispositivo"

# Reduzir agressividade de roaming
# Propriedades > Avançado > Roaming Aggressiveness > Lowest
```
**Quando usar**: Quedas de WiFi com uso intensivo
**Quando NÃO usar**: Problemas de hardware do roteador

### Análise de Espaço em Disco
**Problema genérico**: Disco cheio, identificar o que ocupa espaço
**Solução padrão**:
```powershell
# Espaço livre
Get-PSDrive C | Select-Object Used,Free

# Maiores pastas (usar WinDirStat para análise visual)
# Locais comuns de acúmulo:
# - %TEMP% (arquivos temporários)
# - C:\Users\[user]\AppData\Local\Temp
# - C:\Windows\Temp
# - Downloads não limpos
```
**Quando usar**: Alertas de espaço baixo
**Quando NÃO usar**: SSDs com TRIM ativo geralmente não precisam defrag

### Recuperação de Contexto Após Reinício
**Problema genérico**: PC reiniciou, precisa continuar trabalho
**Solução padrão**:
```
1. Verificar ~/.claude/history.jsonl para últimos comandos
2. Verificar ~/.claude/todos/ para tarefas pendentes
3. Buscar arquivos modificados recentemente:
   Get-ChildItem -Recurse | Where-Object {$_.LastWriteTime -gt (Get-Date).AddHours(-2)}
4. Ler MDs de contexto/histórico criados
```
**Quando usar**: Após crashes ou reinícios inesperados
**Quando NÃO usar**: N/A

### Automação com Task Scheduler Windows
**Problema genérico**: Executar tarefas automaticamente ao ligar PC
**Solução padrão**:
```powershell
# Criar tarefa via XML (mais controle)
schtasks /create /xml "tarefa.xml" /tn "NomeDaTarefa" /f

# Estrutura do XML para LogonTrigger:
# <LogonTrigger>
#   <Enabled>true</Enabled>
#   <Delay>PT2M</Delay>  <!-- 2 minutos após login -->
#   <UserId>USUARIO</UserId>
# </LogonTrigger>

# Verificar se tarefa existe
schtasks /query /tn "NomeDaTarefa"

# Executar manualmente
schtasks /run /tn "NomeDaTarefa"
```
**Quando usar**: Backups, consolidações, syncs periódicos
**Quando NÃO usar**: Tarefas que precisam rodar 24/7 (usar serviço)

### Stack Next.js + FastAPI + PostgreSQL
**Problema genérico**: Aplicação fullstack moderna com Python backend
**Solução padrão**:
```yaml
frontend:
  framework: Next.js 14+
  deploy: Vercel
  auth: NextAuth.js + Google OAuth
  state: IndexedDB para cache local

backend:
  framework: FastAPI
  deploy: Render
  orm: SQLAlchemy + Pydantic v2
  config: pydantic-settings (não BaseSettings diretamente)

database:
  dev: SQLite ou JSON files
  prod: PostgreSQL (Render managed)

devops:
  ci: GitHub Actions
  local: Docker Compose
```
**Quando usar**: Projetos SaaS com Python ML/IA
**Quando NÃO usar**: Projetos simples (apenas frontend estático)

### Validação de Amostra Estatística
**Problema genérico**: Verificar se amostra representa população
**Solução padrão**:
```python
# Índice de Conformidade
def calcular_conformidade(amostra: dict, referencia: dict) -> float:
    """Calcula quão bem a amostra representa a referência."""
    desvios = []
    for variavel, valor_amostra in amostra.items():
        valor_ref = referencia.get(variavel, valor_amostra)
        desvio = abs(valor_amostra - valor_ref)
        desvios.append(desvio)
    return 100 - sum(desvios) / len(desvios)

# Meta: >= 90% de conformidade
```
**Quando usar**: Geração de dados sintéticos, pesquisas
**Quando NÃO usar**: Dados já validados

### Análise Quantitativa de Conversas WhatsApp (Brasil)
**Problema genérico**: Extrair métricas de conversas WhatsApp exportadas
**Solução padrão**:
```python
import re
from datetime import datetime

# Regex para formato brasileiro (DD/MM/YYYY HH:MM)
WHATSAPP_BR_PATTERN = r'^(\d{2}/\d{2}/\d{4}) (\d{2}:\d{2}) - ([^:]+): (.+)$'

def parse_whatsapp_msg(line: str) -> dict | None:
    """Parse uma linha de conversa WhatsApp BR."""
    match = re.match(WHATSAPP_BR_PATTERN, line)
    if match:
        return {
            'data': match.group(1),
            'hora': match.group(2),
            'remetente': match.group(3),
            'mensagem': match.group(4)
        }
    return None

# Métricas úteis para casos jurídicos:
# - Contagem de mensagens por pessoa
# - Tempo médio de resposta
# - Pedidos de informação ignorados
# - Indicadores de comportamento (padrões de linguagem)
# - Elementos de obstrução por categoria
```
**Quando usar**: Análise de conversas para casos jurídicos, análise de comunicação
**Quando NÃO usar**: Conversas em outros idiomas/formatos de data

<!-- ADICIONAR_SOLUCAO_AQUI -->

---

## Heurísticas de Debugging

1. **Verificar Event Viewer primeiro para crashes do Windows**
   - Origem: Conserto-PC
   - Taxa de sucesso estimada: 70%
   - Comando: `eventvwr.msc` ou `Get-EventLog -LogName System -EntryType Error -Newest 20`

2. **Problemas de rede? Verificar economia de energia do adaptador**
   - Origem: Conserto-PC
   - Taxa de sucesso estimada: 60%
   - Windows frequentemente desliga adaptadores para economizar energia

3. **Pasta sumiu? Verificar se está em cloud storage não sincronizado**
   - Origem: Migração OneDrive
   - Taxa de sucesso estimada: 80%
   - OneDrive/Google Drive podem mover pastas para locais inesperados

4. **PC reiniciando? Verificar temperatura e drivers de GPU**
   - Origem: Conserto-PC
   - Taxa de sucesso estimada: 50%
   - GPUs NVIDIA e drivers AMD são causas comuns

5. **Progresso/Percentual > 100%? Verificar lógica de cálculo**
   - Origem: C-Agentes (Bug 201%)
   - Taxa de sucesso estimada: 90%
   - Sempre clampar valores calculados entre 0-100%

6. **Dados sintéticos inconsistentes? Validar coerência interna**
   - Origem: C-Agentes
   - Taxa de sucesso estimada: 85%
   - Cruzar atributos demográficos com narrativas geradas

7. **Mapeamento frontend/backend diferente? Normalizar valores**
   - Origem: C-Agentes (moto vs motocicleta)
   - Taxa de sucesso estimada: 95%
   - Usar enums ou constantes compartilhadas entre camadas

<!-- ADICIONAR_HEURISTICA_AQUI -->

---

## Integrações e APIs

### Google Drive Desktop
**Pegadinhas conhecidas**:
- Migração de OneDrive não é automática - requer cópia manual
- Caminho padrão: `G:\Meu Drive\`
- Sincronização inicial consome muita banda
- Pastas especiais (Desktop, Documents) precisam reconfiguração manual

**Configuração ideal**:
```
1. NÃO desinstalar cloud storage anterior antes de migrar
2. Copiar arquivos primeiro, verificar, depois desinstalar antigo
3. Configurar pastas especiais após sincronização completa
```

### clasp (Google Apps Script CLI)
**Pegadinhas conhecidas**:
- Requer `clasp login` antes de usar
- API do Apps Script deve estar ativada no projeto GCP
- Projetos vinculados precisam de `.clasp.json`

**Configuração ideal**:
```bash
npm install -g @google/clasp
clasp login
# Ativar API em: https://script.google.com/home/usersettings
```

### Intel Wireless Drivers
**Pegadinhas conhecidas**:
- Windows Update nem sempre tem versão mais recente
- Intel Driver & Support Assistant é mais confiável
- Drivers genéricos do Windows podem causar instabilidade

**Configuração ideal**:
```
1. Baixar Intel Driver & Support Assistant
2. Usar drivers específicos da Intel, não genéricos
3. Desabilitar economia de energia após atualização
```

### Vercel + Render Deploy
**Pegadinhas conhecidas**:
- Vercel free tier tem limite de deploys (429 rate limit)
- Render free tier suspende após inatividade
- Environment variables devem estar em ambos separadamente
- CORS deve permitir domínios de ambos

**Configuração ideal**:
```yaml
vercel:
  env_vars:
    - NEXT_PUBLIC_API_URL  # URL do Render
    - NEXTAUTH_SECRET
    - GOOGLE_CLIENT_ID
    - GOOGLE_CLIENT_SECRET
  build_command: npm run build
  output_directory: .next

render:
  env_vars:
    - DATABASE_URL
    - ANTHROPIC_API_KEY
    - FRONTEND_URL  # URL do Vercel
  build_command: pip install -r requirements.txt
  start_command: uvicorn app.main:app --host 0.0.0.0
```

### Pydantic v2 Migration
**Pegadinhas conhecidas**:
- `BaseSettings` agora vem de `pydantic_settings`
- `class Config` substituída por `model_config = SettingsConfigDict(...)`
- Validadores usam `@field_validator` em vez de `@validator`
- Deprecation warnings se usar padrões antigos

**Configuração ideal**:
```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    api_key: str
    database_url: str
```

### Google OAuth com NextAuth
**Pegadinhas conhecidas**:
- Callback URL deve estar configurado no Google Console
- URL diferente para dev (localhost) e prod
- NEXTAUTH_URL deve corresponder ao ambiente
- Scopes mínimos: email, profile, openid

**Configuração ideal**:
```
Google Console > Credentials > OAuth 2.0:
  Authorized redirect URIs:
    - http://localhost:3000/api/auth/callback/google
    - https://seuapp.vercel.app/api/auth/callback/google

.env.local:
  NEXTAUTH_URL=http://localhost:3000 (ou URL prod)
  NEXTAUTH_SECRET=<gerado com openssl rand -base64 32>
```

<!-- ADICIONAR_INTEGRACAO_AQUI -->

---

## Configurações de Sistema Recomendadas

### Windows 11 para Desenvolvimento
```yaml
energia:
  plano: Alto Desempenho
  hibernar_disco: Nunca
  suspender: Nunca (se estável)

rede:
  adaptador_wifi:
    economia_energia: Desabilitado
    roaming_aggressiveness: Lowest (em ambiente fixo)

disco:
  indexacao: Apenas em pastas necessárias
  desfragmentacao: Automático para HDD, desabilitado para SSD

desenvolvimento:
  wsl2: Habilitado se usar Linux
  hyper_v: Conforme necessidade
  developer_mode: Habilitado
```

---

## Histórico de Contribuições

| Data | Projeto Origem | Conhecimento Adicionado | Seção |
|------|----------------|-------------------------|-------|
| 2026-01-19 | Conserto-PC | Diagnóstico de rede WiFi | Soluções |
| 2026-01-19 | Conserto-PC | Recuperação após reinício | Soluções |
| 2026-01-19 | Migração OneDrive | Princípio de operações atômicas | Princípios |
| 2026-01-19 | Conserto-PC | Heurísticas de debugging Windows | Heurísticas |
| 2026-01-19 | SIEC | Configuração clasp | Integrações |
| 2026-01-20 | Sistema-Memoria | Hub único de escrita Multi-IA | Princípios |
| 2026-01-20 | Sistema-Memoria | Custom Instructions compactas | Princípios |
| 2026-01-20 | Sistema-Memoria | Automação Task Scheduler | Soluções |
| 2026-01-20 | Ciclo Sono | Validação de agentes sintéticos | Princípios |
| 2026-01-20 | Ciclo Sono | Deploy iterativo com testes | Princípios |
| 2026-01-20 | Ciclo Sono | Credenciais nunca no chat | Princípios |
| 2026-01-20 | Ciclo Sono | Stack Next.js + FastAPI | Soluções |
| 2026-01-20 | Ciclo Sono | Validação amostra estatística | Soluções |
| 2026-01-20 | Ciclo Sono | Vercel + Render deploy | Integrações |
| 2026-01-20 | Ciclo Sono | Pydantic v2 migration | Integrações |
| 2026-01-20 | Ciclo Sono | Google OAuth NextAuth | Integrações |
| 2026-01-20 | Reconvencao | Documentação jurídica multi-camadas | Princípios |
| 2026-01-20 | Reconvencao | Tabelas GPS para navegação IA | Princípios |
| 2026-01-20 | Reconvencao | Parser WhatsApp BR | Soluções |
| 2026-01-20 | C-Agentes | Heurística clampar valores 0-100% | Heurísticas |
| 2026-01-20 | C-Agentes | Validação coerência dados sintéticos | Heurísticas |
| 2026-01-20 | C-Agentes | Normalização mapeamento frontend/backend | Heurísticas |
| 2026-01-20 | Extração Históricos | Consolidação 4 projetos analisados | Cross-projeto |
<!-- HISTORICO_CONTRIBUICOES -->
