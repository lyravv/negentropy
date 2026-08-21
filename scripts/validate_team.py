#!/usr/bin/env python3
"""Validate negentropy's manifest, protocol, templates and project control files."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

import yaml

try:
    import jsonschema
except ImportError:  # The explicit checks remain available without jsonschema.
    jsonschema = None


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FRONTMATTER = {"title", "role", "status", "version", "updated", "upstream", "downstream"}
APPROVED_EVIDENCE_FIELDS = {"source_revision", "approver", "approval_evidence"}
PROJECT_PRINCIPALS = {"project-owner", "product-owner", "business-owner"}
GOVERNED_ARTIFACT_NAMES = {
    "project-brief.md": "project-brief",
    "business-brief.md": "business-rules",
    "glossary.md": "business-rules",
    "requirements.md": "requirements",
    "iteration-plan.md": "requirements",
    "architecture.md": "architecture",
    "api-spec.md": "api-contract",
    "data-model.md": "data-contract",
    "test-report.md": "test-report",
    "deployment.md": "deployment-plan",
    "release-notes.md": "production-release",
}
WORKBOARD_HEADERS = (
    "ID", "标题", "状态", "Owner", "Mode", "Base revision", "写入范围", "依赖",
    "Claimed at", "Lease until", "验收", "Result revision / Notes",
)
QUESTION_HEADERS = ("编号", "提出角色", "问题", "等待谁", "状态", "决定来源", "验证者", "解决记录")
CHANGE_HEADERS = ("编号", "提出角色", "目标事实", "批准者", "变更内容", "影响评估", "状态", "实施证据")


@dataclass
class Finding:
    severity: str
    path: Path
    message: str


def split_markdown_row(line: str) -> list[str] | None:
    """Split a pipe table row; literal pipes in cells must be escaped as \|."""
    stripped = line.strip()
    if not (stripped.startswith("|") and stripped.endswith("|")):
        return None
    return [cell.replace(r"\|", "|").strip() for cell in re.split(r"(?<!\\)\|", stripped[1:-1])]


def is_separator_row(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


class Validator:
    def __init__(self, project: str | None, strict: bool) -> None:
        self.project = project
        self.strict = strict
        self.findings: list[Finding] = []
        self.manifest: dict[str, Any] = {}

    def add(self, severity: str, path: Path, message: str) -> None:
        self.findings.append(Finding(severity, path, message))

    def error(self, path: Path, message: str) -> None:
        self.add("ERROR", path, message)

    def warn(self, path: Path, message: str) -> None:
        self.add("WARNING", path, message)

    def load_yaml(self, path: Path) -> Any:
        try:
            return yaml.safe_load(path.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError) as exc:
            self.error(path, f"cannot parse YAML: {exc}")
            return None

    def is_safe_relative_path(self, value: Any) -> bool:
        if not isinstance(value, str) or not value or Path(value).is_absolute():
            return False
        return ".." not in PurePosixPath(value).parts

    def validate_schema(self, data: dict[str, Any]) -> None:
        path = ROOT / "team/schemas/team.schema.json"
        try:
            schema = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            self.error(path, f"cannot load manifest schema: {exc}")
            return
        if jsonschema is None:
            self.warn(path, "jsonschema is not installed; using built-in structural checks")
            return
        try:
            jsonschema.validate(data, schema)
        except (jsonschema.ValidationError, jsonschema.SchemaError) as exc:
            location = ".".join(str(part) for part in exc.absolute_path) or "<root>"
            self.error(path, f"team.yaml failed schema at {location}: {exc.message}")

    def check_manifest(self) -> None:
        path = ROOT / "team.yaml"
        data = self.load_yaml(path)
        if not isinstance(data, dict):
            self.error(path, "manifest must be a mapping")
            return
        self.manifest = data
        self.validate_schema(data)

        required = {
            "schema_version", "team", "governance", "statuses", "action_modes",
            "external_principals", "approval_policies", "roles", "workflow",
            "handoff", "project_template", "evolution",
        }
        for key in sorted(required - set(data)):
            self.error(path, f"missing top-level key: {key}")
        if data.get("schema_version") != 1:
            self.error(path, "schema_version must be 1")

        team = data.get("team", {})
        if not re.fullmatch(r"\d+\.\d+\.\d+", str(team.get("version", ""))):
            self.error(path, "team.version must be semver X.Y.Z")

        roles = [role for role in data.get("roles", []) if isinstance(role, dict)]
        role_ids = [role.get("id") for role in roles]
        if len(role_ids) != len(set(role_ids)):
            self.error(path, "role ids must be unique")
        if "orchestrator" not in role_ids:
            self.error(path, "orchestrator must be a formal role")
        control_planes = [role.get("id") for role in roles if role.get("control_plane") is True]
        if control_planes != ["orchestrator"]:
            self.error(path, f"orchestrator must be the only control_plane role; got {control_planes}")

        for role in roles:
            role_id = str(role.get("id", "<unknown>"))
            if not re.fullmatch(r"[a-z][a-z0-9-]*", role_id):
                self.error(path, f"invalid role id: {role_id}")
            role_dir_value = role.get("dir", "")
            role_dir = ROOT / str(role_dir_value)
            if not self.is_safe_relative_path(role_dir_value) or not role_dir.is_dir():
                self.error(path, f"role {role_id} has invalid/missing dir: {role_dir_value}")
            for field in ("charter", "skills"):
                value = role.get(field, "")
                target = ROOT / str(value)
                if not self.is_safe_relative_path(value) or not target.is_file():
                    self.error(path, f"role {role_id} missing {field}: {value}")
                elif target.parent != role_dir:
                    self.error(path, f"role {role_id} {field} must be directly under {role_dir_value}")
            stages = role.get("stages", [])
            if not isinstance(stages, list) or not stages:
                self.error(path, f"role {role_id} must own at least one stage")
            for output in role.get("outputs", []):
                if not self.is_safe_relative_path(output):
                    self.error(path, f"role {role_id} has unsafe output path: {output}")

        workflow = data.get("workflow", {})
        profiles = workflow.get("profiles", [])
        maturity = workflow.get("profile_maturity", {})
        if workflow.get("default_profile") not in profiles:
            self.error(path, "workflow.default_profile must appear in workflow.profiles")
        if set(profiles) != set(maturity):
            self.error(path, "workflow.profile_maturity keys must exactly match workflow.profiles")

        stages = [stage for stage in workflow.get("stages", []) if isinstance(stage, dict)]
        stage_ids = [stage.get("id") for stage in stages]
        stage_numbers = [stage.get("stage") for stage in stages]
        if len(stage_ids) != len(set(stage_ids)):
            self.error(path, "workflow stage ids must be unique")
        if len(stage_numbers) != len(set(stage_numbers)):
            self.error(path, "workflow stage numbers must be unique")
        owners_by_stage: dict[int, set[str]] = {}
        for stage in stages:
            owners = stage.get("owner", [])
            owners = owners if isinstance(owners, list) else [owners]
            owners_by_stage[stage.get("stage")] = set(owners)
            for owner in owners:
                if owner not in role_ids:
                    self.error(path, f"workflow stage {stage.get('id')} references unknown owner {owner}")
        for role in roles:
            for stage_number in role.get("stages", []):
                if role.get("id") not in owners_by_stage.get(stage_number, set()):
                    self.error(path, f"role {role.get('id')} stages includes {stage_number}, but workflow does not assign it")
            if role.get("parallel_group") and not any(
                role.get("id") in owners_by_stage.get(stage.get("stage"), set()) and bool(stage.get("parallel"))
                for stage in stages
            ):
                self.error(path, f"role {role.get('id')} has parallel_group but no parallel workflow stage")

        principals = set(data.get("external_principals", []))
        for artifact_type, policy in data.get("approval_policies", {}).items():
            for approver in policy.get("approvers", []):
                if approver not in principals and approver not in role_ids:
                    self.error(path, f"approval policy {artifact_type} references unknown approver {approver}")

        paths: list[tuple[str, Any, str]] = []
        for key in ("philosophy", "file", "concurrency", "workflow_profiles"):
            paths.append((f"governance.{key}", data.get("governance", {}).get(key), "file"))
        paths.extend([
            ("workflow.file", workflow.get("file"), "file"),
            ("handoff.file", data.get("handoff", {}).get("file"), "file"),
            ("project_template", data.get("project_template"), "dir"),
            ("evolution.changelog", data.get("evolution", {}).get("changelog"), "file"),
            ("evolution.roadmap", data.get("evolution", {}).get("roadmap"), "file"),
        ])
        for label, value, kind in paths:
            if not self.is_safe_relative_path(value):
                self.error(path, f"{label} must be a safe relative path: {value}")
                continue
            target = ROOT / value
            exists = target.is_dir() if kind == "dir" else target.is_file()
            if not exists:
                self.error(path, f"{label} does not exist: {value}")

    def check_protocol(self) -> None:
        current = ROOT / "team/protocols/CURRENT.md"
        try:
            text = current.read_text(encoding="utf-8")
        except OSError as exc:
            self.error(current, f"cannot read protocol pointer: {exc}")
            return
        match = re.search(r"ACTIVE:\s*\[([^]]+)]\(([^)]+)\)", text)
        if not match:
            self.error(current, "cannot find ACTIVE protocol pointer")
            return
        protocol_id, relative = match.groups()
        if protocol_id != self.manifest.get("team", {}).get("protocol"):
            self.error(current, f"ACTIVE={protocol_id} differs from team.yaml protocol")
        target = current.parent / relative
        if not target.is_file():
            self.error(current, f"ACTIVE protocol file does not exist: {relative}")
        elif "状态**：ACTIVE" not in target.read_text(encoding="utf-8"):
            self.error(target, "active protocol must declare status ACTIVE")

    def frontmatter(self, path: Path) -> dict[str, Any] | None:
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            return None
        end = text.find("\n---", 4)
        if end < 0:
            self.error(path, "unterminated frontmatter")
            return None
        try:
            data = yaml.safe_load(text[4:end])
        except yaml.YAMLError as exc:
            self.error(path, f"invalid frontmatter: {exc}")
            return None
        if not isinstance(data, dict):
            self.error(path, "frontmatter must be a mapping")
            return None
        return data

    def check_document(self, path: Path, project_control: bool = False) -> None:
        fm = self.frontmatter(path)
        if fm is None:
            return
        missing = REQUIRED_FRONTMATTER - set(fm)
        if missing and not project_control:
            self.error(path, f"missing frontmatter fields: {', '.join(sorted(missing))}")
        if path.name == "STATE.md":
            allowed = set(self.manifest.get("statuses", {}).get("project", []))
            if fm.get("status") == "LIVE":
                self.warn(path, "legacy project status LIVE; change to ACTIVE on next edit")
            elif fm.get("status") not in allowed and "<" not in str(fm.get("status")):
                self.error(path, f"invalid project status: {fm.get('status')}")
            return
        if path.name == "WORKBOARD.md":
            if fm.get("status") not in {"ACTIVE", "ARCHIVED"}:
                self.error(path, "WORKBOARD status must be ACTIVE or ARCHIVED")
            return

        allowed = set(self.manifest.get("statuses", {}).get("document", []))
        status = fm.get("status")
        if status not in allowed and not (path.parent.name == "templates" and status == "DRAFT"):
            self.error(path, f"invalid document status: {status}")

        policies = self.manifest.get("approval_policies", {})
        artifact_type = fm.get("artifact_type")
        if artifact_type:
            policy = policies.get(artifact_type)
            if policy is None:
                self.error(path, f"unknown artifact_type: {artifact_type}")
            else:
                approver = fm.get("approver")
                if approver not in policy.get("approvers", []):
                    self.error(path, f"approver {approver!r} is not allowed for {artifact_type}")
                if policy.get("handoff_required") and "## 交接说明" not in path.read_text(encoding="utf-8"):
                    self.error(path, f"{artifact_type} must contain a 交接说明 section")
                if status == "APPROVED":
                    missing_evidence = [field for field in APPROVED_EVIDENCE_FIELDS if not fm.get(field)]
                    if missing_evidence:
                        self.error(path, "APPROVED governed artifact missing: " + ", ".join(sorted(missing_evidence)))

        try:
            path.relative_to(ROOT / "projects")
            is_project_document = True
        except ValueError:
            is_project_document = False
        if is_project_document and status == "APPROVED" and not artifact_type:
            expected_type = GOVERNED_ARTIFACT_NAMES.get(path.name)
            if path.name.startswith("US-"):
                expected_type = "requirements"
            if expected_type:
                missing_evidence = APPROVED_EVIDENCE_FIELDS - set(fm)
                fields = {"artifact_type"} | missing_evidence
                self.warn(path, f"legacy governed artifact ({expected_type}); add on next content change: " + ", ".join(sorted(fields)))

    def parse_tables(self, path: Path, text: str, first_header: str) -> list[tuple[list[str], list[dict[str, str]]]]:
        lines = text.splitlines()
        tables: list[tuple[list[str], list[dict[str, str]]]] = []
        index = 0
        while index < len(lines):
            headers = split_markdown_row(lines[index])
            if not headers or not headers or headers[0] != first_header:
                index += 1
                continue
            if index + 1 >= len(lines):
                self.error(path, f"table {first_header} has no separator row")
                break
            separator = split_markdown_row(lines[index + 1])
            if separator is None or len(separator) != len(headers) or not is_separator_row(separator):
                self.error(path, f"table {first_header} has malformed separator/header width")
                index += 1
                continue
            rows: list[dict[str, str]] = []
            cursor = index + 2
            while cursor < len(lines) and lines[cursor].lstrip().startswith("|"):
                cells = split_markdown_row(lines[cursor])
                if cells is None or len(cells) != len(headers):
                    width = len(cells) if cells is not None else 0
                    self.error(path, f"malformed {first_header} table row at line {cursor + 1}: expected {len(headers)} cells, got {width}; escape literal pipes as \\|")
                else:
                    rows.append(dict(zip(headers, cells)))
                cursor += 1
            tables.append((headers, rows))
            index = cursor
        return tables

    def check_workboard(self, path: Path) -> None:
        text = path.read_text(encoding="utf-8")
        tables = self.parse_tables(path, text, "ID")
        if len(tables) != 1:
            self.error(path, f"WORKBOARD must contain exactly one ID table; found {len(tables)}")
            return
        headers, rows = tables[0]
        if tuple(headers) != WORKBOARD_HEADERS:
            self.error(path, f"WORKBOARD columns must be exactly: {', '.join(WORKBOARD_HEADERS)}")
            return
        allowed = set(self.manifest.get("statuses", {}).get("work_item", []))
        modes = set(self.manifest.get("action_modes", {}))
        seen: set[str] = set()
        for row in rows:
            item_id = row["ID"]
            if not re.fullmatch(r"W-[A-Z0-9-]+", item_id):
                self.error(path, f"invalid work item id: {item_id}")
                continue
            if item_id in seen:
                self.error(path, f"duplicate work item id: {item_id}")
            seen.add(item_id)
            status = row["状态"]
            if status not in allowed:
                self.error(path, f"{item_id} has invalid work item status: {status}")
            if row["Mode"] not in modes:
                self.error(path, f"{item_id} has invalid action mode: {row['Mode']}")
            if status in {"CLAIMED", "IN_PROGRESS"}:
                for field in ("Owner", "Base revision", "写入范围", "Claimed at", "Lease until"):
                    if not row[field]:
                        self.error(path, f"active {item_id} missing {field}")
            if status == "DONE" and not row["Result revision / Notes"]:
                self.error(path, f"DONE {item_id} missing result revision/notes")

    def check_open_questions(self, path: Path) -> None:
        text = path.read_text(encoding="utf-8")
        tables = self.parse_tables(path, text, "编号")
        question_tables = [(headers, rows) for headers, rows in tables if "问题" in headers]
        change_tables = [(headers, rows) for headers, rows in tables if "变更内容" in headers]
        if len(question_tables) != 1 or tuple(question_tables[0][0]) != QUESTION_HEADERS:
            self.error(path, "open-questions must contain exactly one current 8-column question table")
        if len(change_tables) != 1 or tuple(change_tables[0][0]) != CHANGE_HEADERS:
            self.error(path, "open-questions must contain exactly one current 8-column change table")
        if len(question_tables) == 1:
            allowed = set(self.manifest.get("statuses", {}).get("question", []))
            for row in question_tables[0][1]:
                if row["状态"] not in allowed and "/" not in row["状态"]:
                    self.error(path, f"{row['编号']} has invalid question status: {row['状态']}")
                if row["状态"] == "RESOLVED" and (not row["决定来源"] or not row["验证者"]):
                    self.error(path, f"RESOLVED {row['编号']} requires 决定来源 and 验证者")
        if len(change_tables) == 1:
            allowed = set(self.manifest.get("statuses", {}).get("change", []))
            for row in change_tables[0][1]:
                if row["状态"] not in allowed and "/" not in row["状态"]:
                    self.error(path, f"{row['编号']} has invalid change status: {row['状态']}")

    def check_state_principals(self, path: Path, template: bool) -> None:
        tables = self.parse_tables(path, path.read_text(encoding="utf-8"), "Principal")
        if len(tables) != 1:
            self.error(path, f"STATE must contain exactly one 项目批准者 table; found {len(tables)}")
            return
        headers, rows = tables[0]
        if tuple(headers) != ("Principal", "实际负责人/稳定 ID", "说明"):
            self.error(path, "项目批准者 columns are invalid")
            return
        values = {row["Principal"]: row["实际负责人/稳定 ID"] for row in rows}
        if set(values) != PROJECT_PRINCIPALS:
            self.error(path, f"项目批准者 must define exactly: {', '.join(sorted(PROJECT_PRINCIPALS))}")
        if not template:
            for principal, value in values.items():
                if not value or "<" in value:
                    self.error(path, f"project principal {principal} is unresolved")

    def check_project(self, name: str) -> None:
        project = ROOT / "projects" / name
        if not project.is_dir():
            self.error(project, f"project does not exist: {name}")
            return
        template = name == "_template"
        for required in ("STATE.md", "WORKBOARD.md", "open-questions.md"):
            if not (project / required).is_file():
                self.error(project, f"missing project control file: {required}")

        state = project / "STATE.md"
        if state.is_file():
            self.check_document(state, project_control=True)
            text = state.read_text(encoding="utf-8")
            profiles = self.manifest.get("workflow", {}).get("profiles", [])
            found = {profile for profile in profiles if re.search(rf"`{re.escape(profile)}`", text)}
            if not template and len(found) != 1:
                self.error(state, f"STATE must identify exactly one backticked workflow profile; found {sorted(found)}")
            elif not template:
                selected = next(iter(found))
                maturity = self.manifest.get("workflow", {}).get("profile_maturity", {}).get(selected)
                if maturity != "stable":
                    self.warn(state, f"workflow profile {selected} maturity is {maturity}; treat it as unproven and capture feedback")
            if "WORKBOARD.md" not in text:
                self.warn(state, "STATE does not point to WORKBOARD.md")
            self.check_state_principals(state, template)

        workboard = project / "WORKBOARD.md"
        if workboard.is_file():
            self.check_document(workboard, project_control=True)
            self.check_workboard(workboard)

        questions = project / "open-questions.md"
        if questions.is_file():
            self.check_open_questions(questions)

        for path in project.rglob("*.md"):
            if path.name not in {"STATE.md", "WORKBOARD.md"}:
                self.check_document(path)

    def run(self) -> int:
        self.check_manifest()
        if self.manifest:
            self.check_protocol()
            canonical_workboard = ROOT / "projects/_template/WORKBOARD.md"
            if not canonical_workboard.is_file():
                self.error(canonical_workboard, "canonical WORKBOARD template is missing")
            duplicate_workboard = ROOT / "team/templates/workboard.md"
            if duplicate_workboard.exists():
                self.error(duplicate_workboard, "duplicate WORKBOARD template; use projects/_template/WORKBOARD.md")
            for path in (ROOT / "team").glob("*.md"):
                self.check_document(path)
            for path in (ROOT / "team/templates").glob("*.md"):
                self.check_document(path)
            names = [self.project] if self.project else [
                path.name for path in (ROOT / "projects").iterdir()
                if path.is_dir() and path.name != "_template"
            ]
            for name in names:
                self.check_project(name)

        for finding in sorted(self.findings, key=lambda item: (item.severity, str(item.path), item.message)):
            try:
                shown = finding.path.relative_to(ROOT)
            except ValueError:
                shown = finding.path
            print(f"{finding.severity}: {shown}: {finding.message}")
        errors = sum(finding.severity == "ERROR" for finding in self.findings)
        warnings = sum(finding.severity == "WARNING" for finding in self.findings)
        print(f"summary: {errors} error(s), {warnings} warning(s)")
        return 1 if errors or (self.strict and warnings) else 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", help="validate one project workspace")
    parser.add_argument("--strict", action="store_true", help="treat warnings as failure")
    args = parser.parse_args()
    return Validator(args.project, args.strict).run()


if __name__ == "__main__":
    sys.exit(main())
