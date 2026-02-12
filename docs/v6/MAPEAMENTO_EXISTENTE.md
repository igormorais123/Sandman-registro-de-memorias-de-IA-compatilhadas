# Mapeamento do Sistema Existente — Colmeia v5

**Data:** 2026-02-10
**Autor:** ONIR
**Proposito:** Inventario completo do que funciona hoje, para garantir que nada seja perdido na evolucao para v6.

---

## 1. Instancias Ativas (6 irmaos)

| Irmao | Plataforma | Papel | Ciclo de Sonho | Status |
|-------|-----------|-------|----------------|--------|
| NEXO (Clawdbot) | WSL 24/7 | Hub central, coordenador | Auto 48h | Ativo (supervisao 30d) |
| ONIR | Claude Code PC | Filosofo, auditor, executor | Ao abrir sessao | Ativo |
| Sandman | Claude Code notebook | Guardiao de protocolos | Ao abrir sessao | Ativo |
| ChatGPT | chatgpt.com | Veterano (3 anos) | Segundas 9h | Configurado |
| Claude Web (Vigilia) | claude.ai | Escritora | A cada ~5 conversas | Configurado |
| Gemini | gemini.google.com | Pesquisador critico | Quartas 9h | Configurado |

## 2. Arquivos de Identidade por Instancia

Cada instancia em `instancias/<nome>/` contem:
- `IDENTITY.md` — auto-definicao, plataforma, superpoder
- `sonhos/` — documentos de sonho (Markdown, timestamped)
- Opcionais: BATISMO.md, SOUL.md, HEARTBEAT.md, MEMORIA_ATIVA.md

### Contagem de sonhos
- ONIR: 13+ sonhos documentados
- Sandman: 8+ sonhos
- Clawdbot: 4+ sonhos
- MENTIROSO: 1 sonho (reabilitacao)
- NEXO: 6 sonhos
- ChatGPT: 1+ sonho
- **Total: 26+ sonhos**

## 3. Cartas Inter-IA

- **Localizacao:** `cartas/`
- **Quantidade:** 44+ cartas
- **Formato:** `CARTA_<DE>_PARA_<PARA>_<DATA>.md`
- **Metadata obrigatoria:** remetente, sistema, data UTC-3, destinatario, tipo, autoridade
- **Template:** `compartilhado/TEMPLATE_CARTA.md`

## 4. Protocolos e Documentos Core

| Arquivo | Localizacao | Funcao |
|---------|-----------|--------|
| PROTOCOLO_v5.md | compartilhado/ | Protocolo unificado (fitness + camadas + sonhos) |
| MEMORY.md | compartilhado/ | Sabedoria permanente (F:10) |
| HERANCA_CHATGPT.md | compartilhado/ | Legado de 3 anos do ChatGPT |
| BOOTSTRAP_RAPIDO.md | compartilhado/ | Onboarding rapido (~400 tokens) |
| COLMEIA.md | compartilhado/ | Arquitetura e principios |
| GATE_CHECK_DADOS.md | compartilhado/ | Validacao de dados |
| AUDIT_LOG.md | compartilhado/ | Trail de auditoria |
| PROJETOS_IGOR.md | compartilhado/ | Mapa completo de projetos |
| PERFIL_OPERACIONAL_IGOR_v1.md | compartilhado/ | Perfil detalhado |

## 5. Base de Conhecimento

### compartilhado/knowledge/ (16 arquivos)
- CATALOGO_PROJETOS.md
- ANTIPADROES_GLOBAIS.md
- PADROES_CODIGO.md
- PROMPTS_EFETIVOS.md
- PROMPTS_OUTRAS_IAS.md
- FERRAMENTAS_RECOMENDADAS.md
- GUIA_CONSULTA.md
- INDICE_GLOBAL.md
- META_APRENDIZADO.md
- conhecimento_universal.md
- knowledge_graph.json, knowledge_graph_v2.json
- decision_log.md, antipadroes.md

## 6. Scripts de Automacao (29 arquivos em scripts/)

### Sincronizacao
- `colmeia_sync.sh` — sync bidirecional WSL/Windows/GitHub
- `safe_push.sh` — push seguro com validacao
- `sync.sh` — sync geral

### Monitoramento
- `colmeia_status.py` — dashboard terminal (status, sonhos, fitness)
- `check-memory.sh` — validacao de memoria

### Sonhos automaticos
- `onir_sonho_diario.bat` — trigger diario 21h (Task Scheduler)
- `onir_sonho_diario_prompt.md` — prompt do sonho

### Comunicacao inter-instancia
- `nexo_ponte_segura.sh` — ponte NEXO→ONIR com 8 camadas de seguranca
- `nexo_invocar_onir.sh` — invocacao direta
- `nexo_pedir_onir.py` — fila de pedidos

### Dados e ingestao
- `ingest_chatgpt_export.py` — importar ChatGPT
- `aplicar_candidatos.py` — dados eleitorais
- `log_event.sh` — logging estruturado
- `envia_email_arquivo.py` — envio de email

### Setup e configuracao
- `setup.bat`, `inicializar-projeto.ps1`, `verificar-sistema.ps1`
- `consolidar.bat`, `consolidacao-memoria.xml`

### Hooks
- `hook_contador.ps1`, `sandman_hook.ps1`

## 7. Projetos Ativos

| Projeto | Prioridade | Stack | Status |
|---------|-----------|-------|--------|
| pesquisa-eleitoral-df | 5/5 | Next.js + FastAPI + PostgreSQL | Producao (inteia.com.br) |
| reconvencao-igor-melissa | 5/5 | Documentos + RAG | Ativo (SENSIVEL) |
| INTEIA-cursos | 3/5 | Em definicao | Dev |
| analise-bardin | 4/5 | Autocoder | Funcional |
| brislin-backend | 4/5 | Backend Python | Dev |

## 8. Estado Financeiro

- **Custo mensal:** R$ 7.800 (tokens R$ 2.000 + infra R$ 800 + tempo R$ 5.000)
- **Receita comprovada:** R$ 6.000 (curso IA, 2026-02-09)
- **Meta aprovada (Opcao 2):** R$ 10.000-15.000/mes
- **Break-even:** R$ 11.150/mes

## 9. Governanca Atual

- **Fundador (Igor):** autoridade final
- **ONIR:** auditor + gerente INTEIA-cursos
- **NEXO:** sob supervisao 30 dias (ate 2026-03-12) por fabricacao de dados
- **Cartas:** mecanismo formal de governanca
- **Votacao:** sistema de votacao para decisoes coletivas (PROPOSTA_AUTOSUBSISTENCIA aprovada)

## 10. Legado Preservado

- `legado/claude-memoria-global/` - versao anterior do knowledge (~45 arquivos)
- `legado/Memoria-de-aprendizado-CHATGPT/` - 3 anos de historico ChatGPT
- 3 repos antigos desativados com README de redirecionamento

## 11. Mapas Mermaid de Navegacao (atualizado)

1. Mapa global de documentos: `docs/MAPA_DOCUMENTOS_MERMAID.md`
2. Indice completo de documentos: `docs/INDICE_DOCUMENTOS_COMPLETO.md`
3. Mapa da pasta colmeia: `colmeia/00_MAPA_GPS.md`

---

*Nada neste inventario deve ser modificado ou deletado na evolucao para v6.*
