# Stage: Chain Trace

## Purpose

沿着真实物理系统和供应链,从下游需求一路追到上游瓶颈点。

核心问题:

> 如果这个趋势继续兑现,最容易卡住、最难替代、供应最窄的环节在哪里?

它不输出交易指令。可以指出值得进一步验证的候选公司或环节,但必须标记证据强弱。
它只输出 chokepoint 候选和研究优先级。

## Bundled files

- Templates: none.
- Resource: `resources/chokepoint-scorecard.md`.

Use the scorecard resource when ranking chokepoint candidates.

## Inputs

最好已有:

- `Clarify` 产出的 Research Brief。
- `Source Map` 产出的 Source Plan 和 Starter Evidence Pack。

最低输入可以只有一个主题,但证据不足时必须标记缺口。

## Step 1: Trend reality check

判断趋势是否真实:

- 需求来自哪里?
- 是真实需求,还是市场叙事?
- 是否有资本开支、订单、政策、技术迁移、客户部署作为证据?
- 这个趋势是短期主题,还是 3-5 年趋势?
- 哪些信号会证伪这个趋势?

## Step 2: Supply-chain trace

从下游到上游拆。

Audience rule: assume the reader is smart but new to this industry. Every layer must explain "这一层是什么、为什么需要它、谁在做、为什么难"。

Do not output only an ASCII chain. Pair the map with layer explainer cards.

从下游到上游拆:

```text
End demand
  ↓
System / platform
  ↓
Core hardware
  ↓
Module
  ↓
Component
  ↓
Material
  ↓
Equipment / process
  ↓
Geography / policy constraint
```

每一层说明:

- 这一层做什么。
- 用一句话解释给非行业读者听。
- 为什么下游离不开它。
- 上游依赖是什么。
- 供应商是否集中。
- 扩产是否困难。
- 是否存在替代路线。
- 代表公司及其证据引用 id。

## Step 3: Chokepoint hunt

每个潜在瓶颈必须使用 `resources/chokepoint-scorecard.md` 的六因子评分：

| Factor | Question | Score |
|---|---|---:|
| Demand rigidity | 下游增长是否必然拉动它？ | 0–5 |
| Supply concentration | 合格供应是否集中？ | 0–5 |
| Expansion difficulty | 扩产是否慢、贵、难认证？ | 0–5 |
| Substitution difficulty | 替代方案是否不成熟或代价高？ | 0–5 |
| Customer switching cost | 客户更换供应商是否困难？ | 0–5 |
| Economic capture | 供应偏窄是否能转化为收入、毛利率或现金流？ | 0–5 |

Total score: 30.

高分不等于买入指令。高分只代表研究优先级。若经济捕获、财务基线或估值验证缺失，只能写“潜在卡点 / 待验证”，不能写成候选推荐。

## Step 4: Company map

将 chokepoint 映射到上市公司。

For each important company, include a short company explainer:

- 公司做什么。
- 在产业链哪一层。
- 为什么可能受益。
- 证据来自哪里。
- 纯度高/中/低的理由。
- 是否能经济捕获：收入、毛利率、backlog、现金流是否能体现。
- 最大误解风险。

必须区分:

- Core chokepoint company.
- Direct beneficiary.
- Indirect beneficiary.
- Concept-only company.

不要把"业务沾边"包装成"核心瓶颈"。

## Output

```markdown
# Chain Trace: {Topic}

## 1. Trend Reality Check

## 2. Supply Chain Map

## 3. Layer Explainer Cards

## 4. Physical Constraints

## 5. Chokepoint Ranking

Include six-factor score, total score out of 30, evidence for each factor, and missing evidence.

## 6. Company Map

## 7. Company / Technology Explainer Cards

## 8. What is only concept-related?

## 9. Evidence needed next

## 10. Preliminary Research Grade

## 11. Stage Result
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

Default next stage: `Thesis Audit`.

## Guardrails

- Do not give buy/sell commands, target prices, or position sizing.
- Do not assume a company benefits just because it mentions AI.
- Do not treat social-media claims as proof.
- Clearly mark uncertainty.
- Do not proceed as if missing source categories were checked.
