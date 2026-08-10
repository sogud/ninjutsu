# TradingView Reader Playbook

## Best for

Read-only market data and chart-context extraction from TradingView when the user already has access.

Use it for:

- quotes, screeners, movers, watchlists, chart state, and screenshots;
- options chains, expiries, implied volatility, and greeks when available;
- TradingView news and symbol search;
- liquidity, correlation, crowding, and options-market context for `Thesis Audit` stage.

Reference pattern: finance-skills `tradingview-reader`, through an OpenCLI-style TradingView adapter.

## Canonical install source

Use `../tool-install-sources.md` before setup.

| Field | Value |
|---|---|
| Canonical source | `https://github.com/himself65/finance-skills/tree/main/opencli-plugins/tradingview` |
| Plugin metadata | `https://github.com/himself65/finance-skills/blob/main/opencli-plugin.json` |
| Connector | OpenCLI plugin `tradingview` |
| Setup Mode | Local install; desktop/browser login session; paid data entitlement may be required |
| Verify | `opencli tradingview status` |
| Output preference | `-f json`, `-f csv`, or limited markdown tables |

Run install, launch, status, or data commands only after user approval.

## Detection flow

1. Detect OpenCLI first.
2. Check whether TradingView plugin is installed.
3. Run status check if approved.
4. Confirm TradingView account/data entitlement if options/news/screener data is missing.
5. Use `launch` only after the user confirms unsaved layouts/drawings are safe.

Suggested status labels:

| Status | Meaning |
|---|---|
| `TV_READY` | plugin installed, session reachable, read commands available. |
| `TV_PLUGIN_MISSING` | OpenCLI exists but TradingView adapter missing. |
| `TV_LOGIN_NEEDED` | adapter exists but user must log in. |
| `TV_ENTITLEMENT_LIMIT` | account lacks data entitlement for requested data. |
| `TV_CDP_UNAVAILABLE` | local app/browser connection unavailable. |

## Read-only guardrails

Never:

- place trades;
- create, delete, or edit alerts;
- edit watchlists;
- change layouts or drawings;
- expose cookies or private session tokens;
- dump private watchlists unless the user explicitly asks.

Chart screenshots and watchlists are user context, not external evidence unless cited as such.

## Source Tier

| Data type | Tier | Evidence role |
|---|---:|---|
| Exchange/market data displayed through TradingView | 3 | Numeric baseline. |
| Options chain / greeks / IV | 3 | Numeric baseline / risk context. |
| TradingView news | 4 | Event clue. |
| User watchlists / chart state / alerts | User-provided context | Research input, not evidence. |
| Screenshots | Depends on underlying page | Visual record; preserve context. |

TradingView convenience does not make a claim primary. Use official filings, exchange data, company IR, or regulator sources for final Facts.

## Structured acquisition recipe

### Quote / market data

1. Confirm symbol and exchange.
2. Collect quote with timestamp, currency, exchange, and session state.
3. Record columns returned and data entitlement caveat.
4. Use as Numeric baseline only.

### Screener / movers

1. Define market, columns, filters, sort, and limit.
2. Use structured output.
3. Preserve query/filter in Source Registry.
4. Use to discover candidates, not to prove fundamentals.

### Options chain

1. List expiries first.
2. Select one or a few relevant expiries.
3. Limit strikes around spot unless the user asks for full chain.
4. Record expiry, strike, type, bid, ask, mid, IV, greeks, timestamp.
5. Use for options-market/crowding/liquidity context only.

### Chart state / screenshot

1. Record ticker, exchange, interval, indicators, timestamp.
2. Use screenshot as visual context.
3. Do not infer fundamentals from chart patterns.

## Required provenance

Record:

- TradingView source / adapter used.
- Symbol, exchange, asset type, and currency.
- Timestamp and timezone.
- Query/filter/columns.
- Data entitlement caveat if relevant.
- Screenshot file path or stable locator if used.
- Original news URL when using TradingView news.
- Whether command was read-only.

## What it can support

- Liquidity and market-structure checks: volume, spread proxies, options liquidity, IV skew, screener context.
- Correlation/crowding clues through watchlists, sector screeners, movers, and chart state.
- Anti-hype checks when a ticker is moving with a crowded basket or theme.
- Visual context for a chart-driven claim.

## What it cannot support

- Company fundamentals by itself.
- Technical feasibility, customer relationships, revenue exposure, or supply-chain chokepoints.
- Final valuation conclusions.
- Trading actions or strategy execution.
- Any Strong Fact without source reconciliation.

## Source Gate rules

Hard gate fails if:

- TradingView chart/price/options data is used as fundamental proof;
- symbol/exchange/timestamp are missing;
- private chart/watchlist context is presented as external evidence;
- data entitlement is unclear for a key numeric claim.

## Fallbacks

- yfinance for basic quotes and history.
- Official exchange data pages.
- Broker or paid terminal if the user has access.
- Funda / Polygon / Tiingo / Alpha Vantage for structured market data.
- Manual TradingView screenshot provided by the user.
