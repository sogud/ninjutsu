---
name: to-spec
description: Turn the current conversation, agreed plan, or supplied requirements into a local Markdown implementation spec. Use when the user asks to write a spec, PRD, implementation specification, technical specification, or to document an agreed feature. Inspect the target repo, synthesize without restarting the interview, save the spec in the repo's documented local location, and never create or publish GitHub Issues or other tracker items.
---

# to-spec

把当前对话中已经明确的需求整理成一份本地可实施 Spec。不要重新访谈用户，也不要把 Spec 发布到任何外部系统。

## Rules

- 只写目标工作区或仓库内的 Markdown 文件。
- 禁止创建 GitHub Issue、调用 Issue Tracker、添加标签或发布外部 PRD。
- 优先使用目标仓已有的领域术语、文档结构、ADR 和测试方式。
- 先检查当前分支和工作区状态；保留用户已有改动，不修改无关文件。
- 已有信息足够时直接综合；必要但未确认的内容写成假设或 Open Questions，不重开需求访谈。
- 只写实现需要的决定，不为显得完整增加重复抽象、兼容层或未来功能。

## Process

1. 确认目标仓、任务范围和本地规则。
2. 读取与功能直接相关的代码、领域文档、ADR、测试和现有 Spec 约定。
3. 选择最高且最少的测试入口：优先复用现有公开接口；只有现有入口无法验证目标行为时才提出新入口。
4. 从当前对话提取已确认需求、限制、假设和暂不做的内容。
5. 按下面模板写 Spec。
6. 按以下优先级保存：
   1. 用户指定路径；
   2. 目标仓规则声明的 Spec 或文档目录；
   3. 目标功能所属模块的 `docs/<topic>-spec.md`；
   4. 仓库根目录的 `docs/<topic>-spec.md`。
7. 检查 Spec 是否与代码现状一致，运行 `git diff --check -- <spec-file>`。
8. 报告文件位置、核心范围、验证结果和仍未决定的问题。

## Template

```markdown
# <Feature> Spec

## Problem Statement

从用户角度说明当前问题、现状和为什么需要改变。

## Solution

说明用户最终能做什么，以及系统需要提供的核心行为。

## User Stories

使用编号列表：

1. As a <actor>, I want <feature>, so that <benefit>.

覆盖正常流程、失败情况、数据边界、可观察结果和维护者需求。数量由功能复杂度决定，不为“全面”重复同义需求。

## Implementation Decisions

记录已经决定的模块边界、主要接口、数据契约、状态变化、错误行为、兼容要求和架构选择。

避免写容易过期的具体文件路径和完整代码。只有简短类型、状态机或 schema 比文字更准确时才内联，并注明它表达的是决定而不是实现草稿。

## Testing Decisions

说明：

- 最高层测试入口；
- 要验证的外部行为；
- 需要保留的现有回归测试；
- 失败和边界情况；
- 可执行的验收标准。

## Out of Scope

列出本次明确不做、需要另开 Spec 或缺少授权的内容。

## Open Questions

只记录真正影响实现、但当前对话没有答案的问题。没有则写 `None`。

## Further Notes

记录来源、迁移提示、风险或后续阶段条件。没有实质内容时省略。
```

## Quality Check

- 每项决定都能追溯到用户请求、现有代码事实或明确假设。
- Problem、Solution、Stories、Implementation 和 Testing 互相一致。
- 测试验证外部行为，不绑定内部实现细节。
- Out of Scope 能阻止自然但未经同意的范围扩大。
- Open Questions 不伪装成已决定事项。
- 文档不包含 Issue Tracker、GitHub Issue、标签或发布步骤。
