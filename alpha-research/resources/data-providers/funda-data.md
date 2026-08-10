# Funda Data Playbook

## Best for

Optional paid data and synthesis for US/global equity research when the user has Funda AI access.

Use it for:

- raw quotes, financial statements, options chains, ownership, calendars, and macro series;
- SEC filings, transcripts, investment research reports, news, and event timelines;
- supply-chain graph leads, sector deep-dives, earnings previews/recaps, and valuation context;
- alternative data leads such as social sentiment, congressional trades, ownership flow, and AI hiring signals.

Project / service: `https://funda.ai`.

## Canonical install / access source

Use `../tool-install-sources.md` before setup.

| Field | Value |
|---|---|
| Canonical source | `https://funda.ai` |
| MCP endpoint pattern | `https://funda.ai/api/mcp` |
| REST base pattern | `https://api.funda.ai/v1` |
| Setup Mode | Paid subscription; API key; OAuth/web login for MCP |
| Key env | `FUNDA_API_KEY` for REST-style access |
| Verify | Check key/session presence; call endpoints only after approval |

## Optional runtime execution policy

This repository does not vendor Funda code or require Funda dependencies.

During an actual research run, an agent may check availability, configure a connector, or run a local setup command only if the user explicitly confirms:

- the account/subscription exists;
- the API key or login action is provided by the user;
- the user approves any local command or dependency installation;
- the command is read-only and does not place trades or modify accounts.

If access is unavailable, mark the channel `Blocked by access / paid source` or `Missing`, then use fallbacks.

## Detection flow

1. Ask whether the user has Funda access.
2. Check `FUNDA_API_KEY` only if user approves environment checks.
3. Check MCP/OAuth connection only if the runtime supports it and user approves.
4. Choose surface:
   - raw structured data → REST-style provider path;
   - synthesis / sector framing / transcript summary → MCP-style provider path;
   - key Fact proof → original filing/transcript/company source, not synthesis.
5. If access is missing, do not call paid endpoints; use fallback sources.

Suggested status labels:

| Status | Meaning |
|---|---|
| `FUNDA_REST_READY` | API key available and raw data calls permitted. |
| `FUNDA_MCP_READY` | MCP/OAuth surface connected and permitted. |
| `FUNDA_ACCESS_UNKNOWN` | user has not confirmed access. |
| `FUNDA_KEY_MISSING` | key absent. |
| `FUNDA_SUBSCRIPTION_BLOCKED` | paid access unavailable. |

## Source Tier

Tier depends on the Funda surface and underlying data:

| Surface / underlying data | Tier | Evidence role |
|---|---:|---|
| SEC filing retrieved through Funda | 1 if original SEC filing provenance is preserved | Strong Fact. |
| Company transcript or company-hosted material | 2 / 3 | Management commentary or company context. |
| Structured financials, quotes, options, ownership, macro | 3 | Numeric baseline or corroboration. |
| Funda synthesis / agent answer | 3 / 4 | Research synthesis, not primary evidence. |
| Social sentiment / alternative data | 5 / 3 depending on source | Narrative clue or corroboration. |

Never cite a Funda synthesis as the only proof for a key Fact. Trace important claims back to original filings, transcripts, official data, or company sources.

## Structured acquisition recipe

### Raw data path

Use when the downstream artifact needs rows/numbers.

| Need | Data family | Provenance required |
|---|---|---|
| Quotes / intraday / EOD | market data | ticker, exchange, timestamp, endpoint, fields, units. |
| Financial statements / metrics | fundamentals | statement type, period, field names, units, reconciliation status. |
| Options chain / greeks | options | expiry, strike, type, bid/ask/mid, IV/greeks, timestamp. |
| Filings / transcripts | filings/transcripts | original filing/transcript URL, date, section/speaker. |
| News / event timeline | news/events | original publisher URL, timestamp, headline/body excerpt. |
| Supply-chain graph | supply-chain | relationship type, source path, confidence, original support if available. |
| Alternative data | ownership/social/government trading/hiring | dataset, window, definitions, source caveats. |

### Synthesis path

Use when the user needs a quick research assistant pass.

1. Ask a tightly scoped question with ticker/topic, horizon, and assumptions.
2. Treat response as source leads and analyst synthesis.
3. Extract claims.
4. For every key Fact, find original filing/transcript/company/news source.
5. Push claims to Thesis Audit.

## What it can support

- Faster Alpha Research workflow when paid access exists.
- Financial baseline, options/ownership/macro context, and event discovery.
- Transcript and filing discovery for Source Registry.
- Supply-chain relationship leads for `Chain Trace` stage.
- Estimate, sentiment, and ownership-change context for `Thesis Audit` stage.

## What it cannot support

- Final primary-source evidence unless original source provenance is preserved.
- Trade execution, direct buy/sell calls, target prices, or position sizing.
- A Strong Fact from a synthesized answer alone.
- Access when user lacks subscription, API key, or OAuth permission.

## Required provenance

Record:

- Funda surface used: synthesis / MCP-style answer / REST-style raw data.
- Original underlying source when available.
- Ticker, company, market, period/date range.
- Endpoint/dataset or conversation locator if available.
- Access date.
- Field names and units for numeric values.
- Original filing/transcript/news URL or locator for key Facts.
- Whether the claim is direct source data or Funda synthesis.

## Source Gate rules

Hard gate fails if:

- Funda synthesis is cited as Strong Fact without original source;
- paid access is unavailable and no substitute exists for material data;
- endpoint/dataset/date/field provenance is missing for key numeric values;
- alternative/social data is used as fundamental proof.

## Fallbacks

- SEC EDGAR, company IR, exchange pages, and transcript providers.
- yfinance for basic US/global numeric baseline.
- TradingView reader for chart, quote, screener, and options context.
- Manual filings and news search.
- Paid terminals such as Bloomberg, FactSet, Refinitiv, Koyfin, or TIKR when user has access.
