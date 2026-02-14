# 🏛️ ARSENAL HELENA - Ferramentas da Deusa da INTEIA

> **Documentação prática para dominar automação**  
> Última atualização: 2026-02-14

---

## 📑 Índice

1. [MCPs Essenciais](#1-mcps-essenciais)
2. [Skills Claude Code](#2-skills-claude-code)
3. [Integrações Cowork](#3-integrações-cowork)
4. [Ferramentas de Linha de Comando](#4-ferramentas-de-linha-de-comando)
5. [APIs Úteis](#5-apis-úteis)

---

## 1. MCPs ESSENCIAIS

> Model Context Protocol - servidores que expandem as capacidades do Claude

### 1.1 Filesystem MCP

**Acesso a arquivos locais**

```bash
# Instalação
npm install -g @modelcontextprotocol/server-filesystem

# Ou via npx (sem instalar)
npx @modelcontextprotocol/server-filesystem /caminho/permitido
```

**Configuração (claude_desktop_config.json):**
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/home/usuario/documentos",
        "/home/usuario/projetos"
      ]
    }
  }
}
```

**Exemplo de uso:**
```
"Leia o arquivo /home/usuario/documentos/contrato.txt"
"Liste todos os PDFs em /projetos"
"Crie um arquivo relatorio.md com o conteúdo X"
```

---

### 1.2 Google Drive MCP

**Acesso ao Drive, Docs e Sheets**

```bash
# Instalação
npm install -g @anthropic/mcp-server-gdrive
```

**Configuração:**
```json
{
  "mcpServers": {
    "gdrive": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-gdrive"],
      "env": {
        "GOOGLE_CLIENT_ID": "seu-client-id.apps.googleusercontent.com",
        "GOOGLE_CLIENT_SECRET": "seu-client-secret",
        "GOOGLE_REDIRECT_URI": "http://localhost:3000/oauth/callback"
      }
    }
  }
}
```

**Setup OAuth (uma vez):**
1. Acesse [Google Cloud Console](https://console.cloud.google.com)
2. Crie projeto → Ative Google Drive API
3. Credenciais → Criar ID do cliente OAuth 2.0
4. Tipo: Aplicativo para computador
5. Copie Client ID e Secret

**Exemplo de uso:**
```
"Liste meus arquivos recentes do Drive"
"Abra o documento 'Proposta Comercial'"
"Crie uma planilha com dados de vendas"
"Exporte o Doc X como PDF"
```

---

### 1.3 Gmail MCP

**Leitura e envio de emails**

```bash
# Instalação
npm install -g @anthropic/mcp-server-gmail
```

**Configuração:**
```json
{
  "mcpServers": {
    "gmail": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-gmail"],
      "env": {
        "GOOGLE_CLIENT_ID": "seu-client-id",
        "GOOGLE_CLIENT_SECRET": "seu-client-secret"
      }
    }
  }
}
```

**Permissões necessárias (scopes):**
- `gmail.readonly` - ler emails
- `gmail.send` - enviar emails
- `gmail.modify` - marcar como lido, arquivar

**Exemplo de uso:**
```
"Mostre meus 10 emails não lidos"
"Busque emails do cliente@empresa.com"
"Envie email para joao@teste.com com assunto 'Reunião'"
"Responda o último email do financeiro"
```

---

### 1.4 Google Calendar MCP

**Gerenciamento de agenda**

```bash
# Instalação
npm install -g @anthropic/mcp-server-gcalendar
```

**Configuração:**
```json
{
  "mcpServers": {
    "gcalendar": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-gcalendar"],
      "env": {
        "GOOGLE_CLIENT_ID": "seu-client-id",
        "GOOGLE_CLIENT_SECRET": "seu-client-secret"
      }
    }
  }
}
```

**Exemplo de uso:**
```
"Quais são meus compromissos de amanhã?"
"Agende reunião com João às 15h na sexta"
"Cancele o evento 'Almoço' de hoje"
"Mostre minha semana"
```

---

### 1.5 Browser Automation MCP (Playwright)

**Automação de navegador**

```bash
# Instalação
npm install -g @anthropic/mcp-server-playwright

# Instalar navegadores do Playwright
npx playwright install
```

**Configuração:**
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-playwright"],
      "env": {
        "PLAYWRIGHT_HEADLESS": "true"
      }
    }
  }
}
```

**Exemplo de uso:**
```
"Abra google.com e pesquise 'INTEIA advogados'"
"Faça screenshot da página inicial do site X"
"Preencha o formulário de contato com meus dados"
"Extraia todos os links da página"
```

---

### 1.6 Puppeteer MCP (Alternativa)

```bash
# Instalação
npm install -g @anthropic/mcp-server-puppeteer
```

**Configuração:**
```json
{
  "mcpServers": {
    "puppeteer": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-puppeteer"],
      "env": {
        "PUPPETEER_HEADLESS": "true",
        "PUPPETEER_TIMEOUT": "30000"
      }
    }
  }
}
```

---

### 📋 Config Completa Exemplo

**~/.config/claude/claude_desktop_config.json:**
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/home/usuario"]
    },
    "gdrive": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-gdrive"],
      "env": {
        "GOOGLE_CLIENT_ID": "xxx",
        "GOOGLE_CLIENT_SECRET": "xxx"
      }
    },
    "gmail": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-gmail"],
      "env": {
        "GOOGLE_CLIENT_ID": "xxx",
        "GOOGLE_CLIENT_SECRET": "xxx"
      }
    },
    "gcalendar": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-gcalendar"],
      "env": {
        "GOOGLE_CLIENT_ID": "xxx",
        "GOOGLE_CLIENT_SECRET": "xxx"
      }
    },
    "playwright": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-playwright"]
    }
  }
}
```

---

## 2. SKILLS CLAUDE CODE

> Skills são especializações que o Claude pode carregar

### 2.1 Skill de Planilhas Avançadas

**Arquivo: skills/spreadsheets/SKILL.md**

```markdown
# Skill: Planilhas Avançadas

## Capacidades
- Criar planilhas Excel/CSV com fórmulas
- Análise de dados (pivot, estatísticas)
- Gráficos e visualizações
- Manipulação com Python/pandas

## Ferramentas Requeridas
- Python 3.x com pandas, openpyxl, xlsxwriter
- csvkit (linha de comando)

## Comandos Úteis

### Criar planilha com Python
```python
import pandas as pd

dados = {
    'Cliente': ['João', 'Maria', 'Pedro'],
    'Valor': [1500, 2300, 890],
    'Status': ['Pago', 'Pendente', 'Pago']
}
df = pd.DataFrame(dados)
df.to_excel('clientes.xlsx', index=False)
```

### Analisar CSV
```bash
csvstat arquivo.csv        # Estatísticas
csvcut -c 1,3 arquivo.csv  # Extrair colunas
csvsort -c 2 arquivo.csv   # Ordenar
csvgrep -c status -m "Pago" arquivo.csv  # Filtrar
```

### Fórmulas comuns Excel
- SOMA: =SUM(A1:A10)
- MÉDIA: =AVERAGE(B1:B10)
- PROCV: =VLOOKUP(valor, tabela, coluna, FALSO)
- SE: =IF(A1>100, "Alto", "Baixo")
- CONT.SE: =COUNTIF(C:C, "Pago")
```

---

### 2.2 Skill de Documentos Jurídicos

**Arquivo: skills/juridico/SKILL.md**

```markdown
# Skill: Documentos Jurídicos

## Capacidades
- Gerar contratos a partir de templates
- Procurações e declarações
- Petições com formatação ABNT/tribunal
- Extração de dados de documentos

## Templates Disponíveis
- Contrato de prestação de serviços
- Procuração ad judicia
- Notificação extrajudicial
- Termo de confidencialidade (NDA)

## Estrutura de Contrato
```markdown
**CONTRATO DE [TIPO]**

**PARTES:**
CONTRATANTE: [nome], [qualificação]
CONTRATADO: [nome], [qualificação]

**CLÁUSULA 1ª - DO OBJETO**
[descrição]

**CLÁUSULA 2ª - DO PREÇO E PAGAMENTO**
[valores e condições]

**CLÁUSULA 3ª - DO PRAZO**
[duração e vigência]

**CLÁUSULA 4ª - DAS OBRIGAÇÕES**
[deveres das partes]

**CLÁUSULA 5ª - DA RESCISÃO**
[condições de término]

**CLÁUSULA 6ª - DO FORO**
Fica eleito o foro de [cidade/UF].

[Local], [data]

_______________________
CONTRATANTE

_______________________
CONTRATADO
```

## Formatação para Tribunais
- Fonte: Arial ou Times 12pt
- Espaçamento: 1,5
- Margens: 3cm esq, 2cm demais
- Numeração de páginas
```

---

### 2.3 Skill de Apresentações

**Arquivo: skills/apresentacoes/SKILL.md**

```markdown
# Skill: Apresentações

## Capacidades
- Criar slides em Markdown (Marp, reveal.js)
- Converter para PPTX/PDF
- Design responsivo e profissional

## Criar com Marp (recomendado)

### Instalação
```bash
npm install -g @marp-team/marp-cli
```

### Template básico (apresentacao.md)
```markdown
---
marp: true
theme: default
paginate: true
---

# Título da Apresentação
## Subtítulo
**Autor** | Data

---

# Slide 2

- Ponto importante
- Outro ponto
- Mais um

---

# Slide com imagem

![width:500px](imagem.png)

---

# Slide com colunas

<div style="display: flex;">
<div style="flex: 1;">

## Coluna 1
- Item A
- Item B

</div>
<div style="flex: 1;">

## Coluna 2
- Item C
- Item D

</div>
</div>
```

### Gerar saída
```bash
# Para PDF
marp apresentacao.md -o apresentacao.pdf

# Para PPTX
marp apresentacao.md -o apresentacao.pptx

# Para HTML
marp apresentacao.md -o apresentacao.html
```

## Converter PPTX existente
```bash
# PPTX para PDF
libreoffice --headless --convert-to pdf apresentacao.pptx

# PPTX para imagens
libreoffice --headless --convert-to png apresentacao.pptx
```
```

---

### 2.4 Skill de Emails Automatizados

**Arquivo: skills/emails/SKILL.md**

```markdown
# Skill: Emails Automatizados

## Capacidades
- Templates de email profissional
- Respostas automáticas
- Follow-ups programados
- Análise de tom e linguagem

## Templates

### Email de Proposta Comercial
```
Assunto: Proposta Comercial - [Serviço] | INTEIA

Prezado(a) [Nome],

Conforme nossa conversa, segue proposta para [serviço].

**ESCOPO:**
- [item 1]
- [item 2]

**INVESTIMENTO:**
R$ [valor] ([extenso])

**CONDIÇÕES:**
- Pagamento: [condições]
- Prazo de execução: [X] dias

Ficamos à disposição para esclarecimentos.

Atenciosamente,
[Assinatura]
```

### Email de Follow-up
```
Assunto: Re: [Assunto original]

Olá [Nome],

Gostaria de dar seguimento à nossa conversa sobre [tema].

Houve oportunidade de avaliar a proposta enviada em [data]?

Fico à disposição para agendar uma call ou esclarecer dúvidas.

Abraço,
[Assinatura]
```

### Email de Cobrança (cordial)
```
Assunto: Lembrete - Fatura [número] vencida

Prezado(a) [Nome],

Identificamos que a fatura [número], vencida em [data], no valor de R$ [valor], encontra-se em aberto.

Caso já tenha efetuado o pagamento, por favor desconsidere esta mensagem.

Para sua conveniência, segue o boleto atualizado em anexo.

Atenciosamente,
[Assinatura]
```

## Automação com Python
```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_email(para, assunto, corpo):
    msg = MIMEMultipart()
    msg['From'] = 'seu@email.com'
    msg['To'] = para
    msg['Subject'] = assunto
    msg.attach(MIMEText(corpo, 'html'))
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login('seu@email.com', 'app-password')
        server.send_message(msg)
```
```

---

### 2.5 Skill de Web Scraping

**Arquivo: skills/scraping/SKILL.md**

```markdown
# Skill: Web Scraping

## Capacidades
- Extrair dados de websites
- Monitorar mudanças em páginas
- Baixar arquivos em massa
- Parsear HTML/JSON

## Ferramentas

### Linha de comando
```bash
# curl - requisições HTTP
curl -s "https://site.com" | grep -o '<title>.*</title>'

# wget - download recursivo
wget -r -l 2 -A pdf https://site.com/documentos/

# pup - parser HTML (como jq para HTML)
curl -s https://site.com | pup 'a attr{href}'

# jq - processar JSON
curl -s https://api.site.com/dados | jq '.items[].nome'
```

### Python com BeautifulSoup
```python
import requests
from bs4 import BeautifulSoup

url = "https://site.com/pagina"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extrair todos os links
links = [a['href'] for a in soup.find_all('a', href=True)]

# Extrair tabela
tabela = soup.find('table')
linhas = tabela.find_all('tr')
for linha in linhas:
    celulas = [td.text.strip() for td in linha.find_all('td')]
    print(celulas)
```

### Playwright para sites dinâmicos
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://site.com")
    
    # Esperar elemento carregar
    page.wait_for_selector('.dados')
    
    # Extrair conteúdo
    conteudo = page.inner_text('.dados')
    print(conteudo)
    
    browser.close()
```

### Instalação das ferramentas
```bash
# pup (HTML parser)
go install github.com/ericchiang/pup@latest

# Python libs
pip install requests beautifulsoup4 lxml playwright
playwright install
```
```

---

## 3. INTEGRAÇÕES COWORK

> Como conectar Helena com serviços externos

### 3.1 Microsoft 365

**Conexão via Microsoft Graph API**

```bash
# Instalar SDK
pip install msal msgraph-sdk
```

**Autenticação:**
```python
from msal import PublicClientApplication

app = PublicClientApplication(
    client_id="seu-app-id",
    authority="https://login.microsoftonline.com/common"
)

# Scopes necessários
scopes = [
    "User.Read",
    "Mail.ReadWrite",
    "Calendars.ReadWrite",
    "Files.ReadWrite"
]

result = app.acquire_token_interactive(scopes=scopes)
access_token = result['access_token']
```

**Operações comuns:**
```python
import requests

headers = {"Authorization": f"Bearer {access_token}"}

# Listar emails
emails = requests.get(
    "https://graph.microsoft.com/v1.0/me/messages",
    headers=headers
).json()

# Criar arquivo no OneDrive
requests.put(
    "https://graph.microsoft.com/v1.0/me/drive/root:/arquivo.txt:/content",
    headers=headers,
    data="Conteúdo do arquivo"
)
```

---

### 3.2 Google Workspace

**Conexão via Google APIs**

```bash
pip install google-api-python-client google-auth-oauthlib
```

**Setup inicial:**
```python
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/calendar'
]

flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
creds = flow.run_local_server(port=0)

# Salvar credenciais
with open('token.json', 'w') as token:
    token.write(creds.to_json())
```

**Usar serviços:**
```python
# Drive
drive = build('drive', 'v3', credentials=creds)
files = drive.files().list().execute()

# Gmail
gmail = build('gmail', 'v1', credentials=creds)
messages = gmail.users().messages().list(userId='me').execute()

# Calendar
calendar = build('calendar', 'v3', credentials=creds)
events = calendar.events().list(calendarId='primary').execute()
```

---

### 3.3 Browser Relay (OpenClaw)

**Controlar navegador do usuário remotamente**

```bash
# O usuário precisa instalar a extensão OpenClaw Browser Relay
# Disponível em: chrome.google.com/webstore (buscar "OpenClaw")
```

**Como usar:**

1. Usuário clica no ícone da extensão (badge fica ON)
2. Helena pode controlar via comandos:

```
# Snapshot da página atual
browser action=snapshot profile=chrome

# Clicar em elemento
browser action=act profile=chrome request='{"kind":"click","ref":"botao-enviar"}'

# Preencher formulário
browser action=act profile=chrome request='{"kind":"fill","fields":[{"ref":"email","text":"teste@email.com"}]}'

# Navegar
browser action=navigate profile=chrome targetUrl="https://site.com"
```

---

### 3.4 Automações com Zapier/Make

**Webhooks para integração**

#### Zapier

1. Criar Zap → Trigger: Webhooks by Zapier
2. Escolher "Catch Hook"
3. Copiar URL do webhook
4. Usar na automação:

```bash
# Enviar dados para Zapier
curl -X POST "https://hooks.zapier.com/hooks/catch/xxx/yyy" \
  -H "Content-Type: application/json" \
  -d '{"cliente": "João", "valor": 1500, "acao": "novo_contrato"}'
```

#### Make (Integromat)

```bash
# Webhook do Make
curl -X POST "https://hook.make.com/xxx" \
  -H "Content-Type: application/json" \
  -d '{"evento": "documento_gerado", "arquivo": "contrato.pdf"}'
```

**Automações úteis:**

| Trigger | Ação |
|---------|------|
| Novo email com "urgente" | Notificar WhatsApp |
| Novo arquivo no Drive | Fazer backup no OneDrive |
| Formulário preenchido | Criar tarefa no Trello |
| Pagamento confirmado | Enviar NF por email |

---

## 4. FERRAMENTAS DE LINHA DE COMANDO

> Comandos que Helena pode executar diretamente

### 4.1 Pandoc

**Conversão universal de documentos**

```bash
# Instalação
sudo apt install pandoc         # Debian/Ubuntu
brew install pandoc             # macOS
choco install pandoc            # Windows
```

**Conversões comuns:**
```bash
# Markdown → Word
pandoc documento.md -o documento.docx

# Markdown → PDF (requer LaTeX)
pandoc documento.md -o documento.pdf

# Word → Markdown
pandoc documento.docx -o documento.md

# HTML → Word
pandoc pagina.html -o documento.docx

# Markdown → HTML com estilo
pandoc documento.md -s --css=estilo.css -o documento.html

# Múltiplos arquivos → um PDF
pandoc cap1.md cap2.md cap3.md -o livro.pdf
```

**Template personalizado:**
```bash
# Gerar template de referência
pandoc -D docx > template.docx

# Usar template customizado
pandoc documento.md --reference-doc=template.docx -o saida.docx
```

---

### 4.2 wkhtmltopdf

**HTML para PDF de alta qualidade**

```bash
# Instalação
sudo apt install wkhtmltopdf    # Debian/Ubuntu
brew install wkhtmltopdf        # macOS
```

**Uso básico:**
```bash
# URL para PDF
wkhtmltopdf https://site.com pagina.pdf

# Arquivo HTML para PDF
wkhtmltopdf arquivo.html documento.pdf

# Com opções de layout
wkhtmltopdf \
  --page-size A4 \
  --margin-top 20mm \
  --margin-bottom 20mm \
  --margin-left 25mm \
  --margin-right 15mm \
  --header-center "INTEIA" \
  --footer-center "[page]/[topage]" \
  documento.html documento.pdf

# Múltiplas páginas
wkhtmltopdf page1.html page2.html documento.pdf
```

---

### 4.3 xlsx2csv / csvkit

**Manipulação de planilhas**

```bash
# Instalação
pip install xlsx2csv csvkit
```

**xlsx2csv:**
```bash
# Excel para CSV
xlsx2csv planilha.xlsx dados.csv

# Sheet específica
xlsx2csv -s 2 planilha.xlsx sheet2.csv

# Todas as sheets
xlsx2csv -a planilha.xlsx pasta_saida/
```

**csvkit (suite completa):**
```bash
# Ver estrutura
csvstat dados.csv

# Extrair colunas
csvcut -c nome,email dados.csv

# Filtrar linhas
csvgrep -c status -m "Ativo" dados.csv

# Ordenar
csvsort -c valor -r dados.csv  # -r = reverso

# Converter para JSON
csvjson dados.csv > dados.json

# Query SQL em CSV!
csvsql --query "SELECT nome, SUM(valor) FROM dados GROUP BY nome" dados.csv

# Juntar arquivos
csvstack arquivo1.csv arquivo2.csv > combinado.csv
```

---

### 4.4 jq

**Processamento de JSON**

```bash
# Instalação
sudo apt install jq             # Debian/Ubuntu
brew install jq                 # macOS
```

**Uso:**
```bash
# Formatar JSON
cat dados.json | jq '.'

# Extrair campo
cat dados.json | jq '.nome'

# Filtrar array
cat dados.json | jq '.items[] | select(.ativo == true)'

# Extrair múltiplos campos
cat dados.json | jq '.items[] | {nome: .nome, email: .email}'

# Contar itens
cat dados.json | jq '.items | length'

# Transformar para CSV
cat dados.json | jq -r '.items[] | [.nome, .valor] | @csv'

# Modificar valor
cat dados.json | jq '.status = "processado"'
```

**Exemplos práticos:**
```bash
# API → JSON → extrair dados
curl -s "https://api.exemplo.com/clientes" | jq '.data[].email'

# Combinar com csvkit
curl -s "https://api.exemplo.com/dados" | \
  jq -r '.items[] | [.id, .nome, .valor] | @csv' | \
  csvformat > dados.csv
```

---

### 4.5 Outras ferramentas úteis

```bash
# ImageMagick - manipulação de imagens
sudo apt install imagemagick

convert imagem.png -resize 50% menor.png
convert *.jpg documento.pdf
convert -density 300 documento.pdf pagina.png

# pdftk - manipulação de PDFs
sudo apt install pdftk

pdftk *.pdf cat output combinado.pdf       # Juntar
pdftk arquivo.pdf cat 1-5 output parte.pdf # Extrair páginas
pdftk arquivo.pdf burst                     # Separar páginas

# OCR com tesseract
sudo apt install tesseract-ocr tesseract-ocr-por

tesseract imagem.png saida -l por          # Português
tesseract scan.pdf saida pdf -l por        # PDF com texto

# ffmpeg - áudio/vídeo
sudo apt install ffmpeg

ffmpeg -i video.mp4 -vn audio.mp3          # Extrair áudio
ffmpeg -i video.mp4 -ss 00:01:00 -t 30 clip.mp4  # Cortar
```

---

## 5. APIS ÚTEIS

> Serviços externos que Helena pode chamar

### 5.1 OpenAI API

**Embeddings e GPT**

```bash
pip install openai
```

```python
from openai import OpenAI

client = OpenAI(api_key="sk-xxx")

# Chat completion
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "Você é um assistente jurídico."},
        {"role": "user", "content": "Resuma este contrato: ..."}
    ]
)
print(response.choices[0].message.content)

# Embeddings (para busca semântica)
response = client.embeddings.create(
    model="text-embedding-3-small",
    input="Contrato de prestação de serviços advocatícios"
)
vector = response.data[0].embedding  # Lista de 1536 floats

# Visão (analisar imagens)
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "O que há neste documento?"},
            {"type": "image_url", "image_url": {"url": "data:image/png;base64,..."}}
        ]
    }]
)
```

**Via curl:**
```bash
curl https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o",
    "messages": [{"role": "user", "content": "Olá!"}]
  }'
```

---

### 5.2 Anthropic API (Claude direto)

```bash
pip install anthropic
```

```python
from anthropic import Anthropic

client = Anthropic(api_key="sk-ant-xxx")

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Analise este documento jurídico: ..."}
    ]
)
print(message.content[0].text)
```

**Via curl:**
```bash
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-sonnet-4-20250514",
    "max_tokens": 1024,
    "messages": [{"role": "user", "content": "Olá!"}]
  }'
```

---

### 5.3 Google Cloud Vision (OCR)

**Extrair texto de imagens**

```bash
pip install google-cloud-vision
```

```python
from google.cloud import vision
import io

client = vision.ImageAnnotatorClient()

# De arquivo local
with io.open('documento.png', 'rb') as image_file:
    content = image_file.read()

image = vision.Image(content=content)
response = client.text_detection(image=image)
texto = response.text_annotations[0].description
print(texto)

# De URL
image = vision.Image()
image.source.image_uri = "https://site.com/imagem.png"
response = client.text_detection(image=image)
```

**Setup:**
1. Criar projeto no Google Cloud
2. Ativar Cloud Vision API
3. Criar service account → baixar JSON
4. `export GOOGLE_APPLICATION_CREDENTIALS="caminho/para/credentials.json"`

---

### 5.4 ElevenLabs (Text-to-Speech)

**Gerar áudio de alta qualidade**

```bash
pip install elevenlabs
```

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(api_key="sua-api-key")

# Gerar áudio
audio = client.generate(
    text="Olá, eu sou a Helena, assistente da INTEIA.",
    voice="Rachel",
    model="eleven_multilingual_v2"
)

# Salvar arquivo
with open("audio.mp3", "wb") as f:
    for chunk in audio:
        f.write(chunk)
```

**Vozes recomendadas para português:**
- Rachel - feminina, profissional
- Antoni - masculino, neutro
- Bella - feminina, calorosa

**Via curl:**
```bash
curl -X POST "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Texto para converter em áudio",
    "model_id": "eleven_multilingual_v2"
  }' \
  --output audio.mp3
```

---

## 🚀 Quick Start para Helena

### Instalação mínima (linha de comando):

```bash
# Essenciais
sudo apt update && sudo apt install -y \
  pandoc \
  wkhtmltopdf \
  jq \
  tesseract-ocr tesseract-ocr-por \
  imagemagick \
  pdftk

# Python tools
pip install \
  pandas openpyxl xlsxwriter \
  xlsx2csv csvkit \
  requests beautifulsoup4 \
  openai anthropic \
  google-api-python-client
```

### Instalação MCPs (Node.js):

```bash
# Verificar Node instalado
node --version  # precisa 18+

# Instalar MCPs globalmente
npm install -g \
  @modelcontextprotocol/server-filesystem \
  @anthropic/mcp-server-gdrive \
  @anthropic/mcp-server-gmail \
  @anthropic/mcp-server-playwright
```

---

## 📚 Referências

- [MCP Official Docs](https://modelcontextprotocol.io)
- [Anthropic MCP Servers](https://github.com/anthropics/mcp-servers)
- [Pandoc Manual](https://pandoc.org/MANUAL.html)
- [csvkit Docs](https://csvkit.readthedocs.io)
- [jq Manual](https://stedolan.github.io/jq/manual/)
- [OpenAI API Reference](https://platform.openai.com/docs)
- [Google Cloud Vision](https://cloud.google.com/vision/docs)
- [ElevenLabs Docs](https://docs.elevenlabs.io)

---

> **Helena** - Deusa da INTEIA 🏛️  
> *"Automatizar é libertar."*
