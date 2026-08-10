# Stage: Source Map

## Purpose

`Source Map` 是信息获取中枢。

它回答：这个研究主题应该从哪些来源获取准确、有用、可审计的数据？

它输出 Source Plan + Tool Capability Plan + Source Registry + Source Gate Decision + Starter Evidence Pack。
它不直接写最终投资结论，不输出直接交易信号。

## Bundled files

- Template: `templates/source-map.md`.
- Resources: none.

## Authoritative source rules

For full collection installs, use these `alpha-research` resources:

- `resources/research-tool-stack.md` for Setup Mode, Channel Status, Source Confidence Tier, tool selection, provenance, freshness, market coverage, minimum evidence, hard source gate, and quality ceilings.
- `resources/source-profiles.md` for required source mix by research object.
- `resources/source-recipes.md` for acquisition sequence.
- `resources/data-rigor.md` for financial sanity checks, minimum data pack, and peer baseline rules.
- `resources/tool-install-sources.md` for canonical install sources and detection checks.
- `resources/data-providers/*.md` for source-specific guidance.

When a specific source needs operational guidance, use `alpha-research` internal provider resources: `resources/data-providers/*.md`.

When a tool is missing or the agent needs canonical install sources, use `resources/tool-install-sources.md`.

If those resources are unavailable, apply the same principle: match source categories to the research object and market scope, preserve provenance for key sources, and mark gaps explicitly.

## Inputs

最好输入 `Clarify` 的 Research Brief。

至少需要：

- Topic.
- Research object.
- Market scope.
- Current belief.
- Key unknowns.
- Research mode: normal or anti-hype, if relevant.

## Profile and recipe selection

Before listing sources, select:

- Source Profile(s): from `source-profiles.md`.
- Source Recipe(s): from `source-recipes.md`.
- Reason for profile/recipe choice.

If multiple profiles apply, take the union of hard-gate requirements.

## Required source categories

Cover these categories by default:

1. Company primary sources.
2. Regulatory / exchange disclosures.
3. Industry and market sources.
4. Technical sources: papers, patents, standards, white papers.
5. News and event sources.
6. Financial data sources.
7. Field / alternative data leads.
8. Social / narrative sources.

Use the minimum acceptable evidence rules from `research-tool-stack.md` to decide which categories are required for the current research object.

## Tool Capability Plan

Do not write vague instructions like “search the web.”

Map each information need to:

- Source category.
- Tool capability.
- Candidate tools or sources.
- Setup Mode.
- Source Confidence Tier.
- Evidence role.
- Limitations.

Use explicit optional examples while keeping the workflow portable.

Examples:

| Need | Source category | Tool capability | Optional examples | Evidence role |
|---|---|---|---|---|
| Company revenue exposure | Filing / IR | filing fetch, IR fetch | SEC, HKEXnews, 巨潮资讯, company IR, Funda with original filing provenance | Strong Fact |
| Numeric baseline | Financial data | quotes, statements, options, ownership, market data | yfinance, a-stock-data, Funda, TradingView, AkShare, Tushare | Numeric baseline |
| Material performance limit | Technical | academic search, standards search | arXiv, Semantic Scholar, IEEE, standards bodies | Technical basis |
| Real-time narrative | Social | social search, browser automation | X/Grok, Reddit, 雪球, 股吧, OpenCLI-like tools | Rumor / narrative clue |

## Source acquisition requirement

Do not stop at web search snippets.

`Source Map` must actually collect or open enough source records to create a citable Source Registry before the workflow proceeds to serious synthesis. It must also record an Acquisition Log showing what was opened, queried, or blocked.

Minimum acceptable collection:

- Company / listed-company research: latest filing/disclosure, company IR or earnings material, financial data baseline, recent news/events, and a minimum data pack for final explanation.
- Company minimum data pack: revenue and segment revenue, margin, cash flow, cash/debt, market value or liquidity, valuation multiple, guidance/orders/backlog where available, customer concentration where material, and source dates.
- If valuation, ranking, or relative company priority will be discussed, collect a peer / comparable baseline or explicitly mark it as missing.
- Industry / supply-chain research: at least two primary company sources, one market/industry source, one technical/patent/standards source if technical, and financial baseline for mapped public companies.
- A-share company mapping: 巨潮资讯 or exchange disclosure source is required for key company Facts; optional tools such as a-stock-data, AkShare, Tushare, or OpenCLI can help, but original provenance must be kept.
- Commodity research: official/recognized commodity data is required for supply/demand/inventory claims; exchange source is required for futures curve claims; CFTC/flow source is required for positioning/crowding claims; company filings/IR are required for commodity-linked candidate recommendations.
- Anti-hype mode: original narrative source or earliest visible narrative source plus primary-source check. Use OpenCLI, browser automation, a social-source reader, or a manual original URL when social/narrative origin is material. If this requires approval or login and the user has not approved, mark it `Blocked` and fail the relevant source gate.
- Company / candidate ranking: financial baseline from yfinance, a-stock-data, Funda, TradingView, official filings/exchange data, or documented manual equivalent. Web search snippets are not a financial baseline.

If a required source-specific tool is unavailable, mark the channel `Missing` / `Blocked by access` and lower confidence. Do not replace primary-source work with generic web search.

## Source Registry

Every source used later must get a stable citation id.

Format:

```text
[S1], [S2], [S3] ...
```

For every source, capture:

- citation id;
- title;
- publisher / owner;
- URL or stable locator;
- publication date / filing date / reporting period;
- access date;
- source tier;
- evidence role;
- quote / page / table / section when supporting a key Fact.

## Source Gate Decision

Produce a hard gate decision before recommending the next stage.

Use one of:

- **PASS**: required source categories are represented by citable, previewable sources.
- **FAIL**: one or more hard source gate rules fail.

FAIL if any of these are true:

- Source Registry is empty or lacks URLs/stable locators.
- Key Facts are supported only by web-search snippets.
- The Acquisition Log shows only generic web search for required company, financial, technical, commodity, or narrative channels.
- Company/listed-company claims lack official filing/disclosure or company primary source.
- Public-company ranking lacks financial baseline.
- Technical feasibility claims lack technical/patent/standard/official product evidence.
- Commodity supply/demand/inventory claims lack official/recognized commodity data.
- Futures curve/positioning/crowding claims lack exchange, CFTC, or flow source.
- Commodity-linked company recommendations lack filings/IR/financial baseline.
- Anti-hype narrative-origin claims lack original or earliest visible narrative source.
- Wrapper/aggregator output lacks original source provenance for key Facts.
- Anti-hype narrative/crowding claims are made without OpenCLI/browser/social-source/manual original URL capture when material.
- Company ranking, valuation, liquidity, or estimate-revision discussion lacks a suitable financial data source or official/manual equivalent.
- Company report would discuss valuation, priority, or recommendation logic without the minimum data pack or explicit Evidence Gaps.
- Relative valuation or priority is discussed without peer / comparable baseline or an explicit reason why clean comparables are unavailable.
- Final citations would point to local artifacts rather than original sources.

When gate = FAIL, do not recommend `Chain Trace` as normal continuation unless the next step is explicitly limited to source acquisition or hypothesis-only mapping. Recommend missing-source collection first.

## Starter Evidence Pack

Collect or identify the first evidence layer.

For each source, record enough provenance for later audit.
Do not over-expand the table unless the source supports a key Fact.

For each source, record:

- Citation id.
- Source title.
- URL or stable locator.
- Source type.
- What it can prove.
- Evidence strength.
- Which later stage should use it.
- Gaps and caveats.

For key Fact sources, preserve publication date, access date, and quoted excerpt / page / table / section when possible.
For social sources, preserve author/handle, timestamp, and original post URL when possible. If only a profile is available, link the `@handle` profile and mark the post URL missing; do not use it as a key Fact.

## Evidence discipline

- Primary sources beat summaries.
- Filings beat media articles.
- Customer announcements beat speculation.
- Papers explain technical possibility, not company revenue.
- Patents show activity, not commercial traction.
- Social media is Rumor / narrative clue unless confirmed elsewhere.
- Missing source categories must remain Evidence Gaps.
- Missing numeric data must remain Data Gaps; do not hide it behind prose.
- Use market-specific official sources for the target market.

## Anti-hype mode

If research mode is anti-hype, add:

- Original narrative source.
- Earliest visible claim.
- Claim propagation path.
- Influencer / media amplification.
- Which claims are unsupported.
- What primary evidence would confirm or reject the narrative.

## Output

Use `templates/source-map.md` and produce:

```markdown
# Source Map: {Topic}

## 1. Research Question

## 2. Source Profile and Recipe

## 3. Information Needs

## 4. Source Plan

## 5. Tool Capability Plan

## 5.1 Acquisition Log

## 6. Tool Status

## 7. Source Registry

## 8. Source Gate Decision

## 9. Starter Evidence Pack

## 10. Evidence Gaps

## 11. Source Quality Warnings

## 12. Stage Result
```

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

Default next stage: `Chain Trace` only when Source Gate is PASS.

If Source Gate is FAIL, default next step is `alpha-research` internal source acquisition using `tool-install-sources.md` and relevant `resources/data-providers/*.md`, then rerun `Source Map`.

## Guardrails

- Do not invent sources.
- Do not cite a source that was not actually identified.
- Do not use web-search result text as the final citation when a real page, filing, PDF, data endpoint, or original social post can be opened.
- Do not let a source map pass without URLs or stable locators for key Facts.
- Do not let a source map pass if required financial data, OpenCLI/browser narrative capture, filings, or technical sources are merely planned but not acquired or explicitly blocked.
- Do not mark Source Gate PASS if hard source gate rules fail.
- Do not convert source availability into thesis confidence.
- Do not treat social media as primary evidence.
- Do not use wrong-market sources when target-market sources are required.
- Do not produce unsupported candidate/company recommendations or direct trade instructions.
