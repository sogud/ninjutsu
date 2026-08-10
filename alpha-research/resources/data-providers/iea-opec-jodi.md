# IEA / OPEC / JODI Oil Playbook

## Best for

Global oil balance research: demand, non-OPEC supply, OPEC supply, inventories, trade, refinery throughput, and cross-country oil database checks.

Use for:

- global supply/demand balances;
- OPEC+ production and policy context;
- demand revisions;
- non-OPEC supply developments;
- OECD/commercial inventory context;
- country-level production, imports, exports, refinery intake, and product flows.

## Canonical sources

| Source | URL | Use |
|---|---|---|
| IEA data and statistics | `https://www.iea.org/data-and-statistics` | IEA datasets, some paid/subscription. |
| IEA Oil Market Report | `https://www.iea.org/reports/oil-market-report` | Monthly oil balance and revisions; often subscription. |
| OPEC Monthly Oil Market Report | `https://www.opec.org/monthly-oil-market-report.html` | OPEC official monthly oil market report. |
| OPEC digital MOMR | `https://publications.opec.org/momr` | Digital Monthly Oil Market Report. |
| JODI Oil | `https://www.jodidata.org/oil/` | Joint Organisations Data Initiative oil database. |
| JODI data downloads | `https://www.jodidata.org/oil/database/data-downloads.aspx` | CSV/Beyond 20/20 downloads. |

## Setup Mode

- Manual fallback / web/PDF fetch for OPEC and public pages.
- Paid terminal / subscription for some IEA datasets and reports.
- Manual CSV download for JODI.

Ask before using paid/subscription access.

## Source Tier

| Source | Tier | Notes |
|---|---:|---|
| IEA | 3 / 4 | Recognized international agency; methodology and access caveats matter. |
| OPEC | 3 / 4 | Official producer-group view; check incentives and secondary-source definitions. |
| JODI | 3 | Multi-country official submissions; data can be lagged/revised. |

## Structured acquisition recipe

1. Define balance question.
   - Demand growth, supply growth, inventory draw/build, spare capacity, compliance, trade flow.
2. Pull at least one global balance source.
   - IEA or OPEC for global narrative and table.
   - JODI for country-level corroboration when relevant.
3. Record definitions.
   - Liquids vs crude, OPEC crude vs NGLs, OECD vs global, monthly vs annual, direct communication vs secondary sources.
4. Compare revisions.
   - For oil theses, revision direction often matters as much as level.
5. Cross-check incentives.
   - OPEC statements and reports are useful but not neutral proof of future discipline.
6. Feed Source Registry.
   - Preserve PDF page/table or database filters.

## Required provenance

- Publication/database name.
- Month/period and release date.
- Table/page/section or filter path.
- Units: mb/d, kb/d, barrels, days of demand, etc.
- Definition: crude / liquids / products / OECD / non-OECD.
- URL/stable locator.
- Access/subscription caveat if applicable.

## What it can support

- Oil supply/demand balance context.
- Demand/supply revision analysis.
- OPEC+ supply and spare-capacity context.
- Country-level production/trade/refinery data via JODI.

## What it cannot support

- Real-time tanker tracking unless paired with a shipping provider.
- Futures curve or positioning without CME/ICE/CFTC.
- Company-level recommendations without filings/IR and financial baseline.
- Direct trading calls or price targets.

## Source Gate rules

Hard gate fails if:

- oil balance conclusions lack EIA/IEA/OPEC/JODI or equivalent recognized data;
- OPEC policy narrative is treated as supply Fact without production/compliance data;
- JODI values lack country/product/flow/period definitions;
- oil-linked company recommendation lacks company primary sources.

## Fallbacks

- EIA WPSR/STEO for US and global context.
- Energy Institute Statistical Review for historical annual context.
- National energy ministries/regulators.
- Paid shipping data if user has access.
