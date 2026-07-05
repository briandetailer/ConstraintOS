from constraintos.reference_docs import generate_architecture_index_markdown, generate_cli_reference_markdown, generate_schema_reference_markdown


def test_generate_schema_reference_markdown() -> None:
    text = generate_schema_reference_markdown()
    assert "ConstraintOS Schema Reference" in text
    assert "Registered Schemas" in text
    assert "failure" in text


def test_generate_cli_reference_markdown() -> None:
    text = generate_cli_reference_markdown()
    assert "ConstraintOS CLI Reference" in text
    assert "id-audit" in text
    assert "repo-health" in text


def test_generate_architecture_index_markdown() -> None:
    text = generate_architecture_index_markdown()
    assert "ConstraintOS Architecture Index" in text
    assert "governs production" in text
