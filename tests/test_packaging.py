"""Check that both plugin packages resolve to the same local implementation."""

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_json(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


class PackagingTests(unittest.TestCase):
    def test_hosts_share_identity_and_release_metadata(self):
        claude = read_json(".claude-plugin/plugin.json")
        codex = read_json(".codex-plugin/plugin.json")
        for field in (
            "name",
            "version",
            "description",
            "author",
            "repository",
            "license",
        ):
            with self.subTest(field=field):
                self.assertEqual(claude[field], codex[field])
        self.assertEqual(codex["name"], "vibe-wise")
        self.assertEqual(codex["author"]["name"], "Noah Kim")
        self.assertEqual(
            codex["repository"], "https://github.com/Chombled/vibe-wise-codex"
        )
        self.assertRegex(codex["version"], r"^\d+\.\d+\.\d+$")

    def test_codex_components_and_assets_resolve_inside_plugin(self):
        manifest = read_json(".codex-plugin/plugin.json")
        self.assertEqual(manifest["skills"], "./skills/")
        self.assertEqual(manifest["hooks"], "./hooks/hooks.json")
        for value in (
            manifest["skills"],
            manifest["hooks"],
            manifest["interface"]["composerIcon"],
            manifest["interface"]["logo"],
        ):
            with self.subTest(path=value):
                self.assertTrue(value.startswith("./"))
                path = (ROOT / value).resolve()
                path.relative_to(ROOT)
                self.assertTrue(path.exists())
        registration = read_json(manifest["hooks"])["hooks"]["SessionStart"]
        self.assertEqual(len(registration), 1)
        self.assertEqual(len(registration[0]["hooks"]), 1)
        self.assertEqual(registration[0]["hooks"][0]["type"], "command")

    def test_marketplaces_resolve_the_repository_plugin(self):
        claude = read_json(".claude-plugin/marketplace.json")
        codex = read_json(".agents/plugins/marketplace.json")
        self.assertEqual(codex["name"], "vibe-wise-codex")
        for marketplace in (claude, codex):
            self.assertEqual(len(marketplace["plugins"]), 1)
            entry = marketplace["plugins"][0]
            self.assertEqual(entry["name"], "vibe-wise")
            source = entry["source"]
            if isinstance(source, dict):
                self.assertEqual(source["source"], "local")
                source = source["path"]
                self.assertEqual(entry["policy"]["installation"], "AVAILABLE")
                self.assertEqual(entry["policy"]["authentication"], "ON_INSTALL")
                self.assertEqual(entry["category"], "Productivity")
            self.assertTrue(source.startswith("./"))
            self.assertEqual((ROOT / source).resolve(), ROOT)

    def test_both_skills_require_explicit_invocation_on_both_hosts(self):
        for name in ("learn", "reset"):
            with self.subTest(skill=name):
                skill = ROOT / "skills" / name
                frontmatter = (
                    (skill / "SKILL.md").read_text(encoding="utf-8").split("---", 2)[1]
                )
                self.assertIn(
                    "disable-model-invocation: true", frontmatter.splitlines()
                )
                # Validate the invocation policy rather than the prompt's prose.
                metadata = (skill / "agents/openai.yaml").read_text(encoding="utf-8")
                policy = re.search(
                    r"^policy:\n((?:[ \t]+.*\n)+)", metadata, re.MULTILINE
                )
                self.assertIsNotNone(policy)
                self.assertRegex(policy[1], r"(?m)^  allow_implicit_invocation: false$")


if __name__ == "__main__":
    unittest.main()
