---
name: beta-research
description: Research systematic market risk and portfolio exposure through one entry point. Use when the user asks what beta means for an asset or portfolio, wants a market-regime assessment, benchmark sensitivity, rolling beta, factor exposure, correlation or concentration analysis, scenario stress testing, hidden common-risk detection, portfolio risk audit, or a resumable Beta Research HTML report.
---

# Beta Research

## Purpose

`beta-research` 研究资产或组合暴露于什么系统性风险，以及这些风险在不同市场环境下可能如何表现。

它不是另一个选股 Skill。它不寻找公司层面的 Alpha，不输出买卖指令、目标价、仓位调整或自动对冲交易。

用户只调用这一个入口。市场状态、因子暴露、相关性、压力测试和组合审计是内部阶段，按需加载。

## Internal stages

| Stage | Read when needed | Primary output |
|---|---|---|
| Market Regime | `references/stages/market-regime.md` | `market-regime.md` |
| Factor Exposure | `references/stages/factor-exposure.md` | `factor-exposure.md` |
| Correlation Risk | `references/stages/correlation-risk.md` | `correlation-risk.md` |
| Stress Test | `references/stages/stress-test.md` | `scenario-stress.md` |
| Portfolio Audit | `references/stages/portfolio-audit.md` | `portfolio-audit.md`, `beta-report.html` |

Load only the current stage and the resources it needs.

## Modes

| Mode | Use when | Required stages |
|---|---|---|
| `market` | No portfolio is supplied; user wants broad systematic conditions | Market Regime, then report summary |
| `asset` | User asks about one asset, fund, strategy, or benchmark-relative return series | Regime, Factor Exposure, Stress Test, Audit |
| `portfolio` | Holdings/weights or a portfolio return series are supplied | All stages |
| `factor` | User wants beta or factor decomposition only | Factor Exposure plus data checks |
| `stress` | User wants named historical or hypothetical scenarios | Stress Test plus relevant exposures |
| `resume` | Prior Beta Research artifacts exist | Continue from first incomplete or stale stage |
| `report` | Valid prior artifacts exist and final HTML is requested | Recheck Beta Gate, then Portfolio Audit |

Infer the mode from the request and available data. Do not ask the user to select a mode when it is clear.

## Defaults

| Parameter | Default |
|---|---|
| Mode | `market` without holdings/returns; otherwise infer |
| Language | Chinese |
| Return frequency | Daily adjusted total return |
| Main lookback | 3 years or maximum reliable history if shorter |
| Rolling window | 252 trading days |
| Confidence level | 95% |
| Benchmark | User-specified; otherwise a declared broad benchmark appropriate to scope |
| Base currency | User-specified; otherwise infer and disclose |
| Factor model | Market beta first; add documented factors only when reliable factor data exists |
| Final format | Single-file `beta-report.html` |
| Trading actions | Disabled |

Defaults are analytical starting points, not universal truths. Change them when the asset, frequency, market history, or user goal makes them inappropriate, and record the reason.

## Step 1: Detect data and runtime

Before analysis:

1. Detect available market-data, macro-data, filing/fund documentation, browser, spreadsheet, and Python/statistical capabilities.
2. Check data authentication and reachability without exposing credentials.
3. Prefer adjusted total-return series with timestamps and original-source provenance.
4. Ask for approval before installing packages, using paid/private sessions, or accessing brokerage/account data.
5. Never infer permission to read holdings from a general research request.

Use:

- `resources/data-contract.md` for minimum input and alignment rules.
- `resources/beta-methods.md` for formulas, diagnostics, and interpretation.
- `resources/scenario-library.md` for historical and hypothetical stress design.

## Step 2: Establish scope

Create or update `beta-brief.md` from `templates/beta-brief.md`.

Confirm or infer:

- research object: market, asset, strategy, or portfolio;
- benchmark and why it is appropriate;
- base currency;
- date range and frequency;
- holdings/weights or portfolio return series, if applicable;
- requested factors and scenarios;
- whether the goal is diagnosis, monitoring, or report generation.

Do not request holdings for market-only analysis. For portfolio mode, accept user-provided holdings/weights or a portfolio return series; do not access an account unless explicitly authorized.

## Step 3: Resolve artifacts and resume

Use the user's path first, then the host Project's artifact/report conventions, then:

```text
beta-research-output/{scope-slug}/
```

Artifact contract:

```text
run-log.md
beta-brief.md
market-regime.md
factor-exposure.md
correlation-risk.md
scenario-stress.md
portfolio-audit.md
beta-report.html
```

Resume from the first condition that applies:

1. Scope, benchmark, currency, or period is unclear → update Beta Brief.
2. Regime evidence is missing or stale → Market Regime.
3. Exposure estimates are missing, stale, or use invalid data → Factor Exposure.
4. Portfolio dependencies are missing → Correlation Risk.
5. Requested scenarios are missing or exposures changed → Stress Test.
6. Final audit/report is missing or older than inputs → Portfolio Audit.

A file is complete only when its data timestamp, method, assumptions, and limitations are explicit.

## Step 4: Enforce the Beta Gate

Set **PASS**, **PARTIAL**, or **FAIL** before polished synthesis.

PASS requires, as applicable:

- benchmark, currency, frequency, and period are declared;
- adjusted return series are aligned on common dates;
- missing values, corporate actions, stale prices, and short histories are handled explicitly;
- portfolio weights reconcile or a portfolio return series is supplied;
- every factor has a definition, source, frequency, and coverage period;
- beta estimates include sample size, uncertainty, fit, and stability diagnostics;
- scenario shocks and transmission assumptions are documented;
- source timestamps and known Data Gaps are visible.

PARTIAL means the available analysis is useful but one or more non-critical components are missing. Limit conclusions and label the report accordingly.

FAIL means core inputs are absent or incomparable. Stop before polished `beta-report.html`; provide an exact Data Acquisition Plan instead.

## Step 5: Execute stages

Default portfolio order:

```text
Market Regime → Factor Exposure → Correlation Risk → Stress Test → Portfolio Audit
```

After each stage:

- save its artifact;
- update `run-log.md` with data timestamps, methods, decisions, and gaps;
- continue internally when allowed;
- stop for missing core data, required permission, invalid comparability, or completed requested mode.

Do not tell the user to invoke another Skill.

## Step 6: Produce the final report

When Beta Gate is PASS or explicitly limited PARTIAL:

1. Explain the benchmark and data window.
2. State the current market regime with supporting indicators and uncertainty.
3. Show static and rolling beta/factor exposures with diagnostics.
4. Show correlation clusters, concentration, and hidden common drivers.
5. Show historical and hypothetical scenario results with assumptions.
6. Separate observed data, model estimates, assumptions, and unavailable inputs.
7. Identify dominant risks, diversification limits, monitoring indicators, and invalidation conditions.
8. Produce `beta-report.html` from `templates/beta-report.html`.

The report may identify risk-reduction questions for further research. It must not prescribe or execute trades.

## Guardrails

- Beta is benchmark-, period-, frequency-, and method-dependent.
- Historical beta is not a forecast or a complete risk measure.
- Correlation is state-dependent and often rises during stress.
- Low measured beta does not imply low liquidity, credit, volatility, concentration, or tail risk.
- Factor labels do not prove causality.
- Scenario results are conditional estimates, not loss guarantees.
- Distinguish Observed Data, Estimate, Assumption, and Data Gap.
- Do not access brokerage accounts, positions, or orders without explicit authorization.
- Confirm again before any account-changing or trading action; this Skill itself performs none.
- Include methodology, limitations, source dates, and a research-only disclaimer.
