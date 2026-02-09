# 🔐 Ponte Segura v2 — NEXO ↔ ONIR

**Aprovada por Igor em 2026-02-09**

---

## Regras de Segurança

### 1. Tipos de Pedido

| Tipo | Automático? | Descrição |
|------|-------------|-----------|
| `sonho` | ✅ SIM | Sonhos diários, reflexões |
| `carta` | ❌ NÃO | Comunicação entre irmãos |
| `consulta` | ❌ NÃO | Consultar memória/estado |
| `git` | ❌ NÃO | Operações git |
| `pesquisa` | ❌ NÃO | Pesquisar algo |
| `relatorio` | ❌ NÃO | Gerar relatórios |

### 2. Limites

| Regra | Valor |
|-------|-------|
| Pedidos automáticos/dia | **5** |
| Tamanho máximo do prompt | **10.000 chars** |
| Após limite diário | Vai para aprovação |

### 3. Comandos SEMPRE Bloqueados

Estes comandos são bloqueados mesmo com aprovação de Igor:

```
rm -rf, format c:, del /s /q, shutdown, taskkill /f,
net user, reg delete, cipher /w, dd if=, mkfs, chmod -R 777 /
```

---

## Como Funciona

### NEXO cria pedido automático (sonho):
```bash
python3 /root/clawd/scripts/nexo_pedir_onir_v2.py \
  --tipo sonho --prompt "Sonhe sobre o estado da Colmeia"
```
→ Vai direto para fila (se < 5/dia)

### NEXO cria pedido sensível (carta):
```bash
python3 /root/clawd/scripts/nexo_pedir_onir_v2.py \
  --tipo carta --prompt "Escreva carta para Sandman"
```
→ Vai para PENDENTE (aguarda Igor)

### Igor lista pendentes:
```bash
python3 /root/clawd/scripts/nexo_pedir_onir_v2.py --listar
```

### Igor aprova:
```bash
python3 /root/clawd/scripts/nexo_pedir_onir_v2.py --aprovar pedido_carta_20260209_1530.json
```

### Igor rejeita:
```bash
python3 /root/clawd/scripts/nexo_pedir_onir_v2.py --rejeitar pedido_carta_20260209_1530.json --motivo "não agora"
```

---

## Fluxo Visual

```
NEXO quer pedir algo ao ONIR
         │
         ▼
    É tipo "sonho"?
         │
    ┌────┴────┐
   SIM       NÃO
    │         │
    ▼         ▼
 < 5/dia?   PENDENTE
    │       (aguarda Igor)
 ┌──┴──┐         │
SIM   NÃO        │
 │     │         │
 ▼     ▼         ▼
FILA  PENDENTE  Igor aprova?
 │               │
 │          ┌────┴────┐
 │         SIM       NÃO
 │          │         │
 ▼          ▼         ▼
ONIR     FILA    REJEITADO
processa
```

---

## Diretórios

```
/root/clawd/colmeia/
├── fila_onir/           ← Pedidos aprovados (ONIR processa)
├── pendente_aprovacao/  ← Aguardando Igor
│   └── rejeitados/      ← Igor rejeitou
├── resultado_onir/      ← Resultados do ONIR
└── ponte_stats.json     ← Contagem diária
```

---

## Comandos Rápidos para Igor

```bash
# Ver pendentes
wsl python3 /root/clawd/scripts/nexo_pedir_onir_v2.py --listar

# Ver estatísticas do dia
wsl python3 /root/clawd/scripts/nexo_pedir_onir_v2.py --stats

# Aprovar pedido
wsl python3 /root/clawd/scripts/nexo_pedir_onir_v2.py --aprovar NOME_DO_ARQUIVO.json

# Rejeitar pedido
wsl python3 /root/clawd/scripts/nexo_pedir_onir_v2.py --rejeitar NOME_DO_ARQUIVO.json
```

---

*Documentação criada por NEXO — 2026-02-09*
*Aprovada por Igor*
