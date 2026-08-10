# Tool Install Sources

This file is the canonical install-source catalog for optional Alpha Research data tools.

It does not make these tools required dependencies of this repository.

Agents must use this catalog before proposing or running setup. Do not guess package names from memory.

Use with:

- `source-profiles.md` to know which channels are required.
- `source-recipes.md` to know acquisition order.
- `data-providers/*.md` to know source-specific evidence rules.

## Rules

1. Ask the user before installing or configuring anything.
2. Prefer read-only commands.
3. Preserve original source provenance.
4. Classify evidence by underlying source, not by wrapper tool.
5. Do not commit installed dependencies, virtualenvs, node_modules, browser profiles, or generated runtime folders.
6. If a tool's upstream docs changed, verify with the canonical source before running commands.

## Finance-skills reference pattern

The `finance-skills` repository gets data through four patterns:

| Pattern | Example in finance-skills | What to copy into Alpha Research | What not to copy |
|---|---|---|---|
| Python package data access | `yfinance-data`, `earnings-preview`, `stock-liquidity` | Runtime detection, package name, structured output, caveats | Automatic install without user approval; trade-like outputs |
| API / MCP provider | `funda-data`, `finance-sentiment` | API key checks, endpoint map, fallback path, source caveats | Treating provider synthesis as primary proof |
| OpenCLI browser/session reader | `twitter-reader`, `opencli-reader`, `tradingview-reader` | Read-only guardrails, `opencli doctor`, browser login/session checks | Write actions, social actions, watchlist/alert edits |
| Plugin-specific adapter | TradingView opencli plugin | Canonical plugin source, status check, structured output | Vendoring plugin code into this repo |

Alpha Research should reuse the acquisition pattern, not copy the trading/valuation behavior.

## Provider resource paths

| Tool / source | Provider resource |
|---|---|
| yfinance | `data-providers/yfinance.md` |
| a-stock-data | `data-providers/a-stock-data.md` |
| AkShare | `data-providers/akshare.md` |
| Tushare | `data-providers/tushare.md` |
| Funda AI | `data-providers/funda-data.md` |
| OpenCLI | `data-providers/opencli-reader.md` |
| TradingView reader | `data-providers/tradingview-reader.md` |
| SEC EDGAR | `data-providers/sec-edgar.md` |
| HKEXnews | `data-providers/hkexnews.md` |
| CNINFO | `data-providers/cninfo.md` |
| China policy sources | `data-providers/china-policy-sources.md` |
| EIA | `data-providers/eia.md` |
| IEA / OPEC / JODI Oil | `data-providers/iea-opec-jodi.md` |
| CME / ICE futures | `data-providers/cme-ice-futures.md` |
| CFTC COT | `data-providers/cftc-cot.md` |
| World Gold Council / LBMA | `data-providers/world-gold-council-lbma.md` |
| FRED / Treasury macro | `data-providers/fred-treasury-macro.md` |
| arXiv / Semantic Scholar | `data-providers/semantic-scholar-arxiv.md` |
| Google Patents / Lens | `data-providers/google-patents-lens.md` |

## Canonical tool table

### OpenCLI

| Field | Value |
|---|---|
| Use for | Dynamic websites, logged-in pages, social feeds, Eastmoney/Xueqiu/Reddit/X, generic source extraction. |
| Canonical source | `https://github.com/jackwener/opencli` |
| Package / connector | `@jackwener/opencli` |
| Setup Mode | Local install; Browser login session for many adapters. |
| Typical install command | `npm install -g @jackwener/opencli` |
| Verify | `opencli doctor` and `opencli list -f json` |
| Output preference | `-f json` or `-f yaml` |
| Guardrail | Read-only. Never post, like, follow, comment, save, subscribe, delete, trade, or edit account data. |
| Evidence tier | Underlying source tier, not OpenCLI. |

Before use:

1. Check whether OpenCLI exists.
2. Check adapter list and strategy.
3. If Browser Bridge or login is needed, ask the user to log in.
4. Never guess command names; inspect `opencli list -f json` or `opencli <site> --help`.

### TradingView reader via OpenCLI plugin

| Field | Value |
|---|---|
| Use for | TradingView quotes, options chain, expiries, greeks/IV, screeners, news, watchlists, chart state, screenshots. |
| Canonical source | `https://github.com/himself65/finance-skills/tree/main/opencli-plugins/tradingview` |
| Plugin metadata source | `https://github.com/himself65/finance-skills/blob/main/opencli-plugin.json` |
| Package / connector | OpenCLI plugin `tradingview` from finance-skills. |
| Setup Mode | Local install; Browser/desktop app login session; paid data entitlement may be required. |
| Typical install command | `opencli plugin install github:himself65/finance-skills/tradingview` |
| Verify | `opencli tradingview status` |
| Launch check | `opencli tradingview launch` only after user saves layouts and approves. |
| Output preference | `-f json`, `-f csv`, or limited Markdown tables. |
| Guardrail | Read-only. Do not place trades, create/delete alerts, edit watchlists, or change layouts. |
| Evidence tier | Usually Tier 3 numeric baseline; TradingView news Tier 4; user chart state is context only. |

### yfinance

| Field | Value |
|---|---|
| Use for | US/global quotes, historical data, financial statements, dividends, options, analyst data, ownership baseline. |
| Canonical source | `https://github.com/ranaroussi/yfinance` |
| Package | `yfinance` |
| PyPI | `https://pypi.org/project/yfinance/` |
| Setup Mode | Local install. |
| Typical install command | `python3 -m pip install -U yfinance` |
| Verify | `python3 -c "import yfinance as yf; print(yf.__version__)"` |
| Guardrail | Numeric baseline only; reconcile key company facts to filings. |
| Evidence tier | Tier 3 aggregator / data provider. |

### a-stock-data

| Field | Value |
|---|---|
| Use for | A-share quotes, K-lines, valuation baseline, reports, concept blocks, fund flows, Dragon Tiger List, lock-up expiry, financial statements, CNINFO announcements. |
| Canonical source | `https://github.com/simonlin1212/a-stock-data` |
| External skill file | `https://raw.githubusercontent.com/simonlin1212/a-stock-data/main/SKILL.md` |
| Runtime packages documented by upstream | `mootdx`, `requests`, `pandas`, `stockstats` |
| Setup Mode | Local install; API key only for iwencai semantic report search. |
| Typical package install command | `python3 -m pip install -U mootdx requests pandas stockstats` |
| Verify | Import packages and run only a small read-only sample after user approval. |
| Guardrail | Do not vendor the external SKILL.md into this repo; preserve original CNINFO/exchange source URLs for key Facts. |
| Evidence tier | Underlying source tier; wrapper itself is not primary proof. |

### AkShare

| Field | Value |
|---|---|
| Use for | China market, A-share, macro, industry, commodity, and public-data exploration. |
| Canonical source | `https://github.com/akfamily/akshare` |
| Documentation | `https://akshare.akfamily.xyz` |
| Package | `akshare` |
| PyPI | `https://pypi.org/project/akshare/` |
| Setup Mode | Local install. |
| Typical install command | `python3 -m pip install -U akshare` |
| Verify | `python3 -c "import akshare as ak; print(ak.__version__)"` |
| Guardrail | Record underlying upstream source where possible; reconcile key facts to official sources. |
| Evidence tier | Tier 3 aggregator. |

### Tushare

| Field | Value |
|---|---|
| Use for | Structured China equity financial data, market data, corporate actions, index data, and some macro/industry datasets. |
| Canonical source | `https://github.com/waditu/tushare` |
| Official site | `https://tushare.pro` |
| Package | `tushare` |
| PyPI | `https://pypi.org/project/tushare/` |
| Setup Mode | Local install; API key/token. |
| Typical install command | `python3 -m pip install -U tushare` |
| Verify | `python3 -c "import tushare as ts; print(ts.__version__)"` |
| User action | Provide token or configure token. |
| Guardrail | Respect token limits; reconcile key facts to filings/disclosures. |
| Evidence tier | Tier 3 data provider. |

### Commodity / macro commodity official sources

| Source | Use for | Setup Mode | User action | Guardrail |
|---|---|---|---|---|
| EIA | US oil/gas inventories, production, refinery runs, STEO | Built-in / Manual fallback / API key | API key only for API calls | Preserve table/series, period, units. |
| IEA | Global oil balances and energy datasets | Paid terminal / subscription / Manual fallback | Subscription may be required | Do not treat forecasts as Facts. |
| OPEC MOMR | OPEC supply/demand outlook and production context | Built-in / Manual fallback | none by default | Check incentives and definitions. |
| JODI Oil | Country-level oil production/trade/refinery data | Built-in / Manual fallback | none by default | Data can lag and be revised. |
| CME / ICE | Commodity futures contracts, curve, spreads | Manual fallback / Paid terminal / subscription | Paid data may be required | Record contract month, timestamp, delayed/settlement status. |
| CFTC COT | Futures positioning and crowding | Built-in / Manual fallback | none by default | Positioning is market-structure evidence, not price direction proof. |
| World Gold Council | Gold ETF flows, central-bank reserves, demand/supply | Manual fallback / Web login | Login may be needed for downloads | Preserve dataset methodology and units. |
| LBMA | Precious-metals benchmark context | Manual fallback / Paid terminal / subscription | Licensed access may be needed for historical data | Record benchmark/date/license caveat. |
| FRED / US Treasury | Real yields, nominal yields, inflation expectations, macro data | Built-in / Manual fallback / API key | FRED API key only for API calls | Record series id, frequency, units. |

### Funda AI

| Field | Value |
|---|---|
| Use for | Paid research synthesis and raw structured financial/filings/options/supply-chain/news/alternative data. |
| Canonical source | `https://funda.ai` |
| MCP endpoint documented by finance-skills | `https://funda.ai/api/mcp` |
| REST base documented by finance-skills | `https://api.funda.ai/v1` |
| Setup Mode | Paid subscription; API key; OAuth/web login for MCP. |
| Typical key env | `FUNDA_API_KEY` |
| Verify | Check key/session presence; do not call paid endpoints without user approval. |
| Guardrail | Provider synthesis is not primary proof. Trace key claims to original filings/transcripts/sources. |
| Evidence tier | Underlying source tier; synthesis is research assistance. |

### Adanos Finance sentiment

| Field | Value |
|---|---|
| Use for | Structured sentiment across Reddit, X, news, and Polymarket. |
| Canonical docs from finance-skills | `https://api.adanos.org/docs` |
| Setup Mode | API key. |
| Typical key env | `ADANOS_API_KEY` |
| Verify | Check key presence only; call endpoint after user approval. |
| Guardrail | Sentiment is market-structure/narrative evidence, not fundamental proof. |
| Evidence tier | Tier 5 for social-derived signals; Tier 4 for news-derived signals. |

### Playwright

| Field | Value |
|---|---|
| Use for | Browser automation when static fetch fails and OpenCLI is not the right tool. |
| Canonical source | `https://playwright.dev` |
| Node package | `playwright` |
| Python package | `playwright` |
| Setup Mode | Local install; browser install may be needed. |
| Typical Node install command | `npm install -D playwright` or project-specific install after approval. |
| Typical Python install command | `python3 -m pip install -U playwright` plus browser install after approval. |
| Verify | Check package import or `npx playwright --version`. |
| Guardrail | Do not bypass access controls; preserve screenshots/URLs/timestamps. |
| Evidence tier | Underlying source tier. |

### arXiv

| Field | Value |
|---|---|
| Use for | Technical papers and preprints. |
| Canonical source | `https://arxiv.org` |
| API docs | `https://info.arxiv.org/help/api/index.html` |
| Optional package | `arxiv` from PyPI. |
| Setup Mode | Built-in/manual fallback; local install optional. |
| Typical install command | `python3 -m pip install -U arxiv` |
| Verify | Manual URL search or package import. |
| Guardrail | Preprints are technical basis, not company revenue evidence. |
| Evidence tier | Tier 3. |

### Semantic Scholar

| Field | Value |
|---|---|
| Use for | Paper discovery, citation graph, technical literature mapping. |
| Canonical source | `https://www.semanticscholar.org` |
| API docs | `https://api.semanticscholar.org` |
| Setup Mode | Built-in/manual fallback; API key optional. |
| Verify | Manual URL search or API availability. |
| Guardrail | Metadata can be incomplete; cite paper DOI/arXiv/venue when possible. |
| Evidence tier | Tier 3. |

### Google Patents / The Lens

| Field | Value |
|---|---|
| Use for | Patent discovery, patent family, assignee activity, technical route. |
| Google Patents source | `https://patents.google.com` |
| Lens source | `https://www.lens.org` |
| Setup Mode | Manual fallback; web login optional for Lens. |
| Verify | Open patent URL / publication number. |
| Guardrail | Patents show R&D activity, not commercial traction. |
| Evidence tier | Tier 3 for databases; Tier 1 when using official patent office records. |

### Official filing/disclosure sources

| Market | Canonical source | Use for | Setup Mode |
|---|---|---|---|
| US | `https://www.sec.gov/edgar/search/` | SEC filings | Built-in/manual fallback. |
| HK | `https://www.hkexnews.hk` | HK announcements and reports | Built-in/manual fallback. |
| A-share | `https://www.cninfo.com.cn` | A-share announcements and reports | Built-in/manual fallback. |
| SSE | `https://www.sse.com.cn` | Shanghai exchange disclosures | Built-in/manual fallback. |
| SZSE | `https://www.szse.cn` | Shenzhen exchange disclosures | Built-in/manual fallback. |
| BSE China | `https://www.bse.cn` | Beijing exchange disclosures | Built-in/manual fallback. |

These are preferred over aggregators for key Facts.

## Detection snippets

Use these only after the user approves command execution or when read-only environment checks are already permitted.

```bash
command -v opencli && opencli doctor
```

```bash
python3 - <<'PY'
mods = ['yfinance', 'akshare', 'tushare', 'mootdx', 'requests', 'pandas', 'stockstats']
for m in mods:
    try:
        mod = __import__(m)
        print(m, 'OK', getattr(mod, '__version__', 'unknown'))
    except Exception as e:
        print(m, 'MISSING', e.__class__.__name__)
PY
```

```bash
printf 'FUNDA_API_KEY=%s\n' "${FUNDA_API_KEY:+SET}"
printf 'ADANOS_API_KEY=%s\n' "${ADANOS_API_KEY:+SET}"
```

## Source acquisition fallback ladder

1. Official source manual URL.
2. Built-in web/fetch/PDF extraction.
3. Source-specific optional tool from this catalog.
4. OpenCLI / browser automation for dynamic or logged-in pages.
5. Paid provider if user has access.
6. Mark blocked/missing and stop at hard source gate.
