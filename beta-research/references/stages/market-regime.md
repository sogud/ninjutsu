# Stage: Market Regime

## Purpose

Describe the systematic environment without turning a noisy macro snapshot into a confident market forecast.

## Inputs

- Scope, benchmark, base currency, and analysis date.
- Growth, inflation, policy-rate, yield-curve, liquidity, credit, volatility, breadth, and cross-asset data as material.
- Source dates and publication lags.

## Process

1. **Timestamp the snapshot.** Separate market prices from lagged economic releases.
2. **Assess growth.** Use activity, earnings breadth, labor, credit, and revisions appropriate to the market.
3. **Assess inflation.** Separate headline, core, wages, and market-implied inflation where available.
4. **Assess policy and liquidity.** Record central-bank stance, real yields, financial conditions, currency, and funding stress.
5. **Assess risk appetite.** Check volatility, credit spreads, breadth, correlation, and defensive/cyclical leadership.
6. **Classify cautiously.** Use a plain-language regime label plus confidence and competing interpretations.

Suggested regime dimensions:

| Dimension | Possible state |
|---|---|
| Growth | accelerating / stable / slowing / contraction |
| Inflation | rising / stable / falling |
| Policy | easing / neutral / tightening |
| Liquidity | improving / mixed / deteriorating |
| Risk appetite | risk-on / mixed / risk-off |

Do not compress conflicting evidence into one label. A mixed regime is a valid result.

## Output

Produce `market-regime.md`:

1. Snapshot date and data cutoff.
2. Benchmark and scope.
3. Regime dashboard.
4. Supporting indicators with sources.
5. Conflicting indicators.
6. Likely systematic beneficiaries and vulnerabilities, expressed as exposures rather than trade calls.
7. Confidence and monitoring triggers.
8. Data Gaps.
9. Stage Result.

## Gate

PASS when the label is supported by multiple current indicators and publication lags are explicit.

PARTIAL when important channels are stale or unavailable. Lower confidence rather than filling gaps with narrative.
