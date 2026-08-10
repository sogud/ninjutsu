# Required Research Tool Stack

This resource is the authoritative tool-stack and source-quality contract for Alpha Research.

It defines the information channels, tool choices, setup modes, source confidence tiers, market-specific sources, hard source gate, and quality ceiling rules required for credible investment research.

Use it together with:

- `source-profiles.md` for required source mix by research object.
- `source-recipes.md` for acquisition order.
- `data-rigor.md` for financial-data and valuation sanity checks.
- `tool-install-sources.md` for canonical install sources.
- `data-providers/*.md` for provider-specific rules.

Core rule:

> Every complete Alpha Research environment must have at least one usable implementation for each required information channel. A single research run may mark a channel as `Not material for this topic`, but it must not pretend that an unavailable relevant channel was checked.

## 1. Setup Mode enum

Use these setup modes when describing each tool or source.

| Setup Mode | Meaning |
|---|---|
| Built-in | The current agent/runtime already provides the capability. |
| Local install | Requires installing a local CLI, package, desktop tool, or browser extension. Do not include concrete install commands in this resource. |
| API key | Requires the user to provide and configure an API key. |
| Web login | Requires the user to sign in on a website. |
| Browser login session | Requires reusing an authenticated browser session after the user logs in. |
| Paid terminal / subscription | Requires paid access such as a financial terminal, research database, or premium data product. |
| Manual fallback | User or agent manually opens the official source and records the result. |

Rules:

- A tool may have multiple setup modes.
- The agent may help plan setup.
- The user must provide API keys, credentials, paid access, or login actions.
- The agent must not bypass access controls, paywalls, login gates, or contractual restrictions.
- If local installation is needed, the agent should use `resources/tool-install-sources.md` for canonical source/package names, propose environment-specific steps, and wait for user confirmation before acting.
- If the user explicitly approves runtime setup, the agent may execute code, scripts, connector setup, or dependency installation for that environment. Do not add those dependencies to this repository unless separately requested.

## 2. Channel Status enum

Use these statuses in setup reviews and source maps.

| Channel Status | Meaning |
|---|---|
| Available | The channel can be used now. |
| Available with user action | The channel is available after user action, such as login, API key, subscription access, or install confirmation. |
| Missing | No usable implementation is currently available. |
| Not material for this topic | The channel exists in the required stack but is not relevant to this specific research question. |
| Blocked by access / paid source | The channel would be relevant, but current access rights do not allow use. |

Rules:

- Do not collapse these into a boolean available/missing field.
- `Missing` and `Blocked by access / paid source` must become evidence gaps when relevant.
- `Not material for this topic` requires a short reason.

## 3. Source Confidence Tier

Source Confidence Tier ranks the source before claim-level evidence analysis.

| Tier | Name | Meaning |
|---:|---|---|
| 1 | Official primary source | Regulator, exchange, government, court, customs, official statistics, official standard body, official procurement system. |
| 2 | Company primary source | Company filing, annual report, IR page, earnings call, presentation, product page, company press release. |
| 3 | Recognized data provider / exchange data | Financial data provider, exchange data product, academic database, patent database, established industry database. |
| 4 | Reputable media / industry report | Reliable financial media, trade publication, consulting report, broker report, industry association report. |
| 5 | Social / forum / influencer narrative | X/Twitter, Reddit, Stocktwits, 雪球, 股吧, forums, influencers, newsletters, chat groups, unsourced screenshots. |

Rules:

- Tier is source reliability, not claim strength.
- A high-tier source only supports claims it actually states.
- A Tier 1 filing that does not mention a customer cannot prove that customer relationship.
- Tier 5 can identify narrative, rumor origin, and crowding, but cannot close evidence.

## 4. Evidence roles

| Evidence role | Meaning |
|---|---|
| Strong Fact | Direct primary evidence for a specific claim. |
| Numeric baseline | Revenue, margin, valuation, ownership, liquidity, or time-series baseline that should be reconciled to primary sources. |
| Technical basis | Supports physical, engineering, scientific, or standards logic. |
| Event clue | Indicates a recent event that may need primary confirmation. |
| Corroboration | Indirect support that strengthens or weakens a thesis but is not standalone proof. |
| Rumor / narrative clue | Shows market narrative, rumor, crowding, or reflexivity risk. |

## 5. Agent setup protocol

When running `/alpha-research` setup preflight, the agent should follow this protocol:

1. Inventory current access and known tools.
2. For each of the 11 required information channels, assign a Channel Status.
3. For every `Missing` channel, propose acceptable tools or source paths from this document.
4. For every `Available with user action` channel, state the needed user action: API key, web login, browser login session, subscription access, or install confirmation.
5. For every local install candidate, use `resources/tool-install-sources.md`, identify canonical source/package names, describe the setup action type, and ask for confirmation before executing any command.
6. If the user approves runtime setup, commands must be scoped to the current environment and must not modify trading/brokerage accounts.
7. For every paid or access-restricted source, ask whether the user has access; do not bypass restrictions.
8. Produce a setup report with channels, available implementations, missing capabilities, and recommended next actions.
9. Do not claim the environment is report-ready if relevant required channels remain `Missing` or `Blocked by access / paid source`.

## 6. Tool selection principles

Use these principles when choosing among acceptable tools:

1. Prefer official primary sources over aggregators.
2. Prefer stable URLs, citations, timestamps, and retrievable originals.
3. Prefer target-market official sources.
4. Prefer tools that preserve provenance.
5. Prefer no-login tools only when evidence quality is equal.
6. Use paid/subscription tools only if the user has access.
7. Use browser automation only when normal fetch/search cannot access the source.
8. Use social tools only for narrative, rumor origin, crowding, or reflexivity.
9. Never upgrade social/news claims without primary confirmation.
10. For wrappers and aggregators, classify evidence by the underlying source, not by wrapper convenience.
11. If a relevant channel is missing, mark the gap instead of fabricating confidence.

## 7. Provenance capture requirements

Use layered provenance. Do not overburden every source, but preserve enough information for later evidence audit.

### All sources

Capture:

- Citation id (`[S1]`, `[S2]`, etc.).
- Source title.
- URL or stable locator.
- Publisher / owner.
- Source Confidence Tier.
- Evidence role.

### Key Fact sources

For any source used to support a key Fact, also capture:

- Publication date, filing date, or reporting period.
- Access date.
- Quoted excerpt, page number, table number, section name, or paragraph locator when possible.

Key Facts in a final report must have a citation id and a URL/stable locator. A search-result snippet is not enough.

### Social / narrative sources

For social or forum sources, also capture:

- Author / handle.
- Timestamp.
- Original post URL or stable screenshot locator.
- The exact claim being made.

## 8. Source freshness rules

| Source type | Freshness rule |
|---|---|
| Filings | Use latest annual report plus latest quarterly/interim report when available. |
| Earnings calls / presentations | Use the latest cycle; compare historical commentary when trend change matters. |
| News / events | Usually prefer last 12 months unless historical context is required. |
| Financial data | Use latest period plus 3–5 year trend when possible. |
| Technical papers | Recent papers matter for frontier claims; older seminal papers are acceptable for basic principles. |
| Patents | Record publication date, assignee, family, and legal status when available. |
| Social narrative | Timestamp is mandatory; stale social claims cannot prove current crowding. |
| Policy | Distinguish draft, consultation, final rule, effective date, and implementation details. |
| Industry reports | Check publication date and data vintage. |

## 9. Market coverage caveat

No tool covers all markets equally.

Rules:

- Match tool coverage to market scope.
- A US-focused tool may be weak for A-share, HK, China policy, or non-US markets.
- A social source strong for US narratives may be weak for China narratives, and vice versa.
- Financial data providers may have delayed, incomplete, restated, or differently standardized data.
- Reconcile important company-level facts to target-market primary sources.

Examples:

- Use SEC EDGAR for US filings, HKEXnews for HK disclosures, 巨潮资讯 and exchanges for A-share disclosures.
- Do not rely on X/Grok alone for A-share narrative; use 雪球、东方财富股吧、互动易、上证 e 互动 when relevant.
- Do not rely on generic news for China policy; use official ministries, regulators, and statistics sources.

## 10. Minimum acceptable evidence by research object

Use this section to decide whether the source plan is sufficient.

### Company research

Required:

- Filing / disclosure.
- Company IR.
- Financial data.
- News / event search.

Useful:

- Social / narrative search.
- Alternative data leads.
- Browser automation if disclosures or investor materials are dynamic.

Quality warning:

- Company research without filings/disclosures is not report-ready.
- Company research without financial data cannot support valuation, quality, liquidity, or balance-sheet discussion.
- Company research that discusses valuation, ranking, or relative priority needs the minimum data pack from `data-rigor.md` or explicit Data Gaps.
- Relative attractiveness claims need a peer/comparable baseline or a clear explanation of why clean peers are unavailable.

### Technology / material research

Required:

- Academic / technical search.
- Patent / standards search.
- Industry / market sources.
- Company exposure evidence for any mapped public company.

Useful:

- Alternative data leads.
- News / events.
- Procurement / tender data where commercialization depends on projects.

Quality warning:

- Do not use news or social media to establish technical feasibility.
- Papers explain technical possibility; they do not prove company revenue.

### Industry / supply-chain research

Required:

- Industry and market sources.
- Company filings / IR for mapped companies.
- Financial data for exposure and purity.
- News / events.

Useful:

- Trade / customs data.
- Procurement / tender data.
- Alternative data leads.
- Browser automation for supplier directories or dynamic databases.

Quality warning:

- Do not classify a company as a chokepoint without exposure and purity evidence.

### Policy / macro research

Required:

- Official policy source.
- Official statistics or macro data source.
- Industry / association data where relevant.
- News only as event clue.

Useful:

- Trade / customs data.
- Procurement / subsidy data.
- Local government sources.

Quality warning:

- Distinguish draft policy, final policy, implementation rules, and actual funding.

### Commodity / macro commodity research

Required:

- Commodity-specific official data source for supply, demand, inventory, reserves, or flows.
- Futures / benchmark source when price, curve, spread, contango, backwardation, or roll yield is discussed.
- Positioning / flow source when crowding, speculative length, ETF flow, or market-structure risk is discussed.
- Macro source when rates, FX, inflation, or growth drive the thesis.
- Company filings / IR and financial data for any commodity-linked candidate/company recommendation.

Useful:

- Shipping, sanctions, policy, weather, refinery, rig count, and trade data where material.
- Paid commodity terminals or datasets when the user has access.
- Browser automation for exchange tables or dynamic dashboards.

Quality warning:

- Price charts and news headlines are not enough for commodity research.
- Futures curve and positioning are market-structure evidence; they are not standalone proof of physical fundamentals.
- Commodity-linked company recommendations require both the commodity driver and company exposure evidence.

### Narrative / anti-hype research

Required:

- Original narrative source.
- Social / narrative search.
- Primary source confirmation or rejection.
- Thesis Audit evidence audit.
- Thesis Audit bear-case evidence.

Useful:

- Price / liquidity / ownership data.
- News timeline.
- Browser automation for social or forum sources.

Quality warning:

- Narrative research without original narrative capture cannot claim to have tested hype.

## 11. Required channel catalog

Every channel below is required for a complete Alpha Research environment.

### 11.1 Web Search

Purpose:

- Find public entry points, current news, official source names, company pages, industry terms, and narrative origin points.

| Tool / source | Setup Mode | Source Tier | Best for | Evidence role | Limitations |
|---|---|---:|---|---|---|
| Agent-native web search | Built-in | 4 | General discovery inside an agent runtime | Entry point / clue | Quality varies by runtime; must preserve URLs. |
| Perplexity | API key / Web login | 4 | Cited web answers and source discovery | Entry point / clue | Synthesized answers are not primary evidence. |
| Exa | API key | 4 | Semantic web search and source finding | Entry point / clue | Search result relevance does not imply evidence strength. |
| Tavily | API key | 4 | Search API for agent workflows | Entry point / clue | Requires source verification. |
| Brave Search | API key / Manual fallback | 4 | General web search with independent index | Entry point / clue | Results are discovery only. |
| Google Search | Manual fallback / API key | 4 | Broad discovery and site-specific search | Entry point / clue | Ranking is not evidence quality. |
| Bing Search | Manual fallback / API key | 4 | Broad discovery and news/source search | Entry point / clue | Requires source verification. |
| Kagi | API key / Web login | 4 | High-quality general search | Entry point / clue | Paid access may be needed. |
| SerpAPI | API key | 4 | Programmatic search results | Entry point / clue | Aggregates search engine results; not evidence. |
| DuckDuckGo | Manual fallback | 4 | Lightweight general search | Entry point / clue | Coverage and freshness vary. |

### 11.2 Web / PDF Fetch

Purpose:

- Read original web pages, filings, PDFs, presentations, annual reports, white papers, and technical documents.

| Tool / source | Setup Mode | Source Tier | Best for | Evidence role | Limitations |
|---|---|---:|---|---|---|
| Agent-native URL fetch | Built-in | Depends on source | Reading source pages | Depends on source | May fail on dynamic or blocked pages. |
| Browser fetch | Built-in / Browser login session | Depends on source | Reading pages with browser rendering | Depends on source | Must preserve URL and extracted text. |
| Jina Reader | Built-in / API key | Depends on source | Clean web page extraction | Depends on source | Extraction can omit tables or dynamic content. |
| Readability-style fetcher | Built-in / Local install | Depends on source | Clean article/page text | Depends on source | May remove important tables or footnotes. |
| PDF text extraction | Built-in / Local install | Depends on source | Filings, reports, white papers | Depends on source | Scanned PDFs need OCR. |
| PyMuPDF | Local install | Depends on source | PDF text/tables/page references | Depends on source | Table extraction can require manual validation. |
| pdftotext-like tools | Local install | Depends on source | Fast PDF text extraction | Depends on source | Layout and tables may be degraded. |
| OCR tools | Local install / API key | Depends on source | Scanned PDFs and images | Depends on source | OCR errors must be checked for key facts. |

### 11.3 Filing / Disclosure Access

Purpose:

- Verify revenue, risk factors, customers, capex, margins, ownership, dilution, business description, and official announcements.

| Tool / source | Setup Mode | Source Tier | Best for | Evidence role | Limitations |
|---|---|---:|---|---|---|
| SEC EDGAR | Built-in / Manual fallback | 1 | US 10-K, 10-Q, 20-F, 6-K, S-1, F-1 | Strong Fact | US-listed coverage; filings can be dense. |
| HKEXnews | Built-in / Manual fallback | 1 | HK announcements, annual/interim reports, prospectuses | Strong Fact | Search UX can be cumbersome. |
| 巨潮资讯 | Built-in / Manual fallback | 1 | A-share announcements and reports | Strong Fact | Some documents require careful Chinese parsing. |
| a-stock-data CNINFO access | Local install | 3 / underlying 1 | Optional A-share announcement discovery through CNINFO | Strong Fact only with original CNINFO provenance | External tool with code/dependencies; classify by original source. |
| Shanghai Stock Exchange disclosures | Built-in / Manual fallback | 1 | SSE filings and announcements | Strong Fact | Exchange-specific coverage. |
| Shenzhen Stock Exchange disclosures | Built-in / Manual fallback | 1 | SZSE filings and announcements | Strong Fact | Exchange-specific coverage. |
| Beijing Stock Exchange disclosures | Built-in / Manual fallback | 1 | BSE filings and announcements | Strong Fact | Smaller universe. |
| Company annual reports | Built-in / Manual fallback | 2 | Company primary annual disclosure | Strong Fact | Use official version and period. |
| Prospectuses | Built-in / Manual fallback | 1 / 2 | Business model, risks, history, ownership | Strong Fact | May become stale after listing. |
| Filing fetch APIs | API key / Local install | 1 / 3 | Programmatic filing access | Strong Fact | Must verify official source and document version. |
| Funda AI filings / transcripts | API key / Paid terminal / subscription | 1 / 3 depending on original | Optional SEC filings, transcripts, and report discovery | Strong Fact only with original filing provenance | Paid access; synthesized output is not primary evidence. |

### 11.4 Company IR Access

Purpose:

- Collect investor presentations, earnings calls, product pages, press releases, management commentary, and company-provided context.

| Tool / source | Setup Mode | Source Tier | Best for | Evidence role | Limitations |
|---|---|---:|---|---|---|
| Company IR website | Manual fallback / Browser login session | 2 | Official presentations, events, financial reports | Strong / Medium | Management framing may be promotional. |
| Earnings call transcripts | Web login / Paid terminal / Manual fallback | 2 / 3 | Management commentary and Q&A | Strong / Medium | Transcript accuracy and access vary. |
| Investor presentations | Manual fallback / Browser login session | 2 | Strategy, segments, product claims | Medium | Slides may omit risks and exact definitions. |
| Product pages | Manual fallback / Browser login session | 2 | Product existence and technical claims | Medium | Product page does not prove scale or revenue. |
| Company press releases | Manual fallback / Web login | 2 | Official event announcements | Event clue / Medium | Press releases can be selective. |
| Seeking Alpha transcripts | Web login / Paid subscription | 3 | US earnings transcripts | Medium | Not primary; verify against company where needed. |
| Koyfin / TIKR transcripts | Paid terminal / subscription | 3 | Transcripts and financial context | Medium | Paid access; provider coverage varies. |
| Broker transcript databases | Paid terminal / subscription | 3 | Detailed transcripts and notes | Medium | May include broker interpretation. |
| Funda AI transcripts / synthesis | API key / Paid terminal / subscription | 2 / 3 | Optional transcript discovery and research synthesis | Medium / Corroboration | Verify management quotes and key claims against original transcripts.

### 11.5 Financial Data Access

Purpose:

- Establish numeric baseline: revenue, margins, cash flow, valuation, liquidity, ownership, debt, share count, and segment exposure.

| Tool / source | Setup Mode | Source Tier | Best for | Evidence role | Limitations |
|---|---|---:|---|---|---|
| Company filings | Manual fallback / Built-in | 1 / 2 | Final reported financials | Strong Fact | Slow for screening; must normalize manually. |
| Exchange data pages | Manual fallback / Built-in | 1 / 3 | Official market data and announcements | Numeric baseline | Coverage and history vary. |
| yfinance | Local install | 3 | US/global price and basic fundamentals baseline | Numeric baseline | Coverage can be incomplete; reconcile key numbers. |
| a-stock-data | Local install / API key for iwencai | 3 / underlying source tier | Optional A-share quotes, valuation baseline, reports, flows, signal data, news, F10, and CNINFO access | Numeric baseline / Event clue / Corroboration | External skill with runtime dependencies; do not treat wrapper output as primary evidence. |
| Funda AI | API key / Web login / Paid terminal / subscription | 3 / underlying source tier | Optional paid raw data, filings, transcripts, options, ownership, supply-chain, news, and synthesis | Numeric baseline / Event clue / Corroboration | Paid access; synthesized answers require primary-source reconciliation. |
| TradingView reader | Local install / Browser login session / Paid terminal / subscription | 3 | Optional quotes, screeners, chart state, options chains, IV, and greeks | Numeric baseline / Corroboration | Read-only; data entitlements vary; not primary evidence. |
| AkShare | Local install | 3 | China market and macro data access | Numeric baseline | Data source changes can break fields. |
| Tushare | API key / Local install | 3 | China equity and financial datasets | Numeric baseline | API token and point limits may apply. |
| Financial Modeling Prep | API key | 3 | Financial statements and ratios | Numeric baseline | Provider methodology must be checked. |
| Alpha Vantage | API key | 3 | Prices and some fundamentals | Numeric baseline | Rate limits and coverage constraints. |
| Tiingo | API key | 3 | Market data and historical prices | Numeric baseline | API access required. |
| Polygon.io | API key | 3 | Market data, especially US | Numeric baseline | Paid tiers may be needed. |
| Nasdaq Data Link | API key | 3 | Datasets and time series | Numeric baseline | Dataset availability varies. |
| Koyfin | Paid terminal / subscription | 3 | Financial screens and charts | Numeric baseline | Paid access; reconcile key facts. |
| TIKR | Paid terminal / subscription | 3 | Global company financials | Numeric baseline | Paid access; coverage varies. |
| Bloomberg / FactSet / Refinitiv | Paid terminal / subscription | 3 | Professional financial data | Numeric baseline | Expensive; methodology still needs checking. |
| EIA | Built-in / Manual fallback / API key | 1 | US oil/gas inventories, production, refinery runs, STEO | Strong Fact / Numeric baseline | API key for API calls; record table/series, period, units. |
| IEA / OPEC / JODI | Manual fallback / Paid terminal / subscription | 3 / 4 | Global oil balances, country oil data, OPEC context | Numeric baseline / Corroboration | Access and incentives vary; preserve definitions. |
| CME / ICE futures | Manual fallback / Paid terminal / subscription | 1 / 3 | Commodity futures curves, contracts, spreads | Numeric baseline / Market-structure evidence | Delayed/real-time caveat; curve is not standalone fundamental proof. |
| CFTC COT | Built-in / Manual fallback | 1 | Futures positioning and crowding | Market-structure evidence | Weekly lag; not a direct price signal. |
| World Gold Council / LBMA | Manual fallback / Web login / Paid terminal / subscription | 3 / 4 | Gold ETF flows, reserves, demand/supply, precious-metal benchmark context | Numeric baseline / Corroboration | Some downloads/licensed data may require login. |
| FRED / Treasury macro | Built-in / Manual fallback / API key | 1 / 3 | Real yields, rates, inflation expectations, dollar/macro drivers | Macro baseline | Record series id, frequency, units, and transformations. |

### 11.6 Academic / Technical Search

Purpose:

- Understand material science, engineering constraints, architecture changes, performance limits, and technical substitution risk.

| Tool / source | Setup Mode | Source Tier | Best for | Evidence role | Limitations |
|---|---|---:|---|---|---|
| arXiv | Built-in / Manual fallback | 3 | Preprints and frontier technical work | Technical basis | Preprints may not be peer reviewed. |
| Semantic Scholar | API key / Manual fallback | 3 | Paper discovery and citation graph | Technical basis | Metadata can be incomplete. |
| Google Scholar | Manual fallback | 3 | Broad academic discovery | Technical basis | Access and scraping are constrained. |
| IEEE pages | Web login / Paid subscription / Manual fallback | 3 | Electrical, semiconductor, communications standards/papers | Technical basis | Paywalls common. |
| ACM Digital Library | Web login / Paid subscription | 3 | Computing research | Technical basis | Paywalls common. |
| PubMed | Built-in / Manual fallback | 3 | Biomedical and life sciences | Technical basis | Not company revenue evidence. |
| SSRN | Manual fallback / Web login | 3 | Finance/economics working papers | Technical basis | Working papers may change. |
| University/lab publications | Manual fallback | 3 / 4 | Technical context and early research | Technical basis | Commercial readiness is not implied. |
| Standards body documents | Manual fallback / Paid subscription | 1 / 3 | Official technical standards | Technical basis / Strong Fact | Access varies by standards body. |

### 11.7 Patent / Standards Search

Purpose:

- Track technical routes, company R&D focus, possible moats, and standards adoption.

| Tool / source | Setup Mode | Source Tier | Best for | Evidence role | Limitations |
|---|---|---:|---|---|---|
| Google Patents | Manual fallback | 3 | Patent discovery and family lookup | Technical basis | Patent count does not prove business traction. |
| The Lens | Web login / Manual fallback | 3 | Patent and scholarly search | Technical basis | Advanced features may require account. |
| PatentsView | Built-in / API key | 3 | US patent data analysis | Technical basis | US-focused. |
| USPTO | Manual fallback | 1 | Official US patent records | Technical basis | Interface can be complex. |
| WIPO Patentscope | Manual fallback | 1 | International patent applications | Technical basis | Legal status needs care. |
| Espacenet | Manual fallback | 1 / 3 | European/global patent search | Technical basis | Interface complexity. |
| CNIPA patent search | Manual fallback | 1 | China patent records | Technical basis | Chinese search terms needed. |
| IEEE / 3GPP / JEDEC / ISO / IEC | Manual fallback / Paid subscription | 1 | Official standards | Technical basis / Strong Fact | Some standards are paywalled. |
| OCP / PCI-SIG / CXL / UCIe groups | Manual fallback / Web login | 1 / 3 | Architecture and interoperability standards | Technical basis | Membership/access limitations may apply. |

### 11.8 News / Event Search

Purpose:

- Track recent events, orders, policy changes, customer announcements, capacity additions, lawsuits, recalls, and geopolitical shifts.

| Tool / source | Setup Mode | Source Tier | Best for | Evidence role | Limitations |
|---|---|---:|---|---|---|
| Google News | Manual fallback | 4 | Broad news discovery | Event clue | News is not primary confirmation. |
| Bing News | Manual fallback / API key | 4 | Broad news discovery | Event clue | Requires source verification. |
| GDELT | API key / Manual fallback | 4 | Global event/news database | Event clue | Entity matching can be noisy. |
| Company press releases | Manual fallback | 2 | Official company events | Event clue / Medium | Promotional framing. |
| Funda AI news / event timeline | API key / Paid terminal / subscription | 3 / 4 | Optional structured news, transcripts, event timelines | Event clue / Corroboration | Paid access; verify key claims against originals. |
| TradingView news | Local install / Browser login session / Paid terminal / subscription | 4 | Optional market news discovery | Event clue | Read-only; preserve original story links. |
| Regulatory news services | Built-in / Manual fallback | 1 / 3 | Official market announcements | Strong / Event clue | Market-specific coverage. |
| Reputable financial media | Web login / Paid subscription / Manual fallback | 4 | Event context and interviews | Medium / Event clue | Separate reporting from interpretation. |
| Trade publications | Web login / Paid subscription / Manual fallback | 4 | Industry-specific events | Medium / Event clue | May rely on unnamed sources. |
| Local business journals | Web login / Paid subscription / Manual fallback | 4 | Local plant, hiring, subsidy, litigation events | Event clue | Coverage can be fragmented. |
| Government policy websites | Manual fallback | 1 | Official policy events | Strong Fact | Must track effective status. |

### 11.9 Social / Narrative Search

Purpose:

- Identify real-time market narratives, rumor origin, crowding, influencer claims, and reflexivity risk.

| Tool / source | Setup Mode | Source Tier | Best for | Evidence role | Limitations |
|---|---|---:|---|---|---|
| X / Twitter search | Web login / Browser login session | 5 | US/global real-time narrative | Rumor / narrative clue | Never Strong Fact; access varies. |
| Grok with X access | Web login / Paid subscription | 5 | X-native narrative and recent discussions | Rumor / narrative clue | Depends on subscription and X coverage. |
| Reddit search | Web login / Manual fallback | 5 | Retail narrative and community concerns | Rumor / narrative clue | Not representative of fundamentals. |
| Stocktwits | Web login / Manual fallback | 5 | US stock chatter | Rumor / narrative clue | High noise. |
| Seeking Alpha comments | Web login / Paid subscription | 5 | Investor narrative around articles | Rumor / narrative clue | Not primary evidence. |
| 雪球 | Web login / Browser login session | 5 | China/HK retail narrative | Rumor / narrative clue | High noise; login may be needed. |
| 东方财富股吧 | Web login / Browser login session / Manual fallback | 5 | A-share retail narrative | Rumor / narrative clue | High noise and manipulation risk. |
| 同花顺社区 | Web login / Browser login session | 5 | A-share retail narrative | Rumor / narrative clue | High noise. |
| OpenCLI reader | Local install / Browser login session | Underlying source tier, often 5 for social | Read-only dynamic/social/feed extraction | Rumor / narrative clue / depends on source | Transport layer only; never cite wrapper as proof. |
| OpenCLI-like website control | Local install / Browser login session | 5 | Logged-in social and dynamic pages | Rumor / narrative clue | Tool controls access; source remains low tier. |
| Agent browser tools | Built-in / Browser login session | 5 | Social page extraction | Rumor / narrative clue | Must preserve original URLs/timestamps. |

### 11.10 Browser Automation for Dynamic or Logged-in Pages

Purpose:

- Access dynamic pages, logged-in data, tables, social sites, filings interfaces, screenshots, and pages that normal fetch tools cannot read.

| Tool / source | Setup Mode | Source Tier | Best for | Evidence role | Limitations |
|---|---|---:|---|---|---|
| Playwright | Local install | Depends on source | Browser automation and screenshots | Depends on source | Requires local setup; do not bypass access controls. |
| Agent browser tools | Built-in / Browser login session | Depends on source | Interactive pages and logged-in sessions | Depends on source | Depends on runtime. |
| OpenCLI reader | Local install / Browser login session | Depends on source | Read-only adapter access to dynamic websites and logged-in pages | Depends on source | User must approve setup and login reuse; no write actions. |
| OpenCLI-like tools | Local install / Browser login session | Depends on source | Turning web apps into controllable CLI-like interfaces | Depends on source | Needs setup and user login for protected sites. |
| Browser DevTools automation | Built-in / Local install | Depends on source | Debugging/extracting dynamic pages | Depends on source | Technical overhead. |
| Browser extensions controlled by agent | Local install / Browser login session | Depends on source | Logged-in workflows | Depends on source | Security and privacy considerations. |

### 11.11 Alternative Data Leads

Purpose:

- Find indirect evidence for demand, supply, capacity, hiring, pricing, channel traction, customer behavior, and supply-chain shifts.

| Tool / source | Setup Mode | Source Tier | Best for | Evidence role | Limitations |
|---|---|---:|---|---|---|
| Funda AI alternative datasets | API key / Paid terminal / subscription | 3 / 5 depending on dataset | Optional ownership, sentiment, government trading, hiring, and supply-chain leads | Corroboration / Rumor clue | Paid access; verify material claims with primary sources. |
| Job postings | Manual fallback / Browser login session / API key | 4 | Hiring direction and capacity hints | Corroboration | Hiring is indirect evidence. |
| Supplier directories | Manual fallback / Browser login session | 4 | Supplier/customer ecosystem mapping | Corroboration | Directory presence does not prove revenue. |
| Import/export data | Paid subscription / Manual fallback | 3 / 4 | Trade flows and customer/supplier clues | Corroboration | Coverage and entity matching vary. |
| Tender and procurement databases | Manual fallback / Browser login session | 1 / 3 | Project demand and government/customer buying | Strong / Corroboration | Award does not always equal revenue recognition. |
| Government subsidy databases | Manual fallback | 1 | Subsidy and project support | Strong / Corroboration | Need actual disbursement/implementation status. |
| Pricing trackers | API key / Paid subscription / Manual fallback | 3 / 4 | Commodity or component pricing | Numeric baseline / Corroboration | Methodology and sample size matter. |
| Capacity announcements | Manual fallback / News search | 2 / 4 | Supply expansion | Event clue | Announced capacity may not be delivered. |
| App/web traffic tools | Paid subscription / API key | 3 | Digital demand signals | Corroboration | Methodology can be opaque. |
| Satellite/geospatial data | Paid subscription | 3 | Physical activity and logistics | Corroboration | Expensive and specialized. |
| Customer reviews/channel checks | Manual fallback / Browser login session | 5 / 4 | Product feedback and channel traction | Weak / Corroboration | Anecdotal and biased. |

## 12. Market-specific source map

Use the same Source Functions across markets. If a function is not relevant, mark `Not material / no common official source`.

### 12.1 US

| Source Function | Primary sources / tools | Source Tier | Notes |
|---|---|---:|---|
| Company disclosure | SEC EDGAR; 10-K, 10-Q, 8-K, 20-F, 6-K, S-1, F-1 | 1 | Core source for US-listed companies. |
| Company IR | Company IR pages, earnings calls, presentations, press releases | 2 | Verify management claims against filings. |
| Exchange / market data | Nasdaq, NYSE, Cboe, OTC Markets, FINRA where relevant | 1 / 3 | Market data and listing context. |
| Company registry / legal entity | State registries, Delaware Division of Corporations, SEC company identifiers | 1 / 3 | Entity data can be limited without paid tools. |
| Sector regulator | FDA, DOE, FCC, FERC, EPA, NHTSA, FAA, CMS, USDA, CFTC, FTC, DOJ as relevant | 1 | Choose by sector. |
| Macro / policy data | BEA, BLS, Census Bureau, Federal Reserve, Treasury, EIA, USDA | 1 | Use official series and release dates. |
| Trade / customs / tariff | USITC DataWeb, USTR, Commerce, Census trade data, CBP | 1 | Useful for tariffs and trade flows. |
| Industry statistics / association data | SIA, AIA, API, EEI, NAR, industry-specific associations | 4 / 3 | Check methodology and sponsor incentives. |
| Procurement / tender / subsidy | SAM.gov, USAspending.gov, Grants.gov, DOE awards, state incentive databases | 1 | Distinguish award, obligation, and disbursement. |
| Investor interaction / Q&A | Earnings call Q&A, investor day Q&A | 2 / 3 | No common official retail Q&A system like A-share. |

### 12.2 HK

| Source Function | Primary sources / tools | Source Tier | Notes |
|---|---|---:|---|
| Company disclosure | HKEXnews announcements, annual/interim reports, prospectuses | 1 | Core source for HK-listed companies. |
| Company IR | Company IR pages, presentations, webcasts, press releases | 2 | Verify claims against HKEX filings. |
| Exchange / market data | HKEX market data, CCASS data where relevant | 1 / 3 | Ownership/settlement data can help liquidity analysis. |
| Company registry / legal entity | Hong Kong Companies Registry / ICRIS | 1 | May require web access or paid document retrieval. |
| Sector regulator | SFC, HKMA, Insurance Authority, OFCA, Transport Department as relevant | 1 | Choose by sector. |
| Macro / policy data | Census and Statistics Department, HKMA, HKSAR government departments | 1 | Official macro and policy data. |
| Trade / customs / tariff | Census and Statistics Department trade data, Trade and Industry Department | 1 | Use official trade series. |
| Industry statistics / association data | HKTDC, industry associations, sector bodies | 3 / 4 | Check data vintage and methodology. |
| Procurement / tender / subsidy | HKSAR tender notices, government procurement pages | 1 | Relevant for public projects. |
| Investor interaction / Q&A | Earnings call Q&A, company briefings | 2 / 3 | No broad official investor Q&A system. |

### 12.3 A-share

| Source Function | Primary sources / tools | Source Tier | Notes |
|---|---|---:|---|
| Company disclosure | 巨潮资讯, 上交所公告, 深交所公告, 北交所公告, annual/interim/quarterly reports | 1 | Core source for A-share companies. |
| Company IR | Company IR pages, results briefings, exchange-hosted investor relations records | 2 | Verify with official announcements. |
| Exchange / market data | 上交所, 深交所, 北交所, 中证指数, 中登 where relevant; a-stock-data as optional acquisition wrapper | 1 / 3 | Use official exchange/index sources where possible; reconcile wrapper output to original sources for key facts. |
| Company registry / legal entity | 国家企业信用信息公示系统, 信用中国 | 1 | Legal entity and administrative information. |
| Sector regulator | 证监会, 金融监管总局, 人民银行, 工信部, 发改委, 能源局, 药监局 etc. | 1 | Choose by sector. |
| Macro / policy data | 国家统计局, 发改委, 工信部, 财政部, 人民银行, 能源局 | 1 | Official macro and policy layer. |
| Trade / customs / tariff | 海关总署, 商务部, 税委会 / tariff-related official sources | 1 | Use official trade/customs data. |
| Industry statistics / association data | 中国汽车工业协会, 中国半导体行业协会, 中国光伏行业协会, sector associations | 4 / 3 | Association data may be useful but methodology varies. |
| Procurement / tender / subsidy | 中国政府采购网, 全国公共资源交易平台, 中国招标投标公共服务平台, local government procurement platforms | 1 / 3 | Verify award, project status, and purchaser. |
| Investor interaction / Q&A | 深交所互动易, 上证 e 互动, 北交所 investor interaction where available | 2 / 5 | Company answers are useful but not equivalent to audited filings. |

### 12.4 China macro / policy / industry data

This layer includes official and quasi-official sources only. It excludes social media and financial-media narrative.

| Source Function | Primary sources / tools | Source Tier | Notes |
|---|---|---:|---|
| Company disclosure | Not material / use A-share, HK, or global company disclosure sources | — | This group is not company-disclosure first. |
| Company IR | Not material / use target company's IR | — | Use company-specific market source. |
| Exchange / market data | Not material unless tied to listed securities | — | Use A-share/HK/US market sources. |
| Company registry / legal entity | 国家企业信用信息公示系统, 信用中国 | 1 | Useful for legal entity checks. |
| Sector regulator | 发改委, 工信部, 财政部, 人民银行, 商务部, 能源局, 药监局, 生态环境部, 交通运输部, 住建部, 农业农村部, 自然资源部, 市监总局 | 1 | Choose by sector and policy question. |
| Macro / policy data | 国家统计局, 人民银行, 财政部, 发改委, 工信部, 地方统计局 / 发改委 / 工信厅 | 1 | Official macro, production, investment, and policy data. |
| Trade / customs / tariff | 海关总署, 商务部, 税委会, port/local customs releases | 1 | Trade flow and tariff evidence. |
| Industry statistics / association data | Official or quasi-official industry associations; sector yearbooks where available | 3 / 4 | Check methodology, sponsor, and data vintage. |
| Procurement / tender / subsidy | 中国政府采购网, 全国公共资源交易平台, 地方公共资源交易中心, 中国招标投标公共服务平台, ministry/local subsidy notices | 1 / 3 | Distinguish policy intent, award, and actual disbursement. |
| Investor interaction / Q&A | Not material unless linked to listed companies | — | Use A-share investor interaction channels. |

### 12.5 Global / non-US non-HK non-A-share

| Source Function | Primary sources / tools | Source Tier | Notes |
|---|---|---:|---|
| Company disclosure | Local exchange filings, local securities regulator, company annual reports | 1 / 2 | Identify the home market's official disclosure system. |
| Company IR | Company IR pages, annual reports, presentations, press releases | 2 | Verify against local filings. |
| Exchange / market data | Local exchange, index provider, market regulator | 1 / 3 | Coverage differs by country. |
| Company registry / legal entity | Local company registry, commercial registry, court registry | 1 / 3 | Access and language vary. |
| Sector regulator | Local sector regulators; EU/EMA/ECHA/ESMA/ECB etc. where relevant | 1 | Choose by jurisdiction and sector. |
| Macro / policy data | National statistics office, central bank, finance ministry, World Bank, IMF, OECD, Eurostat | 1 / 3 | Prefer national official data when possible. |
| Trade / customs / tariff | UN Comtrade, WTO, ITC Trade Map, national customs, tariff authorities | 1 / 3 | Entity/product mapping can be hard. |
| Industry statistics / association data | IEA, IRENA, OPEC, WSTS, SEMI, GSMA, IATA, sector associations | 3 / 4 | Check methodology and member incentives. |
| Procurement / tender / subsidy | Government procurement portals, EU TED, World Bank procurement, local tender systems | 1 / 3 | Verify award and implementation status. |
| Investor interaction / Q&A | Earnings calls, investor days, AGM materials | 2 / 3 | Varies by market practice. |

### 12.6 Commodity / macro commodity

| Source Function | Primary sources / tools | Source Tier | Notes |
|---|---|---:|---|
| Commodity supply / demand / inventory | EIA, IEA, OPEC, JODI, WGC, official exchange/warehouse sources, national ministries | 1 / 3 / 4 | Choose by commodity; record period and units. |
| Futures / benchmark data | CME, ICE, LBMA, SGE, LME, SHFE/INE, recognized market-data provider | 1 / 3 | Required for curve/spread/benchmark claims. |
| Positioning / flows | CFTC COT, ETF holdings/flows, exchange open interest, fund-flow data | 1 / 3 | Required for crowding/positioning claims. |
| Macro drivers | FRED, US Treasury, Federal Reserve, central banks, national statistics offices | 1 / 3 | Required for rates/FX/inflation/growth claims. |
| Physical constraints | inventories, refinery runs, rig count, mine supply, sanctions, shipping, weather, policy | 1 / 3 / 4 | Match source to physical driver. |
| Company disclosure | SEC/HKEX/CNINFO/local exchange filings, company IR, reserve/production reports | 1 / 2 | Required for commodity-linked company recommendations. |
| Narrative / geopolitics | Official policy/sanctions/shipping/security source plus reputable media | 1 / 4 / 5 | Media/social are clues unless confirmed by primary source. |

## 13. Hard source gate rules

These rules constrain Alpha Research before a final report can be produced.

Hard source gate status is not a grade. It is a pass/fail gate.

If any required hard gate fails, stop final-report generation. Produce a Source Gate Failure report and a Source Acquisition Plan instead. Do not continue to polished `report.html` as if the research is complete.

| Hard gate failure | Applies when | Required action |
|---|---|---|
| No Source Registry exists | Any Alpha Research final report | Stop. Build Source Registry first. |
| Key Facts lack citation ids with URL / stable locator | Any Alpha Research final report | Stop. Collect previewable sources or stable locators. |
| Final citations would not be clickable | Any final HTML report | Stop. Convert Source Registry entries to clickable inline citations and bibliography links. |
| Local artifact cited as proof for external Fact | Any final HTML report | Stop. Replace local report/source-map links with the original source URLs used by that artifact. |
| Evidence comes only from web search snippets | Any Alpha Research final report with key Facts | Stop. Open the real page, filing, PDF, data endpoint, original post, or official source. |
| Filing / disclosure source missing | Company research or listed-company map | Stop for company conclusions. Fetch official filing/disclosure or remove company-level conclusions. |
| Financial baseline missing | Company research or public-company ranking | Stop for valuation/quality/purity ranking. Fetch financial data or remove ranking. |
| Company IR / primary company source missing | Product, customer, deployment, roadmap, or management claim | Stop for that claim. Fetch company source or downgrade/remove the claim. |
| Technical source missing | Technology, material, semiconductor, biotech, or engineering-heavy thesis | Stop for technical feasibility claims. Fetch paper, standard, patent, or official technical source. |
| Market-specific official source missing | US / HK / A-share / China policy / other market facts | Stop for those market-specific facts. Use target-market official source. |
| Top chokepoint lacks direct evidence | Industry / supply-chain research | Stop before ranking it as a core chokepoint. Add evidence or demote to hypothesis. |
| Commodity balance source missing | Commodity / macro commodity research | Stop before making supply/demand/inventory conclusions. Add official or recognized commodity data. |
| Futures curve / positioning source missing | Commodity curve, roll-yield, contango/backwardation, or crowding claim | Stop before making market-structure conclusions. Add exchange/CFTC/flow source or remove claim. |
| Commodity-linked company exposure missing | Candidate/company recommendation tied to commodity driver | Stop before recommending the company. Add filings/IR/financial baseline and exposure logic. |
| Original narrative source missing | Anti-hype mode | Stop before claiming narrative origin/crowding path. Find earliest visible source or mark unknown. |
| OpenCLI/browser/social/manual narrative capture missing | Anti-hype mode with social/forum/narrative claims | Stop before claiming origin or crowding path. Use an original source capture path, or mark the channel blocked and ask for user approval/access. |
| Financial data source missing | Company ranking, valuation, liquidity, or candidate comparison | Stop before ranking or valuation discussion. Use yfinance, a-stock-data, Funda, TradingView, official filings/exchange data, or documented manual equivalent. |
| Aggregator/wrapper cited as primary proof | Any key Fact | Stop. Preserve original source provenance or downgrade to baseline/corroboration. |

Allowed blocked output:

- `source-gate.md`, `tool-status.md`, or a clearly marked section in `source-map.md` / `report-quality.md`.
- Missing source list.
- Source Acquisition Plan.
- Questions for the user: API key, login, subscription, browser session, or permission to run approved setup commands.

Disallowed blocked output:

- A polished final report with confident conclusions.
- Company priority ranking based on missing filings/financial data.
- Strong Facts without previewable citations.

## 14. Quality ceiling rules

These rules constrain `Report Quality` stage after the hard source gate passes.

They are report quality limits, not investment ratings.

| Condition | Maximum Quality Grade | Reason |
|---|---|---|
| Any relevant required channel is `Missing` | B | Source coverage is incomplete. |
| Any relevant required channel is `Blocked by access / paid source` and no substitute exists | B | Access gap may hide important evidence. |
| Filing / disclosure access is missing for company research | C | Company research lacks primary disclosure. |
| Company IR is missing for company research | B | Management and product context are incomplete. |
| Financial data is missing for company research | C | Numeric baseline is insufficient. |
| Academic / technical search is missing for technology, material, biotech, semiconductor, or engineering-heavy topics | C | Technical basis cannot be validated. |
| Patent / standards search is missing when technical moat or standard adoption is central | B | Technical route and moat analysis is incomplete. |
| Social / narrative search is missing for anti-hype mode | B | Narrative origin and crowding were not checked. |
| Market-specific official sources are not checked for the target market | C | Wrong-market evidence risk. |
| Commodity-specific official/recognized data is missing for commodity balance claims | C | Supply/demand/inventory thesis lacks commodity data. |
| Futures curve or positioning data is missing when curve/crowding is central | B | Market-structure analysis is incomplete. |
| Commodity-linked company recommendation lacks filings/IR/financial baseline | C | Candidate logic lacks company-level proof. |
| Most key claims rely on news or social sources without primary confirmation | D | Mostly narrative. |
| Source provenance is unclear for key Facts | C | Claims are not auditable. |
| Key Facts lack citation ids with URL / stable locator | C | Readers cannot preview or verify the data. |
| Final HTML citations are not clickable | C | Readers cannot verify claims from the report. |
| Local artifacts are cited as proof for external Facts | C | The report points to process output instead of original evidence. |
| A wrapper or aggregator is cited without original source provenance for key Facts | C | Tool output is not auditable enough for primary claims. |
| Signal/flow/hot-tag/chart data is used as fundamental proof | D | Market-structure or narrative data was upgraded beyond what it can prove. |
| Anti-hype narrative origin is discussed without OpenCLI/browser/social/manual original-source capture | C | Narrative/crowding path is not auditable. |
| Company ranking or valuation uses only articles/search summaries and no financial data source | C | Numeric baseline is not reliable enough. |
| Key source dates are stale or unknown for time-sensitive claims | C | Freshness risk. |

Rules:

- Quality Grade A requires no material source-channel gaps for the selected research object.
- Quality Grade B may still have evidence gaps, but they must be explicit and non-fatal.
- Quality Grade C means more source work is needed before the report should be treated as reliable.
- Quality Grade D means the report is mostly narrative or not acceptable as research.

## 15. Required setup output

A setup review should produce:

| Channel | Channel Status | Available implementation | Setup Mode | Missing capability / user action | Notes |
|---|---|---|---|---|---|
| Web search |  |  |  |  |  |
| Web / PDF fetch |  |  |  |  |  |
| Filing / disclosure |  |  |  |  |  |
| Company IR |  |  |  |  |  |
| Financial data |  |  |  |  |  |
| Academic / technical |  |  |  |  |  |
| Patent / standards |  |  |  |  |  |
| News / event |  |  |  |  |  |
| Social / narrative |  |  |  |  |  |
| Browser automation |  |  |  |  |  |
| Alternative data leads |  |  |  |  |  |

## 16. Final rule

Information quality determines research quality.

A beautiful report built from weak sources is still weak research.
