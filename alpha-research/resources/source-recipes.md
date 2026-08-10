# Source Recipes

Source Recipes are step-by-step acquisition procedures.

Use them after selecting a Source Profile and before writing `Source Map` stage.

For financial and valuation work, also apply `data-rigor.md`.

Each recipe follows the finance-skills pattern:

```text
Detect → Choose path → Ask approval if needed → Fetch/read → Structure output → Preserve provenance → Feed Source Registry
```

## Universal acquisition loop

For every material source channel:

1. **Detect** availability.
   - Built-in search/fetch available?
   - Tool installed?
   - API key/session present?
   - Paid/source access available?
2. **Choose path**.
   - Official/manual source first.
   - Tool wrapper only when it improves retrieval or structure.
   - Browser/OpenCLI only when static fetch fails or logged-in page is needed.
3. **Ask approval** before commands, installs, API calls, paid access, browser login, or local scripts.
4. **Fetch/read source**.
   - Prefer original page/PDF/filing/API response over search snippets.
   - Prefer structured output (`json`, `csv`, markdown table) when using tools.
5. **Create Source Registry entry**.
6. **Classify evidence by underlying source**.
7. **Apply Source Gate**.

## Recipe 1: US public company

Use for US-listed companies, ADRs with SEC filings, and US-centered company maps.

### Required steps

1. SEC filing baseline.
   - Source: SEC EDGAR.
   - Collect latest 10-K/20-F and latest 10-Q/6-K or earnings release.
   - Registry: filing type, period, filing date, URL/accession, section/page/quote.
2. Company IR.
   - Source: company IR site.
   - Collect latest presentation, earnings release, transcript, product/technical page if relevant.
3. Financial baseline and data-rigor pack.
   - Detect yfinance / Funda / TradingView / paid terminal / official manual source.
   - If missing and user approves, use `tool-install-sources.md`.
   - Pull price, market cap, revenue, segment revenue, margin, cash/debt, share count, volume, guidance/backlog/orders, customer concentration, and options/flows if material.
   - Apply `data-rigor.md`: record units, currency, period, source date, and at least one manual arithmetic check when valuation is discussed.
   - Record retrieval method, fields, date/time, and original URL/provenance.
4. News/events.
   - Use company press releases and reputable news for recent events.
   - Trace event claims back to company/filing when possible.
5. Anti-hype if relevant.
   - Use OpenCLI/Grok/X/Reddit only for narrative and crowding.

### Source Gate fails if

- no SEC/company filing for company facts;
- no financial baseline for company ranking;
- no company source for product/roadmap claims;
- valuation or priority is discussed without minimum data pack or explicit Data Gaps;
- relative attractiveness is discussed without peer/comparable baseline or explanation;
- source registry lacks URLs/locators.

## Recipe 2: A-share company

Use for A-share companies, A-share concept stocks, and A-share company maps.

### Required steps

1. Official disclosure.
   - Source: 巨潮资讯 / 上交所 / 深交所 / 北交所.
   - Collect latest annual report or relevant announcement.
   - Use CNINFO/exchange URL as the citation, not only a data wrapper.
2. Company IR / investor interaction.
   - Source: company IR, 业绩说明会, 投资者互动平台 where relevant.
   - Use for product/exposure claims, but do not treat as audited financial proof.
3. Financial baseline.
   - Preferred optional tools: a-stock-data, Tushare, AkShare.
   - Always reconcile key financial values to official reports for final Facts.
4. Market/narrative.
   - Use Eastmoney/Xueqiu/THS/OpenCLI only for narrative/crowding.
   - Preserve original URL, author/handle, timestamp.
5. Policy/industry if relevant.
   - Use official ministries/statistics/procurement sources.

### Source Gate fails if

- company Fact lacks CNINFO/exchange/company source;
- CPO/AI/概念 exposure is only from concept tags;
- financial baseline is missing for ranking;
- narrative origin is claimed without original/earliest source.

## Recipe 3: HK listed company

1. Use HKEXnews for annual/interim reports, announcements, prospectus.
2. Use company IR for presentation/transcript/product claims.
3. Use financial data provider only as baseline.
4. Use China/HK narrative sources only as narrative clues.
5. Preserve stock code, announcement title, date, URL, page/section, quote.

Source Gate fails without HKEX/company source for key company claims.

## Recipe 4: Technology / semiconductor / photonics

Use for CPO, silicon photonics, chips, materials, biotech, engineering constraints.

### Required steps

1. Technical basis.
   - Search arXiv/Semantic Scholar/IEEE/standards/official technical docs.
   - Collect at least one technical source for feasibility/performance claims.
2. Patent / standards route.
   - Search Google Patents/Lens/official patent offices if moat or route matters.
   - Record publication number, assignee, date, URL, claim/abstract excerpt.
3. Company product source.
   - Use official product pages, conference slides, IR, press releases.
   - Product existence does not prove revenue.
4. Public company exposure.
   - For mapped companies, collect filings/IR and financial baseline.
5. Industry scale.
   - Use market reports/industry associations as forecasts, not Facts.

### Source Gate fails if

- technical feasibility claims rely on news/social only;
- public company exposure lacks filings/IR;
- chokepoint ranking lacks direct evidence for supply narrowness/expansion difficulty.

## Recipe 5: Industry / supply-chain chokepoint

1. Define end demand.
   - Customer capex, orders, deployments, policy mandates, or official demand data.
2. Build physical chain.
   - For each layer, identify function, dependency, supplier set, expansion constraint, substitution route.
3. Collect primary sources for top layers.
   - At least two company primary sources for key claims.
4. Collect industry/technical sources.
   - Market scale and physical constraints.
5. Map public companies.
   - Each mapped public company needs exposure evidence and financial baseline.
6. Separate concept-only.
   - If exposure is only concept tags or media narrative, mark concept-only.

### Source Gate fails if

- top chokepoint lacks evidence;
- company map lacks official exposure evidence;
- no financial baseline exists for public-company prioritization.

## Recipe 6: Anti-hype / narrative

1. Identify claim text precisely.
   - Example: “2026 是 CPO 商用元年”.
2. Find original/earliest visible source.
   - Use OpenCLI, browser automation, X/Grok, Xueqiu, Eastmoney, Google News, or a manual original URL.
   - Web search is only the discovery layer; the final Source Registry needs the original post/page/article URL.
   - Preserve URL, author/publisher, handle if social, timestamp, retrieval method, and access caveat.
3. Build amplification timeline.
   - Media → social → forums → price action / hot tags.
4. Primary-source check.
   - For each narrative claim, look for filing/IR/official/technical confirmation.
5. Market-structure check.
   - Volume, liquidity, correlation, options, fund flow, estimate revisions when material.
6. Classify.
   - Supported Fact / Inference / Assumption / Rumor.

### Source Gate fails if

- narrative origin is unknown but report claims origin;
- OpenCLI/browser/social/manual original-source capture was required but not done or explicitly blocked;
- social/forum evidence is upgraded to Fact;
- no primary-source check exists.

## Recipe 7: Financial baseline

Use before any ranking, valuation-quality discussion, liquidity discussion, or market-structure section.

### US/global path

1. Detect yfinance.
2. If available, pull:
   - price;
   - market cap;
   - revenue / margin / cash / debt where available;
   - share count;
   - 3–5 year price/volume history;
   - options chain if material.
3. If yfinance weak/missing, use Funda/TradingView/paid terminal if available.
4. Reconcile key financial line items to filings.

### A-share path

1. Use official filing for final financials.
2. Use a-stock-data/AkShare/Tushare for quick baseline.
3. Record endpoint/function, fields, units, date range.
4. Reconcile line items to CNINFO/exchange reports.

### Source Gate fails if

- ranking uses stale or uncited financial values;
- PE/market cap/revenue claims have no date and source;
- the only financial baseline is a web-search snippet or article summary;
- wrapper output lacks original source/field provenance.

## Recipe 8: Gold

Use for gold, gold miners, gold ETFs, central-bank buying, real-rate sensitivity, and precious-metals narratives.

### Required steps

1. Price and benchmark baseline.
   - Source: LBMA gold price, CME gold futures, SGE where China premium matters, or a recognized market-data provider with underlying source noted.
   - Record benchmark, currency, timestamp/date, contract month if futures.
2. Macro driver baseline.
   - Source: FRED / US Treasury / central bank data.
   - Pull real yields, nominal yields, inflation expectations, USD/DXY proxy, policy-rate context where material.
3. Demand / flow baseline.
   - Source: World Gold Council ETF holdings/flows, central-bank reserve data, IMF/official central bank sources.
   - Separate ETF demand, central-bank demand, jewelry/technology demand, and investment demand.
4. Positioning / crowding.
   - Source: CFTC COT for COMEX gold if futures positioning is discussed.
   - Record report date, category definitions, net/non-commercial positions, open interest.
5. Supply / physical context.
   - Source: World Gold Council supply data, miner filings/IR, official import/export/SGE/LBMA source when relevant.
6. Linked companies.
   - For miners/royalty companies/ETFs, collect filings/IR, reserves/production/costs/hedges, financial baseline.

### Source Gate fails if

- gold thesis relies only on spot-price charts, headlines, or social narrative;
- real-rate / USD / inflation claims lack macro data;
- ETF/central-bank flow claims lack WGC/IMF/official source;
- crowding claims lack CFTC or equivalent positioning source;
- gold-company recommendation lacks filings/IR and financial baseline.

## Recipe 9: Crude oil

Use for WTI/Brent, oil producers, refiners, services, tankers, OPEC+ narratives, and geopolitical oil shocks.

### Required steps

1. Price and curve baseline.
   - Source: CME WTI and/or ICE Brent.
   - Record contract month, settlement/quote date, currency, curve shape, contango/backwardation, spreads.
2. Supply / demand / inventory.
   - Source: EIA Weekly Petroleum Status Report, EIA STEO, IEA Oil Market Report, OPEC Monthly Oil Market Report, JODI.
   - Record period, units, region, table/source URL.
3. US physical indicators when relevant.
   - Source: EIA crude/product inventories, refinery utilization, production, imports/exports, SPR, implied demand.
   - Baker Hughes rig count can be used as corroboration.
4. OPEC+ / geopolitical / shipping.
   - Use official OPEC statements, government/sanctions sources, shipping data where available, and reputable news only as context.
5. Positioning / crowding.
   - Source: CFTC COT for WTI/Brent-linked contracts where available.
6. Linked companies.
   - For E&Ps/refiners/services/tankers, collect filings/IR, production mix, reserves, costs, hedges, crack spreads/exposure, balance sheet.

### Source Gate fails if

- oil thesis lacks at least one official supply/demand/inventory source;
- curve claims lack CME/ICE/exchange source;
- OPEC/geopolitical claims rely only on media headlines;
- crowding claims lack CFTC or equivalent positioning source;
- oil-linked company recommendation lacks filings/IR and financial baseline.

## Recipe 10: Futures curve / positioning / commodity market structure

Use for any commodity when the argument depends on curve, roll yield, inventories, crowded positioning, ETF flow, or speculative pressure.

1. Define instrument precisely.
   - Commodity, benchmark, exchange, contract code, delivery month, currency, units.
2. Collect curve data.
   - Source: CME/ICE/LME/SHFE/INE/SGE or recognized provider with underlying exchange preserved.
   - Record front month, next months, spread, settlement date, data delay/entitlement caveat.
3. Collect inventory / physical balance.
   - Source: official exchange warehouse data, EIA/JODI/WGC/LBMA/industry source depending on commodity.
4. Collect positioning.
   - Source: CFTC COT, exchange open interest, ETF holdings/flows where relevant.
5. Interpret separately.
   - Curve ≠ fundamentals proof by itself.
   - Positioning ≠ direction signal by itself.
   - Use as market-structure/risk evidence.

### Source Gate fails if

- backwardation/contango/roll-yield claims lack exchange/provider data;
- crowding claims lack positioning/flow data;
- chart-only claims are treated as fundamental evidence.

## Recipe 11: Commodity-linked company recommendation

Use when a commodity thesis maps to miners, E&Ps, refiners, service companies, tankers, commodity ETFs, royalty companies, or equipment suppliers.

1. Start from commodity driver.
   - Identify whether the company benefits from price, volume, spread, cost curve, reserves, inventory, service activity, or policy.
2. Collect company primary sources.
   - Filing/annual report, IR presentation, production/reserve report, cost guidance, hedging disclosure, segment exposure.
3. Collect financial baseline.
   - Revenue, EBITDA/margin/cash flow, debt, capex, share count, liquidity, valuation baseline if used.
4. Build exposure logic.
   - Link commodity variable → company economics → evidence → risk.
5. Add counterarguments.
   - Cost inflation, hedges, decline rates, political risk, resource tax/royalty, FX, balance sheet, operational incidents.
6. Define failure criteria.
   - Commodity driver breaks, company exposure lower than expected, margins/cash flow fail to respond, capex/hedges offset upside.

### Source Gate fails if

- company recommendation is based only on commodity price direction;
- exposure is not documented in filings/IR;
- financial baseline is missing;
- risks and failure criteria are absent.

## Recipe 12: Dynamic website / social source via OpenCLI

1. Detect OpenCLI.
2. Inspect adapter list.
   - Do not guess command names.
   - Use `opencli list -f json` or `opencli <site> --help` after approval.
3. Check adapter strategy.
   - PUBLIC/LOCAL may not need login.
   - COOKIE/HEADER/INTERCEPT/UI needs browser login and user approval.
4. Run read-only command with structured output.
   - Prefer `-f json`.
   - Limit rows.
5. Preserve underlying source.
   - Platform, URL, author/handle, timestamp, query/filter, extracted text.
6. Classify as narrative unless underlying source is official/primary.

## Recipe 13: Paid provider / Funda

1. Ask whether user has access.
2. Detect `FUNDA_API_KEY` or MCP/OAuth connection only after permission.
3. Use raw data endpoints for structured data when possible.
4. Use synthesis for leads, not primary proof.
5. Extract original source URLs from response when available.
6. Reconcile key claims to filings/transcripts/company sources.

## Recipe 14: Tool missing

When a required tool is missing:

1. Open `tool-install-sources.md`.
2. Identify canonical source and package/connector.
3. Ask for permission with:
   - command;
   - source URL;
   - why needed;
   - read-only boundary;
   - credential/login requirement.
4. If approved, execute setup.
5. Verify.
6. Update `tool-status.md`.
7. Rerun Source Gate.

If not approved, mark channel Missing / Blocked and stop if hard gate fails.
