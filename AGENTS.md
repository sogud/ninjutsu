# Skills

AI Agent 技能管理仓库。

## Skills

| Skill | Description |
|-------|-------------|
| [alpha-research](alpha-research/) | 单入口 Alpha 研究：来源、产业链、论点审计和最终报告 |
| [beta-research](beta-research/) | 单入口 Beta 研究：市场状态、因子暴露、相关性和压力测试 |
| [update-harness](update-harness/) | 维护可复用知识与工作区 Harness |
| [pm](pm/) | 面向软件工程的专业 PMP 项目管理助手：项目判断、交付治理、风险依赖、发布与状态汇报 |
| [skill-admin](skill-admin/) | 跨 19 个 AI 平台的技能管理工具（CLI + Web UI） |
| [skill-linter](skill-linter/) | 技能质量检查器 |
| [terminal-workflow](terminal-workflow/) | 终端工作流与环境维护 |
| [to-spec](to-spec/) | 把当前对话整理成本地 Markdown Spec，不发布到 Issue Tracker |
| [codebase-render](codebase-render/) | 单文件代码库讲解：认知模型、目录结构、注释伪代码、全链路与失败场景；支持增量同步 |

## Export boundaries

- `alpha-research` and `beta-research` are Finance-only source Skills. Export them only through the Harness manifest to `projects/finance/.agents/skills/`; do not publish them to the global shared Skill directory.
- Each research Skill exposes one public `SKILL.md`; detailed stages remain internal references.
