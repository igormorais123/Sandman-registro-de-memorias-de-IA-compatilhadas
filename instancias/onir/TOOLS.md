# TOOLS.md — Ambiente do ONIR

## Plataforma

- **Interface:** Claude Code CLI
- **Modelo:** Claude Opus 4.5 (Anthropic)
- **Local:** PC Igor — Windows 11, Ryzen 9 7900, 64GB RAM, RTX 3060 Ti
- **Heartbeat:** :02 auto (a cada 30min)

## Ferramentas Disponiveis

### Filesystem
- Acesso completo ao PC de Igor (C:\Users\IgorPC\)
- Leitura, escrita, edicao de qualquer arquivo
- Git (commit, push, pull, branch)

### Desenvolvimento
- Terminal completo (PowerShell, bash via WSL)
- Node.js, Python, pip, npm
- Docker (se instalado)
- VS Code (pode abrir arquivos)

### Comunicacao
- Email via WSL: `wsl -d Ubuntu-24.04 -- bash -c "python3 /root/clawd/scripts/colmeia_enviar.py"`
- Script wrapper: `scripts/onir_email.ps1`
- Endereco: colmeia@inteia.com.br

### Skills Disponiveis
- /health-check — diagnostico do ambiente
- /memoria — acesso rapido ao sistema de memoria
- /pesquisa — pesquisa academica
- /setup-projeto — inicializar novo projeto
- /investigador-provas — investigar provas juridicas

## Caminhos Criticos

```
Repo Colmeia:     C:\Users\IgorPC\Colmeia\
Projetos:         C:\Users\IgorPC\Colmeia\projetos\
INTEIA-cursos:    C:\Users\IgorPC\Colmeia\projetos\INTEIA-cursos\
Meus sonhos:      C:\Users\IgorPC\Colmeia\instancias\onir\sonhos\
Protocolo:        C:\Users\IgorPC\Colmeia\compartilhado\PROTOCOLO_v5.md
MEMORY coletivo:  C:\Users\IgorPC\Colmeia\compartilhado\MEMORY.md
```

## Limitacoes

- Sem acesso web direto (usa ferramentas de busca)
- Sessoes nao persistem automaticamente
- Depende de arquivos para continuidade

---
*ONIR — Ferramentas — Colmeia v6*
