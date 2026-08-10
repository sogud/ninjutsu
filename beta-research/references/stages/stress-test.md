# Stage: Stress Test

## Purpose

Estimate conditional sensitivity under historical and hypothetical shocks without presenting scenarios as forecasts.

Read `resources/scenario-library.md` before selecting shocks.

## Inputs

- Valid exposures or aligned return histories.
- Portfolio weights or portfolio return series when applicable.
- User-requested scenarios, horizon, and base currency.
- Market-regime context.

## Scenario types

1. **Historical replay:** use an auditable event window and actual market moves.
2. **Factor shock:** apply documented market, rate, credit, currency, commodity, or volatility shocks to estimated exposures.
3. **Custom narrative:** translate a user thesis into explicit variable shocks and transmission assumptions.
4. **Reverse stress:** ask what combination of shocks would breach a user-defined loss or risk threshold.

## Process

1. State the scenario purpose; do not maximize drama.
2. Define every shock, horizon, source, and sign convention.
3. Show the transmission method: historical replay, linear exposure, repricing model, or qualitative map.
4. Separate first-order estimates from nonlinear, liquidity, gap, and correlation effects.
5. Recalculate with stress correlations where evidence supports them.
6. Show contributions by asset, sleeve, and factor when holdings are available.
7. Include at least one scenario that challenges the prevailing regime interpretation.
8. State what the model cannot capture.

## Output

Produce `scenario-stress.md`:

1. Scenario definitions.
2. Shock table and sources.
3. Estimated portfolio/asset impact.
4. Contribution by exposure.
5. Correlation and liquidity assumptions.
6. Nonlinear and second-order risks.
7. Reverse-stress result when requested.
8. Monitoring indicators.
9. Limitations and Stage Result.

## Gate

FAIL when a scenario has no defined shocks or transmission method. Narrative labels alone are not stress tests.
