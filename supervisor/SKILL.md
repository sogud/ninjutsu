---
name: agent-overseer
description: 监工模式：把长任务派给 Herdr 另一个窗格的 agent，然后定时巡检、按原则代答问卷、卡住升级、完成后核验交账。用户说"监工""盯一下""监督它做完""激活监工模式""派任务给隔壁 pane 并盯着"时使用。依赖 HERDR_ENV=1 的 Herdr 环境与 subagent schedule。
---

# Agent Monitor（监工模式）

把一个长任务交给另一个窗格的 agent 执行，主会话不阻塞；定时子 agent 巡检：
干活不打扰、问卷按原则代答、红线升级给用户、完成必须客观核验后才交账。

## 前提

- `test "${HERDR_ENV:-}" = 1` 通过（本会话在 Herdr 内）
- 有 subagent schedule 能力（pi-subagents）
- 目标 pane 里是一个可接受 prompt 的 agent（`herdr agent list` 可见）

## 流程（五步）

### 1. 定位目标
`herdr pane list` / `herdr agent list` → 记下 PANE_ID（如 w1:p1）、agent 类型、cwd。
读目标 pane 最近输出（`herdr pane read <id> --lines 40`）确认它当前状态与手头工作，
避免把新任务撞进它正忙的事情里。

### 2. 写任务书
路径：`<workspace>/.artifacts/<name>-mission.md`。必须包含：
- 目标与范围（做什么、**不做什么**）
- 纪律（典型项：不 git commit/push、每阶段验证方式、改动边界）
- **客观完成标准**——可机器核验的条目（文件存在、测试 exit 0、git grep 命中、
  关键数字），绝不写"agent 自述完成"这类主观标准
- 要求结束时输出总结：做了什么、验证结果、剩余风险

### 3. 派发
目标 idle 时：`herdr agent prompt <PANE_ID> "读取 <任务书路径> 并严格执行……全部完成前不要停。"`
（busy 时派发会打断它——先等 idle 或与用户确认接受打断。）
2-5 秒后 `herdr agent get <PANE_ID>` 确认 agent_status 变为 working。

### 4. 创建监工 schedule
`subagent schedule.create`：`every` 默认 10m，agent 用 `delegate`，
task 用下面的巡检指令模板（替换全部占位符）。schedule 名字带任务标识，如 `<name>-monitor`。

### 5. 收尾
监工报 done 后**主会话亲自核验**完成标准（跑测试、查文件、读 pane 总结），
核验通过才向用户交账；`schedule.pause`（可能复用）或 `schedule.delete`。
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
- `DONE_CRITERIA`：从任务书的客观完成标准逐条翻译成可执行检查

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
7. **上下文压缩是按需的，不是仪式**：只有水位 ≥70% 或新旧任务相关性弱时才压；
   判断时机是派发下一任务前（那时才知道相关性），不是 done 的瞬间；
   严禁任务中途压缩。

## 管理命令

- 查：`subagent schedule.list`；停：`schedule.pause <id>`；删：`schedule.delete <id>`
- 改频率/改指令 = 删旧建新（schedule 不支持原地编辑 task）
- 同一目标同时只留一个监工，防止双监工互相催促
