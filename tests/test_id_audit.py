from pathlib import Path

from constraintos.id_audit import audit_ids, extract_ids


def test_extract_ids() -> None:
    data = {"artifact": {"id": "ART-0001"}, "other": {"id": "OTHER-0001"}}
    assert "ART-0001" in extract_ids(data)
    assert "OTHER-0001" in extract_ids(data)


def test_audit_ids_detects_duplicate(tmp_path: Path) -> None:
    examples = tmp_path / "examples"
    examples.mkdir()
    (examples / "one.yaml").write_text("thing:\n  id: DUP-0001\n", encoding="utf-8")
    (examples / "two.yaml").write_text("thing:\n  id: DUP-0001\n", encoding="utf-8")
    report = audit_ids(tmp_path)
    assert report["id_audit_report"]["status"] == "fail"
    assert report["id_audit_report"]["findings"] == 1
