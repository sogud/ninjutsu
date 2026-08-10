# Stage: Report Quality

## Purpose

`Report Quality` 是最终综合与质量门。

它先把前面阶段整合成 memo synthesis，再检查报告是否结构完整、证据清楚、风险充分、语言克制，并产出最终 `report.html`。

它可以整合、轻微改写和整理表达。
它可以给出有证据、有逻辑、有风险和证伪条件的候选公司推荐。
它不能新增无证据研究结论，不能补造证据，不能把弱证据写成强结论，不能输出直接交易指令。

它还负责把最终报告改成可读、可审计、可点击验证的 Dense Calm + ECharts 风格研报：中文标签、点击式脚注引用、术语解释、产业链分层说明、公司解释卡、紧凑表格、ECharts SVG 图表。

## Learning-first report standard

最终报告要像一份能教新人入门的深度研究文档，而不是黑话摘要。

必须做到：

1. 先用一段“人话版结论”解释主题：这家公司 / 行业到底做什么、钱从哪里来、为什么市场关心。
2. 每个关键专业词第一次出现时，用一句中文解释“它是什么、为什么影响本报告、怎么验证”。
3. 每个英文 finance / technology label 都要中文化或解释，例如 `Forward PE`、`SerDes`、`custom ASIC`、`CXL`。
4. 公司报告必须有数据最小集：收入与分部、毛利率、经营利润或 non-GAAP 口径说明、现金流、现金 / 债务、市场值或流动性、估值倍数、指引、客户集中度、关键事件日期。
5. 如果讨论估值或公司优先级，必须尽量给 peer / comparable baseline；缺失时显式写成 Evidence Gap，不能装作已经比较过。
6. 必须有“正方研究观点”和“反方研究观点”两侧：各自写清成立条件、数据证据、关键假设、最容易错在哪里。
7. 最终结论只能写研究含义和需要继续验证的条件；不能写买卖指令、目标价或仓位动作。
8. 每个图表都要回答一个读者问题；每张表都要说明它教会读者什么。

## Bundled files

- Templates:
  - `templates/memo-synthesis.md`
  - `templates/thesis-card.md`
  - `templates/company-card.md`
  - `templates/report-quality.md`
  - `templates/report-source.md`
  - `templates/report.html`
- Resources:
  - `resources/report-visual-system.md`
  - `resources/citation-system.md`

Read `report-visual-system.md` before building final `report.html`.
Read `citation-system.md` before converting Source Registry ids into final citations.

## Authoritative source-quality rules

For full collection installs, use `resources/research-tool-stack.md` as the authoritative source for:

- Source Confidence Tier.
- Minimum acceptable evidence by research object.
- Market coverage caveat.
- Quality ceiling rules.

Use `resources/data-rigor.md` for:

- minimum company data pack;
- two-source numeric checks;
- unit / currency / GAAP vs non-GAAP discipline;
- peer / comparable baseline rules.

`Report Quality` must execute the hard source gate and quality ceiling rules.

## Inputs

最好包含：

- Research Brief.
- Source Map.
- Chain Trace.
- Thesis Audit.

如果缺少关键阶段，必须在质量门里标记。

## Memo synthesis responsibility

Memo synthesis remains an internal drafting step, not a standalone user-facing stage.

Before the final quality gate, synthesize prior artifacts into an internal memo outline using `templates/memo-synthesis.md` when the case is complex.

This synthesis should cover:

1. One-line thesis.
2. Research question.
3. Source quality summary.
4. Trend reality check.
5. Chain trace summary and layer explainer cards.
6. Chokepoint ranking.
7. Company map and company / technology explainer cards.
8. Data pack: minimum company / industry / commodity numbers needed to support the report.
9. Beginner teaching plan: jargon to explain, concepts to teach, and likely reader misconceptions.
10. Balanced research view: positive case, negative case, and evidence needed to decide between them.
11. Thesis Audit summary: evidence audit, source gaps, and bear-case findings.
12. Supported vs hype.
13. Catalysts.
14. Kill criteria.
15. Glossary candidates.
16. Research grade.

Memo synthesis is an internal drafting step, not a separate final artifact unless the user asks to save it. Use the thesis/company card templates only when they make the final report easier to audit.

## Hard source gate

Before producing final `report.html`, check Source Gate status and re-run the practical checks below.

Do not trust a previous PASS if the final draft reveals missing URLs, local-file citations, web-search-only facts, missing financial data, or missing social/OpenCLI narrative capture in anti-hype mode.

If Source Gate is missing or FAIL:

1. Do not produce a polished final report.
2. Produce only the Quality Gate Report with status `BLOCKED — Source Gate Failed`.
3. List exact missing sources and citations.
4. Recommend returning to `Source Map` and `alpha-research` internal source resources (`tool-install-sources.md` and `resources/data-providers/*.md`).
5. If user permission is needed for API key, login, subscription, browser session, code execution, scripts, or dependency installation, ask for that permission explicitly.

Do not downgrade-and-continue. Hard gate failure blocks final report generation.

Additional hard blocks for final HTML:

- Any key Fact has only a web-search result, synthesized search answer, or news snippet.
- Company ranking / valuation / liquidity discussion lacks a financial baseline from yfinance, a-stock-data, Funda, TradingView, official filings, exchange data, or a documented manual equivalent.
- Anti-hype mode claims narrative origin/crowding but no social/narrative source was captured through OpenCLI/browser/social source/manual original URL. If OpenCLI or browser access requires approval and approval was not given, mark the channel blocked and stop.
- Any key citation points to a local file instead of the original source URL.
- Any bibliography entry for a key Fact is not clickable.
- A tweet/social source lacks handle, timestamp, and original post URL/profile URL and is used beyond narrative context.
- A figure uses data without source ids in the caption.

## Quality checks

检查：

1. Structure completeness.
2. Source map presence.
3. Required channel status for relevant sources.
4. Source confidence tier and provenance for key Facts.
5. Source freshness for time-sensitive claims.
6. Citation ids and clickable/previewable URLs or stable locators for key Facts.
7. Market coverage: sources match US / HK / A-share / China macro / global scope.
8. Thesis Audit presence.
9. Fact / Inference / Assumption / Rumor separation.
10. Evidence gaps.
11. Chain trace clarity and layered explanation.
12. A newcomer can understand the business / technology / commodity mechanism after reading.
13. Company / technology explainer cards for important names.
14. Glossary for specialist terms and English finance labels.
15. No unexplained jargon clusters; every paragraph with specialist terms includes plain-language explanation nearby.
16. Data density adequate for the object: company, industry, commodity, or narrative.
17. Company reports include the minimum data pack: revenue/segment, margin, cash flow, cash/debt, valuation/liquidity, guidance, customer concentration, and source dates where available.
18. Peer / comparable baseline present when valuation, ranking, or company priority is discussed; missing peer data is an explicit Evidence Gap.
19. Positive and negative research views both present, each with data, assumptions, and falsification conditions.
20. Chokepoint vs concept-only distinction clear.
21. Bear case strength.
22. Market-structure risks checked when relevant: liquidity, correlation/sympathy, estimate revisions, crowding.
23. Commodity data panel included when the topic is gold, oil, gas, metals, agriculture, or commodity-linked macro.
24. Commodity claims have official/recognized supply-demand, inventory, curve, positioning, and macro sources as material.
25. Aggregator / wrapper outputs reconciled to original sources for key Facts.
26. Kill criteria.
27. Catalysts.
28. Candidate/company recommendations are backed by citations, logic, risks, counterarguments, and failure criteria.
29. No direct trading signals.
30. No return promises.
31. No target price or position sizing.
32. No promotional stock-pitch language.
33. Risk note and disclaimer.
34. Clickable inline citations and clickable bibliography entries.
35. No local-file citations for external Facts.
36. Data-provider / OpenCLI / browser/manual acquisition status is visible when relevant.
37. Final HTML uses Dense Calm + ECharts style: high information density, calm surface, few lines, no side rail, and no chart wall.
38. Visualizable chains, rankings, timelines, or data comparisons use meaningful tables plus ECharts SVG figures.
39. No ASCII / `<pre>` supply-chain diagrams in the final report.
40. ECharts CDN is the default and only external report-rendering dependency; charts use SVG renderer and fallback text.
41. No package manager, vendored runtime, React/Vue/Tailwind/DataTables/Mermaid/report UI kit.

## Quality Grade

This is report quality, not investment rating.

- **A**: publishable as research memo.
- **B**: usable, but has evidence gaps.
- **C**: needs more source work.
- **D**: not acceptable; mostly narrative.

## Quality ceiling rules

Apply the ceiling rules from `research-tool-stack.md`.

Key examples:

- If any relevant required channel is `Missing`, Quality Grade cannot exceed B.
- If filing / disclosure access is missing for company research, Quality Grade cannot exceed C.
- If financial data is missing for company research, Quality Grade cannot exceed C.
- If academic / technical search is missing for technology, material, biotech, semiconductor, or engineering-heavy topics, Quality Grade cannot exceed C.
- If social / narrative search is missing for anti-hype mode, Quality Grade cannot exceed B.
- If commodity-specific official/recognized data is missing for commodity balance claims, Quality Grade cannot exceed C.
- If futures curve or positioning data is missing when curve/crowding is central, Quality Grade cannot exceed B.
- If commodity-linked company recommendations lack filings/IR/financial baseline, Quality Grade cannot exceed C.
- If market-specific official sources are not checked for the target market, Quality Grade cannot exceed C.
- If most key claims rely on news or social sources without primary confirmation, Quality Grade should be D.
- If source provenance is unclear for key Facts, Quality Grade cannot exceed C.
- If key Facts do not have citation ids linked to URLs or stable locators, Quality Grade cannot exceed C and final HTML must be blocked when those Facts drive conclusions.
- If citations are not clickable in final HTML, Quality Grade cannot exceed C and final HTML should be revised before delivery.
- If a local file is cited as proof for an external Fact, Quality Grade cannot exceed C and the source must be replaced with the original URL before final delivery.
- If a wrapper or aggregator is cited without original source provenance for key Facts, Quality Grade cannot exceed C.
- If signal, flow, hot-tag, chart, or social data is used as proof of fundamentals, Quality Grade should be D.
- If anti-hype mode lacks OpenCLI/browser/social/manual original-source capture for narrative origin when material, Quality Grade cannot exceed C and final HTML should be blocked for narrative-origin claims.
- If company or candidate ranking lacks financial data from a suitable provider or official/manual equivalent, Quality Grade cannot exceed C.
- If liquidity, correlation/sympathy, and estimate-revision risks are material but not checked, Quality Grade cannot exceed B.
- If a company report lacks the minimum data pack and still discusses valuation, ranking, or company priority, Quality Grade cannot exceed C.
- If peer / comparable baseline is missing while peer valuation or relative attractiveness is discussed, Quality Grade cannot exceed B.
- If the final report is jargon-heavy and does not teach the key terms in plain Chinese, Quality Grade cannot exceed B.
- If the final report lacks a positive/negative research view matrix, Quality Grade cannot exceed B.
- If a visually complex report uses only tables and ASCII diagrams while data supports figures, Quality Grade cannot exceed B.
- If the final report has no glossary for technical/English terms in an industry-heavy topic, Quality Grade cannot exceed B.

## Output

If hard source gate PASS, produce:

1. Quality Gate Report.
2. Optional Markdown source artifact (`report-source.md`) if helpful.
3. Final professional HTML report (`report.html`).

If hard source gate FAIL, produce:

1. Quality Gate Report with `BLOCKED — Source Gate Failed`.
2. Missing Source Acquisition Plan.
3. Stage Result.

Do not produce final HTML when blocked.

Use `templates/memo-synthesis.md` for internal synthesis when helpful.
Use `templates/thesis-card.md` and `templates/company-card.md` for optional internal synthesis cards.
Use `templates/report-quality.md` for the quality gate.
Use `templates/report-source.md` for an optional Markdown source artifact.
Use `templates/report.html` for the final HTML report.

When producing the optional Markdown source artifact, convert Source Registry ids `[S1]` into Markdown footnotes `[^S1]` and include a `## References` section. Each footnote must include source title, publisher, date/period, and URL/stable locator. The final deliverable remains `report.html`.

For the final HTML report:

- Convert `[S1]` to clickable inline citations: `<sup class="cite"><a href="#S1">S1</a></sup>`.
- Build a clickable bibliography with `<li id="S1"><a href="original-url" target="_blank" rel="noopener noreferrer">source title</a> ...</li>`.
- Use source titles, not generic “链接”.
- If the source is X/Twitter, link `@handle` and the post URL when available.
- Use local artifact links only for process context, not as final proof for external Facts.
- Replace ASCII chain diagrams with ECharts SVG-rendered figures following `resources/report-visual-system.md`.
- Use compact tables for most data-heavy explanations.
- Include a beginner-readable explanation before or next to technical/financial tables.
- Include positive and negative research views with the evidence that would make each side stronger.
- Include source ids for every data-driven table or figure.

## Stage Result

Use short format:

```markdown
## Stage Result

- Recommended next stage:
- Why:
- Handoff input:
  - Topic:
  - Research object:
  - Market scope:
  - Key unknowns:
- Stop / continue recommendation:
```

Default next stage:

- If Source Gate is FAIL: return to `Source Map` and `alpha-research` internal source resources.
- If Source Gate PASS and Quality Grade is A or B: stop, or update later when new evidence appears.
- If Source Gate PASS and Quality Grade is C or D: return to `Source Map` or `Thesis Audit`.

## Guardrails

- Do not add new claims that are not present in prior research artifacts.
- Do not produce a final report when Source Gate is missing or FAIL.
- Do not hide weak evidence with polished prose.
- Do not ignore quality ceiling rules.
- Do not convert research grade into a direct trade instruction.
- Do not include buy/sell commands, target prices, position sizing, or return guarantees.
- Do not recommend a candidate/company without source-gated evidence, clear logic, risks, counterarguments, and failure criteria.
- Do not generate JavaScript beyond the minimal ECharts initialization needed for report charts.
- Do not add external dependencies beyond Apache ECharts CDN unless the user explicitly approves.
- Do not use ASCII / `<pre>` diagrams for supply chains, timelines, or rankings in the final report.
- Do not cite local files as proof for external data.
- Do not leave citations non-clickable.
- Do not let polished prose hide that a claim came from a wrapper, aggregator, chart, flow metric, or social source.
- Do not leave unexplained labels such as Company, Ticker, Anti-hype, Strength, Fact, Inference, Assumption, or Rumor in a Chinese report; translate or explain them.
- Do not stack specialist terms without teaching them. If a term is important enough to use, it is important enough to explain.
