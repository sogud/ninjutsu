# Stage: Clarify

## Purpose

把模糊的投资想法，拷问成一个清晰的 Research Brief。

这个阶段不做结论，不判断涨跌，不输出交易指令。
它只负责让研究问题变清楚。

## Bundled files

- Template: `templates/research-brief.md`.
- Resources: none.

Use the template when producing the final Research Brief.

## When to use

用户说出类似问题时使用：

- “AI 光通信怎么看？”
- “某某股票还能买吗？”
- “机器人有没有机会？”
- “Serenity 提到的公司是不是核心瓶颈？”
- “我想找下一个机会。”
- “这个热门故事靠谱吗？”

## Process

先问必要问题，不要直接跳到结论。

必须确认：

1. **Research object**：趋势、行业、公司、材料、技术、持仓，还是热门叙事？
2. **Research goal**：完整研究、验证 thesis，候选公司推荐，还是 anti-hype mode？
3. **Market scope**：美股、港股、A 股、全球，还是不限？
4. **Current belief**：用户现在已经相信什么？
5. **Biggest concern**：用户最担心错在哪里？
6. **Time horizon**：短期事件、1–3 年趋势，还是 3–5 年趋势？
7. **Output language / format**：中文/英文；Markdown 默认，HTML 可选。

## Default assumptions

如果用户没有说明，默认：

- Market scope: global.
- Research mode: normal.
- Output language: Chinese.
- Output format: Markdown.
- Evidence standard: strict.
- Candidate/company recommendations are allowed only after source-gated evidence is collected.
- No direct buy/sell signals.
- Include risk reminder.

## Output

Use `templates/research-brief.md` and produce:

```markdown
# Research Brief

## Topic

## Research Question

## Research Object

## User Goal

## Market Scope

## Current Belief

## Biggest Concern

## Time Horizon

## Key Unknowns

## Recommended Next Step

## Notes

## Stage Result
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

Default next stage: `Source Map`.

## Guardrails

- Do not provide investment advice.
- Do not give buy/sell commands.
- Do not turn a vague question into a confident conclusion.
- Do not skip source planning before serious research.
