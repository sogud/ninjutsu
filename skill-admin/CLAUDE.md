# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Skill Admin - CLI tool for managing skills across 20+ AI platforms. Agents and Claude are the default shared domain. OpenClaw, Hermes, and all other platforms remain private unless explicitly selected.

## Commands

```bash
# Run the tool
python3 scripts/skill-admin.py <command>

# Commands
current                   # Show detected runtime and usable skill paths
list [platform]           # Unified list entrypoint; use --current for runtime scope
recommend <query>         # Recommend current-runtime skills for a requirement
guide <query>             # Alias of recommend
scan                      # Alias of list
sync [platform ...]       # Default Agents + Claude; explicit platforms receive one-way shared links
sync-all [platform ...]   # Backward-compatible safe alias
graph [platform]          # Generate skill category graph
topology                  # Show symlink structure
backup                    # Backup all skills
install <url> [platform]  # Install from GitHub
compare <p1> <p2>         # Compare two platforms

# Examples
python3 scripts/skill-admin.py current
python3 scripts/skill-admin.py list --current
python3 scripts/skill-admin.py recommend "修页面样式" --top 5
python3 scripts/skill-admin.py sync
python3 scripts/skill-admin.py sync openclaw
python3 scripts/skill-admin.py graph agents
```

## Architecture

```
~/.agents/skills/          # Single source of truth
    ├── skill-a/           # Real directory
    └── skill-b/           # Real directory

~/.claude/skills/          # Symlinks to .agents
    ├── skill-a -> ../../.agents/skills/skill-a
    └── skill-b -> ../../.agents/skills/skill-b

~/.openclaw/skills/        # Private by default; never imported automatically
~/.hermes/skills/          # Private by default; never imported automatically

# Explicit `sync openclaw` may publish shared links into OpenClaw,
# but OpenClaw-owned real directories never flow back to .agents.
```

## Key Data Structures

**Platform config** (in `PLATFORMS`):
```python
PLATFORMS = {
    "claude": HOME / ".claude/skills",
    "agents": HOME / ".agents/skills",
}
```

**Skill metadata** (from SKILL.md frontmatter):
```yaml
---
name: skill-name
category: automation      # Used by graph command
description: Description
---
```

## Adding New Features

- Add platform to `PLATFORMS`
- Add command handler in `main()`
- Add help text in `show_help()`
- Update SKILL.md with new command docs
