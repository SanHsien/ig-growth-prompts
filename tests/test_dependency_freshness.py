"""Behaviour tests for tools/check_dependency_freshness.py (no network: fetchers are stubs)."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "tools"))

import check_dependency_freshness as checker  # noqa: E402

SHA = "3d3c42e5aac5ba805825da76410c181273ba90b1"


def status(packages, latest: str):
    return checker.collect_status(packages, lambda _name: latest, deferrals={})


class TestBuildRequires(unittest.TestCase):
    def test_reads_only_the_build_system_requires(self):
        text = (
            "[build-system]\n"
            "requires = [\n"
            '  "setuptools>=61.0",  # freshness-hold: PEP 621\n'
            '  "wheel>=0.40",\n'
            "]\n"
            "[project]\n"
            'requires = ["other>=1"]\n'
        )
        rows = checker.parse_build_requires(text)
        self.assertEqual([(r["name"], r["minimum"], r["hold"]) for r in rows], [("setuptools", "61.0", "PEP 621"), ("wheel", "0.40", "")])

    def test_an_entry_with_extras_does_not_end_the_array(self):
        text = '[build-system]\nrequires = [\n  "pkg[extra]>=1",\n  "setuptools>=61.0",\n]\n'
        self.assertEqual([r["name"] for r in checker.parse_build_requires(text)], ["pkg", "setuptools"])

    def test_an_aged_floor_needs_review(self):
        [row] = status(checker.parse_build_requires('[build-system]\nrequires = ["setuptools>=61.0"]\n'), "84.2.1")
        self.assertTrue(checker.needs_review(row))

    def test_the_repository_floor_is_held_with_a_reason(self):
        [row] = status(checker.load_direct_dependencies(), "84.2.1")
        self.assertEqual(row["name"], "setuptools")
        self.assertTrue(row["hold"])
        self.assertFalse(checker.needs_review(row))
        self.assertFalse(row["check_failed"])


class TestWorkflowActions(unittest.TestCase):
    def test_tag_pin_compares_at_its_own_precision(self):
        [row] = status(checker.parse_workflow_actions("      - uses: actions/checkout@v7\n", "ci.yml"), "7.9.0")
        self.assertEqual(row["minimum"], "7")
        self.assertFalse(row["outdated"])
        [row] = status(checker.parse_workflow_actions("      - uses: actions/checkout@v7\n", "ci.yml"), "8.0.0")
        self.assertTrue(checker.needs_review(row))

    def test_sha_pin_reads_version_from_comment(self):
        [row] = status(checker.parse_workflow_actions(f"      - uses: actions/checkout@{SHA} # v7.0.1\n", "ci.yml"), "7.1.0")
        self.assertEqual(row["minimum"], "7.0.1")
        self.assertTrue(checker.needs_review(row))

    def test_held_action_is_held_not_a_failed_check(self):
        [row] = status(checker.parse_workflow_actions("      - uses: actions/checkout@v7 # freshness-hold: upstream workflow\n", "ci.yml"), "8.0.0")
        self.assertFalse(row["check_failed"], row)
        self.assertFalse(checker.needs_review(row))
        self.assertIn("HELD: upstream workflow", "\n".join(checker._render_table([row])))

    def test_every_repository_workflow_action_is_read(self):
        names = {row["name"] for row in checker.load_workflow_actions()}
        self.assertIn("actions/checkout", names)
        self.assertIn("softprops/action-gh-release", names)


if __name__ == "__main__":
    unittest.main()
