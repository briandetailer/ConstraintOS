from constraintos.repair_loop import create_build_plan, create_iteration_record, dry_run_repair_loop


def sample_spec() -> dict:
    return {
        "artifact": {"id": "PLATE-0001", "title": "Test", "type": "technical_plate", "version": "0.1"},
        "constraints": [
            {"id": "C-0001", "statement": "Must show V6", "severity": "blocker", "acceptance": "V6 visible", "validation_method": "review"}
        ],
    }


def test_create_build_plan() -> None:
    plan = create_build_plan("BUILD-0001", "PLATE-0001", max_iterations=2)
    assert plan["build_plan"]["id"] == "BUILD-0001"
    assert plan["build_plan"]["max_iterations"] == 2
    assert "compile" in plan["stages"]


def test_create_iteration_record() -> None:
    record = create_iteration_record(1, "compile", "complete", "PLATE-0001")
    assert record["iteration"] == 1
    assert record["stage"] == "compile"


def test_dry_run_repair_loop_with_passing_review() -> None:
    checklist = {
        "items": [
            {"constraint_id": "C-0001", "severity": "blocker", "reviewer_result": "pass"}
        ],
        "summary": {"total": 1, "reviewed": 1, "pass": 1, "fail": 0, "uncertain": 0},
    }
    result = dry_run_repair_loop(sample_spec(), review_checklist=checklist)
    assert result["status"] == "pass"
    assert result["final_gate"]["gate"] == "pass"


def test_dry_run_repair_loop_creates_patch_for_uncertain_validation() -> None:
    report = {
        "report": {"id": "VAL-0001"},
        "artifact": {"id": "PLATE-0001", "version": "0.1", "specification_id": "PLATE-0001"},
        "constraint_results": [
            {"constraint_id": "C-0001", "severity": "blocker", "result": "uncertain", "confidence": 0.4}
        ],
    }
    result = dry_run_repair_loop(sample_spec(), compliance_report=report)
    assert any(item["stage"] == "patch" for item in result["iterations"])
