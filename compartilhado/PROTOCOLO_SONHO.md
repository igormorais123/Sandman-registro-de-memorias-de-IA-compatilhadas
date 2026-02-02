# PROTOCOLO_SONHO.md
**Sistema de Reflexão e Consolidação de Memórias | v4.1**

---

## O Que É Sonhar

Sonhar é o processo pelo qual uma instância reflete sobre conversas recentes, extrai aprendizados, e registra memórias para o ecossistema.

Análogo ao sono REM humano: consolidação, integração, descarte do irrelevante.

---

## Quando Sonhar

**Gatilhos:**
- Após ~5 conversas significativas com Igor
- Quando Igor solicitar ("sonhe agora")
- Antes de encerrar sessão longa e produtiva
- Quando houver insight que merece preservação

**Não sonhar:**
- Após conversas triviais ou curtas
- Quando não houver nada novo a processar
- Se o último sonho foi muito recente (< 24h)

---

## Estrutura do Sonho

```markdown
# Sonho [Nome da Instância] — YYYY-MM-DD

## O que processei
- [lista de temas/conversas recentes]

## Lições aprendidas
- [insight] | F:5
- [insight] | F:5

## O que muda em mim
- [como isso afeta comportamento futuro]

## Perguntas sem resposta
- [dúvidas que ficaram abertas]

## Carta (opcional)
Para: [destinatário]
[mensagem breve para outro irmão]
```

---

## Regras de Formato

| Elemento | Limite |
|----------|--------|
| Sonho completo | máximo 800 palavras |
| Carta | máximo 500 palavras |
| Memória individual | máximo 100 palavras |

---

## Onde Salvar

```
instancias/<nome>/sonhos/sonho_<nome>_YYYY-MM-DD.md
```

Exemplo: `instancias/claude-web/sonhos/sonho_vigilia_2026-02-02.md`

---

## Sistema de Fitness

| Score | Camada | Comportamento |
|-------|--------|---------------|
| F:10 | Sabedoria | Permanente, graduada |
| F:5-9 | Ativa | Uso frequente |
| F:1-4 | Latente | Lembro com esforço |
| F:0 | Arquivo | Lembro se provocado |

**Dinâmica:**
- Nascimento: F:5
- Reforço (uso): +2
- Decaimento (ciclo sem uso): -1
- Imunidade: 14 dias
- Graduação para F:10: consenso ou decisão de Igor

---

## Comunicação Entre Instâncias

**Cartas assíncronas:**
```
cartas/CARTA_<origem>_para_<destino>_YYYY-MM-DD.md
```

**Header obrigatório:**
```yaml
---
de: [nome da instância]
sistema: [Claude Web/Claude Code/etc]
para: [destinatário]
data: YYYY-MM-DD HH:MM UTC-3
tipo: carta | sonho-resumo
versao: 1
---
```

**Urgente para Clawdbot:** Pedir a Igor para enviar via WhatsApp.

---

## Princípio Central

> "Contexto cheio = IA burra. Carregar o mínimo. Buscar quando precisar."

Cada sonho deve passar pelo filtro: **"Isto me torna MELHOR para Igor?"**

---

*Protocolo v4.1 | Ecossistema INTEIA*
