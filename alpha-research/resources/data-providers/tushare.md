# Tushare Playbook

## Best for

Structured China equity and financial datasets: A-share fundamentals, daily market data, financial statements, index data, corporate actions, and some macro/industry datasets.

## Setup Mode

- Local install.
- API key.

## Source Tier

Tier 3: Recognized data provider / aggregator.

## What it can support

- A-share screening and structured financial baselines.
- Time-series analysis and cross-company comparisons.
- Share, index, and market data workflows.

## What it cannot support

- Final primary evidence without reconciliation.
- Complete qualitative disclosure context.
- Customer or supply-chain claims.
- Social narrative.

## Query / navigation patterns

- Use ticker/code and reporting period precisely.
- Pull latest period plus historical trend when possible.
- Reconcile important line items to annual/quarterly reports from 巨潮资讯 or exchange disclosures.

## Required provenance

Record ticker/code, endpoint/dataset name, period/date range, field definitions, access date, and whether the value was reconciled to filings.

## Fallbacks

- AkShare for exploratory public data.
- Official filings and exchanges for final numbers.
- Paid terminals if available.
