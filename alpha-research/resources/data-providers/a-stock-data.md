# a-stock-data Playbook

## Best for

A-share data acquisition inside an Alpha Research workflow.

Use it as an optional external skill/tool when the research object is an A-share company, theme, sector, or A-share market narrative and the agent needs quick access to:

- real-time quotes, K-line data, PE/PB, market cap, turnover, index, and ETF data;
- research report discovery and consensus EPS clues;
- theme / concept attribution, northbound flow, fund flow, Dragon Tiger List, lock-up expiry, industry ranking;
- margin trading, block trades, shareholder count, dividends, and 120-day fund flow;
- stock news and market news;
- basic company data, F10 text, financial statements, and CNINFO announcements.

Project: `https://github.com/simonlin1212/a-stock-data`.

## Canonical install source

Use `../tool-install-sources.md` before setup.

| Field | Value |
|---|---|
| Canonical source | `https://github.com/simonlin1212/a-stock-data` |
| External skill file | `https://raw.githubusercontent.com/simonlin1212/a-stock-data/main/SKILL.md` |
| Runtime packages documented upstream | `mootdx`, `requests`, `pandas`, `stockstats` |
| Setup Mode | Local install; API key only for iwencai semantic report search |
| Verify | Import packages; run a tiny read-only sample only after approval |

Do not vendor the external `SKILL.md` into this repository. Treat it as an optional external capability the user may install or load in their own agent runtime.

## Optional runtime execution policy

During an actual research run, an agent may check availability, execute code snippets, or install required local dependencies only after explicit user approval for the current environment.

Keep usage read-only. Do not place trades, submit orders, modify brokerage accounts, or run high-frequency batch extraction.

## Detection flow

1. Check whether the user wants A-share runtime data acquisition.
2. Check Python package availability only after approval.
3. If missing, ask whether to install documented upstream packages.
4. If iwencai semantic report search is needed, ask for API key; otherwise no key is required by most documented endpoints.
5. Run only a small read-only sample first.
6. If an endpoint is blocked, rate-limited, stale, or missing, mark the data gap and use official/manual fallback.

Suggested status labels:

| Status | Meaning |
|---|---|
| `ASTOCK_READY` | dependencies available and a small read-only sample works. |
| `ASTOCK_DEPS_MISSING` | required Python packages missing. |
| `ASTOCK_IWENCAI_KEY_NEEDED` | semantic report search requested but key missing. |
| `ASTOCK_ENDPOINT_BLOCKED` | endpoint failed, rate-limited, or source changed. |
| `ASTOCK_NOT_APPROVED` | user did not approve runtime execution/install. |

## Source Tier

Tier depends on the underlying source preserved in the output:

| Underlying source | Tier | Evidence role |
|---|---:|---|
| CNINFO / exchange announcement reached through the tool | 1 | Strong Fact only if original title, date, URL, and excerpt are preserved. |
| Company F10 / company primary material | 2 | Company primary context; verify material facts with filings. |
| mootdx / Tencent / Eastmoney / Sina / THS / Baidu market data | 3 | Numeric baseline or corroboration. |
| Eastmoney / THS reports, news, and market information | 4 / 3 | Event clue, consensus clue, or market context. |
| Theme attribution, fund flow, hot-stock tags, forum-like signal data | 3 / 5 depending on source | Corroboration or narrative clue, not standalone Fact. |

The wrapper itself is not the source of truth. Classify evidence by the original data source.

## Structured acquisition recipe

### A-share company baseline

1. Use official CNINFO/exchange filings for final company Facts.
2. Use a-stock-data for quick baseline:
   - quote / market cap / PE/PB;
   - K-line and volume;
   - announcements discovery;
   - F10/basic company context;
   - financial statements snapshot;
   - shareholder count/dividends/lock-up where relevant.
3. Preserve endpoint/function/source names and original URLs if available.
4. Reconcile key values to annual/quarterly reports before final report.

### A-share theme / concept scan

1. Use concept blocks, industry ranking, hot-stock tags, and report search as discovery.
2. Treat concept attribution as hypothesis, not Fact.
3. For every mapped company, verify real exposure through filings/IR/announcements.
4. Separate direct beneficiary from concept-only.

### Anti-hype / crowding

1. Use hot-stock tags, fund flow, Dragon Tiger List, news, concept blocks.
2. Keep all signal data below Strong Fact unless primary evidence confirms it.
3. Preserve timestamped source provenance.
4. Use `Thesis Audit` stage for crowding/reflexivity interpretation.

## Required provenance

For each extracted item, record:

- Original source name, not only `a-stock-data`.
- Endpoint/function/source category.
- Ticker, exchange, and company name.
- Date / time range / reporting period.
- Access date.
- Original URL or stable locator when available.
- Field names and units for numeric values.
- Quote/page/table/section for any key Fact.

For CNINFO announcements, preserve announcement title, publication date, document URL, page/section if available, and quoted Chinese excerpt.

## What it can support

- Fast initial A-share numeric baseline for source mapping.
- A-share ticker normalization and market-prefix convenience.
- Initial valuation context: price, market cap, PE/PB, consensus EPS clues.
- Event discovery: announcements, reports, news, lock-up expiry, Dragon Tiger List, block trades.
- Narrative and signal discovery: themes, concept blocks, strong-stock reasons, northbound flow, fund flow.
- Candidate evidence leads for Source Registry and Thesis Audit.

## What it cannot support

- Final audited financial facts unless reconciled to official filings.
- Direct buy/sell signals, target prices, or position sizing.
- Proof of a customer relationship, order, revenue exposure, or moat unless a primary source states it.
- Stable long-term availability of every endpoint.
- Bypassing website access controls, rate limits, or data-provider terms.

## Rate limits and fragility

The upstream project documents endpoint breakage and anti-scraping risk, especially for Eastmoney-style endpoints.

Rules:

- Do not run high-concurrency or high-frequency batch extraction.
- Prefer official sources for final evidence.
- Mark data gaps when an endpoint fails.
- Do not silently substitute stale or failed values.
- If local execution requires installation, ask the user before installing anything.

## Source Gate rules

Hard gate fails if:

- A-share company Facts lack CNINFO/exchange/company source;
- concept tags are used as proof of company exposure;
- financial rankings lack reporting period/date and field provenance;
- wrapper output lacks original source provenance for key Facts.

## Fallbacks

- CNINFO, 上交所, 深交所, 北交所 official disclosure pages.
- Company IR pages.
- Tushare for structured China equity data.
- AkShare for exploratory China market and macro data.
- Official exchange, index, regulator, statistics, customs, procurement, and policy sources.
- Manual browser search with preserved provenance.
