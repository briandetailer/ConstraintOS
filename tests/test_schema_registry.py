from constraintos.schema_registry import detect_record_type, detect_schema, registry_report


def test_detect_registry_schema_for_phase_22_artifact() -> None:
    assert detect_schema({"local_runtime_profile": {}}) == "schemas/local-runtime-profile.schema.json"
    assert detect_record_type({"local_runtime_profile": {}}) == "local_runtime_profile"


def test_detect_registry_schema_for_phase_23_artifact() -> None:
    assert detect_schema({"ci_readiness_report": {}}) == "schemas/ci-readiness-report.schema.json"
    assert detect_record_type({"integration_audit": {}}) == "integration_audit"


def test_detect_render_specification_schema() -> None:
    assert detect_schema({"render_specification": {}}) == "schemas/render-specification.schema.json"
    assert detect_record_type({"render_specification": {}}) == "render_specification"


def test_detect_special_schema_rule() -> None:
    data = {"status": "ok", "service": "constraintos-api", "version": "1.0"}
    assert detect_schema(data) == "schemas/api-health.schema.json"
    assert detect_record_type(data) == "api_health_response"


def test_unknown_schema_returns_none() -> None:
    assert detect_schema({"unknown": {}}) is None
    assert detect_record_type({"unknown": {}}) is None


def test_registry_report() -> None:
    report = registry_report()
    assert report["schema_registry_report"]["registered"] > 40
    assert report["schema_registry_report"]["special_rules"] > 0
