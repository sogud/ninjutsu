# CFTC COT Playbook

## Best for

Commitments of Traders (COT) positioning and crowding analysis in US-regulated futures markets.

Use for:

- gold and silver futures positioning;
- crude oil and natural gas positioning;
- agriculture and metals futures positioning;
- managed money / non-commercial net length;
- producer/merchant hedging context;
- open interest and crowded-narrative checks.

## Canonical sources

| Source | URL | Use |
|---|---|---|
| CFTC COT main page | `https://www.cftc.gov/MarketReports/CommitmentsofTraders/index.htm` | Official COT report entry. |
| CFTC Public Reporting | `https://publicreporting.cftc.gov/` | Public reporting interface and API help. |
| CFTC Public Reporting Help | `https://publicreporting.cftc.gov/stories/s/Public-Reporting-FAQ/inwp-fmhz/` | FAQ/API guidance. |
| Historical compressed COT | `https://www.cftc.gov/MarketReports/CommitmentsofTraders/HistoricalCompressed/index.htm` | Download historical COT files. |
| Disaggregated Combined Data Hub | `https://publicreportinghub.cftc.gov/Commitments-of-Traders/Disaggregated-Combined/kh3c-gbw2/about_data` | Disaggregated dataset metadata. |

## Setup Mode

- Manual fallback / CSV download.
- API/data hub access if supported by the runtime.
- No local install required by default.

## Source Tier

Tier 1: official regulator data.

Positioning interpretation remains an inference. COT does not predict price direction by itself.

## Structured acquisition recipe

1. Choose report type.
   - Legacy, Disaggregated, Traders in Financial Futures, or Supplemental.
2. Map contract.
   - Commodity, exchange, contract market name, CFTC market code when available.
3. Select reporting date.
   - COT is weekly and lagged; record report date and release date if available.
4. Extract position categories.
   - Managed money, producer/merchant, swap dealer, non-commercial, commercial depending on report type.
5. Normalize if useful.
   - Net position, gross long/short, percent of open interest, percentile vs historical range.
6. Interpret carefully.
   - Crowding risk, squeeze risk, unwind risk, hedging pressure.
   - Not a standalone buy/sell signal.

## Required provenance

- CFTC report type.
- Contract market name / commodity / exchange.
- Report date.
- Category definitions used.
- Long, short, spread, net position, open interest if cited.
- URL or file locator.
- Download/access date.

## What it can support

- Positioning/crowding Facts.
- Speculative vs hedging context.
- Market-structure risk in gold, oil, gas, metals, and agriculture.
- Anti-hype checks when narrative is crowded.

## What it cannot support

- Physical supply/demand balance.
- Company fundamentals.
- Price targets or direct trading signals.
- Current intraday positioning.

## Source Gate rules

Hard gate fails if:

- crowding/positioning claims lack CFTC or equivalent data;
- COT report type/date/contract are missing;
- positioning is presented as direct evidence of commodity fundamentals;
- lag and category caveats are omitted.

## Fallbacks

- Exchange open interest and volume.
- ETF holdings/flows for gold.
- Paid terminal positioning dashboards if user has access.
- TradingView/open-source charting only as visual context with provenance.
