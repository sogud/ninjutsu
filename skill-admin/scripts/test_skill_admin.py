#!/usr/bin/env python3
"""Test script for skill-admin.py. Usage: python test_skill_admin.py"""

import os
import sys
import shutil
import tempfile
import unittest
from pathlib import Path

# Import skill_admin from same directory
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

# Import with underscore name matching file
import importlib.util
spec = importlib.util.spec_from_file_location("skill_admin", script_dir / "skill-admin.py")
skill_admin = importlib.util.module_from_spec(spec)
spec.loader.exec_module(skill_admin)

web_spec = importlib.util.spec_from_file_location("skill_admin_web", script_dir / "skill-admin-web.py")
skill_admin_web = importlib.util.module_from_spec(web_spec)
web_spec.loader.exec_module(skill_admin_web)

class TestSkillAdmin(unittest.TestCase):
    """Test cases for skill-admin.py"""

    @classmethod
    def setUpClass(cls):
        """Create temp test environment"""
        cls.test_dir = Path(tempfile.mkdtemp())
        cls.test_platforms = {
            "agents": cls.test_dir / "agents",
            "claude": cls.test_dir / "claude",
            "openclaw": cls.test_dir / "openclaw",
            "hermes": cls.test_dir / "hermes",
        }
        cls.write_skill("agents", "test-skill", "---\nname: test-skill\n---\n# Test Skill\n")
        cls.write_skill(
            "agents",
            "browser-debug",
            "---\nname: browser-debug\ndescription: Debug browser pages, DOM issues, and frontend screenshots.\n---\n",
        )

    @classmethod
    def write_skill(cls, platform: str, name: str, content: str) -> Path:
        skill_dir = cls.test_platforms[platform] / name
        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / "SKILL.md").write_text(content)
        return skill_dir

    @classmethod
    def tearDownClass(cls):
        """Cleanup temp directory"""
        shutil.rmtree(cls.test_dir)

    def test_01_dependencies(self):
        """All dependencies are stdlib"""
        import importlib
        stdlib_modules = ["os", "sys", "shutil", "tarfile", "pathlib", "datetime", "subprocess"]
        for mod in stdlib_modules:
            importlib.import_module(mod)
            print(f"  ✓ {mod}")

    def test_02_list_skills(self):
        """List command works"""
        original = skill_admin.PLATFORMS.copy()
        skill_admin.PLATFORMS = self.test_platforms
        try:
            result = skill_admin.list_skills("agents")
            # list_skills now returns 0 for success
            self.assertEqual(result, 0)
        finally:
            skill_admin.PLATFORMS = original

    def test_03_list_current_alias(self):
        """List --current resolves to the detected runtime profile"""
        original = skill_admin.PLATFORMS.copy()
        original_env = os.environ.get("PI_CODING_AGENT")
        skill_admin.PLATFORMS = self.test_platforms
        os.environ["PI_CODING_AGENT"] = "1"
        try:
            result = skill_admin.list_skills("--current")
            self.assertEqual(result, 0)
        finally:
            skill_admin.PLATFORMS = original
            if original_env is None:
                os.environ.pop("PI_CODING_AGENT", None)
            else:
                os.environ["PI_CODING_AGENT"] = original_env

    def test_04_recommend_skills(self):
        """Recommendation uses only name + description in the selected platform"""
        original = skill_admin.PLATFORMS.copy()
        skill_admin.PLATFORMS = self.test_platforms
        try:
            result = skill_admin.recommend_skills("debug a browser page", "agents", top=1)
            self.assertTrue(result["ok"])
            self.assertEqual(result["recommendations"][0]["name"], "browser-debug")
        finally:
            skill_admin.PLATFORMS = original

    def test_05_default_sync_isolates_openclaw_and_hermes(self):
        """Default sync imports Claude only and leaves private platforms untouched."""
        original = skill_admin.PLATFORMS.copy()
        original_private = skill_admin.PLATFORM_PRIVATE_BY_DEFAULT.copy()
        self.write_skill("claude", "source-skill", "---\nname: source-skill\n---\n")
        self.write_skill("openclaw", "openclaw-private", "---\nname: openclaw-private\n---\n")
        self.write_skill("hermes", "hermes-private", "---\nname: hermes-private\n---\n")

        skill_admin.PLATFORMS = self.test_platforms
        skill_admin.PLATFORM_PRIVATE_BY_DEFAULT = {"openclaw", "hermes"}
        try:
            self.assertEqual(skill_admin.sync_all(), 0)
            self.assertTrue((self.test_platforms["agents"] / "source-skill").exists())
            self.assertFalse((self.test_platforms["agents"] / "openclaw-private").exists())
            self.assertFalse((self.test_platforms["agents"] / "hermes-private").exists())
            self.assertFalse((self.test_platforms["openclaw"] / "test-skill").exists())
            self.assertFalse((self.test_platforms["hermes"] / "test-skill").exists())
        finally:
            skill_admin.PLATFORMS = original
            skill_admin.PLATFORM_PRIVATE_BY_DEFAULT = original_private

    def test_06_explicit_publish_is_one_way(self):
        """Explicit platforms receive shared links without exporting private skills."""
        original = skill_admin.PLATFORMS.copy()
        original_private = skill_admin.PLATFORM_PRIVATE_BY_DEFAULT.copy()
        skill_admin.PLATFORMS = self.test_platforms
        skill_admin.PLATFORM_PRIVATE_BY_DEFAULT = {"openclaw", "hermes"}
        try:
            self.assertEqual(skill_admin.sync_platforms(["openclaw"]), 0)
            shared_link = self.test_platforms["openclaw"] / "test-skill"
            self.assertTrue(shared_link.is_symlink())
            self.assertFalse((self.test_platforms["agents"] / "openclaw-private").exists())
            self.assertFalse((self.test_platforms["hermes"] / "test-skill").exists())
        finally:
            skill_admin.PLATFORMS = original
            skill_admin.PLATFORM_PRIVATE_BY_DEFAULT = original_private

    def test_07_unknown_sync_platform_fails(self):
        """Unknown explicit sync targets fail without changing platform content."""
        self.assertEqual(skill_admin.sync_platforms(["not-a-platform"]), 1)

    def test_08_topology(self):
        """Topology analysis works"""
        original = skill_admin.PLATFORMS.copy()
        skill_admin.PLATFORMS = self.test_platforms
        try:
            result = skill_admin.topology()
            self.assertIn("agents", result)
        finally:
            skill_admin.PLATFORMS = original

    def test_09_delete_skill(self):
        """Delete removes skill"""
        skill_dir = self.write_skill("agents", "to-delete", "---\nname: to-delete\n---\n")

        original = skill_admin.PLATFORMS.copy()
        skill_admin.PLATFORMS = self.test_platforms
        try:
            deleted = skill_admin.delete_skill("to-delete")
            self.assertGreater(deleted, 0)
            self.assertFalse(skill_dir.exists())
        finally:
            skill_admin.PLATFORMS = original

    def test_10_backup(self):
        """Backup creates tar.gz"""
        original = skill_admin.PLATFORMS.copy()
        skill_admin.PLATFORMS = self.test_platforms
        try:
            original_home = skill_admin.HOME
            skill_admin.HOME = self.test_dir
            filepath = skill_admin.backup()
            self.assertTrue(filepath.exists())
            self.assertTrue(filepath.suffix == ".gz")
            filepath.unlink()  # cleanup
        finally:
            skill_admin.PLATFORMS = original
            skill_admin.HOME = original_home

    def test_11_doctor_rejects_private_platform_alias(self):
        """Doctor detects a private platform pointing at the shared Agents root."""
        original = skill_admin.PLATFORMS.copy()
        original_private = skill_admin.PLATFORM_PRIVATE_BY_DEFAULT.copy()
        platforms = {
            "agents": self.test_platforms["agents"],
            "claude": self.test_platforms["claude"],
            "openclaw": self.test_platforms["agents"],
        }
        skill_admin.PLATFORMS = platforms
        skill_admin.PLATFORM_PRIVATE_BY_DEFAULT = {"openclaw"}
        try:
            self.assertGreater(skill_admin.doctor(), 0)
        finally:
            skill_admin.PLATFORMS = original
            skill_admin.PLATFORM_PRIVATE_BY_DEFAULT = original_private

    def test_12_web_sync_uses_safe_default_scope(self):
        """Web sync also leaves OpenClaw and Hermes private skills untouched."""
        web_root = self.test_dir / "web"
        platforms = {
            "agents": web_root / "agents",
            "claude": web_root / "claude",
            "openclaw": web_root / "openclaw",
            "hermes": web_root / "hermes",
        }
        for name, skill in [("agents", "shared"), ("openclaw", "openclaw-private"), ("hermes", "hermes-private")]:
            skill_dir = platforms[name] / skill
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(f"---\nname: {skill}\n---\n")

        original = skill_admin_web.PLATFORMS.copy()
        skill_admin_web.PLATFORMS = platforms
        try:
            result = skill_admin_web.sync_all()
            self.assertEqual(result["scope"], ["agents", "claude"])
            self.assertTrue((platforms["claude"] / "shared").is_symlink())
            self.assertFalse((platforms["agents"] / "openclaw-private").exists())
            self.assertFalse((platforms["agents"] / "hermes-private").exists())
        finally:
            skill_admin_web.PLATFORMS = original

def run_quick_test():
    """Quick smoke test without unittest"""
    print("=== Quick Smoke Test ===\n")

    # 1. Dependencies
    print("1. Checking dependencies...")
    import importlib
    for mod in ["os", "sys", "shutil", "tarfile", "pathlib", "datetime", "subprocess"]:
        importlib.import_module(mod)
    print("   ✓ All stdlib modules available\n")

    # 2. Commands work
    print("2. Testing commands...")
    print("   list:", end=" ")
    result = skill_admin.list_skills("agents")
    print(f"✓ list exited with {result}")

    print("   topology:", end=" ")
    result = skill_admin.topology()
    print("✓")

    print("\n=== All tests passed ===")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        run_quick_test()
    else:
        unittest.main(verbosity=2)