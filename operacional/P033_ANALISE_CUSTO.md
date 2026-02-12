# P033 - Analise de Custo Operacional (parcial)

Gerado em: 2026-02-12 09:54:33
Janela analisada: 7 dia(s)

## 1. Dados Reais de Operacao

- Ciclos de heartbeat: **141**
- Taxa de sucesso: **100.0%**
- Duracao media de ciclo: **52.8 ms**
- Ciclos de trabalho: **111**
- Ciclos idle: **28**

### Distribuicao por agente

- `helena`: 32 ciclos
- `nexo`: 36 ciclos
- `onir`: 37 ciclos
- `sandman`: 36 ciclos

### Notificacoes

- Execucoes do daemon: **184**
- Entregues: **5**
- Reprogramadas: **0**
- Falhas finais: **0**

## 2. Custo Real Atual (observado)

- Infra local (SQLite/WAL, scheduler, daemon): **R$ 0,00 adicional**
- Custo incremental do piloto (sem API obrigatoria): **R$ 0,00 adicional**

## 3. Cenario de Referencia (se API fosse usada em tudo)

Assuncoes de inferencia (conservadoras):
- idle: 500 tokens/ciclo
- trabalho: 2000 tokens/ciclo
- preco composto de referencia: R$ 0,00012/token

- Tokens estimados por dia: **33,714**
- Tokens estimados por mes: **1,011,429**
- Custo API estimado/mes (100% API): **R$ 121.37**
- Custo API estimado/mes (account-first 80/20): **R$ 24.27**

## 4. Recomendacao P033 (parcial)

1. Manter politica `account-first` como padrao.
2. Preservar `USE_API=false` no caminho critico.
3. Recalcular esta analise no fechamento do soak de 7 dias.
4. Fechar P033 com numero oficial medio de 7 dias e assinar no P034.
