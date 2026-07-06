from constraintos.validation.provenance import derive_provenance_manifest_id


def test_derive_provenance_manifest_id_from_standard_validation_report_id() -> None:
    assert derive_provenance_manifest_id("VALIDATION-REPORT-0007") == "PROVENANCE-0007"


def test_derive_provenance_manifest_id_from_short_validation_id() -> None:
    assert derive_provenance_manifest_id("VALIDATION-0008") == "PROVENANCE-0008"


def test_derive_provenance_manifest_id_falls_back_when_validation_id_is_missing() -> None:
    assert derive_provenance_manifest_id(None) == "PROVENANCE-0001"
