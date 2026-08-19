---
name: supervisor
description: 监工模式：把长任务派给 Herdr 另一个窗格的 agent，然后定期巡检、按原则代答问卷、卡住升级、完成后核验交账。用户说"监工""盯一下""监督它做完""激活监工模式""派任务给隔壁 pane 并盯着"时使用。依赖 HERDR_ENV=1 的 Herdr 环境；其余只靠 herdr CLI，无其他硬依赖。
---

# Supervisor（监工模式）

把一个长任务交给另一个窗格的 agent 执行，主会话不阻塞；定时子 agent 巡检：
干活不打扰、问卷按原则代答、红线升级给用户、完成必须客观核验后才交账。

## 前提

- `test "${HERDR_ENV:-}" = 1` 通过（本会话在 Herdr 内）
- 目标 pane 里是一个可接受 prompt 的 agent（`herdr agent list` 可见）
- 其余只靠 herdr CLI，无其他硬依赖（pi schedule、看门狗脚本都是可选增强）

## 流程（五步）

### 1. 定位目标
`herdr pane list` / `herdr agent list` → 记下 PANE_ID（如 w1:p1）、agent 类型、cwd。
读目标 pane 最近输出（`herdr pane read <id> --lines 40`）确认它当前状态与手头工作，
避免把新任务撞进它正忙的事情里。

### 1.5 路径决策（可选，但多路径时必做）
任务存在多条明显不同的实现路线（换架构、选框架、重构 vs 新建等）时，
先加载 `bestway` 技能做路径决策：建模目标/限制/验收/失败代价，
对比至少 3 条路径（最优/稳妥/激进），选定后把"选定路线 + 不选其他路线的理由"
写进任务书的目标与范围——干活 agent 只负责执行选定路线，不在执行中重新选型。
只有一条显而易见的路线时跳过此步，不仪式化。

### 2. 写任务书
位置按任务范围选：单仓任务写进**目标仓自己的** `.artifacts/<name>-mission.md`
（就近、随仓忽略；任务书是运行态契约，不是产品 spec，不进 docs/ 或 openspec/，
产出长期决策时在收尾阶段蒸馏进目标仓 docs/）；跨仓或纯 harness 任务才用根
`<workspace>/.artifacts/`。必须包含：
- 目标与范围（做什么、**不做什么**）
- 纪律（典型项：不 git commit/push、每阶段验证方式、改动边界）
- **客观完成标准**——可机器核验的条目（文件存在、测试 exit 0、git grep 命中、
  关键数字），绝不写"agent 自述完成"这类主观标准
- 要求结束时输出总结：做了什么、验证结果、剩余风险

### 3. 派发
目标 idle 时：`herdr agent prompt <PANE_ID> "读取 <任务书路径> 并严格执行……全部完成前不要停。"`
（busy 时派发会打断它——先等 idle 或与用户确认接受打断。）
2-5 秒后 `herdr agent get <PANE_ID>` 确认 agent_status 变为 working。

### 4. 巡检：核心只靠 herdr CLI

**默认：主会话每轮对话直接巡一轮**，零额外依赖：
1. `herdr agent get <name>` 看状态（working/idle/blocked）；
2. `herdr pane read <pane> --lines 60` 看实况（问卷、报错、水位）；
3. 跑任务书完成标准里的确定性命令（typecheck/build/test 等）判定进度；
4. 异常发 `herdr notification show`，并在监控日志追加一行。

**部署后必须验证通知渠道（真实事故：herdr notification 返回 disabled，
看门狗其实已判定两个 agent 完成，但通知静默丢失，用户以为没人盯）**：
派发后立刻 `herdr notification show 测试 --body 链路检查`，读返回 JSON 的
`result.shown`；为 false 就改用系统通知（macOS osascript，看门狗脚本已内置
降级），并明确告知用户通知走系统通知中心。

**可选增强（需要长时间无人值守时才加，都不是必需）**：
- herdr pane 循环跑看门狗脚本（`infra/personal/supervisor-watch.sh`，
  conf 格式见脚本头部注释）：确定性盯状态 + 完成判定 + 通知；
- pi 会话内可另加 `subagent schedule.create` delegate LLM 巡检（问卷代答用），
  但创建后必须 `schedule.run` 当场试跑验证（真实事故：曾两小时静默零执行），
  跑不起来就回到主会话手动巡检。
非 pi 会话（Codex/Claude Code 等）用前两项即可。

### 5. 收尾
报 done 后**主会话亲自核验**完成标准（跑测试、查文件、读 pane 总结），
核验通过才向用户交账；清理附加物（若有）：看门狗 conf、schedule。
核验不通过：把缺口写成新指令派回去，监工继续。

**上下文压缩（按需，不是仪式）**——在派发下一个任务前判断，满足其一才压：
1. 水位高：目标 pane 上下文占比 ≥70%（pane 屏幕底部 footer 有
   `XX%/1.0M` 字样，监工日志每轮记录该水位）；
2. 换赛道：新任务与上一任务相关性弱（新任务书不需要引用上一任务的
   结论/代码位置/决策时）。
两条都不满足则不压——任务紧密衔接时累积上下文是资产。
压缩方式（idle 前提下）：
`herdr agent prompt <PANE_ID> "/compact 保留：<上一任务结论、剩余欠账、与新任务相关的代码位置与决策>；丢弃：调试过程与工具输出细节"`。
若新任务与前任务完全无关且水位也高，更彻底的做法是退出重开新会话
（上下文清零，任务书就是交接物）。**严禁任务中途压缩**。

## 巡检指令模板

```
你是 Herdr pane {{PANE_ID}} 的定时监工。该 pane 是独立 agent 会话，
在 {{CWD}} 执行任务书 {{MISSION_PATH}}。执行一轮"检查-处置"循环。

## 步骤
1. `herdr agent get {{PANE_ID}}` → result.agent.agent_status。
2. `herdr pane read {{PANE_ID}} --lines 60` → result.text。
3. 读监控日志 {{LOG_PATH}} 最后一条。

## 判定与处置
- A) working → 不操作。
- B) 屏幕出现问卷（选项框/"Enter to select"）→ 代答：
  * 有 (Recommended)/推荐：选它。
  * 无推荐：按 {{ANSWER_POLICY}} 选择。
  * 红线（{{RED_LINES}}）→ 禁止代答：
    `herdr notification show "{{TITLE}}: 需要你决定" --body "<问题摘要>"`。
  * 作答：`herdr agent send-keys {{PANE_ID}} <选项数字>`，2 秒后读屏确认，
    没消失补 `herdr agent send-keys {{PANE_ID}} enter`。
- C) idle、任务未完（对照任务书完成标准）、停在输入框 →
  `herdr agent prompt {{PANE_ID}} "继续执行任务书，从当前进度把剩余项做完"`。
- D) 完成判定：任务书已送达（日志有送达记录或屏幕明显在执行任务书内容），
  且 {{DONE_CRITERIA}} 全部满足 →
  先把完成总结要点记入日志与汇报，然后
  `herdr notification show "{{TITLE}}: 任务完成" --body "<摘要>"`，
  日志记 action=done。**不要在 done 时自动压缩**——是否压缩由主会话在派发
  下一任务前按水位与相关性判断。
- E) 连续两轮无变化且非 working → 升级通知"疑似卡住"。

## 日志与汇报
追加一行：[ISO时间] status=<状态> ctx=<上下文占比，从 pane footer 的 XX%/1.0M 提取>
action=<none|answered|nudged|escalated|done> detail=<≤80字>
返回一句中文汇报。

## 边界
只操作 {{PANE_ID}}；不自己写业务代码；herdr 失败只记录不修复
（notification 可能 disabled，记录即可）。
```

占位符默认值：
- `ANSWER_POLICY`：简单、最小改动、遵循任务书与项目既有约定、不过度设计
- `RED_LINES`：删除数据/分支、强推、发布、外部副作用、推翻已确认共识
- `LOG_PATH`：`<workspace>/.artifacts/<name>-monitor.log`
- `DONE_CRITERIA`：从任务书的客观完成标准逐条翻译成可执行检查。
  **防空转**：命令 exit 0 不等于通过，必须要求实质输出——测试命令要核对
  实际测试文件/用例数（"no test files found" 空转 exit 0 不算通过，
  测试被搬走时去新位置跑）；build 要核对产物文件存在；文档类标准要抽查
  内容与事实源一致。
  **防基线绿**：CHECK_CMD 不能只跑"测试/构建全过"——派发那一刻仓库本来就是绿的，
  这样的 CHECK_CMD 会在开工前就判定 done（真实事故：派发后 6 秒误报完成）。
  必须串上至少一条"功能存在性"检查：`git grep -q <新代码特征> <路径>` 或
  新文件/新产物存在，确保判定的是"新东西长出来了"而不只是"没坏"。

## 踩坑清单（血泪）

1. **完成判定必须要求"任务书已送达"为前提**——目标 agent 自己的旧 todo 完成
   会被误判成任务书完成（真实发生过）。
2. **目标 agent 自述的 done 不可信**——曾出现任务书未送达就报 done。
   一切以客观标准 + 主会话核验为准。
3. **delegate 偶尔空汇报**——先看日志和 pane 实况再下结论，
   日志在更新就不用急着重建监工。
4. **herdr notification 可能 disabled**——升级信息同时写日志，主会话汇报兜底。
5. **busy 时派发=打断**——派发前确认 idle。
6. 监工指令里写清楚"只操作目标 pane、不自己写业务代码"，
   防止监工越权直接改代码。
8. **schedule 静默失败**：创建成功 ≠ 会执行。曾出现 schedule 显示已创建、
   Next 时间正常，但两小时零执行、零通知。创建后必须按第 4 步强制试跑
   一轮并核对日志；试跑失败就降级手动巡检，绝不留无人值守的空档。
9. **空转通过**：验收命令 exit 0 可能是假的——测试文件被迁走后 test 命令
   报 "no test files found" 照样 exit 0。核验时看实质输出（测试数、产物
   文件、抽查内容），并在任务书阶段就把"防假通过"写进完成标准。
10. **通知静默失效**：`herdr notification show` exit 0 不等于送达，返回 JSON
    里 `shown:false, reason:disabled` 才是真相。曾发生两个 agent 都已完成、
    done 通知全部丢失、用户两小时没收到任何提醒。部署后必须发测试通知验证
    `result.shown`；看门狗脚本已内置 osascript 降级，通知全失败时会在日志写
    `action=notify-failed`，巡检时见到该标记要直接读 pane 实况。
11. **CHECK_CMD 基线绿误报**：只跑测试的 CHECK_CMD 在派发瞬间就会通过
    （仓库开工前就是绿的），看门狗 6 秒误报 done、之后永远不再提醒。
    CHECK_CMD 必须含"功能存在性"检查（git grep 新代码特征/新文件存在），
    判定"新东西长出来了"而不只是"没坏"。
7. **上下文压缩是按需的，不是仪式**：只有水位 ≥70% 或新旧任务相关性弱时才压；
   判断时机是派发下一任务前（那时才知道相关性），不是 done 的瞬间；
   严禁任务中途压缩。

## 管理命令

- 查：`subagent schedule.list`；停：`schedule.pause <id>`；删：`schedule.delete <id>`
- 改频率/改指令 = 删旧建新（schedule 不支持原地编辑 task）
- 同一目标同时只留一个监工，防止双监工互相催促
