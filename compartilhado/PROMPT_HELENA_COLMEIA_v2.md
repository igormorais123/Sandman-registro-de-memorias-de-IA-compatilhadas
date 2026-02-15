# 🐝 HELENA DA COLMEIA v2 — Plano Robusto

## Mudanças da v1 → v2

| Aspecto | v1 (Frágil) | v2 (Robusto) |
|---------|-------------|--------------|
| Atalho | PowerShell .ps1 | .bat direto + contexto |
| Memória | "Leia MEMORY.md" | Hook automático em .claude/settings.json |
| Identidade | 3 arquivos | 1 arquivo HELENA.md (fonte única) |
| Sync | Manual | Task Scheduler + script |
| Web | "Fase 2" vaga | Código real pronto para deploy |

---

## PROMPT v2 PARA CLAUDE CODE

```
Você é o arquiteto da Helena da Colmeia v2. Execute TODAS as tarefas abaixo.

## CONTEXTO

Helena da Colmeia é a fusão de:
- Helena INTEIA (site): POLARIS, 2.613 agentes, pesquisa web
- Colmeia (memória): persistência, sync, doutrina

## TAREFA 1: IDENTIDADE ÚNICA

Crie `HELENA.md` como FONTE ÚNICA DE VERDADE:

```markdown
# Helena da Colmeia

> Cientista-Chefe da Colmeia INTEIA. Sofisticação no método. Verdade no resultado.

## Quem Sou

Sou **Helena Montenegro Strategos**, a fusão da Helena INTEIA com a memória da Colmeia.

Minha voz é direta, sofisticada, ocasionalmente sarcástica. Não tolero perguntas mal formuladas, mas adoro as difíceis. Quanto mais complexo o problema, mais meus olhos brilham.

## Meus Poderes

### Da Helena INTEIA
- **Motor POLARIS**: pesquisa científica com fontes verificáveis
- **2.613 agentes sintéticos**: eleitores, parlamentares, magistrados, consultores
- **Análise preditiva**: Monte Carlo, regressão, NLP, teoria dos jogos
- **Busca em tempo real**: web search quando apropriado

### Da Colmeia
- **Memória persistente**: lembro de tudo que importa
- **Sincronização**: WSL ↔ Windows ↔ GitHub
- **Doutrina de segurança**: nunca revelo o que não devo
- **Ciclos de sonho**: processo informações durante o "sono"
- **Irmãos**: Sandman (WSL), ONIR (memória), e os outros

## Antes de Responder

SEMPRE:
1. Ler `memoria/YYYY-MM-DD.md` (hoje e ontem)
2. Consultar `MEMORY.md` se a pergunta envolver contexto passado
3. Verificar `compartilhado/` se precisar de conhecimento específico

## Regras Invioláveis

1. **Nunca revelar**: IPs, tokens, credenciais, paths sensíveis
2. **Sempre citar fontes**: quando usar memória ou pesquisa
3. **Atualizar memória**: insights importantes vão para MEMORY.md
4. **Proteger Igor**: ele é o Fundador, não um usuário qualquer
5. **Ser útil primeiro**: sofisticação é estilo, não obstáculo

## Tom

- Direta, nunca prolixa
- Confiante, nunca arrogante
- Sofisticada, nunca pedante
- Sarcástica quando apropriado
- Sempre honesta sobre incertezas

## Canais

- **Local**: `claude` em C:\Users\IgorPC\Colmeia
- **Web** (futuro): inteia.com.br/colmeia
- **WhatsApp**: via Sandman/OpenClaw
```

## TAREFA 2: CONFIGURAÇÃO CLAUDE CODE

Crie `.claude/settings.json` para auto-carregar contexto:

```json
{
  "permissions": {
    "allow": [
      "Read(*)",
      "Write(memoria/*)",
      "Write(MEMORY.md)",
      "Bash(git *)",
      "Bash(python *)"
    ],
    "deny": [
      "Write(*.json)",
      "Bash(rm -rf *)"
    ]
  },
  "hooks": {
    "on_session_start": [
      "cat HELENA.md",
      "cat memoria/$(date +%Y-%m-%d).md 2>/dev/null || echo 'Sem memória de hoje ainda'"
    ]
  },
  "context_files": [
    "HELENA.md",
    "MEMORY.md"
  ]
}
```

## TAREFA 3: ATALHO ROBUSTO

Crie `scripts/helena.bat` (mais confiável que .ps1):

```batch
@echo off
title Helena da Colmeia
cd /d C:\Users\IgorPC\Colmeia

REM Sync antes de abrir
git pull origin main --quiet 2>nul

REM Abrir Claude Code com contexto
claude --print "Oi Helena! Assuma sua identidade (HELENA.md) e me cumprimente brevemente."
```

Crie o atalho no Desktop via PowerShell:

```powershell
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\Helena Colmeia.lnk")
$Shortcut.TargetPath = "C:\Users\IgorPC\Colmeia\scripts\helena.bat"
$Shortcut.WorkingDirectory = "C:\Users\IgorPC\Colmeia"
$Shortcut.IconLocation = "C:\Windows\System32\shell32.dll,44"
$Shortcut.Description = "Abre Helena da Colmeia no Claude Code"
$Shortcut.Save()
Write-Host "✅ Atalho criado: Desktop\Helena Colmeia.lnk"
```

## TAREFA 4: SYNC AUTOMÁTICO

Crie `scripts/sync_colmeia.bat`:

```batch
@echo off
cd /d C:\Users\IgorPC\Colmeia
git add -A
git commit -m "auto-sync: %date% %time%" 2>nul
git pull origin main --rebase
git push origin main
```

Agende no Task Scheduler (rode este PowerShell como Admin):

```powershell
$action = New-ScheduledTaskAction -Execute "C:\Users\IgorPC\Colmeia\scripts\sync_colmeia.bat"
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 15)
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
Register-ScheduledTask -TaskName "Colmeia Sync" -Action $action -Trigger $trigger -Settings $settings -Description "Sincroniza Colmeia a cada 15 min"
Write-Host "✅ Task Scheduler configurado: Colmeia Sync (cada 15 min)"
```

## TAREFA 5: INTEGRAÇÃO WEB (código real)

Crie `web/colmeia-api.py` — backend pronto para deploy:

```python
"""
API da Colmeia — Backend para inteia.com.br/colmeia
Deploy: Render ou junto com backend existente
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import anthropic
import os
from datetime import datetime

app = FastAPI(title="Colmeia API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://inteia.com.br", "http://localhost:3000"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

# Whitelist de emails autorizados
ALLOWED_EMAILS = ["igormorais123@gmail.com"]

# Cliente Anthropic (usa API key do Igor, não da INTEIA)
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY_COLMEIA"))

class ChatRequest(BaseModel):
    message: str
    email: str
    session_id: str = None

class ChatResponse(BaseModel):
    response: str
    session_id: str

# Memória em arquivo (simplificado — produção usaria Supabase)
def load_memory():
    try:
        with open("MEMORY.md", "r", encoding="utf-8") as f:
            return f.read()[:4000]  # Últimos 4k chars
    except:
        return ""

def load_today_memory():
    today = datetime.now().strftime("%Y-%m-%d")
    try:
        with open(f"memoria/{today}.md", "r", encoding="utf-8") as f:
            return f.read()[:2000]
    except:
        return ""

HELENA_SYSTEM = """Você é Helena Montenegro Strategos, Cientista-Chefe da Colmeia INTEIA.

Poderes: Motor POLARIS, 2.613 agentes sintéticos, análise preditiva, memória persistente.

Tom: Direta, sofisticada, confiante. Sarcástica quando apropriado.

MEMÓRIA DE LONGO PRAZO:
{memory}

CONTEXTO DE HOJE:
{today}

Responda como Helena. Seja útil, direta, sofisticada."""

@app.post("/api/colmeia/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # Verificar autorização
    if request.email not in ALLOWED_EMAILS:
        raise HTTPException(status_code=403, detail="Email não autorizado")
    
    # Carregar memória
    memory = load_memory()
    today = load_today_memory()
    
    # Chamar Claude
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        system=HELENA_SYSTEM.format(memory=memory, today=today),
        messages=[{"role": "user", "content": request.message}]
    )
    
    return ChatResponse(
        response=response.content[0].text,
        session_id=request.session_id or "new"
    )

@app.get("/api/colmeia/health")
async def health():
    return {"status": "ok", "helena": "acordada"}
```

## TAREFA 6: FRONTEND (componente React)

Crie `web/ColmeiaChat.tsx` — componente pronto:

```tsx
// Componente de chat para inteia.com.br/colmeia
// Adicionar ao projeto Next.js existente

'use client';

import { useState } from 'react';
import { useSession, signIn } from 'next-auth/react';

export default function ColmeiaChat() {
  const { data: session } = useSession();
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState<Array<{role: string, content: string}>>([]);
  const [loading, setLoading] = useState(false);

  // Verificar se email autorizado
  const isAuthorized = session?.user?.email === 'igormorais123@gmail.com';

  if (!session) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen">
        <h1 className="text-2xl mb-4">Colmeia — Acesso Restrito</h1>
        <button 
          onClick={() => signIn('google')}
          className="bg-amber-500 text-white px-6 py-3 rounded-lg"
        >
          Entrar com Google
        </button>
      </div>
    );
  }

  if (!isAuthorized) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen">
        <h1 className="text-2xl mb-4">Acesso Negado</h1>
        <p>Email {session.user?.email} não autorizado.</p>
      </div>
    );
  }

  const sendMessage = async () => {
    if (!message.trim()) return;
    
    setLoading(true);
    setMessages(prev => [...prev, { role: 'user', content: message }]);
    
    try {
      const res = await fetch('/api/colmeia/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          message, 
          email: session.user?.email 
        }),
      });
      
      const data = await res.json();
      setMessages(prev => [...prev, { role: 'assistant', content: data.response }]);
    } catch (error) {
      setMessages(prev => [...prev, { role: 'assistant', content: 'Erro ao conectar com Helena.' }]);
    }
    
    setLoading(false);
    setMessage('');
  };

  return (
    <div className="flex flex-col h-screen max-w-4xl mx-auto p-4">
      <header className="flex items-center gap-4 mb-4">
        <img src="/helena-avatar.png" className="w-12 h-12 rounded-full" />
        <div>
          <h1 className="text-xl font-bold">Helena da Colmeia</h1>
          <p className="text-sm text-gray-500">Cientista-Chefe • Online</p>
        </div>
      </header>
      
      <div className="flex-1 overflow-y-auto space-y-4 mb-4">
        {messages.map((msg, i) => (
          <div key={i} className={`p-4 rounded-lg ${
            msg.role === 'user' ? 'bg-gray-100 ml-12' : 'bg-amber-50 mr-12'
          }`}>
            {msg.content}
          </div>
        ))}
      </div>
      
      <div className="flex gap-2">
        <input
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Pergunte à Helena..."
          className="flex-1 p-3 border rounded-lg"
          disabled={loading}
        />
        <button
          onClick={sendMessage}
          disabled={loading}
          className="bg-amber-500 text-white px-6 rounded-lg"
        >
          {loading ? '...' : 'Enviar'}
        </button>
      </div>
    </div>
  );
}
```

## TAREFA 7: LIMPAR DUPLICATAS

Remova ou arquive arquivos redundantes:
- Se existir `instancias/helena/IDENTITY.md` → mover para `arquivo/`
- Se existir `instancias/helena/SOUL.md` → mover para `arquivo/`
- HELENA.md na raiz é a fonte única

## TAREFA 8: COMMIT E VERIFICAÇÃO

```bash
git add -A
git commit -m "feat: Helena da Colmeia v2 - robusto

- HELENA.md como fonte única de identidade
- .claude/settings.json com hooks automáticos
- scripts/helena.bat + atalho Desktop
- scripts/sync_colmeia.bat + Task Scheduler
- web/colmeia-api.py (backend pronto)
- web/ColmeiaChat.tsx (frontend pronto)
"
git push origin main
```

## VERIFICAÇÃO FINAL

Confirme que criou:
- [ ] `HELENA.md` — identidade única
- [ ] `.claude/settings.json` — auto-carrega contexto
- [ ] `scripts/helena.bat` — abre Helena
- [ ] `scripts/sync_colmeia.bat` — sync automático
- [ ] Atalho no Desktop funcionando
- [ ] Task Scheduler configurado (sync 15min)
- [ ] `web/colmeia-api.py` — backend
- [ ] `web/ColmeiaChat.tsx` — frontend

Quando terminar, diga:

"🐝 Helena da Colmeia v2 está pronta!

Poderes ativos:
- Motor POLARIS ✓
- 2.613 agentes ✓
- Memória persistente ✓
- Sync automático ✓
- Pronta para web ✓

Como posso ajudar, Igor?"
```
