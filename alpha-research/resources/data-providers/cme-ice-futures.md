# CME / ICE Futures Curve Playbook

## Best for

Commodity futures market structure:

- WTI crude, gasoline, heating oil, natural gas, gold, copper, grains, and other CME/NYMEX/COMEX products;
- Brent and other ICE contracts;
- futures curve shape, spreads, contango/backwardation, roll-yield context;
- settlement/quote references for price-driven commodity research.

## Canonical sources

| Source | URL | Use |
|---|---|---|
| CME Group markets | `https://www.cmegroup.com/markets/` | Futures product pages and delayed quotes. |
| CME WTI crude | `https://www.cmegroup.com/markets/energy/wti-crude-oil-futures.html` | WTI contract/product source. |
| CME crude quotes | `https://www.cmegroup.com/markets/energy/crude-oil/light-sweet-crude.quotes.html` | WTI quote/contract chain page. |
| CME gold futures | `https://www.cmegroup.com/markets/metals/precious/gold.html` | COMEX gold contract source. |
| ICE Brent data | `https://www.ice.com/products/219/Brent-Crude-Futures/data` | ICE Brent futures data page. |
| ICE products | `https://www.ice.com/products` | ICE product discovery. |

## Setup Mode

- Manual fallback / web fetch for product pages and delayed quotes.
- Paid terminal / subscription for professional real-time/historical data.
- TradingView/OpenCLI may be used as transport if original exchange/product details are preserved.

Ask before using logged-in, paid, or local tool access.

## Source Tier

Tier 1 / 3 depending on access path:

- exchange product pages and official settlement/contract specs: Tier 1 / 3;
- market-data vendors: Tier 3;
- charts/screenshots: visual context only unless source details are preserved.

## Structured acquisition recipe

1. Identify benchmark and exchange.
   - Example: WTI CL on NYMEX/CME, Brent on ICE, Gold GC on COMEX/CME.
2. Record contract metadata.
   - Contract code, delivery month, currency, unit, settlement/quote date, delayed/real-time status.
3. Build curve table.
   - Front month plus relevant forward months.
   - Spreads: M1-M2, M1-M6, M1-M12 where relevant.
4. Interpret curve carefully.
   - Backwardation can indicate tightness but is not standalone proof.
   - Contango can reflect storage/financing/seasonality, not only weak demand.
5. Connect to physical data.
   - Pair curve with EIA/IEA/OPEC/JODI/WGC/LBMA/inventory data.
6. Preserve provenance.
   - URL, timestamp, quote/settlement status, data delay, source/tool used.

## Required provenance

- Exchange and product name.
- Contract code and month.
- Quote/settlement date and timestamp/timezone.
- Currency and unit.
- Delayed/real-time/settlement caveat.
- URL or stable locator.
- Data source path if using vendor/TradingView.

## What it can support

- Futures curve and spread Facts.
- Contango/backwardation observation.
- Market-structure risk and roll-yield context.
- Price benchmark baseline.

## What it cannot support

- Physical supply/demand conclusions by itself.
- Company earnings exposure by itself.
- Crowding/positioning without CFTC/open interest/flow data.
- Direct trading signals or price targets.

## Source Gate rules

Hard gate fails if:

- curve claims lack contract/month/date/source provenance;
- curve shape is used as sole proof of physical tightness;
- company recommendation is based only on commodity futures prices;
- chart-only output lacks stable source details.

## Fallbacks

- TradingView reader for read-only curve extraction when source provenance is preserved.
- Paid terminals if user has access.
- Exchange settlement reports/manual pages.
- CFTC COT for positioning.
