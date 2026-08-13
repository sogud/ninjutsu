# skills

Personal agent skills collection — workflows, review checklists, and
research pipelines authored for daily use with pi / Claude Code / Codex / Qoder.

> Note: skill bodies are written in Chinese (the author's working language).
> Structure and triggers follow the standard `SKILL.md` convention, so they are
> usable by any agent regardless.

## Skills

| Skill | What it does |
| --- | --- |
| `add-comment` | Comment code at three signal levels (L1 concise / L2 detailed / L3 teaching); comments explain *why*, never restate the code |
| `agent-overseer` | Overseer mode: dispatch a long task to an agent in another terminal pane, poll it on a schedule, answer its questionnaires by policy, escalate red lines, verify before reporting done |
| `open-source-review` | Pre-publication audit: current content, full git history, and open-source hygiene (license / README / i18n / AI-residue / visual-asset privacy). Review-only; cleanup requires per-item authorization |
| `pm` | PMP-style software project management: PRD-to-plan, RAID, RACI, release readiness, status reporting |
| `setup-workspace` | Bootstrap a new machine for the agentspace harness: clone repos, symlink global agent configs, tool inventory, doctor |
| `skill-admin` | Audit and route skills across agent platforms (agents / Claude / others) with a single source of truth |
| `terminal-workflow` | Terminal toolchain management (Ghostty / Kitty / Zsh / Tmux / Neovim) with config locations and workflows |
| `to-spec` | Turn agreed requirements into a local Markdown implementation spec without publishing tracker items |
| `update-workspace-harness` | Evolve the workspace harness from real failure cases: classify gaps (routing / knowledge / action / loop / workflow), update only the single source of truth |
| `alpha-research` / `beta-research` | Finance research pipelines (fundamentals / event-driven) over public data sources |

## License

MIT
