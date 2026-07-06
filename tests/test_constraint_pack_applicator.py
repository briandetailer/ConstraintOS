from pathlib import Path

import pytest
import yaml

from constraintos.constraint_pack import apply_constraint_pack


RENDER_SPECIFICATION = Path("examples/render/lf4_engine_render_specification.yaml")
CONSTRAINT_PACK = Path("examples/constraint_packs/lf4_engine_constraint_pack.yaml")


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_apply_constraint_pack_adds_pack_reference_without_duplicates() -> None:
    render_specification = load_yaml(RENDER_SPECIFICATION)
    constraint_pack = load_yaml(CONSTRAINT_PACK)

    applied = apply_constraint_pack(render_specification, constraint_pack)
    applied_again = apply_constraint_pack(applied, constraint_pack)

    assert applied_again["constraint_packs"] == [
        {"id": "CPACK-0001", "version": "0.1", "title": "LF4 Engineering Atlas Constraint Pack"}
    ]


def test_apply_constraint_pack_preserves_existing_duplicate_constraints() -> None:
    render_specification = load_yaml(RENDER_SPECIFICATION)
    constraint_pack = load_yaml(CONSTRAINT_PACK)

    applied = apply_constraint_pack(render_specification, constraint_pack)

    assert [item["id"] for item in applied["requirements"]] == ["REQ-0001", "REQ-0002", "REQ-0003"]
    assert [item["id"] for item in applied["negative_constraints"]] == ["NEG-0001", "NEG-0002"]
    assert [item["id"] for item in applied["validation"]["gates"]] == ["GATE-0001", "GATE-0002", "GATE-0003"]


def test_apply_constraint_pack_does_not_mutate_inputs() -> None:
    render_specification = load_yaml(RENDER_SPECIFICATION)
    constraint_pack = load_yaml(CONSTRAINT_PACK)

    apply_constraint_pack(render_specification, constraint_pack)

    assert "constraint_packs" not in render_specification


def test_apply_constraint_pack_rejects_duplicate_requirement_with_different_content() -> None:
    render_specification = load_yaml(RENDER_SPECIFICATION)
    constraint_pack = load_yaml(CONSTRAINT_PACK)
    constraint_pack["requirements"][0]["statement"] = "Different requirement text."

    with pytest.raises(ValueError, match="duplicate requirements id has different content: REQ-0001"):
        apply_constraint_pack(render_specification, constraint_pack)


def test_apply_constraint_pack_rejects_duplicate_gate_with_different_content() -> None:
    render_specification = load_yaml(RENDER_SPECIFICATION)
    constraint_pack = load_yaml(CONSTRAINT_PACK)
    constraint_pack["validation"]["gates"][0]["name"] = "Different Gate"

    with pytest.raises(ValueError, match="duplicate validation.gates id has different content: GATE-0001"):
        apply_constraint_pack(render_specification, constraint_pack)


def test_apply_constraint_pack_rejects_duplicate_pack_reference_with_different_content() -> None:
    render_specification = load_yaml(RENDER_SPECIFICATION)
    render_specification["constraint_packs"] = [{"id": "CPACK-0001", "version": "9.9", "title": "Different"}]
    constraint_pack = load_yaml(CONSTRAINT_PACK)

    with pytest.raises(ValueError, match="duplicate constraint pack reference has different content: CPACK-0001"):
        apply_constraint_pack(render_specification, constraint_pack)
