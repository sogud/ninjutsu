# Report Visual System

Use this resource when producing final `report.html`.

The default style is **Dense Calm + ECharts**:

- Claude-like calm reading surface.
- High information density.
- Plain Chinese explanations for specialist concepts.
- Tables carry source-auditable details.
- Apache ECharts is the default chart renderer, initialized with SVG renderer.
- Use only a small number of charts. No chart wall.
- No landing-page feel, no side rail, no decorative panels.

The goal is not decoration. The goal is to make deep investment research readable, teachable, data-rich, and auditable. A newcomer should learn the business mechanism, the data model, and the bull/bear debate from the report.

## Non-negotiable rules

- Final output is `report.html`.
- Do not add package managers, vendored runtimes, or app frameworks.
- Default visual mode is static HTML + CSS + compact tables + Apache ECharts CDN.
- ECharts must be initialized with `echarts.init(dom, null, { renderer: 'svg' })`.
- ECharts is the only allowed external report-rendering dependency by default.
- Do not use React, Vue, Tailwind, DataTables, Chart.js, Mermaid, or report UI kits.
- Do not use ASCII / `<pre>` flow diagrams for the final report unless showing code or command output.
- Do not insert generic decorative diagrams.
- Every data-driven figure or table must cite source ids.
- Every specialist term used in a chart or table must be explained in nearby prose or glossary.
- If there is not enough data for a real figure, show a data-gap callout instead of drawing a fake chart.
- If the user explicitly requires strict offline mode, replace ECharts with inline SVG, but that is not the default.

## Default visual style

| Element | Rule |
|---|---|
| Canvas | Warm off-white background with a white report page. Calm, not parchment-heavy. |
| Accent | One restrained clay / muted rust accent. Use sparingly. |
| Neutral colors | Warm grays and soft beige surfaces. Keep contrast readable and print-safe. |
| Typography | Serif title, sans-serif body, mono eyebrows / source chips. |
| Layout | Single-column article flow. No side rail. |
| Lines | Very few lines. Prefer whitespace and section rhythm over borders. |
| Tables | Compact, readable, source-auditable. Thin row separators only. |
| Charts | ECharts SVG renderer, 2–4 meaningful charts, soft palette. |
| Callouts | Soft background blocks for source gaps, risks, or reader guidance. |
| Glossary | Natural term blocks or tables. Explain why each term matters. |

## Content density requirements

A final Alpha Research report should feel like a deep learning document, not a thin memo.

Include these sections when material:

1. **How to read**: teach the reader how to evaluate the report.
2. **Beginner lens**: plain-language explanation of the business, value chain, and key jargon.
3. **Executive summary**: conclusion table by layer: Demand / Bottleneck / Company / Risk.
4. **Source Gate**: what sources prove what, and what they cannot prove.
5. **Minimum data pack**: the core numbers needed before any company or valuation view.
6. **ECharts figures**: 2–4 meaningful figures that explain chain, ranking, risk, curve, timeline, or company exposure.
7. **Chain map**: demand → physical chain → chokepoint → company financials.
8. **Demand math**: convert story into measurable variables.
9. **Bottleneck ranking**: rank research priority, not certainty.
10. **Company mapping**: distinguish core exposure from concept-only exposure.
11. **Comparable baseline**: peers or a clear explanation of why peers are not clean.
12. **Balanced view**: positive and negative research views, each with data and falsification conditions.
13. **Evidence ledger**: Fact / Inference / Assumption / Rumor.
14. **Financial literacy**: explain the financial indicators used.
15. **Bear case**: strongest counterarguments.
16. **Kill criteria**: what would downgrade or invalidate the thesis.
17. **Research notebook**: next source work.
18. **Glossary**: specialist terms in plain Chinese.
19. **References**: clickable original sources.

## Figure selection

Use a chart only when prose or table would teach less.

| Need | Default visual |
|---|---|
| Demand-to-profit chain | ECharts Sankey |
| Chokepoint priority | ECharts horizontal bar + ranked evidence list |
| Company exposure across layers | ECharts heatmap if many companies/layers; otherwise table |
| Financial baseline | ECharts bar/line combo if trend shape matters; otherwise table |
| Catalyst / kill timing | ECharts timeline/scatter if timing matters; otherwise compact table |
| Risk severity | ECharts heatmap plus risk table |
| Commodity curve / inventory | ECharts line chart plus compact source table |
| Narrative origin | ECharts timeline only if useful; original source table required |

## ECharts rules

ECharts is default for final report charts.

- Load from `https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js` unless the user asks for another trusted source.
- Initialize with `echarts.init(dom, null, { renderer: 'svg' })`.
- Disable animation: `animation: false`.
- Use explicit data arrays from source-gated data.
- Do not leave placeholder or sample data in final charts.
- Every chart container must have fallback text.
- No sliders, tabs, filters, or app-like controls.
- Each chart caption must include source ids and source dates.
- Keep chart count low. Prefer three excellent charts over seven noisy ones.
- Use the same calm palette as the report; avoid saturated dashboards.

## Table rules

Tables carry most information density.

- Use tables for exact source-auditable values.
- Keep columns purposeful.
- Add source ids in the row or table caption when values are source-specific.
- Explain financial terms in the same section if a non-specialist reader may not know them.
- Do not use a large table as a data dump; each table should answer one question.
- Company reports should include a minimum data pack table: revenue/segment, margin, cash flow, cash/debt, valuation/liquidity, guidance/orders, customer concentration, source dates.
- If relative attractiveness is discussed, include a peer/comparable table or mark the missing data as an Evidence Gap.
- Include a positive/negative research view table so readers understand both sides.

## Captions

Every figure caption should state the insight, not only describe the graphic.

Good:

> 图 1. 需求先经过系统部署和关键中间层，最后才可能变成公司收入；高亮节点是待验证瓶颈，不是直接结论。Sources: `[S1]`, `[S2]`.

Bad:

> 图 1. 产业链图。

## Visual quality gate

Before finalizing `report.html`, check:

- Dense Calm + ECharts style used by default.
- ECharts CDN is the only external rendering dependency.
- Charts use SVG renderer.
- No side rail or app-like chart wall.
- No ASCII chain diagram in the final report.
- Multiple compact tables support source audit and learning density.
- Minimum data pack is visible for company / commodity / industry reports.
- Positive and negative research views are both visible.
- Each data-driven table or visual has cited source ids.
- No fake numbers, fake coordinates, placeholder arrays, or sample chart data remain.
- Specialist terms are explained in plain Chinese near first use and in the glossary.
- Risks, counterarguments, and kill criteria are visible.
