from constraintos.adapters import DryRunRendererAdapter, RenderRequest, RenderResponse, RendererProfile


def test_dry_run_adapter_prepare() -> None:
    adapter = DryRunRendererAdapter()
    request = adapter.prepare("Render this instruction", "PLATE-0001", {"source": "test"})
    assert isinstance(request, RenderRequest)
    assert request.renderer == "dry-run"
    assert request.artifact_id == "PLATE-0001"
    assert request.metadata["source"] == "test"


def test_dry_run_adapter_render() -> None:
    adapter = DryRunRendererAdapter()
    request = adapter.prepare("Render this instruction", "PLATE-0001")
    response = adapter.render(request)
    assert isinstance(response, RenderResponse)
    assert response.status == "dry_run"
    assert response.output_reference is None
    assert response.messages


def test_renderer_profile_contract() -> None:
    adapter = DryRunRendererAdapter()
    profile = adapter.profile
    assert isinstance(profile, RendererProfile)
    assert profile.name == "dry-run"
    assert "semantic" in profile.supported_constraint_types
