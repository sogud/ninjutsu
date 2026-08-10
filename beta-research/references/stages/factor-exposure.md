# Stage: Factor Exposure

## Purpose

Estimate how an asset, strategy, or portfolio has moved with its benchmark and documented risk factors.

Read `resources/data-contract.md` and `resources/beta-methods.md` before calculation.

## Inputs

- Adjusted total-return series for the research object and benchmark.
- Portfolio holdings/weights or portfolio return series when in portfolio mode.
- Factor return series only when definitions and dates are auditable.
- Frequency, lookback, rolling window, base currency, and risk-free treatment.

## Process

1. Validate timestamps, currency, corporate actions, missing values, stale observations, and sample length.
2. Convert prices to aligned returns; never regress unmatched price levels.
3. Estimate market beta, alpha/intercept, fit, uncertainty, and sample size.
4. Estimate rolling beta to test stability.
5. Add sector/style/macro factors only when multicollinearity and data coverage are acceptable.
6. Compare full-period, recent-period, upside, and downside behavior when sample size supports it.
7. For portfolios, reconcile weights and compare holdings-based exposure with realized portfolio-return exposure when both exist.
8. Investigate unstable signs, implausible coefficients, low fit, and sensitivity to benchmark choice.

## Required diagnostics

- Benchmark and rationale.
- Number of observations.
- Beta estimate and confidence interval or standard error.
- R² and residual volatility.
- Rolling range and latest rolling value.
- Factor definitions and source.
- Sensitivity to lookback/frequency where material.

Do not interpret a statistically weak coefficient as a stable economic exposure.

## Output

Produce `factor-exposure.md`:

1. Data and method card.
2. Market beta table.
3. Rolling beta findings.
4. Multifactor exposure table, if valid.
5. Holdings-based versus realized exposure, if applicable.
6. Stability and uncertainty.
7. Economic interpretation.
8. Data and model limitations.
9. Stage Result.

## Gate

FAIL when benchmark or return alignment is invalid, sample history is insufficient for the requested estimate, or factor provenance is unknown.
