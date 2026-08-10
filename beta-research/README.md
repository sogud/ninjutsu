# Beta Research

单入口系统性风险研究 Skill。

```text
/beta-research
```

它研究市场状态、基准敏感度、滚动 Beta、因子暴露、相关性、集中度和情景压力。支持市场、单资产和用户提供持仓/收益序列的组合分析。

内部流程：

```text
Market Regime → Factor Exposure → Correlation Risk → Stress Test → Portfolio Audit
```

阶段文档位于 `references/stages/`，方法和数据契约位于 `resources/`，最终模板位于 `templates/`。内部阶段不是独立 Skill。

Beta Research 只提供研究诊断，不读取未授权账户，不执行交易，不输出目标价、仓位调整或收益承诺。
