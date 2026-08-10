# Source Profiles

Source Profiles define the minimum source mix for common Alpha Research objects.

Use this file before `Source Map` stage builds the Tool Capability Plan.

A profile is not a tool list. It is a required evidence pattern.

## How to use

1. Pick the closest profile from the table below.
2. Mark required channels as material / not material.
3. Use `source-recipes.md` for the acquisition sequence.
4. Use `tool-install-sources.md` only when the needed tool is missing.
5. Use `data-providers/*.md` for source-specific guardrails.
6. Enforce the hard source gate before final report generation.

## Profile index

| Profile | Use when | Required source groups | Default hard-gate stance |
|---|---|---|---|
| US Public Company | US-listed company, US ADR, US financial baseline | SEC, company IR, financial data, news/events, market-structure if material | Hard stop without SEC/IR + financial baseline. |
| A-share Company | A-share listed company or A-share concept/company map | CNINFO/exchange, company IR/investor Q&A, financial data, A-share narrative, news/events | Hard stop without official disclosure + financial baseline. |
| HK Company | HK-listed company | HKEXnews, company IR, financial data, news/events, HK/China narrative if material | Hard stop without HKEX/company source. |
| China Policy / Macro / Industry | China policy, industrial data, procurement/subsidy, macro | Official policy/statistics/regulator, procurement/tender if relevant, industry association, news only as clue | Hard stop without official policy/statistics source. |
| Commodity / Macro Commodity | Gold, oil, gas, industrial metals, agricultural commodities, commodity-linked macro | Official supply/demand/inventory data, futures curve, positioning, macro drivers, physical-market data, company profile if mapped | Hard stop without commodity-specific official data and market-structure baseline. |
| Technology / Semiconductor | Technical feasibility, semiconductor, material, photonics, biotech, engineering | Technical papers, patents/standards, company product/IR, filings for mapped companies, financial baseline | Hard stop without technical source for technical claims. |
| Industry / Supply Chain | Supply-chain chokepoint mapping | Demand source, company primary sources, filings/IR for mapped companies, industry data, technical/patent if technical, financial baseline | Hard stop before ranking chokepoints without direct evidence. |
| Anti-hype / Narrative | Hot sector, social narrative, concept stocks, crowded story | Original/earliest narrative, social/forum, primary-source check, financial/market-structure baseline | Hard stop before claiming narrative origin without original/earliest source. |
| Private / Startup / Unlisted | Private company, startup, supplier not public | Company site/press, registry, funding sources, customer/product evidence, hiring/alternative data | No public-company ranking; mark unverifiable financials. |

## US Public Company Profile

Required:

| Source function | Preferred sources / tools | Provider resource | Hard gate |
|---|---|---|---|
| Filing / disclosure | SEC EDGAR, 10-K, 10-Q, 8-K, S-1/F-1, 20-F/6-K | `data-providers/sec-edgar.md` | Required for company Facts. |
| Company IR | Company IR page, earnings release, transcript, presentation | `data-providers/company-ir.md` | Required for product/roadmap/management claims. |
| Financial baseline | yfinance, Funda, paid terminal | `data-providers/yfinance.md`, `data-providers/funda-data.md` | Required for valuation, liquidity, growth, financial quality. |
| Market data / options | yfinance, TradingView, Funda, paid terminal | `data-providers/tradingview-reader.md` | Required if market-structure risk is material. |
| News/events | company press releases, reputable news, Funda news if available | `data-providers/funda-data.md` | Required for recent event claims. |
| Narrative | X/Grok, Reddit, Stocktwits, OpenCLI | `data-providers/opencli-reader.md`, `data-providers/grok-x.md` | Required for anti-hype mode. |

Minimum Source Registry:

- latest annual filing;
- latest quarterly filing or earnings release;
- company IR/product source for product claims;
- financial baseline source;
- at least one recent event/news source when event-driven.

## A-share Company Profile

Required:

| Source function | Preferred sources / tools | Provider resource | Hard gate |
|---|---|---|---|
| Filing / disclosure | 巨潮资讯, 上交所, 深交所, 北交所 | `data-providers/cninfo.md` | Required for all key company Facts. |
| Company IR / Q&A | 公司 IR, 投资者互动, 业绩说明会 | `data-providers/company-ir.md` | Required for product/exposure statements. |
| Financial baseline | a-stock-data, AkShare, Tushare, official filings | `data-providers/a-stock-data.md`, `data-providers/akshare.md`, `data-providers/tushare.md` | Required for rankings and financial claims. |
| Market/narrative | 东方财富, 雪球, 同花顺社区, OpenCLI | `data-providers/opencli-reader.md`, `data-providers/opencli-social.md` | Required for anti-hype / concept-stock work. |
| News/events | company announcements, exchange announcements, reputable China finance media | `data-providers/cninfo.md` | Required for event claims. |
| Policy/industry | official ministries, statistics, procurement/tender if relevant | `data-providers/china-policy-sources.md` | Required for policy claims. |

Minimum Source Registry:

- latest annual report or latest filing matching the claim;
- latest quarterly/interim report if financial claims are current;
- one official disclosure for each key product/order/customer claim;
- financial baseline source with fields/units;
- original/earliest narrative source if anti-hype.

## HK Company Profile

Required:

| Source function | Preferred sources / tools | Provider resource | Hard gate |
|---|---|---|---|
| Filing / disclosure | HKEXnews annual/interim reports, announcements, prospectus | `data-providers/hkexnews.md` | Required. |
| Company IR | Company IR page, presentation, earnings materials | `data-providers/company-ir.md` | Required for management/product claims. |
| Financial baseline | filings, yfinance if listed/covered, paid terminal | `data-providers/yfinance.md` | Required for ranking/valuation claims. |
| China/HK narrative | 雪球, 東方財富, broker/media, OpenCLI if needed | `data-providers/opencli-reader.md` | Required for anti-hype. |

## China Policy / Macro / Industry Profile

Required:

| Source function | Preferred sources / tools | Provider resource | Hard gate |
|---|---|---|---|
| Official policy | ministries, regulators, government notices | `data-providers/china-policy-sources.md` | Required for policy claims. |
| Official statistics | 国家统计局, 央行, 海关, local statistics | `data-providers/china-policy-sources.md` | Required for macro/production/trade claims. |
| Procurement / tender / subsidy | 中国政府采购网, 公共资源交易平台, 招投标平台 | `data-providers/china-policy-sources.md` | Required when demand depends on public projects. |
| Industry association | official/quasi-official associations | `data-providers/china-policy-sources.md` | Useful but not a substitute for official sources. |
| News | reputable media | — | Event clue only. |

## Commodity / Macro Commodity Profile

Use for gold, crude oil, natural gas, copper, aluminum, lithium, uranium, agriculture, and commodity-linked macro theses.

Required:

| Source function | Preferred sources / tools | Provider resource | Hard gate |
|---|---|---|---|
| Official supply / demand / inventory | EIA, IEA, OPEC, JODI, World Gold Council, LBMA, SGE, LME/SHFE/CME/ICE official pages | `data-providers/eia.md`, `data-providers/iea-opec-jodi.md`, `data-providers/world-gold-council-lbma.md`, `data-providers/cme-ice-futures.md` | Required for commodity balance claims. |
| Futures curve / term structure | CME, ICE, LME, SHFE/INE/SGE where relevant, TradingView as transport only | `data-providers/cme-ice-futures.md`, `data-providers/tradingview-reader.md` | Required for contango/backwardation/curve claims. |
| Positioning / crowding | CFTC COT, exchange open interest, ETF holdings, fund flows | `data-providers/cftc-cot.md`, `data-providers/world-gold-council-lbma.md` | Required for crowding/positioning claims. |
| Macro drivers | FRED, US Treasury, central bank data, DXY source, real rates, inflation expectations | `data-providers/fred-treasury-macro.md` | Required for gold and macro-rate claims. |
| Physical bottlenecks | inventories, refinery utilization, rig count, mine supply, shipping, sanctions, official policy | commodity-specific provider | Required for physical-market chokepoint claims. |
| Linked public companies | filings, IR, segment exposure, production cost curve, reserves, hedges, financial baseline | market-specific company profile | Required for candidate/company recommendations. |
| Narrative / geopolitics | original policy/official/security/shipping source plus reputable news | source-specific | Required for geopolitical claims; media alone is not enough. |

Minimum Source Registry:

- one commodity-specific official data source for the primary driver;
- one market-structure source for price/curve/positioning claims;
- one macro source for rate/FX/inflation claims when material;
- one official physical-market source for supply/demand/inventory claims;
- filings/IR/financial baseline for any recommended commodity-linked company.

### Gold minimum evidence

Required when researching gold:

- gold price benchmark or futures source: LBMA, CME, SGE, or equivalent;
- real-rate / Treasury / inflation expectation source: FRED or US Treasury;
- dollar / macro context source;
- ETF holdings or central bank reserve data: World Gold Council / IMF / official central bank source;
- CFTC COT or comparable positioning source if crowding is discussed.

Hard gate fails if gold conclusions rely only on spot-price charts or headlines.

### Oil minimum evidence

Required when researching crude oil:

- supply/demand/inventory source: EIA weekly/monthly data, IEA, OPEC, or JODI;
- futures curve source: CME WTI or ICE Brent;
- positioning source: CFTC COT if crowding/speculative positioning is discussed;
- physical balance context: inventories, refinery runs, rig count, OPEC+ policy, shipping/geopolitics if material;
- company filings/IR for any oil producer/refiner/oilfield-service recommendation.

Hard gate fails if oil conclusions rely only on spot-price charts, media headlines, or OPEC rhetoric without data.

## Technology / Semiconductor Profile

Required:

| Source function | Preferred sources / tools | Provider resource | Hard gate |
|---|---|---|---|
| Technical basis | arXiv, Semantic Scholar, IEEE/ACM/PubMed, standards | `data-providers/semantic-scholar-arxiv.md` | Required for feasibility/performance claims. |
| Patent / standards | Google Patents, Lens, USPTO/WIPO/Espacenet/CNIPA, standards bodies | `data-providers/google-patents-lens.md` | Required for moat/route/standards claims. |
| Company product source | company product pages, IR, technical blogs, conference slides | `data-providers/company-ir.md` | Required for company-specific technology claims. |
| Filing / disclosure | SEC/HKEX/CNINFO/exchange reports for mapped public companies | market-specific provider | Required for public-company exposure. |
| Financial baseline | yfinance, a-stock-data, AkShare, Tushare, Funda | provider-specific | Required for company ranking. |

## Industry / Supply Chain Profile

Required:

| Source function | Preferred sources / tools | Provider resource | Hard gate |
|---|---|---|---|
| End-demand evidence | customer capex, orders, deployments, policy demand, official data | market-specific | Required for trend reality. |
| Company primary | supplier/customer announcements, IR, filings | company/market provider | Required for mapped company roles. |
| Industry data | market reports, industry association, trade publications | provider-specific | Required for scale/context. |
| Technical/patent | papers, patents, standards where technical | technical provider | Required if bottleneck is technical. |
| Financial baseline | yfinance/a-stock-data/Funda/Tushare/AkShare | provider-specific | Required for public company purity/ranking. |
| Alternative data | hiring, tender, import/export, supplier directory | source-specific | Corroboration only. |

## Anti-hype / Narrative Profile

Required:

| Source function | Preferred sources / tools | Provider resource | Hard gate |
|---|---|---|---|
| Original narrative | earliest visible post/article/report/headline | OpenCLI/Grok/social provider | Required before claiming origin. |
| Amplification path | social search, media timeline, forum posts, hot-stock tags | `data-providers/opencli-reader.md`, `data-providers/grok-x.md` | Required for crowding analysis. |
| Primary-source check | filings, IR, official policy, technical source | market/source provider | Required to separate fact from hype. |
| Market-structure | price/volume/liquidity, fund flow, options, estimate revisions | yfinance, TradingView, a-stock-data, Funda | Required when crowding/valuation is discussed. |

## Profile selection rules

- If multiple profiles apply, take the union of required sources.
- If the output includes company ranking, add the company profile for that market.
- If the output includes commodity price, supply/demand balance, inventory, curve, or positioning claims, add the commodity profile.
- If the output includes commodity-linked company recommendations, add both the commodity profile and the relevant company-market profile.
- If the output includes technical feasibility, add the technology profile.
- If the output includes “概念股”, “hot”, “theme”, “AI narrative”, “oil shock”, “gold rush”, or social claims, add anti-hype profile.
- If a required profile source is blocked, stop at hard source gate unless the claim is removed or downgraded.
