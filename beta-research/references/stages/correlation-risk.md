# Stage: Correlation Risk

## Purpose

Find concentration and shared drivers that position labels or asset counts may hide.

## Inputs

- Aligned asset or sleeve return series.
- Portfolio weights when portfolio concentration is requested.
- Sector, geography, currency, duration, credit, commodity, or style classifications when available.

## Process

1. Validate common dates and remove series with misleadingly sparse overlap.
2. Calculate full-period and recent rolling correlations.
3. Compare normal and stressed windows when enough observations exist.
4. Identify clusters and common drivers; do not treat ticker count as diversification.
5. Calculate weight concentration and effective number of positions when weights exist.
6. Attribute concentration by issuer, sector, geography, currency, duration, and factor as material.
7. Highlight unstable correlations and pairs that converge during stress.
8. Distinguish correlation from causality and from direct economic exposure.

Useful diagnostics:

- weighted top positions and sleeves;
- Herfindahl concentration and effective position count;
- average pairwise correlation;
- rolling correlation range;
- cluster membership;
- common benchmark/factor sensitivity;
- residual or idiosyncratic share where available.

## Output

Produce `correlation-risk.md`:

1. Data window and coverage.
2. Weight concentration.
3. Correlation matrix or compact heatmap.
4. Correlation clusters.
5. Hidden common drivers.
6. Stress-correlation observations.
7. Apparent diversification that may fail.
8. Data Gaps and limitations.
9. Stage Result.

## Gate

PARTIAL when only holdings labels are available without return histories. Describe structural overlap, but do not present estimated correlations.
