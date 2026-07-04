from constraintos.atlas_builder import create_volume_completion_report, create_volume_plan, run_volume_dry_build


def sample_spec() -> dict:
    return {
        "artifact": {"id": "PLATE-0001", "title": "Test Plate", "type": "technical_plate", "version": "0.1"},
        "constraints": [
            {"id": "C-0001", "statement": "Must show V6", "severity": "blocker", "acceptance": "V6 visible", "validation_method": "review"}
        ],
    }


def test_create_volume_plan_orders_plates() -> None:
    plan = create_volume_plan(
        "VOLUME-0001",
        "Test Volume",
        [
            {"id": "PLATE-0002", "title": "Second", "specification_path": "second.yaml", "sequence": 2},
            {"id": "PLATE-0001", "title": "First", "specification_path": "first.yaml", "sequence": 1},
        ],
    )
    assert plan["plates"][0]["id"] == "PLATE-0001"
    assert plan["volume_plan"]["id"] == "VOLUME-0001"


def test_run_volume_dry_build_complete() -> None:
    plan = create_volume_plan("VOLUME-0001", "Test Volume", [{"id": "PLATE-0001", "title": "First", "specification_path": "first.yaml", "sequence": 1}])
    build = run_volume_dry_build(plan, {"PLATE-0001": sample_spec()})
    assert build["volume_build"]["status"] == "complete"
    assert build["summary"]["processed"] == 1


def test_run_volume_dry_build_blocks_missing_spec() -> None:
    plan = create_volume_plan("VOLUME-0001", "Test Volume", [{"id": "PLATE-0001", "title": "First", "specification_path": "first.yaml", "sequence": 1}])
    build = run_volume_dry_build(plan, {})
    assert build["volume_build"]["status"] == "blocked"
    assert build["summary"]["blocked"] == 1


def test_create_volume_completion_report() -> None:
    build = {"volume_build": {"id": "BUILD-VOLUME-0001", "volume_id": "VOLUME-0001", "status": "complete"}, "summary": {"blocked": 0}}
    report = create_volume_completion_report(build)
    assert report["recommendation"] == "proceed"
