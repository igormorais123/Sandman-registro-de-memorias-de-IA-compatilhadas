# Towards Execution-Grounded Automated AI Research

**Fonte:** @theartificialintelligens (Instagram)
**Data:** 2025-02-02 (há 2 dias do post)
**Salvo:** 2025-02-04 02:27

## Paper

**Título:** Towards Execution-Grounded Automated AI Research

**Autores:** Chenglei Si, Zitong Yang, Yejin Choi, Emmanuel Candès, Diyi Yang, Tatsunori Hashimoto (Stanford)

## Resumo

O paper propõe um **Automated Idea Executor** que:
1. Pega ideias de pesquisa geradas por LLMs
2. Transforma em código executável
3. Roda experimentos em GPU paralelas
4. Usa os resultados como feedback para melhorar as ideias

### Arquitetura
- **Implementer:** Multi-threaded LLM API query
- **Scheduler:** Resource allocation for execution queue
- **Worker:** GPU pre-train/post-train job
- **Automated AI Researcher:** Ideator update via evolutionary search/RL

### Métodos de Aprendizado
1. **Evolutionary search** (execution-guided) - Sample-efficient
2. **Reinforcement learning** - Continuous improvement

### Resultados
- Outperforms GRPO baseline (69.4% vs 48.0%) em post-training
- Encontra receita de pre-training que supera nanoGPT baseline (19.7 min vs 35.9 min)
- Tudo em apenas 10 epochs de busca

## Relevância para INTEIA

Este paper é MUITO relevante para o sistema de pesquisa eleitoral:
- Mostra como automatizar pesquisa de IA
- Feedback loop entre ideias e execução
- Pode informar como evoluir os agentes sintéticos
- Conceito de "execution grounding" = ideias validadas por código real

## Link (buscar)
Provavelmente em arxiv.org - buscar por "Execution-Grounded Automated AI Research Chenglei Si"
