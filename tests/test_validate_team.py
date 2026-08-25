from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate_team.py"
SPEC = importlib.util.spec_from_file_location("validate_team", MODULE_PATH)
assert SPEC and SPEC.loader
validate_team = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validate_team
SPEC.loader.exec_module(validate_team)


class WorkboardHygieneTest(unittest.TestCase):
    def validator(self, terminal_limit: int = 10):
        validator = validate_team.Validator(
            project=None,
            strict=False,
            now=datetime(2026, 8, 25, 12, 0, tzinfo=timezone.utc),
        )
        validator.manifest = {
            "statuses": {
                "work_item": ["READY", "CLAIMED", "IN_PROGRESS", "IN_REVIEW", "BLOCKED", "DONE", "CANCELLED"]
            },
            "action_modes": {"implement": {}},
            "governance": {"workboard": {"recent_terminal_limit": terminal_limit}},
        }
        return validator

    def check_rows(self, rows: list[str], terminal_limit: int = 10):
        header = "| " + " | ".join(validate_team.WORKBOARD_HEADERS) + " |"
        separator = "|" + "|".join("---" for _ in validate_team.WORKBOARD_HEADERS) + "|"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "WORKBOARD.md"
            path.write_text("\n".join([header, separator, *rows]) + "\n", encoding="utf-8")
            validator = self.validator(terminal_limit)
            validator.check_workboard(path)
            return validator.findings

    def test_expired_lease_is_warning_not_error(self):
        row = (
            "| W-ACTIVE | active | IN_PROGRESS | agent | implement | abcdef1 | src/ | none | "
            "2026-08-25T10:00+08:00 | 2026-08-25T11:00+08:00 | tests | pending |"
        )
        findings = self.check_rows([row])
        self.assertEqual([finding.severity for finding in findings], ["WARNING"])
        self.assertIn("lease expired", findings[0].message)

    def test_done_worktree_warnings_are_aggregated(self):
        rows = [
            "| W-ONE | one | DONE | agent | implement | abcdef1 | src/a | none | d | d | tests | WORKTREE; pending commit |",
            "| W-TWO | two | DONE | agent | implement | abcdef1 | src/b | none | d | d | tests | WORKTREE |",
        ]
        findings = self.check_rows(rows)
        self.assertEqual(len(findings), 1)
        self.assertIn("2 DONE item(s)", findings[0].message)

    def test_committed_revision_closes_worktree_warning(self):
        row = (
            "| W-DONE | done | DONE | agent | implement | abcdef1 | src/ | none | d | d | tests | "
            "WORKTREE later committed as 1e53457 |"
        )
        self.assertEqual(self.check_rows([row]), [])

    def test_terminal_retention_warning_is_aggregated(self):
        rows = [
            f"| W-{index} | done | DONE | agent | implement | abcdef1 | src/ | none | d | d | tests | commit 1e5345{index} |"
            for index in range(3)
        ]
        findings = self.check_rows(rows, terminal_limit=2)
        self.assertEqual(len(findings), 1)
        self.assertIn("retains 3 terminal items (limit 2)", findings[0].message)


if __name__ == "__main__":
    unittest.main()
