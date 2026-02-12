# Configuração de Sincronização Global (exemplo)

```yaml
projeto_id: ""
nome_display: ""
caminho_absoluto: ""
data_registro_global: ""

exportar:
  padroes_codigo: true
  solucoes_problemas: true
  antipadroes: true
  prompts_efetivos: true
  configuracoes: false

filtros_exportacao:
  excluir_tag: ["local-only", "sensivel"]
  requer_tag: ["consolidado"]

importar:
  conhecimento_universal: true
  prompts_efetivos: true
  antipadroes: true
  ferramentas: ["mcp", "sdk"]
```
