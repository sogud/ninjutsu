---
name: add-comment
description: Add high-signal comments to existing or just-completed code changes. Comments only, never change behavior. Judge the code's purpose first, then pick a level — L1 concise (engineering default), L2 detailed (critical paths / handoff), L3 teaching (learning code, explain every symbol). Comment language follows the target codebase's existing comment language — never default to Chinese or English. Use when the user asks to "add comments", "comment this", "explain every X", or "make it readable like prose".
---

# add-comment

Add high-signal comments so future readers quickly grasp *why it's written
this way, where data comes from, how state flows, how to verify* — not a
prose translation of the code.

## Comment language

Match the dominant language of existing comments in the target file/repo.
Never default to Chinese or English. If the codebase has no comments, follow
its docs/README language; if still ambiguous, follow the user's request
language and say so in the report.

## Levels

Judge the purpose first, pick a level, state the choice in the report.
The user's explicit level always wins.

| Signal | Level |
| --- | --- |
| learn/tutorial/playground dirs, `examples/` exercises, study-note code | L3 |
| "explain every X", "make it readable like prose", "teach me" | L3 |
| production/business code, daily bugfixes | L1 |
| cross-module paths, handoff, complex state machines, async orchestration | L2 |

Mixed cases: judge per file. Unjudgeable → L1, with the reasoning stated.

### L1 concise (engineering default)

- Comment only the non-obvious: boundaries, data contracts, persistence,
  async side effects, fallbacks, ordering dependencies.
- 2–3 lines each: why this way, where the data comes from.
- Never restate what the code already shows.

```ts
// Session restore replays only server-persisted data; component-local
// state is lost. Selection must go into the persisted payload.
const saved = data.transferState;
```

### L2 detailed (critical paths / handoff)

L1 plus: entry responsibilities and callers; field provenance across
adapters/props; state ownership (who writes / who reads / when it changes);
timing (sync vs async, fire-and-forget vs awaited, rollback on failure).
The reader is assumed fluent in the language — no syntax teaching.

### L3 teaching (learning code)

L2 plus symbol level: every syntax/keyword/type/API the target reader may
not know.

- Default reader profile: frontend (JS/TS) background unless stated; map to
  known concepts only when accurate (`fold ≈ reduce`, `Option ≈ typed null`).
- File-header overview; section banners; per-function purpose; branch rationale.
- Verify facts (API semantics, defaults, units) against source/docs first.
- High density allowed; two bottom lines hold: never change behavior,
  never invent facts.

```rust
// Unlike JS, `let` bindings are immutable by default;
// `let mut` is required to mutate.
let s = String::from("hello");
```

## Do not

- Change logic, names, control flow, or formatting while commenting.
- Invent interfaces / fields / config keys.
- Zero-information comments ("set the variable", "call the function") —
  except L3 syntax explanations, which are reader knowledge, not restatement.
- Treat TODOs as facts; unverified contracts get "unverified" or nothing.
- Rewrite production files at L3 density unless explicitly asked.

## Verify

`git diff --check -- <files>`; run lint/build when comments could affect
syntax (JSX/TSX); `cargo check` or equivalent for compiled languages.

## Report

Purpose judgment and level choice; files touched; comments-only confirmation;
verification run; implementation risks the comments surfaced but didn't fix.
