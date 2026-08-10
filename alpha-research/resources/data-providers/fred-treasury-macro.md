# FRED / Treasury Macro Playbook

## Best for

Macro drivers behind commodities, especially gold and oil:

- nominal Treasury yields;
- TIPS real yields;
- breakeven inflation expectations;
- Fed funds and policy-rate context;
- dollar / broad dollar indexes where available;
- CPI/PCE/inflation and macro activity series;
- recession, industrial production, PMI-like macro context where relevant.

## Canonical sources

| Source | URL | Use |
|---|---|---|
| FRED | `https://fred.stlouisfed.org/` | St. Louis Fed economic data. |
| FRED API docs | `https://fred.stlouisfed.org/docs/api/fred/` | API documentation. |
| FRED API v2 | `https://fred.stlouisfed.org/docs/api/fred/v2/index.html` | Newer API documentation. |
| US Treasury rates | `https://home.treasury.gov/resource-center/data-chart-center/interest-rates` | Treasury yield curve and related official data. |
| Treasury FiscalData | `https://fiscaldata.treasury.gov/` | Treasury datasets and APIs. |
| Federal Reserve data | `https://www.federalreserve.gov/data.htm` | Fed official statistical releases. |

## Setup Mode

- Manual fallback / CSV download from FRED/Treasury pages.
- API key for FRED API.
- Built-in data fetch if runtime has web/PDF/table extraction.

Ask before checking API keys or running API calls.

## Source Tier

| Source | Tier | Notes |
|---|---:|---|
| US Treasury / Federal Reserve | 1 | Official government/central-bank source. |
| FRED | 3 / underlying source tier | Recognized data hub; cite original source when material. |

## Structured acquisition recipe

1. Define macro channel.
   - Gold: real yields, nominal yields, breakevens, dollar, Fed policy, inflation.
   - Oil: dollar, rates, growth/activity, inflation, recession demand risk.
2. Choose series.
   - Record series id/name, source, frequency, units, seasonality.
3. Pull time window.
   - Use enough history for regime context; avoid overfitting one-day moves.
4. Preserve transformations.
   - Level, change, real vs nominal, spread, moving average, percentile.
5. Link to commodity thesis.
   - Macro data supports driver context; it does not by itself prove commodity supply/demand.

## Required provenance

- Series id and series title.
- Source owner.
- Date range and frequency.
- Units and seasonal adjustment.
- Access/download date.
- URL or API route.
- Transformation applied, if any.

## What it can support

- Real-rate and inflation-expectation Facts.
- USD/rates macro context.
- Macro-growth context for demand-sensitive commodities.
- Cross-checks for commodity narrative claims.

## What it cannot support

- Physical commodity supply/demand by itself.
- Company exposure by itself.
- Futures curve or positioning without exchange/CFTC data.
- Direct trading signals or target prices.

## Source Gate rules

Hard gate fails if:

- gold thesis makes real-rate/USD/inflation claims without macro data;
- macro series lacks id/date/frequency/unit provenance;
- macro correlation is presented as causation without commodity-specific evidence;
- commodity-linked company recommendation lacks company primary sources.

## Fallbacks

- Federal Reserve statistical releases.
- US Treasury official rates pages.
- IMF, World Bank, OECD, national statistics offices for non-US macro.
- Paid terminals if user has access.
