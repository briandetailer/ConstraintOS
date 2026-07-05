from constraintos.integration_audit import audit_example_detection, create_ci_readiness_report, detect_integration_schema


def test_detect_phase_20_artifact() -> None:
    assert detect_integration_schema({"runtime_health_report": {}}) == "schemas/runtime-health-report.schema.json"


def test_detect_phase_21_artifact() -> None:
    assert detect_integration_schema({"environment_profile": {}}) == "schemas/environment-profile.schema.json"


def test_detect_phase_22_artifact() -> None:
    assert detect_integration_schema({"local_runtime_profile": {}}) == "schemas/local-runtime-profile.schema.json"


def test_audit_example_detection_passes() -> None:
    audit = audit_example_detection([
        {"runtime_health_report": {}},
        {"environment_profile": {}},
        {"local_deployment_checklist": {}},
    ])
    assert audit.status == "pass"
    assert audit.checked == 3


def test_audit_example_detection_fails_unknown() -> None:
    audit = audit_example_detection([{"unknown": {}}])
    assert audit.status == "fail"
    assert audit.missing == ["example-1"]


def test_ci_readiness_report() -> None:
    report = create_ci_readiness_report(
        {"integration_audit": {"status": "pass"}},
        {"integration_audit": {"status": "pass"}},
    )
    assert report["ci_readiness_report"]["status"] == "ready"
    assert report["recommendation"] == "run_ci"
