# SEC EDGAR Playbook

## Best for

US-listed company primary disclosures: 10-K, 10-Q, 8-K, S-1, F-1, 20-F, 6-K, proxy statements, ownership forms, risk factors, segment discussion, and audited financials.

## Setup Mode

- Built-in when the agent has web/fetch access.
- Manual fallback through the SEC EDGAR website.
- API key only if using a third-party filings API.

## Source Tier

Tier 1: Official primary source.

## What it can support

- Reported revenue, margins, cash flow, share count, debt, dilution, and risk factors.
- Management's formal business description.
- Filed customer concentration if disclosed.
- Material events from 8-K filings.
- IPO history and shareholder structure from registration statements.

## What it cannot support

- Undisclosed customer relationships.
- Real-time order status.
- Current social narrative.
- Technical feasibility beyond what the company discloses.

## Query / navigation patterns

- Company name or ticker → CIK → latest annual and quarterly filings.
- For company research, collect latest annual report plus latest quarterly/interim filing.
- For event-driven research, inspect recent 8-K or 6-K filings.
- For IPO or newly listed companies, inspect S-1/F-1 and amendments.

## Required provenance

For key facts, preserve filing type, filing date, reporting period, accession number or stable URL, section/table/page locator, and quoted excerpt.

## Fallbacks

- Company IR filing archive.
- Exchange or regulator mirrors.
- Recognized filings data provider, reconciled to official SEC filing.
