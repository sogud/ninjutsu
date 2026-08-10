# AkShare Playbook

## Best for

China market and macro data exploration: A-share market data, indices, funds, macro series, industry data, commodities, and many public Chinese data endpoints.

## Setup Mode

- Local install.

## Source Tier

Tier 3: Recognized data provider / aggregator.

## What it can support

- Quick data access for A-share and China market baselines.
- Macro and industry series discovery.
- Screening and exploratory charts.
- Cross-checking public datasets before going to official sources.

## What it cannot support

- Final audited company facts without filings.
- Stable long-term API contracts.
- Evidence provenance unless original upstream source is recorded.
- Social or qualitative claims.

## Query / navigation patterns

- Identify the underlying AkShare function and its upstream source.
- Record the original source if AkShare wraps another public dataset.
- Use for quick exploration, then reconcile key claims to official filings, exchanges, ministries, or statistics sources.

## Required provenance

Record dataset/function name, original upstream source if known, period/date range, access date, and fields used.

## Fallbacks

- Tushare for structured China financial data.
- Official exchanges, 巨潮资讯, 国家统计局, 海关总署, ministries, and association sources.
