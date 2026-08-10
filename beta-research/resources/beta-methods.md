# Beta and Exposure Methods

## Market beta

For aligned excess returns:

\[
r_{i,t}-r_{f,t}=\alpha_i+\beta_i(r_{m,t}-r_{f,t})+\epsilon_t
\]

Equivalent covariance estimate:

\[
\beta_i=\frac{\operatorname{Cov}(r_i,r_m)}{\operatorname{Var}(r_m)}
\]

Always report benchmark, period, frequency, observations, uncertainty, R², and residual volatility.

## Multifactor model

\[
r_t-r_{f,t}=\alpha+\sum_{k=1}^{K}\beta_k f_{k,t}+\epsilon_t
\]

Use only factors with documented construction and adequate common history. Diagnose multicollinearity and unstable coefficients. A factor loading is statistical exposure, not proof of economic causality.

## Portfolio aggregation

First-order holdings-based exposure:

\[
\beta_p \approx \sum_i w_i\beta_i
\]

This approximation may fail with derivatives, leverage, changing weights, nonlinear payoffs, stale pricing, or omitted factors. Compare with realized portfolio-return regression when available.

## Rolling estimates

Use rolling windows to test stability. State:

- window length;
- minimum observations;
- rebalance/weight assumptions;
- latest value, median, range, and structural breaks.

Do not overinterpret short windows with noisy estimates.

## Upside and downside beta

Estimate conditional beta only with enough observations and a clearly defined condition, such as benchmark returns above or below zero. Report reduced sample size and selection effects.

## Correlation and concentration

Pairwise correlation:

\[
\rho_{ij}=\frac{\operatorname{Cov}(r_i,r_j)}{\sigma_i\sigma_j}
\]

Weight concentration:

\[
HHI=\sum_i w_i^2, \qquad N_{effective}=\frac{1}{HHI}
\]

For long/short or leveraged portfolios, disclose whether weights use net, gross, or absolute exposure.

## Scenario approximation

First-order factor shock:

\[
\Delta P/P \approx \sum_k \beta_k\Delta f_k
\]

This is a local linear approximation. Explicitly discuss convexity, optionality, basis risk, correlation shifts, liquidity gaps, and path dependency.

## Diagnostics checklist

- Benchmark sensitivity.
- Lookback and frequency sensitivity.
- Confidence interval or standard error.
- R² and residual distribution.
- Autocorrelation and heteroskedasticity caveat where material.
- Outlier/event sensitivity.
- Coefficient sign and economic plausibility.
- Structural breaks and regime dependence.
- Out-of-sample or holdout comparison when enough history exists.

## Interpretation limits

- High beta means high benchmark sensitivity, not necessarily high total risk.
- Low beta can coexist with severe liquidity, credit, concentration, or tail risk.
- Beta can change quickly after business-model, leverage, index, duration, or regime changes.
- Alpha/intercept from a regression is not automatically skill or investable excess return.
