# HKEXnews Playbook

## Best for

Hong Kong-listed company primary disclosures: announcements, annual reports, interim reports, prospectuses, circulars, transactions, placements, connected transactions, and listing documents.

## Setup Mode

- Built-in when the agent has web/fetch access.
- Manual fallback through HKEXnews search.
- Browser automation if search pages or PDFs are difficult to fetch directly.

## Source Tier

Tier 1: Official primary source.

## What it can support

- HK-listed company filings and announcements.
- Reported financials and segment data.
- Listing history and prospectus disclosures.
- Corporate actions and major transactions.
- Official risk factors and management discussion.

## What it cannot support

- Undisclosed customer or supplier relationships.
- Mainland policy facts unless the announcement quotes official policy.
- Market rumors or retail narrative.

## Query / navigation patterns

- Search by stock code and date range.
- For company research, collect latest annual report, latest interim report, and recent announcements.
- For IPO research, collect prospectus and post-listing updates.
- For corporate events, inspect announcement categories and circulars.

## Required provenance

Preserve stock code, company name, announcement title, publication date, document URL, section/page, and quoted excerpt.

## Fallbacks

- Company IR page.
- AnnualReports-style archives only as discovery, not final proof.
- Financial data provider, reconciled back to HKEX documents.
