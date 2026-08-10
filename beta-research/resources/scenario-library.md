# Scenario Library

Scenarios are conditional experiments, not forecasts. Select only scenarios material to the asset or portfolio.

## Historical replay

Choose event windows with auditable dates and explain why the comparison is relevant.

Possible families:

- rapid equity drawdown;
- inflation and rate shock;
- growth/recession scare;
- credit/liquidity seizure;
- volatility spike;
- commodity supply shock;
- currency dislocation;
- regional policy or geopolitical event.

Do not assume today's market structure, holdings, duration, leverage, or policy response matches history.

## Hypothetical factor shocks

Define each variable numerically and state horizon/sign convention.

| Factor | Example unit | Key nonlinearities |
|---|---|---|
| Equity market | percentage return | volatility and correlation rise |
| Rates | basis points by tenor | duration, convexity, curve shape |
| Credit | spread basis points | default, liquidity, recovery |
| FX | percentage move by pair | translation and transaction exposure |
| Commodity | percentage move | basis, curve, operating leverage |
| Volatility | volatility points | option convexity and skew |
| Liquidity | spread/volume/funding change | forced selling and price gaps |

Examples are units, not default shock sizes. Choose magnitudes from user goals, historical distributions, or an explicitly documented severe-but-plausible assumption.

## Combined scenarios

Avoid internally inconsistent shock bundles. State the causal narrative only after defining variables.

Example structure:

```text
Scenario name:
Horizon:
Trigger:
Equity shock:
Rate-curve shock:
Credit-spread shock:
FX/commodity shock:
Volatility/liquidity assumption:
Correlation assumption:
Transmission method:
```

## Reverse stress

Start from a user-defined risk threshold, then solve or search for combinations of market/factor shocks that breach it.

Report multiple plausible combinations instead of implying one exact path.

## Required caveats

- Linear beta may understate nonlinear losses.
- Historical covariance often breaks during stress.
- Stale or illiquid assets can show delayed losses.
- Leverage, margin, redemptions, and path dependency can dominate first-order estimates.
- Scenario aggregation must avoid double counting correlated shocks.
