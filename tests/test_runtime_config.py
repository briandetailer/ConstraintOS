from constraintos.runtime_config import FeatureFlags, RuntimeLimits, create_development_profile, create_production_profile, validate_runtime_safety


def test_create_development_profile() -> None:
    profile = create_development_profile()
    assert profile["environment_profile"]["mode"] == "development"


def test_create_production_profile() -> None:
    profile = create_production_profile()
    assert profile["environment_profile"]["mode"] == "production"


def test_runtime_limits_model() -> None:
    limits = RuntimeLimits("LIMITS-0001", max_concurrent_jobs=2).to_dict()
    assert limits["runtime_limits"]["max_concurrent_jobs"] == 2
    assert limits["runtime_limits"]["allow_live_renderers"] is False


def test_feature_flags_model() -> None:
    flags = FeatureFlags("FLAGS-0001", {"debug_mode": False}).to_dict()
    assert flags["flags"]["debug_mode"] is False


def test_runtime_safety_passes_for_development() -> None:
    result = validate_runtime_safety(create_development_profile(), RuntimeLimits("LIMITS-0001").to_dict(), FeatureFlags("FLAGS-0001", {"debug_mode": True}).to_dict())
    assert result["runtime_safety_check"]["status"] == "pass"


def test_runtime_safety_fails_for_production_debug() -> None:
    result = validate_runtime_safety(create_production_profile(), RuntimeLimits("LIMITS-0001").to_dict(), FeatureFlags("FLAGS-0001", {"debug_mode": True}).to_dict())
    assert result["runtime_safety_check"]["status"] == "fail"
