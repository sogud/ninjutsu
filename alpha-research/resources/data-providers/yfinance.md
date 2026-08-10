# yfinance Playbook

## Best for

Quick numeric baseline for US/global securities:

- current price, market cap, shares, beta, volume;
- historical OHLCV and return history;
- basic financial statements and ratios;
- dividends/splits;
- options expiries/chains;
- analyst estimates, recommendations, and ownership fields when available.

Use yfinance as a baseline provider, not as final audited proof.

## Canonical install source

Use `../tool-install-sources.md` before setup.

| Field | Value |
|---|---|
| Canonical source | `https://github.com/ranaroussi/yfinance` |
| PyPI | `https://pypi.org/project/yfinance/` |
| Package | `yfinance` |
| Setup Mode | Local install |
| Verify | `python3 -c "import yfinance as yf; print(yf.__version__)"` |

Run install/verification commands only after user approval for the current environment.

## Detection flow

1. Check package availability.
2. If missing, ask user whether to install from the canonical source.
3. If installed, run a tiny read-only smoke check on a known ticker only if user allows execution.
4. If smoke check fails or Yahoo data is incomplete, use fallback provider.

Suggested status labels:

| Status | Meaning |
|---|---|
| `YFINANCE_READY` | import works and basic ticker fetch works. |
| `YFINANCE_INSTALLED_UNTESTED` | import works but no data call yet. |
| `YFINANCE_MISSING` | package unavailable. |
| `YFINANCE_FETCH_FAIL` | package exists but data unavailable/rate-limited. |

## Source Tier

Tier 3: recognized data provider / exchange data aggregator.

Classify individual claims by data type:

| Data type | Evidence role | Use limit |
|---|---|---|
| Price / volume / market cap | Numeric baseline | Good for baseline; record timestamp/date. |
| Financial statements | Numeric baseline | Reconcile key numbers to filings. |
| Options chain | Market-structure context | Not a trade recommendation. |
| Analyst estimates / recommendations | Consensus clue | Not primary evidence. |
| News | Event clue | Verify with original publisher/company. |

## Structured acquisition recipe

For a company baseline, collect only what the research needs:

| Need | yfinance object / field family | Required provenance |
|---|---|---|
| Current price / market cap | `Ticker.info`, `fast_info` | ticker, exchange, field, access date/time. |
| 3–5 year price/volume | `Ticker.history()` / download | ticker, period, interval, adjusted/unadjusted. |
| Financial statements | income, balance, cash flow | statement type, period, field names, units. |
| Options context | `options`, `option_chain(date)` | expiry, strike range, bid/ask/mid, IV/greeks if present. |
| Estimates | estimate/recommendation fields | provider field names, period, analyst count if present. |

Prefer concise tables over raw dumps.

## Required provenance

Record:

- Source title: `Yahoo Finance via yfinance`.
- Ticker and exchange/suffix.
- Query date/time and timezone if intraday/current.
- Period/date range and interval.
- Field names and units.
- yfinance version if known.
- Original Yahoo Finance URL if available.
- Whether the value was reconciled to filings.

## What it can support

- Quick financial baseline.
- Initial peer comparisons.
- Liquidity and market-structure risk checks.
- Options context when data exists.
- Estimate-revision / consensus clues when fields are populated.

## What it cannot support

- Final audited company facts without filings.
- Complete A-share/HK coverage.
- Customer relationships, product claims, technical feasibility, or segment purity.
- Professional real-time quote accuracy.
- Trade signals, target prices, or position sizing.

## Source Gate rules

Hard gate fails if:

- public-company ranking uses yfinance numbers without date/field provenance;
- company financial Facts are not reconciled to official filings when material;
- yfinance is the only source for product/customer/technical claims;
- options/price data is used as fundamental proof.

## Fallbacks

- Company filings for final financials.
- SEC/HKEX/CNINFO/exchange pages.
- Funda / TradingView / Polygon / Tiingo / Alpha Vantage / paid terminal if user has access.
- Manual Yahoo Finance page with URL and timestamp.
