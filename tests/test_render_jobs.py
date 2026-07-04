from constraintos.render_jobs import create_output_reference, create_render_job, run_dry_render_job, update_manifest_with_output


def test_create_render_job() -> None:
    job = create_render_job("RENDER-0001", "PLATE-0001", "dry-run", "Render instruction")
    data = job.to_dict()
    assert data["render_job"]["id"] == "RENDER-0001"
    assert data["render_job"]["status"] == "queued"
    assert data["instruction"] == "Render instruction"


def test_create_output_reference() -> None:
    output = create_output_reference("OUTPUT-PLATE-0001", "PLATE-0001", "dry-run", "dry-run://PLATE-0001", "text/plain")
    data = output.to_dict()
    assert data["output_reference"]["id"] == "OUTPUT-PLATE-0001"
    assert data["output_reference"]["uri"] == "dry-run://PLATE-0001"


def test_run_dry_render_job() -> None:
    job = create_render_job("RENDER-0001", "PLATE-0001", "dry-run", "Render instruction")
    result = run_dry_render_job(job)
    assert result["render_job"]["status"] == "dry_run"
    assert result["response"]["status"] == "dry_run"
    assert result["output"]["output_reference"]["renderer"] == "dry-run"


def test_update_manifest_with_output() -> None:
    manifest = {"outputs": []}
    output = create_output_reference("OUTPUT-PLATE-0001", "PLATE-0001", "dry-run", "dry-run://PLATE-0001").to_dict()
    updated = update_manifest_with_output(manifest, output)
    assert len(updated["outputs"]) == 1
