import json
import py_compile
import re
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def read_text(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


class RepositoryIntegrityTests(unittest.TestCase):
    def test_critical_paths_exist(self) -> None:
        required_paths = [
            "README.md",
            "LICENSE",
            "CONTRIBUTING.md",
            "ATTRIBUTION.md",
            ".claude-plugin/plugin.json",
            ".claude-plugin/marketplace.json",
            "skills/nature-paper-hub/SKILL.md",
            "skills/nature-paper-hub/references",
            "templates/journal-specs.json",
            "templates/nature-latex.tex",
            "data/papers-index.json",
            "scripts/requirements.txt",
        ]
        for relative in required_paths:
            self.assertTrue((REPO_ROOT / relative).exists(), relative)

    def test_plugin_version_matches_hub_skill(self) -> None:
        plugin = json.loads(read_text(".claude-plugin/plugin.json"))
        skill_text = read_text("skills/nature-paper-hub/SKILL.md")
        match = re.search(r"^version:\s*([0-9]+\.[0-9]+\.[0-9]+)\s*$", skill_text, re.MULTILINE)

        self.assertIsNotNone(match)
        self.assertEqual(plugin["version"], match.group(1))

    def test_journal_specs_cover_19_journals(self) -> None:
        data = json.loads(read_text("templates/journal-specs.json"))
        journals = data.get("journals", {})

        self.assertEqual(len(journals), 19)
        for key, journal in journals.items():
            with self.subTest(journal=key):
                self.assertTrue(journal.get("name"))
                self.assertTrue(str(journal.get("url", "")).startswith("https://"))
                self.assertIn("article_types", journal)
                self.assertIsInstance(journal["article_types"], dict)
                self.assertGreater(len(journal["article_types"]), 0)

    def test_clean_papers_index_contract(self) -> None:
        data = json.loads(read_text("data/papers-index.json"))
        papers = data["papers"] if isinstance(data, dict) and "papers" in data else data

        self.assertEqual(len(papers), 485)
        self.assertFalse((REPO_ROOT / "data/papers-index.raw.json").exists())
        for idx, paper in enumerate(papers[:20]):
            with self.subTest(index=idx):
                self.assertTrue(paper.get("title"))

    def test_hub_references_count(self) -> None:
        references = sorted((REPO_ROOT / "skills/nature-paper-hub/references").glob("*.md"))
        self.assertEqual(len(references), 6)

    def test_readme_manual_install_keeps_full_resources(self) -> None:
        readme = read_text("README.md")
        forbidden_snippets = [
            "cp nature-paper-hub/skills/nature-paper-hub/SKILL.md",
            "cp nature-paper-hub/skills/*/SKILL.md",
            "~/.claude/agents",
        ]
        for snippet in forbidden_snippets:
            self.assertNotIn(snippet, readme)

        self.assertIn("CLAUDE_PLUGIN_ROOT", readme)
        self.assertIn("cp -R skills/nature-* ~/.codex/skills/", readme)
        self.assertIn("cp -R skills/nature-* ~/.claude/skills/", readme)

    def test_scripts_compile_without_repo_cache_writes(self) -> None:
        scripts = sorted((REPO_ROOT / "scripts").glob("*.py"))
        self.assertGreater(len(scripts), 0)
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            for script in scripts:
                cfile = tmp / f"{script.stem}.pyc"
                with self.subTest(script=script.name):
                    py_compile.compile(str(script), cfile=str(cfile), doraise=True)


if __name__ == "__main__":
    unittest.main()
