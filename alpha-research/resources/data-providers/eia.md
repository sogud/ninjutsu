# EIA Playbook

## Best for

Official US energy data used in oil, gas, refined products, inventories, production, refinery utilization, SPR, imports/exports, and short-term energy forecasts.

Use for:

- crude oil and product inventories;
- refinery runs / utilization;
- crude production and imports/exports;
- implied product demand;
- Strategic Petroleum Reserve (SPR);
- Weekly Petroleum Status Report (WPSR);
- Short-Term Energy Outlook (STEO);
- natural gas storage and production where relevant.

## Canonical sources

| Source | URL | Use |
|---|---|---|
| EIA open data | `https://www.eia.gov/opendata/` | API and browsable datasets. |
| EIA API documentation | `https://www.eia.gov/opendata/documentation.php` | API usage and parameters. |
| Weekly Petroleum Status Report | `https://www.eia.gov/petroleum/supply/weekly/` | Weekly inventory/supply/refinery tables. |
| Short-Term Energy Outlook | `https://www.eia.gov/outlooks/steo/` | Forecasts and supply/demand outlook. |
| Natural Gas Storage | `https://www.eia.gov/naturalgas/storage/` | Gas inventory context. |

## Setup Mode

- Built-in / manual fallback for web/PDF/CSV/XLS pages.
- API key for API access.

Ask before checking API keys or running API calls.

## Source Tier

Tier 1: official government statistics.

Claims still depend on the table/series used. Do not cite a broad EIA page if the claim relies on a specific table.

## Structured acquisition recipe

1. Identify commodity and driver.
   - Crude, gasoline, distillate, jet fuel, natural gas, SPR, refinery runs, production.
2. Choose publication.
   - WPSR for weekly US oil inventory/supply changes.
   - STEO for forecast/balance outlook.
   - API series for repeatable time series.
3. Preserve table/series provenance.
   - Publication, table, series id if known, period, units, release date, URL.
4. Convert units carefully.
   - barrels, thousand barrels, million barrels per day, Bcf, dollars/barrel.
5. Separate data from interpretation.
   - EIA table is Fact; market implication is Inference.

## Required provenance

- EIA publication name.
- Table number/name or API route/series id.
- Period and release date.
- Units.
- Access date.
- URL or stable locator.
- Extracted value and whether seasonally adjusted.

## What it can support

- US oil and gas inventory/supply/demand Facts.
- Refinery utilization and product-demand evidence.
- US production and import/export trends.
- Forecast baseline from STEO.

## What it cannot support

- Non-US physical balances by itself.
- OPEC+ compliance by itself.
- Company economics without filings/IR.
- Direct trading signals or price targets.

## Source Gate rules

Hard gate fails if:

- oil/gas supply-demand claims lack EIA, IEA, OPEC, JODI, or another official/recognized data source;
- EIA numbers lack table/series/date/unit provenance;
- weekly noise is treated as long-term thesis without multi-period context.

## Fallbacks

- IEA, OPEC, JODI for global balances.
- CME/ICE for curve and price structure.
- CFTC COT for positioning.
- Company filings/IR for company exposure.
