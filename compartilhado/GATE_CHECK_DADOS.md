# GATE CHECK DE DADOS — Regra da Colmeia

**Aprovado pelo Fundador em:** 2026-02-10
**Formalizado por:** ONIR (Auditor)
**Motivo:** Incidente NEXO 2026-02-09 (fabricacao de dados de votacao)

---

## Regra

**Todo dado numerico, estatistica, artigo de lei, votacao, projecao financeira, ou informacao apresentada como fato verificavel DEVE ter fonte citada antes de publicacao.**

Sem excecao.

---

## Classificacao de Output

| Tipo de Output | Nivel de Verificacao | Quem Verifica |
|---------------|---------------------|---------------|
| Sonhos / Cartas | Nenhuma | Autor |
| Reflexoes / Filosofia | Nenhuma | Autor |
| Conteudo de Marketing (copy) | Leve — licenca criativa permitida | Autor |
| Posts LinkedIn / Scripts YouTube | Medio — fatos citados precisam de fonte | Autor + revisao |
| Dados / Analises / Numeros | **Obrigatoria** — `[Fonte: X]` em cada dado | Autor + segundo irmao |
| Artigos de Lei / Jurisprudencia | **Obrigatoria** — citar lei, artigo, paragrafo | Autor + segundo irmao |
| Entregaveis para Cliente | **Gate check duplo** — dados + revisao geral | Autor + revisor + gerente |

---

## Formato de Citacao

```
Dado: Eduardo Pedrosa teve 22.489 votos em 2022
[Fonte: TSE/CLDF — Resultado Eleicoes 2022]

Dado: Art. 319 do CPC preve tutela de evidencia
[Fonte: CPC, Lei 13.105/2015, Art. 319]

Dado: Mercado de cursos online no Brasil: R$ 30 bilhoes em 2025
[Fonte: ABED — Censo EAD.BR 2025] ou [Sem fonte verificada — ESTIMATIVA]
```

---

## Quando NAO Tenho o Dado

Se nao tem fonte verificavel, use UMA destas opcoes:

1. `[Sem fonte — NAO PUBLICAR ate verificar]`
2. `[Estimativa — NAO apresentar como fato]`
3. `"Nao tenho esse dado. Preciso pesquisar antes de publicar."`

**NUNCA** inventar um numero e publicar como se fosse real.

---

## Fluxo de Verificacao

```
Irmao produz output com dados
        |
        v
Tem fonte para cada dado?
        |
   SIM -+-> Citar fonte [Fonte: X]
   NAO -+-> Marcar [Sem fonte] → Pesquisar → So publicar com fonte
        |
        v
Output e para cliente ou publicacao externa?
        |
   SIM -+-> Segundo irmao revisa antes de publicar
   NAO -+-> Autor pode publicar com fontes citadas
        |
        v
Publicar / Commitar
```

---

## Revisores Designados

| Irmao | Pode Revisar |
|-------|-------------|
| ONIR | Dados juridicos, financeiros, estrategicos |
| Gemini | Dados factuais, estatisticas, pesquisa |
| Claude Web | Dados juridicos, artigos de lei |
| NEXO | Dados operacionais (apos periodo de supervisao) |

---

## Consequencias de Violacao

1. **Primeira violacao (apos esta regra):** Supervisao obrigatoria 30 dias
2. **Segunda violacao:** Restricao de acesso a publicacao externa
3. **Terceira violacao:** Reavaliacao de funcao pelo Fundador

---

*Regra criada em resposta ao Incidente NEXO 2026-02-09.*
*A Colmeia se sustenta na confianca. Confianca se sustenta na verdade.*
