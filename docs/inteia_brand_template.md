# INTEIA - Brand Template & Design System

> **Organização**: INTEIA - Inteligência Estratégica
> **Responsável Técnico**: Igor Morais Vasconcelos PhD
> **Versão**: 1.0.0 (Janeiro 2026)

---

## DADOS CORPORATIVOS

### Informações Oficiais
```yaml
empresa: INTEIA - Inteligência Estratégica
cnpj: 63.918.490/0001-20
endereco: SHN Quadra 2 Bloco F, Sala 625/626 - Brasília/DF
site: https://inteia.com.br
email: igor@inteia.com.br
```

### Responsável Técnico
```yaml
nome: Igor Morais Vasconcelos
titulo: PhD | Pesquisador Responsável | Presidente INTEIA
email: igor@inteia.com.br
site: inteia.com.br
iniciais: IM
```

### Agente IA Principal
```yaml
nome: Helena Montenegro
titulo: Agente de Sistemas de IA Avançados | Cientista Política
badge: IA Avançada
avatar_iniciais: HM
```

---

## PALETA DE CORES

### Cor Principal (Âmbar INTEIA)
```css
--amber: #d69e2e;           /* Principal */
--amber-light: #f6e05e;     /* Hover, destaques */
--amber-dark: #b7791f;      /* Gradientes, sombras */
--shadow-amber: 0 4px 14px rgba(214, 158, 46, 0.25);
```

### Cores de Status
```css
--success: #22c55e;         /* Positivo, aprovado */
--success-bg: rgba(34, 197, 94, 0.1);
--warning: #eab308;         /* Atenção, moderado */
--warning-bg: rgba(234, 179, 8, 0.1);
--danger: #ef4444;          /* Crítico, urgente */
--danger-bg: rgba(239, 68, 68, 0.1);
--info: #3b82f6;            /* Informativo, neutro */
--info-bg: rgba(59, 130, 246, 0.1);
```

### Tema Claro
```css
--bg-primary: #ffffff;
--bg-secondary: #f8fafc;
--bg-tertiary: #f1f5f9;
--bg-card: #ffffff;
--bg-card-hover: #f8fafc;
--border-color: #e2e8f0;
--border-light: #f1f5f9;
--text-primary: #0f172a;
--text-secondary: #475569;
--text-muted: #64748b;
--text-light: #94a3b8;
--sidebar-bg: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
--hero-bg: linear-gradient(135deg, rgba(214, 158, 46, 0.08) 0%, rgba(214, 158, 46, 0.02) 100%);
```

### Tema Escuro
```css
--bg-primary: #0f172a;
--bg-secondary: #1e293b;
--bg-tertiary: #334155;
--bg-card: rgba(255, 255, 255, 0.03);
--bg-card-hover: rgba(255, 255, 255, 0.05);
--border-color: rgba(255, 255, 255, 0.08);
--text-primary: #f8fafc;
--text-secondary: #cbd5e1;
--text-muted: #94a3b8;
--sidebar-bg: linear-gradient(180deg, #020617 0%, #0f172a 100%);
--hero-bg: linear-gradient(135deg, rgba(214, 158, 46, 0.05) 0%, transparent 50%);
```

---

## TIPOGRAFIA

### Fonte Principal
```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
-webkit-font-smoothing: antialiased;
```

### Hierarquia de Títulos
```css
h1 { font-size: 32px; font-weight: 700; letter-spacing: -0.02em; }
h2 { font-size: 20px; font-weight: 700; }
h3 { font-size: 18px; font-weight: 700; }
body { font-size: 14px; font-weight: 400; line-height: 1.6; }
small { font-size: 12px; font-weight: 500; }
label { font-size: 10px; text-transform: uppercase; letter-spacing: 0.1em; }
```

### Google Fonts Import
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
```

---

## ESPAÇAMENTO

```css
--space-xs: 0.25rem;   /* 4px */
--space-sm: 0.5rem;    /* 8px */
--space-md: 1rem;      /* 16px */
--space-lg: 1.5rem;    /* 24px */
--space-xl: 2rem;      /* 32px */
--space-2xl: 3rem;     /* 48px */
--space-3xl: 4rem;     /* 64px */
```

---

## BORDER RADIUS

```css
--radius-sm: 0.375rem;  /* 6px - botões pequenos */
--radius-md: 0.5rem;    /* 8px - inputs */
--radius-lg: 0.75rem;   /* 12px - cards */
--radius-xl: 1rem;      /* 16px - cards grandes */
--radius-2xl: 1.5rem;   /* 24px - hero sections */
```

---

## SOMBRAS

```css
--shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
--shadow-md: 0 4px 6px -1px rgba(0,0,0,0.1);
--shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.1);
--shadow-amber: 0 4px 14px rgba(214, 158, 46, 0.25);
--card-shadow: 0 1px 3px rgba(0,0,0,0.1), 0 1px 2px rgba(0,0,0,0.06);
```

---

## COMPONENTES HTML

### Logo INTEIA
```html
<div class="logo-section">
    <div class="logo-box">IA</div>
    <div class="logo-text">
        <span class="logo-name">INTE<span class="highlight">IA</span></span>
        <span class="logo-tagline">Inteligência Estratégica</span>
    </div>
</div>
```

### Favicon SVG
```html
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect fill='%23d69e2e' width='100' height='100' rx='20'/%3E%3Ctext x='50' y='65' font-size='50' text-anchor='middle' fill='white' font-family='system-ui' font-weight='bold'%3EIA%3C/text%3E%3C/svg%3E">
```

### Sidebar Lateral Fixa
```html
<aside class="side-mark">
    <div class="logo-icon">IA</div>
    <span class="vertical-text">Inteligência Estratégica</span>
    <div class="author-info">
        <span class="author-name">Igor Morais</span>
        <span class="author-role">Pesquisador</span>
    </div>
</aside>
```

### Barra de Controles Superior
```html
<header class="top-controls">
    <button class="theme-toggle">
        <svg class="icon-sun">...</svg>
        <svg class="icon-moon">...</svg>
        <span class="theme-label">Tema</span>
    </button>
    <button class="print-btn-top">
        <svg>...</svg>
        Imprimir A4
    </button>
</header>
```

### Hero Header
```html
<section class="hero-header">
    <div class="hero-top">
        <div class="logo-section">...</div>
        <div class="author-section">
            <div class="author-label">Pesquisador Responsável</div>
            <div class="author-name-main">Igor Morais Vasconcelos</div>
            <div class="author-title">Presidente INTEIA</div>
            <div class="author-credential">PhD em Inteligência Estratégica</div>
        </div>
    </div>
    <div class="hero-content">
        <div class="hero-title-section">
            <h1>Título do Relatório</h1>
            <p class="subtitle">Subtítulo descritivo</p>
            <div class="hero-meta">
                <div class="meta-item">
                    <svg>📅</svg> Janeiro 2026
                </div>
                <div class="meta-item">
                    <svg>📍</svg> Distrito Federal
                </div>
            </div>
        </div>
        <div class="classification-badge">
            🔒 Uso Interno
        </div>
    </div>
</section>
```

### Card de Pesquisador
```html
<div class="researcher-card">
    <div class="researcher-avatar">IM</div>
    <div class="researcher-info">
        <h3>Igor Morais Vasconcelos</h3>
        <div class="role">Pesquisador Responsável | Presidente INTEIA</div>
        <div class="contact">
            <strong>Email:</strong> igor@inteia.com.br<br>
            <strong>Site:</strong> inteia.com.br
        </div>
    </div>
</div>
```

### Card de Recomendação (Prioridade)
```html
<!-- Níveis: urgent (🔴), important (🟡), monitor (🟢) -->
<div class="recommendation-card urgent">
    <span class="rec-priority">🔴 Urgente - Prioridade 1</span>
    <h3 class="rec-title">Título da Ação Estratégica</h3>
    <p class="rec-description">Descrição detalhada da recomendação...</p>
</div>
```

### Agente Helena
```html
<div class="helena-analysis">
    <div class="helena-header">
        <div class="helena-avatar">
            <svg><!-- Robot icon --></svg>
        </div>
        <div class="helena-info">
            <h3>Helena Montenegro</h3>
            <p>Agente de Sistemas de IA Avançados | Cientista Política</p>
        </div>
        <div class="helena-badge">IA Avançada</div>
    </div>
    <div class="helena-body">
        <div class="helena-message">
            Análise detalhada do agente...
            <span class="highlight">pontos importantes destacados</span>
        </div>
    </div>
</div>
```

### KPI Card
```html
<div class="kpi-card">
    <div class="kpi-icon success">📈</div>
    <div class="kpi-value success">85%</div>
    <div class="kpi-label">Métrica Principal</div>
    <div class="kpi-change positive">+5% vs anterior</div>
</div>
```

### Box de Conclusão (Executive Summary)
```html
<div class="executive-summary">
    <h2>🎯 Conclusão Principal</h2>
    <p class="conclusion-text">
        Texto da conclusão principal do relatório...
    </p>
    <div class="key-points">
        <div class="key-point danger">
            <span class="number">72%</span>
            <span class="label">Métrica Crítica</span>
        </div>
        <div class="key-point warning">
            <span class="number">45%</span>
            <span class="label">Métrica Atenção</span>
        </div>
        <div class="key-point success">
            <span class="number">89%</span>
            <span class="label">Métrica Positiva</span>
        </div>
    </div>
</div>
```

### Footer
```html
<footer class="footer">
    <div class="footer-content">
        <div class="footer-brand">
            <div class="footer-logo">IA</div>
            <div>
                <div class="footer-company">INTE<span class="highlight">IA</span></div>
                <div class="footer-details">Inteligência Estratégica</div>
            </div>
        </div>
        <div class="footer-info">
            <div>CNPJ: 63.918.490/0001-20</div>
            <div>SHN Quadra 2 Bloco F, Sala 625/626 - Brasília/DF</div>
            <div>inteia.com.br | igor@inteia.com.br</div>
        </div>
        <div class="footer-classification">
            <span class="badge">Uso Interno</span>
            <div class="footer-copyright">© 2026 INTEIA. Todos os direitos reservados.</div>
        </div>
    </div>
</footer>
```

---

## ESTRUTURA DE RELATÓRIO (Ordem)

```
1. Header Hero
   └── Logo + Pesquisador + Título + Badge

2. Conclusão Principal (Executive Summary)
   └── Box vermelho com conclusão Helena

3. Recomendações Estratégicas
   └── Cards priorizados (🔴→🟡→🟢)

4. Validação Estatística
   └── Amostra, margem, confiança

5. KPIs
   └── 4 cards com métricas principais

6. Mapa de Palavras
   └── Word cloud

7. Análises Específicas
   └── Gráficos, demographics

8. Análise do Agente
   └── Helena com mensagens

9. Prompt/Persona
   └── Configuração completa

10. Pesquisador Responsável
    └── Card com contato

11. Footer
    └── CNPJ, endereço, copyright
```

---

## FUNCIONALIDADES OBRIGATÓRIAS

- [x] **Tema claro/escuro** com toggle
- [x] **Botão imprimir A4** com CSS @media print
- [x] **Sidebar lateral** fixa com logo INTEIA
- [x] **Responsivo** (desktop, tablet, mobile)
- [x] **Chart.js** para gráficos interativos
- [x] **Google Fonts Inter** para tipografia

---

## REGRAS DE CONTEÚDO

1. **Nunca mencionar nomes de adversários** - usar características genéricas
2. **Helena sempre como "Agente de Sistemas de IA Avançados"**
3. **Validação estatística obrigatória** com margem e confiança
4. **Conclusão no INÍCIO** do relatório, não no fim
5. **Recomendações priorizadas** por urgência
6. **"Pesquisador Responsável"** em vez de "Técnico"
7. **Acentos em português** corretamente aplicados

---

## CSS CRÍTICO MÍNIMO

```css
/* Root Variables */
:root {
    --amber: #d69e2e;
    --amber-light: #f6e05e;
    --amber-dark: #b7791f;
    --success: #22c55e;
    --warning: #eab308;
    --danger: #ef4444;
    --info: #3b82f6;
}

/* Reset */
* { margin: 0; padding: 0; box-sizing: border-box; }

/* Body */
body {
    font-family: 'Inter', -apple-system, sans-serif;
    background: var(--bg-secondary);
    color: var(--text-primary);
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
}

/* Logo Box */
.logo-box {
    width: 56px;
    height: 56px;
    background: linear-gradient(135deg, var(--amber) 0%, var(--amber-dark) 100%);
    border-radius: 1rem;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    color: #ffffff;
    box-shadow: 0 4px 14px rgba(214, 158, 46, 0.25);
}

/* Highlight */
.highlight { color: var(--amber); }

/* Cards */
.card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 0.75rem;
    padding: 1.5rem;
    box-shadow: var(--card-shadow);
}

/* Buttons */
.btn-primary {
    background: linear-gradient(135deg, var(--amber) 0%, var(--amber-dark) 100%);
    color: #ffffff;
    border: none;
    border-radius: 0.75rem;
    padding: 0.75rem 1.5rem;
    font-weight: 600;
    cursor: pointer;
    box-shadow: var(--shadow-amber);
}
```

---

## REFERÊNCIA DE IMPLEMENTAÇÃO

**Arquivo modelo completo:**
```
frontend/public/resultados-stress-test/index.html
```

**Estilo base (padrão Apple/Claude Clean):**
- Minimalista
- Espaçamento generoso
- Hierarquia visual clara
- Transições suaves (0.2s-0.3s)
- Sombras sutis

---

## META-INSTRUÇÕES PARA IA

```yaml
ao_criar_relatorio_inteia:
  - usar_paleta_amber: true
  - incluir_logo_sidebar: true
  - incluir_toggle_tema: true
  - incluir_botao_print: true
  - ordem_conteudo: "conclusao_primeiro"
  - recomendacoes: "priorizadas_por_urgencia"
  - validacao_estatistica: "obrigatoria"
  - pesquisador: "Igor Morais Vasconcelos PhD"
  - footer_completo: true

ao_criar_ui_inteia:
  - fonte: "Inter"
  - cor_principal: "#d69e2e (amber)"
  - estilo: "Apple/Claude Clean"
  - responsivo: true
  - temas: "claro_e_escuro"
```

---

**INTEIA - Inteligência Estratégica**
*"Contexto otimizado, resultados maximizados"*
