#!/usr/bin/env python3
"""
Skill Admin Web - Zero-dependency web UI for managing skills across AI platforms.

Usage:
  python skill-admin-web.py              # Start on port 8080
  python skill-admin-web.py --port 9000  # Custom port

Dependencies: None (Python 3.8+ stdlib only)
"""

import json
import os
import re
import sys
import shutil
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List
from collections import defaultdict
from urllib.parse import parse_qs, urlparse

# === Shared Configuration ===
HOME = Path.home()
PLATFORMS: Dict[str, Path] = {
    "claude": HOME / ".claude/skills",
    "cursor": HOME / ".cursor/skills",
    "copilot": HOME / ".copilot/skills",
    "vscode": HOME / ".vscode/skills",
    "cline": HOME / ".cline/skills",
    "roo": HOME / ".roo/skills",
    "goose": HOME / ".goose/skills",
    "codex": HOME / ".codex/skills",
    "windsurf": HOME / ".windsurf/skills",
    "trae": HOME / ".trae/skills",
    "kiro": HOME / ".kiro/skills",
    "opencode": HOME / ".opencode/skills",
    "openclaw": HOME / ".openclaw/skills",
    "hermes": HOME / ".hermes/skills",
    "qoder": HOME / ".qoder/skills",
    "qoderwork": HOME / ".qoderwork/skills",
    "gemini": HOME / ".gemini/skills",
    "antigravity": HOME / ".antigravity/skills",
    "agents": HOME / ".agents/skills",
}

DEFAULT_SYNC_PLATFORMS = ("agents", "claude")

# === Backend Logic ===

def _parse_yaml_block(lines, start_idx, indicator):
    """Parse YAML block scalar value given the indicator (>, |, >-, etc.)."""
    folded = indicator.startswith('>')
    chomp_strip = indicator.endswith('-')

    # Collect indented continuation lines
    value_lines = []
    idx = start_idx + 1
    while idx < len(lines):
        line = lines[idx]
        # Block scalar continuation: indented or empty line
        if line == '' or (line and line[0] in (' ', '\t')):
            stripped = line.strip() if line else ''
            value_lines.append(stripped)
            idx += 1
        else:
            break

    # Process value
    if folded:
        # Folded: single newlines become spaces, double newlines = paragraph break
        value = ' '.join(line for line in value_lines if line)
    else:
        # Literal: preserve newlines
        value = '\n'.join(value_lines)

    if chomp_strip:
        value = value.rstrip()

    return value, idx - 1


def _extract_frontmatter(content):
    """Extract frontmatter dict from SKILL.md content, handling block scalars."""
    match = re.match(r'^---\n(.+?)\n---', content, re.DOTALL)
    if not match:
        return {}

    result = {}
    lines = match.group(1).split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if ':' in line:
            key, val = line.split(':', 1)
            key = key.strip()
            val = val.strip()
            if val in ('>', '|', '>-', '|-', '>+', '|+'):
                val, i = _parse_yaml_block(lines, i, val)
            result[key] = val
        i += 1
    return result


def scan_skills(platform: Optional[str] = None) -> List[dict]:
    """Scan skills and return all entries across platforms, no dedup."""
    skills = []
    targets = [platform] if platform else list(PLATFORMS.keys())

    for name in targets:
        if name not in PLATFORMS:
            continue
        path = PLATFORMS[name]
        if not path.exists():
            continue

        for entry in path.iterdir():
            if entry.name.startswith('.') or entry.name == 'node_modules':
                continue
            if not (entry.is_dir() or entry.is_symlink()):
                continue
            skill_md = entry / "SKILL.md"
            if not skill_md.exists():
                continue

            try:
                content = skill_md.read_text()
                fm = _extract_frontmatter(content)
                skill_name = fm.get('name', entry.name)
                desc = fm.get('description', '')
            except:
                skill_name = entry.name
                desc = ''

            skills.append({
                "name": skill_name,
                "dir_name": entry.name,
                "platform": name,
                "path": str(entry),
                "real_path": str(entry.resolve()) if entry.is_symlink() else str(entry),
                "is_symlink": entry.is_symlink(),
                "description": desc,
                "has_skill_md": True,
            })

    return sorted(skills, key=lambda x: (x["platform"], x["name"].lower()))


def get_skill_detail(skill_name: str, platform: str = "agents") -> Optional[dict]:
    """Get full skill details including SKILL.md content."""
    path = PLATFORMS.get(platform)
    if not path:
        return None

    skill_path = path / skill_name
    if not skill_path.exists() and not skill_path.is_symlink():
        # Try resolving symlink
        for name, p in PLATFORMS.items():
            if not p.exists():
                continue
            for entry in p.iterdir():
                if entry.name == skill_name and (entry.is_dir() or entry.is_symlink()):
                    skill_path = entry
                    platform = name
                    break

    if not skill_path.exists() and not skill_path.is_symlink():
        return None

    skill_md = skill_path / "SKILL.md"
    content = ""
    frontmatter = {}

    if skill_md.exists():
        try:
            content = skill_md.read_text()
            frontmatter = _extract_frontmatter(content)
            match = re.match(r'^---\n(.+?)\n---\n?(.*)', content, re.DOTALL)
            if match:
                content = match.group(2)
        except:
            pass

    return {
        "name": skill_name,
        "platform": platform,
        "path": str(skill_path),
        "is_symlink": skill_path.is_symlink(),
        "frontmatter": frontmatter,
        "content": content,
        "full_content": skill_md.read_text() if skill_md.exists() else "",
    }


def create_skill(name: str, platform: str, content: str) -> dict:
    """Create a new skill."""
    path = PLATFORMS.get(platform)
    if not path:
        return {"error": f"Unknown platform: {platform}"}

    skill_dir = path / name
    if skill_dir.exists():
        return {"error": f"Skill '{name}' already exists on {platform}"}

    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(content, encoding='utf-8')

    return {
        "success": True,
        "name": name,
        "platform": platform,
        "path": str(skill_dir),
    }


def update_skill(name: str, platform: str, content: str) -> dict:
    """Update a skill's SKILL.md content."""
    path = PLATFORMS.get(platform)
    if not path:
        return {"error": f"Unknown platform: {platform}"}

    skill_path = path / name
    if not skill_path.exists() and not skill_path.is_symlink():
        return {"error": f"Skill '{name}' not found on {platform}"}

    # Follow symlink to find real path
    if skill_path.is_symlink():
        skill_path = skill_path.resolve()
    elif skill_path.is_dir():
        # It's a real dir
        pass

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return {"error": f"SKILL.md not found for '{name}'"}

    try:
        skill_md.write_text(content, encoding='utf-8')
        return {"success": True, "name": name, "platform": platform}
    except Exception as e:
        return {"error": str(e)}


def delete_skill(name: str, platforms: List[str]) -> dict:
    """Delete a skill from the specified platforms only."""
    deleted = []
    errors = []

    for platform in platforms:
        path = PLATFORMS.get(platform)
        if not path or not path.exists():
            errors.append({"platform": platform, "error": "Platform not found"})
            continue

        skill_path = path / name
        if not skill_path.exists() and not skill_path.is_symlink():
            errors.append({"platform": platform, "error": "Skill not found"})
            continue

        try:
            if skill_path.is_symlink():
                skill_path.unlink()
            else:
                shutil.rmtree(skill_path)
            deleted.append(platform)
        except Exception as e:
            errors.append({"platform": platform, "error": str(e)})

    return {
        "success": True,
        "deleted_from": deleted,
        "errors": errors,
    }


def sync_all() -> dict:
    """Safely sync only the shared Agents/Claude domain."""
    agents_dir = PLATFORMS["agents"]
    claude_dir = PLATFORMS["claude"]
    agents_dir.mkdir(parents=True, exist_ok=True)
    claude_dir.mkdir(parents=True, exist_ok=True)

    copied, linked, cleaned, conflicts = 0, 0, 0, 0
    if claude_dir.resolve() != agents_dir.resolve():
        for skill in list(claude_dir.iterdir()):
            if skill.is_symlink() and not skill.exists():
                skill.unlink()
                cleaned += 1

        for skill in claude_dir.iterdir():
            if skill.is_symlink() or skill.name.startswith('.'):
                continue
            if not skill.is_dir() or not (skill / "SKILL.md").is_file():
                continue
            target = agents_dir / skill.name
            if not target.exists() and not target.is_symlink():
                shutil.copytree(skill, target)
                copied += 1

        for skill in agents_dir.iterdir():
            if skill.name.startswith('.') or not skill.is_dir() or not (skill / "SKILL.md").is_file():
                continue
            link = claude_dir / skill.name
            if link.exists() or link.is_symlink():
                if link.is_symlink() and link.exists() and link.resolve() == skill.resolve():
                    continue
                conflicts += 1
                continue
            relative_target = Path(os.path.relpath(skill, start=claude_dir))
            link.symlink_to(relative_target)
            linked += 1

    return {
        "success": True,
        "scope": list(DEFAULT_SYNC_PLATFORMS),
        "copied": copied,
        "linked": linked,
        "cleaned": cleaned,
        "conflicts": conflicts,
        "isolated_platforms_untouched": sorted(set(PLATFORMS) - set(DEFAULT_SYNC_PLATFORMS)),
    }


def get_platforms_info() -> List[dict]:
    """Get info about all platforms."""
    result = []
    for name, path in PLATFORMS.items():
        info = {
            "name": name,
            "path": str(path),
            "exists": path.exists(),
            "skill_count": 0,
            "real_count": 0,
            "link_count": 0,
        }
        if path.exists():
            for entry in path.iterdir():
                if entry.name.startswith('.'):
                    continue
                if entry.is_dir() and (entry / "SKILL.md").exists():
                    info["skill_count"] += 1
                    if entry.is_symlink():
                        info["link_count"] += 1
                    else:
                        info["real_count"] += 1
        result.append(info)
    return result


def get_delete_info(name: str, platform: str) -> dict:
    """Get delete impact info for confirmation dialog."""
    path = PLATFORMS.get(platform)
    if not path or not path.exists():
        return {"exists": False, "error": f"Platform '{platform}' not found"}

    skill_path = path / name
    if not skill_path.exists() and not skill_path.is_symlink():
        return {"exists": False}

    is_symlink = skill_path.is_symlink()
    info = {
        "exists": True,
        "name": name,
        "platform": platform,
        "is_symlink": is_symlink,
        "will_delete_symlinks": [platform] if is_symlink else [],
        "will_delete_source": not is_symlink,
        "other_platforms_with_symlinks": [],
        "total_affected_platforms": 1,
    }

    if not is_symlink:
        # Check for symlink references
        real_target = skill_path.resolve()
        symlink_users = []
        for op_name, op_path in PLATFORMS.items():
            if op_name == platform or not op_path.exists():
                continue
            op_skill = op_path / name
            if op_skill.is_symlink():
                try:
                    if op_skill.resolve() == real_target:
                        symlink_users.append(op_name)
                except:
                    pass

        info["other_platforms_with_symlinks"] = sorted(symlink_users)
        info["total_affected_platforms"] = 1 + len(symlink_users)

    return info


# === HTTP Handler ===

HTML_PAGE = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Skill Admin</title>
<style>
:root {
  --bg: #0f1117;
  --surface: #1a1d27;
  --surface2: #242836;
  --border: #2e3345;
  --text: #e2e4ed;
  --text2: #8b8fa3;
  --accent: #6c5ce7;
  --accent2: #a29bfe;
  --green: #00b894;
  --red: #e74c3c;
  --yellow: #fdcb6e;
  --radius: 10px;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: var(--bg); color: var(--text); min-height: 100vh; }

/* Header */
.header { background: var(--surface); border-bottom: 1px solid var(--border); padding: 16px 24px; display: flex; align-items: center; justify-content: space-between; position: sticky; top: 0; z-index: 100; }
.header h1 { font-size: 20px; font-weight: 700; display: flex; align-items: center; gap: 10px; }
.header h1 span { font-size: 24px; }
.header-actions { display: flex; gap: 10px; align-items: center; }

/* Stats bar */
.stats-bar { background: var(--surface2); padding: 10px 24px; display: flex; gap: 20px; font-size: 13px; color: var(--text2); border-bottom: 1px solid var(--border); }
.stats-bar .stat { display: flex; align-items: center; gap: 6px; }
.stats-bar .stat b { color: var(--text); }

/* Toolbar */
.toolbar { padding: 16px 24px; display: flex; gap: 12px; flex-wrap: wrap; align-items: center; }
.search-box { flex: 1; min-width: 250px; position: relative; }
.search-box input { width: 100%; padding: 10px 14px 10px 38px; background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); color: var(--text); font-size: 14px; outline: none; transition: border-color .2s; }
.search-box input:focus { border-color: var(--accent); }
.search-box::before { content: '🔍'; position: absolute; left: 12px; top: 50%; transform: translateY(-50%); font-size: 14px; }
.filter-chips { display: flex; gap: 8px; flex-wrap: wrap; }
.chip { padding: 6px 14px; border-radius: 20px; border: 1px solid var(--border); background: transparent; color: var(--text2); cursor: pointer; font-size: 13px; transition: all .2s; }
.chip:hover { border-color: var(--accent); color: var(--text); }
.chip.active { background: var(--accent); border-color: var(--accent); color: #fff; }

/* Buttons */
.btn { padding: 8px 16px; border-radius: var(--radius); border: none; cursor: pointer; font-size: 14px; font-weight: 500; transition: all .2s; display: inline-flex; align-items: center; gap: 6px; }
.btn-primary { background: var(--accent); color: #fff; }
.btn-primary:hover { background: var(--accent2); }
.btn-secondary { background: var(--surface2); color: var(--text); border: 1px solid var(--border); }
.btn-secondary:hover { border-color: var(--accent); }
.btn-danger { background: var(--red); color: #fff; }
.btn-danger:hover { opacity: .85; }
.btn-sm { padding: 5px 10px; font-size: 12px; }

/* Table */
.table-wrap { padding: 0 24px 24px; overflow-x: auto; }
table { width: 100%; border-collapse: collapse; }
th { text-align: left; padding: 12px 16px; font-size: 12px; text-transform: uppercase; color: var(--text2); border-bottom: 1px solid var(--border); font-weight: 600; letter-spacing: .5px; }
td { padding: 12px 16px; border-bottom: 1px solid var(--border); font-size: 14px; vertical-align: middle; }
tr:hover td { background: rgba(108,92,231,.05); }
.skill-name { font-weight: 600; color: var(--accent2); cursor: pointer; }
.skill-name:hover { text-decoration: underline; }
.platform-tag { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; background: var(--surface2); border: 1px solid var(--border); }
.platform-tag.agents { border-color: var(--green); color: var(--green); }
.platform-tag.claude { border-color: var(--accent2); color: var(--accent2); }
.link-badge { font-size: 11px; color: var(--yellow); margin-left: 6px; }
.desc-cell { color: var(--text2); max-width: 400px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.actions-cell { display: flex; gap: 6px; }

/* Modal */
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,.6); z-index: 200; display: none; align-items: center; justify-content: center; }
.modal-overlay.show { display: flex; }
.modal { background: var(--surface); border: 1px solid var(--border); border-radius: 14px; width: 90%; max-width: 800px; max-height: 85vh; display: flex; flex-direction: column; }
.modal-header { padding: 20px 24px; border-bottom: 1px solid var(--border); display: flex; align-items: center; justify-content: space-between; }
.modal-header h2 { font-size: 18px; }
.modal-close { background: none; border: none; color: var(--text2); font-size: 22px; cursor: pointer; padding: 4px 8px; border-radius: 6px; }
.modal-close:hover { background: var(--surface2); color: var(--text); }
.modal-body { padding: 24px; overflow-y: auto; flex: 1; }
.modal-footer { padding: 16px 24px; border-top: 1px solid var(--border); display: flex; gap: 10px; justify-content: flex-end; }

/* Form */
.form-group { margin-bottom: 18px; }
.form-group label { display: block; font-size: 13px; font-weight: 600; margin-bottom: 6px; color: var(--text2); }
.form-group input, .form-group select, .form-group textarea { width: 100%; padding: 10px 14px; background: var(--surface2); border: 1px solid var(--border); border-radius: var(--radius); color: var(--text); font-size: 14px; outline: none; font-family: inherit; }
.form-group input:focus, .form-group select:focus, .form-group textarea:focus { border-color: var(--accent); }
.form-group textarea { font-family: 'SF Mono', 'Fira Code', monospace; font-size: 13px; line-height: 1.6; min-height: 300px; resize: vertical; }

/* Toast */
.toast { position: fixed; bottom: 24px; right: 24px; padding: 12px 20px; border-radius: var(--radius); background: var(--green); color: #fff; font-size: 14px; font-weight: 500; z-index: 300; transform: translateY(100px); opacity: 0; transition: all .3s; }
.toast.show { transform: translateY(0); opacity: 1; }
.toast.error { background: var(--red); }

/* Loading */
.loading { text-align: center; padding: 40px; color: var(--text2); }

/* Platform select in create */
.platform-checkboxes { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 8px; }
.platform-checkbox { display: flex; align-items: center; gap: 8px; padding: 8px 12px; border-radius: 8px; border: 1px solid var(--border); cursor: pointer; font-size: 13px; }
.platform-checkbox:hover { border-color: var(--accent); }
.platform-checkbox input { accent-color: var(--accent); }
.platform-checkbox .count { margin-left: auto; font-size: 11px; color: var(--text2); }

.empty-state { text-align: center; padding: 60px 20px; color: var(--text2); }
.empty-state .icon { font-size: 48px; margin-bottom: 12px; }
.empty-state p { font-size: 15px; }
.delete-info-text { font-size: 14px; line-height: 1.6; margin-bottom: 8px; color: var(--text2); }
.delete-info-text b { color: var(--text); }
.delete-warn { color: var(--red); font-weight: 600; }
.platform-list { display: flex; flex-wrap: wrap; gap: 6px; margin: 8px 0; }
.delete-radio { padding: 12px 14px; border-radius: 8px; border: 1px solid var(--border); margin-bottom: 8px; cursor: pointer; transition: border-color .2s; }
.delete-radio:hover { border-color: var(--accent); }
.delete-radio input { accent-color: var(--red); margin-right: 10px; }
.delete-radio label { cursor: pointer; font-size: 13px; color: var(--text); }
.delete-radio label b { font-weight: 600; }
</style>
</head>
<body>

<div class="header">
  <h1><span>🛠️</span> Skill Admin</h1>
  <div class="header-actions">
    <button class="btn btn-secondary" onclick="syncAll()">🔄 Sync Agents + Claude</button>
    <button class="btn btn-primary" onclick="openCreateModal()">+ New Skill</button>
  </div>
</div>

<div class="stats-bar" id="statsBar">Loading...</div>

<div class="toolbar">
  <div class="search-box">
    <input type="text" id="searchInput" placeholder="Search skills by name, description, or platform..." oninput="filterSkills()">
  </div>
  <div class="filter-chips" id="filterChips">
    <button class="chip active" data-filter="all" onclick="setFilter(this)">All</button>
  </div>
</div>

<div class="table-wrap">
  <div id="loading" class="loading">Loading skills...</div>
  <table id="skillsTable" style="display:none;">
    <thead>
      <tr>
        <th>Skill Name</th>
        <th>Description</th>
        <th>Platform</th>
        <th>Type</th>
        <th style="width:160px">Actions</th>
      </tr>
    </thead>
    <tbody id="skillsBody"></tbody>
  </table>
  <div id="emptyState" class="empty-state" style="display:none;">
    <div class="icon">📦</div>
    <p>No skills found. Try a different search or create a new one.</p>
  </div>
</div>

<!-- View/Edit Modal -->
<div class="modal-overlay" id="editModal">
  <div class="modal">
    <div class="modal-header">
      <h2 id="editModalTitle">Edit Skill</h2>
      <button class="modal-close" onclick="closeModal('editModal')">&times;</button>
    </div>
    <div class="modal-body">
      <div class="form-group">
        <label>SKILL.md Content</label>
        <textarea id="skillContent" spellcheck="false"></textarea>
      </div>
      <input type="hidden" id="editSkillName">
      <input type="hidden" id="editSkillPlatform">
    </div>
    <div class="modal-footer">
      <button class="btn btn-secondary" onclick="closeModal('editModal')">Cancel</button>
      <button class="btn btn-primary" onclick="saveSkill()">💾 Save</button>
    </div>
  </div>
</div>

<!-- Create Modal -->
<div class="modal-overlay" id="createModal">
  <div class="modal">
    <div class="modal-header">
      <h2>Create New Skill</h2>
      <button class="modal-close" onclick="closeModal('createModal')">&times;</button>
    </div>
    <div class="modal-body">
      <div class="form-group">
        <label>Skill Name</label>
        <input type="text" id="createSkillName" placeholder="my-awesome-skill">
      </div>
      <div class="form-group">
        <label>Target Platform</label>
        <select id="createSkillPlatform">
          <option value="agents">.agents (Recommended)</option>
          <option value="claude">Claude Code</option>
          <option value="cursor">Cursor</option>
          <option value="copilot">GitHub Copilot</option>
          <option value="vscode">VSCode</option>
          <option value="cline">Cline</option>
          <option value="roo">Roo</option>
          <option value="gemini">Gemini</option>
        </select>
      </div>
      <div class="form-group">
        <label>SKILL.md Content</label>
        <textarea id="createSkillContent" spellcheck="false" placeholder='---
name: my-awesome-skill
description: What this skill does
---

# Instructions
Your skill instructions here...'></textarea>
      </div>
    </div>
    <div class="modal-footer">
      <button class="btn btn-secondary" onclick="closeModal('createModal')">Cancel</button>
      <button class="btn btn-primary" onclick="createSkill()">✨ Create</button>
    </div>
  </div>
</div>

<!-- Delete Confirmation Modal -->
<div class="modal-overlay" id="deleteModal">
  <div class="modal">
    <div class="modal-header">
      <h2>⚠️ Delete Skill</h2>
      <button class="modal-close" onclick="closeModal('deleteModal')">&times;</button>
    </div>
    <div class="modal-body">
      <p style="margin-bottom:12px;">Delete <b id="deleteSkillName"></b> from <b id="deleteSkillPlatform"></b>?</p>
      <div id="deleteDetails"></div>
      <div id="deleteOptions" style="margin-top:16px;"></div>
    </div>
    <div class="modal-footer">
      <button class="btn btn-secondary" onclick="closeModal('deleteModal')">Cancel</button>
      <button class="btn btn-danger" id="deleteConfirmBtn">🗑️ Delete</button>
    </div>
  </div>
</div>

<div class="toast" id="toast"></div>

<script>
let allSkills = [];
let currentFilter = 'all';

async function api(path, method = 'GET', body = null) {
  const opts = { method, headers: { 'Content-Type': 'application/json' } };
  if (body) opts.body = JSON.stringify(body);
  const res = await fetch('/api' + path, opts);
  return res.json();
}

function showToast(msg, isError = false) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.className = 'toast show' + (isError ? ' error' : '');
  setTimeout(() => t.className = 'toast', 3000);
}

function openModal(id) { document.getElementById(id).classList.add('show'); }
function closeModal(id) { document.getElementById(id).classList.remove('show'); }

async function loadSkills() {
  try {
    allSkills = await api('/skills');
    buildFilterChips();
    updateStats();
    filterSkills();
    document.getElementById('loading').style.display = 'none';
    document.getElementById('skillsTable').style.display = 'table';
  } catch (e) {
    document.getElementById('loading').textContent = 'Failed to load: ' + e.message;
  }
}

function updateStats() {
  const unique = new Set(allSkills.map(s => s.name));
  const platforms = [...new Set(allSkills.map(s => s.platform))];
  const symlinks = allSkills.filter(s => s.is_symlink).length;
  const primary = allSkills.filter(s => !s.is_symlink).length;
  document.getElementById('statsBar').innerHTML =
    `<div class="stat">📦 Unique skills: <b>${unique.size}</b></div>
     <div class="stat">📁 Real: <b>${primary}</b> | 🔗 Symlinks: <b>${symlinks}</b></div>
     <div class="stat">🖥️ Active platforms: <b>${platforms.length}</b></div>
     <div class="stat">📊 Total entries: <b>${allSkills.length}</b></div>`;
}

function buildFilterChips() {
  const platforms = [...new Set(allSkills.map(s => s.platform))].sort();
  const container = document.getElementById('filterChips');
  container.innerHTML = `<button class="chip ${currentFilter === 'all' ? 'active' : ''}" onclick="setFilter(this)" data-filter="all">All</button>`;
  for (const p of platforms) {
    container.innerHTML += `<button class="chip ${currentFilter === p ? 'active' : ''}" onclick="setFilter(this)" data-filter="${p}">${p}</button>`;
  }
}

function setFilter(el) {
  currentFilter = el.dataset.filter;
  document.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
  el.classList.add('active');
  filterSkills();
}

function filterSkills() {
  const q = document.getElementById('searchInput').value.toLowerCase().trim();
  let filtered = allSkills;
  if (currentFilter !== 'all') {
    filtered = filtered.filter(s => s.platform === currentFilter);
  }
  if (q) {
    filtered = filtered.filter(s =>
      s.name.toLowerCase().includes(q) ||
      s.description.toLowerCase().includes(q) ||
      s.platform.toLowerCase().includes(q)
    );
  }
  renderSkills(filtered);
}

function renderSkills(skills) {
  skills = skills || allSkills;
  const body = document.getElementById('skillsBody');
  const empty = document.getElementById('emptyState');
  const table = document.getElementById('skillsTable');

  if (!skills.length) {
    table.style.display = 'none';
    empty.style.display = 'block';
    return;
  }

  empty.style.display = 'none';
  table.style.display = 'table';

  body.innerHTML = skills.map(s => `
    <tr>
      <td><span class="skill-name" onclick="openEditModal('${s.name}','${s.platform}')">${s.name}</span></td>
      <td class="desc-cell" title="${s.description.replace(/"/g, '&quot;')}">${s.description || '—'}</td>
      <td><span class="platform-tag ${s.platform}">${s.platform}</span></td>
      <td>${s.is_symlink ? '🔗 link' : '📁 real'}</td>
      <td class="actions-cell">
        <button class="btn btn-sm btn-secondary" onclick="openEditModal('${s.name}','${s.platform}')">✏️ Edit</button>
        <button class="btn btn-sm btn-danger" onclick="confirmDelete('${s.name}','${s.platform}')">🗑️</button>
      </td>
    </tr>
  `).join('');
}

function openEditModal(name, platform) {
  document.getElementById('editModalTitle').textContent = `Edit: ${name}`;
  document.getElementById('editSkillName').value = name;
  document.getElementById('editSkillPlatform').value = platform;
  document.getElementById('skillContent').value = 'Loading...';
  openModal('editModal');

  api(`/skills/${encodeURIComponent(name)}?platform=${encodeURIComponent(platform)}`)
    .then(data => {
      if (data.error) {
        document.getElementById('skillContent').value = 'Error: ' + data.error;
        return;
      }
      document.getElementById('skillContent').value = data.full_content || data.content || '';
    });
}

async function saveSkill() {
  const name = document.getElementById('editSkillName').value;
  const platform = document.getElementById('editSkillPlatform').value;
  const content = document.getElementById('skillContent').value;

  const res = await api(`/skills/${encodeURIComponent(name)}`, 'PUT', { platform, content });
  if (res.error) {
    showToast(res.error, true);
    return;
  }
  closeModal('editModal');
  showToast('Skill updated!');
  loadSkills();
}

function openCreateModal() {
  document.getElementById('createSkillName').value = '';
  document.getElementById('createSkillContent').value = `---
name: 
description: 
---

# Instructions

`;
  openModal('createModal');
}

async function createSkill() {
  const name = document.getElementById('createSkillName').value.trim();
  const platform = document.getElementById('createSkillPlatform').value;
  const content = document.getElementById('createSkillContent').value;

  if (!name) { showToast('Please enter a skill name', true); return; }

  const res = await api('/skills', 'POST', { name, platform, content });
  if (res.error) {
    showToast(res.error, true);
    return;
  }
  closeModal('createModal');
  showToast(`Skill "${name}" created!`);
  loadSkills();
}

async function confirmDelete(name, platform) {
  const info = await api(`/skills/${encodeURIComponent(name)}/delete-info?platform=${encodeURIComponent(platform)}`);
  if (!info.exists) { showToast('Skill not found', true); return; }

  document.getElementById('deleteSkillName').textContent = name;
  document.getElementById('deleteSkillPlatform').textContent = platform;

  const detail = document.getElementById('deleteDetails');
  const options = document.getElementById('deleteOptions');
  const btn = document.getElementById('deleteConfirmBtn');

  if (info.is_symlink) {
    // Simple: just a symlink, no options needed
    detail.innerHTML = `<p class="delete-info-text">This is a <b>symlink</b> on <b>${platform}</b>. Only the symlink will be removed.</p>`;
    options.innerHTML = '';
    btn.textContent = '🗑️ Delete Symlink';
    btn.className = 'btn btn-danger';
    btn.onclick = () => {
      closeModal('deleteModal');
      doDelete(name, [platform]);
    };
  } else if (info.other_platforms_with_symlinks.length > 0) {
    // Real source with symlink references → show options
    const count = info.other_platforms_with_symlinks.length;
    detail.innerHTML = `<p class="delete-info-text delete-warn">⚠️ This is the <b>real source</b> on <b>${platform}</b>.</p>
      <p class="delete-info-text">Found <b>${count} symlink(s)</b> on: ${info.other_platforms_with_symlinks.map(p => `<span class="platform-tag">${p}</span>`).join(' ')}</p>`;

    options.innerHTML = `
      <div class="delete-radio" onclick="setDeleteMode('all')">
        <input type="radio" name="deleteMode" value="all" id="modeAll" checked>
        <label for="modeAll"><b>Delete from all platforms</b> — remove source + all ${count} symlinks</label>
      </div>
      <div class="delete-radio" onclick="setDeleteMode('this')">
        <input type="radio" name="deleteMode" value="this" id="modeThis">
        <label for="modeThis"><b>Only delete from ${platform}</b> — remove source, symlinks become broken</label>
      </div>`;
    btn.textContent = '🗑️ Delete';
    btn.className = 'btn btn-danger';
    btn.onclick = () => {
      const mode = document.getElementById('modeAll').checked ? 'all' : 'this';
      closeModal('deleteModal');
      doDelete(name, mode === 'all' ? [platform, ...info.other_platforms_with_symlinks] : [platform]);
    };
  } else {
    // Real source, no symlinks
    detail.innerHTML = `<p class="delete-info-text delete-warn">⚠️ This is a <b>real skill directory</b>. Deleting will remove the source files.</p>`;
    options.innerHTML = '';
    btn.textContent = '🗑️ Delete';
    btn.className = 'btn btn-danger';
    btn.onclick = () => {
      closeModal('deleteModal');
      doDelete(name, [platform]);
    };
  }

  openModal('deleteModal');
}

function setDeleteMode(mode) {
  document.getElementById(mode === 'all' ? 'modeAll' : 'modeThis').checked = true;
}

async function doDelete(name, platforms) {
  const res = await api(`/skills/${encodeURIComponent(name)}`, 'DELETE', { platforms });
  if (res.error) { showToast(res.error, true); return; }
  showToast(`Deleted "${name}" from ${res.deleted_from.join(', ')}`);
  loadSkills();
}

async function syncAll() {
  if (!confirm('Sync shared skills between Agents and Claude? Other platforms remain isolated.')) return;
  const res = await api('/sync', 'POST');
  if (res.error) { showToast(res.error, true); return; }
  showToast(`Agents + Claude synced: ${res.copied} copied, ${res.linked} linked`);
  loadSkills();
}

// Close modal on overlay click
document.querySelectorAll('.modal-overlay').forEach(m => {
  m.addEventListener('click', e => { if (e.target === m) closeModal(m.id); });
});

// Escape key
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') document.querySelectorAll('.modal-overlay.show').forEach(m => closeModal(m.id));
});

loadSkills();
</script>
</body>
</html>
"""


class SkillAdminHandler(SimpleHTTPRequestHandler):
    """HTTP handler for Skill Admin Web UI."""

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == '/' or path == '/index.html':
            self._send_html()
            return

        if path == '/api/skills':
            platform = parse_qs(parsed.query).get('platform', [None])[0]
            skills = scan_skills(platform)
            self._send_json(skills)
            return

        # DELETE pre-check (must be before /api/skills/ detail handler)
        if path.endswith('/delete-info'):
            name = path.split('/api/skills/')[1].replace('/delete-info', '')
            platform = parse_qs(parsed.query).get('platform', ['agents'])[0]
            info = get_delete_info(name, platform)
            self._send_json(info)
            return

        if path.startswith('/api/skills/'):
            name = path.split('/api/skills/')[1]
            platform = parse_qs(parsed.query).get('platform', ['agents'])[0]
            detail = get_skill_detail(name, platform)
            if detail:
                self._send_json(detail)
            else:
                self._send_json({"error": "Skill not found"}, 404)
            return

        if path == '/api/platforms':
            self._send_json(get_platforms_info())
            return

        # Serve static files from scripts dir (if any)
        super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length else b'{}'

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self._send_json({"error": "Invalid JSON"}, 400)
            return

        if path == '/api/skills':
            name = data.get('name', '')
            platform = data.get('platform', 'agents')
            content = data.get('content', '')
            result = create_skill(name, platform, content)
            if 'error' in result:
                self._send_json(result, 400)
            else:
                self._send_json(result)
            return

        if path == '/api/sync':
            self._send_json(sync_all())
            return

        self._send_json({"error": "Not found"}, 404)

    def do_PUT(self):
        parsed = urlparse(self.path)
        path = parsed.path
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length else b'{}'

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self._send_json({"error": "Invalid JSON"}, 400)
            return

        if path.startswith('/api/skills/'):
            name = path.split('/api/skills/')[1]
            platform = data.get('platform', 'agents')
            content = data.get('content', '')
            result = update_skill(name, platform, content)
            if 'error' in result:
                self._send_json(result, 400)
            else:
                self._send_json(result)
            return

        self._send_json({"error": "Not found"}, 404)

    def do_DELETE(self):
        parsed = urlparse(self.path)
        path = parsed.path
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length else b'{}'

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            data = {}

        if path.startswith('/api/skills/'):
            name = path.split('/api/skills/')[1]
            platforms = data.get('platforms', [])
            if not platforms:
                self._send_json({"error": "No platforms specified"}, 400)
                return
            result = delete_skill(name, platforms)
            self._send_json(result)
            return

        self._send_json({"error": "Not found"}, 404)

    def _send_html(self):
        html = HTML_PAGE.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', len(html))
        self.end_headers()
        self.wfile.write(html)

    def _send_json(self, data: dict, status: int = 200):
        body = json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        """Custom log format."""
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"[{timestamp}] {format % args}")


def main():
    port = 8080
    if '--port' in sys.argv:
        idx = sys.argv.index('--port')
        if idx + 1 < len(sys.argv):
            try:
                port = int(sys.argv[idx + 1])
            except ValueError:
                print(f"Invalid port: {sys.argv[idx + 1]}")
                sys.exit(1)

    if '--help' in sys.argv or '-h' in sys.argv:
        print("Usage: python skill-admin-web.py [--port PORT]")
        print()
        print("Options:")
        print("  --port PORT    Port to listen on (default: 8080)")
        print("  --help, -h     Show this help message")
        return

    server = HTTPServer(('0.0.0.0', port), SkillAdminHandler)
    url = f"http://localhost:{port}"

    print(f"")
    print(f"  🛠️  Skill Admin Web")
    print(f"  ====================")
    print(f"  Server running at: {url}")
    print(f"  Press Ctrl+C to stop")
    print(f"")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print(f"\n\n  👋 Shutting down...")
        server.server_close()


if __name__ == '__main__':
    main()
