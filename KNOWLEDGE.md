# Knowledge

Persistent workspace knowledge captured from conversations and code context.

## Skill Admin Web UI 开发

> Captured: 2025-05-14
> Tags: skill-admin, web-ui, python, zero-dependency
> Context: 为 skill-admin 开发零依赖 Web 管理界面，支持增删改查

### Summary

用 Python 标准库 `http.server` 构建零依赖 Web 服务，前端为单页 HTML（内嵌 CSS/JS），实现跨 20+ AI 平台的技能可视化管理。

### Key Decisions

#### 后台启动模式

- `web` 命令默认后台运行（`subprocess.Popen` + DEVNULL），不阻塞 AI 对话
- 用 `.web.pid` 文件记录进程 ID，`web-stop` 通过 `os.kill(pid, SIGTERM)` 停止

#### 扫描逻辑（关键修复）

1. **不递归扫描** — 只遍历每个平台 `skills/` 目录的顶层条目，避免嵌套目录误报
2. **不去重** — 每个平台独立列出所有技能，即使通过 symlink 指向同一源
3. **YAML block scalar 解析** — 支持 `>`、`>-`、`|`、`|-` 等多行描述语法

#### 删除保护

- 删除 symlink → 只删 symlink
- 删除真实源（.agents）+ 有其他平台引用 → 弹窗显示影响范围，用户确认
- 提供两个选项：全部删除 vs 只删当前平台

### 项目架构

```text
skill-admin/scripts/
├── skill-admin.py        # CLI 主程序
├── skill-admin-web.py    # Web 服务（HTTP server + 单页前端）
├── skill-security.sh     # 安全扫描脚本
└── security-rules.yaml   # 安全规则配置
```

### Platform Support

| 平台 | 路径 |
|------|------|
| claude | `~/.claude/skills` |
| cursor | `~/.cursor/skills` |
| qoder | `~/.qoder/skills` |
| qoderwork | `~/.qoderwork/skills` |
| agents | `~/.agents/skills` |
| ... | 共 19 个平台 |

### When to Use

- 为 AI Agent 开发管理工具
- 需要零依赖部署的场景
- 跨平台技能/插件同步管理
- 批量操作（创建、编辑、删除、同步）

### Related

- `skill-admin/SKILL.md` — 技能定义
- `ninjutsu/skill-admin/` — Git 仓库
