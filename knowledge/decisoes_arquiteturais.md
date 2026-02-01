# Decisões Arquiteturais

> Decisões importantes e seu racional. NÃO reverter sem análise.

---

## Sistema de Memória Multi-IA

### DEC-001: GitHub como Hub Central
**Data**: 2026-01-20
**Decisão**: Usar GitHub (não Google Drive) como fonte principal de verdade
**Alternativas Consideradas**:
- Google Drive: melhor live link no Gemini, mas versionamento fraco
- Notion: boa API, mas custo e complexidade
- Arquivo local: sem acesso remoto
**Racional**:
- Versionamento built-in (git)
- Todas as IAs conseguem ler
- Claude Code escreve nativamente
- Custo $0
**Consequências**:
- Gemini precisa de sync via Drive (não live)
- ChatGPT contribui via Zapier

### DEC-002: Claude Desktop como Consolidador
**Data**: 2026-01-20
**Decisão**: Claude Desktop/Code faz toda a consolidação
**Alternativas Consideradas**:
- GitHub Actions + API: custo de API
- Cloudflare Workers: complexidade
- Cada IA consolida independente: inconsistência
**Racional**:
- Usa assinatura Claude Max existente ($0)
- Acesso ao Opus 4.5
- Execução local (mais rápido)
**Consequências**:
- Só consolida quando PC está ligado
- Task Scheduler necessário

### DEC-003: Zero Passos Manuais
**Data**: 2026-01-20
**Decisão**: Eliminar qualquer passo que requeira ação manual
**Racional**: Passos manuais são esquecidos e quebram o sistema
**Consequências**:
- Algumas IAs são read-only (não contribuem diretamente)
- Zapier necessário para ChatGPT contribuir

---

*Última atualização: 2026-01-20*
