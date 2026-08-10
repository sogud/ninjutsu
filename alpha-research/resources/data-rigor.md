# Data Rigor Rules

Use this resource whenever a report uses company financials, market data, valuation, ranking, liquidity, or peer comparison.

The purpose is to prevent AI-looking reports with numbers that are plausible but not audit-ready.

## Core principle

Do not let the model “think through” numbers in prose.

For every important numeric claim, capture:

- exact value;
- unit;
- currency;
- period/date/time;
- source id;
- original source URL or stable locator;
- whether the value is reported, adjusted, estimated, or calculated.

## Minimum company data pack

Company reports should collect as much of this as possible before final synthesis:

| Data item | Why it matters | Preferred source |
|---|---|---|
| Revenue and segment revenue | Proves actual business exposure. | Filing / annual report / earnings release |
| Gross margin and operating margin | Shows pricing power and cost pressure. | Filing / earnings release |
| GAAP vs non-GAAP reconciliation | Prevents mixing profit definitions. | Earnings release / filing reconciliation table |
| Operating cash flow and free cash flow | Checks whether earnings become cash. | Cash-flow statement |
| Cash, debt, net cash / net debt | Shows balance-sheet flexibility. | Balance sheet / filing |
| Share count | Needed for market cap, per-share metrics, dilution. | Filing / exchange / data provider |
| Market cap and liquidity | Shows expectation level and tradability. | Exchange / recognized data provider |
| Valuation multiples | Helps test whether the story is already priced. | Provider + manual calculation when possible |
| Guidance, backlog, orders, or bookings | Forward demand clue. | Company guidance / filing / transcript |
| Customer concentration | Dependency and bargaining risk. | Filing / prospectus / annual report |
| Peer / comparable baseline | Required for relative valuation or priority claims. | Same-field data from comparable companies |

If a row is material but missing, label it `Evidence Gap` or `Data Gap` in the final report.

## Two-source rule

For key financial and market values, prefer two independent sources.

Examples:

| Value | Source 1 | Source 2 |
|---|---|---|
| Revenue / segment revenue | Filing | Earnings release / annual report table |
| Market cap | Exchange or provider | Manual price × shares check |
| Cash / debt | Filing | Annual report / provider with filing provenance |
| Valuation multiple | Provider | Manual calculation from price, shares, earnings |
| Peer metric | Same provider for all peers | Filings or official reports for spot checks |

If only one source is available, do not hide it. Mark `single-source` and cap confidence.

## Manual arithmetic checks

When the report uses valuation or market-size math, write the formula in the working artifact or final appendix.

Minimum checks:

```text
market cap = share price × diluted shares outstanding
enterprise value = market cap + total debt + preferred / minority interest - cash and equivalents
free cash flow = operating cash flow - capital expenditure
FCF yield = free cash flow / market cap
forward PE = market cap / forward net income, or share price / forward EPS
PS = market cap / revenue
net debt = total debt - cash and equivalents
```

Rules:

- Never mix millions, billions, 亿, and 万亿 without stating unit.
- Never mix USD, HKD, CNY, JPY, or EUR without stating currency.
- Never compare calendar-year data to fiscal-year data without explaining period mismatch.
- Never compare GAAP margin to non-GAAP margin as if they are the same.
- If a provider value conflicts with filing data, filing wins unless there is a clear restatement or timing reason.

## Difference thresholds

Use these as report-quality heuristics:

| Difference between sources | Treatment |
|---:|---|
| ≤1% | Treat as consistent, record both sources. |
| 1–5% | Use primary source; mention provider difference if the value is important. |
| >5% | Stop and reconcile before using the number as a key Fact. |
| Different accounting definitions | Do not average. Explain GAAP / non-GAAP / adjusted / continuing operations difference. |

## Peer baseline rules

If a report discusses relative attractiveness, valuation, ranking, or “better candidate,” it must include a peer/comparable baseline or state why no clean peer exists.

Peer table should explain:

- why each peer is comparable;
- why it may not be comparable;
- revenue growth;
- margin;
- valuation multiple;
- liquidity or market cap;
- source date.

Do not compare a company to a peer only because they share a theme tag.

## Final report requirements

The final `report.html` should show:

- data pack table;
- source date / access date for market data;
- formula notes for calculated values when important;
- data gaps;
- peer baseline when relative valuation or priority is discussed;
- positive and negative research views using the same data.

## Quality ceiling

- Missing financial baseline for company valuation or ranking: max grade C.
- Missing peer baseline while discussing relative attractiveness: max grade B.
- Key numeric values from a single non-primary source: max grade B for that section.
- Unreconciled >5% data conflict: block strong conclusion using that number.
