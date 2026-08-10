# World Gold Council / LBMA Playbook

## Best for

Gold market research:

- gold ETF holdings and flows;
- central-bank gold reserves and buying;
- gold demand/supply categories;
- LBMA gold/silver/platinum/palladium benchmark context;
- London precious-metals market structure;
- gold narrative checks around real rates, dollar, central banks, and safe-haven demand.

## Canonical sources

| Source | URL | Use |
|---|---|---|
| World Gold Council data hub | `https://www.gold.org/goldhub/data` | Gold demand, supply, price, ETF, central bank datasets. |
| WGC ETF holdings and flows | `https://www.gold.org/goldhub/data/gold-etfs-holdings-and-flows` | Physically-backed gold ETF holdings/flows. |
| WGC central bank reserves | `https://www.gold.org/goldhub/data/gold-reserves-by-country` | Country-level gold reserves, compiled from IMF IFS statistics. |
| LBMA precious metal prices | `https://www.lbma.org.uk/prices-and-data/precious-metal-prices` | Gold/silver/platinum/palladium benchmark context. |
| LBMA gold price | `https://www.lbma.org.uk/prices-and-data/lbma-gold-price` | LBMA Gold Price description and benchmark administration. |
| Shanghai Gold Exchange | `https://www.sge.com.cn/` | China gold benchmark/premium/physical-market context when relevant. |

## Setup Mode

- Manual fallback / web/PDF/CSV download.
- Web login may be required for some WGC downloads.
- Paid/licensed access may be required for some LBMA historical data.

Ask before using logged-in or licensed data.

## Source Tier

| Source | Tier | Notes |
|---|---:|---|
| WGC datasets | 3 / 4 | Recognized industry data; check methodology and download limitations. |
| LBMA benchmark pages | 1 / 3 | Benchmark/market data context; licensing constraints may apply. |
| SGE | 1 / 3 | China exchange/benchmark context. |
| IMF/central bank source behind reserves | 1 / 3 | Prefer original official source when available. |

## Structured acquisition recipe

1. Define gold thesis driver.
   - Real rates, USD, ETF flows, central-bank buying, jewelry demand, mine supply, safe-haven demand, China premium.
2. Select data source.
   - WGC for ETF/central-bank/demand-supply.
   - LBMA/CME/SGE for benchmark/price structure.
   - FRED/Treasury for macro-rate drivers.
   - CFTC COT for futures positioning.
3. Preserve methodology.
   - WGC category definitions, tonnes vs USD, monthly/quarterly frequency, revisions.
4. Separate flow and price.
   - ETF/central-bank flows can explain demand context; they do not mechanically prove future price direction.
5. If recommending companies.
   - Add miner/royalty/ETF filings, production, reserves, costs, hedging, financial baseline.

## Required provenance

- Dataset/report name.
- Date/period and frequency.
- Units: tonnes, USD, local currency, ounces.
- Methodology/category definition where relevant.
- URL/stable locator.
- Access date.
- Login/license caveat if applicable.

## What it can support

- Gold ETF flow Facts.
- Central-bank reserve/buying context.
- Demand/supply category context.
- LBMA benchmark description and price-source context.
- China gold-market premium context if SGE data is used.

## What it cannot support

- Real-rate/FX macro claims without FRED/Treasury/FX data.
- Futures crowding without CFTC/open-interest data.
- Miner economics without company filings/IR.
- Direct trading signals, target prices, or position sizing.

## Source Gate rules

Hard gate fails if:

- gold thesis lacks benchmark/flow/macro source appropriate to the claim;
- ETF or central-bank claims lack WGC/IMF/official provenance;
- gold-company recommendation lacks company primary sources;
- price-only chart narrative is treated as fundamental proof.

## Fallbacks

- FRED/Treasury for macro drivers.
- CFTC COT for futures positioning.
- CME gold futures for futures curve/benchmark.
- IMF IFS / central bank official pages for reserve data.
- Company filings/IR for miner/royalty/ETF exposure.
