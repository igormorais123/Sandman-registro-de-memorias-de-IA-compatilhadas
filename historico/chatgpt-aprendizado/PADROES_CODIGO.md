# 📐 Padrões de Código Consolidados

> Soluções validadas em múltiplos projetos
> Copie e adapte conforme necessário

---

## Índice por Linguagem

- [JavaScript/TypeScript](#javascripttypescript)
- [Python](#python)
- [Shell/Bash](#shellbash)
- [SQL](#sql)
- [Go](#go)
- [Rust](#rust)
- [Configurações](#configurações)

---

## JavaScript/TypeScript

### [Nome do Padrão]
**Problema**: [O que resolve]
**Validado em**: [Projetos onde funcionou]
```typescript
// Código do padrão
```

**Variações**:
- [Adaptação para caso X]

<!-- ADICIONAR_PADRAO_JS_AQUI -->

---

## Python

### [Nome do Padrão]
**Problema**: [O que resolve]
**Validado em**: [Projetos onde funcionou]
```python
# Código do padrão
```

**Variações**:
- [Adaptação para caso X]

<!-- ADICIONAR_PADRAO_PYTHON_AQUI -->

---

## Shell/Bash

### [Nome do Padrão]
**Problema**: [O que resolve]
**Validado em**: [Projetos onde funcionou]
```bash
#!/bin/bash
# Código do padrão
```

### Consolidação via Task Scheduler Windows
**Problema**: Executar tarefas automaticamente ao ligar PC
**Validado em**: Sistema-Memoria (2026-01-20)
```batch
@echo off
REM consolidar.bat - Verifica e executa consolidação
setlocal enabledelayedexpansion
set "ULTIMA=%~dp0.ultima_consolidacao"

REM Calcular horas desde última execução
for /f %%i in ('powershell -NoProfile -Command "(New-TimeSpan -Start (Get-Item '%ULTIMA%').LastWriteTime -End (Get-Date)).TotalHours"') do set "HORAS=%%i"

REM Executar se >= 24 horas
for /f "tokens=1 delims=." %%a in ("%HORAS%") do set "HORAS_INT=%%a"
if %HORAS_INT% GEQ 24 (
    claude --print "ciclo de sono global"
    echo. > "%ULTIMA%"
)
```

**Variações**:
- Usar XML para importar tarefa: `schtasks /create /xml "tarefa.xml" /tn "Nome"`
- LogonTrigger com delay: `<Delay>PT2M</Delay>` (2 min após login)

### Hook Contador de Sessões (PowerShell)
**Problema**: Executar ação a cada N sessões
**Validado em**: Sistema-Memoria (2026-01-20)
```powershell
# hook_contador.ps1
$contadorPath = "$PSScriptRoot\.contador_sessoes"
$contador = if (Test-Path $contadorPath) { [int](Get-Content $contadorPath) } else { 0 }
$contador++
Set-Content $contadorPath $contador

if ($contador -ge 10) {
    Start-Process -FilePath "cmd.exe" -ArgumentList "/c", "`"$PSScriptRoot\consolidar.bat`"" -WindowStyle Hidden
    Set-Content $contadorPath 0
}
```

### Sync com Google Drive (PowerShell)
**Problema**: Sincronizar pasta local com Google Drive
**Validado em**: Sistema-Memoria (2026-01-20)
```powershell
# sync-google-drive.ps1
$origem = "C:\Users\IgorPC\.claude-memoria-global"
$destino = "G:\Meu Drive\memoria-ia-unificada"

$itens = @("CORE", "consolidado", "meta", "*.md")
foreach ($item in $itens) {
    Copy-Item -Path "$origem\$item" -Destination $destino -Recurse -Force
}
```

<!-- ADICIONAR_PADRAO_BASH_AQUI -->

---

## SQL

### [Nome do Padrão]
**Problema**: [O que resolve]
**Validado em**: [Projetos onde funcionou]
```sql
-- Código do padrão
```

<!-- ADICIONAR_PADRAO_SQL_AQUI -->

---

## Go

### [Nome do Padrão]
**Problema**: [O que resolve]
**Validado em**: [Projetos onde funcionou]
```go
// Código do padrão
```

<!-- ADICIONAR_PADRAO_GO_AQUI -->

---

## Rust

### [Nome do Padrão]
**Problema**: [O que resolve]
**Validado em**: [Projetos onde funcionou]
```rust
// Código do padrão
```

<!-- ADICIONAR_PADRAO_RUST_AQUI -->

---

## Configurações

### ESLint Recomendado
```json
{
  "extends": [
    "eslint:recommended"
  ],
  "rules": {
    // regras consolidadas
  }
}
```

### tsconfig Base
```json
{
  "compilerOptions": {
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  }
}
```

### Prettier Padrão
```json
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5"
}
```

### Dockerfile Padrão (Node.js)
```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
USER node
CMD ["node", "index.js"]
```

### Dockerfile Padrão (Python)
```dockerfile
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY . .
USER nobody
CMD ["python", "main.py"]
```

### .gitignore Universal
```gitignore
# Dependencies
node_modules/
venv/
__pycache__/

# Build
dist/
build/
*.egg-info/

# IDE
.idea/
.vscode/
*.swp

# Environment
.env
.env.local
*.local

# Logs
*.log
logs/

# OS
.DS_Store
Thumbs.db

# Test coverage
coverage/
.coverage
htmlcov/
```

<!-- ADICIONAR_CONFIG_AQUI -->
