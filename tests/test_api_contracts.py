from constraintos.api_contracts import create_api_catalog, create_api_error, create_service_boundary


def test_create_api_catalog() -> None:
    catalog = create_api_catalog()
    assert catalog["api_catalog"]["id"] == "API-CATALOG-0001"
    assert any(endpoint["path"] == "/compile" for endpoint in catalog["endpoints"])


def test_create_api_error() -> None:
    error = create_api_error("ERROR-0001", "VALIDATION_FAILED", "Validation failed", retryable=False)
    assert error["api_error"]["code"] == "VALIDATION_FAILED"
    assert error["api_error"]["retryable"] is False


def test_create_service_boundary() -> None:
    boundary = create_service_boundary("SERVICE-0001", "Kernel API", ["compile", "validate"], ["billing", "tenancy"])
    assert "compile" in boundary["owns"]
    assert "billing" in boundary["does_not_own"]
