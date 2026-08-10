# Beta Research Data Contract

## Minimum inputs by mode

| Mode | Required | Optional |
|---|---|---|
| Market | Scope, analysis date, benchmark, regime indicators | Cross-asset and factor data |
| Asset | Adjusted asset and benchmark return history | Risk-free and factor returns |
| Portfolio | Holdings plus weights, or portfolio return history; benchmark | Holdings histories, factors, classifications |
| Stress | Exposure estimates or aligned histories; explicit shocks | Nonlinear pricing models |

## Return-series rules

- Prefer adjusted total-return data including splits and distributions.
- Record source, symbol/identifier, timezone, currency, frequency, start/end date, and access time.
- Align on common trading dates before covariance, regression, or correlation.
- Do not forward-fill returns across non-trading or stale-price periods without explicit justification.
- Explain missing-value treatment and dropped observations.
- Convert currency consistently or disclose that local-currency and investor-currency results differ.
- Use return series, not price levels, for beta and correlation.
- Flag survivorship, backfill, stale pricing, delisting, and benchmark-composition bias.

## Portfolio rules

- Weights must state the effective date and should reconcile to approximately 100%; explain cash, leverage, shorts, derivatives, and residuals.
- For derivatives, notional weight is not enough when delta, duration, convexity, or nonlinear exposure is material.
- Distinguish holdings-based exposure from realized return-based exposure.
- Never silently retrieve holdings from a brokerage account.

## Factor rules

For every factor, record:

- economic meaning;
- exact construction/provider;
- return type and currency;
- frequency and coverage;
- whether it is investable, academic, macro, or custom;
- known overlap with other factors.

Do not combine incompatible factor definitions as though they were the same series.

## Data-quality statuses

- **Ready:** sufficient, aligned, current, and documented.
- **Limited:** usable with explicit constraints.
- **Blocked:** missing core series, invalid alignment, unknown provenance, or incomparable definitions.
