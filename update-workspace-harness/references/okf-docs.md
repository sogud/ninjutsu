# OKF 文档约定

工作区的 `docs/` 是 OKF v0.2 bundle，仅保存稳定、可复用、脱离当前会话仍可理解的知识。

## 文件角色

- 根 `docs/index.md` 声明 `okf_version: "0.2"`，并作为唯一入口索引。
- `docs/log.md` 只记录重要且已确认的知识变更。
- 普通知识页使用 YAML frontmatter，至少包含 `type`；按需要补充 `title`、`description`、`tags`、`sources`、`status` 或 `stale_after`。
- 工作区专属字段使用 `x_<workspace>` 命名空间，不占用 OKF 标准字段。
- 子目录 `index.md` 与 `log.md` 不是 concept，除根 `index.md` 外不写 OKF frontmatter。

## 内容边界

- `docs/`：规则、架构、概念、仓库职责和已验证流程。
- skill 目录：动作、参数约束和工作流；不保存事实正文的副本。
- 结构化定义、生成物和可重建产物使用目标工作区已有的指定位置；不为它们在 `docs/` 创建副本。

## 更新方式

1. 先确认信息稳定、可复用且有证据；一次性过程、猜测和敏感信息不写入 OKF。
2. 检查是否已有正文；更新唯一页面，不创建平行专题。
3. 新增页面时补入口索引和必要的 Markdown 链接。
4. 有来源、时效或不确定性时，用 frontmatter 和正文明确说明；不要伪造核验时间或来源。
5. 校验 frontmatter、索引链接、相对路径和 `git diff --check`。
