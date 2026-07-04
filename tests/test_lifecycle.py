import pytest

from constraintos.lifecycle import LifecycleError, create_approval_record, create_manifest, transition_manifest


def test_create_manifest_starts_draft() -> None:
    manifest = create_manifest("MANIFEST-0001", "PLATE-0001", "technical_plate", "Test Plate")
    assert manifest["state"] == "draft"
    assert manifest["artifact"]["id"] == "PLATE-0001"


def test_valid_transition() -> None:
    manifest = create_manifest("MANIFEST-0001", "PLATE-0001", "technical_plate", "Test Plate")
    compiled = transition_manifest(manifest, "compiled", "compiled successfully")
    assert compiled["state"] == "compiled"
    assert compiled["history"][-1]["from"] == "draft"


def test_invalid_transition() -> None:
    manifest = create_manifest("MANIFEST-0001", "PLATE-0001", "technical_plate", "Test Plate")
    with pytest.raises(LifecycleError):
        transition_manifest(manifest, "published", "cannot skip states")


def test_create_approval_record() -> None:
    record = create_approval_record("APPROVAL-0001", "PLATE-0001", "0.1", "VAL-0001", "reviewer", "approved", "Approved for publication")
    assert record["approval"]["status"] == "approved"
    assert record["artifact"]["compliance_report_id"] == "VAL-0001"
