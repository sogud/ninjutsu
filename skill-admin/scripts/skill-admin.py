#!/usr/bin/env python3
"""
Skill Admin - Manage skills across 20+ AI platforms.
Usage: python skill-admin.py <command> [args]

Dependencies: None (stdlib only)
Python: 3.8+ required (pathlib, shutil, tarfile, urllib)
"""

import os
import re
import sys
import shutil
import tarfile
import subprocess
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Set, Tuple
from collections import defaultdict

# Configuration
HOME = Path.home()
PLATFORMS: Dict[str, Path] = {
    # Mainstream AI coding assistants
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
    # AI agent platforms
    "qoder": HOME / ".qoder/skills",
    "qoderwork": HOME / ".qoderwork/skills",
    "gemini": HOME / ".gemini/skills",
    "antigravity": HOME / ".antigravity/skills",
    "agents": HOME / ".agents/skills",
}

DEFAULT_SYNC_PLATFORMS: Tuple[str, ...] = ("agents", "claude")
PLATFORM_PRIVATE_BY_DEFAULT: Set[str] = set(PLATFORMS) - set(DEFAULT_SYNC_PLATFORMS)

RUNTIME_PROFILES: Dict[str, Dict[str, object]] = {
    # Pi intentionally recommends only skills available through .agents.
    "pi": {"display": "Pi", "platforms": ["agents"], "signals": ["PI_CODING_AGENT"]},
    "claude": {
        "display": "Claude Code",
        "platforms": ["claude"],
        "signals": ["CLAUDE_CODE", "CLAUDECODE", "CLAUDE_PROJECT_DIR"],
    },
    "cursor": {"display": "Cursor", "platforms": ["cursor"], "signals": ["CURSOR_TRACE_ID", "CURSOR_AGENT"]},
    "codex": {"display": "Codex", "platforms": ["codex"], "signals": ["CODEX_SANDBOX", "OPENAI_CODEX"]},
    "gemini": {"display": "Gemini", "platforms": ["gemini"], "signals": ["GEMINI_CLI"]},
    "hermes": {"display": "Hermes", "platforms": ["hermes"], "signals": ["HERMES_AGENT"]},
    "opencode": {"display": "OpenCode", "platforms": ["opencode"], "signals": ["OPENCODE"]},
    # Conservative fallback: do not recommend across every installed platform.
    "agents": {"display": ".agents default", "platforms": ["agents"], "signals": []},
}

CURRENT_PLATFORM_ALIASES = {"current", "--current"}
DESCRIPTION_KEYS = {"description", "description_zh"}
BLOCK_SCALAR_MARKERS = {"", ">", ">-", "|", "|-"}
ASCII_TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9_-]*")
ASCII_TRIGGER_RE = re.compile(r"^[a-z0-9_-]+$")

RECOMMEND_EXPANSIONS: List[Tuple[Tuple[str, ...], Tuple[str, ...], str]] = [
    (("调试", "排错", "报错", "错误", "失败", "bug", "debug", "broken", "crash"),
     ("debug", "diagnose", "error", "recovery", "hunt", "investigate", "qa", "test", "devtools"),
     "调试/排错"),
    (("网页", "页面", "浏览器", "dom", "截图", "点击", "表单", "browser", "web", "screenshot"),
     ("browser", "web", "devtools", "opencli", "playwright", "screenshot", "frontend", "visual"),
     "浏览器/页面"),
    (("ui", "ux", "界面", "样式", "设计稿", "视觉", "还原", "布局", "figma", "design"),
     ("ui", "ux", "frontend", "visual", "repair", "design", "figma", "web-design"),
     "UI/视觉"),
    (("文档", "文章", "写作", "改写", "润色", "docs", "doc", "writing", "article", "guide"),
     ("doc", "docs", "document", "writing", "article", "guide", "obsidian", "pdf", "docx"),
     "文档/写作"),
    (("计划", "方案", "prd", "需求", "issue", "拆解", "plan", "proposal"),
     ("plan", "prd", "issue", "triage", "proposal", "refactor", "architecture"),
     "计划/需求"),
    (("代码审查", "review", "质量", "安全", "漏洞", "security", "hardening"),
     ("review", "quality", "security", "hardening", "guard", "lint"),
     "质量/安全"),
    (("数据", "查询", "sql", "报表", "分析", "odps", "data", "analytics"),
     ("data", "query", "sql", "odps", "analytics", "finance", "stock", "rum"),
     "数据/分析"),
    (("估值", "dcf", "intrinsic", "fair value", "valuation"),
     ("valuation", "company-valuation", "dcf", "intrinsic", "sotp", "fair value"),
     "估值"),
    (("股票", "财报", "期权", "金融", "stock", "finance", "earnings", "options"),
     ("stock", "finance", "earnings", "valuation", "options", "yfinance", "trading", "market"),
     "金融/市场"),
    (("会议室", "订会议室", "book room", "meeting room"),
     ("book-room", "会议室", "book meeting room", "meeting room", "room"),
     "会议室"),
    (("钉钉", "会议", "日程", "审批", "员工", "ding", "dingtalk"),
     ("ding", "dingtalk", "dws", "calendar", "meeting", "approval", "employee"),
     "办公协作"),
    (("技能", "skill", "用什么技能", "推荐技能", "哪个技能"),
     ("skill", "admin", "find-skills"),
     "技能管理"),
]

# ANSI colors
class Color:
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    CYAN = "\033[0;36m"
    RESET = "\033[0m"

def print_info(msg: str) -> None:
    print(f"{Color.CYAN}[INFO]{Color.RESET} {msg}")

def print_success(msg: str) -> None:
    print(f"{Color.GREEN}[SUCCESS]{Color.RESET} {msg}")

def print_error(msg: str) -> None:
    print(f"{Color.RED}[ERROR]{Color.RESET} {msg}")


def clean_field(value: object, max_len: Optional[int] = None) -> str:
    """Clean values for stable tab-separated CLI output."""
    text = str(value or "").replace("\t", " ").replace("\n", " ").strip()
    text = re.sub(r"\s+", " ", text)
    if max_len and len(text) > max_len:
        return text[: max_len - 1].rstrip() + "…"
    return text


def is_frontmatter_key(line: str) -> bool:
    return bool(line and not line.startswith((' ', '\t')) and ':' in line)


def read_frontmatter_block(lines: List[str], start: int) -> Tuple[str, int]:
    block: List[str] = []
    index = start
    while index < len(lines) and not is_frontmatter_key(lines[index]):
        block.append(lines[index].strip())
        index += 1
    return ' '.join(part for part in block if part).strip().strip('"\''), index


def read_skill_metadata(skill_md: Path, default_name: str, description_limit: Optional[int] = 500) -> Dict[str, str]:
    """Read name/description/category from SKILL.md frontmatter only."""
    metadata = {"name": default_name, "description": "", "category": "general"}
    try:
        content = skill_md.read_text(encoding="utf-8", errors="ignore")
        match = re.match(r'^---\n(.+?)\n---', content, re.DOTALL)
        if not match:
            return metadata

        lines = match.group(1).splitlines()
        i = 0
        while i < len(lines):
            line = lines[i]
            if not is_frontmatter_key(line):
                i += 1
                continue

            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip().strip('"\'')

            if key in DESCRIPTION_KEYS and value in BLOCK_SCALAR_MARKERS:
                value, i = read_frontmatter_block(lines, i + 1)
                if value:
                    metadata["description"] = clean_field(value, description_limit)
                continue

            if key == 'name' and value:
                metadata["name"] = value
            elif key in DESCRIPTION_KEYS and value:
                metadata["description"] = clean_field(value, description_limit)
            elif key == 'category' and value:
                metadata["category"] = value
            i += 1
    except Exception:
        pass
    return metadata


def detect_current_runtime() -> str:
    """Detect the runtime asking for help; fallback to .agents-only scope."""
    for runtime, profile in RUNTIME_PROFILES.items():
        signals = profile.get("signals", [])
        if any(os.environ.get(signal) for signal in signals):
            return runtime
    return "agents"


def get_current_profile() -> Dict[str, object]:
    runtime = detect_current_runtime()
    profile = dict(RUNTIME_PROFILES.get(runtime, RUNTIME_PROFILES["agents"]))
    profile["id"] = runtime
    return profile


def profile_platforms(profile: Dict[str, object]) -> List[str]:
    return [p for p in profile.get("platforms", []) if p in PLATFORMS]


def current_platform_filter() -> Tuple[List[str], str, Dict[str, object]]:
    profile = get_current_profile()
    return profile_platforms(profile), f"current:{profile.get('id')}", profile


def resolve_platform_filter(platform: Optional[str], default_all: bool) -> Tuple[List[str], str, Dict[str, object]]:
    """Resolve list/recommend platform input into concrete platform keys."""
    profile: Dict[str, object] = {}

    if platform in CURRENT_PLATFORM_ALIASES:
        return current_platform_filter()

    if not platform:
        if default_all:
            return list(PLATFORMS.keys()), "all", profile
        return current_platform_filter()

    if platform == "all":
        return list(PLATFORMS.keys()), "all", profile

    if platform not in PLATFORMS:
        print_error(f"Unknown platform: {platform}")
        return [], platform, profile

    return [platform], platform, profile


def collect_skills(target_platforms: List[str]) -> Dict[str, object]:
    """Collect skills and platform stats for the selected platform keys."""
    skills: List[Dict[str, object]] = []
    platform_stats = defaultdict(lambda: {"real": set(), "links": set()})
    unique_real_paths = set()

    for plat_name in target_platforms:
        path = PLATFORMS[plat_name]
        if not path.exists():
            continue

        for entry in path.iterdir():
            if entry.name.startswith('.') or entry.name == 'node_modules':
                continue
            if not entry.is_dir():
                continue

            skill_md = entry / "SKILL.md"
            if not skill_md.exists():
                continue

            real_path = entry.resolve()
            unique_real_paths.add(str(real_path))

            source = identify_source(entry)
            is_symlink = entry.is_symlink()

            stats_key = "links" if is_symlink else "real"
            platform_stats[source][stats_key].add(entry.name)

            metadata = read_skill_metadata(skill_md, entry.name)
            skills.append({
                "name": metadata["name"],
                "path": entry,
                "real_path": real_path,
                "desc": metadata["description"],
                "source": source,
                "platform_key": plat_name,
                "is_symlink": is_symlink,
            })

    platform_totals = {}
    for source, stats in platform_stats.items():
        total = len(stats["real"]) + len(stats["links"])
        if total > 0:
            platform_totals[source] = {
                "total": total,
                "real": len(stats["real"]),
                "links": len(stats["links"]),
            }

    return {
        "skills": skills,
        "platform_totals": platform_totals,
        "unique_real_paths": unique_real_paths,
    }


# === Commands ===

def list_skills(platform: Optional[str] = None) -> int:
    """Unified list command with AI-friendly structured output."""
    target_platforms, filter_label, _profile = resolve_platform_filter(platform, default_all=True)
    if not target_platforms:
        return 1

    print_info("Listing skills across platforms...\n")

    inventory = collect_skills(target_platforms)
    skills = inventory["skills"]
    platform_totals = inventory["platform_totals"]
    total_unique = len(inventory["unique_real_paths"])

    by_source = defaultdict(list)
    for skill in skills:
        by_source[skill["source"]].append(skill)

    sorted_platforms = sorted(platform_totals.items(), key=lambda x: (-x[1]["total"], x[0]))

    print("SKILL_LIST_BEGIN")
    print(f"SUMMARY\tunique_skills={total_unique}\tplatforms={len(platform_totals)}\tfilter={filter_label}")

    for source, stats in sorted_platforms:
        source_skills = sorted(by_source.get(source, []), key=lambda x: x["name"])
        real_count = stats["real"]
        links_count = stats["links"]
        total_count = stats["total"]
        unique_count = len(source_skills)

        print(
            f"PLATFORM\tname={source}\ttotal={total_count}\treal={real_count}\tlinks={links_count}\tunique={unique_count}"
        )

        for skill in source_skills:
            skill_type = "link" if skill["is_symlink"] else "real"
            desc = clean_field(skill["desc"], 160)
            print(
                f"SKILL\tplatform={source}\tname={skill['name']}\ttype={skill_type}\tpath={skill['path']}\tdescription={desc}"
            )

    print("SKILL_LIST_END")

    return 0


def show_current() -> int:
    """Show the current runtime and the skill paths considered usable."""
    profile = get_current_profile()
    platform_keys = profile_platforms(profile)
    inventory = collect_skills(platform_keys)

    print("CURRENT_PLATFORM_BEGIN")
    print(
        f"RUNTIME\tid={profile.get('id')}\tdisplay={clean_field(profile.get('display'))}\tplatforms={','.join(platform_keys)}"
    )
    for platform_key in platform_keys:
        path = PLATFORMS[platform_key]
        print(
            f"USABLE_PATH\tplatform={platform_key}\tpath={path}\texists={str(path.exists()).lower()}"
        )
    print(f"SUMMARY\tskill_count={len(inventory['skills'])}\tunique_skills={len(inventory['unique_real_paths'])}")
    print("CURRENT_PLATFORM_END")
    return 0


def tokenize_query(query: str) -> List[str]:
    """ASCII tokenization; Chinese matching is handled by RECOMMEND_EXPANSIONS."""
    return ASCII_TOKEN_RE.findall(query.lower())


def query_has_trigger(query_lower: str, query_tokens: Set[str], trigger: str) -> bool:
    trigger_lower = trigger.lower()
    if ASCII_TRIGGER_RE.match(trigger_lower):
        return trigger_lower in query_tokens
    return trigger_lower in query_lower


def score_skill_for_query(skill: Dict[str, object], query: str) -> Tuple[int, List[str]]:
    """Score a skill using only its name and frontmatter description."""
    name = clean_field(skill.get("name")).lower()
    desc = clean_field(skill.get("desc")).lower()
    haystack = f"{name} {desc}"
    query_lower = query.lower()
    query_tokens = set(tokenize_query(query))
    score = 0
    matched: List[str] = []

    if name and name in query_lower:
        score += 60
        matched.append("技能名直接命中")

    for token in query_tokens:
        if len(token) < 2:
            continue
        if token == name:
            score += 45
            matched.append(token)
        elif token in name:
            score += 22
            matched.append(token)
        elif token in desc:
            score += 8
            matched.append(token)

    for triggers, terms, label in RECOMMEND_EXPANSIONS:
        if not any(query_has_trigger(query_lower, query_tokens, trigger) for trigger in triggers):
            continue
        local_score = 0
        for term in terms:
            term_lower = term.lower()
            if term_lower in name:
                local_score += 18
            elif term_lower in haystack:
                local_score += 7
        if local_score > 0:
            score += min(local_score, 35)
            matched.append(label)

    # Prefer skills whose names are concise and specific when scores tie.
    if score > 0 and len(name) <= 24:
        score += 2

    return score, sorted(set(matched))


def recommendation_reason(matched: List[str], description: str) -> str:
    if not matched:
        return description or "技能名称或描述与需求相近"

    prefix = f"匹配：{', '.join(matched[:4])}"
    return f"{prefix}；{description}" if description else prefix


def recommend_skills(query: str, platform: Optional[str] = None, top: int = 5) -> Dict[str, object]:
    """Return ranked skill recommendations scoped to the selected/current runtime."""
    target_platforms, filter_label, profile = resolve_platform_filter(platform, default_all=False)
    if not target_platforms:
        return {"ok": False, "error": "unknown platform", "recommendations": []}

    inventory = collect_skills(target_platforms)
    ranked: List[Dict[str, object]] = []
    seen_names: Set[str] = set()

    for skill in inventory["skills"]:
        name_key = clean_field(skill.get("name")).lower()
        if name_key in seen_names:
            continue
        seen_names.add(name_key)

        score, matched = score_skill_for_query(skill, query)
        if score <= 0:
            continue
        description = clean_field(skill.get("desc"), 180)
        reason = recommendation_reason(matched, description)

        ranked.append({
            "name": skill["name"],
            "score": score,
            "reason": reason,
            "description": description,
            "path": skill["path"],
            "platform": skill["source"],
        })

    ranked.sort(key=lambda item: (-int(item["score"]), str(item["name"])))
    top = max(1, min(top, 20))

    return {
        "ok": True,
        "query": query,
        "filter": filter_label,
        "runtime": profile.get("id", "explicit") if profile else "explicit",
        "runtime_display": profile.get("display", "explicit platform") if profile else "explicit platform",
        "usable_skills": len(inventory["skills"]),
        "unique_skills": len(inventory["unique_real_paths"]),
        "recommendations": ranked[:top],
    }


def parse_recommend_args(args: List[str]) -> Tuple[str, str, int]:
    platform = "current"
    top = 5
    query_parts: List[str] = []
    i = 0
    while i < len(args):
        arg = args[i]
        if arg in ("--platform", "-p"):
            if i + 1 >= len(args):
                raise ValueError("--platform requires a value")
            platform = args[i + 1]
            i += 2
        elif arg in ("--top", "-n"):
            if i + 1 >= len(args):
                raise ValueError("--top requires a value")
            top = int(args[i + 1])
            i += 2
        else:
            query_parts.append(arg)
            i += 1

    query = " ".join(query_parts).strip()
    if not query:
        raise ValueError("Usage: recommend <需求描述> [--platform current|agents|claude|all] [--top N]")
    return query, platform, top


def recommend_command(args: List[str]) -> int:
    try:
        query, platform, top = parse_recommend_args(args)
    except ValueError as exc:
        print_error(str(exc))
        return 1

    result = recommend_skills(query, platform, top)
    if not result.get("ok"):
        return 1

    print("SKILL_RECOMMEND_BEGIN")
    print(
        f"CONTEXT\truntime={clean_field(result['runtime'])}\truntime_display={clean_field(result['runtime_display'])}"
        f"\tfilter={clean_field(result['filter'])}\tquery={clean_field(result['query'])}"
        f"\tusable_skills={result['usable_skills']}\tunique_skills={result['unique_skills']}\ttop={top}"
    )

    recommendations = result["recommendations"]
    if not recommendations:
        print("NO_MATCH\tmessage=当前可用技能里没有明显匹配；可以直接用普通对话/代码模式处理，或换个需求描述重试")
    else:
        for index, rec in enumerate(recommendations, start=1):
            print(
                f"RECOMMEND\trank={index}\tname={clean_field(rec['name'])}\tscore={rec['score']}"
                f"\tplatform={clean_field(rec['platform'])}\tpath={clean_field(rec['path'])}"
                f"\treason={clean_field(rec['reason'], 260)}"
            )

    print("SKILL_RECOMMEND_END")
    return 0


def _is_skill_dir(path: Path) -> bool:
    return path.is_dir() and (path / "SKILL.md").is_file()


def _same_directory(left: Path, right: Path) -> bool:
    try:
        return left.resolve() == right.resolve()
    except OSError:
        return False


def sync_platforms(extra_platforms: Optional[List[str]] = None) -> int:
    """Sync the shared Agents/Claude domain and optionally publish to named platforms.

    Only Claude may import real skill directories into the canonical Agents directory.
    Other platforms are private by default. When explicitly named, they receive links
    to shared Agents skills, but their real/private skills are never imported back.
    """
    requested = extra_platforms or []
    unknown = [name for name in requested if name not in PLATFORMS]
    if unknown:
        print_error(f"Unknown sync platform(s): {', '.join(unknown)}")
        return 1

    selected = list(DEFAULT_SYNC_PLATFORMS)
    for name in requested:
        if name not in selected:
            selected.append(name)

    agents_dir = PLATFORMS["agents"]
    agents_dir.mkdir(parents=True, exist_ok=True)
    copied, linked, cleaned, conflicts = 0, 0, 0, 0

    print("SYNC_BEGIN")
    print(f"SCOPE\tshared={','.join(DEFAULT_SYNC_PLATFORMS)}\texplicit={','.join(requested) or '-'}")

    for name in selected:
        if name == "agents":
            continue
        path = PLATFORMS[name]
        path.mkdir(parents=True, exist_ok=True)

        if _same_directory(path, agents_dir):
            print(f"PLATFORM\tname={name}\taction=already-shared")
            continue

        for skill in list(path.iterdir()):
            if skill.is_symlink() and not skill.exists():
                skill.unlink()
                cleaned += 1

        # Claude belongs to the shared domain. Explicit/private platforms never
        # push their own real directories into Agents.
        if name == "claude":
            for skill in path.iterdir():
                if skill.is_symlink() or skill.name.startswith(".") or not _is_skill_dir(skill):
                    continue
                target = agents_dir / skill.name
                if not target.exists() and not target.is_symlink():
                    shutil.copytree(skill, target)
                    copied += 1

        for skill in agents_dir.iterdir():
            if skill.name.startswith(".") or not _is_skill_dir(skill):
                continue
            link = path / skill.name
            if link.exists() or link.is_symlink():
                if link.is_symlink() and link.exists() and link.resolve() == skill.resolve():
                    continue
                conflicts += 1
                continue
            relative_target = Path(os.path.relpath(skill, start=path))
            link.symlink_to(relative_target)
            linked += 1

        action = "shared-peer" if name == "claude" else "explicit-publish"
        print(f"PLATFORM\tname={name}\taction={action}")

    untouched = sorted(PLATFORM_PRIVATE_BY_DEFAULT - set(requested))
    print(f"ISOLATED\tuntouched={','.join(untouched) or '-'}")
    print(f"RESULT\tcopied={copied}\tlinked={linked}\tcleaned={cleaned}\tconflicts={conflicts}")
    print("SYNC_END")
    return 0


def sync_all(extra_platforms: Optional[List[str]] = None) -> int:
    """Backward-compatible safe sync alias; defaults to Agents and Claude only."""
    return sync_platforms(extra_platforms)

def delete_skill(name: str) -> int:
    """Delete skill from all platforms."""
    deleted = 0
    for platform, path in PLATFORMS.items():
        skill_path = path / name
        if skill_path.exists() or skill_path.is_symlink():
            if skill_path.is_symlink():
                skill_path.unlink()
            else:
                shutil.rmtree(skill_path)
            print(f"{Color.YELLOW}Deleted from:{Color.RESET} {platform}")
            deleted += 1
    return deleted

def topology() -> Dict[str, Dict[str, int]]:
    """Analyze symlink topology."""
    print(f"{Color.CYAN}=== Symlink Topology ==={Color.RESET}")
    result = {}
    for name, path in PLATFORMS.items():
        if not path.exists():
            continue
        skills = list(path.iterdir())
        real = sum(1 for d in skills if d.is_dir() and not d.is_symlink())
        links = sum(1 for d in skills if d.is_symlink())
        print(f"{name}: {Color.GREEN}{real} real{Color.RESET}, {Color.YELLOW}{links} links{Color.RESET}")
        result[name] = {"real": real, "links": links}
    return result

def backup() -> Path:
    """Create backup of all skills."""
    backup_dir = HOME / "skill-backups"
    backup_dir.mkdir(exist_ok=True)
    filename = f"skills_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tar.gz"
    filepath = backup_dir / filename

    agents_dir = PLATFORMS["agents"]
    if not agents_dir.exists():
        print_error("No skills to backup")
        return filepath

    with tarfile.open(filepath, "w:gz") as tar:
        tar.add(agents_dir, arcname=".agents/skills")

    size_mb = filepath.stat().st_size / 1024 / 1024
    print(f"{Color.GREEN}Backup:{Color.RESET} {filepath} ({size_mb:.2f} MB)")
    return filepath

def graph(platform: Optional[str] = None) -> None:
    """Generate skill graph with categories - Unicode table format."""
    print_info("Generating skill graph...\n")

    # Category definitions with icons
    category_defs = {
        "automation": {"icon": "⚙️", "desc": "Workflow automation and task execution"},
        "development": {"icon": "💻", "desc": "Code development and debugging"},
        "testing": {"icon": "🧪", "desc": "Testing and quality assurance"},
        "design": {"icon": "🎨", "desc": "UI/UX design and frontend patterns"},
        "documentation": {"icon": "📚", "desc": "Documentation and knowledge management"},
        "security": {"icon": "🔒", "desc": "Security analysis and protection"},
        "performance": {"icon": "⚡", "desc": "Performance optimization and monitoring"},
        "integration": {"icon": "🔗", "desc": "API and service integration"},
        "ai-ml": {"icon": "🤖", "desc": "AI/ML and LLM applications"},
        "devops": {"icon": "🚀", "desc": "DevOps and deployment"},
        "data": {"icon": "📊", "desc": "Data processing and analysis"},
        "mobile": {"icon": "📱", "desc": "Mobile development (iOS/Android)"},
        "general": {"icon": "📦", "desc": "General purpose utilities"},
    }

    all_skills = {}  # skillName -> {category, description, platforms}

    if platform and platform not in PLATFORMS:
        print_error(f"Unknown platform: {platform}")
        return

    target_platforms = [platform] if platform else list(PLATFORMS.keys())

    for name in target_platforms:
        path = PLATFORMS[name]
        if not path.exists():
            continue

        for skill_dir in path.iterdir():
            if skill_dir.is_symlink():
                continue
            if not skill_dir.is_dir():
                continue
            if skill_dir.name in ["learned", "superpowers"]:
                continue

            skill_name = skill_dir.name

            if skill_name not in all_skills:
                metadata = read_skill_metadata(skill_dir / "SKILL.md", skill_name, 80)
                all_skills[skill_name] = {
                    "category": metadata["category"],
                    "description": metadata["description"],
                    "platforms": [name]
                }
            else:
                all_skills[skill_name]["platforms"].append(name)

    # Group by category
    by_category = defaultdict(list)
    for skill_name, info in all_skills.items():
        by_category[info["category"]].append({"name": skill_name, **info})

    # Print skill graph with Unicode table
    total = len(all_skills)
    num_categories = len(by_category)

    print(f"{Color.CYAN}╔════════════════════════════════════════════════════════════╗{Color.RESET}")
    print(f"{Color.CYAN}║                    📊 SKILL GRAPH                          ║{Color.RESET}")
    print(f"{Color.CYAN}╠════════════════════════════════════════════════════════════╣{Color.RESET}")
    print(f"{Color.CYAN}║ Total Skills: {str(total).ljust(45)}║{Color.RESET}")
    print(f"{Color.CYAN}║ Categories: {str(num_categories).ljust(46)}║{Color.RESET}")
    print(f"{Color.CYAN}╚════════════════════════════════════════════════════════════╝{Color.RESET}\n")

    # Sort categories by count
    sorted_categories = sorted(by_category.items(), key=lambda x: -len(x[1]))

    for category, skills in sorted_categories:
        def_info = category_defs.get(category, category_defs["general"])
        print(f"{Color.YELLOW}{def_info['icon']} {category.upper()} ({len(skills)}){Color.RESET}")
        print(f"  └ {def_info['desc']}\n")

        for skill in sorted(skills, key=lambda x: x["name"]):
            platforms_str = ""
            if len(skill["platforms"]) > 1:
                platforms_str = f" {Color.GREEN}[{len(skill['platforms'])} platforms]{Color.RESET}"
            print(f"    • {skill['name']}{platforms_str}")
            if skill["description"]:
                desc = skill["description"][:60] + "..." if len(skill["description"]) > 60 else skill["description"]
                print(f"      {Color.CYAN}{desc}{Color.RESET}")
        print()

def install_from_github(url: str, target_platform: str = "agents") -> bool:
    """Install skill from GitHub URL."""
    match = re.search(r'github\.com/([^/]+)/([^/]+)', url)
    if not match:
        print_error("Invalid GitHub URL")
        return False

    owner, repo = match.groups()

    for branch in ["main", "master"]:
        skill_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/SKILL.md"
        try:
            print_info(f"Trying branch {branch}...")
            with urllib.request.urlopen(skill_url, timeout=10) as response:
                content = response.read().decode('utf-8')
                break
        except urllib.error.HTTPError:
            continue
    else:
        print_error("Could not find SKILL.md in repository")
        return False

    target_dir = PLATFORMS.get(target_platform)
    if not target_dir:
        print_error(f"Unknown platform: {target_platform}")
        return False

    skill_dir = target_dir / repo
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(content)

    print_success(f"Installed {repo} to {target_platform}")
    return True


def compare_platforms(p1: str, p2: str) -> Dict[str, Set[str]]:
    """Compare skills between two platforms."""
    path1 = PLATFORMS.get(p1)
    path2 = PLATFORMS.get(p2)

    if not path1 or not path2:
        print_error("Unknown platform")
        return {}

    if not path1.exists() or not path2.exists():
        print_error("Platform directory not found")
        return {}

    skills1 = {d.name for d in path1.iterdir() if d.is_dir() or d.is_symlink()}
    skills2 = {d.name for d in path2.iterdir() if d.is_dir() or d.is_symlink()}

    only_p1 = skills1 - skills2
    only_p2 = skills2 - skills1
    common = skills1 & skills2

    print(f"{Color.CYAN}=== {p1} vs {p2} ==={Color.RESET}\n")

    print(f"{Color.GREEN}Common ({len(common)}):{Color.RESET}")
    for s in sorted(common)[:10]:
        print(f"  ✓ {s}")
    if len(common) > 10:
        print(f"  ... and {len(common) - 10} more")

    print(f"\n{Color.YELLOW}Only in {p1} ({len(only_p1)}):{Color.RESET}")
    for s in sorted(only_p1):
        print(f"  → {s}")

    print(f"\n{Color.YELLOW}Only in {p2} ({len(only_p2)}):{Color.RESET}")
    for s in sorted(only_p2):
        print(f"  → {s}")

    return {"only_p1": only_p1, "only_p2": only_p2, "common": common}

def security(target: Optional[str] = None) -> int:
    """Run security scan via skill-security.sh."""
    script_dir = Path(__file__).parent
    security_script = script_dir / "skill-security.sh"

    if not security_script.exists():
        print_error("skill-security.sh not found")
        return 1

    target_path = target or str(PLATFORMS.get("agents", ""))
    result = subprocess.run(["bash", str(security_script), target_path])
    return result.returncode

def identify_source(skill_path: Path) -> str:
    """Identify the source/platform of a skill."""
    path_str = str(skill_path)

    # Known platforms (check in order of specificity)
    if "/.claude/skills/" in path_str:
        return "Claude Code"
    if "/.claude/plugins/" in path_str:
        return "Claude Plugins"
    if "/.cursor/skills/" in path_str:
        return "Cursor"
    if "/.cursor/extensions/" in path_str:
        return "Cursor Extensions"
    if "/.copilot/skills/" in path_str:
        return "GitHub Copilot"
    if "/.vscode/skills/" in path_str:
        return "VSCode"
    if "/.vscode/extensions/" in path_str:
        return "VSCode Extensions"
    if "/.agents/skills/" in path_str:
        return ".agents"
    if "/.qoder/skills/" in path_str:
        return "Qoder"
    if "/.qoderwork/skills/" in path_str:
        return "QoderWork"
    if "/.opencode/skills/" in path_str:
        return "OpenCode"
    if "/.openclaw/skills/" in path_str:
        return "OpenClaw"
    if "/.hermes/skills/" in path_str:
        return "Hermes"
    if "/.kiro/skills/" in path_str:
        return "Kiro"
    if "/.trae/skills/" in path_str:
        return "Trae"
    if "/.roo/skills/" in path_str:
        return "Roo"
    if "/.gemini/skills/" in path_str:
        return "Gemini"
    if "/.codex/skills/" in path_str:
        return "Codex"
    if "/.cline/skills/" in path_str:
        return "Cline"
    if "/.opencode/" in path_str:
        return "OpenCode"
    if "/.cc-switch/skills/" in path_str:
        return "CC-Switch"
    if "/.aider/" in path_str:
        return "Aider"
    if "/.continue/" in path_str:
        return "Continue"
    if "/.config/" in path_str:
        return "Config"

    return "Other"

def scan_all() -> None:
    """Backward-compatible alias for the unified list command."""
    print_info("`scan` is now an alias of `list`.\n")
    list_skills()

def cleanup(platform: Optional[str] = None) -> int:
    """Clean empty directories and broken symlinks from platforms."""
    print_info("Cleaning up skills...\n")
    
    cleaned_dirs, cleaned_links = 0, 0
    
    targets = [platform] if platform else list(DEFAULT_SYNC_PLATFORMS)
    
    for name in targets:
        if name not in PLATFORMS:
            continue
        path = PLATFORMS[name]
        if not path.exists():
            continue
            
        for skill in path.iterdir():
            if skill.name.startswith('.'):
                continue
                
            if skill.is_symlink():
                # Check if symlink target exists
                try:
                    if not skill.exists():
                        skill.unlink()
                        print(f"{Color.RED}Removed broken link:{Color.RESET} {name}/{skill.name}")
                        cleaned_links += 1
                except Exception as e:
                    print_error(f"Failed to remove {skill.name}: {e}")
                    
            elif skill.is_dir():
                # Check if directory is empty
                try:
                    visible = [f for f in skill.iterdir() if not f.name.startswith('.')]
                    if not visible:
                        shutil.rmtree(skill)
                        print(f"{Color.YELLOW}Cleaned empty dir:{Color.RESET} {name}/{skill.name}")
                        cleaned_dirs += 1
                except Exception as e:
                    print_error(f"Failed to clean {skill.name}: {e}")
    
    print(f"\n{Color.GREEN}Cleanup complete:{Color.RESET} {cleaned_links} broken links, {cleaned_dirs} empty dirs")
    return cleaned_links + cleaned_dirs

def doctor() -> int:
    """Health check for skill ecosystem."""
    print(f"{Color.CYAN}╔════════════════════════════════════════════════════════════╗{Color.RESET}")
    print(f"{Color.CYAN}║              🔍 SKILL HEALTH CHECK                         ║{Color.RESET}")
    print(f"{Color.CYAN}╚════════════════════════════════════════════════════════════╝{Color.RESET}\n")
    
    issues = []
    warnings = []
    
    # Check 1: Platform directories exist
    print(f"{Color.YELLOW}1. Platform Directory Check{Color.RESET}")
    for name, path in PLATFORMS.items():
        if path.exists():
            print(f"  ✓ {name}")
        elif name in DEFAULT_SYNC_PLATFORMS:
            print(f"  ✗ {name} (required shared platform missing)")
            issues.append(f"required shared platform directory not found: {name}")
        else:
            print(f"  - {name} (not configured; isolated)")
    
    # Check 2: Broken symlinks
    print(f"\n{Color.YELLOW}2. Broken Symlink Check{Color.RESET}")
    broken_links = []
    for name, path in PLATFORMS.items():
        if not path.exists():
            continue
        for skill in path.iterdir():
            if skill.is_symlink() and not skill.exists():
                broken_links.append((name, skill.name))
    
    if broken_links:
        for platform, skill in broken_links:
            print(f"  ✗ {platform}/{skill}")
        issues.append(f"{len(broken_links)} broken symlinks found")
    else:
        print(f"  ✓ No broken symlinks")
    
    # Check 3: Empty directories
    print(f"\n{Color.YELLOW}3. Empty Directory Check{Color.RESET}")
    empty_dirs = []
    for name, path in PLATFORMS.items():
        if not path.exists():
            continue
        for skill in path.iterdir():
            if skill.name.startswith((".", "_")):
                continue
            if skill.is_dir() and not skill.is_symlink():
                try:
                    visible = [f for f in skill.iterdir() if not f.name.startswith('.')]
                    if not visible:
                        empty_dirs.append((name, skill.name))
                except:
                    pass
    
    if empty_dirs:
        for platform, skill in empty_dirs:
            print(f"  ✗ {platform}/{skill}")
        issues.append(f"{len(empty_dirs)} empty directories found")
    else:
        print(f"  ✓ No empty directories")
    
    # Check 4: Duplicate skills across platforms
    print(f"\n{Color.YELLOW}4. Duplicate Check{Color.RESET}")
    skill_platforms = defaultdict(list)
    for name, path in PLATFORMS.items():
        if not path.exists():
            continue
        for skill in path.iterdir():
            if not skill.name.startswith((".", "_")) and _is_skill_dir(skill):
                skill_platforms[skill.name].append(name)
    
    duplicates = {k: v for k, v in skill_platforms.items() if len(v) > 1}
    if duplicates:
        for skill, platforms in sorted(duplicates.items()):
            if len(platforms) > 1:
                print(f"  ! {skill} ({len(platforms)} platforms)")
        print(f"  {Color.CYAN}Note: Duplicates across platforms are normal (symlinks){Color.RESET}")
    else:
        print(f"  ✓ No duplicates")
    
    # Check 5: Skills without SKILL.md
    print(f"\n{Color.YELLOW}5. SKILL.md Check{Color.RESET}")
    missing_skill_md = []
    for name, path in PLATFORMS.items():
        if not path.exists():
            continue
        for skill in path.iterdir():
            if skill.name.startswith((".", "_")):
                continue
            if skill.is_dir() and not skill.is_symlink():
                if not (skill / "SKILL.md").exists():
                    missing_skill_md.append((name, skill.name))
    
    if missing_skill_md:
        for platform, skill in missing_skill_md:
            print(f"  ✗ {platform}/{skill}")
        issues.append(f"{len(missing_skill_md)} skills missing SKILL.md")
    else:
        print(f"  ✓ All skills have SKILL.md")

    # Check 6: Default-private platforms must not alias or leak into Agents
    print(f"\n{Color.YELLOW}6. Platform Boundary Check{Color.RESET}")
    agents_dir = PLATFORMS["agents"]
    agents_names = {
        path.name for path in agents_dir.iterdir() if _is_skill_dir(path)
    } if agents_dir.exists() else set()
    boundary_issues = []
    for name in sorted(PLATFORM_PRIVATE_BY_DEFAULT):
        path = PLATFORMS[name]
        if not path.exists():
            continue
        if _same_directory(path, agents_dir):
            boundary_issues.append(f"{name} aliases the shared Agents directory")
            continue
        leaked = sorted(
            skill.name
            for skill in path.iterdir()
            if not skill.is_symlink() and _is_skill_dir(skill) and skill.name in agents_names
        )
        if leaked:
            boundary_issues.append(f"{name} private skills also exist in Agents: {', '.join(leaked)}")
    if boundary_issues:
        for issue in boundary_issues:
            print(f"  ✗ {issue}")
        issues.append(f"{len(boundary_issues)} platform boundary issue(s)")
    else:
        print("  ✓ Private platform directories are isolated from Agents")
    
    # Summary
    print(f"\n{Color.CYAN}=== Summary ==={Color.RESET}")
    if issues:
        print(f"{Color.RED}❌ Found {len(issues)} issue(s):{Color.RESET}")
        for issue in issues:
            print(f"  • {issue}")
    elif warnings:
        print(f"{Color.YELLOW}⚠️  Found {len(warnings)} warning(s):{Color.RESET}")
        for warning in warnings:
            print(f"  • {warning}")
    else:
        print(f"{Color.GREEN}✅ All checks passed!{Color.RESET}")
    
    if issues:
        print(f"\n{Color.CYAN}Review the reported paths; cleanup only removes broken links and empty directories.{Color.RESET}")
    
    return len(issues)

def web_server(port: int = 8080) -> int:
    """Launch the web UI server in background."""
    web_script = Path(__file__).parent / "skill-admin-web.py"
    if not web_script.exists():
        print_error("skill-admin-web.py not found")
        return 1

    # Always run in background so it doesn't block
    proc = subprocess.Popen(
        [sys.executable, str(web_script), "--port", str(port)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    pid_file = Path(__file__).parent / ".web.pid"
    pid_file.write_text(str(proc.pid))
    url = f"http://localhost:{port}"
    print_info(f"Skill Admin Web started in background")
    print_info(f"  URL: {url}")
    print_info(f"  PID: {proc.pid}")
    print_info(f"  Stop: python skill-admin.py web-stop")
    return 0

def web_stop() -> int:
    """Stop the background web server."""
    pid_file = Path(__file__).parent / ".web.pid"
    if not pid_file.exists():
        print_error("No running web server found (no .web.pid)")
        return 1

    try:
        pid = int(pid_file.read_text().strip())
        import signal
        os.kill(pid, signal.SIGTERM)
        pid_file.unlink()
        print_success(f"Web server (PID {pid}) stopped")
        return 0
    except ProcessLookupError:
        print_info("Web server was already stopped (stale PID removed)")
        pid_file.unlink()
        return 0
    except Exception as e:
        print_error(f"Failed to stop: {e}")
        return 1

def show_help() -> None:
    print(f"""{Color.CYAN}Skill Admin{Color.RESET} - Manage skills across AI platforms

{Color.YELLOW}Usage:{Color.RESET} python skill-admin.py <command> [args]

{Color.GREEN}Commands:{Color.RESET}
  web [port]             Launch web UI in background (default port 8080)
  web-stop               Stop the background web server
  current                Show detected runtime and usable skill paths
  list [platform]        Unified skill listing entrypoint; use --current for runtime scope
  recommend <query>      Recommend current-runtime skills for a requirement
  guide <query>          Alias of recommend
  scan                   Alias of list
  sync [platform ...]    Sync Agents + Claude; explicitly named platforms receive shared links
  sync-all [platform...] Backward-compatible safe alias for sync
  cleanup [platform]     Clean Agents + Claude by default; explicit platform only when named
  doctor                 Health check for skill ecosystem
  delete <name>          Delete skill from all platforms
  graph [platform]       Generate skill category graph
  install <url> [plat]   Install skill from GitHub
  compare <p1> <p2>      Compare skills between platforms
  topology               Show symlink structure (real vs links)
  backup                 Create tar.gz backup
  security [path]        Scan for malicious code (11 dimensions)

{Color.GREEN}Platform Identifiers:{Color.RESET}
  claude, cursor, copilot, vscode, cline, roo, goose, codex
  windsurf, trae, kiro, opencode, openclaw, hermes, qoder
  qoderwork, gemini, antigravity, agents

{Color.YELLOW}Examples:{Color.RESET}
  python skill-admin.py web
  python skill-admin.py web 9000
  python skill-admin.py web-stop
  python skill-admin.py current
  python skill-admin.py list claude
  python skill-admin.py list --current
  python skill-admin.py recommend "修一个页面样式问题" --top 5
  python skill-admin.py list
  python skill-admin.py sync
  python skill-admin.py sync openclaw   # explicit one-way publish; no private-skill import
  python skill-admin.py cleanup
  python skill-admin.py doctor
  python skill-admin.py graph
  python skill-admin.py install https://github.com/user/repo
  python skill-admin.py compare claude cursor
  python skill-admin.py delete skill-name
  python skill-admin.py security ~/.agents/skills/xxx

{Color.CYAN}Dependencies:{Color.RESET} None (Python 3.8+ stdlib only)
""")

# === Main ===

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    args = sys.argv[2:]
    arg1 = args[0] if len(args) > 0 else None
    arg2 = args[1] if len(args) > 1 else None

    commands = {
        "web": lambda: web_server(int(arg1) if arg1 else 8080),
        "web-stop": web_stop,
        "current": show_current,
        "list": lambda: list_skills(arg1),
        "recommend": lambda: recommend_command(args),
        "guide": lambda: recommend_command(args),
        "scan": scan_all,
        "sync": lambda: sync_platforms(args),
        "sync-all": lambda: sync_all(args),
        "cleanup": lambda: cleanup(arg1),
        "doctor": doctor,
        "delete": lambda: delete_skill(arg1) if arg1 else print_error("Usage: delete <name>"),
        "graph": lambda: graph(arg1),
        "install": lambda: install_from_github(arg1, arg2 or "agents") if arg1 else print_error("Usage: install <url>"),
        "compare": lambda: compare_platforms(arg1, arg2) if arg1 and arg2 else print_error("Usage: compare <p1> <p2>"),
        "topology": topology,
        "backup": backup,
        "security": lambda: security(arg1),
        "help": show_help,
        "-h": show_help,
        "--help": show_help,
    }

    if cmd in commands:
        return commands[cmd]()
    else:
        print_error(f"Unknown command: {cmd}")
        show_help()
        return 1

if __name__ == "__main__":
    sys.exit(main() or 0)
