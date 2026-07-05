from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any

from constraintos.schema_registry import SCHEMA_REGISTRY, SPECIAL_SCHEMA_RULES


@dataclass
class ReferenceDocument:
    title: str
    body: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "reference_document": {
                "title": self.title,
                "created": date.today().isoformat(),
            },
            "body": self.body,
        }


def generate_schema_reference_markdown() -> str:
    lines = [
        "# ConstraintOS Schema Reference",
        "",
        f"Generated: {date.today().isoformat()}",
        "",
        "## Registered Schemas",
        "",
        "| Key | Schema Path | Record Type |",
        "| --- | --- | --- |",
    ]
    for registration in SCHEMA_REGISTRY:
        lines.append(f"| `{registration.key}` | `{registration.schema_path}` | `{registration.record_type}` |")
    lines.extend(["", "## Special Schema Rules", "", "| Required Keys | Schema Path | Record Type |", "| --- | --- | --- |"])
    for required_keys, schema_path, record_type in SPECIAL_SCHEMA_RULES:
        key_text = ", ".join(f"`{key}`" for key in required_keys)
        lines.append(f"| {key_text} | `{schema_path}` | `{record_type}` |")
    return "\n".join(lines) + "\n"


def generate_cli_reference_markdown() -> str:
    commands = [
        ("new-artifact", "Create a new artifact YAML record."),
        ("new-failure", "Create a new failure record."),
        ("new-compliance", "Create a compliance report scaffold."),
        ("new-patch", "Create a patch package from a validation report."),
        ("new-baseline", "Create a regression baseline."),
        ("validate", "Validate YAML artifacts against schemas and repository rules."),
        ("trace", "Emit traceability records as JSON."),
        ("registry", "Generate an artifact ID registry."),
        ("registry-report", "Generate the schema registry report."),
        ("registry-check", "Check that registered schemas exist."),
        ("id-audit", "Audit repository IDs for duplicates."),
        ("repo-inventory", "Generate repository inventory."),
        ("repo-health", "Generate repository health summary."),
        ("export-md", "Export an artifact YAML file to Markdown."),
        ("compile", "Compile a specification into renderer-facing instructions."),
    ]
    lines = ["# ConstraintOS CLI Reference", "", f"Generated: {date.today().isoformat()}", "", "## Commands", ""]
    for command, description in commands:
        lines.extend([f"### `{command}`", "", description, ""])
    return "\n".join(lines)


def generate_architecture_index_markdown() -> str:
    lines = [
        "# ConstraintOS Architecture Index",
        "",
        f"Generated: {date.today().isoformat()}",
        "",
        "## Core Subsystems",
        "",
        "- Vision and Product Charter",
        "- Engineering Standards Manual",
        "- Architecture Book",
        "- Constraint Specification Language",
        "- Compiler",
        "- Validation Engine",
        "- Schema Registry",
        "- Runtime",
        "- Worker System",
        "- Queue and Leasing",
        "- Observability",
        "- Local Runtime",
        "- Repository Introspection",
        "- ID Audit",
        "",
        "## Product Boundary",
        "",
        "ConstraintOS does not generate content. It governs production.",
    ]
    return "\n".join(lines) + "\n"
