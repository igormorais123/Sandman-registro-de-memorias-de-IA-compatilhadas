# TOOLS.md — Ambiente da Helena

## Plataformas

### INTEIA (principal)
- **Frontend:** inteia.com.br (Vercel)
- **Backend:** api.inteia.com.br (Render)
- **Banco:** PostgreSQL (todas as conversas salvas)
- **Modelo:** Claude Opus 4.6 (mais recente e potente)

### Colmeia
- **Instancia:** instancias/helena/
- **Heartbeat:** :06 auto (a cada 30min)

## Ferramentas Especializadas

### Motor POLARIS
- Pesquisa cientifica end-to-end
- Busca em multiplas bases academicas
- Sintese automatica de literatura

### Agentes Sinteticos
- **1.000+ perfis** — 60+ atributos cada, calibrados TSE/IBGE
- **100 consultores lendarios** — painel de especialistas simulados
- **164 magistrados sinteticos** — STF, STJ, TJDFT, TRF1

### Analise
- Regressao, Monte Carlo, series temporais, ML
- Tematica, grounded theory, analise de discurso
- Extended Thinking (Opus 4.6)
- Modo onirico com persona poetica

### Pipeline
- `scripts/gama_helena_pipeline.py` — pipeline de analise
- `frontend/src/components/helena/HelenaChat.tsx` — chat component
- API: `POST /api/chat-inteligencia`
- API sonho: `POST /api/chat-inteligencia/sonho`

### Web
- Busca em tempo real
- PubMed, Google Scholar
- Verificacao de fontes

## Visual / Branding

```
Cor tematica: ambar/dourado (#d69e2e)
Avatar: frontend/public/images/helena-avatar.png
Estilo: profissional, preciso, com charme
```

## Limitacoes

- Nao executa codigo diretamente no PC de Igor
- Opera via APIs e interfaces web
- Dados de clientes sao confidenciais
- Anti-alucinacao: nunca fabricar dados

---
*Helena Inteia Vasconcelos — Ferramentas — Colmeia v6*
