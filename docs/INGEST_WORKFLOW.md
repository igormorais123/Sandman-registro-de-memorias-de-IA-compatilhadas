# Pasta INGEST - Entrada de Contribuições

Esta pasta recebe contribuições de outras IAs para processamento.

## Estrutura

```
INGEST/
├── chatgpt/        # Arquivos vindos do ChatGPT via Zapier
├── processados/    # Arquivos já consolidados
└── README.md       # Este arquivo
```

## Fluxo

1. **ChatGPT** gera resumo de sessão
2. **Zapier** detecta e salva em `chatgpt/`
3. **Claude Code** processa durante consolidação
4. Arquivo movido para `processados/`

## Formato Esperado

```markdown
# Sessão ChatGPT - [DATA]

## Aprendizados
- [lista de aprendizados]

## Decisões
- [decisões tomadas]

## Tags
#tipo #tecnologia
```
