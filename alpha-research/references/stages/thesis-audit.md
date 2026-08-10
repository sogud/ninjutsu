# Stage: Thesis Audit

## Purpose

`Thesis Audit` 是证据审计 + 反方审查。

它合并两个动作：

1. **Evidence Audit**：防止把“推断”当成“事实”，把“故事”当成“证据”。
2. **Bear-case review**：从反方视角攻击 thesis，找出最脆弱的地方。

它可以判断候选公司推荐逻辑是否站得住。
它不输出直接交易指令、目标价、仓位建议或收益承诺。

## Bundled files

- Template: `templates/thesis-audit.md`.
- Resources:
  - `resources/source-quality.md`.
  - `resources/bear-case-checklist.md`.

Use the template for output.
Use `source-quality.md` when judging claim strength.
Use `bear-case-checklist.md` to ensure the bear case is complete.

## Inputs

最好包含：

- `Clarify` 的 Research Brief。
- `Source Map` 的 Source Registry、Source Gate Decision、Starter Evidence Pack。
- `Chain Trace` 的产业链、卡点、候选公司映射。

如果缺少关键输入，必须明确标记缺口。

## Source gate awareness

If `Source Map` marked Source Gate as FAIL, `Thesis Audit` may still audit existing claims, but it must not recommend continuing to final report synthesis. Its next recommendation should be source acquisition and rerunning `Source Map`.

## Claim taxonomy

每个关键判断必须归类为：

- **Fact**: 由一手资料或可靠资料直接支持。
- **Inference**: 基于事实做出的合理推断。
- **Assumption**: thesis 成立所需，但尚未被证实的条件。
- **Rumor**: 社交媒体、论坛、小作文、弱来源信息。

## Citation requirement

Every Fact and key numeric baseline must reference a Source Registry citation id such as `[S1]`.

Rules:

- A claim without a URL/stable locator cannot be Strong.
- A wrapper or aggregator output cannot be Strong unless the original source URL/locator is preserved.
- Web-search snippets are discovery, not final evidence.
- If a source is not previewable or auditable, mark the claim Medium at best and explain why.
- For technical terms, add a plain-language note when the claim uses specialist vocabulary.

## Evidence strength

使用四档：

- **Strong**: 一手来源直接支持。
- **Medium**: 多个可靠来源间接支持。
- **Weak**: 只有间接、模糊或单一弱来源。
- **Unknown**: 当前没有足够证据。

## Required bear-case attacks

必须检查：

1. Technical substitution: 技术路线是否可能被替代？
2. Supply expansion: 供应是否会快速扩张，导致瓶颈消失？
3. Customer internalization: 大客户是否可能自研或内制？
4. Pricing pressure: 价格战是否会吃掉利润？
5. Valuation pull-forward: 当前估值是否已经提前反映未来增长？
6. Liquidity risk: 成交额、价差、换手、期权流动性是否支撑研究对象的可投资性讨论？
7. Correlation / sympathy risk: 它是否只是跟随同主题、同指数、同供应链篮子上涨？
8. Estimate revision risk: 分析师预期是否已经上修过度，或存在下修触发点？
9. Crowding risk: 是否已有明显跟风盘、拥挤持仓或期权/社媒放大？
10. Narrative risk: 叙事是否大于事实？
11. Customer concentration: 客户集中是否过高？
12. Financial fragility: 资产负债表、现金流或稀释风险是否明显？
13. Execution risk: 扩产、认证、良率、交付是否可能失败？
14. Geopolitical risk: 出口管制、关税、制裁、供应链迁移是否会改变逻辑？
15. Commodity risk if relevant: 供需、库存、期限结构、持仓、宏观驱动是否支持商品逻辑？

## Market-structure checks

When relevant, check:

- Liquidity: average daily value traded, bid/ask spread, turnover, float, lock-up expiry, and options liquidity.
- Correlation: realized correlation to sector peers, index, theme basket, customer/supplier basket, or high-beta growth basket.
- Estimate revisions: EPS/revenue estimate trend, revision breadth, consensus range, and whether the thesis depends on already-raised expectations.
- Crowding: fund flow, hot-stock tags, social amplification, Dragon Tiger List / unusual options activity where market-specific data is available.
- Commodity positioning: CFTC COT, ETF flows, futures open interest, curve shape, and inventory data where commodity-linked.

These are risk signals, not trading instructions. Do not output entry points, stop-losses, position sizing, target prices, or buy/sell commands.

## Anti-hype mode

如果 research mode 是 anti-hype，重点攻击：

- 原始叙事来源。
- 社媒扩散路径。
- 弱证据被升级的问题。
- 估值和拥挤交易。
- 叙事反身性。
- “沾边公司”被包装成“瓶颈公司”的风险。

## Process

1. Extract important claims from prior artifacts.
2. Link each claim to Source Registry citation ids.
3. Classify claims as Fact / Inference / Assumption / Rumor.
4. Audit citations and source quality.
5. Identify evidence gaps and glossary terms.
6. Attack the thesis from the bear side.
7. Write concrete kill criteria.
8. Judge whether candidate/company recommendations are sufficiently supported.

## Output

Use `templates/thesis-audit.md` and produce:

```markdown
# Thesis Audit: {Topic}

## 1. Thesis Under Review

## 2. Core Claims

## 3. Evidence Audit

## 4. Citation Audit

## 5. Evidence Gaps

## 6. What Would Confirm the Thesis?

## 7. What Would Weaken the Thesis?

## 8. Strongest Bear Case

## 9. Risk Attack Matrix

## 10. Market-Structure Checks

## 11. Narrative vs Reality

## 12. Kill Criteria

## 13. Candidate Recommendation Audit

## 14. Glossary Candidates

## 15. Audit Grades

## 16. Stage Result
```

## Stage Result

Use short format:

```markdown
## Stage Result

- Recommended next stage:
- Why:
- Handoff input:
  - Topic:
  - Research object:
  - Market scope:
  - Key unknowns:
- Stop / continue recommendation:
```

Default next stage: `Report Quality` only when Source Gate is PASS.

If Source Gate is FAIL, default next step is `Source Map` plus `alpha-research` internal source resources for missing sources.

## Guardrails

- Do not invent sources.
- Do not upgrade a claim without evidence.
- Do not mark claims Strong if they lack citation ids with previewable URLs or stable locators.
- Do not treat customer speculation as confirmed customer relationship.
- Do not treat market reaction as fundamental proof.
- Do not soften risk to please the user.
- Do not assume a popular thesis is true.
- Do not recommend a candidate/company unless evidence, logic, risks, counterarguments, and failure criteria are explicit.
- If no source is available, say: “Evidence not yet sufficient.”
