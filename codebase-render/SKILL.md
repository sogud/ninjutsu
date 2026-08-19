---
name: codebase-render
description: Produce ONE self-contained architecture document that lets a reader master a codebase without opening source files — cognitive model, glossary, why-each-component-exists, data shapes, per-file annotated pseudocode, end-to-end chains, failure scenarios, with mermaid diagrams. Two modes - full write-up and incremental doc-sync after code changes. Use when the user asks to "understand this codebase", "explain the whole architecture in one doc", "write a walkthrough I can learn from", "一文读懂", "吃透代码", "读代码", or says code changed and the doc needs updating.
---

# codebase-render

Write ONE document that teaches an entire codebase. The reader should finish
it able to predict what any core file does, why it exists, and what happens
when it fails — without opening the source.

## Two modes

- **Full write-up** (no master doc exists yet, or the user asks for a new
  one): produce the complete document, run adversarial acceptance.
- **Incremental sync** (master doc exists, code changed): diff the repo since
  the doc's baseline, verify each change in source, patch ONLY the affected
  sections in place (same single file, same structure). Never create a second
  file. Fact-check the patched claims against source before delivery; skip the
  full newcomer round unless the change restructures core concepts.

## Hard rules

1. **One file.** All content in a single Markdown document. Never split; if an
   earlier draft was split, merge and delete the rest (move to trash, never
   `rm -rf`).
2. **Read before writing.** Every pseudocode block and claim must be derived
   from code actually read this session (source, graph tools, or verified
   prior reads). Never invent behavior. Unverified details get `[待核实]`.
3. **Pseudocode over raw code.** Translate logic into language-neutral
   pseudocode with inline comments explaining *why*, not just *what*.
   Raw code only for tiny contract/interface shapes and example data.
4. **Comments do the teaching.** Every non-trivial pseudocode line group gets
   a comment: purpose, data source, failure behavior, or ordering constraint.
5. **Numbers are sacred.** Ports, timeouts, limits, file paths, error strings
   must be copied from source exactly — verify before writing.
6. **Document language follows the user's request language.** Pseudocode
   identifiers stay in the codebase's language.
7. **No code changes.** This skill produces documentation only.

## Required document structure (full write-up)

```
# <Repo> 架构完整说明书
0. 预备知识（读者零背景假设）
   a. 认知对齐   — table: prerequisite concept → one-line explanation →
                  what it maps to in THIS repo
   b. 术语表     — every domain term used later, defined once, consistently
   c. 组件存在原因 — for EACH core component: problem → what breaks without
                  it → so we have it. Cover "X vs Y 分工" pairs explicitly.
   d. 核心数据结构 — real shapes with example values: persisted records,
                  in-memory state, event unions, on-disk runtime files
1. 整体架构图    — ASCII diagram + equivalent mermaid flowchart + one-sentence
                  summary
2. 目录结构      — annotated tree; every listed dir gets a role note
3. 不变的规则    — 2–4 invariants the whole system obeys (memorize first)
4. 核心机制最小示例 — the key abstraction (DI, plugin, state machine…) as a
                  minimal runnable-style pseudocode demo
5. 核心文件逐个讲 — per file: annotated pseudocode of the essential functions
                  + "要点" bullets. Use mermaid where a state machine or
                  multi-step ownership/concurrency check exists.
6. 完整链路逐帧走读 — 3–5 end-to-end chains (startup, main request path,
                  shutdown, plus domain-specific): numbered steps AND a
                  mermaid sequenceDiagram for the primary chain.
7. 失败场景速查表 — table: scenario → behavior → who handles it.
                  Cleanup/timeout/fallback logic MUST appear here.
8. 最小示例：扩展系统 — "add a new X" minimal example proving the seams
9. 阅读顺序建议  — table: order → file → doc section → what you learn
```

Skip a section only if the codebase genuinely lacks it, and say so.

## Writing process (full write-up)

1. **Map**: directory tree + 8–15 core files (entry points, registries, state
   machines, boundary layers). Graph/outline tools first, verify with reads.
2. **Read top-down**: entry → composition root → registries → state machines →
   boundary/IO layers.
3. **Extract invariants**: ownership, validation boundaries, lifecycle,
   concurrency rules → section 3.
4. **Translate** each core file to annotated pseudocode. Drop boilerplate,
   never drop error paths, locks, or cleanup logic.
5. **Walk the chains** through the real files as numbered sequences.
6. **Assemble** into the single file with a table of contents; record the
   repo's commit hash as the doc baseline at the top.
7. **Self-check**: can a newcomer answer "what happens when X fails?" from the
   doc alone? Does every pseudocode block have a why-comment? One file?
8. **Adversarial acceptance** (mandatory): two fresh-context subagents in
   parallel —
   - *Newcomer simulation*: reads ONLY the doc (source forbidden), answers
     ~10 comprehension questions, grades each answer doc-sufficient / shaky /
     missing, lists sticking points by severity.
   - *Code fact-checker*: samples ≥12 concrete claims (paths, ports, limits,
     timeouts, error strings) against source, verdict per claim.
   Then verify disputed behavior in source yourself and patch before delivery.

## Incremental sync process

1. Get commits/diff since the doc baseline (git log/diff, working tree status).
2. Classify changes: architecture-level (new app/package/service, new data
   shape, lifecycle change) vs leaf-level (internal refactor, copy fixes).
   Only architecture-level changes touch the doc.
3. Verify each change by reading the actual new code — never trust commit
   messages alone.
4. Patch sections in place: architecture diagram, directory tree, glossary,
   component rationale (0c), data shapes (0d), per-file pseudocode, chains,
   failure table, reading order. Update the baseline commit hash.
5. Fact-check every patched claim against source (numbers especially).

## Anti-patterns

- Multi-file doc series — always one file.
- Prose summaries without pseudocode ("this module handles X" — useless).
- Copy-pasting raw source without translation or comments.
- Happy paths only — failure and cleanup logic is mandatory.
- Claiming behavior not verified by reading code this session.
- Using a term before defining it (glossary 0b or inline at first use).
- Naming components without justifying them (0c covers every component).
- Describing logic without showing data shapes (0d for every state table).
- Incremental sync that creates a "v2" document instead of patching in place.
