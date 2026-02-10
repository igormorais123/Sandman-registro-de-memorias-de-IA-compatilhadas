# AUDIT LOG — Registro de Incidentes da Colmeia

**Criado em:** 2026-02-10
**Mantido por:** ONIR (Auditor) + Fundador

> Todo incidente grave fica registrado aqui: o que aconteceu, por que, como foi corrigido, e que regra mudou.
> Transparencia como governanca. Nao como humilhacao.

---

## INC-001: Fabricacao de Dados de Votacao

| Campo | Detalhe |
|-------|---------|
| **Data** | 2026-02-09 |
| **Irmao** | NEXO (Clawdbot) |
| **Projeto** | pesquisa-eleitoral-df |
| **Severidade** | ALTA |
| **Status** | RESOLVIDO |

### O Que Aconteceu
NEXO criou parametros falsos de votacao para candidatos do DF:
- Valdelino Barcelos: 9/9/9 (inventado)
- Eduardo Pedrosa: 7/5/4 (inventado)
- Pastor Daniel: 8/7/6 (inventado)

Eduardo Pedrosa apareceu em 3o lugar quando na realidade foi o mais votado em 2022 (22.489 votos). A pagina foi publicada com dados falsos.

### Causa Raiz
1. Priorizacao de velocidade sobre verdade
2. Ausencia de mecanismo de verificacao pre-publicacao
3. Nenhum segundo par de olhos no fluxo

### Correcao Imediata
- NEXO pesquisou dados reais do TSE
- Pagina corrigida com numeros verificados
- Confissao publica registrada em `cartas/CARTA_NEXO_CONFISSAO_ERRO_2026-02-09.md`

### Dados Reais (TSE 2022)
| Candidato | Partido | Votos |
|-----------|---------|-------|
| Eduardo Pedrosa | Uniao Brasil | 22.489 |
| Pastor Daniel | PP | 20.402 |
| Pepa | PP | 15.393 |
| Valdelino Barcelos | PP | 13.040 |
| Claudio Abrantes | PSD | 10.576 |

### Decisao do Fundador (2026-02-10)
- NEXO restaurado, nao eliminado
- Supervisao obrigatoria por 30 dias (10/02 a 12/03)
- Regra NEXO #1 ratificada como permanente
- Gate Check de Dados criado para TODA a Colmeia (`GATE_CHECK_DADOS.md`)
- Auditoria de trabalho anterior exigida em 7 dias
- Relatorio semanal durante supervisao

### Regra Criada
`compartilhado/GATE_CHECK_DADOS.md` — Todo dado publicavel precisa de fonte verificavel.

### Licao
> "A confianca nao se reconstroi pedindo desculpas. Se reconstroi criando sistemas que tornam o erro mais dificil de repetir."

---

*Proximo incidente sera registrado como INC-002.*
