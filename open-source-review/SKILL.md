---
name: open-source-review
description: 开源前审查：扫描目标仓库的当前内容、完整 git 历史与开源规范，找出密钥、个人隐私、公司内部信息、过程沉淀等不适合公开的内容，产出分级报告与清理建议。只审查不执行清理，重写历史等破坏性操作必须用户授权。用户说"开源审查""开源前检查""这个能开源吗""open source audit""适不适合开源"时使用。
---

# Open Source Review（开源审查）

目标：在仓库公开之前，回答一个问题——**这里面有没有不该被看到的东西，
项目够不够开源规范**。审查三层：当前内容、完整 git 历史、开源元信息。

## 原则

- **只审查，不清理**：产出报告与建议；删文件、重写历史、改 README 等执行动作
  必须用户逐项授权。重写 git 历史是破坏性操作，单独确认。
- **历史 ≠ 当前**：现在删掉的文件、改掉的密钥，只要进过 commit 就还在历史里。
  只扫工作树等于没审。
- **报告分级**：🔴 阻断（必须处理才能公开）/ 🟡 建议（影响形象或体验）/
  🟢 通过。每条发现给出：位置（文件:行 或 commit）+ 内容摘要 + 原因 + 处理建议。
- **先懂这个仓再审**：读目标仓 README/AGENTS.md/上下文，判断它的敏感源类型
  （工作仓→公司信息为主；个人仓→隐私为主；学习仓→可能含工作残留）。
- 不整读大二进制/大日志（上下文体积红线）；扫描用工具与模式匹配。

## 流程

### 1. 摸底
- 仓库基本信息：语言、体积、commit 数、分支/tag、贡献者及其邮箱
  （`git shortlog -sne --all`——**作者邮箱本身就是公开后会暴露的信息**，必查）
- 读 README/AGENTS.md，确定该仓的敏感源画像
- 确认目标：直接公开、私有转公开、还是 fork 出干净版

### 2. 当前内容扫描
敏感模式匹配（`rg`，按需补充该仓特有模式）：

- **密钥凭据**：`AKIA[0-9A-Z]{16}`、`sk-[A-Za-z0-9]{20,}`、`-----BEGIN .* PRIVATE KEY-----`、
  `ghp_/gho_/xoxb_/Bearer `、`password\s*[:=]`、`.env*`、`auth.json`、`credentials`、
  `*token*`、`*secret*`、连接串（`mysql://`、`postgres://`、`mongodb+srv://`）
- **个人隐私**：绝对路径暴露用户名（如 `/Users/<name>/`、`/home/<name>/`）、
  个人邮箱、手机号模式、真实姓名出现的位置（package.json author、注释、文档）
- **公司内部**：内部域名（按用户环境定制，如 `*-corp.example`、`*.internal.example`、
  内网 IP 段 `10./172.16-31./192.168.`）、内部系统名、工号、内部 wiki/文档链接
- **过程沉淀**：`.artifacts/`、调研笔记、竞品分析、临时快照、debug 日志、
  含内部上下文的 TODO/FIXME 注释、会话记录
- **AI 协作残留**（AI 摸过的仓特色风险，传统扫描器不查）：handoff/交接文件
  （handoff.md 类）、会话记录与上下文导出、agent 工作目录（.claude/.codex/.pi/
  会话产物）、带个人记忆的 CLAUDE.md/AGENTS.md、计划/评审产物里的内部上下文、
  生成代码里的用户名绝对路径、AI 署名（Co-Authored-By bot、"🤖 Generated"
  类 commit message——不算敏感但决定要不要保留）
- **依赖供应链**：私有 registry 源、指向私有仓的 git 依赖、内部包名

### 3. Git 历史扫描（最容易漏的一层）
- **历史文件全集**：`git log --all --diff-filter=A --name-only --format=` 列出
  曾经存在过的所有文件；对当前已删但历史存在的敏感文件名（.env、key、内部文档、
  日志、数据文件）逐个 `git log --all -p -- <file>` 抽查内容
- **密钥进历史**：有 gitleaks 就跑 `gitleaks detect --no-git` 之外的全历史模式
  （`gitleaks detect` 默认扫全历史）；没有则 `brew install gitleaks`，装不了
  退回 rg 模式对 `git log -p` 抽样
- **密钥活性验证**（决定严重度的关键步）：gitleaks 找到的密钥，用 trufflehog
  验证是否仍然有效（`trufflehog git file://. --only-verified`，没有则
  `brew install trufflehog`）。**活着的密钥 = 清理历史也不够，必须先轮换作废**
  （公开史里它永远在）；已失效的才只需清历史。报告里每个密钥发现必须标注
  活性状态；无法验证的按活着处理
- **commit message 审查**：`git log --all --format=%B` 扫敏感词（内部系统名、
  人名、"先不加密码后面删"之类的自白、AI 署名是否保留）
- **作者身份**：贡献者邮箱是否为工作/私人邮箱，公开后会永久暴露——
  建议项：新历史用 noreply 邮箱

### 4. 开源规范检查
逐项核对并标注现状：

- LICENSE：有没有、与声明是否一致（package.json/Cargo.toml 的 license 字段）
- README：动机（为什么有这个项目）、quickstart（能不能 5 分钟跑起来）、
  示例、截图/动图（UI 项目）、语言风格（开源读者视角，内部黑话要翻译或删）
- .gitignore 卫生：会不会把本地配置再提交出去
- CONTRIBUTING / issue 模板 / CI：加分项，缺了标 🟡
- 命名与死目录：内部代号、空壳目录、占位文件

### 5. 全球化与专业度（全球项目维度）

- **LICENSE 实质**：是否 OSI 批准（Apache-2.0/MIT 等）；LICENSE 文件与
  package.json/Cargo.toml 的 license 字段一致；无 LICENSE = 🔴（法律上非开源）
- **README 全球可读**：英文主体；结构含一句话价值主张、少量有意义徽章
  （CI/license，不要虚荣徽章）、视觉（截图/GIF）、Features、可复制运行的
  Quick start、详细文档链到 docs/、Contributing/Security/License；
  无内部黑话、无机翻味；用户/评估者/贡献者三种读者一分钟内各取所需
- **治理文件**：CONTRIBUTING（含 AI 贡献政策）、CODE_OF_CONDUCT、SECURITY
  政策；缺了标 🟡
- **i18n 就绪**：UI 字符串是否硬编码在组件里；有无 i18n 框架
  （i18next/Paraglide/react-intl）；locale 覆盖（至少 en + 一门其他）；
  默认语言；语言切换入口；服务端字符串语言一致性
- **视觉资产隐私**：README/文档截图必须用干净 demo 状态截取
  （空工作区/合成数据），严禁从用户运行中实例截屏——活数据=隐私泄露。
  审查时把截图/动图当隐私面检查：画面里的任务名、对话、路径、账号一律红线
- **注释专业度**：不做不可靠的"AI 检测"，扫信息密度与署名：
  obvious-comment（"// 初始化计数器"）、narrator-comment（"// 本函数处理…"）、
  step-comment（"// Step 1:"）等低密度模式；AI 署名（Co-Authored-By bot、
  "🤖 Generated"）；注释语言一致性（全球项目里本地语言注释 = 🟡）。
  参照 sloplint/signal-oss 的密度思路，命中是 review prompt 不是罪证

### 6. 报告与建议
输出分级清单后，给出处理路径（只建议，不执行）：

- 🔴 密钥/隐私/公司信息：从当前删除 + **历史清理**选项说明：
  `git filter-repo`（推荐）或 squash 成全新初始 commit（最简单彻底，
  代价是丢历史）；若仓库尚未 push 公开，重写无副作用
- 🔴 **私有内容移出公开仓时，移文件不够**：只要它进过历史，
  必须重置历史（squash 全新初始 commit + force push + 本地 reflog expire + gc），
  否则它永远躺在公开历史里。移完后用
  `git log --all --name-only --format= | grep <敏感词>` 验证清零
- 🔴 活着的密钥：**先轮换作废，再清历史**——顺序不能反，清史不改变泄露事实
- 🟡 README/规范：给具体改写建议或直接起草（经授权）
- 作者邮箱：重建历史时统一换 noreply 邮箱
- 若敏感内容过多：建议"重写干净历史 + 保留私有原仓"而不是就地清洗

## 交付格式

```
# 开源审查报告：<repo>
结论：可公开 / 处理 🔴 后可公开 / 不建议当前形态公开
🔴 阻断项（N）：…每条：位置 + 摘要 + 原因 + 建议
🟡 建议项（N）：…
🟢 通过项：密钥扫描/历史文件/规范核对的覆盖范围声明
未覆盖：明确说出没查到的角落（大二进制、未读的外部依赖源码等）
```

"未覆盖"一节必须有——审查的价值在于边界清晰，不装全知。
