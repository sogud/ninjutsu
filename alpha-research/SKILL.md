---
name: alpha-research
description: Run source-grounded investment research through one entry point. Use when the user wants to clarify a vague market idea, build a source map, investigate a trend or company, trace a supply chain or chokepoint, audit an investment thesis, challenge a popular narrative, resume an interrupted Alpha Research run, or produce a final evidence-gated HTML report.
---

# Alpha Research

## Purpose

`alpha-research` 是唯一公开入口。它把澄清问题、来源获取、产业链追踪、论点审计和报告质量门组织成一条可恢复的研究流程。

用户不需要选择或切换其它 Skill。阶段是本 Skill 的内部模块，按需读取。

可以给出有数据、逻辑、引用、风险和证伪条件的候选公司研究判断，但不能输出买卖指令、目标价、仓位建议或收益承诺。

## Internal stages

| Stage | Read when needed | Primary output |
|---|---|---|
| Clarify | `references/stages/clarify.md` | `research-brief.md` |
| Source Map | `references/stages/source-map.md` | `source-map.md` and Source Gate |
| Chain Trace | `references/stages/chain-trace.md` | `chain-trace.md` |
| Thesis Audit | `references/stages/thesis-audit.md` | `thesis-audit.md` |
| Report Quality | `references/stages/report-quality.md` | `report-quality.md` and `report.html` |

Do not load every stage file up front. Read the current stage and any dependency needed to interpret existing artifacts.

## Modes

Infer the mode from the request. Do not ask the user to choose a mode when it is already clear.

| Mode | When to use | Stage behavior |
|---|---|---|
| `full` | End-to-end research; default | Run all required stages in order |
| `clarify` | The question or thesis is vague | Run Clarify only |
| `source` | The user needs evidence collection or a failed Source Gate repaired | Run Source Map and acquisition |
| `trace` | The user asks about supply chains, physical constraints, or chokepoints | Run Chain Trace after checking source readiness |
| `audit` | The user supplies a thesis or prior research to challenge | Run Thesis Audit; mark missing dependencies |
| `report` | Prior artifacts exist and the user wants the final report | Recheck gates, then run Report Quality |
| `resume` | An earlier run was interrupted | Detect the first incomplete or invalid stage and continue |

An explicit stage request may start in that stage, but it does not bypass evidence requirements or the final Source Gate.

## Defaults

| Parameter | Default |
|---|---|
| Mode | `full` unless the request or existing artifacts imply another mode |
| Language | Chinese |
| Market scope | Global |
| Evidence standard | Strict |
| Source collection | Enabled |
| Final format | Single-file `report.html` |
| Reader | Intelligent non-specialist investor/research reader |
| Candidate companies | Allowed only after source-gated evidence, risks, counterarguments, and failure criteria |
| Trading actions | Disabled |

Infer defaults silently. Ask only when the answer materially changes scope, evidence requirements, permissions, or conclusions.

## Step 1: Detect runtime and permissions

Before research:

1. Detect available web search, fetch/PDF, filing, company IR, financial-data, academic, patent, news, social, browser, and alternative-data capabilities.
2. Detect whether relevant tools are authenticated and reachable; do not assume installation or login.
3. Prefer original sources and platform-native tools already available.
4. Ask for explicit approval before installing dependencies, running setup commands, checking paid/private sessions, or requesting API keys.
5. Record available, missing, blocked, and not-material channels in `run-log.md` or `tool-status.md`.

Use:

- `resources/research-tool-stack.md` for channel requirements and quality ceilings.
- `resources/source-profiles.md` for source mixes by research object.
- `resources/source-recipes.md` for acquisition order and fallback paths.
- `resources/data-rigor.md` for financial-data checks and minimum company data packs.
- `resources/tool-install-sources.md` for optional tool setup after approval.
- `resources/data-providers/` for provider-specific playbooks.

Tools transport evidence; they are not evidence. Final citations must point to original filings, disclosures, official data, papers, patents, market data, news, or original narrative sources.

## Step 2: Resolve the run directory

Use this priority:

1. A path explicitly supplied by the user.
2. The host Project's declared report root and topic directory.
3. An existing Alpha Research run matching the topic.
4. Portable fallback: `alpha-research-output/{topic-slug}/`.

Use this artifact contract:

```text
run-log.md
research-brief.md
source-map.md
chain-trace.md
thesis-audit.md
report-quality.md
report-source.md  # optional intermediate
report.html       # final report
```

Never create a second copy of a formal report when the host Project defines a canonical report root.

## Step 3: Detect progress and route

Inspect existing artifacts before asking questions or starting work.

Resume from the first condition that applies:

1. Missing or materially ambiguous `research-brief.md` → Clarify.
2. Missing `source-map.md`, Source Gate missing, or Source Gate FAIL → Source Map and source acquisition.
3. Missing `chain-trace.md` when supply-chain analysis is material → Chain Trace.
4. Missing or stale `thesis-audit.md` → Thesis Audit.
5. Missing `report.html`, failed final gate, or artifacts changed after the report → Report Quality.
6. Valid final report with no new evidence → stop and explain that the run is complete.

Do not repeat questions answered by existing artifacts. A stage is complete only when its output and gate conditions are satisfied, not merely when its file exists.

## Step 4: Execute stages

Default order:

```text
Clarify → Source Map → Chain Trace → Thesis Audit → Report Quality
```

After each stage:

- save or update its artifact;
- update `run-log.md` with decisions, sources, gaps, and gate status;
- continue internally when the next stage is allowed;
- stop only for a hard gate, required user permission, missing critical input, or completed requested mode.

Do not tell the user to invoke another Skill. Refer to the next internal stage instead.

## Step 5: Enforce hard gates

Source Gate must be **PASS** before polished final synthesis.

PASS requires:

- a Source Registry with stable citation ids;
- clickable original URLs or previewable stable locators for key Facts;
- source-specific channels appropriate to the research object;
- official filing/disclosure and financial baseline for material company claims;
- technical/patent/standards evidence for material technical claims;
- original narrative capture for material anti-hype claims;
- official/recognized commodity data for material commodity claims.

If Source Gate is **FAIL**:

1. stop before final `report.html`;
2. produce exact missing-source and acquisition actions;
3. request approval where access or setup is required;
4. label any requested working note `Draft — Source Gate Failed`.

Re-run the gate against the final draft. A previous PASS becomes invalid when the report introduces uncited Facts, local-file citations, unsupported figures, or missing financial/narrative evidence.

## Step 6: Produce the final response

When the final gate passes, produce:

1. Research conclusion in plain language.
2. Source and evidence quality summary.
3. Supply-chain/chokepoint findings when material.
4. Positive and negative research views.
5. Risks, Evidence Gaps, and kill criteria.
6. Candidate-company logic only when sufficiently supported.
7. Final Dense Calm + ECharts `report.html` with clickable citations and sourced SVG charts.

Markdown files are process artifacts. `report.html` is the default final deliverable.

## Guardrails

- Separate Fact, Inference, Assumption, and Rumor.
- Do not invent sources, data, citations, customers, or technical relationships.
- Do not promote weak evidence through confident prose or polished design.
- Do not use search snippets or local process files as proof for external Facts.
- Do not turn chokepoint score or report grade into an investment rating.
- Do not output buy/sell commands, target prices, position sizing, or return guarantees.
- Do not access brokerage accounts, positions, or trading functions unless explicitly requested; confirm again before any write operation.
- Explain specialist language for an intelligent non-specialist reader.
- Always include counterarguments, risks, failure criteria, and a research disclaimer.
